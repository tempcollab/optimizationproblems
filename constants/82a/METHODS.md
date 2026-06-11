# C_82a — Essential minimum of the Zhang–Zagier height: consolidated methods

This is a self-contained methods summary of the two-sided improvement of constant
C_82a achieved over rounds R1–R17. It is written to stand alone: a reader need not
open the per-angle approach docs. All numbers are quoted from the verified ledgers
(`current.md`, `82a.md`); none are recomputed here.

---

## 1. The constant and the bar

For an algebraic number α with naive (logarithmic Weil) height h(α), the
**Zhang–Zagier height** is h_Z(α) = h(α) + h(1−α). The constant

> **C_82 = sup{ H : { α ∈ Q̄ : h_Z(α) ≤ H } is finite }**

is the **essential minimum** of h_Z — the largest height threshold below which only
finitely many algebraic numbers sit. It is not known exactly; the work is to squeeze
the open interval [lower, upper] around it.

**The bar we beat (best previously verified bounds):**

| side | previous record | value | reference |
|------|-----------------|-------|-----------|
| lower | Flammang 2018 | 0.24874 (= log 1.282416 = 0.2487458) | [F18] |
| upper | Doche 2001 | 0.25444 (= log 1.289735 = 0.25443677) | [Doc01b] |

(The structural paper [BMQS] quotes a *weaker* pair 0.248247 ≤ ess ≤ 0.254437 and
does not cite Flammang, so the genuine verified bar is the Flammang/Doche pair above.)

---

## 2. The two-sided result

| side | new verified value | round | margin over previous record |
|------|--------------------|-------|------------------------------|
| **upper** | **C_82 ≤ 0.2540419719** | R11 | −3.42×10⁻⁴ below [Doc01b] 0.25443677 |
| **lower** | **C_82 ≥ 0.2524001332** | R17 | +3.654×10⁻³ above [F18] 0.2487458 |

**Resulting enclosure:** 0.2524001332 ≤ C_82 ≤ 0.2540419719, a **gap of ≈ 1.64×10⁻³**,
down from ≈ 5.7×10⁻³ at the start of the run — the open interval was closed by ≈ 70%.

**Reproduce (each side is a single command):**

- Lower (R17): `python3 constants/82a/certificate/verify_vec_energy.py`
  → `CERTIFIED min_t f(t) ≥ 0.2524001332` (7858 cells, depth 4, frontier resolved, ≈4.3 s).
- Upper (R11): `python3 constants/82a/certificate/verify_upper_q6.py certify 13.937341 12.515102 2.541409 2.068537 0.753965 0 0 0.891271 0.246614 200000 14 1e-10`
  → `CERTIFIED 0.2540419719` (669734 leaves, frontier resolved, ≈5 min).

The **lower-side OSS log-energy/discriminant column is the novel publishable
contribution** of this run; the upper side is a strong reproduce-and-enrich of the
Doche family.

---

## 3. Upper bound: Doche limit-point family + free-exponent perturbing-block enrichment

### 3.1 The framework

Upper bounds on the essential minimum come from the **measure (primal) side** of the
LP dual pair [BMQS, Thm 6.5]: an explicit conjugation-invariant probability measure μ
with ∫ log|Q| dμ ≥ 0 for all Q ∈ Z[x]\{0} gives C_82 ≤ ∫ g dμ. Doche realizes such
measures as **asymptotic Galois-conjugate distributions of a perturbed-polynomial
limit-point family** h = ∏ Pᵢ^{qᵢ} · ∏ Qₖ^{qₖ}, evaluated through

> C_82 ≤ log h(q) = (1/D) ∫₀¹ G(s) ds,   G built from log|·| on the contour
> w = z(1−z), |z| = 1.

The base distinguished block is Doche's **Q = Q₁·Q₂ (deg 56)**; the Pᵢ are the five
[Doc01b] base polynomials {P₁,P₂,P₄,P₆,P₈}.

### 3.2 The free-exponent perturbing-block lever (Doc01a general-ℓ)

The improvement comes not from re-tuning q on the base family, but from **enriching
the dictionary** with new free-exponent perturbing blocks Qₖ raised to continuous
exponents qₖ — the [Doc01a] §4 general-ℓ construction. The governing normalization is
the **D-formula**

> **D = max( Σᵢ qᵢ·deg Pᵢ ,  56 + Σₖ qₖ·deg Qₖ )**

