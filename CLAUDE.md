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

The strongest result is a **machine-checked** one: a bound whose proof Lean type-checks,
so "valid" means `lake build` passes, not "a reviewer re-derived it and spotted no hole."
That gate is categorically stronger — it eliminates the whole class of floating-point /
overlooked-step bugs that a hand-checked numerical certificate can hide.

So the target selection is Lean-aware. What decides fit is **the shape of the
load-bearing step**, not the field label:

- **Lean-fit** — the certifying step is finite, discrete, or algebraic: a finite case
  enumeration, a divisibility/congruence argument, an explicit construction whose
  validity is a polynomial identity or a degree/coprimality condition, a combinatorial
  counting bound, an inequality chained through `Mathlib` lemmas. Lean checks these
  natively. **These are the preferred targets**, and their certificate is a `.lean` file.
- **Lean-hostile** — the bound bottoms out in a continuum estimate: interval quadrature
  over many cells, an SDP feasibility certificate, a Mahler-measure integral (the 82a
  kind). Formalizing these in Lean is its own research project; do **not** force Lean
  here. They stay directed-rounded numerical certificates with adversarial review.

Field is not the filter: some number theory is analysis-heavy (L-functions, exponential
sums → continuum estimates → Lean-hostile), and some analytically-flavoured constants
have a discrete core that is Lean-fit. Triage on the certifying step. When two constants
are equally promising, prefer the Lean-fit one — its result is a theorem, not a
certificate.

## For the orchestrator

This is a research repo, not a code repo:

- **Setup: install the research toolchain, once.** There's no app to build, so skip
  `npm ci` / `uv sync` and don't install project packages. But this work needs two
  things, so install them at the start of round 1:
  - **A PDF text extractor** — reading the full papers behind the record bounds is
    the core of exploration, not optional. The sandbox has no root/`sudo`, so the
    `apt-get`/`poppler-utils` route is unavailable — use the pure-Python,
    pip-installable extractor instead: `pip install --user pdfminer.six`. Then a
    saved PDF is read with `pdf2txt.py paper.pdf` (or `extract_text` in Python).
  - **A scientific Python stack** for building and checking bounds:
    `uv pip install --system numpy scipy` (add `cvxpy` / `sympy` when an angle needs
    an SDP solver or symbolic algebra).
  - **The Lean toolchain** — the preferred certification path (see below). Round 1
    scaffolds it once, in order:
    1. Install `elan` (no root — it lands in `~/.elan`): `curl` the elan installer
       and run it.
    2. **Create the project** if `lean/` doesn't exist yet: at the repo root,
       `lake +<toolchain> new lean math` (the `math` template wires in Mathlib as a
       dependency), giving `lean/lakefile`, `lean/lean-toolchain`, and a
       `lean/lake-manifest.json`. If `lean/` already exists, skip this.
    3. **Pin the versions** — choose a known-good Lean + Mathlib pair and freeze it:
       the `lean/lean-toolchain` file and the Mathlib rev in `lean/lake-manifest.json`
       must be committed, because the sandbox persists across rounds, so a version
       chosen now holds for the whole run; letting `lake` float to latest risks a
       proof that compiled in round 3 breaking in round 40.
    4. From `lean/`, `lake exe cache get` to pull the prebuilt Mathlib cache (a large
       one-time download; building it from source would take hours), then
       `lake build` once to confirm the project compiles before any proof is written.
    The sandbox keeps `~/.elan` and the compiled Mathlib between rounds, so this cost
    is paid once and every later round just type-checks the new proof against the
    cached library. A constant's Lean proof lives inside the `lean/` project tree (so
    Lake can build it) — e.g. `lean/Constants/C<id>.lean` — and
    `constants/<id>/certificate/` records how to build and check it (the `lake build`
    target and the `#print axioms` line), pointing at that proof file.
  Installing is allowed and expected here — the "no installs" instinct doesn't apply
  to this repo. Beyond these, agents run numerical code and Lean proofs to build and
  check bounds; that's the work, not a build step.
- **Reading arXiv papers — do it, don't work from abstracts.** Prefer the full-text
  HTML render `arxiv.org/html/<id>` (WebFetch reads it directly, no download). Fall
  back to `arxiv.org/abs/<id>` for the abstract/metadata. **Do NOT WebFetch
  `arxiv.org/pdf/<id>`** — it returns raw bytes; download the PDF (into
  `constants/<id>/literature/pdfs/`, never into `/tmp/memory/` or a round dir — those
  are archived as text and a stray binary breaks the snapshot) and run
  `pdf2txt.py` (pdfminer.six) instead.
