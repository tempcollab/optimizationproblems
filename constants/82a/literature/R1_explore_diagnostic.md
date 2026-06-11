# R1 Diagnostic exploration — C_82a (Zhang-Zagier essential minimum), LOWER bound

Two-part diagnostic. PART A: is the held lower bound (R14/R15/R17, 0.25090..0.25240
via the OSS log-energy column) wrong? PART B: where is the genuine slack in the
LOWER bound?

---

## PART A — VERDICT: the R14/R15/R17 lower bounds are INVALID. RETRACT. Reset held to 0.2487458 [F18].

The OSS log-energy certificate `verify_vec_energy.py` has a **load-bearing,
reproducible bug in the min-locus reduction to |z|=1** (the (C5) / "superharmonicity"
step). The certified number 0.2524 is `min f` *on the unit circle only*; the quantity
that must be bounded below — `(1/d) ∫ f dν` over the true conjugate measure ν — is NOT
bounded by it, because the energy term pushes `f` far below its on-circle values OFF
the circle, exactly where ν lives.

### The single most likely concrete bug (decisive, reproducible)

**`verify_vec_energy.py` lines 44–47 (and the cert header lines 71–80): the
"min-locus reduction to |z|=1" is INVALID once the OSS energy term is added.**

The cert certifies, by interval branch-and-bound, only
`f(z) ≥ m` for z on the arc `|z|=1, t∈[0,π]` (`certify()` line 261, `a = np.linspace(0,π,…)`).
It then invokes (header line 44–47):

> "The min-locus reduction to |z|=1 is Flammang's (R1): −2 λ0 U_μ0 is SUPERHARMONIC
> (positive log-potential of a measure ON |z|=1), so f attains its minimum on |z|=1."

This reasoning is **backwards**. `U_μ0(z) = ∫ log|z−w| dμ0(w)` is **subharmonic**
(Δ U_μ0 = 2π μ0 ≥ 0), harmonic off supp(μ0). Hence `−2 λ0 U_μ0` is **superharmonic**.
Adding a superharmonic term to Flammang's `f0` (which legitimately has its min on the
unit circles, because `log⁺|z|` is subharmonic and `−c_j log|Q_j|` is harmonic-with-+∞-poles)
**destroys** the "min on |z|=1" property: a superharmonic perturbation makes interior/
exterior values *lower* than a harmonic interpolation, so the sum `f = f0 − 2λ0 U_μ0`
can — and does — dip well below its `|z|=1` values off the circle.

This is not abstract. Direct measurement of the TRUE `f` (frozen R17 data, fine
quadrature of the histogram potential):

| where | min f |
|---|---|
| on `\|z\|=1` (what the cert certifies) | **0.25255** |
| off `\|z\|=1` (radius scan 0.85–1.15) | **0.0953** |
| 2-D plane scan (global) | **≤ −0.06**, attained near z ≈ 1.20 − 0.68i (`\|z\|≈1.38`) |

So `min_C f ≈ −0.06 ≪ 0.2524`. The conjugate measure ν of a Zhang-Zagier minimal
polynomial is **not** supported on `|z|=1` — the conjugates spread over the plane (in
the `|z(1−z)|` lemniscate region). Averaging `f` against that ν gives at best
`min_plane f ≈ −0.06`, which is **below Flammang's 0.2487**, so the energy column
delivers **no valid raise at all**. The certified `0.2524` is an artifact of
restricting the minimization to a locus where ν does not live.

**Reproduce** (≈90 s): for the frozen R17 `mu0`, evaluate
`f(z) = log⁺|z(1−z)| − Σ c_j log|Q_j(z−z²)| − λ0(2 U_μ0(z) − Î)` on a 2-D grid; the
global min is ≈ −0.06 at `|z|≈1.38`, vs the cert's on-circle 0.2525. (script logic in
the diagnostic run; uses `verify_vec_energy.CENTERS/MASSES/CJ/LAM0/IHAT`.)

### A second, independent structural invalidity (confirms retraction)

The proof of column (C3) (`verify_vec_energy.py` lines 25–39) claims
`∫(2 U_μ0 − Î) dν ≥ 0` because `2 I(ν,μ0) − I(μ0) ≥ I(ν) = (1/d²) log|disc(P)| ≥ 0`.
But in the **z-variable** the discriminant identity is
`disc(P) = a_lead^{2d−2} ∏_{i<j}(α_i−α_j)²`, so

  `I(ν) = (1/d²)[ log|disc(P)| − (2d−2) log|a_lead| ].`

The Zhang-Zagier height is defined for **all** algebraic numbers α (not just integers),
so `a_lead` can be > 1 and the `−(2d−2) log|a_lead|` term is ≤ 0 and can dominate. Then
`I(ν) ≥ 0` **fails**, and the column is not a valid `≥ 0` column. (For the trace
problem OSS attack, α is a totally-positive algebraic *integer*, `a_lead = 1`, and `ν`
lives on a real interval — both hypotheses that make the OSS column valid there are
**absent** here.) This matches the user's directive that the OSS column is a no-go for ZZ.

