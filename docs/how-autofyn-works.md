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

Each round flows **explore → plan → select+rank → build ×(1–3) → review**:

1. **`math-explorer`** (explore) — reads `constants/<id>.md` (the canonical ledger with
   the current record upper/lower bounds and citation chain), digests the full papers
   behind those records, samples the existing approaches to see what was tried and how the
   last builds went, and reports the terrain: where the gap is exploitable, which bound is
   softer, what dead-ended, and relevant or analogous papers. It does **not** attempt the
   improvement and does **not** rank.
2. **`proof-outliner`** (plan) — assembles the round's candidate field (up to ~5): live
   approaches worth expanding plus new angles, each with its hard step named and a slug.
   Produces candidate skeletons, not a finished proof; it does **not** rank or register —
   it hands the field to the outline-reviewer.
3. **`outline-reviewer`** (review + selection) — the selection layer. Cuts the angles that
   can't beat the record or can't be certified, `register_approach`s the approved new ones
   (the gate — a cut angle never enters), **ranks the field** head-to-head with
   `update_ranking` (here, pre-build, several live angles sit side by side and the
   comparison has signal), and picks the **build set** of 1–3 to build in parallel.
4. **`proof-builder`** ×(1–3) (build) — one builder per approach in the build set, in
   parallel; each turns its assigned angle into a concrete improvement (a rigorous
   argument, an explicit construction, or a certificate checked with Bash) and writes the
   candidate plus its artifact into `constants/<id>/`.
5. **`proof-reviewer`** (review) — adversarially verifies each built approach: re-runs the
   certificate, independently re-derives the key inequality, confirms the new bound beats
   the table value, assigns a verification level, and returns **APPROVE / CHANGES REQUESTED
   / RETHINK** per approach. It calls `record_outcome` once per built approach (marking each
   `stale`); next round's outline-reviewer folds those outcomes into the ranking. It does
   **not** rank.

## Why this works for math

- **Machine-checked where possible.** The loop prefers **Lean-fit** constants — those
  whose load-bearing step is finite/discrete/algebraic — and certifies them with a Lean
  proof that `lake build` type-checks. "Valid" then means the kernel accepts it, not that a
  reviewer spotted no hole. Analysis-heavy (Lean-hostile) bounds stay directed-rounded
  numerical certificates with adversarial review.
- **No fake solves.** A bound counts only when `proof-reviewer` reproduces the check —
  `lake build` clean (no `sorry`/axiom) for a Lean proof, or an independent re-derivation +
  re-run for a numerical certificate. The orchestrator can't self-approve.
- **Dense signal — the approach ranking.** Progress isn't a sparse "did we beat the record"
  count; it's the state of the approach population, which moves every productive round. A
  verified advance lifts an angle's Elo, a refuted one sinks, the held bound tightens — so
  the orchestrator can see the search sharpening even between record-breaks. The signal is
  honest because the lift comes only from an advance the `proof-reviewer` verified, never a
  builder's claim. Ranking sits at the outline-reviewer, which sees
  the whole candidate field at once and folds in the prior round's recorded outcomes — so
  approaches are scored against each other where the comparison has signal, not on one
  agent's isolated say-so.

The result of a successful run is a PR: an improved bound with a re-runnable certificate
and an updated ledger.
