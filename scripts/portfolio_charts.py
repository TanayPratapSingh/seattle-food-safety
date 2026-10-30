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
NOTEBOOK = Path(__file__).resolve().parent.parent / "seattle_food_safety.ipynb"
GROUPS = ("Neither", "Asian", "Other ethnic")
RANKINGS = ("Previous score", "Cuisine flag only", "Logistic regression", "Gradient boosting", "Review text")


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


def aucs(cells: list) -> dict:
    """Test AUC and its 95% interval for each ranking, overall and within Neither (cell 31)."""
    text = output(cells, 31, "auc_interval")
    names = "|".join(RANKINGS)
    rows = re.findall(rf"({names})\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\\?$", text, re.M)
    assert len(rows) == 2 * len(RANKINGS), rows
    out = {}
    for i, (name, auc, low, high) in enumerate(rows):
        out["All inspections" if i < len(RANKINGS) else "Neither only", name] = tuple(map(float, (auc, low, high)))
    return out


def visits(cells: list) -> dict:
    """Share of a 20% inspection budget each group receives under the two rules (cell 43)."""
    text = output(cells, 43, "per_group")
    out, rule = {}, None
    for line in text.splitlines():
        head = re.match(r"(riskiest 20% .*?): (\d+) visits, (\d+) serious found", line)
        if head:
            rule = head[1]
            out[rule] = {"visits": int(head[2]), "serious": int(head[3])}
            continue
        row = re.match(r"\s+(Asian|Neither|Other ethnic): ([\d.]+) of visits", line)
        if row:
            out[rule][row[1]] = float(row[2])
    assert len(out) == 2 and all(abs(sum(r[g] for g in GROUPS) - 1) < 0.002 for r in out.values()), out
    neither = re.search(r"Neither: ([\d.]+) of test rows, ([\d.]+) serious", output(cells, 29, "valid_p"))
    out["Neither in test"] = {"rows": float(neither[1]), "serious": float(neither[2])}
    return out


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


def draw_aucs(a: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(16, 6.2), dpi=100)
    fig.patch.set_facecolor(BG)
    style(ax)
    ax.grid(axis="x", color=BEIGE, linewidth=0.8)
    for subset, color, dy in (("All inspections", GRAY, 0.16), ("Neither only", BLUE, -0.16)):
        for i, name in enumerate(reversed(RANKINGS)):
            auc, low, high = a[subset, name]
            ax.plot([low, high], [i + dy] * 2, color=color, linewidth=3, solid_capstyle="round")
            ax.plot(auc, i + dy, "o", color=color, markersize=10, label=subset if i == 0 else None)
            ax.text(high + 0.008, i + dy, f"{auc:.3f}", va="center", fontsize=12.5, color=color)
    ax.axvline(0.5, color=GRAY, linewidth=1, linestyle=":")
    ax.set_yticks(range(len(RANKINGS)), list(reversed(RANKINGS)), fontsize=15, color=INK)
    ax.set_xlim(0.45, 0.95)
    ax.set_xlabel("test AUC, 2012 to February 2013 (0.5 is a coin flip); lines are 95% intervals from resampling whole restaurants",
                  fontsize=13, color=GRAY)
    ax.legend(frameon=False, fontsize=13, loc="center", bbox_to_anchor=(0.6, 0.62), labelcolor=INK)
    ax.set_title("Over all inspections the cuisine flag alone reaches most of the headline AUC.\n"
                 "Within Neither restaurants, where the records look sound, boosting edges the last score.",
                 loc="left", fontsize=16, color=INK, pad=14)
    save(fig, out)


def draw_visits(v: dict, out: Path) -> None:
    neither = v.pop("Neither in test")
    rules = list(v)
    colors = {"Asian": GRAY, "Other ethnic": BEIGE, "Neither": BLUE}
    fig, ax = plt.subplots(figsize=(16, 5.2), dpi=100)
    fig.patch.set_facecolor(BG)
    style(ax)
    for i, rule in enumerate(reversed(rules)):
        left = 0.0
        for g in ("Asian", "Other ethnic", "Neither"):
            share = v[rule][g]
            ax.barh(i, share, left=left, color=colors[g], height=0.58, label=g if i == 0 else None)
            if share > 0.06:
                ax.text(left + share / 2, i, f"{g}{chr(10) if share < 0.2 else ' '}{100 * share:.0f}%", va="center",
                        ha="center", fontsize=13.5,
                        color="white" if g != "Other ethnic" else INK, fontweight="bold")
            left += share
        ax.text(1.015, i, f"{v[rule]['visits']} visits,\n{v[rule]['serious']} serious found", va="center",
                fontsize=12.5, color=GRAY)
    ax.set_yticks(range(len(rules)), [r[0].upper() + r[1:] for r in reversed(rules)], fontsize=15, color=INK)
    ax.set_xlim(0, 1.16)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"])
    ax.set_title("Who gets the visits if the department can do 20% of test inspections, ranked by the boosting model\n"
                 f"(Neither restaurants are {100 * neither['rows']:.0f}% of test inspections and {100 * neither['serious']:.1f}% of theirs "
                 "are serious;\nranked overall, the model sends none of its visits there)",
                 loc="left", fontsize=16, color=INK, pad=14)
    save(fig, out)


if __name__ == "__main__":
    dest = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "figures")
    dest.mkdir(parents=True, exist_ok=True)
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    draw_matches(label_matches(cells), dest / "labels_disagree.png")
    draw_aucs(aucs(cells), dest / "auc_by_subset.png")
    draw_visits(visits(cells), dest / "who_gets_visits.png")
    print(f"wrote the charts to {dest}")
