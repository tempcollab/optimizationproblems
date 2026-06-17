# optimizationproblems — bound-improvement loop

This is Tao's registry of optimization constants. The [README](README.md) table is
the index of all the constants and their current best bounds; each
`constants/<id>.md` (e.g. `1a.md`, `42a.md`) is the ledger for one constant $C_{id}$
— its best known upper and lower bounds, with the citation chain to the papers that
achieved them. Almost none are known exactly; the gap between the bounds is the open
frontier. A few have been pinned exactly (e.g. 11b, 48 — equal bounds in the table).

**The goal is to improve a bound — by any valid means.** Take one constant and push
its upper bound down, or its lower bound up, past the value in its table. The bar is
just that: a valid bound that strictly beats the record, with a check the reviewer
can reproduce. Studying how the record was achieved and strengthening it is the usual
road, but not the only one — a new technique or a from-scratch construction is just
as welcome and is often where the biggest jumps come from. Don't anchor to the record
if you see a better road.

Moving a single bound is a real, paper-worthy result — these are the same constants
AlphaEvolve, ThetaEvolve, and others compete on.

## Prefer Lean-certifiable constants

**Prefer constants whose bound becomes a machine-checked Lean theorem** — a
`lake build`-passing proof is a stronger result than a hand-reviewed numerical certificate.
Fit is decided by the **shape of the load-bearing step**, not the field:

- **Lean-fit** (preferred, certificate is a `.lean` file) — the certifying step is finite,
  discrete, or algebraic: case enumeration, a divisibility/congruence argument, a
  construction whose validity is a polynomial identity or degree/coprimality condition, a
  counting bound, an inequality through `Mathlib`.
- **Lean-hostile** (numerical certificate, do not force Lean) — a continuum estimate:
  interval quadrature, SDP feasibility, a Mahler-measure integral (the 82a kind).

Triage on the step, not the label — some number theory is analysis-heavy, some "analysis"
constants have a discrete core. Between two equally promising constants, take the Lean-fit one.

## For the orchestrator

This is a research repo, not a code repo:

- **Setup: install the research toolchain, once (round 1).** No app to build — skip
  `npm ci` / `uv sync`. Install (no root; the sandbox persists, so this is paid once):
  - **PDF extractor:** `pip install --user pdfminer.six`; read a saved PDF with `pdf2txt.py`.
  - **Scientific Python:** `uv pip install --system numpy scipy` (add `cvxpy` / `sympy` per
    the angle).
  - **Lean** (the preferred certification path): install `elan` (→ `~/.elan`); create a
    `lean/` project at the repo root with the Mathlib `math` template if absent; **pin and
    commit** `lean/lean-toolchain` + the Mathlib rev in `lean/lake-manifest.json` (a floating
    version breaks later-round proofs); `lake exe cache get` then `lake build` to confirm. A
    constant's proof lives in the `lean/` tree (e.g. `lean/Constants/C<id>.lean`) so Lake
    builds it; `constants/<id>/certificate/` records its `lake build` target + `#print axioms`
    line.
  Installing is allowed and expected here — the "no installs" instinct doesn't apply
  to this repo. Beyond these, agents run numerical code and Lean proofs to build and
  check bounds; that's the work, not a build step.
- **Snapshot safety (repo-wide).** `/tmp/memory/` and the round dirs are archived as
  text each round; a stray binary there breaks the snapshot. Any binary an agent
  downloads (e.g. a paper PDF) goes under `constants/<id>/literature/pdfs/`, never into
  `/tmp/memory/` or a round dir. (How the explorer reads papers is in its prompt.)
- **One constant per run.** A run attacks exactly ONE constant `<id>`, chosen in
  round 1 and fixed for the whole run. All rounds push that one constant. Everything
  below — the metric, the eval, `current.md` — is about that single `<id>`.
- **Progress signal — the approach ranking, not a record-count.** Track the state of the
  approach population: Elo, which angles are live vs dead-ended, and the verified `held`
  bound's gap to the record. It moves every productive round (a verified advance lifts an
  Elo, a refuted one sinks) so it gives gradient between record-breaks. **Eval:**
  `python .autofyn/eval.py <id>`, written into `run_state.md` at the **end of round 1** once
  triage has fixed `<id>` (before that, `<id>` is unknown; the eval prints a cold-start
  baseline). An actual record-break is the headline event, flagged separately by
  `## Status: improved` in `current.md`.
- **Pick the most promising constant — tractable, not widest-gap.** Skip the closed
  (upper = lower, e.g. 11b) and the conjecture-hard (a movable side equivalent to a major
  open problem, e.g. de Bruijn–Newman ⇔ RH); prefer the Lean-fit. The explorer triages in
  round 1.
- **One folder per problem.** All work for a constant lives in `constants/<id>/`. Edit the
  canonical `constants/<id>.md` record only once an improvement is verified.
