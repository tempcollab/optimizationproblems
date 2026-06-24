"""MCP server: persistent Elo ranking over per-constant proof-approach artifacts.

Context-space expert iteration needs a *selection* layer over the population of
attack angles a constant accumulates across rounds. The approach bodies stay
free-form markdown the builder authors (`constants/<id>/approaches/<slug>.md`);
this server owns ONLY the structured ranking metadata for those approaches, in a
sidecar `constants/<id>/approaches/.ranking.json`. Subagents never hand-edit the
metadata — they go through these tools, so the fields the sampler sorts on can't
drift or be corrupted at 50+ approaches over a 24h run.

Four tools:
  - sample_approaches  (math-explorer, proof-outliner) — P-UCB over metadata,
    returns a small candidate set so the caller reads only k bodies, not all of
    them. The explorer samples to report the terrain; the outliner samples to
    assemble the candidate field. Neither ranks — the outline-reviewer does.
  - register_approach  (outline-reviewer) — the gate: seed an approved new angle
    at the cold-start Elo; a rejected angle is never registered.
  - record_outcome     (proof-reviewer) — record what happened to each approach
    built this round: bumps `expanded`, writes the outcome+note, sets `stale=true`.
  - update_ranking     (outline-reviewer) — fold the round's pairwise comparisons
    over the candidate field into Elo and clear `stale`. Ranking sits here because
    the outline-reviewer sees the whole field side by side, pre-build, where the
    comparison has signal; it also picks up the `stale` outcomes the proof-reviewer
    recorded last round.

Elo: 1500 start, K=32, soft floor — a dead-ended approach loses rating and, with
a high `expanded` count, is naturally de-prioritised by P-UCB; it is never hard
-retired, so a good-but-unlucky angle can revive if its siblings die off.
"""

import json
import math
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Constants — one source of truth (no magic values inline).
# ---------------------------------------------------------------------------
CONSTANTS_DIR_NAME = "constants"
APPROACHES_DIR_NAME = "approaches"
RANKING_FILE_NAME = ".ranking.json"

ELO_INITIAL = 1500.0
ELO_K_FACTOR = 32.0
ELO_FLOOR = 1000.0  # soft floor — rating cannot drop below this, never removed

# P-UCB: exploit(elo, scaled) + C * sqrt(ln(total_expanded + 1) / (1 + expanded))
PUCB_EXPLORATION_C = 0.5
PUCB_ELO_SCALE = 400.0  # divides Elo deviation from initial into the exploit term

OUTCOME_VALUES = ("advanced", "partial", "dead-end", "verified-milestone")

# The repo root is two levels up from this file: <repo>/.autofyn/approach_ranker.py
REPO_ROOT = Path(__file__).resolve().parent.parent

mcp = FastMCP("approach-ranker")


# ---------------------------------------------------------------------------
# Persistence helpers — the sidecar metadata store.
# ---------------------------------------------------------------------------
def _ranking_path(constant_id: str) -> Path:
    """Return the sidecar metadata file path for a constant, creating dirs."""
    approaches_dir = REPO_ROOT / CONSTANTS_DIR_NAME / constant_id / APPROACHES_DIR_NAME
    approaches_dir.mkdir(parents=True, exist_ok=True)
    return approaches_dir / RANKING_FILE_NAME


def _load(constant_id: str) -> dict[str, dict]:
    """Load the metadata map {slug: record} for a constant. Empty if none yet."""
    path = _ranking_path(constant_id)
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _save(constant_id: str, data: dict[str, dict]) -> None:
    """Atomically persist the metadata map for a constant."""
    path = _ranking_path(constant_id)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True))
    tmp.replace(path)


def _new_record(slug: str, summary: str) -> dict:
    """Build a cold-start metadata record for a freshly registered approach."""
    return {
        "slug": slug,
        "summary": summary,
        "elo": ELO_INITIAL,
        "selected": 0,
        "expanded": 0,
        "stale": False,
        "last_outcome": None,
        "last_note": None,
        "last_round": None,
    }


