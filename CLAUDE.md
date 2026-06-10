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

- **Setup: none.** No build, no package, no test suite. Don't run `pip install` /
  `npm ci` / `uv sync`. Agents *will* run numerical code to build and check bounds —
  that's the work, not a build step.
- **Goal & eval.** Maximize the number of constants where we hold a bound that beats
  the value in `constants/<id>.md`, backed by a check that survives the reviewer.
  The measure, per constant: did we move a bound, and how well verified is it?
- **Depth over breadth.** One constant per run — the softest gap. Moving one bound
  is the win.
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
room. Roughly: a `current.md` snapshot (best bounds, the gap, what we hold), a place
for the literature and our digests, one living document per attack angle (the idea,
its status, and how it could be pushed further), and the construction/certificate
artifacts. Shape it as the work needs. An approach is a document you revisit and
strengthen, so nothing is lost between runs.

## Rigor rules

The reviewer enforces these:

- **Beat the record, exactly.** State the current table value and the new value. An
  "improvement" that doesn't strictly beat the table isn't one.
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
