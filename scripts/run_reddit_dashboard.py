from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from dashboard.app import create_app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local Reddit reference dashboard.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8010, help="Port to bind (default: 8010)")
    parser.add_argument("--no-debug", action="store_true", help="Disable Flask debug mode and the auto-reloader")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    debug = not args.no_debug
    app = create_app()
    app.run(host=args.host, port=args.port, debug=debug)


if __name__ == "__main__":
    main()
