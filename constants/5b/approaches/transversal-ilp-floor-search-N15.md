# transversal-ilp-floor-search-N15

**Angle.** Search for a 15-point **(4,5)-set** `A` with `h(A) = 8` (the largest Sidon
subset = independence number `alpha` of the 3-AP hypergraph, MT26 Lemma 2.3). Such a set
gives `c* <= 8/15 = 0.5333 < 4/7` — a strict beat of the verified record upper bound.
The proven floor `c* >= 9/17` forces `h >= ceil(9*15/17) = 8`, so `8` is the FLOOR and must
be hit **exactly** (`h = 9` gives `9/15 = 0.6 > 4/7`, no beat).

## Round 2 — built (NO beat; negative result + a spec correction)

**Status: live, no improvement.** Claim: **none** — no 15-point (4,5)-set with `h <= 8`
was found; the realized minimum is `h = 10` (ratio `10/15 = 0.667 > 4/7`). This does **not**
beat the record. Reported honestly as a negative result, not a bound.

### SPEC CORRECTION (the most important finding of the round)

The round-1 digest (`literature/MT26-ma-tang-digest.md`, line 7-9) claimed:

> "(4,5)-set: every 4-subset has >=5 distinct pairwise differences. **Equivalently** a weak
> Sidon set: all pairwise sums distinct."

**This equivalence is FALSE.** Verified against the arXiv:2602.23282 abstract: a (4,5)-set
is the **difference** condition — every 4-element subset has `>= 5` distinct pairwise
absolute differences. This is **strictly stronger** than weak-Sidon (sums distinct):

- `{0,1,2,4}` has 6 distinct sums `{1,2,3,4,5,6}` (weak Sidon) but only 4 distinct
  differences `{1,2,3,4}` → it is **NOT** a (4,5)-set.
- Direction proven (exact, in `certificate/search_N15.py`): `(4,5)-set ⟹ weak Sidon`
  (a repeated sum in a 4-subset forces `<= 4` distinct diffs), but **not** conversely.

Consequence for the engine: `lean/Constants/C5b.lean` certifies `weakSidonB` (sums
distinct), which is the **weaker** predicate. The round-1 bound is **still valid** because
the record set `A_base` is a genuine (4,5)-set under the corrected definition (re-verified:
`is_45set(A_base)=True`, `h=8`). But **before any NEW gadget is trusted**, the Lean engine's
`weakSidonB` must be replaced by a decidable `is45setB` (every 4-sublist has `>= 5` distinct
`|x-y|`; `C(15,4)=1365` quads, well within `decide`). Flagged for the reviewer.

### What was searched (all exact-integer; `alpha = h` via exact branch-and-bound)

All under the **corrected** (4,5)-set definition:

1. **Single-point extension of `A_base`** (exhaustive, `v in [-20000, 40000]`): **0**
   extensions to 15 points keep `h <= 8`. Adding any point to a max-Sidon-8 set extends the
   independent set.
2. **Exact-`alpha` simulated annealing** — 30 seeds across multiple runs, move sets =
   {random replace, +-small step, AP-targeted `2a-b`, 2-swap}, windows `W` up to `1e7`,
   restarts from `h=10` incumbents. **Wall at `h = 10`**; `h = 9` never reached.
3. **CP-SAT max-#3AP proposer** (`W in {160,200,260}`): packs 12-13 3-APs but exact `alpha`
   stays 11-12 — re-confirms the round-1 lesson that **edge count != small alpha**.
4. **Dense small-span (4,5)-set enumeration**: `h = 10`.
5. **CEGAR feasibility model** (`weak-Sidon AllDifferent` + lazy "no independent 9-subset"
   cuts): the reified `x_i+x_k != 2 x_j` constraints made even a single feasibility solve
   exceed the per-solve budget; inconclusive (not a proof of non-existence). Recorded as a
   method that needs a better encoding next round.

Best realized: `h = 10`, set `[20,24,25,79,86,133,148,191,212,233,242,269,459,590,1160]`
(verified genuine (4,5)-set; size-10 Sidon witness recorded). Ratio `0.667`.

### Certificate

`constants/5b/certificate/search_N15.py` — re-runnable, deterministic summary
(`python search_N15.py`): re-verifies the spec correction, `A_base` as a genuine (4,5)-set
with `h=8`, and the best/greedy `h=10`/`h=11` 15-point (4,5)-sets with explicit Sidon
witnesses. No Lean certificate this round — there is no beating gadget to certify.

## Interpretation

Consistent with the math-explorer's floor-squeeze read: the proven `9/17` floor pins the
admissible `h` to the single value `8` at `N=15`, and that value appears **unreachable** for
`N=15` — the realized minimum sits at `floor + 2 = 10`. This is suggestive (not a proof)
that `N=15` cannot beat `4/7`, mirroring `N=9` (floor 5 unreached, min realized 6).

## What would push it further

- **First: fix the Lean engine's predicate** (`is45setB` = `>=5`-diff over 4-sublists) so
  any future gadget is certified against the *correct* (4,5)-set property. Cheap (`C(N,4)`
  enumeration, `decide`-tractable) and necessary for soundness.
- A **complete** bounded search at `N=15` would turn the suggestive wall at `h=10` into a
  proof that `N=15` cannot beat `4/7` — but the tree is large; needs the transversal/`alpha`
  lower-bound prune plus a proven window cap (a span bound for (4,5)-sets with small `alpha`).
- Re-encode CEGAR without reified `!=` (channel each `x_i` to a one-hot over the window;
  express weak-Sidon as `AllDifferent` on precomputed sum cells) to make the
  direct-`alpha <= 8` feasibility question solvable — this is the only method that could give
  a definitive YES, and it stalled only on encoding, not on logic.
- Given the floor-squeeze evidence at `N=9, 13(partial), 15`, weigh shifting the build budget
  to a **larger feasible N with more room** (`N=18`, floor 10, ratio 0.556) or the
  **modular-construction** family, where the antagonism between (4,5) and small-`alpha` has
  room to be decoupled by coordinate separation.
