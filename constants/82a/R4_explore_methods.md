# R4 explore — NON-energy, non-contour-LP LOWER-bound machinery map for C_82a

Explorer R4 (distinct angle: methods that do NOT reduce to a pointwise auxiliary function on the
circles and are NOT the OSS energy column). Does NOT attempt the improvement.

## 82a  (C_82: essential minimum of the Zhang-Zagier height h_Z(alpha)=h(alpha)+h(1-alpha))
- Current bounds: lower = **0.2487458 = log(1.282416)** [F18, Flammang 2018, verified R1] ·
  upper = 0.2540419719 [this repo R11, verified] (table/record upper Doc01b 0.25444).
- TARGET this run = the LOWER bound. Bar to beat: 0.2487458 (NOT the retracted R14-R17 OSS values).

### Softer target: the lower bound is NOT the softer target — but it is the ASSIGNED target.
The upper side is the demonstrably pushable frontier (6 straight record-breaks R5-R11, held
0.2540419719). The LOWER side is, after R1-R3, provably stuck for every screenable/known method.
The user's standing focus is the LOWER bound; this report maps the non-energy lower-bound terrain
honestly and the bottom line is a research-longshot verdict, not a cheap lever.

### How the record was achieved (from the papers, re-confirmed)
- **Lower [F18]:** Smyth auxiliary function `f(z)=log+|z|+log+|1-z| - sum_j c_j log|Q_j(z(1-z))|`,
  Q_j in Z[w], w=z(1-z), c_j>0; min over |z|=1 gives `zeta(alpha) >= 1.282416`. Rigor = resultant-
  integrality drop-out `prod_i Q_j(alpha_i(1-alpha_i)) = Res(P,Q_j(z(1-z)))` a nonzero integer
  (needs a=1; the ess-min is realized on integers via the +2log a/d Weil penalty). Search = weighted
  integer transfinite diameter + LLL, k=5..32. Doche->Flammang gain was only +5e-4.
- **Upper [Doc01b + repo R5-R11]:** Doche perturbed-polynomial limit-point family h=Q1*Q2*(perturbers),
  free-exponent blocks; certified by outward-rounded max(A,B) quadrature enclosure.

### Where the slack is (the lens for every angle)
~0.19 of the ~0.24 per-conjugate gap is the **MIN-REDUCTION** `sum_i f(alpha_i) >= d*min_PLANE f`,
NOT the column dictionary (~0.05, R3-ceilinged). Verified: roots of the smallest-height ZZ poly lie
on the lemniscate |z(1-z)|=const (|z| in [0.51,1.98], none within 0.02 of |z|=1), where
mean_nu f ~0.44 >> on-circle min 0.249. A raise MUST control where the conjugate measure nu sits.

---

## Ranked map of NON-energy, non-contour-LP mechanisms (with cheap-lever-vs-longshot verdict)

**THE WALL (read first):** every rigorous handle on "where nu sits" in the entire height literature
routes through LOGARITHMIC ENERGY (mutual energy I(mu,nu)>=0 / log|disc|). For ZZ that mechanism is
(a) BARRED (user four-mechanism no-go, R1) and (b) capacity-1 TRIVIAL on the |z|=1 contour (BMQS
Thm B: the energy constraint is not independent of the log|Q| columns; the circle has capacity 1).
All four named non-energy angles collapse onto this wall or onto Flammang's own contour LP. Below,
ranked by remaining (slim) tractability.

### #1 (softest of a hard field) — Quantitative equidistribution (Bilu / Petsche / Favre-Rivera-Letelier).  LONGSHOT, leaning DEAD.
- WHAT: FR06 Thm 3.1 (transcribed verbatim from arXiv:1606.04299 §3): for every C^1 f and every alpha,
  `|int f dnu - int f dlambda_{S1}| <= Lip(f) * ( pi/d + (4 h(alpha) + C0 log(d+1)/d)^{1/2} )`, C0<=15,
  lambda_{S1} = uniform on the unit circle.
- WHY IT IS THE NAMED "control how far nu sits from the minimizer" angle: it is literally a
  quantitative discrepancy between nu and a reference measure.
- WHY IT FAILS (two independent killers, verified from the theorem statement):
  1. **CIRCULAR.** The error term is (4 h)^{1/2} — it CONTAINS the height you want to bound. The
     inequality only says "small height => near-equidistributed"; it cannot manufacture a height floor
     from below. Solving mean_nu f >= mean_lambda f - Lip(f)(4h)^{1/2} for h gives no positive bound.
  2. **CAPACITY-1 / WRONG TARGET.** It equidistributes to the UNIT CIRCLE measure (capacity 1), the
     exact locus where the energy leverage vanishes and where the ZZ slack is NOT (the slack is the
     off-circle lemniscate mass). The bound pushes nu TOWARD the circle; the slack needs it held OFF.
