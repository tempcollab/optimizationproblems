# Approach: UPPER bound via continuous optimization of Doche's limit-point integral h(q)

Status: PROPOSED (round 2). TOP-RANKED upper-bound attack. Supersedes the round-1
`upper-bound-perturbed-polys.md` (which was based on a mislabeled construction — it
treated the bound as a single small height; it is a LIMIT POINT). 

Moves: UPPER bound. Target to beat: **0.25444 = log(1.289735) [Doche Doc01b]**.
A record break = any q* (and any admissible {P_m, Q_i} dictionary) with a RIGOROUS
enclosure log h(q*) < 0.25443677.

---

## Background pinned this round (the calibration the explorer demanded)

Doche's limit-point measure is built in the symmetric variable X = z(1-z). The
Zhang-Zagier measure of an integer polynomial P(X) of degree d in X is (VERIFIED
this round against Doche's published heights H(P3)=1.272019650, H(P4)=1.288842118,
H(P5)=1.289442542, H(Qa)=1.290471208 — all reproduced to 9 digits):

    zeta(P) = exp( (1/d) * sum over X-roots X0 of [ log+ |z| + log+ |1-z| ] )

where the two z-roots of X0 are z = (1 + sqrt(1-4 X0))/2 and 1-z (symmetric pair),
and log+ w = max(0, log|w|).  KEY NORMALIZATION FACT (this is what broke the round-1
explorer's quick reconstruction and my first attempt): each X-root contributes BOTH
z-roots' max(1,|.|), and you normalize by the degree in X (NOT by the degree 2d in
z). Equivalently zeta is the ordinary z-variable absolute Mahler/ZZ measure.

The exact polynomials (from Doc01a, transcribed from the PDF this round) for the
*calibration* family (5 base polys + Q1 = Qa*Qb) are stored / re-derivable:

    P1(X) = X
    P2(X) = 1 - X
    P3(X) = X^4 - 2X^3 + 4X^2 - 3X + 1
    P4(X) = X^12 -3X^11 +8X^10 -18X^9 +36X^8 -62X^7 +97X^6 -123X^5 +114X^4 -73X^3 +31X^2 -8X +1
    P5(X) = X^12 -3X^11 +7X^10 -14X^9 +30X^8 -58X^7 +96X^6 -123X^5 +114X^4 -73X^3 +31X^2 -8X +1
    Qa(X) = X^24 -6X^23 +24X^22 -77X^21 +217X^20 -546X^19 +1252X^18 -2647X^17 +5195X^16
            -9457X^15 +15898X^14 -24521X^13 +34402X^12 -43345X^11 +48207X^10 -46413X^9
            +37963X^8 -25934X^7 +14558X^6 -6596X^5 +2357X^4 -642X^3 +126X^2 -16X +1
    Qb(X) = X^24 -5X^23 +16X^22 -39X^21 +85X^20 -180X^19 +385X^18 -796X^17 +1551X^16
            -2907X^15 +5421X^14 -10003X^13 +17368X^12 -26734X^11 +34951X^10 -37880X^9
            +33603X^8 -24203X^7 +14041X^6 -6486X^5 +2342X^4 -641X^3 +126X^2 -16X +1
    Q1 = Qa * Qb   (degree 48 in X)
    Calibration: h(17.9, 12.2, 0.9, 0.35, 0.29) = 1.2916673   [Doc01a]

Doc01b's RECORD family uses base polys {P1,P2,P4,P6,P8} (subset of P1..P8) plus two
perturbing factors Q1,Q2 in X, parameters q=(q1..q5), and reaches 1.289735. The full
P6,P8,Q1,Q2 coefficient lists for the record family are displayed as FORMULA IMAGES
in Doc01b and were NOT recoverable by pdfminer (the equations dropped). They must be
re-transcribed from the PDF figure pages by the builder, OR — and this is the cleaner
route — the builder works in the Doc01a calibration family (P1..P5 + Q1=Qa*Qb), which
IS fully recovered above, and simply re-optimizes q there. Doc01a's family already
gets 1.2916673; the question is only whether continuous optimization of q over THAT
recovered family already drops below 1.289735, or whether the Doc01b polynomial set
must be reconstructed to get there.

