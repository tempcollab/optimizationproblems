# R4 approach — min-vs-mean / effective-equidistribution route for the C_82a LOWER bound

Status: **OPEN / no cheap or screenable lever found this round.** Verified-NEGATIVE on
the only known tool (FR06 / Petsche effective equidistribution), plus a load-bearing
CORRECTION of the wrong R3 root-location diagnosis. This is NOT a blanket closure of
the min-vs-mean mechanism.

Target to beat: **C_82 >= 0.2487458 = log(1.282416)** [Flammang F18, verified R1].
No raise is claimed. Deliverable = a reproducible verified-NEGATIVE milestone.

Artifacts:
- `../certificate/gap_diagnostic.py` (+ `gap_diagnostic.json`) — the root-location
  correction, reproducible. Run `python3 gap_diagnostic.py` and
  `python3 gap_diagnostic.py selftest`.
- This note — the equidistribution-route obstruction, with the FR06 theorem verbatim
  and the circularity made numeric.

---

## 0. The lower-bound identity and the ONLY non-barred live mechanism

For a ZZ-minimal algebraic number alpha of degree d with conjugates alpha_1..alpha_d
(and their images z_i in the z-plane), Flammang's auxiliary function gives, by
resultant-integrality drop-out of the integer columns Q_j,

    h_Z(alpha) = (1/d) sum_i sigma_ZZ(z_i)  >=  (1/d) sum_i f(z_i),

where  f(z) = sigma_ZZ(z) - sum_j c_j log|Q_j(z(1-z))|,  sigma_ZZ = log+|z| + log+|1-z|.
Flammang then bounds  (1/d) sum_i f(z_i) >= min_{|z|=1} f = 0.2487462  (the MIN
reduction). The ONLY way to beat Flammang WITHOUT a new integer column (the column
dictionary is R3-ceilinged at 0.2487857) is a **min-vs-mean** improvement:

    (1/d) sum_i f(z_i)  >=  circle-min f  +  delta,     delta > 1.5e-4  uniformly in d,

i.e. exploit that the conjugate measure nu = (1/d) sum delta_{z_i} cannot concentrate
at the single binding lobe, so its f-MEAN exceeds the circle MIN. Every barred/closed
route (OSS energy, multivariate-integrality, power-sum, resultant LP, contour-LP/Z[w]/
SOS, asymmetric-z, k>32 LLL, integer-locus, BMRL) is excluded by run_state Rules; the
min-vs-mean route is the only one left to assess. This note assesses it.

---

## 1. CORRECTION of the wrong R3 root-location diagnosis (the load-bearing fix)

The run_state R3 Rule and the math-explorer memory asserted:

  > "~0.19 of the slack is the MIN-REDUCTION; ZZ-minimal roots sit OFF both circles on
  >  the lemniscate |z(1-z)| = const where mean_nu f ~ 0.44 >> 0.249."

**This is WRONG.** `gap_diagnostic.py` recomputes, across ALL 24 Flammang Table-1 polys,
the roots z of Q_j(z(1-z)) = 0, their distance to the two circles, and mean sigma_ZZ.
The corrected, reproducible picture (selftest cores [A]-[E], all PASS):

- **Roots HUG the two circles.** For deg_w >= 12 the mean distance to {|z|=1 or
  |1-z|=1} is 0.012-0.034 and the max is usually < 0.05 (j=13 max 0.025, j=15 0.030,
  j=17 0.038, j=23 0.050). There is NO far-lemniscate mass.
- **The |z| in [0.5, 2.0] spread is the OTHER circle, not off-circle.** A root with
  |z| ~ 1.97 has |1 - z| ~ 1, i.e. it sits on the second circle |1-z|=1. The two
  circles together produce the [0.5,2.0] modulus range; every such root is within
  ~0.05 of one of them.
- **mean sigma_ZZ ~ 0.24-0.27, NOT 0.44** (j=8 0.260, j=13 0.254, j=15 0.253,
  j=17 0.256, j=24 0.271). The honest ZZ height density does not reach 0.44 anywhere
  in the substantive sequence.