### Reconciliation with the user's four mechanisms

The user's four mechanisms all say the OSS energy contribution for ZZ is *structurally
inert / ≈ 0 after the haircut* (2-pt cut energy ≈ 0; symmetrized cross-energy
`≥ +0.2557 > 0` so the cut never binds in the valid direction; w-coordinate floor
≈ −0.03 with raise ≈ 5e-5; 4-pt moment optimum strictly interior, J(p0)=+0.36). Those
are the *honest* magnitudes: the genuine, validly-signed energy raise is ≈ 0. The
certificate appears to get +0.0037 only because **two safeguards are broken at once**:
(i) the min is taken on the wrong locus (|z|=1, where ν does not live), and (ii) the
column's `I(ν) ≥ 0` premise fails for non-integer α. The +0.0257 "raise" the
`checks()` anchor reports is itself a tell: with `λ0 = 0` the frozen `c_j` give
`min f0 = 0.2266` (BELOW Flammang's 0.2487 — the frozen `c_j` are *joint cut-LP duals*,
not the no-energy Flammang duals), and the energy term merely climbs back to 0.2525.
The cert is using a mis-located, mis-signed term to repair deficient `c_j` and then
claiming it beats Flammang.

**Action for the reviewer:** retract R14/R15/R17. Reset `held` lower to
**0.2487458 = log(1.282416)** [F18, R1-reproduced]. Set `## Status: none` on the lower
side (the upper side, 0.2540419719 [R11], is independent and stands). Strike the three
disputed rows from `82a.md` "Known lower bounds" (or annotate as withdrawn). The
milestone-count impact: R12/R14/R15/R17 lower-side milestones were predicated on an
invalid certificate; the proof-reviewer should re-log accordingly.

---

## PART B — Where the genuine LOWER-bound slack lives

### How the record lower bound is achieved (Smyth/Flammang, [F18])

Auxiliary function `f(z) = log⁺|z| + log⁺|1−z| − Σ_{j=1}^{24} c_j log|Q_j(z(1−z))|`,
`c_j > 0`, `Q_j ∈ ℤ[w]`, `w = z(1−z)`. Chain: sum over conjugates; each
`∏_i Q_j(α_i(1−α_i)) = Res(P, Q_j(z(1−z)))` is a nonzero integer ⇒ `log| | ≥ 0` ⇒ the
`c_j` terms drop ⇒ `(1/d) log Z(α) ≥ m = min_{|z|=1} f`. The `c_j` are tuned by Smyth's
**semi-infinite LP** at a *fixed* polynomial dictionary; the dictionary is enlarged by
**weighted integer transfinite diameter + LLL** (Re/Im linear forms at control points
near the active minima), `k` swept 5→32. Result: `ζ ≥ 1.282416`, i.e.
**C_82 ≥ 0.2487458** (off the finite exception set `(z²−z)(z²−z+1)φ10(z)φ10(1−z)`).
Doche's predecessor was 0.2482474; the Doche→Flammang gain was only ≈ 5e-4 after a
large search.

### How tight is 0.24874 vs the truth (~0.2543)?

- Verified lower: **0.2487458** [F18]. Verified upper: **0.2540419719** [R11, this repo].
  Open gap ≈ **0.0053**.
- Doche's smallest *known single* height is 1.2875274 ⇒ log = 0.25272, and he
  conjectures the smallest **limit point** (= the true ess min) is `< 1.2875274`, i.e.
  C_82 ≈ 0.2527 or a touch below. So the lower bound is loose by ≈ **0.0040** relative
  to the conjectured true value — there is genuine, large headroom on the lower side,
  but every past gain on it has been small and search-driven.

### Where the Smyth/Flammang LP is loose (the real levers)

1. **Column dictionary (the dominant slack).** Flammang stopped the LLL/transfinite-
   diameter breeding at `k ≤ 32` "at compute limits." The semi-infinite LP is optimal
   *over her 24 columns*; the slack is entirely in *which integer polynomials `Q_j(w)`
   are present*. The R1 `lp-column-generation` approach priced thousands of cheap
   candidates (products, ±1 perturbations, deg ≤ 4) against the LP dual `μ*` and found
   **no improving integer column** (best reduced cost ≈ −1e-7, LP moved ≈ 2e-11). So
   the cheap dictionary is exhausted; a real gain needs **genuinely new high-degree
   (k>32) columns bred by Flammang's own LLL recipe** at control points near the active
   minima — the compute-heavy step she stopped at. This is the single most credible,
   in-method lever, and it is *not* a dead end, only un-attempted at scale.

