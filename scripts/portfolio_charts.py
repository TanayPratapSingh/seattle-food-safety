"""Draw the README charts from the outputs saved in the executed notebook.

    python scripts/portfolio_charts.py [output dir]

The dataset is not in this repository, so nothing is recomputed. Every bar and
point is parsed from a cell output the notebook printed when it ran, and the
script stops if a cell no longer holds the code it expects.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BG, BLUE, BEIGE, GRAY, INK = "#FCFBF9", "#2F78D4", "#DCD8D0", "#6B6B70", "#1C1C1E"
NOTEBOOK = Path(__file__).resolve().parent.parent / "tanay_singh_reglab_takehome.ipynb"
GROUPS = ("Neither", "Asian", "Other ethnic")


def output(cells: list, index: int, marker: str) -> str:
    """All text a code cell printed or displayed, after checking it is the cell we mean."""
    cell = cells[index]
    assert marker in "".join(cell["source"]), f"cell {index} no longer contains {marker!r}"
    parts = []
    for o in cell["outputs"]:
        parts.append("".join(o.get("text") or o.get("data", {}).get("text/plain", "")))
    return "\n".join(parts)


def label_matches(cells: list) -> dict:
    """Share of back to back pairs whose "previous score" equals the file's earlier score (cell 22)."""
    text = output(cells, 22, 'pairs["matches"]')
    found = {m[1]: (float(m[2]), int(m[3]))
             for m in re.finditer(r"^(Asian|Neither|Other ethnic)\s+([\d.]+)\s+(\d+)$", text, re.M)}
    assert set(found) == set(GROUPS), found
    return found


def style(ax) -> None:
    ax.set_facecolor(BG)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(BEIGE)
    ax.tick_params(colors=GRAY, labelsize=13, length=0)


def save(fig, out: Path) -> None:
    fig.tight_layout()
    fig.savefig(out, facecolor=BG)
    plt.close(fig)


def draw_matches(m: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(16, 5.2), dpi=100)
    fig.patch.set_facecolor(BG)
    style(ax)
    for i, g in enumerate(reversed(GROUPS)):
        share, pairs = m[g]
        ax.barh(i, 1, color=BEIGE, height=0.58)
        ax.barh(i, share, color=BLUE if g == "Neither" else GRAY, height=0.58)
        ax.text(1.015, i, f"{pairs:,} pairs", va="center", fontsize=13, color=GRAY)
        inside = share > 0.15
        ax.text(share - 0.012 if inside else share + 0.012, i, f"{100 * share:.1f}%", va="center",
                ha="right" if inside else "left", fontsize=15, color="white" if inside else INK, fontweight="bold")
    ax.set_yticks(range(len(GROUPS)), [f"{g} restaurants" for g in reversed(GROUPS)], fontsize=15, color=INK)
    ax.set_xlim(0, 1.15)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"])
    ax.set_title("How often the \"previous score\" column equals the score the same file records for that earlier inspection\n"
                 "(back to back inspection periods only; bookkeeping like this should not depend on the kind of restaurant)",
                 loc="left", fontsize=16, color=INK, pad=14)
    save(fig, out)


if __name__ == "__main__":
    dest = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "figures")
    dest.mkdir(parents=True, exist_ok=True)
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    draw_matches(label_matches(cells), dest / "labels_disagree.png")
    print(f"wrote the charts to {dest}")
