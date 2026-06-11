# R5 — Power-sum / w-moment column AND SSS trace-transplant: verified-NEGATIVE closure

**Type:** verified-NEGATIVE lever-closure (a logged milestone under the run's
verified-progress metric). **Does NOT raise the bound.** Held lower stays
Flammang [F18] **0.2487458 = log(1.282416)**, Status `none`.

**Certificate:** `constants/82a/certificate/screen_powersum.py`
(`certify` / `selftest` / `tamper`, all PASS, runs in seconds; exact integer
Newton/Faddeev arithmetic + numpy cross-check).

---

## What this closes

Two previously-unexamined NON-energy lower-bound levers, named in the R5 dispatch
and floated by explorer A (`/tmp/round-5/R5_explore_minmean.md` §1b, §1a):

- **(a) the power-sum / w-moment column** `int w^k dmu_w = S_k/d`, with
  `w_i = z_i(1-z_i)` the conjugates of `w = alpha(1-alpha)` and `mu_w` the
  conjugate (counting) measure of a ZZ-minimal `alpha` of degree `d`.
- **(b) the single-variable Schur-Siegel-Smyth (SSS) trace-transplant** — whether
  Smyth's mean-DIRECT trace lower bound transplants to ZZ to cash the persistent
  min-vs-mean gap WITHOUT an energy column.

Neither was touched by R3 (which ceilinged the `log|Q|>=0` contour-LP span at
0.2487857) or R4 (which closed FR06/Petsche equidistribution). This is genuinely
new closure.

---

## Lever (a): the power-sum / moment column — CLOSED on three independent mechanisms

Flammang's lower bound is the LP
`max m s.t. sigma_ZZ(z) - sum_j c_j log|Q_j(w)| >= m for all z, c_j>=0, Q_j in Z[w]`,
with the honest Zhang-Zagier density `sigma_ZZ(z) = log+|z| + log+|1-z|`
([F18] eq. 2.1; `log+ x = log max(1,x)`). Each column is a SINGLE integral of
`log|integer poly|`, entering as a sign-DEFINITE inequality
`int log|Q_j(w)| dmu_w >= 0` (resultant-integrality, off a finite exception set).

A power-sum / moment functional `int w^k dmu_w = S_k/d` is a different object: a
SINGLE integral of a MONOMIAL `w^k`, equal to a polynomial-dependent real with no
log and no kernel. It is neither the `log|Q|>=0` cone (R3) nor the double-integral
log-energy `int int log|w_1-w_2| dmu dmu` (barred OSS). The screen establishes it
supplies no usable inequality, for three independent reasons:

- **MECH 1 (load-bearing, screened): SIGN-INDEFINITE.** `S_k/d` takes BOTH signs
  across ZZ-minimal polys, so it can never be a sign-definite `>=0` drop-out column
  — it never enters the LP, hence cannot raise the bound. Screened (exact):
  `z^2-z-1` -> `S_k/d = -1, +1, -1, +1, -1`; `z^2-z+1` -> `+1` all `k`;
  `z^3-z-1` -> `-0.667, -0.667, +2.333, -2, -2.333`. Signs `{+, -, 0}` all appear.

- **MECH 2 (load-bearing, screened): NON-integer off the a=1 locus.** The premise
  "`sum w_i^k` are exact integers" (explorer A §1b) is TRUE only on the
  algebraic-integer locus (leading coeff `a=1`) and FALSE over the actual ZZ
  domain. ZZ ranges over ALL algebraic numbers; for a primitive `alpha` with
  `a>1` the `w_i = alpha_i(1-alpha_i)` are NOT algebraic integers, so `S_k(w)`
  carries `a`-power denominators and is non-integer — no integrality drop-out
  exists. Screened (exact Fractions): `10z^2-6z+1` (a=10) ->
  `S_1=11/25=0.44, S_2=117/1250=0.0936, S_3=2398/125000=0.019184`, none integers;
  same for `3z^2-z+1` (a=3) and `7z^3-2z-1` (a=7). This is the SAME `a^deg`
  leading-coefficient wall that retracted the OSS energy column in R1
  (`I(nu)=(1/d^2)[log|disc|-(2d-2)log a] < 0` for `a>1`).

- **MECH 3 (supporting): vanishing on the integer locus.** Even restricted to
  `a=1`, `int w^k dmu_w = S_k/d` is an equality to `S_k/d`, which -> 0 as
  `d -> inf` (the low-order symmetric structure of `w=z-z^2` is fixed-size while
  `d` grows). Demonstrated with the family `z^d - z - 1`: `S_1/d` runs
  `-1, -0.667, 0, 0, 0, 0` for `d = 2,3,5,8,13,21`. So the "constraint" dissolves
  — it is an equality to an unconstrained real, not a fixed positive floor.

**Disjointness (the hard step, complete).** Any fixed real moment functional
`sum_k a_k int w^k dmu_w = int P(w) dmu_w = (sum_i P(w_i))/d` inherits all three
failures: (i) sign-indefinite across polys (Mech 1), (ii) non-integer off the
integer locus (Mech 2), (iii) -> 0 on it (Mech 3). The moment span is therefore
disjoint from BOTH the `log|Q|>=0` cone (every member is a contour-LP column,
R3-ceilinged) AND the energy cone (a double integral with a log kernel, barred).
A power/moment column is neither, and supplies no inequality at all — it cannot
enter the auxiliary-function LP. **Lever (a) CLOSED on Mech 1 and Mech 2 each
independently**, with Mech 3 as corroboration.

---