2. **Contour modeling — |z|=1 vs the lemniscate w = z(1−z).** Flammang's reduction to
   `|z|=1` is **valid for her `f0`** (subharmonic-off-circles argument), so this is NOT
   a loose spot for the pure auxiliary-function method. It only becomes fatal when a
   *non-harmonic* extra term (the OSS potential) is bolted on — see PART A. Any new
   lower-bound column must either (a) keep `f` harmonic/subharmonic off the unit circles
   so the `|z|=1` reduction survives, or (b) certify the min over the full plane / the
   genuine support region of ν (the `|z(1−z)| = const` lemniscate family), not over
   `|z|=1`. Treat the support locus as a hard constraint on any future column, not as a
   modeling convenience.

3. **The integrality / finite-exception argument.** `Res(P, Q_j(z(1−z))) ∈ ℤ\{0}` off a
   finite set is exact and not loose. A would-be new column must reproduce this exact
   structure (a quantity that is a nonzero integer off a finite exception set). The OSS
   discriminant column *fails* this for ZZ because of the leading-coefficient term
   (PART A, second bug) — a cautionary template: "looks like an integrality column" is
   not enough; the `a_lead` factor must be controlled.

### What BMQS 2026 (arXiv:2601.18978) says about pushing the LP — and whether they "close the gap"

BMQS is **theoretical/structural**, NOT a numerical advance for ZZ (see
`bmqs_2026_digest.md`):
- They prove the lower-bound (Smyth dual `D(g)`) and upper-bound (measure primal
  `P(g)`) methods are **LP-dual**, with **strong duality**: `D(g) = ess(h_g) = P(g)`
  (Thm D / 6.5). "Closing the gap" is meant **theoretically** — both methods converge to
  the same value if run indefinitely — *not* a finite recipe that closes the numeric gap.
- Thm E / 7.6: for a computable Green function `ess(h_g)` is a computable real, via a
  theoretical algorithm (reduce `D`, `P` to countable subsets, generate converging
  bracketing sequences). They explicitly say (§1.7) "no practical algorithm is known to
  approximate them up to any arbitrary precision … the methods reach a point where it is
  unclear how to continue, due to the enormous size of the search space and the lack of
  an efficient criterion to find the optimal direction," and "the obtained algorithm is
  far from being practical."
- They give **no new numeric bound, no table, no ZZ computation**, and quote the weaker
  0.248247 ≤ ess ≤ 0.254437 (Zagier/Doche), not even citing Flammang. So BMQS does
  **not** tell us the Smyth LP can be pushed by any specific amount; it confirms the LP
  framing is correct (scipy `linprog` is the right tool) and that the bottleneck is
  precisely the **missing efficient column-generation direction** — which is exactly the
  un-attempted lever (1) above. The "efficient criterion to find the optimal direction"
  they flag as missing is, in LP terms, reduced-cost column generation against the dual
  `μ*` — the R1 approach tried it cheaply and found the cheap dictionary exhausted, so
  the genuinely open question is whether LLL-bred high-degree columns price in.

### Concrete angles for the outliner (do NOT re-attempt OSS energy)

- **A (in-method, highest-credibility):** implement Flammang's LLL / weighted-integer-
  transfinite-diameter column breeding for `k = 24…40` at control points near the active
  minima, add the surviving factors, re-solve the semi-infinite LP, re-certify with the
  existing R1 interval B&B (`verify_vec.py`). Hard step: producing an integer column with
  improving reduced cost that *survives re-optimization* (gets `c_Q > 0`). Risk high
  (gains historically ≈ 5e-4), but it is the only lever BMQS's own analysis points to and
  it keeps the valid `|z|=1` reduction intact.
- **B (a genuinely different valid column):** any new `≥ 0` column for ZZ must be a
  quantity that is a nonzero integer off a finite exception set *and* keep `f`
  subharmonic-off-circles (so the `|z|=1` reduction holds) — e.g. resultants
  `Res(P, R(z(1−z)))` with new `R ∈ ℤ[w]`, NOT the discriminant/energy (which fails both
  the `a_lead` integrality and the harmonicity requirements for ZZ). 
- **C (dead-end avoidance):** the OSS log-energy / discriminant-moment column is a
  PROVEN no-go for ZZ (user's four mechanisms + the two structural bugs above). Do not
  revisit it in any disguise (w-coordinate energy, symmetrized cut, k-point moment).

---

## Files

- This report: `constants/82a/literature/R1_explore_diagnostic.md`.
- Re-used digests: `flammang_F18_digest.md`, `doche_doc01b_digest.md`,
  `bmqs_2026_digest.md` (all accurate; no re-fetch needed).
- Certificate under retraction: `certificate/verify_vec_energy.py`
  (bug at lines 44–47 / header 71–80, min-locus reduction; column-validity at lines
  25–39), `freeze_energy.py`, `frozen_energy.npz`.