- **One constant per run.** A run attacks exactly ONE constant `<id>`, chosen in
  round 1 and fixed for the whole run. All rounds push that one constant. Everything
  below — the metric, the eval, `current.md` — is about that single `<id>`.
- **Goal & eval — the one signal is the approach ranking.** Beating the record can take
  many rounds, so a binary "did we beat it" metric reads 0 for most of a run and gives the
  loop no gradient. The dense signal is the **state of the approach population** — the Elo
  ranking, which angles are live and which dead-ended, and the best verified bound we hold.
  That state moves every productive round (a verified advance lifts an approach's Elo, a
  refuted one sinks; the held bound tightens) even when no record falls, so it is what the
  orchestrator tracks to judge "are we progressing". The reviewer's per-approach
  `record_outcome` is what feeds it (see the workflow); the outline-reviewer folds those
  into the Elo each round.
  - **Eval:** a command that reads the population state for the run's constant — from the
    ranker sidecar `constants/<id>/approaches/.ranking.json` (top Elo, live vs dead-ended
    counts) together with the verified `held` bound and its gap to the record in
    `current.md` — and prints that as the round's progress line. Progress is the population
    sharpening and the gap shrinking; regression is the leader stalling while nothing new
    fires. No milestone-line counting: that was the pre-ranking metric and the ranking
    subsumes it.
  - The signal is only as honest as the reviewer is adversarial — an Elo lift comes from a
    *verified* advance, never the builder's unverified claim, so a round that produced
    nothing reproducible moves nothing.
  - The rare actual record-break is the headline event, flagged separately: that constant's
    `current.md` gets `## Status: improved` (else `none`).
- **Pick the most promising constant, not the widest gap.** Promising means
  *tractable*: a real, attackable opening with the right kind of machinery available.
  A huge gap can be huge because the bound is hopeless (moving it would settle a
  Millennium problem — e.g. the de Bruijn–Newman lower bound ⇔ the Riemann
  Hypothesis), and some constants are already closed (upper = lower, e.g. 11b). The
  explorer triages this in round 1; skip the closed and the conjecture-hard, prefer the
  Lean-fit, and spend the run where verified progress is actually reachable. A steadily
  sharpening approach population on the chosen constant is the win; an actual record-break is the
  breakthrough.
- **One folder per problem.** Everything for a constant lives in `constants/<id>/`,
  beside Tao's record file `constants/<id>.md`. The record is the current bound to
  beat; edit it only once an improvement is verified. The folder is the scratchpad —
  work there freely.
- **Build set → parallel builders.** The outline-reviewer ends its report with
  `build set: <slug>[, <slug>...]` — the slugs it chose to build this round (it sizes the
  set, often just 1, at most 3). Dispatch **exactly one proof-builder per slug listed** —
  no more, no fewer — in parallel (the "parallel same-type agents, distinct output
  filenames" pattern), each told which slug it owns. Don't collapse a multi-slug set to one
  builder, and don't pad a single-slug set to three.
- **Route per approach.** The proof-reviewer returns one verdict per built slug. Route
  each independently — APPROVE records it, CHANGES REQUESTED → its builder, RETHINK → the
  outliner. A mixed result is normal; end the round once every slug is routed.

## Workflow

Each run picks **one** constant and loops (each agent's job is in its own prompt; routing
in the orchestrator bullets above):

**math-explorer → proof-outliner → outline-reviewer → proof-builder ×(1–3) → proof-reviewer**

Record every attempt in `constants/<id>/`. The next round starts fresh with no memory —
the folder is how it knows what was tried and why a line stalled.

## The `constants/<id>/` folder

The run's constant gets a workspace beside its record file — research needs room. It
holds the literature digests (`literature/`), one living document per attack angle
(`approaches/<slug>.md` — the idea, its status, and how to push it), the
construction/certificate artifacts (`certificate/`), and the tracking file
`current.md`. The proof work lives in `approaches/` + `certificate/`; `current.md`
records only the verified bottom line. An approach is a document you revisit and
strengthen, so nothing is lost between runs.

Approach bodies (`approaches/<slug>.md`) are free-form. Their ranking metadata (Elo,
counts, stale flag, last outcome) lives in the tool-owned sidecar
`approaches/.ranking.json` — never hand-edited; only the ranking tools touch it
(`sample_approaches`/`register_approach`/`record_outcome`/`update_ranking`, served by
`.autofyn/approach_ranker.py`).

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
