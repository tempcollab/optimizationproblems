# R4 digest — NON-energy / non-contour-LP lower-bound machinery for C_82a (ZZ ess. min)

Explorer R4. Bar to beat: **C_82 >= 0.2487458 = log(1.282416)** [Flammang F18, verified R1].
Brief: survey lower-bound machines that do NOT reduce to a pointwise auxiliary function on the
circles AND are NOT the (barred) OSS log-energy column. Four named angles: resultant/Bombieri-
Zannier; quantitative equidistribution (Bilu/Petsche/Favre-Rivera-Letelier); integer-Chebyshev /
transfinite diameter on the lemniscate; positive-definite-kernel / Polya smoothing distinct from L2.

## Load-bearing structural fact (the lens for all four angles)

The ZZ lower-bound proof loses ~0.19 of ~0.24 per-conjugate slack in the MIN-REDUCTION
`sum_i f(alpha_i) >= d * min_PLANE f` (role memory R3, verified: roots of the smallest-height ZZ
poly sit on the lemniscate |z(1-z)|=const at |z| in [0.51,1.98], NONE within 0.02 of |z|=1, where
mean_nu f ~0.44 >> the on-circle min 0.249). Recapturing it rigorously requires controlling WHERE
the conjugate measure nu actually sits — i.e. an equidistribution / lemniscate-support argument.
EVERY rigorous handle on "where nu sits" in the literature routes through LOGARITHMIC ENERGY, which
is barred for ZZ and goes trivial at capacity 1 (the |z|=1 circles have capacity 1). This is the
wall all four angles hit. Details below.

## Angle 1 — Quantitative equidistribution (Bilu / Petsche / Favre-Rivera-Letelier). VERDICT: CIRCULAR, capacity-1 trivial.