(the "perturb branch" 56 + Σ qₖ deg Qₖ dominates once a block is active), with the
auxiliary B = log|Q₁Q₂| + Σₖ qₖ log|Qₖ|. This is the verbatim [Doc01a] §4 display
D = 2b·max(Σₘ qₘ deg Pₘ, deg Q_{ℓ+1} + Σₘ q_{k+m} deg Qₘ).

### 3.3 Admissibility (the validity gate)

A perturbing block is admissible — so the resulting log h(q) is a *valid* upper bound,
not a broken-integrand artifact — iff [Doc01a Lemma 5 + non-triviality condition (4)]:

- deg Q_{ℓ+1} = 56 > 0;
- each block Qₖ satisfies Qₖ(0) = Qₖ(1) = 1 (neither X nor 1−X divides it);
- Qₖ squarefree (irreducible suffices);
- coprimality gcd(Qₖ, ·) = 1 against **every** kept factor P₁,P₂,P₄,P₆,P₈,Q₁,Q₂ and
  against every other active block (the load-bearing inter-block gcd, e.g. gcd(Q₆,Q₅)=1);
- condition (4): ∏ Pⁿ ≠ ∏ Qⁿ, which then holds by unique factorization once all
  factors are non-constant and pairwise coprime.

### 3.4 A fresh admissible-block source: Flammang Table 1

The key structural insight (R10–R11) was that an admissible perturbing block can be
**any** integer polynomial in X = z(1−z) meeting §3.3 — it need not come from Doche's
own calibration set. The run drew two new blocks from **[F18] Table 1** (the
polynomials Flammang uses on the *lower* side; their lower-bound weights are irrelevant
to the upper-side perturbing role):

- **Q₅ = j13** (deg 12): X¹²−3X¹¹+8X¹⁰−18X⁹+36X⁸−62X⁷+97X⁶−123X⁵+114X⁴−73X³+31X²−8X+1.
- **Q₆ = j15** (deg 16): descending coeffs [1,−4,10,−17,26,−47,119,−298,592,−878,963,−780,464,−199,59,−11,1].

The final R11 family is **h = Q₁·Q₂·Q₅^{qE}·Q₆^{qF}** with
q = (13.937341, 12.515102, 2.541409, 2.068537, 0.753965), qE = 0.891271, qF = 0.246614,
giving D = max(59.198095, 56 + 0.891271·12 + 0.246614·16) = 70.641076 and
∫₀¹ G ds ≤ 17.9457982425, so **17.9457982425 / 70.641076 = 0.2540419719**.

### 3.5 The certificate: outward-rounded max(A,B) quadrature

Each ∫ over a contour cell is enclosed by an **outward-rounded max(A,B) quadrature
interval**, using the O(h²) straddle bound
∫_cell max(A,B) ≤ width·max(A_mid↑, B_mid↑) + max(slope)·r² + (⅓)max(curv)·r³
(from max(a+x, b+y) ≤ max(a,b) + max(x,y)), summed over leaves only with exact tiling
and all-outward rounding. The branch-and-bound **frontier is fully resolved** (669734
leaves, 0 unresolved, 6 rounds), so the enclosure is rigorous, not a grid probe. The
harness self-tests against an independent mpmath high-precision Gauss/adaptive quad
(worst cell_hi − true_int ≈ +1.3×10⁻¹⁷ ≥ 0, the safe side), and a tamper target below
the true min correctly reports `BEATS=False`.

