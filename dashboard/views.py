from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urlencode


def format_timestamp(value: float | None) -> str:
    if value is None:
        return "unknown"
    return datetime.fromtimestamp(value, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def summarize_text(text: str | None, limit: int = 240) -> str:
    if not text:
        return ""
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def selection_query(source_ids: list[str], **extra: object) -> str:
    pairs: list[tuple[str, str]] = [("source_id", source_id) for source_id in source_ids]
    for key, value in extra.items():
        if value is None:
            continue
        pairs.append((key, str(value)))
    return urlencode(pairs)
