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
- **Goal & eval.** Beating a record on these constants can take many rounds — you
  do not improve a bound every round, and a binary "did we beat the record" metric
  would read 0 for most of a run and give the loop no signal. So the metric is
  **verified progress**, not record-breaks: every round that genuinely advances the
  frontier (reproduced the record method, built a feasible construction, closed a
  certificate gap, tightened a verified bound, and ultimately beat the record) is a
  milestone the reviewer logs. Beating the record is the headline milestone, not the
  only one that counts.
  - **Metric:** number of reviewer-verified progress milestones — the `- R<round>:`
    lines the reviewer appends to the `## Progress log` of each attacked constant's
    `current.md`. **Baseline: 0.** (Set the eval to a command that counts those
    lines across `constants/*/current.md`.)
  - A milestone is logged **only by the proof-reviewer, only for a round whose
    advance it verified** — so the builder can't pad it. A round that produced
    nothing new (re-digested the same paper, an unreproducible claim) logs no
    milestone and the count plateaus.
  - The rare actual record-break is additionally flagged: that constant's
    `current.md` gets `## Status: improved` (else `none`).
- **Depth over breadth.** One constant per run — the **most promising** one, not the
  widest gap. Promising means *tractable*: a real, attackable opening with the right
  kind of machinery available. A huge gap can be huge because the bound is hopeless
  (moving it would settle a Millennium problem — e.g. the de Bruijn–Newman lower
  bound ⇔ the Riemann Hypothesis), and some constants are already closed (upper =
  lower, e.g. 11b). The explorer triages this first; skip the closed and the
  conjecture-hard, and spend the run where verified progress is actually reachable.
  Steady verified progress on one such constant is the win; an actual record-break is
  the breakthrough.
- **One folder per problem.** Everything for a constant lives in `constants/<id>/`,
  beside Tao's record file `constants/<id>.md`. The record is the current bound to
  beat; edit it only once an improvement is verified. The folder is the scratchpad —
  work there freely.

## Workflow

Each run, pick **one** constant and run the loop:

**math-explorer → proof-outliner → outline-reviewer *(optional)* → proof-builder → proof-reviewer**, then route on the reviewer's verdict:
- **APPROVE** → record the improvement; push further or move on.
- **CHANGES REQUESTED** → back to **proof-builder** to close the gap.
- **RETHINK** → back to **proof-outliner** for a different angle.


1. **math-explorer** — Read `constants/<id>.md` and any existing `constants/<id>/`.
   Fetch and digest the papers behind the record bounds so we know the number to beat
   and don't repeat a dead end. Report where the slack is, which bound is softer, and
   any angle the prior work didn't try. Does NOT attempt the improvement.
   You may run **several explorers in parallel** for wider
   coverage — each taking a distinct angle (the record papers, techniques from an
   analogous constant, the computational/relaxation side) so they surface
   uncorrelated openings instead of one framing.
2. **proof-outliner** — Propose several attack angles, not one — strengthen the
   record, borrow a technique from an analogous constant, an explicit construction, a
   computational relaxation. Rank them; name the hard step in each.
3. **outline-reviewer** *(optional)* — On a non-trivial angle, check it can actually
   beat the record before the builder spends compute.
4. **proof-builder** — Turn the chosen angle into a concrete improvement and the
   artifact that backs it (an argument, a construction, or a certificate it runs to
   check). The deep step — runs on the strongest model.
5. **proof-reviewer** — Adversarially verify: reproduce the check, re-derive the
   load-bearing step independently, confirm the bound strictly beats the table value.
   Emit the verdict that routes the round.

Record every attempt in `constants/<id>/`. The next round starts with a fresh context
and no memory of this one — the folder is how it knows what was tried and why a line
stalled, so it builds on the work instead of repeating it.

## The `constants/<id>/` folder

Each attacked constant gets a workspace beside its record file — research needs
room. It holds the literature digests (`literature/`), one living document per
attack angle (`approaches/<slug>.md` — the idea, its status, and how to push it),
the construction/certificate artifacts (`certificate/`), and the tracking file
`current.md`. Shape the rest as the work needs; an approach is a document you
revisit and strengthen, so nothing is lost between runs.

### `current.md` — the tracking file (contract)

The per-constant scratchpad the eval reads. It MUST contain these sections:

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