## The integrand (eq (9) of Doc01a, Jensen-reduced)

The double integral over [0,1]^2 collapses (t-integral via Jensen / formula (2)) to
a single integral. With k base polys P_m and one perturbing block Q1 (general l):

    f(q) = log M(Q1)  +  int_0^1  log+ | prod_{m=1}^k P_m(chi(s))^{q_m} / Q1(chi(s)) | ds
    chi(s) = e^{2 i pi s} (1 - e^{2 i pi s})
    h(q) = exp( f(q) )

WHERE M(Q1) here is the ZZ/z-variable absolute measure of Q1 (NOT the X-variable
Mahler measure — same normalization subtlety as above). CALIBRATION GATE: the builder
MUST reproduce h(17.9,12.2,0.9,0.35,0.29) = 1.2916673 to >=5 digits with the chosen
M(Q1) convention BEFORE trusting any optimizer output. (My round-2 sanity run with
M(Q1) = X-variable abs Mahler gave 1.32099 — WRONG; the z-variable normalization that
reproduced all four published heights above is the correct one and must be carried
into both the M(Q1) term and the log+ integrand.)

---

## Angle 1 (TOP): continuous optimization of q over the recovered Doc01a family

Skeleton:
  1. Re-implement zeta(P) and the eq-(9) integrand with the z-variable normalization
     verified above. CALIBRATION GATE: reproduce 1.2916673 at Doche's q. — by direct
     numerics, cross-checked against the 4 published single-poly heights.
  2. Minimize h(q) over q in R_+^5 by multistart (Nelder-Mead + L-BFGS with finite-diff
     or analytic d/dq of the integrand; the integrand is smooth in q away from the
     log+ kink). Seed from Doche's q and from coordinate-descent grids. — by scipy.
  3. If min over the Doc01a family already < 1.289735: that is a candidate break.
     If not (likely — Doc01a's optimum is ~1.2916, above the record), reconstruct the
     Doc01b record family {P1,P2,P4,P6,P8,Q1,Q2} from the PDF figure pages and
     re-optimize there. — by PDF transcription + same optimizer.
  4. RIGOROUS enclosure of log h(q*) at the optimizer's point: outward-rounded /
     interval Riemann sum (or Gauss-Legendre with an interval remainder bound) of the
     1-D s-integral, with guard intervals around (i) the log+ kink where
     |prod P^q / Q1| crosses 1, and (ii) the integrable log singularities where the
     integrand argument hits 0 on the contour s in [0,1] (bound the cell by the
     analytic local behaviour ~ log|s-s0|, which is integrable). Reuse the interval
     machinery style from the round-1 lower-bound certificate (fastiv.py). — by
     interval quadrature.
  5. Verify condition (4) holds for the chosen {P_m, Q_i} and exponents (the algebraic
     admissibility making the family a genuine sequence of integer polynomials), then
     cite Doc01a Lemmas 3,4,5: h(q*) is a limit point of V, hence C_82 <= log h(q*).
     — by checking (4) is satisfied (resultant/divisibility identity) + citation.

Hard step: **getting a rigorous UPPER enclosure of the 1-D integral that is itself
below log(1.289735), AND having the optimizer's q* actually beat the record.**
- Mechanism for the bound being an upper bound: h(q) is exactly the limit measure of a
  genuine integer-polynomial sequence (Doc01a Lemma 2 + Lemmas 3,4,5), so log h(q*) is
  a true upper bound on the essential minimum for ANY admissible q* — no optimality of
  q* is needed, only one admissible q* with a certified-from-above integral value below
  the record. The rigor lives entirely in the quadrature: outward rounding makes the
  Riemann/Gauss sum a guaranteed upper bound on the integral, the kink/singularity
  cells are bounded by integrable analytic tails.
- Mechanism for beating: the record was hand-tuned ("successive attempts"); a real
  optimizer over a SMOOTH 5-D objective essentially always improves a hand-tuned point,
  and the dictionary is admittedly "arbitrary" so enlarging it can only lower the min.
  Headroom is documented (smallest known single height 1.2875274 < 1.289735; true ess
  min likely <= ~0.2527).
- RISK: the Doc01a family's continuous optimum may sit at ~1.2916 (above the record) —
  i.e. the record's edge over Doc01a came from the BETTER POLYNOMIAL SET (P6,P8,Q2),
  not from finer q. If so, step 3's PDF reconstruction of the Doc01b family is REQUIRED
  to break, and the break margin (1.289735 -> ?) may be thin (a few e-4 to e-3).

Check the builder runs / reviewer reproduces: a script that (a) prints the calibration
value 1.2916673 from the recovered Doc01a family at Doche's q (sanity), (b) prints q*
and a NON-INTERVAL float h(q*) (the conjecture), (c) prints the rigorous outward-rounded
interval enclosure [lo, hi] of the integral with hi giving log h(q*) <= value <
0.25443677 (the certified bound), (d) verifies condition (4) for the family. Reviewer
re-runs and re-derives the quadrature upper bound independently.

## Angle 2: enlarge the polynomial dictionary, then optimize (orthogonal slack)

Same machinery as Angle 1 but expand {P_m} (add P3,P5,P6,P7,P8 — all small-height
base polys in X) and add more small-height perturbing factors Q_i in X, with more
q-parameters. Each admissible addition can only lower the achievable min of h(q).
Hard step: maintaining admissibility condition (4) as the dictionary grows (the
resultant/divisibility identity prod P_i | (Q_i - Q_j) heuristic Doche relied on),
and the same rigorous-quadrature enclosure. Best pursued AS PART OF Angle 1 step 3 —
if the recovered Doc01a family doesn't break, throw a wider admissible dictionary at
the optimizer rather than only transcribing Doc01b. Higher upside, slightly more setup.
Verification identical to Angle 1.

## Angle 3 (NOT recommended as primary): a fresh small-height integer-polynomial search

Breed new integer polynomials P(X) of degree ~28-48 with zeta(P) small, by LLL /
weighted integer transfinite diameter targeting roots clustered to make
log+|z|+log+|1-z| small, then use the BEST one as a new perturbing factor Q_i in the
limit-point family (NOT as a standalone height — a single height is only a spectrum
point, dead-ended in round 1). Hard step: the breeding search is heavy and uncertain,
and the payoff only matters once plugged into h(q). Strictly dominated by Angles 1-2
for this round (they reuse Doche's already-good dictionary). Keep as a later lever if
1-2 stall just above the record.

---

## Ranking

1. **Angle 1** first: the integrand and calibration are now PINNED and verified
   (4 published heights reproduced to 9 digits; the z-variable normalization
   identified), the optimization is cheap and smooth, the bound is an upper bound for
   ANY admissible q* (no optimality needed), and the verification is a clean 1-D
   rigorous quadrature. Lowest effort per unit of expected progress.
2. **Angle 2** folded in as Angle-1 step 3's escalation if the recovered Doc01a family
   doesn't already break — it is the most likely SOURCE of a clean margin, since the
   record's edge over Doc01a came from the polynomial set, not the q-tuning.
3. **Angle 3** only if 1-2 stall.

Even short of a break, a re-runnable rigorous RE-CERTIFICATION of 0.25444 (Angle-1
machinery evaluated at the record q with an interval enclosure) is a reviewer-verifiable
milestone the repo lacks on the upper side (the upper analogue of round 1's lower-bound
reproduction). Pair it as Stage A with the break attempt (Stage B) — banks progress
even if the margin proves thin.

## Spec review: REQUIRED
The break rests on (i) the exact integrand + normalization (now calibrated but the
Doc01b record-family polynomials still need PDF re-transcription), (ii) a rigorous
quadrature enclosure handling a log+ kink and integrable log singularities, and (iii)
the possibility that the Doc01a family alone doesn't beat the record (margin risk).
These are non-obvious feasibility/margin claims — review the outline before the builder
spends compute.
