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
  Installing is allowed and expected here — the "no installs" instinct doesn't apply
  to this repo. Beyond these, agents run numerical code to build and check bounds;
  that's the work, not a build step.
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
- **Goal & eval.** Beating the record can take many rounds — you do not improve the
  bound every round, and a binary "did we beat the record" metric would read 0 for
  most of a run and give the loop no signal. So the metric is **verified progress**,
  not record-breaks: every round that genuinely advances the frontier (reproduced the
  record method, built a feasible construction, closed a certificate gap, tightened a
  verified bound, and ultimately beat the record) is a milestone the reviewer logs.
  Beating the record is the headline milestone, not the only one that counts.
  - **Metric:** number of reviewer-verified progress milestones — the `- R<round>:`
    lines the reviewer appends to the `## Progress log` of the run's constant's
    `constants/<id>/current.md`. **Baseline: 0.** (Set the eval to a command that
    counts those lines in that one file.)
  - A milestone is logged **only by the proof-reviewer, only for a round whose
    advance it verified** — so the builder can't pad it. A round that produced
    nothing new (re-digested the same paper, an unreproducible claim) logs no
    milestone and the count plateaus.
  - The rare actual record-break is additionally flagged: that constant's
    `current.md` gets `## Status: improved` (else `none`).
- **Pick the most promising constant, not the widest gap.** Promising means
  *tractable*: a real, attackable opening with the right kind of machinery available.
  A huge gap can be huge because the bound is hopeless (moving it would settle a
  Millennium problem — e.g. the de Bruijn–Newman lower bound ⇔ the Riemann
  Hypothesis), and some constants are already closed (upper = lower, e.g. 11b). The
  explorer triages this in round 1; skip the closed and the conjecture-hard, and spend
  the run where verified progress is actually reachable. Steady verified progress on
  the chosen constant is the win; an actual record-break is the breakthrough.
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

The tracking file for the run's constant — the eval counts its milestone lines. It
MUST contain these sections:

```
## Status            improved | none   (only the reviewer sets `improved`)
## Bounds            table: <record to beat> · held: <best value WE have verified>
## Progress log      - R<round>: <one-line verified advance>   (reviewer-appended)
```

`held` is the reviewer-verified value, never the builder's unverified claim (a
numerical-search result is a conjecture — it goes in an approach doc, not `held`).
The eval counts the `- R<round>:` lines; only the reviewer writes them, and only for
a verified advance.

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
- **The check must be reproducible.** A bound from computation is only as good as the
  check the reviewer can re-run; one that can't be reproduced isn't established.
- **No hand-waving on the load-bearing step.** The reviewer re-derives it; if it
  can't, the bound is wrong.
- **A valid bound first.** A construction that violates the constant's own
  constraints gives no bound at all, however good its value.
- **Prove, don't conjecture.** A numerical search result is a conjecture until
  certified — label it as such; never write an uncertified bound into `constants/`.
- **Name and verify your sources.** State the theorem/technique and the paper it
  comes from; check any reference actually says what's claimed.