- **The bogus "0.44" is the FULL-f-WITH-SELF artifact on the tiny deg-8 poly j=5.**
  Evaluating the FULL f (including its OWN term -c_5 log|Q_5(w)|) AT the roots of
  Q_5(z(1-z)) = 0 gives -c_5 log|0| = +inf at exactly those points, inflating the
  "mean f" to 0.4320 (selftest core [D]). That single tiny poly's inflated number was
  over-generalized into "mean_nu f ~0.44 for all ZZ polys." It is a numerical artifact:
  a genuine ZZ-minimal P is coprime to each Q_j, so log|Q_j(alpha(1-alpha))| is finite.
  j=5's honest mean sigma_ZZ is 0.2406 and its roots lie exactly ON the circles.

**Consequence:** the correct slack is the min-vs-mean gap on the cross-aux f (f with the
self term removed, since P is coprime to Q_j), NOT an off-circle lemniscate leak. The
R3 lemniscate Rule must be retracted; this note + `gap_diagnostic.py` supply the
replacement.

---

## 2. The MEAN gap PERSISTS; the MIN gap collapses (do NOT confuse them)

This is the scope correction the outline-review (Defect 1) demanded. The min-vs-mean
mechanism uses the **MEAN** gap  ( mean_root f - circle-min ), NOT the **MIN** gap.
From `gap_diagnostic.py` (f = cross-aux, self term excluded; selftest core [E]):

```
 deg_w   MIN gap     MEAN gap
   12    +0.00106    +0.00474
   12    +0.00022    +0.00375
   16    -0.00199    +0.00356      <- MIN goes NEGATIVE, MEAN stays positive
   16    -0.00200    +0.00852
   16    +0.00202    +0.00634
   17    -0.00003    +0.00834
   17    +0.00143    +0.00487
   20    -0.00152    +0.00985
   22    -0.00133    +0.00519
   22    -0.00281    +0.02070
   22    +0.00010    +0.00870
   22    +0.00007    +0.02014
```

- The **MIN gap collapses toward (and below) 0** as degree grows — at deg_w >= 16 it
  ranges in [-0.00281, +0.00202]. A "shrinking gap => route dead" argument that reads
  THIS column (as the R4 outline originally did) is reading the WRONG column.
- The **MEAN gap stays positive and persistent**, in [+0.00356, +0.02070] at
  deg_w >= 16 — one to two orders of magnitude ABOVE the 1.5e-4 a raise would need.

So the genuine min-vs-mean slack is **healthy in this data**: the conjugate measure's
f-MEAN sits a robust +0.003 to +0.02 above the circle min, even as individual
conjugates reach (and pass below) the binding lobe. The mechanism is NOT killed by a
collapsing gap.

**Important honesty caveat (outline-review Defect 3).** This sequence is Flammang's
near-extremal Table-1 AUX polynomials, NOT the minimal polynomials of actual small-
height ZZ numbers. The mean-gap data is suggestive, not a proof: it shows the slack is
real and does not collapse on the family we can compute, but it does NOT establish a
degree-uniform mean floor for ALL ZZ-minimal alpha. Establishing such a floor is
exactly what Section 3 shows the known tool cannot do.

---

## 3. The FR06 / Petsche tool CANNOT cash the mean gap (verified-NEGATIVE)

The genuine question is: can the persistent positive mean gap be converted into a
**degree-uniform** floor delta > 1.5e-4 valid for ALL ZZ-minimal alpha? The only known
device for "the conjugate mean exceeds the circle value" is **effective
equidistribution**. We state the tool verbatim and show it cannot do it.

### 3.1 The theorem, verbatim (source-checked)

