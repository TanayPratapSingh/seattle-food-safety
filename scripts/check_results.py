"""Check that every number in RESULTS.md was printed by the notebook cell it cites.

    python scripts/check_results.py

Each table row in RESULTS.md ends with a quoted snippet and a cell, like
`Neither 0.951 5709` and In [10]. The snippet must appear in that cell's saved
output, with runs of whitespace collapsed so table alignment does not matter.
Standard library only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROW = re.compile(r"^\|.*\| `(.+?)` \| In \[(\d+)\] \|$")


def squash(text: str) -> str:
    return " ".join(text.split())


def outputs(notebook: Path) -> dict[int, str]:
    found = {}
    for cell in json.loads(notebook.read_text())["cells"]:
        if cell["cell_type"] == "code":
            parts = ["".join(o.get("text") or o.get("data", {}).get("text/plain", "")) for o in cell["outputs"]]
            found[cell["execution_count"]] = squash(" ".join(parts))
    return found


def main() -> int:
    printed = outputs(ROOT / "tanay_singh_reglab_takehome.ipynb")
    rows = [ROW.match(line) for line in (ROOT / "RESULTS.md").read_text().splitlines()]
    rows = [r for r in rows if r]
    missing = [(r[1], int(r[2])) for r in rows if squash(r[1]) not in printed.get(int(r[2]), "")]
    for snippet, cell in missing:
        print(f"not in the output of In [{cell}]: {snippet}")
    print(f"{len(rows) - len(missing)} of {len(rows)} numbers found in their cells")
    return 1 if missing or not rows else 0


if __name__ == "__main__":
    sys.exit(main())
