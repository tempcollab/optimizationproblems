# C_5b — LP-half-integrality / interleaved-friendliness survey (approach `half-integrality-filtered-search`)

## What this certifies (the de-risk)
The R5 interleaved transversal cert (`lean/Constants/C5bInterleaved.lean`, `hLe_of_interleaved`)
proves `h(A) ≤ N − τ` with a **small decidable branch budget** only when the 3-AP cover LP has
*integral structure on a support P*: it splits any hitting set into an LP-charged part on edges
*entirely inside P* (carrying `a(P)=⌈ν*(edges⊆P)⌉`) plus a residual branch part of budget
`g = τ(residual)−1`. The Lean `decide` tree has `3^g` leaves, so the cert is tractable iff some P
reaches the full τ with small g. R5 found A_base (N=14) is the **worst case** — fully half-integral
(ν*=9/2, all coords in {0,½}, no x=1 vertex), and even the *exhaustive* support search gives no
shrink (g = τ−1 = 5, only P=∅ reaches τ). The open risk: a found N≈30 beat gadget might share this
pathology and be **uncertifiable** with a small budget.

This survey answers: **are the N≈30 (4,5)-sets all fully half-integral like A_base, or do some admit
a partially-integral / interleaved-friendly cover LP?**

## Files
- `lp_halfint_filter.py` — the composable filter + survey. `python3 lp_halfint_filter.py` (~90s).
  `from lp_halfint_filter import screen; s = screen(A)` screens any (4,5)-set.
- `survey_output.txt` — the recorded verified run output (re-derivable by re-running the script).

## Exactness (CLAUDE.md rigor — no float drives any classification)
- `τ` (min 3-AP transversal): exact integer branch-and-bound. Cross-checked against the independent
  `search_N30.alpha_milp`/`alpha_bb` (α = N−τ) — **all four families agree exactly** (verified in
  this round).
- `ν*` (cover LP optimum): exact **rational** via sympy's exact simplex on the matching LP
  (`lpmax`, dual to the cover LP). Independently cross-checked against scipy float (`nu_crosscheck_ok`,
  agree to 1e-6) — never used for classification.
- The optimal LP vertex is rationalized and **certified exactly** (0≤x≤1, every edge covered,
  Σx = ν*); a vertex that fails to certify at small denominator *proves* the LP is not half-integral.
- The interleaved budget over a support P uses exact `ν*(edges⊆P)` and exact integer `τ(residual)`.

## Two orthogonal properties, reported separately (honesty fix this round)
1. **LP structure** (exact, fully determined): `fully-half-integral` (A_base pathology) /
   `partially-integral(x=1)` / `mixed-fractional` / `large-denom-fractional`.
2. **Interleaved-friendliness**: does some support P give `g < τ−1`? `exhaustive` ⇒ a two-sided
   verified verdict; `heuristic-P` ⇒ **one-sided** ("no shrink found", NOT a proof none exists).
   The heuristic only ever produces a FRIENDLY verdict that is *exactly re-derived* (sound direction).

## Verified survey results (this round)
| set | N | m | τ | α | ν* | LP structure | best g | friendliness |
|---|---|---|---|---|---|---|---|---|
| A_base | 14 | 12 | 6 | 8 | 9/2 | fully-half-integral | 5 = τ−1 | HOSTILE (exhaustive, 2¹⁴) |
| 2×A_base | 28 | 24 | 12 | 16 | 9 | fully-half-integral | 11 = τ−1 | no-shrink (heuristic) |
| Fibonacci | 30 | 26 | 11 | 19 | 55303/5896 | partially-integral (1 x=1) | 10 = τ−1 | no-shrink (heuristic) |
| **Random** | **30** | **12** | **10** | **20** | **10** | **partially-integral (10 x=1)** | **1 ≪ τ−1=9** | **interleaved-FRIENDLY** |

All four `is45set` = True (genuine (4,5)-sets, difference condition).

## Headline (the survey question, answered)
**The A_base fully-half-integral pathology is NOT universal at N=30.** Both surveyed N=30 (4,5)-sets
carry LP-forced x=1 vertices (integral structure A_base lacks). Concretely, the random N=30 set
`RAND30` has an **integral** cover LP (ν*=10=τ) and is **interleaved-FRIENDLY with budget g=1**: an
edge-union support P of 24 vertices absorbs 10 of its 12 3-APs entirely (a(P)=⌈ν*(edges⊆P)⌉=8,
integral), leaving a 2-edge residual (τ=2), so `a(P) + τ(residual) = 8 + 2 = 10 = τ` exactly ⇒
`g = τ(residual) − 1 = 1` (a 3¹=3-leaf decide tree, not 3⁹). This is **verified exactly** and locked
in as an assertion in the script.

RAND30 does **not** beat 4/7 (α=20). It is a *certifiability* witness, not a bound: it proves a
density-clearing N=30 gadget would not automatically be uncertifiable.

## Key technical finding (deeper than R5)
**Integral cover LP ≠ interleaved-friendly.** The cert charges only edges *fully inside* P, so a
support that scatters its x=1 vertices one-per-edge charges almost nothing (verified on RAND30:
fixing all 10 x=1 vertices gives a(P)=1, not 10). Friendliness needs a support that absorbs *whole*
3-AP triples. The **edge-union support search** added this round (greedy vertex-disjoint edge packing
+ densest-cluster supports) is what surfaces the g=1 verdict the prior single-shell heuristic missed.

## What would push this further
- Wire the `screen(A)` filter into the gadget search (`search_N30.py`) as an x=1-aware / edge-union
  reward, so a density-clearing candidate is *also* interleaved-friendly by construction.
- Strengthen the N=30 support search from the curated heuristic toward a proof (an exhaustive
  edge-subset DP over the ≤26 edges, not 2^vertices) to upgrade "no shrink found" to a real verdict.

Nothing here is written into `constants/5b.md`; this is a structural survey, conjecture/structure
only — no bound is claimed.