Favre-Rivera-Letelier [FR06] Thm 3.1 (the dimension-1 quantitative Bilu, re-read verbatim from
D'Andrea-Narvaez-Clauss-Sombra arXiv:1606.04299 §3, PDF on disk frl_equidist_jtnb.pdf): there is
C0 <= 15 such that for every C^1 function f on P^1(C) and every algebraic alpha,
  | int f dmu_S - int f dlambda_{S^1} | <= Lip_sph(f) * ( pi/deg(alpha) + (4 h(alpha) + C0 log(deg+1)/deg)^{1/2} ).
Here mu_S = Galois orbit measure, lambda_{S^1} = UNIFORM measure on the unit circle.

WHY IT FAILS for a ZZ lower bound (two independent killers):
1. CIRCULARITY. The error term is dominated by (4 h(alpha))^{1/2}. To deduce a LOWER bound on
   h_Z from "nu close to equilibrium" you would write mean_nu f >= mean_lambda f - Lip(f)(4h)^{1/2}
   and solve for h — but the (4h)^{1/2} term ALREADY contains the quantity you are bounding, and the
   inequality only CONSTRAINS the orbit when h is KNOWN SMALL; it gives no positive lower bound on h.
   (It is an equidistribution-RATE statement: small height => near-equidistributed; it does not, and
   cannot, manufacture a height floor from below.)
2. WRONG TARGET MEASURE / CAPACITY 1. FR06 equidistributes to lambda_{S^1} (unit circle, the relevant
   equilibrium measure has CAPACITY 1). The ZZ slack lives precisely in the GAP between nu (on the
   lemniscate, off the circle) and this circle measure — but the quantitative bound's leverage VANISHES
   at capacity 1 (this is the same capacity-1 inertness the user's no-go and BMQS Thm B already cite for
   the energy cut). The bound says nu is near the circle; it says nothing that separates mean_nu f from
   the on-circle value in the direction needed.

Petsche [Pet05] (thesis, UT Austin) is the same statement via Fourier inversion + Erdos-Turan-Mahler
character-sum estimates — i.e. it IS a logarithmic-energy / discrepancy machine. Same two killers.
CLOSED.

## Angle 2 — Resultant / Bombieri-Zannier / "house" lower bounds. VERDICT: wrong hypothesis class; not transferable.

Bombieri-Zannier height lower bounds (and the modern descendants, e.g. arXiv:2404.11559 "points of
small height in infinite extensions") are LOCAL/SPLITTING results: they lower-bound h(alpha) when
alpha lies in a field with prescribed RAMIFICATION/SPLITTING at fixed primes (totally p-adic numbers,
asymptotically positive extensions). Their engine (arXiv:2404.11559 Lemma 3.1, re-read) is the
"relative Mahler inequality" = bound the DISCRIMINANT from below via Hadamard on the Vandermonde =
the log|disc| / log-energy quantity. Two problems for ZZ:
1. NO SPLITTING HYPOTHESIS. ZZ ranges over ALL algebraic numbers; ZZ-minimal numbers have no special
   splitting, so the prime-splitting lower bound is simply absent (it bounds a DIFFERENT, larger
   constant for a sub-class).
2. The discriminant/Hadamard mechanism IS the barred energy column: I(nu)=(1/d^2)log|disc| can be
   NEGATIVE for non-integer alpha (role memory: P=10z^2-6z+1 gives I(nu)=-0.80<0). For ZZ over all
   algebraic numbers disc is not forced large, and the (2d-2)log a leading-coeff penalty kills it.
The "coupling of a place of alpha with the conjugate structure of 1-alpha" is real but is exactly the
w=z(1-z) symmetric reduction Flammang ALREADY exploits; a genuinely coupled (z,1-z) column is
inadmissible (prod = Res/a^deg < 1 for non-integer alpha; role memory R3, verified). CLOSED.

## Angle 3 — Integer-Chebyshev / integer transfinite diameter on the lemniscate. VERDICT: = Flammang's own method.

Pritsker "Heights of polynomials over lemniscates" (arXiv:2101.06708, re-read): the lower-bound
mechanism is potential-theoretic — logarithmic energy / equilibrium measure on the lemniscate level
set |p(z)|=r. Same barred energy mechanism, capacity-dependent.
Flammang-Rhin-Smyth "integer transfinite diameter of intervals" (JTNB 1997) and the whole integer-
Chebyshev family: role memory R3 (verified against F18 §2.2) — the weighted INTEGER transfinite
diameter t_{Z,phi} tied to the lemniscate contour IS Flammang's auxiliary-function LP in another
language (F18 eq 2.1 is literally the t_{Z,phi} of the ZZ lemniscate). "Borrowing it" recovers the
contour LP, which R3 rigorously CEILINGed at 0.2487857. NOT a distinct machine. CLOSED.

## Angle 4 — Positive-definite-kernel / Polya smoothing distinct from L2 energy. VERDICT: no non-energy PD kernel exists here.

Any conjugation-invariant lower-bound functional of nu that is (i) computable from the minimal poly
via an arithmetic integrality (resultant / discriminant) and (ii) bounded below for ALL ZZ-minimal
nu, is — by BMQS Thm B (verified R1) — NOT independent of the int log|Q| dnu>=0 columns. The only
positive-definite kernel with arithmetic content on Galois orbits is the LOG kernel (-> energy/disc),
which is barred. A Polya/smoothing kernel WITHOUT arithmetic content (e.g. a Fejer/Gaussian
mollifier) gives an analytic inequality with NO integrality drop-out, so its "column" does not drop
and yields no bound (same failure as a non-integer-poly column). There is no published or evident PD
kernel for this problem that is both arithmetic and non-log. CLOSED (subject to the longshot caveat
in the report: a NON-energy containment lemma is the only conceivable opening, and none is known).

## One-line synthesis

All four named non-energy angles, when made rigorous, collapse onto ONE of: (a) the barred
logarithmic-energy/discriminant mechanism (Angles 1,2,4 and Pritsker lemniscate), which is also
capacity-1 trivial on the ZZ circle; or (b) Flammang's own integer-transfinite-diameter contour LP
(Angle 3), already CEILINGed at 0.2487857. No orthogonal lower-bound machine survives. The ZZ lower
bound is genuinely hard: it is stuck at Flammang for the same reason across every framing — the only
rigorous handle on the off-circle conjugate mass is log-energy, and log-energy is barred + inert here.

## Sources read this round (primary text)
- Favre-Rivera-Letelier [FR06] Thm 3.1 (quantitative Bilu, dim 1), via arXiv:1606.04299 §3
  (frl_equidist_jtnb.pdf on disk) — exact discrepancy bound transcribed above.
- D'Andrea-Narvaez-Clauss-Sombra, arXiv:1606.04299 (N-dim quantitative Bilu) — body read; same
  log-energy/Fourier mechanism, rate exponent 1/2 in h.
- Fili-Petsche "Energy integrals over local fields and global height bounds" (arXiv:1306.3544) —
  height lower bound = mutual log-energy I(mu,nu)>=0, TRIVIAL at capacity 1. = barred mechanism.
- Pritsker "Heights of polynomials over lemniscates" (arXiv:2101.06708) — lemniscate lower bound is
  log-energy/equilibrium-measure. = barred mechanism.
- arXiv:2404.11559 (points of small height in infinite extensions) — relative-Mahler/Hadamard-
  discriminant lower bound; splitting-condition hypothesis absent for ZZ; = energy/disc, barred.
- Bombieri-Zannier / totally-p-adic small-height (search-confirmed) — splitting-class only, not a
  general ZZ lower bound.
</content>
</invoke>