## Lever (b): the SSS trace-transplant — CLOSED structurally

Smyth's trace lower bound is MEAN-DIRECT (no min-reduction) for exactly two
reasons (OSS arXiv:2401.03252 §1.1, eq. 2, read from
`literature/pdfs/sss_2401.03252.pdf`):

1. its objective `int x dmu = (1/d) sum alpha_i = trace/d` is a LINEAR functional
   of the conjugates, and
2. `sum alpha_i = trace(alpha)` is an EXACT INTEGER.

Integrate Smyth's inequality `x >= lambda_A + sum_j c_j log|Q_j(x)|` against the
conjugate measure: the log columns drop by integrality, and because the objective
is linear you get `mean-trace >= lambda_A` DIRECTLY — equidistribution is
irrelevant to obtaining the bound (it only governs the rate).

For ZZ both handles fail:

- the objective `sigma_ZZ(z) = log+|z| + log+|1-z|` is NON-linear and
  non-polynomial; and
- the conjugate-sum `sum_i sigma_ZZ(z_i) = d * h_Z(alpha)` IS the unknown height
  itself — there is no exact-integer trace to exploit.

Flammang is therefore FORCED into `(1/d) sum f(z_i) >= min f` (the min-reduction),
and the min-vs-mean gap is intrinsic to ZZ and structurally ABSENT from the trace
problem. The reproducible witness for "there is no integer-trace handle" is the
Mech-2 demo in the same certificate: the only w-power-sum that is an exact integer
needs `a=1`, and even then it is a varying `S_k(w)` (a poly-dependent integer),
never the fixed `sigma_ZZ` objective.

Finally, the HALF of the trace machinery that genuinely "beat naive
equidistribution" (OSS §1.2, the `(x+y)/2` device with `Q = x_1 - x_2`) IS the
log-energy column `int int log|x_1-x_2| dmu dmu` (OSS Thm 1.1) — exactly the
barred OSS family (`I(nu) < 0` for non-integer `alpha`, R1). And the "finite
exceptional cases by hand" device raises only the all-but-finitely-many statement,
not the asymptotic limit point — but `C_82` (an essential minimum) IS the smallest
limit point, so it buys nothing. **Lever (b) CLOSED.**

---

## Certificate design (reproducibility)

`screen_powersum.py`:
- `S_k(w)` computed EXACTLY via the multiplication-by-`w` operator on `Q[z]/(P)`
  (Faddeev-LeVerrier + Newton's identities over `fractions.Fraction`), so
  integrality on `a=1` and non-integrality on `a>1` are exact, not float noise;
  cross-checked against `numpy.roots` to float precision.
- `certify`: prints the Mech-1/2/3 tables and the closure verdict.
- `selftest`: 7 internal checks (exact-vs-numpy agreement; exact integers on
  `a=1`; exact non-integers on `a>1`; the Zagier `-2,2,-2,2,-2` literature values;
  the `10z^2-6z+1` literature non-integers `11/25, 117/1250, 2398/125000`;
  genuine sign-indefiniteness; product-of-roots sanity). All PASS.
- `tamper`: feeds the bogus claim "`int w^k dmu_w >= 0` for all ZZ polys and all
  `k`" (the only premise that would let a power sum enter the LP as a nonnegative
  column) — the screen must, and does, produce explicit `S_k/d < 0`
  counterexamples; and a second bogus "`S_k` always integer" claim fails on the
  `a=10` poly. No auto-pass, no grid fallback.

The `S_k` vs `S_k/d` distinction is kept clean throughout (`z^2-z+1` has `S_k=2`
but `S_k/d=1`); the sign-indefiniteness tamper keys on `S_k/d = int w^k dmu_w`
(the actual moment-column quantity), not on `S_k`.

---

## How a future round could revisit

The moment/trace family is closed. The closure does NOT claim the lower bound is
dead — only that these two specific non-energy levers cannot move it. The only
residue genuinely OUTSIDE both closed walls (contour-LP `log|Q|` span; barred
energy) is recorded below, OPEN.

### Angle 3 (OPEN, NOT built this round): p-adic / local-height residue

The contour LP uses only the single integrality fact `|Res(P, P(1-x))| >= 1`,
collapsing all non-archimedean places into one inequality. Zagier's 1993 proof
uses the finer p-adic structure
`sum_{v not | inf} (log+|alpha|_v + log+|1-alpha|_v)`, controlled by the reduction
of `alpha(1-alpha)` mod `v` — this is neither a contour integral nor a log-energy
column, hence genuinely outside both walls. But Zagier's local argument is
non-effective enough to reach only **0.2406 < Flammang 0.2487458**, and the single
hard step — turning "`alpha(1-alpha)` has constrained reduction mod `p` across
conjugates" into a degree-UNIFORM additive gain `>= delta*d` for ALL ZZ-minimal
`alpha` surviving to the essential minimum — is open arithmetic research, with no
known tool delivering it. Any attempt to make it effective via `|disc|/|Res|`
moments re-enters the barred energy span (the trap to avoid). No screenable lever
this round; recorded OPEN so a future round knows it is the distinct open frontier.

---

## Status / next

- Held lower stays Flammang **0.2487458**; Status `none`. NO raise claimed.
- Milestone: two previously-OPEN non-energy levers closed by one reproducible
  certificate, each on an independently-screened mechanism.
- The lower side has no cheap or screenable raise (R1-R5 converge); the only
  conceivable actual raise is the OPEN p-adic residue above. If the lower-bound
  focus is released, the upper side (held 0.2540419719, R11) is the demonstrably
  pushable frontier.