Favre & Rivera-Letelier, via D'Andrea-Narvaez-Clauss-Sombra, "Quantitative equidistri-
bution of Galois orbits of points of small height on the torus" (arXiv:1606.04299),
§3, **Theorem 3.1** (PDF on disk `literature/pdfs/frl_equidist_jtnb.pdf`, transcribed
verbatim):

  > **Theorem 3.1.** There is a positive constant C0 <= 15 such that for every
  > C^1-function f : P^1(C) -> R and every xi in Qbar^x,
  >
  >   | int_{P^1(C)} f dmu_S  -  int_{P^1(C)} f dlambda_{S^1} |
  >        <=  Lip_sph(f) * ( pi/deg(xi) + ( 4 h(xi) + C0 * log(deg(xi)+1)/deg(xi) )^{1/2} ),
  >
  > where S is the Galois orbit of xi, mu_S the discrete probability measure associated
  > to it, lambda_{S^1} the uniform (Haar) measure on the unit circle |z|=1, and
  > Lip_sph the Lipschitz constant w.r.t. the spherical distance on the Riemann sphere.
  > (In particular, if h(xi) <= 1 the bound holds with C0 replaced by C <= 64.)

Here mu_S is our nu (the conjugate measure), and h(xi) is the standard logarithmic
Weil height. This is the dimension-1 quantitative Bilu equidistribution theorem.

### 3.2 Defect A — CIRCULAR (the error contains the height being bounded)

The mechanism would have to read Theorem 3.1 as a LOWER bound on the f-mean:

    mean_nu f  >=  mean_lambda f  -  Lip(f) * ( pi/d + (4 h + C0 log(d+1)/d)^{1/2} ).      (*)

To beat Flammang we need the right-hand side >= circle-min + 1.5e-4. But the right-hand
side contains  h = h(xi) = h_Z(alpha)/2 + (the part on 1-alpha)  — i.e. **the very
height we are trying to bound from below appears, with a + sign under a square root, in
the error term.** Solving (*) for a floor on h is circular: a large h makes the bound
VACUOUS (the error grows like (4h)^{1/2}); a small h is exactly what we cannot assume.
The inequality is a *rate* statement — "small height => orbit near-equidistributed" —
and by construction it cannot manufacture a height floor from below.

**Made numeric (reproducible from `gap_diagnostic.py` quantities):**
- circle-min f = 0.2487462,  mean_lambda f = 0.2995  (uniform mean of f over |z|=1;
  computed in this round, finite away from the measure-zero Q-zeros).
- The "leverage" the idealized bound could offer is at most
  mean_lambda f - circle-min f = 0.0508.
- The error half-width's height term, for the relevant h ~ 0.249, is
  (4 * 0.249)^{1/2} = 0.998 — **TWENTY times the entire 0.0508 leverage**, before even
  multiplying by Lip(f) and adding pi/d. The bound (*) is therefore not merely
  circular but quantitatively vacuous at the heights in play: it gives
  mean_nu f >= 0.2995 - Lip(f)*0.998 - ... , a NEGATIVE and useless lower bound.

There is no substitution of h that turns (*) into a positive floor above 0.2487462.

### 3.3 Defect B — WRONG TARGET / CAPACITY 1

The reference measure in Theorem 3.1 is lambda_{S^1}, the uniform measure on the SINGLE
unit circle |z|=1 (the equilibrium measure of the closed unit disk, capacity 1). Two
problems:

1. **Capacity-1 / no leverage.** The theorem pushes nu TOWARD lambda_{S^1}; its leverage
   vanishes precisely where the equilibrium measure lives. The min-vs-mean slack we want
   to capture is the deviation of nu AWAY from the circle min toward higher-f regions —
   the bound controls the opposite direction (how CLOSE nu is to the circle), not how
   FAR its f-mean sits above the min.
2. **Wrong locus.** lambda_{S^1} is supported on ONE circle |z|=1, but the ZZ conjugate
   mass sits on BOTH circles |z|=1 and |1-z|=1 (Section 1). The theorem's target does
   not even match the support of nu, so "nu close to lambda_{S^1}" is not the right
   limiting statement for ZZ (the correct ZZ equilibrium object is the two-circle / w-
   lemniscate measure, not lambda_{S^1}). Even the IDEALIZED, height-free reading
   mean_nu f = mean_lambda f = 0.2995 is (i) not a rigorous lower bound (it needs h->0)
   and (ii) the wrong limit measure.