def _view(constant_id: str, record: dict) -> dict:
    """The reading view of an approach: the body path plus the tool-owned ranking fields.

    The prose (the idea, the math, the gap) lives in the body at `path` and the agent
    Reads it there. The ranking state — score and the reviewer's last verdict — lives in
    the json, not the body, so it is returned explicitly here:
      - path           : repo-relative path to the approach body (Read it for the prose)
      - elo            : current rating (1500 = cold start)
      - expanded       : how many times a builder has actually built this angle
      - stale          : true if a reviewer outcome from last round is not yet in the elo
      - last_outcome   : the reviewer's last verdict — advanced|partial|dead-end|verified-milestone (null if never expanded)
      - reviewer_note  : the reviewer's one-line why for that outcome (null if never expanded)
      - last_round     : the round that outcome was recorded (null if never expanded)
    """
    rel = f"{CONSTANTS_DIR_NAME}/{constant_id}/{APPROACHES_DIR_NAME}/{record['slug']}.md"
    return {
        "slug": record["slug"],
        "path": rel,
        "elo": record["elo"],
        "expanded": record["expanded"],
        "stale": record["stale"],
        "last_outcome": record["last_outcome"],
        "reviewer_note": record["last_note"],
        "last_round": record["last_round"],
    }


# ---------------------------------------------------------------------------
# Elo / P-UCB math.
# ---------------------------------------------------------------------------
def _expected(rating_a: float, rating_b: float) -> float:
    """Standard logistic Elo expected score of A against B."""
    return 1.0 / (1.0 + math.pow(10.0, (rating_b - rating_a) / PUCB_ELO_SCALE))


def _apply_pair(records: dict[str, dict], winner: str, loser: str) -> None:
    """Apply one pairwise Elo update in place, respecting the soft floor."""
    rw, rl = records[winner]["elo"], records[loser]["elo"]
    ew = _expected(rw, rl)
    el = _expected(rl, rw)
    records[winner]["elo"] = max(ELO_FLOOR, rw + ELO_K_FACTOR * (1.0 - ew))
    records[loser]["elo"] = max(ELO_FLOOR, rl + ELO_K_FACTOR * (0.0 - el))


def _pucb_score(record: dict, total_expanded: int) -> float:
    """P-UCB selection score: exploit current Elo + explore under-expanded angles.

    The exploration term uses `expanded` (builder rounds spent on this angle) for
    BOTH the per-arm count and the global clock `total_expanded` — one counter, as
    in standard P-UCB. `selected` (sampling exposure) is deliberately NOT in the
    score: sampling is cheap (the explorer surveys the whole field every round) and
    carries no verdict, so it must not decay an angle's exploration bonus. The bonus
    decays only when a builder actually spends a round on the angle.
    """
    exploit = (record["elo"] - ELO_INITIAL) / PUCB_ELO_SCALE
    explore = PUCB_EXPLORATION_C * math.sqrt(
        math.log(total_expanded + 1.0) / (1.0 + record["expanded"])
    )
    return exploit + explore


# ---------------------------------------------------------------------------
# Tools.
# ---------------------------------------------------------------------------
@mcp.tool()
def sample_approaches(constant_id: str, k: int) -> dict:
    """Select the top-k approaches to consider this round (callers: math-explorer, proof-outliner).

    Reads only metadata — never approach bodies — so context stays flat regardless
    of how many approaches the constant has accumulated. Ranks by P-UCB (exploit
    high-Elo + explore under-expanded, both keyed on `expanded`), increments
    `selected` on the chosen ones as telemetry (sampling exposure is tracked but
    does not feed the score).

    Returns each chosen approach as {slug, path, elo, expanded, stale,
    last_outcome, reviewer_note, last_round}, best-first. Read the `path` for the
    body (what was tried, the gap); `last_outcome`/`reviewer_note` give the
    reviewer's last verdict without opening the body. `stale: true` flags an
    approach whose Elo predates an unprocessed outcome — a priority to re-rank.
    """
    records = _load(constant_id)
    if not records:
        return {"constant_id": constant_id, "chosen": [], "total_approaches": 0}
    total_expanded = sum(r["expanded"] for r in records.values())
    ranked = sorted(
        records.values(),
        key=lambda r: _pucb_score(r, total_expanded),
        reverse=True,
    )
    chosen = ranked[: max(k, 1)]
    for record in chosen:
        records[record["slug"]]["selected"] += 1  # telemetry only — not in the score
    _save(constant_id, records)
    return {
        "constant_id": constant_id,
        "total_approaches": len(records),
        "chosen": [_view(constant_id, records[r["slug"]]) for r in chosen],
    }


