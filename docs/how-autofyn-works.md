# How AutoFyn runs this repo

This repo uses [AutoFyn](https://github.com/SignalPilot-Labs/AutoFyn) to improve known
bounds on optimization constants. AutoFyn normally ships a software-engineering team of
subagents; here `.autofyn/subagents.json` **replaces** it with a proof-research pipeline.
This doc explains that pipeline — not AutoFyn in general.

## The round loop

AutoFyn runs in **rounds**. Each round is one fresh Claude session in a sandboxed
container, driven by an *orchestrator* that routes work but never explores, plans, or
proves itself. A round's context is discarded at the end; the only thing that survives is
on disk. So state lives in files, not in a growing context window:

- `/tmp/memory/run_state.md` — the **goal** (a constant + the value to beat), the
  **eval history** (per-round bound deltas), and **learned rules**.
- `/tmp/memory/<agent>.md` — per-subagent rules accumulated across rounds.
- `constants/<id>/` — the durable research folder: `current.md`, literature digests,
  every approach tried (and why it stalled), and certificate code.

The orchestrator reads `run_state.md` first, picks the highest-value next step toward the
goal, and dispatches subagents by **phase**.

## The phases (this repo's subagents)

Each round flows **explore → plan → review → build → review**:

1. **`math-explorer`** (explore) — reads `constants/<id>.md` (the canonical ledger with
   the current record upper/lower bounds and citation chain), digests the full papers
   behind those records, and reports where the gap is most exploitable and which bound is
   softer. It does **not** attempt the improvement.
2. **`proof-outliner`** (plan) — surveys multiple attack angles (analytic argument,
   explicit construction, computational certificate), ranks them, and flags the hard
   steps. Produces candidate skeletons, not a finished proof.
3. **`outline-reviewer`** (review) — checks an outline *before* details are filled in:
   wrong technique, unjustified leaps, missing cases, circular reasoning. Runs on any
   outline marked "Spec review: required."
4. **`proof-builder`** (build) — turns a chosen angle into a concrete improvement: a
   rigorous argument, an explicit construction, or a certificate built and checked with
   Bash. Writes the candidate plus its verification artifact into `constants/<id>/`.
5. **`proof-reviewer`** (review) — adversarially verifies: re-runs the certificate,
   independently re-derives the key inequality, confirms the new bound actually beats the
   table value, assigns a verification level, and returns **APPROVE / CHANGES REQUESTED /
   RETHINK**.

## Why this works for math

- **No fake solves.** The bound only counts when `proof-reviewer` independently
  re-derives it and re-runs the certificate — the orchestrator can't self-approve.
- **Dense reward.** Every round ends with a real eval: does the certified value beat the
  number in `constants/<id>.md`? The delta is logged to eval history.
- **Learning from failures.** Reviewer findings and dead ends become persistent Rules, so
  later rounds don't repeat a stalled angle.

The result of a successful run is a PR: an improved bound with a re-runnable certificate
and an updated ledger.
