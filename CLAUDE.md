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
  - **Lean** (the preferred certification path): install `elan` (→ `~/.elan`). The first Lean
    sketch of the run bootstraps a Lake project **at `constants/<id>/lean/`** (Mathlib `math`
    template); **pin and commit** `lean/lean-toolchain` + the Mathlib rev in
    `lean/lake-manifest.json` (a floating version breaks later-round sketches); `lake exe cache
    get` then `lake build` to confirm. Each sketch is a file `constants/<id>/lean/Sketches/<slug>.lean`;
    later Lean sketches reuse the same project. `constants/<id>/certificate/` records each
    sketch's `lake build` target + `#print axioms` line.
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
- **Progress signal — the sketch ranking, not a record-count.** Track the state of the
  sketch population: Elo, which sketches are live vs dead-ended, holes closing, and the
  verified `held` bound's gap to the record. It moves every productive round (a closed hole
  or verified advance lifts an Elo, a refuted one sinks) so it gives gradient between
  record-breaks. **Eval:**
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
- **The unit is a sketch — a population of competing whole attempts, not one growing proof.**
  An *approach* (slug) is a **sketch**: a complete, building attempt at the target with the
  unproved steps left as holes (Lean `sorry`, Python `# TODO`/`NotImplementedError`). The run
  keeps **several rival sketches at once**; the ranker (Elo) scores them and the sampler picks
  which to work. You route this breadth — never collapse the population to one cumulative proof
  (the single-line trap). How a sketch is worked is in the builder/outliner prompts.
- **Two roles, split by what's hard.** Outliner = strategy + the top-level theorem statement;
  builder = fills holes + intermediate-statement search. The split is specified in their
  prompts — you just dispatch the roles, you don't enforce the boundary.
- **Rank every round — no fast-path.** The outline-reviewer runs **every round** so the Elo
  always reflects the latest verified outcomes and the sampler's explore term keeps the
  population broad. There is no "skip the reviewer and just advance the leader" path — that
  collapses the population to one line (the single-line trap above).
- **Dispatch counts (every round).**
  `math-explorer ×1 → proof-outliner ×1 → outline-reviewer ×1 → proof-builder ×(1–N) →
  proof-reviewer ×1`. Builders fan out **one per sketch in the build set, in parallel** —
  each owns its own sketch file, so they never collide; **one proof-reviewer reviews all of
  them**.
- **Report paths.** Dispatch each subagent to write its report to its canonical
  `/tmp/round-{N}/<agent-name>.md` — don't rename it; the next agent reads that exact path.
- **Build set.** The outline-reviewer's report ends with `build set: <slug>[, <slug>...]` —
  dispatch **exactly one proof-builder per slug**, each told its slug. The set mixes sketches
  to advance (fill more holes) and any new/revised sketch the outliner opened this round.
- **Route per sketch (overrides the engine's whole-round "all APPROVE" gate).** One verdict
  per built slug, routed independently:
  - **APPROVE** — target reached hole-free and beats the record: terminal for the round,
    recorded by the reviewer. Neither holds the round open nor sends siblings back.
  - **CHANGES REQUESTED** — holes closed but more remain, or a gap to fix: re-dispatch only
    that slug's builder to fill more (this round or next; its sketch stays live either way).
  - **RETHINK** — a hole can't be closed the way the sketch sets it up: that slug goes back to
    the outliner to re-plan; the others are unaffected.
  A mixed result is normal, not a failed round. End once every slug is routed.

## Workflow

Each run picks **one** constant and loops over a **population of sketches**, one flow every
round (each agent's job is in its own prompt; routing in the orchestrator bullets above):

`math-explorer → proof-outliner → outline-reviewer → proof-builder ×(1–N) → proof-reviewer`

The outliner's *work* varies — open/revise a sketch when there's strategy to decide, else just
nominate live sketches to advance — but it always hands a field to the outline-reviewer, which
**ranks every round** and is the ranking hub + gate + build-set emitter. Each round starts
fresh with no memory; the sketches in `constants/<id>/` (their files + the `.md` commentary +
the ranker sidecar) are how the next round knows the population and resumes it.

## The `constants/<id>/` folder

A constant's workspace. **One approach = one slug = one sketch file + one commentary doc +
one ranker entry** — no per-approach subfolder. It holds:

- `literature/` — paper digests.
- `lemmas/` — the **shared goal cache**: lemmas proved in one sketch and *certified* by the
  reviewer, so every other sketch can import them instead of re-proving. This is how work
  compounds across the population — a sub-result closed once is reused everywhere. A lemma
  enters here only on the reviewer's certification (the same gate as a bound): the builder
  *proposes* it (proves it green, flags it promotable), the reviewer checks it's genuinely
  `sorry`-free / axiom-clean and generally stated, then admits it. An imported certified
  lemma is trusted without re-derivation — the kernel already checked it. (Lean: files in the
  same Lake project, imported by `Sketches/*.lean`. Python: a shared verified-helpers module.)
- `approaches/<slug>.md` — the sketch's **commentary**: the strategy, which holes remain and
  why, what would push it. Free-form. Not the artifact — the artifact is the sketch file.
- The **sketch file** — the building attempt itself, keyed by the same slug:
  - **Lean:** `lean/Sketches/<slug>.lean`, inside the per-problem Lake project at
    `constants/<id>/lean/` (`lakefile.toml` + `lean-toolchain` + pinned Mathlib). The first
    Lean sketch of the run **bootstraps** that project; every later Lean sketch is just
    another file in `Sketches/`, sharing the one Mathlib build. (Lean files only compile
    inside a Lake project — that's why they live here, not loose in `certificate/`.)
  - **Python / numerical:** `certificate/<slug>.py` — a standalone script, no project needed.
- `current.md` — the verified bottom line.

Ranking metadata (Elo, counts, stale, last outcome) lives in the tool-owned sidecar
`approaches/.ranking.json` — never hand-edited, only the ranking tools (served by
`.autofyn/approach_ranker.py`) touch it.

A **hole** is the unit of open work inside a sketch: a Lean `sorry` or a Python `# TODO` /
`raise NotImplementedError`. A sketch with holes still builds/runs — that's what keeps it a
valid population member while incomplete. The bound is **verified** only when a sketch reaches
the target with **no hole on the path to it** (Lean: `lake build` green *and* `#print axioms`
shows no `sorryAx`; Python: the directed-rounded check reproduces with no step hand-waved).

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
- **A cached lemma carries the same bar as a bound.** A lemma admitted to
  `constants/<id>/lemmas/` is imported by other sketches *on the reviewer's certification
  alone*, with no re-derivation — so it must clear the full bar before promotion: `sorry`-free
  and axiom-clean, with a statement that is correct and no stronger than what was proved. A
  wrong cached lemma silently poisons every sketch that later imports it. Only the reviewer
  promotes; the builder proposes.
