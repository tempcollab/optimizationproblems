# Digest: Doche [Doc01b] "Zhang-Zagier heights of perturbed polynomials" (J. Théor. Nombres Bordeaux 13 (2001) 103-110)

Source PDF: constants/82a/literature/pdfs/doche_perturbed_doc01b.pdf (numdam JTNB_2001__13_1_103_0). Text /tmp/doc01b.txt.

## What it achieves (the RECORD UPPER bound)
Theorem: the smallest limit point of V = { zeta(alpha) : alpha in Qbar } is < 1.289735.
Hence C_82 = ess min h_Z <= log(1.289735) = 0.25443677 ==> registry's 0.25444. CONFIRMED.
(Improves the previous limit-point bound 1.2916674 from Doc01a.)

## CRUCIAL STRUCTURAL FACT (corrects the round-1 mislabel)
The upper bound is a LIMIT POINT of the spectrum, NOT a single algebraic number's height.
- The round-1 doc claimed the upper bound was "a degree-32 example with measure 1.287527" --
  WRONG. 1.287527 (more precisely 1.2875274) is the *smallest single known height*, and it is
  BELOW the record upper bound 1.289735. A single small height does NOT bound the essential
  minimum (the ess min needs an INFINITE set below H; one alpha gives only a spectrum point).
- The record 1.289735 is the value of an explicit CONTINUOUS function h(q) at an optimized
  real parameter vector q. The bound is rigorous because Doche's Lemma (from Doc01a, Lemmas
  3,4,5) turns the limit value h(q) into a genuine sequence of distinct irreducible algebraic
  numbers whose heights -> h(q), making {alpha : h_Z(alpha) <= H} infinite for H = log h(q)+eps.

## The construction (the perturbed-polynomial / limit-point integral)
- Work in the variable X = z(1-z) (the symmetric coordinate; w in Flammang's notation). This is
  the key change over Doc01a (where the search was in z): it allows MORE perturbing factors.
- Take base polynomials P1,P2,P4,P6,P8 (a subset of P1..P8, selection "forced by the search of
  the minimum") and two perturbing factors Q1(X), Q2(X) "chosen for their very small height"
  (and because a product of P_i's divides Q1 - Q2 -- the resultant heuristic).
- Form the family parameterized by rationals q = (q1,...,q5) in Q_+^5, and the limit measure is
      h(q) = exp( double integral over [0,1]^2 of
                 log| ( prod_m P_m(chi(s))^{q_m} ) - e^{2 i pi t} Q1(chi(s)) | / |...| dsdt ),
  with chi(s) = e^{2 i pi s}(1 - e^{2 i pi s}) = the X-coordinate on the relevant circle.
  (Doc01a eq (6)/(9); the t-integral collapses to a log+ via Jensen so it is effectively a
  SINGLE integral over s of a log+ of the family value -- "easily computed by Riemann sum".)
- MINIMIZE h(q) over q. Doche: "we search the best q_i in order to have the smallest limit
  point possible ... we test several choices of q_i" -- a MANUAL / trial search, not a solver.
- Best q found (Doc01b): yields limit point < 1.289735. (Doc01a's best q = (17.9,12.2,0.9,
  0.35,0.29) gave 1.2916673 with the 5-poly z-variable family.)

## Slack / where the upper bound is LOOSE (this is the soft target)
1. h(q) is a SMOOTH function of a low-dim real vector q. Doche minimized it BY HAND
   ("successive attempts", "many attempts"). A real continuous optimizer (Nelder-Mead /
   L-BFGS / multistart, or coordinate descent + grid) over q will almost certainly find a
   lower h than his hand-tuned value -> a smaller limit point -> a strictly better upper bound.
   This is the single most-exploitable opening and is exactly the AlphaEvolve-style case:
   minimize a cheap, smooth, low-dim explicit integral.
2. The CHOICE of polynomials {P_m} and perturbing factors {Q_i} is "arbitrary" (Doche's word).
   A wider dictionary of small-height base/perturbing polynomials in X (e.g. add P3,P5,P7, more
   Q's, or new small-height factors) enlarges the family and can only lower the achievable min.
3. The smallest known single height 1.2875274 is already BELOW the record limit point 1.289735.
   Doche conjectures the smallest limit point is < 1.2875274 ("if this speculation was right").
   So the truth is very likely below log(1.2875274) = 0.25272 -- headroom of >= 0.0017 below the
   current upper record just to reach that, with the real ess min plausibly near ~0.2527 or a bit
   lower (still well above the lower bound 0.24874).

## Verification (what a reviewer reproduces for an upper-bound break)
To certify C_82 <= log h(q*) for an optimized q*:
 (a) confirm condition (4) holds for the chosen (P_m, Q_i) and exponents (an algebraic identity
     making the family a valid sequence of integer polynomials -- the structural admissibility);
 (b) compute the double integral h(q*) with a RIGOROUS quadrature enclosure (interval/outward-
     rounded Riemann sum or Gauss with remainder bound) so log h(q*) is a certified UPPER value;
 (c) cite Doc01a Lemmas 3,4,5: h(q*) is a genuine limit point of V, so C_82 <= log h(q*).
The integrand has a mild log+ kink and possible log singularities where the family value hits 0
on the contour -- the quadrature enclosure must handle those (they are integrable; bound on a
guard interval), the same care as the lower-bound min certificate.

## Dead end noted
Do NOT try to bound C_82 by exhibiting a single small-height alpha (e.g. the 1.2875274 poly):
a single height is a spectrum POINT, not a bound on the essential minimum. The bound MUST come
from a limit point (an infinite family), i.e. from minimizing h(q).