@mcp.tool()
def register_approach(constant_id: str, slug: str, summary: str) -> dict:
    """Seed a new attack angle at the cold-start Elo (caller: outline-reviewer — the gate).

    Called by the outline-reviewer on an APPROVEd/CHANGES-REQUESTED new angle so it
    enters the population with a 1500 rating and zero counts; a RETHINK angle is never
    registered, so a rejected line cannot pollute the pool. The builder still authors
    the approach BODY in
    `constants/<id>/approaches/<slug>.md`; this only registers the ranking metadata.
    A slug that already exists is left untouched (its summary is refreshed).
    """
    records = _load(constant_id)
    if slug in records:
        records[slug]["summary"] = summary
        _save(constant_id, records)
        return {"constant_id": constant_id, "slug": slug, "created": False, "record": _view(constant_id, records[slug])}
    record = _new_record(slug, summary)
    records[slug] = record
    _save(constant_id, records)
    return {"constant_id": constant_id, "slug": slug, "created": True, "record": _view(constant_id, record)}


@mcp.tool()
def record_outcome(
    constant_id: str,
    slug: str,
    round_number: int,
    outcome: Literal["advanced", "partial", "dead-end", "verified-milestone"],
    note: str,
) -> dict:
    """Record what happened to one approach built this round (caller: proof-reviewer).

    Called once per built approach (builds may run in parallel). Bumps `expanded`,
    stamps the round, writes the categorical `outcome` plus a one-line `note` — the
    *why*, e.g. "SDP infeasible at level 2" — and sets `stale=true`. Next round,
    sample_approaches surfaces these as `last_outcome` and `reviewer_note`, and the
    outline-reviewer folds them into the ranking. The stale flag marks that this Elo
    predates the outcome. Does NOT change Elo — Elo only moves through update_ranking,
    from relative comparison.
    """
    if outcome not in OUTCOME_VALUES:
        raise ValueError(f"outcome must be one of {OUTCOME_VALUES}, got {outcome!r}")
    records = _load(constant_id)
    if slug not in records:
        raise KeyError(f"approach {slug!r} not registered for constant {constant_id!r}")
    record = records[slug]
    record["expanded"] += 1
    record["last_outcome"] = outcome
    record["last_note"] = note
    record["last_round"] = round_number
    record["stale"] = True
    _save(constant_id, records)
    return {"constant_id": constant_id, "slug": slug, "record": record}


@mcp.tool()
def update_ranking(constant_id: str, comparisons: list[dict]) -> dict:
    """Fold pairwise comparisons into Elo and clear stale flags (caller: outline-reviewer).

    Called once per round by the outline-reviewer when it ranks the candidate field
    head-to-head, anchored to each approach's last recorded outcome. Each comparison
    is {"winner": <slug>, "loser": <slug>};
    a draw is {"winner": <slug>, "loser": <slug>, "draw": true}. Applies a K=32
    Elo update per pair (soft floor 1000), then clears `stale` on every approach
    that appeared in any comparison — its outcome is now reflected in the rating.

    Returns the updated records for every approach touched, best-first by Elo.
    """
    records = _load(constant_id)
    touched: set[str] = set()
    for pair in comparisons:
        winner, loser = pair["winner"], pair["loser"]
        if winner not in records:
            raise KeyError(f"approach {winner!r} not registered for constant {constant_id!r}")
        if loser not in records:
            raise KeyError(f"approach {loser!r} not registered for constant {constant_id!r}")
        if pair.get("draw"):
            _apply_pair(records, winner, loser)
            _apply_pair(records, loser, winner)  # symmetric → net pull toward parity
        else:
            _apply_pair(records, winner, loser)
        touched.update((winner, loser))
    for slug in touched:
        records[slug]["stale"] = False
    _save(constant_id, records)
    updated = sorted(
        (_view(constant_id, records[slug]) for slug in touched),
        key=lambda r: r["elo"],
        reverse=True,
    )
    return {"constant_id": constant_id, "updated": updated}


if __name__ == "__main__":
    mcp.run()
