#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile

NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


@dataclass(frozen=True)
class ExportSpec:
    slug: str
    label: str
    sheet: str
    column: str
    group: str
    kind: str = "column_values"
    term_column: str = "A"


DIRECT_SHEET_EXPORTS: list[ExportSpec] = [
    ExportSpec(
        slug="emotion-list",
        label="Emotion list",
        sheet="Emotion list",
        column="A",
        group="root",
    ),
    ExportSpec(
        slug="teachworth-feelings",
        label="Teachworth Feelings",
        sheet="Teachworth Feelings",
        column="A",
        group="root",
    ),
    ExportSpec(
        slug="spinoza-emotions",
        label="Spinoza Emotions",
        sheet="Spinoza Emotions",
        column="A",
        group="root",
    ),
    ExportSpec(
        slug="synthia-andrews",
        label="Synthia Andrews",
        sheet="Synthia Andrews",
        column="A",
        group="root",
    ),
    ExportSpec(
        slug="brene-brown-atlas-terms",
        label="Brene Brown Atlas terms",
        sheet="Brene Brown Atlas terms",
        column="B",
        group="root",
    ),
]

FIRST_SHEET_COLUMN_EXPORTS: list[ExportSpec] = [
    ExportSpec(
        slug="emotion-vocabulary-bundles",
        label="Emotion Vocabulary",
        sheet="Emotion list",
        column="AN",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="plutchik-family",
        label="Plutchik Family",
        sheet="Emotion list",
        column="H",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="plutchik-combinations",
        label="Plutchik combination",
        sheet="Emotion list",
        column="K",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="plutchik-dyads",
        label="Plutchik Dyad",
        sheet="Emotion list",
        column="L",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="gloria-wilcox",
        label="Gloria Wilcox",
        sheet="Emotion list",
        column="M",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="wilcox-emotion-wheel-secondary",
        label="Wilcox emotion wheel secondary",
        sheet="Emotion list",
        column="N",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="wilcox-family",
        label="Wilcox family",
        sheet="Emotion list",
        column="O",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="rando-wheel",
        label="Rando Wheel",
        sheet="Emotion list",
        column="P",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="rando-spectrum",
        label="Rando Spectrum",
        sheet="Emotion list",
        column="Q",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="humaine",
        label="HUMAINE",
        sheet="Emotion list",
        column="T",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="parrot-primary",
        label="Parrot Primary",
        sheet="Emotion list",
        column="W",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="parrot-secondary",
        label="Parrot Secondary",
        sheet="Emotion list",
        column="X",
        group="first-sheet-columns",
    ),
    ExportSpec(
        slug="mit-axis",
        label="MIT Axis",
        sheet="Emotion list",
        column="AA",
        group="first-sheet-columns",
    ),
]

FIRST_SHEET_MEMBERSHIP_EXPORTS: list[ExportSpec] = [
    ExportSpec(
        slug="gaslighting-list-terms",
        label="Gaslighting list terms",
        sheet="Emotion list",
        column="AE",
        group="first-sheet-memberships",
        kind="membership_terms",
    ),
    ExportSpec(
        slug="spinoza-terms-from-emotion-list",
        label="Spinoza terms from Emotion list",
        sheet="Emotion list",
        column="AP",
        group="first-sheet-memberships",
        kind="membership_terms",
    ),
    ExportSpec(
        slug="synthia-andrews-terms-from-emotion-list",
        label="Synthia Andrews terms from Emotion list",
        sheet="Emotion list",
        column="AQ",
        group="first-sheet-memberships",
        kind="membership_terms",
    ),
]

ALL_EXPORTS: list[ExportSpec] = (
    DIRECT_SHEET_EXPORTS + FIRST_SHEET_COLUMN_EXPORTS + FIRST_SHEET_MEMBERSHIP_EXPORTS
)


@dataclass(frozen=True)
class ExportMetadata:
    slug: str
    label: str
    group: str
    kind: str
    sheet: str
    column: str
    term_column: str | None
    raw_row_count: int
    term_count: int
    output_file: str

    def to_manifest_dict(self) -> dict[str, object]:
        return {
            "slug": self.slug,
            "label": self.label,
            "group": self.group,
            "kind": self.kind,
            "sheet": self.sheet,
            "column": self.column,
            "term_column": self.term_column,
            "raw_row_count": self.raw_row_count,
            "term_count": self.term_count,
            "output_file": self.output_file,
        }