- **Scope each round small — one verifiable increment, not the whole bound.** A round's
  build is a single step that finishes and verifies this round: one lemma/`sorry`
  discharged, one gap closed, one tightening. If an angle is really a large construction,
  dispatch only its first sub-goal and carry the rest forward. (The repo's reading of the
  engine's "one large task or ≤3 small": ≤3 *small certified* steps.)
- **Dispatch counts — not one-agent-per-phase.**
  `math-explorer ×1 → proof-outliner ×1 → outline-reviewer ×1 → proof-builder ×(1–3) →
  proof-reviewer ×1`. The builders fan out **one per build-set slug, in parallel**; **one
  proof-reviewer reviews all of them** (not one per build). In-phase fan-out (the outliner's
  ~5-approach sampling, the outline-reviewer's ranking) is the subagent's own job — you don't
  manage it.
- **Build set.** The outline-reviewer's report ends with `build set: <slug>[, <slug>...]` —
  dispatch **exactly one proof-builder per slug, no more, no fewer**, each told its slug.
- **Route per approach (overrides the engine's whole-round "all APPROVE" gate).** One verdict
  per built slug, routed independently:
  - **APPROVE** — terminal for the round: recorded by the reviewer, not rebuilt. It neither
    holds the round open nor sends siblings back.
  - **CHANGES REQUESTED** — re-dispatch only that slug's builder (this round or next; its
    approach stays live either way).
  - **RETHINK** — that slug's angle goes back to the outliner; the others are unaffected.
  A mixed result is normal, not a failed round. End once every slug is routed.

## Workflow

Each run picks **one** constant and loops (each agent's job is in its own prompt; routing
in the orchestrator bullets above):

**math-explorer → proof-outliner → outline-reviewer → proof-builder ×(1–3) → proof-reviewer**

The **outline-reviewer always runs** — it is the ranking hub + gate + build-set emitter, not
the engine's skippable "plan review". Each round starts fresh with no memory; `constants/<id>/`
(and the approach docs) is how the next round knows what was tried and resumes it.

## The `constants/<id>/` folder

A constant's workspace holds: `literature/` (paper digests), `approaches/<slug>.md` (one
living doc per angle — idea, status, how to push it), `certificate/` (the artifacts), and
`current.md` (the verified bottom line). Approach bodies are free-form; their ranking
metadata (Elo, counts, stale, last outcome) lives in the tool-owned sidecar
`approaches/.ranking.json` — never hand-edited, only the ranking tools (served by
`.autofyn/approach_ranker.py`) touch it.

### `current.md` — the tracking file (contract)

The tracking file for the run's constant. The eval reads `## Bounds` (the verified `held`
and its gap to the record) from here, alongside the population state in the ranker sidecar.
It MUST contain these sections:

```
## Status            improved | none   (only the reviewer sets `improved`)
## Bounds            table: <record to beat> · held: <best value WE have verified>
## Progress log      - R<round>: <one-line verified advance>   (reviewer-appended)
```

`held` is the reviewer-verified value, never the builder's unverified claim (a
numerical-search result is a conjecture — it goes in an approach doc, not `held`). The
`## Progress log` is the human-readable trail of what each round verified — not the metric
(the ranking is the signal); only the reviewer appends to it, and only for a verified
advance.

## Rigor rules

The reviewer enforces these:

- **Beat the best *verified* value, exactly.** State the current value and the new
  value. The bar is the best **verified** bound — a starred / "unverified" entry is
  NOT the value to beat (e.g. on 31a the bar is the verified 0.792665992, not an
  unverified 0.79970). An "improvement" that doesn't strictly beat the best verified
  bound isn't one.
- **Reconcile the README against the file; use whichever is better.** The README
  table and `constants/<id>.md` can disagree (a PR may have tightened one past the
  other). Check both, and treat the genuinely best verified bound as the value to
  beat.
- **The check must be reproducible.** A bound is only as good as the check the reviewer
  can re-run; one that can't be reproduced isn't established. For a **Lean-fit** bound the
  check is `lake build` on the proof — type-checking *is* the reproduction, and it is the
  gold standard: a bound carried by a Lean proof that compiles needs no further hand
  re-derivation of its formalized steps. For a **Lean-hostile** (numerical) bound the
  check is the directed-rounded certificate, re-run and adversarially re-derived by hand.
- **No hand-waving on the load-bearing step.** For a numerical certificate the reviewer
  re-derives the load-bearing step independently; if it can't, the bound is wrong. For a
  Lean proof the step must be *inside the formalization* — a `sorry`, an unproved
  hypothesis, or an axiom smuggling in the hard step means the bound is not established,
  however green `lake build` looks.
- **A valid bound first.** A construction that violates the constant's own
  constraints gives no bound at all, however good its value.
- **Prove, don't conjecture.** A numerical search result is a conjecture until
  certified — label it as such; never write an uncertified bound into `constants/`.
- **Name and verify your sources.** State the theorem/technique and the paper it
  comes from; check any reference actually says what's claimed.