- VERDICT: **LONGSHOT bordering DEAD.** The only conceivable non-circular escape would be a
  DIFFERENT, height-INDEPENDENT containment lemma (a deterministic region where ZZ-minimal roots
  must lie, proved from the minimal polynomial's coefficient structure, NOT from h). None is known;
  inventing one is open research, not a build. Do not commit a build to FR06/Petsche as stated.

### #2 — Resultant / Bombieri-Zannier / "house" coupling of alpha and 1-alpha.  DEAD (wrong hypothesis + reduces to barred/closed).
- WHAT: lower-bound h via the coupled conjugate structure of alpha and 1-alpha, a la Bombieri-Zannier
  / house / relative-Mahler discriminant bounds.
- WHY DEAD: (i) Bombieri-Zannier-type bounds need a SPLITTING/RAMIFICATION hypothesis (totally p-adic,
  asymptotically positive extensions; arXiv:2404.11559) that ZZ-minimal numbers do not have — they
  bound a different, larger constant for a sub-class. (ii) Their engine (relative Mahler / Hadamard on
  the Vandermonde) IS log|disc| = the barred energy column (I(nu)<0 for non-integer alpha, verified).
  (iii) The genuine alpha<->1-alpha coupling is exactly the w=z(1-z) symmetric reduction Flammang
  already uses; a coupled (z,1-z) column is inadmissible (prod=Res/a^deg<1 for non-integer alpha,
  verified R3). No new slack. CLOSED — do not retry.

### #3 — Integer-Chebyshev / integer transfinite diameter on the lemniscate.  DEAD (= Flammang's own method).
- The weighted integer transfinite diameter t_{Z,phi} on the ZZ lemniscate IS Flammang's auxiliary-
  function LP (F18 §2.2; verified R3). Pritsker's lemniscate height bounds (arXiv:2101.06708) are
  log-energy/equilibrium-measure = barred. Either framing recovers the contour LP, which R3
  rigorously CEILINGed at 0.2487857 (+4e-5 over Flammang). NOT a distinct machine. CLOSED.

### #4 — Positive-definite-kernel / Polya smoothing distinct from L2 energy.  DEAD (no arithmetic non-log PD kernel).
- The only PD kernel on Galois orbits with arithmetic drop-out is the LOG kernel (-> energy/disc),
  barred. A smoothing/Polya kernel WITHOUT arithmetic content has no integrality drop-out, so its
  column does not drop and yields no bound (same failure as a non-integer-poly column). BMQS Thm B:
  any admissible nu-functional is in the span of the int log|Q| dnu>=0 columns — there is no
  independent non-log PD kernel to exploit. CLOSED.

---

## SINGLE SOFTEST TARGET (honest)
If a build is mandated on the LOWER side, **#1 (quantitative equidistribution)** is the only angle
not already rigorously ceilinged or barred — but it is a research LONGSHOT whose load-bearing step
is currently MISSING, not just hard. Expected outcome of any honest attempt = a clean reproducible
VERIFIED-NEGATIVE (the FR06 bound is circular/capacity-1-inert for a ZZ height floor), which is still
a logged milestone. There is NO cheap lever on the lower side.

## THE ONE HARD STEP (for #1, if attempted)
Replace the height-dependent equidistribution error `(4 h)^{1/2}` by a **height-INDEPENDENT
containment lemma**: prove a deterministic region R (off both circles, on/inside the lemniscate)
such that EVERY conjugate of EVERY ZZ-minimal algebraic number lies in R, using only the integrality/
coefficient structure of the minimal polynomial (NOT log-energy, NOT the height itself). Then
`mean_nu f >= min_R f > min_circle f` would recapture part of the 0.19 min-reduction slack. No such
lemma is known; constructing one is the open problem. (Any version that invokes log|disc| or the
height is barred/circular.)

## Dead ends (do NOT retry) — confirmed this round against primary text
- OSS log-energy / discriminant / multivariate-integrality column, any form: barred (user no-go, R1).
- Quantitative equidistribution as STATED (FR06/Petsche/Bilu): circular (error ~ h^{1/2}) AND
  capacity-1 inert on the unit circle. Verified from FR06 Thm 3.1 verbatim.
- Resultant / Bombieri-Zannier / house / relative-Mahler-Hadamard: splitting-hypothesis class only +
  = log|disc| energy + coupled (z,1-z) inadmissible (Res/a^deg<1). CLOSED.
- Integer-Chebyshev / integer transfinite diameter / Pritsker lemniscate: = Flammang's contour LP,
  R3-CEILINGed at 0.2487857 / log-energy. CLOSED.
- Polya / PD-kernel non-energy column: no arithmetic non-log kernel; BMQS Thm B closes the span.
- (prior rounds) w-products, asymmetric-z, k>32/lobe LLL, integer-locus, BMRL transfer, continuum-SOS:
  all closed/ceilinged R1-R3.

## STRATEGIC CALL
The lower side of 82a is, across every framing examined R1-R4, stuck at Flammang for ONE reason: the
only rigorous handle on the off-circle conjugate mass is logarithmic energy, which is both barred and
capacity-1 inert here, and every "non-energy" alternative in the literature reduces to it (or to the
already-ceilinged contour LP). A genuine raise needs a NEW height-independent containment idea that
does not yet exist. Recommend: scope any lower-side round as a longshot expected to log a verified-
NEGATIVE; if the user releases the lower-bound focus, the UPPER side (held 0.2540419719) is where
verified raises remain reachable.

## Digests saved
- constants/82a/literature/R4_nonenergy_methods_digest.md (full angle-by-angle digest, sources).
- PDFs added: constants/82a/literature/pdfs/frl_equidist_jtnb.pdf (arXiv:1606.04299, FR06 Thm 3.1).
  (Already on disk and reused: sss_2401.03252 [OSS], potential_energy_2202.05235, morales_2201.11174,
  bmrl_faltings_1609.00071, flammang_zz_hal, doche_*, bmqs2601.18978.)
</content>