The upper trajectory (all verified, each a strict tightening): R5 0.2543326887 → R6
0.2543309112 → R7 0.2543185491 (first dictionary enrichment, ℓ=1) → R9 0.2542657872
(ℓ=2) → R10 0.2540639638 (first block outside Doche's family, Q₅=j13) → **R11
0.2540419719** (second outside block, Q₆=j15).

---

## 4. Lower bound (the novel core): Flammang LP + OSS log-energy/discriminant column

### 4.1 Flammang's auxiliary-function semi-infinite LP

Lower bounds come from the **Smyth/Flammang dual (auxiliary-function) side** [BMQS,
D(g)]: choose multipliers cⱼ ≥ 0 on integer polynomials Qⱼ so that the pointwise
auxiliary function g(z) − Σⱼ cⱼ log|Qⱼ(w)| ≥ m on the contour forces C_82 ≥ m. Each
column ∫ log|Qⱼ| dν ≥ 0 is valid because |Qⱼ| evaluated on a conjugate set is a
nonzero integer off a finite exception set (resultant-integrality). Flammang's 24
Table-1 columns give the record 0.2487458; R1 reproduced this with a rigorous interval
branch-and-bound certificate, re-deriving the finite-exception integrality from scratch.

### 4.2 The OSS log-energy / discriminant column (the new dual column)

The advance adds a column **Flammang never had**, from Orloski–Sardari–Smith
[OSS, arXiv:2401.03252] — the same logarithmic-energy / discriminant constraint that
produced the largest Schur–Siegel–Smyth jump in 40 years. For the conjugate measure ν
of a minimal polynomial,

> I(ν) = ∫∫ log|z₁ − z₂| dν dν = (1/d²) log|disc(P)| ≥ 0,

because **disc(P) is a nonzero integer off a finite exception set** — exactly the same
integrality clause as the cⱼ columns. The hard quadratic I(ν) ≥ 0 is replaced by its
**linear supergradient outer cut** at a fixed reference measure μ₀ [OSS eq.8]: since
I(·) is concave with gradient 2 K μ₀,

> **∫ ( 2 U_{μ₀}(z) − Î ) dν  ≥  I(ν)  ≥  0**,   the new nonnegative dual column,

where U_{μ₀} is the logarithmic potential of μ₀ and Î ≤ I(μ₀). Validity rests on the
**continuous negative-definiteness of the log kernel** (Ahlfors Lemma 2.1 / OSS eq.6),
which holds because both μ₀ and ν have **finite energy** — *not* on the discrete
diagonal-zeroed kernel (the R12 non-concavity artifact, which has a large positive
eigenvalue and is avoided). A linear cut on a non-empty polytope is at worst slack, so
it sidesteps the unit-circle capacity-0 trap that makes a literal hard p^T K p ≥ 0
constraint vacuous on |z| = 1. Adding the column can only **raise** the minimum:
m₀ ≤ m_cut ≤ m_true ≤ C_82 — a valid outer relaxation that can never overshoot C_82.

### 4.3 The diffuse finite-energy reference measure μ₀

μ₀ is a **histogram of uniform arcs on |z| = 1** (a piecewise-constant density), built
by binning the no-energy LP optimum. It must be diffuse (finite energy) for §4.2 to
apply — an atomic μ₀ gives I(μ₀) = −∞ and the cut is not an eq.6 consequence. For
uniform arcs, **I(μ₀) is exact in closed form**: each block mean of log|e^{is}−e^{is'}|
is B1(d,L) = (F2(|d|−L) + F2(|d|+L) − 2F2(|d|)) / L², with F2(x) = Re Li₃(e^{ix}) − ζ(3)
(from F2'' = log(2 sin(x/2)); the singular d=0 self-block is finite). Rounding the
mpmath value **down** to a float gives the rigorous **downward enclosure Î ≤ I(μ₀)** —
the safe direction that keeps the column ≥ 0.

The R17 record re-froze μ₀ at a **wider arc-width** (freeze parameter B = 55 → 15 arcs,
t-width L = 0.057120, vs R15's L = 0.039270). The wider arcs make the OSS self-cut bind
harder: λ₀ rises 0.0235977 → **0.04012668**, Î = −0.2111616260, and the LP cut value
to m_cut = 0.2526110.

### 4.4 The interval branch-and-bound certificate

The pointwise inequality

> f(z) = g(z) − Σⱼ cⱼ log|Qⱼ(w)| − λ₀ ( 2 U_{μ₀} − Î )  ≥  m,   cⱼ ≥ 0, λ₀ ≥ 0,

is certified **directly on |z| = 1** by an outward-rounded interval branch-and-bound.
The one new ingredient versus R1 is a rigorous **per-cell upper bound on U_{μ₀}** via an
**exact Clausen arc-average** potential: P_k(t) = (Cl₂(t−μ−L/2) − Cl₂(t−μ+L/2)) / L
(Cl₂ = Clausen = Im Li₂), upper-bounded per cell with a rigorous Cl₂ interval enclosure
(scipy `spence` endpoints, monotone between the ±π/3 extrema, outward-padded). The
over-estimate of U_{μ₀} is the **safe direction** (it makes the certified f a valid
*lower* bound — independent mpmath checks give min(Uhi − U_true) ≈ +1.3×10⁻⁴ ≥ 0). The
search is reduced to the **|z| = 1 min-locus** by superharmonicity of −2λ₀ U_{μ₀} (the
log-potential of a measure on the unit circle) together with the z → 1−z symmetry. Near-
node cells (where the subtracted potential → −∞) bisect normally; nothing auto-certifies.

**Result (R17):** `CERTIFIED min_t f(t) ≥ 0.2524001332` (7858 cells, depth 4, frontier
= 0, ≈4.3 s; binding cell t ≈ 0.489). A tamper target above the ≈0.252555 ceiling
(certify(0.2526)/(0.2527)) correctly returns ok=False via a depth-hit; certify(0.2524)
passes — no rubber-stamp, no grid fallback.

The lower trajectory (all verified): R12 stage-1 conjecture (column fires, m_cut ≈
0.2500–0.2504) → R14 0.2509000289 (first rigorous lower-side break, two-sided result) →
R15 0.2511300035 (atomic B&B-target raise, banks the slack) → **R17 0.2524001332**
(re-freeze μ₀ at the wider B=55 arc-width, lifting the ceiling).

---

## 5. Why this is a genuine advance, not truncation-tuning

[BMQS, Thm 6.5] proves **strong duality** between the two classical methods:
D(g) = ess(h_g) = P(g), with **no duality gap**. The residual interval is therefore a
**truncation gap** (how far the finite-dimensional LPs have been pushed), not a duality
gap that no amount of computation can close. Within that frame:

- The **upper** improvement is a genuinely richer measure (new admissible perturbing
  blocks Q₅, Q₆ drawn from a fresh source), certified rigorously, not a re-tuning of the
  base family — each enrichment step is a strict, separately verified tightening.
- The **lower** improvement adds a **new dual column the auxiliary-function method never
  carried**: the OSS log-energy/discriminant constraint. It is independent of Flammang's
  cⱼ columns and can only raise the bound. This is the publishable core: the first
  rigorous transfer of the OSS energy machinery to the Zhang–Zagier essential minimum.

---

## 6. Limits and further work

- **The single-cut lower ceiling is near-exhausted.** A single OSS outer cut at one
  μ₀ has a hard ceiling (≈0.2526 on the best B=55 freeze; R17 certifies 0.2524, ≈1.5×10⁻³
  below it). m_cut(B) is fragile and non-monotone (B=55 is the measured peak; B=53
  collapses to K=13 and the ceiling falls to ≈0.2514), so blind arc-width sweeping does
  not help. Recovering the residual ≈10⁻⁴ Clausen arc-average haircut needs a tighter
  per-cell potential bound than the max-chord arc-average.
- **A second cut is the next real lever.** Further closing needs either a **second
  energy / discriminant-moment cut** (a cutting-plane iteration of the OSS self-cut),
  or the **Fekete-converse two-sided companion** (arXiv:2304.10021), which pairs the
  energy lower bound with a transfinite-diameter upper estimate. Both are non-atomic
  rounds beyond the present single-cut certificate.

---

## References

- **[F18]** Flammang, V. *On the Zhang–Zagier measure.* Int. J. Number Theory 14 (2018),
  no. 10, 2663–2671. (Record lower bound 0.24874; Table 1 polynomials, reused here as
  upper-side perturbing blocks.)
- **[Doc01a]** Doche, Ch. *On the spectrum of the Zhang–Zagier height.* Math. Comp. 70
  (2001), no. 233, 419–430. (General-ℓ perturbed family; §4 D-formula; Lemma 5 +
  non-triviality condition (4).)
- **[Doc01b]** Doche, Ch. *Zhang–Zagier heights of perturbed polynomials.* J. Théor.
  Nombres Bordeaux 13 (2001), no. 1, 103–110. (Record upper bound 0.25444; base
  P₁,P₂,P₄,P₆,P₈ and distinguished block Q = Q₁Q₂.)
- **[OSS]** Orloski, J., Sardari, N. T., Smith, A. *(logarithmic-energy / discriminant
  method)* arXiv:2401.03252. (The energy column I(ν) ≥ 0 and its eq.8 supergradient
  outer cut; Ahlfors Lemma 2.1 / eq.6 continuous negative-definiteness.)
- **[BMQS]** Burgos Gil, J., Menares, R., Qu, B., Sombra, M. *Closing the gap around the
  essential minimum of height functions with linear programming.* arXiv:2601.18978
  (2026). (Thm 6.5 strong duality D(g) = ess(h_g) = P(g): the gap is a truncation gap.)
- **Fekete-converse companion** arXiv:2304.10021. (Further-work route, not used here.)
