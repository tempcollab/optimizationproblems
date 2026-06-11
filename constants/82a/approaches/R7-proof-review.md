# R7 proof-review — UPPER bound, free-exponent Q3 enrichment

**Verdict: APPROVE.  Verification level: verified.  RECORD BREAK.**

New value: **C_82 <= 0.2543185491**  ·  Prior verified record (R6 held): 0.2543309112
Strict beat, margin **1.236e-5**, still < Doc01b bar 0.25443677.

## Goal Progress
- Eval: `grep -rh '^- R[0-9]' constants/*/current.md | wc -l`
- Previous: 3
- Current: 4
- Direction: IMPROVED

## What I verified (all five required steps + extra adversarial checks)

1. **Certificate reproduced from scratch.**
   `verify_upper_q3.py certify 12.040 9.380 2.462 1.711 0.581 0.129 200000 14 1e-10`
   -> CERTIFIED log h(q,qB) <= 0.2543185491, frontier driven to 0 (637808 leaves,
   6 rounds), int_0^2pi G dt <= 94.4313050433, int_0^1 G ds <= 15.0292089803,
   D = 59.096. selftest_q3 0/200 on BOTH flat and midpt branches. Reproduces exactly.

2. **Anchor (Q3 is a genuine extension, not a broken integrand).**
   `verify_upper_q3.py anchor` -> at qB=0 the EDITED harness gives float 0.2543308006,
   matching vu.float_value(R6 q) = 0.2543308006 to >=10 digits, and D collapses to 56.
   So the new value is the same family deformed by a real free-exponent block, and the
   numerator/D ratio is the genuine Doche h(q,qB) — a valid UPPER bound.

3. **Admissibility independently re-derived (my own sympy, not the builder's code).**
   V = prod P^q coprime to W = Q1*Q2*Q3 (gcd(P_i, W) = 1 for all five P_i, gcd(Q1,Q3)=
   gcd(Q2,Q3)=gcd(Q1,Q2)=1); deg Q_{l+1} = deg(Q1*Q2) = 56 > 0; W(0)=W(1)=1 so neither
   X nor (1-X) divides W; Q3 squarefree; every Q non-constant. Therefore Doche Lemma 5
   hypotheses AND non-triviality condition (4) (prod P^n / prod Q^n != +/-1) hold for
   the multi-block (ell=1) construction. The enlarged family genuinely falls under
   Doc01a's upper-bound theorem -> log h(q,qB) is a valid upper bound on C_82.

4. **Free-exponent formula re-derived against the Doc01a PDF directly (load-bearing).**
   Extracted doche_spectrum_doc01a.pdf (lines ~905-1180): the perturbing side is
   `Q_{l+1} * prod_{m<=l} Q_m^{q_{k+m}}`, f(q) = int int log| prod P^q(chi) -
   e^{2ipi t} Q_{l+1} prod Q_m^{q_{k+m}}(chi) | ds dt, and
   D = 2b * max( sum q_m deg P_m , deg Q_{l+1} + sum q_{k+m} deg Q_m ).
   The inner t-integral collapses by Jensen to log max(|prod P^q|, |Q_{l+1} prod
   Q_m^{q_{k+m}}|). With Q_{l+1}=Q1*Q2, single free block Q3 (weight qB): this is
   EXACTLY B = log|Q1Q2| + qB*log|Q3|, D = max(sum q_i deg P_i, 56 + qB*24). Matches
   cell_AB_q3 and _Dval line for line — genuine Doche, NOT an ad-hoc edit.
   Per-cell enclosure cross-checked against my OWN mpmath prec-200 mp.quad on 40 cells
   (my own integrand build), flat+midpt branches: 0 violations, worst
   cell_hi - true_int = +5.05e-14 >= 0 (outward-rounded, sound).
   D arithmetic by hand: A-branch 49.604 < B-branch 56+0.129*24 = 59.096, so D=59.096;
   15.0292089803/59.096 = 0.2543185491. Margin below held = 1.236e-5.

5. **Strict beat confirmed exactly:** 0.2543185491 < 0.2543309112 (best VERIFIED bound),
   margin 1.236e-5 >> the ~1.1e-7 certificate slack and ~1e-10 float noise — a real
   margin, not a rounding artifact.

**Tamper test (no hidden grid-pass).** Feeding a bogus target 0.25431 (below the true
value) to certify_maxAB_q3 correctly reports BEATS=False; the returned bound stays
0.2543185491 regardless of target. No silent grid fallback faking the proof.

## Milestone logged
Yes — R7 line appended to constants/82a/current.md Progress log (the first upper-side
gain from DICTIONARY enrichment rather than q-tuning; honors the R6 user redirect away
from dry same-family polishing).

## Files edited (record-break)
- constants/82a/current.md: held -> upper 0.2543185491 (REVIEWER-VERIFIED, was builder
  claim), Status stays `improved`, R7 milestone appended, note bumped to R7.
- constants/82a.md: new upper-bound table row `0.25432 | this repo (R7)` with full
  certificate description and reproduce command.
- README.md: constant 82 upper 0.25434 -> 0.25432.

## Note for future rounds
The lever is the DICTIONARY (Doche general-ell family), as the structure explore
predicted. Qa (height 1.290471, ABOVE the limit point) already helped 1.24e-5; a
genuinely smaller-height Q3, or a SECOND free block (Qb, 7 exponents), should help
more. The certificate slack here is ~1.07e-7, so the float optimum is the real lever —
push it with better Q3 candidates, not finer quadrature.
