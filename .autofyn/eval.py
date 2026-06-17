"""Progress eval for the bound-improvement loop.

The run's progress signal is the approach population, not a milestone count
(see CLAUDE.md, "Goal & eval"). This reads the population state for one constant
and prints a single progress line the orchestrator logs to Eval History each
round. It is the one source of truth for the eval command — round 1 points
`run_state.md`'s Concrete Target at `python .autofyn/eval.py <id>` once the
constant is chosen.

Reads, for the given constant id:
  - constants/<id>/approaches/.ranking.json  — the ranker sidecar (Elo, expanded,
    last_outcome per approach); top Elo and live-vs-dead counts.
  - constants/<id>/current.md                — the `## Bounds` line (held + record),
    to report the verified gap, and `## Status`.

Prints one line, e.g.:
  82a | held 0.2538893183 gap 5.144e-03 | approaches 6 (live 4, dead 2) top-elo 1572 | status none

Exit code is always 0 — this is a progress readout, not a pass/fail test.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEAD_OUTCOME = "dead-end"


def _ranking_summary(constant_id: str) -> str:
    """Top Elo and live-vs-dead counts from the ranker sidecar, or a cold-start note."""
    path = REPO_ROOT / "constants" / constant_id / "approaches" / ".ranking.json"
    if not path.exists():
        return "approaches 0 (no population yet)"
    records = json.loads(path.read_text())
    if not records:
        return "approaches 0 (no population yet)"
    elos = [r["elo"] for r in records.values()]
    dead = sum(1 for r in records.values() if r.get("last_outcome") == DEAD_OUTCOME)
    live = len(records) - dead
    return f"approaches {len(records)} (live {live}, dead {dead}) top-elo {max(elos):.0f}"


def _bounds_summary(constant_id: str) -> str:
    """The held bound, its gap to the record, and the improved/none status."""
    path = REPO_ROOT / "constants" / constant_id / "current.md"
    if not path.exists():
        return "held — gap — | status —"
    text = path.read_text()
    bounds = re.search(r"##\s*Bounds.*?held:\s*([0-9.eE+-]+)", text)
    record = re.search(r"##\s*Bounds.*?table:\s*([0-9.eE+-]+)", text)
    status = re.search(r"##\s*Status\s*[:\s]*([A-Za-z]+)", text)
    held_s = bounds.group(1) if bounds else "—"
    gap_s = "—"
    if bounds and record:
        try:
            gap_s = f"{abs(float(held_s) - float(record.group(1))):.3e}"
        except ValueError:
            pass
    return f"held {held_s} gap {gap_s} | status {status.group(1) if status else '—'}"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python .autofyn/eval.py <constant-id>", file=sys.stderr)
        return 0
    constant_id = sys.argv[1]
    print(f"{constant_id} | {_bounds_summary(constant_id)} | {_ranking_summary(constant_id)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