Petsche's thesis bound (UT Austin) is the same statement via Fourier inversion +
Erdos-Turan-Mahler character sums — a logarithmic-energy/discrepancy machine with the
identical two defects. Same kill.

---

## 4. Honest scope of the verified-NEGATIVE

What this round **establishes** (rigorous, reproducible):

1. The R3 "far lemniscate, mean_nu f ~0.44" diagnosis is **WRONG and corrected**: ZZ
   conjugates hug the two circles; mean sigma_ZZ ~0.24-0.27; the 0.44 was a self-term
   numerical artifact on the tiny deg-8 poly j=5, over-generalized.
2. The correct slack is the **min-vs-mean MEAN gap**, which is positive and persistent
   (+0.003 to +0.02 at deg_w 16-22) on Flammang's near-extremal family — NOT a
   collapsing min gap.
3. The **only known tool** to convert "conjugate mean exceeds circle min" into a
   uniform floor — FR06/Petsche effective equidistribution — is **inert** here: it is
   (A) circular (error ~ (4h)^{1/2} contains the bounded height; quantitatively vacuous,
   0.998 >> 0.0508 leverage) and (B) capacity-1 / wrong target (equidistributes to
   lambda_{S^1} on a single circle, the wrong limit measure).

What this round **does NOT claim** (scope limits, per outline-review):

- NOT "the min-vs-mean route is DEAD." The genuine mean-gap slack persists and is
  UNCAPTURED, not closed. The route is recorded as **OPEN**: no cheap or screenable
  lever exists, because converting the persistent mean gap into a rigorous degree-
  UNIFORM floor for ALL ZZ-minimal polys still requires a **height-INDEPENDENT
  containment / equidistribution lemma that does not exist** — and every version using
  log|disc| / log-energy is barred, every version using h is circular (FR06).
- NOT a "delta -> 0 as degree grows" closure. That argument is DEFECTIVE: it reads the
  MIN gap (which collapses); the mechanism uses the MEAN gap (which persists).
- NOT the BMQS strong-duality "forces delta -> 0" step. Strong duality pins the LP value
  to C_82, which is the UNKNOWN (0.2487 <= C_82 <= 0.2540); equality at the optimum
  says the optimal mean equals ess(h), NOT that ess(h) = circle-min. The BMQS handoff
  is a non-sequitur and is not used.

## 5. What would push this further (honest)

A genuine raise on this route needs a **height-independent containment lemma**: a
deterministic region R (derived from the integer-coefficient / reciprocal-symmetry
structure of ZZ-minimal polynomials ALONE, NOT from h, NOT from log|disc|) such that
every conjugate of every ZZ-minimal alpha lies in R AND min over the conjugate-MEAN of
f over admissible measures on R exceeds circle-min + delta. The diagnostic shows the
binding lobe IS reached by individual high-degree conjugates (min gap -> 0), so any such
lemma must work at the level of the MEAN (an averaged/equidistribution statement), not a
pointwise exclusion. No such lemma is known; constructing one is open research, not a
screenable lever. Until one appears, the lower bound stays at Flammang 0.2487458 for
this route.

## Sources
- Favre & Rivera-Letelier [FR06] Thm 3.1, via D'Andrea-Narvaez-Clauss-Sombra
  arXiv:1606.04299 §3 (PDF `literature/pdfs/frl_equidist_jtnb.pdf`), transcribed
  verbatim in 3.1.
- V. Flammang, "On the Zhang-Zagier measure", Int. J. Number Theory 14 (2018), Table 1
  (aux function, record lower bound) — `flammang_table1.py`, `flammang_F18_digest.md`.
- run_state R3 Rule (the wrong lemniscate diagnosis) — corrected here.
