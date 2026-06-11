# Approach (R6): re-optimize q in the SAME Doche limit-point family, re-certify

Status: BUILT (round 6) — builder-claimed, PENDING reviewer verification.
Moves: UPPER bound. Same family as the R5 record (Doche [Doc01b] perturbed
limit-point family: base P1,P2,P4,P6,P8 + perturbing block Q = Q1*Q2, D = 56).
NO new factors, NO certificate redesign — this is one atomic step: optimize the
exponent vector q a little further than the hand-found R5 record q*, then
re-certify the single best q with the EXISTING `verify_upper.py` max(A,B)
quadrature.

## Result

- Chosen q = **(11.73584, 8.77354, 2.44938, 1.55411, 0.53442)**
  (a local polish of the R5 record q* = (11.74, 8.77, 2.45, 1.55, 0.53)).
- Optimizer's predicted float log h(q) (N=16e6 midpoint Riemann sum) = **0.2543308006**
  (vs q*'s float 0.2543325796 — a float improvement of ~1.78e-6).
- RIGOROUS certified bound (verify_upper.certify_maxAB, M0=200000, max_refine=14,
  rem_cap=1e-10): **C_82 <= log h(q) <= 0.2543309112**, frontier fully resolved
  (633296 leaves, 0 unresolved cells, 6 refine rounds).
- R5 record (reviewer-verified certified value): 0.2543326887.
- **STRICT improvement, margin = 0.2543326887 - 0.2543309112 = 1.7775e-6.**
- Admissibility (Doche Lemma 5) holds (q-independent — constrains only the
  polynomial dictionary): deg Q = 56 > 0, Q(0)=Q(1)=1 (X, 1-X do not divide Q),
  gcd(P_i, Q) = 1 for all five P_i. Confirmed by `admissibility_check()`.
- Soundness selftest for THIS q (cell_int_maxAB must dominate the true
  int_cell max(A,B) dt, mpmath prec=140 on 200 random cells): 0/200 violations
  for both the flat and the midpoint per-cell branch.
- Calibration gate (q-independent): float_value(Doche q) = 1.28973421, matching
  Doche's published record h = 1.289735 to 7 digits.

## What was done

1. `optimize_hq_b_fast.py` — a FAST multistart Nelder-Mead minimiser of the SAME
   objective `doche_hq_b.log_h` (the R5 objective, imported verbatim). The search
   uses a modest float-quadrature N=100000 (per-eval ~74 ms) and the final score
   uses N=16e6.  Seeds: the R5 record q*, Doche's q, and log-normal jitters around
   both.  The best q came from polishing q* itself (seed 0).  [The pre-existing
   `optimize_hq_b.py` uses N=600000 / 40000 fevals / 81 seeds, ~660 ms/eval — too
   slow to finish in a single round; `_fast` is the same objective with a tractable
   budget.  Both are float SEARCH tools only — a CONJECTURE until certified.]
2. `certify_q.py` — a thin driver that re-certifies a single chosen q with the
   EXISTING harness: it calls `verify_upper.certify_maxAB(q, ...)` (the same code
   that certified the R5 record), runs a q-specific soundness selftest reusing
   `verify_upper.cell_int_maxAB`, and the q-independent `admissibility_check()`.
   No certificate logic was rewritten.

## The bound is valid (why log h(q) is an upper bound)

Identical to R5 / [Doc01b]: for ANY admissible q, log h(q) is the value of a
genuine limit point of the spectrum of h_Z built from a sequence of integer
polynomials (Doche [Doc01a] Lemmas 2,3,4,5 + the non-triviality condition (4),
which holds here since deg Q = 56 > 0 and the P's, Q are non-unit integer
polynomials).  Admissibility is q-INDEPENDENT — it constrains only the fixed
dictionary {P1,P2,P4,P6,P8,Q1,Q2}, NOT the exponents — so the same admissibility
that licensed q* licenses this q.  No optimality of q is needed: a single
admissible q with a certified-from-above integral value below the record IS a
record.

## Reproduce

```
cd constants/82a/certificate
# (optional) re-run the search (~minutes; best q comes from polishing q*):
python3 optimize_hq_b_fast.py
# the deliverable: rigorously certify the chosen q (~150s):
python3 certify_q.py 11.73584 8.77354 2.44938 1.55411 0.53442 200000 14 1e-10
```
Expected final lines:
```
  CERTIFIED  log h(q) <= 0.2543309112
  unresolved frontier cells = 0
  beats R5 record (strict, frontier=0): True
  margin below R5 record = 1.7775e-06
```
Saved transcript: `certificate/cert_q_R6.txt`.

## What would push it further

- The float optimum of THIS exact 5-D family is essentially at this q
  (~0.2543308); further q-tuning yields only sub-1e-6 gains and is bounded below
  by the family's continuous optimum.  The certificate slack on top of the float
  value is only ~1.0e-7 (float 0.2543308006 -> certified 0.2543309112), so the
  certified bound is already nearly tight against the float value.
- The next real lever is a RICHER admissible dictionary (one more small-height
  perturbing factor Q_3, or another base poly P_m), keeping Doche Lemma 5
  (deg>0, Q(0)=Q(1)=1, gcd(P_i,Q)=1) — a genuinely new construction, a separate
  later round (do NOT fold it in here).

## Spec concerns

- The search value (0.2543308) is a CONJECTURE; ONLY the certified 0.2543309112
  (frontier=0) is the bound.  The two agree to ~1e-7, as expected.
- The new artifacts (`optimize_hq_b_fast.py`, `certify_q.py`) only WRAP the
  existing verified harness — `certify_q.py` calls `verify_upper.certify_maxAB`
  unchanged, and the q-specific selftest reuses `verify_upper.cell_int_maxAB`.
  The reviewer can independently re-run with `verify_upper.certify_maxAB(q, ...)`
  directly if preferred.
- The certified value 0.2543309112 still rounds to 0.25433 in the README's 5-dp
  table — the table entry "0.25434" does not change, but the held value tightens
  from 0.2543326887 to 0.2543309112.