def split_cell_ref(cell_ref: str) -> tuple[str, int]:
    match = re.fullmatch(r"([A-Z]+)(\d+)", cell_ref)
    if not match:
        raise ValueError(f"Unsupported cell reference: {cell_ref!r}")
    return match.group(1), int(match.group(2))



def clean_text(raw_value: str) -> str:
    without_format_controls = "".join(
        ch for ch in str(raw_value) if unicodedata.category(ch) != "Cf"
    )
    return " ".join(without_format_controls.split()).strip()


class XlsxReader:
    def __init__(self, workbook_path: Path) -> None:
        self.workbook_path = workbook_path
        self.archive = ZipFile(workbook_path)
        self.shared_strings = self._load_shared_strings()
        self.sheet_targets = self._load_sheet_targets()
        self.sheet_cache: dict[str, list[dict[str, str]]] = {}

    def _load_shared_strings(self) -> list[str]:
        if "xl/sharedStrings.xml" not in self.archive.namelist():
            return []
        root = ET.fromstring(self.archive.read("xl/sharedStrings.xml"))
        values: list[str] = []
        for si in root.findall("main:si", NS):
            values.append("".join((t.text or "") for t in si.iterfind(".//main:t", NS)))
        return values

    def _load_sheet_targets(self) -> dict[str, str]:
        workbook_root = ET.fromstring(self.archive.read("xl/workbook.xml"))
        rel_root = ET.fromstring(self.archive.read("xl/_rels/workbook.xml.rels"))
        rels = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rel_root}
        targets: dict[str, str] = {}
        sheets_node = workbook_root.find("main:sheets", NS)
        if sheets_node is None:
            raise ValueError("Workbook is missing xl/workbook.xml sheets metadata")
        for sheet in sheets_node:
            rel_id = sheet.attrib[
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            ]
            target = rels[rel_id]
            if not target.startswith("xl/"):
                target = "xl/" + target.lstrip("/")
            targets[sheet.attrib["name"]] = target
        return targets

    def cell_value(self, cell: ET.Element) -> str | None:
        value_node = cell.find("main:v", NS)
        inline_node = cell.find("main:is", NS)
        cell_type = cell.attrib.get("t")
        if cell_type == "s" and value_node is not None and value_node.text is not None:
            return self.shared_strings[int(value_node.text)]
        if cell_type == "inlineStr" and inline_node is not None:
            return "".join((t.text or "") for t in inline_node.iterfind(".//main:t", NS))
        return value_node.text if value_node is not None else None

    def read_sheet_rows(self, sheet_name: str) -> list[dict[str, str]]:
        if sheet_name in self.sheet_cache:
            return self.sheet_cache[sheet_name]
        if sheet_name not in self.sheet_targets:
            raise KeyError(f"Sheet not found: {sheet_name}")
        root = ET.fromstring(self.archive.read(self.sheet_targets[sheet_name]))
        rows: list[dict[str, str]] = []
        for row in root.findall(".//main:sheetData/main:row", NS):
            cells: dict[str, str] = {}
            for cell in row.findall("main:c", NS):
                cell_ref = cell.attrib.get("r", "")
                column, _ = split_cell_ref(cell_ref)
                raw_value = self.cell_value(cell)
                if raw_value is None:
                    continue
                cleaned = clean_text(raw_value)
                if cleaned:
                    cells[column] = cleaned
            rows.append(cells)
        self.sheet_cache[sheet_name] = rows
        return rows

    def column_values(self, sheet_name: str, column: str) -> list[str]:
        rows = self.read_sheet_rows(sheet_name)
        return [row[column] for row in rows[1:] if column in row]

    def membership_terms(
        self, sheet_name: str, term_column: str, membership_column: str
    ) -> list[str]:
        rows = self.read_sheet_rows(sheet_name)
        values: list[str] = []
        for row in rows[1:]:
            if membership_column in row and term_column in row:
                values.append(row[term_column])
        return values

    def close(self) -> None:
        self.archive.close()



