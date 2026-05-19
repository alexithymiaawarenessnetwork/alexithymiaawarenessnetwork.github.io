from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from dashboard.app import create_app


def main() -> None:
    app = create_app()
    app.run(host="127.0.0.1", port=8010, debug=True)


if __name__ == "__main__":
    main()
