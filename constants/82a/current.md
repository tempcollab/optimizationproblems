# C_82a — Essential minimum of the Zhang-Zagier height

## Status
improved

## Bounds
table: lower 0.24874 [F18, Flammang 2018] · upper 0.25444 [Doc01b, Doche 2001]
       (upper bar = log(1.289735) = 0.25443677 exactly)
held: lower 0.24874 (reviewer-verified, R1; RIGOROUS interval branch-and-bound
      certificate re-establishing Flammang's record. Reproduces, does NOT beat.)
      Reproduce: python3 constants/82a/certificate/verify_vec.py  (~30s).
      upper 0.2543185491 (REVIEWER-VERIFIED, R7 — RECORD BREAK tightening the
      reviewer-verified R6 held 0.2543309112 by 1.236e-5, still < Doc01b
      0.25443677). Rigorous outward-rounded max(A,B) quadrature enclosure of log h(q,qB)
      over an ENLARGED Doche family: base {P1,P2,P4,P6,P8}, FIXED distinguished block
      Q1*Q2 (deg 56, exponent 1), and a NEW free-exponent third perturbing block
      Q3=Qa (deg 24, H=1.290471208) with exponent qB. q=(12.040,9.380,2.462,1.711,
      0.581), qB=0.129; D = max(sum q_i deg P_i, 56+qB*24) = 59.096; frontier fully
      resolved (637808 leaves, 0 unresolved, 6 refine rounds), int_0^1 G ds <=
      15.0292089803, 15.0292089803/59.096 = 0.2543185491. Reproduce: python3
      constants/82a/certificate/verify_upper_q3.py certify 12.040 9.380 2.462 1.711
      0.581 0.129 200000 14 1e-10 (~3 min; prints admissibility of W=Q1*Q2*Q3,
      selftest_q3 0/200 on the CHANGED integrand, then CERTIFIED 0.2543185491).
      Anchor: verify_upper_q3.py anchor -> qB=0 reproduces the held R6 float
      0.2543308006 (integrand & D unchanged at qB=0). Admissibility of the enlarged
      dictionary (Doche Lemma 5: deg Q3=24>0, Q3(0)=Q3(1)=1, Q3 squarefree, deg W=80,
      W(0)=W(1)=1, gcd(Q3,P_i)=gcd(Q3,Q1)=gcd(Q3,Q2)=1) holds; q-independent.
      [PRIOR held, reviewer-verified R6: upper 0.2543309112, q=(11.73584,8.77354,
      2.44938,1.55411,0.53442), h=Q1*Q2 only, D=56, 633296 leaves; reproduce via
      certify_q.py 11.73584 8.77354 2.44938 1.55411 0.53442 200000 14 1e-10.]
      [superseded R5 value: upper 0.2543326887, q*=(11.74,8.77,2.45,1.55,0.53),
      628608 leaves, frontier=0; reproduce via verify_upper.py stageB.]

R4 builder CLAIM (now reviewer-VERIFIED in R5):
  Rigorous max(A,B) quadrature certificate (certify_maxAB in verify_upper.py):
  - STAGE A (re-cert):   C_82 <= log h(Doche q) <= 0.2544362773 < 0.25444.  [verified R5]
  - STAGE B (record-break): C_82 <= log h(q*) <= 0.2543326887 < 0.25443677,
    q* = (11.74,8.77,2.45,1.55,0.53), a STRICT break (margin 1.041e-4).  [verified R5]
  Both fully resolve (frontier=0). Selftest 0/300 violations vs mpmath; independent
  R5 cross-check vs mpmath Gauss-quad on 40 cells (worst cell_hi - ref = +8.3e-14).

Note: BMQS (arXiv:2601.18978, 2026) quote the weaker 0.248247 <= ess <= 0.254437 (Zagier/Doche)
and do NOT cite Flammang. The genuine verified bar (pre-R5) was the registry's lower 0.24874,
upper 0.25444 = log(1.289735); the upper is now improved to 0.2543185491 (R7).

## What this constant is
h_Z(alpha) = h(alpha) + h(1-alpha); C_82 = sup H such that {alpha : h_Z(alpha) <= H} is finite.
Equivalently the essential minimum of the Zhang-Zagier height. Lower bounds via Smyth's auxiliary-
function / semi-infinite LP method (Doche, Flammang). Upper bounds via small-measure polynomial
families (Doche). This is a CONTINUOUS optimization constant with a reproducible certificate
(auxiliary function + integrality-of-resultant argument) -- the AlphaEvolve-style tractable kind.

## Literature digested
- literature/flammang_F18_digest.md — the record lower bound 0.24874: method, certificate, slack.
- literature/doche_doc01b_digest.md — the record upper bound family (P1,P2,P4,P6,P8; Q=Q1*Q2).
- literature/bmqs_2026_digest.md — LP-duality framing; no new numeric bound; bar unchanged.
- literature/R7_explore_structure.md — proof-structure dissection; the free-exponent ell>1
  perturbing block is the named upper-side lever (Doc01a general-l family).
- literature/pdfs/flammang_zz_hal.pdf, doche_perturbed_doc01b.pdf, bmqs2601.18978.pdf

## Progress log
- R1: Reproduced the record method [F18] with an independent re-runnable RIGOROUS certificate: interval branch-and-bound (outward rounding, 2nd-order mean-value enclosure) certifies min_{t in [0,pi]} g(t) >= 0.24874 (worst cell 0.2487400; independent prec-200 true min 0.2487462), with the finite-exception (resultant-integrality) argument re-derived from scratch; all 24 Q_j confirmed in Z[w], all c_j>0. Verified, not a record-break.
- R5: RECORD BREAK on the UPPER bound. Independently verified C_82 <= log h(q*) <= 0.2543326887 < 0.25443677 = log(1.289735) [Doc01b], margin 1.041e-4, at q*=(11.74,8.77,2.45,1.55,0.53) in Doche's perturbed-polynomial limit-point family. Reproduced stageA (0.2544362773), stageB (0.2543326887, 628608 leaves, frontier=0), selftest (0/300), calib (h=1.2897342 = 1.289735 to 7 digits), admiss (Doche Lemma 5 holds for q*). Re-derived the load-bearing O(h^2) straddle bound from scratch (int_cell max(A,B) <= width*max(A_mid_up,B_mid_up) + max(slope)*r^2 + (1/3)max(curv)*r^3, via max(a+x,b+y)<=max(a,b)+max(x,y)) and matched it to the code incl. integration constants; confirmed leaf-only summation / exact tiling / all-outward-rounded; cross-checked the per-cell bound against an independent mpmath Gauss-quad (40 cells, worst cell_hi-ref = +8.3e-14); confirmed Q=Q1*Q2 family + D=56 normalization against the Doc01b PDF.
- R6: RECORD BREAK (further) on the UPPER bound. Independently verified C_82 <= log h(q) <= 0.2543309112 at re-optimized q=(11.73584,8.77354,2.44938,1.55411,0.53442) in the SAME Doche limit-point family (h=Q1*Q2, D=56), a STRICT tightening of the R5 certified 0.2543326887 (margin 1.7775e-6, still < Doc01b 0.25443677). Reproduced certify_q.py from scratch: CERTIFIED 0.2543309112, frontier fully resolved (633296 leaves, 0 unresolved, 6 rounds, int_0^2pi G dt <= 89.4884617019, int_0^1 G ds <= 14.2425310296, D=56). Re-confirmed admissibility (Doche Lemma 5) independently via sympy: deg Q=56>0, Q(0)=Q(1)=1, gcd(P_i,Q)=1 for all five P_i, all q_i>0 (admissibility is q-independent — same fixed dictionary as R5). Independently cross-checked the per-cell max(A,B) bound vs my own mpmath prec-160 Gauss-quad (mp.quad) on 50 random cells, both flat and full branches: 0 violations, worst cell_hi - true_int = +1.16e-17 >= 0. Independently reproduced the float log h(q)=0.2543308006 with my own midpoint Riemann sum (and the Doche-q calibration h=1.2897342) confirming the q ordering below q*. The certificate harness is the identical R5-verified max(A,B) quadrature with only the (positive) exponent vector changed; final arithmetic 14.2425310296/56 = 0.2543309112 re-derived by hand.
- R7: RECORD BREAK (STRUCTURAL) on the UPPER bound — first gain from ENRICHING the dictionary, not q-tuning. Independently verified C_82 <= log h(q,qB) <= 0.2543185491 in Doche's general-l (ell=1) perturbed family with a NEW free-exponent third perturbing block Q3=Qa (deg 24), q=(12.040,9.380,2.462,1.711,0.581), qB=0.129; a STRICT tightening of the R6 certified 0.2543309112 (margin 1.236e-5, still < Doc01b 0.25443677). Reproduced verify_upper_q3.py certify from scratch: CERTIFIED 0.2543185491, frontier fully resolved (637808 leaves, 0 unresolved, 6 rounds), int_0^2pi G dt <= 94.4313050433, int_0^1 G ds <= 15.0292089803, D = max(49.604, 56+0.129*24) = 59.096 (perturbing branch dominates). Confirmed the free-exponent formula B=log|Q1Q2|+qB*log|Q3|, D=2b*max(sum q_m deg P_m, deg Q_{l+1}+sum q_{k+m} deg Q_m) DIRECTLY against the Doc01a PDF (lines ~905-1180; perturbing side Q_{l+1}*prod Q_m^{q_{k+m}}, condition (4), Lemma 5) — it is genuine Doche, not an ad-hoc edit. Re-derived admissibility of the enlarged W=Q1*Q2*Q3 INDEPENDENTLY via my own sympy: deg Q_{l+1}=56>0, V=prod P^q coprime to W (gcd(P_i,W)=1 all five), W(0)=W(1)=1 (neither X nor 1-X divides W), Q3 squarefree, each Q non-constant => Lemma 5 + condition (4) hold for the multi-block construction. ANCHOR: at qB=0 the edited harness reproduces the held R6 float 0.2543308006 to >=10 digits and D collapses to 56 — proves Q3 genuinely extends and recovers the old family (the new value is a valid UPPER bound, not a broken-integrand artifact). selftest_q3 0/200 on BOTH branches of the CHANGED integrand. Independently cross-checked the per-cell max(A,B) enclosure vs my OWN mpmath prec-200 mp.quad on 40 cells (flat+midpt): 0 violations, worst cell_hi - true_int = +5.05e-14 >= 0 (outward-rounded). TAMPER test: feeding a bogus target 0.25431 (below truth) correctly reports BEATS=False — no grid fallback faking a proof. Final arithmetic 15.0292089803/59.096 = 0.2543185491 re-derived by hand.