def unique_sorted_terms(raw_terms: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_terms: list[str] = []
    for term in raw_terms:
        key = term.casefold()
        if key in seen:
            continue
        seen.add(key)
        unique_terms.append(term)
    return sorted(unique_terms, key=lambda s: s.casefold())



def output_path_for_spec(lists_dir: Path, spec: ExportSpec) -> Path:
    if spec.group == "root":
        return lists_dir / f"{spec.slug}.txt"
    return lists_dir / spec.group / f"{spec.slug}.txt"



def manifest_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        try:
            return path.relative_to(repo_root.parent).as_posix()
        except ValueError:
            return str(path)


def extract_exports(
    workbook_path: Path,
    specs: list[ExportSpec],
    lists_dir: Path,
    repo_root: Path,
) -> tuple[dict[str, list[str]], list[ExportMetadata]]:
    reader = XlsxReader(workbook_path)
    try:
        exports: dict[str, list[str]] = {}
        metadata: list[ExportMetadata] = []
        for spec in specs:
            if spec.kind == "membership_terms":
                raw_values = reader.membership_terms(
                    spec.sheet, spec.term_column, spec.column
                )
                term_column: str | None = spec.term_column
            else:
                raw_values = reader.column_values(spec.sheet, spec.column)
                term_column = None
            sorted_terms = unique_sorted_terms(raw_values)
            output_path = output_path_for_spec(lists_dir, spec)
            exports[spec.slug] = sorted_terms
            metadata.append(
                ExportMetadata(
                    slug=spec.slug,
                    label=spec.label,
                    group=spec.group,
                    kind=spec.kind,
                    sheet=spec.sheet,
                    column=spec.column,
                    term_column=term_column,
                    raw_row_count=len(raw_values),
                    term_count=len(sorted_terms),
                    output_file=manifest_path(output_path, repo_root),
                )
            )
    finally:
        reader.close()
    return exports, metadata



def write_text_list(path: Path, terms: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(terms) + "\n", encoding="utf-8")



def write_manifest(
    path: Path,
    workbook_path: Path,
    combined_output: Path,
    lists_dir: Path,
    metadata: list[ExportMetadata],
    repo_root: Path,
) -> None:
    manifest = {
        "source_workbook": manifest_path(workbook_path, repo_root),
        "combined_output": manifest_path(combined_output, repo_root),
        "lists_directory": manifest_path(lists_dir, repo_root),
        "lists": [item.to_manifest_dict() for item in metadata],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")



def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description=(
            "Extract alphabetized emotion/feeling vocabularies from the existing "
            "Metagamist workbook into AAN text files."
        )
    )
    parser.add_argument(
        "--workbook",
        type=Path,
        default=repo_root.parent
        / "Metagamist"
        / "data"
        / "spreadsheets"
        / "Emotions and circuits.xlsx",
        help="Path to the source workbook (.xlsx)",
    )
    parser.add_argument(
        "--combined-output",
        type=Path,
        default=repo_root / "aan" / "data" / "emotion-terms.txt",
        help="Path for the merged alphabetized output text file",
    )
    parser.add_argument(
        "--lists-dir",
        type=Path,
        default=repo_root / "aan" / "data" / "emotion-vocabularies",
        help="Directory for per-list vocabulary text files",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=repo_root / "aan" / "data" / "emotion-vocabularies" / "manifest.json",
        help="Path for the per-list provenance manifest JSON",
    )
    return parser.parse_args()



def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    args = parse_args()
    workbook_path = Path(args.workbook).resolve()
    combined_output = Path(args.combined_output).resolve()
    lists_dir = Path(args.lists_dir).resolve()
    manifest_path = Path(args.manifest).resolve()

    if not workbook_path.exists():
        print(f"Workbook not found: {workbook_path}", file=sys.stderr)
        return 1

    exports, metadata = extract_exports(workbook_path, ALL_EXPORTS, lists_dir, repo_root)
    combined_specs = {spec.slug for spec in DIRECT_SHEET_EXPORTS}
    combined_terms = unique_sorted_terms(
        [
            term
            for slug, terms in exports.items()
            if slug in combined_specs
            for term in terms
        ]
    )

    write_text_list(combined_output, combined_terms)
    for item in metadata:
        slug = item.slug
        write_text_list(Path(item.output_file), exports[slug])
    write_manifest(manifest_path, workbook_path, combined_output, lists_dir, metadata, repo_root)

    print(f"Workbook: {workbook_path}")
    print(f"Combined output: {combined_output}")
    print(f"Per-list directory: {lists_dir}")
    print(f"Manifest: {manifest_path}")
    print("Lists written:")
    for item in metadata:
        extra = f"; term column={item.term_column}" if item.term_column else ""
        print(
            f"- {item.output_file} <- {item.sheet} [{item.column}] "
            f"kind={item.kind} group={item.group}{extra} | "
            f"raw rows={item.raw_row_count} | terms written={item.term_count}"
        )
    print(f"Merged unique terms written: {len(combined_terms)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
