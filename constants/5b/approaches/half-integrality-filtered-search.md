# Approach: half-integrality-filtered-search

**Constant:** C_5b (Erdős #757), UPPER bound. Record to beat (verified): **4/7 ≈ 0.5714286**.

## Idea
The interleaved transversal cert (`lean/Constants/C5bInterleaved.lean`, `hLe_of_interleaved`, R5)
certifies `h(A) ≤ N − τ` with a **small** decidable branch budget *only* when the 3-AP cover LP has
integral structure on some support P. R5 proved A_base (N=14) is the worst case — **fully
half-integral** (ν*=9/2, all coords in {0,½}, no x=1 vertex), so the cert gives **zero budget shrink**
there (exhaustively verified over all 2¹⁴ supports). The risk this approach de-risks: a found N≈30
beat gadget might share that pathology and be **uncertifiable** with a tractable Lean budget — a beat
we couldn't actually certify.

This approach builds a re-runnable LP-half-integrality / interleaved-friendliness **filter** and a
**verified structural survey** answering: are the N≈30 (4,5)-sets all fully half-integral like A_base,
or do some admit a partially-integral / interleaved-friendly cover LP?

## What was done (R7)
Verified, extended, and corrected the R6 filter machinery (`constants/5b/certificate/halfint/`):

- **Exactness re-confirmed.** τ via integer branch-and-bound, cross-checked exactly against the
  independent `search_N30` milp+B&B (α=N−τ) on all four families. ν* via exact rational simplex
  (sympy `lpmax` on the dual matching LP), cross-checked vs scipy float to 1e-6. The half-integrality
  read-off uses an exactly-certified rational LP vertex.

- **Honesty fix (correctness bug in the R6 labels).** The R6 script conflated two orthogonal
  properties under one "fully-half-integral / interleaved-HOSTILE" label — it tagged the Fibonacci
  N=30 set (ν*=55303/5896, large denom, NOT half-integral, 1 x=1 vertex) and the random N=30 set
  (ν*=10, 10 x=1 vertices) as "fully half-integral", which is false. Now the filter reports **LP
  structure** (`fully-half-integral` / `partially-integral(x=1)` / `mixed-fractional` /
  `large-denom-fractional`, all exact) and **friendliness** (`exhaustive` = two-sided verdict vs
  `heuristic-P` = one-sided "no shrink found, not a proof") **separately**.

- **Edge-union support search added** (the technical advance). The cert charges only edges *entirely
  inside* P, so a support scattering x=1 vertices one-per-edge charges nothing (verified: fixing all
  10 of RAND30's x=1 vertices gives a(P)=1). The new heuristic grows P by *whole 3-AP triples* (greedy
  vertex-disjoint edge packing + densest-cluster supports). This surfaced the headline result the R6
  single-shell heuristic missed.

## Verified survey results
| set | N | τ | α | ν* | LP structure | best g | friendliness |
|---|---|---|---|---|---|---|---|
| A_base | 14 | 6 | 8 | 9/2 | fully-half-integral | 5 = τ−1 | HOSTILE (exhaustive 2¹⁴) |
| 2×A_base | 28 | 12 | 16 | 9 | fully-half-integral | 11 = τ−1 | no-shrink (heuristic) |
| Fibonacci | 30 | 11 | 19 | 55303/5896 | partially-integral (1 x=1) | 10 = τ−1 | no-shrink (heuristic) |
| **RAND30** | **30** | **10** | **20** | **10** | **partially-integral (10 x=1)** | **1 ≪ τ−1=9** | **interleaved-FRIENDLY** |

All four are genuine (4,5)-sets (difference condition, `is45set`=True).

## Headline / claim
**Claim (verified-exactly structural fact, NOT a bound):** the A_base fully-half-integral pathology is
**not universal** among N=30 (4,5)-sets. The random N=30 (4,5)-set `RAND30` has an **integral** cover
LP (ν*=10=τ) and is **interleaved-FRIENDLY with budget g=1**: an edge-union support P of 24 vertices
absorbs 10 of its 12 3-APs (a(P)=⌈ν*(edges⊆P)⌉=8, integral), leaving a 2-edge residual (τ=2), so
`a(P)+τ(res)=8+2=10=τ` exactly ⇒ `g=τ(res)−1=1` (a 3-leaf decide tree, not 3⁹). Re-derived exactly and
locked as an assertion in the script.

**No bound is claimed** against 4/7 — RAND30 has α=20 (ratio 0.667), nowhere near a beat. This is a
*certifiability* witness: it shows a density-clearing N=30 gadget would **not** automatically be
uncertifiable, retiring the R5/explorer-flagged risk that a found beat could be unusable.

## Key finding (deeper than R5)
**Integral cover LP ≠ interleaved-friendly.** Friendliness needs a support absorbing *whole* 3-AP
triples, not merely the presence of x=1 vertices. The cert's edge-inside-P charging is the operative
constraint. The edge-union support construction is the right friendliness primitive going forward.

## How to push further
1. **Wire `screen(A)` into the gadget search** (`search_N30.py` / `search_N30_mtargeted.py`) as an
   x=1-aware / edge-union reward, so a density-clearing candidate is friendly *by construction* —
   directly couples the bound-mover (cpsat) to certifiability.
2. **Upgrade the N=30 friendliness verdict from heuristic to proof**: an exhaustive *edge-subset* DP
   over the ≤26 edges (not 2^vertices) makes "no shrink found" a real two-sided verdict, and finds the
   optimal friendly support for any candidate.
3. The friendly support found here (10-of-12 edges absorbed, residual τ=2) is the template a beat
   gadget should imitate: high edge-packing density into a small-residual support.

## Status
Verified structural survey + corrected/extended filter machinery. No bound. Conjecture/structure only;
`constants/5b.md` untouched. Certificate: `constants/5b/certificate/halfint/` (`lp_halfint_filter.py`,
`survey_output.txt`, `README.md`).
