# Approach: z-variable (and 1-z) auxiliary-function columns for the C_82a LOWER bound

**Spec review: required** — the load-bearing step is the |z|=1 min-locus reduction,
the exact subtlety that invalidated the OSS energy certificate (R14-R17). A z-column
threatens it in a *different* way than OSS did (asymmetry, not superharmonicity), and
my round-1 pre-screen shows the naive form does NOT clear the gate. Review before build.

Status: OUTLINED (round 1). Pre-screened by LP (both-circle re-solve). Two sub-angles
survive screening; the naive bare-z-column form is DISQUALIFIED below — read it.

---

## R1 BUILD RESULT (proof-builder) — retraction DONE; forward lever INERT (closed).

**DELIVERABLE 1 (retraction) — established.** Standalone witness
`certificate/retract_oss_lower.py` (runs ~20 s, no network) proves the R14/R15/R17
OSS-energy lower-bound certificate is INVALID by TWO independent mechanisms, using
the SAME committed frozen data (`frozen_energy.npz`) and the SAME `f`-formula:
- **[a]** `min f` on `|z|=1` = **0.252548** (reproduces the cert's claimed locus value);
- **[b]** `min f` over the 2-D PLANE = **-0.19143** at `|z|~1.61` (near `phi=1.618`),
  FAR below the Flammang record 0.2487458 — so the method proves only
  `C_82 >= min_plane f = -0.191`, i.e. the certificate bounds NOTHING;
- **mechanism:** `Delta U_mu0 = +2.7e-7 > 0` ON `|z|=1` (support band) confirms
  `-2 lambda0 U_mu0` is superharmonic, breaking the `|z|=1` min-locus reduction;
- **[c]** the OSS column premise `I(nu) = (1/d^2) log|disc(P)| >= 0` FAILS for ZZ:
  `P = 10x^2-6x+1` (primitive, irreducible, leading coeff a=10, roots (3+-i)/10 are
  genuine algebraic non-integers) has `I(nu) = (log4 - 2 log10)/4 = -0.804719 < 0`.
All three witnesses PASS. Corrected held lower = **0.2487458** [F18]; see
`certificate/RETRACTION.md` for the exact text the reviewer should enact.

**DELIVERABLE 2 (high-degree LLL w-column breeding) — INERT, lever CLOSED.**
Built `certificate/lll_breed.py`: solves the Smyth LP at Flammang's 24 columns
(reproduces `m* = 0.2487464`), extracts the optimal dual `mu*` (binding-band support
~25 pts, `t in [0.488, 2.828]`), then LLL-breeds integer `w`-columns `Q(w)` of degree
`k = 24..40` seeded at `mu*`'s support across scales `60..1e10` (also tried dense
`sqrt(mu)`-weighted seeds). **Result: every nontrivial bred column prices NON-NEGATIVE
against `mu*`; the only negatives are the trivial monomials `w`, `w^2` at `r ~ -3e-14`
(pure complementary-slackness LP noise — `int log|w| dmu* = 0` exactly for binding
columns).** Best genuine reduced cost is `>= 0`; NOTHING prices in below the `-1e-5`
gate (or even the `-1e-7` noise floor). The `k>32` LLL lever — the only unscreened
forward shot per the outline review — is **CLOSED / inert**, exactly as the review
expected (`~1e-8..1e-11`). Structural reason: `mu*` is (numerically) the equilibrium
measure for which Flammang's 24 columns are the binding constraints, and the
resultant-integrality `int log|Q| dmu* >= 0` holds for the whole integer-`w`
dictionary in the limit — so Flammang's set is LP-optimal against ALL integer
`w`-columns, not just the cheap ones. **No forward improvement this round; the round's
verified advance is the OSS retraction.** Reproduce: `python3 lll_breed.py` (~few min).

---

## PART 0 — RETRACTION NOTE (precondition the builder must establish first)

The held lower 0.2509-0.2524 (R14/R15/R17, `verify_vec_energy.py`, OSS log-energy
column) is **INVALID and must be retracted; reset held lower to 0.2487458 = log(1.282416)
[F18]** before any forward work counts. Two independent structural failures, both
confirmed/sharpened this round:

1. **Wrong min-locus.** The cert certifies `f ≥ m` only on the arc |z|=1
   (`certify()` line 285, `a=np.linspace(0,π,…)`). The added term `-2λ0 U_μ0` is
   **superharmonic** (Δ(-2λ0 U_μ0) = -2λ0·2π μ0 < 0, since U_μ0 is the subharmonic
   log-potential of the mass μ0). Flammang's reduction needs f **harmonic off its
   poles** so the max-principle puts the min on the boundary circles ∪ Q-zero disks;
   a superharmonic perturbation breaks that — f dips well below its |z|=1 values OFF
   the circle. Direct measurement (frozen R17 data): min on |z|=1 = 0.2525, but global
   plane min ≈ **-0.06** near |z|≈1.38. The conjugate measure ν of a ZZ-minimal
   polynomial is NOT supported on |z|=1, so `(1/d)∫f dν` is bounded by the plane min
   (≈ -0.06 < 0.2487), not by 0.2525. **No valid raise.**
2. **I(ν) ≥ 0 fails for ZZ.** Column C3 needs `2I(ν,μ0) - I(μ0) ≥ I(ν) = (1/d²)log|disc(P)| ≥ 0`.
   In the z-variable `disc(P) = a_lead^{2d-2} ∏(α_i-α_j)²`, so
   `I(ν) = (1/d²)[log|disc(P)| - (2d-2)log|a_lead|]`. The ZZ height is defined for ALL
   algebraic α (not just integers), so a_lead can be > 1 and `-(2d-2)log|a_lead| ≤ 0`
   can dominate ⇒ `I(ν) ≥ 0` **fails**. (For the trace problem α is a totally-positive
   algebraic *integer*, a_lead=1 — both OSS hypotheses are absent here.)

Both are reproducible. The +0.0037 "raise" is the artifact of (i) minimizing on a
locus ν avoids and (ii) a column whose `≥0` premise is false. This matches the user's
four-mechanism no-go (the validly-signed energy raise for ZZ is ≈ 0). **Action:
retract R14/R15/R17, reset held to 0.2487458, set Status: none on the lower side**
(upper side 0.2540419719 [R11] is independent and stands).

---

## PART 1 — THE FORWARD ATTACK (non-energy), ranked

Target to beat: **0.2487458 = log(1.282416)** (Flammang [F18], lower bound).
All angles aim strictly above it. NO energy / discriminant-moment / I(μ) self-cut.

### The shared rigor chain (identical to Flammang's, for ANY new column)
For an auxiliary function `f(z) = log⁺|z| + log⁺|1-z| - Σ_j c_j log|Q_j(w)| - Σ_k d_k log|R_k(z)|`
with `c_j, d_k ≥ 0`, `Q_j ∈ ℤ[w]`, `R_k ∈ ℤ[z]`:
- Sum over conjugates α_i of a minimal P: `Σ_i f(α_i) ≥ m·d` where `m = min f` over the
  ν-support.
- `∏_i Q_j(α_i(1-α_i)) = Res(P, Q_j(z(1-z)))` and `∏_i R_k(α_i) = Res(P,R_k)` are
  **nonzero integers off a finite exception set** (det of an integer matrix; nonzero iff
  P ∤ Q_j(z(1-z)) resp. P ∤ R_k) ⇒ `log| | ≥ 0` ⇒ those terms drop ⇒
  `(1/d) log Z(α) ≥ m`. So `C_82 ≥ m`. **This part is exact for z-columns too** —
  the integrality argument is the SAME, no a_lead obstruction, because here we use a
  *resultant of P against a fixed integer polynomial* (always an integer), NOT a
  discriminant of P itself (which carries the a_lead factor that broke OSS).

### THE THREE HARD STEPS, named precisely

**(HS-A) Integrality / exception argument for a z-column.** `Res(P, R(z))` with
`R ∈ ℤ[z]` is a nonzero integer whenever P ∤ R. This is CLEAN — unlike the OSS
discriminant column, there is no a_lead term, because we resultant P against a *fixed*
integer polynomial R, not against P's own derivative. The exception set is exactly the
finite set of minimal polynomials P dividing R(z) (resp. R(1-z) for a 1-z column), to
be adjoined to Flammang's existing exception set `(z²-z)(z²-z+1)φ10(z)φ10(1-z)`.
**This step is SOUND for z-columns** (it is what made the explorers rank the angle —
correctly on this point).

**(HS-B) Does f stay subharmonic-off-circles so the |z|=1 min-locus reduction survives?**
**Partially.** `-d_k log|R_k(z)|` is **harmonic off the zeros of R_k** (Δ log|R_k| = 0
off zeros), exactly like Flammang's `-c_j log|Q_j(w)|` and UNLIKE the superharmonic OSS
term. So the max-principle still puts the min of f on `{|z|=1} ∪ {|1-z|=1} ∪ (R/Q-zero
disks)`, and `-d_k log|R_k| → +∞` at the zeros excludes the disks ⇒ **the min sits on
the two unit circles**. THE STRUCTURE SURVIVES. **BUT:** Flammang's *further* reduction
to `|z|=1` alone uses the z→1-z symmetry, which a z-asymmetric R(z) **breaks**. So the
certificate must minimize over **BOTH** circles |z|=1 and |1-z|=1, not just one. This
is the load-bearing correction.

**(HS-C) The locus trap — caught in pre-screen, DECISIVE.** I solved the discretized
Smyth LP both ways (round 1, scipy linprog, 4000 control points/circle):
- On **|z|=1 only**: adding `R = z³-z+1` raises m by **+1.9e-4** (above the +1e-4 gate),
  c_R = 0.0034 > 0. Three z-cols: +3.1e-4. (Looks like a clean break.)
- On **BOTH circles |z|=1 and |1-z|=1**: the SAME `z³-z+1` raises m by only **+5e-9**,
  c_R → 0. A batch of the 10 best asymmetric z-cols (deg ≤ 4, reduced costs as negative
  as -0.26 on the both-circle dual): total raise **+1.4e-8**. Back at the noise floor.

**Interpretation:** the single-circle LP raise is an ARTIFACT — the column pushes f down
on the |z|=1 arc but *up* on the |1-z|=1 arc; honestly certified (both circles), bare
z-columns buy nothing. This is the SAME wrong-locus error that killed OSS, now caught
before any build. **The explorers' "top" angle (bare z-columns as free slack) is
therefore DISQUALIFIED in its naive form.** What survives is below.

---

### ANGLE 1 (TOP PICK) — High-degree LLL column breeding (in w AND in symmetrized z), priced against the both-circle dual.
**Moves: lower bound, aiming for > 0.2487458 (realistic first gain +1e-4..+5e-4).**

Skeleton:
1. Reproduce the both-circle Smyth LP at Flammang's 24 w-columns; extract the both-circle
   dual measure μ* (support on the binding band) — by scipy linprog (done in pre-screen;
   m* = 0.24874643 matches Flammang).
2. **Breed new integer columns by Flammang's own weighted-integer-transfinite-diameter /
   LLL recipe at degree k = 24…40** (she stopped at k=32 — a compute limit, NOT a
   theoretical one): for each k, minimize `sup_t |Q(v)R(v)| exp(-(r+k)/(2t)log⁺|v|)` over
   integer R via LLL on the Re/Im linear forms at control points v_n seeded **at μ*'s
   support** (the binding band, active min t≈0.577), not Flammang's hand-placed points.
   Breed in **w** AND in the **z→1-z-symmetrized variable** `R(z)R(1-z)` (a single
   ℤ[z]-symmetric column that keeps the symmetry, so it is a genuine new ℤ[w]-or-product
   column reachable only at high degree, and the single-circle reduction stays valid).
3. Price each bred column by reduced cost `∫ log|·| dμ*` against the BOTH-circle dual;
   keep r < -1e-5 (well above the -1e-7 noise floor); add, re-solve the both-circle LP.
4. Iterate (column generation) until no improving column or m clears the gate.
5. Re-certify the final f with `verify_vec.py` (extend to BOTH circles — see Check).

**Hard step:** producing a bred column whose reduced cost is improving on the BOTH-circle
dual AND that survives re-optimization with c > 0 AND raises the both-circle certified
min past 0.2487458 — because the cheap dictionary is LP-optimal (R1: ~2e-11) and the
naive z-cols collapse on both circles (HS-C), so the only remaining slack is genuinely
deep, high-degree LLL-bred columns that pricing CANNOT cheaply generate. Mechanism it
might work: Flammang demonstrably left k>32 unsearched, and seeding LLL at μ*'s actual
support (BMQS's "missing efficient direction") is a sharper criterion than her transfinite
heuristic.

**Check:** (i) re-solve the both-circle LP, confirm m > 0.2487458 + margin; (ii) extend
`verify_vec.py`'s interval B&B to BOTH circles |z|=1 and |1-z|=1 (currently only |z|=1,
line 285) — add the second contour `z = 1+e^{it}` and certify `min over both ≥ m`;
selftest 0 violations; tamper a target above the ceiling → must FAIL. The B&B machinery
transfers verbatim (a z-column adds `-d_k log|R_k(z)|` terms, same log-kink discipline as
the w-columns; the contour eval just adds the second circle).

### ANGLE 2 (HIGH ceiling, heaviest) — Genuine semi-infinite-LP / SOS positivity certificate over the continuum, both circles.
**Moves: lower bound; ceiling = full truncation gap, realistic = whatever the continuum
LP extracts over the discretized one.**

Recast the lower bound as `D(g) = sup_{c,d ≥ 0} min_{both circles} f` and solve it as a
**positivity certificate** rather than a discretized control-point LP. Parametrize each
circle by t, write `g - Σ c_j log|Q_j| - Σ d_k log|R_k| - m ≥ 0` as a trig-polynomial /
rational positivity condition, bound the log terms by supporting affine minorants per arc,
and certify by Fejér-Riesz / Putinar SOS-on-the-circle (cvxpy). The solver chooses c, d
jointly with the positivity multipliers — can beat the discretized LP, whose duals R1 hit
the ~1e-7 noise floor. **Hard step:** the affine-minorant linearization of the logs
introduces slack that can swamp the +1e-4 gate; getting a TIGHT, rigorous SOS certificate
(then rational-rounding the float SDP solution into an interval-verified proof) is real
work. **Check:** the SDP feasibility + a verify_vec.py interval re-certification of the
rounded multipliers. **Best AFTER Angle 1 shows the both-circle LP value clears the gate
— then use SOS to extract the last continuum bit.**

### ANGLE 3 (MEDIUM, transferable-technique, GATED on a literature read) — BMRL Faltings ess-min closing technique.
**Moves: lower bound; room unknown until digested.**

The analogous Faltings stable-height ess-min was CLOSED to 6 digits
(-0.748629 ≤ μ_ess ≤ -0.748622) by Burgos Gil–Menares–Rivera-Letelier [BMRL, Math. Comp.
2018]. Both are height-function ess-mins in the BMQS framework, so BMRL is the closest
worked example of driving the bound with a non-energy method. Candidate transferable
mechanism: their explicit equilibrium-measure / Green-function quadrature on the relevant
curve. **Hard step:** establishing that BMRL's closing technique is genuinely DIFFERENT
from Flammang's Smyth-LP (not the same auxiliary-function machinery relabeled) and that
its curve-specific analytic input has a ZZ analogue — a literature-read gating step before
any build (BMRL not yet on disk; fetch + digest first). **Check:** the digest itself;
no build until the mechanism is confirmed distinct and transferable.

### DISQUALIFIED (do not build) — Bare asymmetric z-columns as standalone free slack.
The explorers' Angle 1 in its naive form. Pre-screen (HS-C): single-circle LP raise
+1.9e-4 is an ARTIFACT; both-circle LP raise +1.4e-8 (noise floor). The asymmetry that
makes a z-column "independent of the w-subalgebra" is exactly what lets it lower f on
one circle while raising it on the other, so it buys no certified bound. Same wrong-locus
trap as OSS. (Symmetrized z-cols R(z)R(1-z) are folded into Angle 1, where they're a
legitimate-but-hard high-degree breeding target.)

### DEAD ENDS — do NOT retry (proven this run)
- OSS log-energy / discriminant-moment / any I(μ)≥0 self-cut: PROVEN no-go (user's four
  mechanisms + the two structural bugs in PART 0). Any disguise (w-energy, symmetrized
  cut, k-point moment).
- Cheap w-variable column generation / products / ±1 perturbations: R1, LP moved ~2e-11.
- Bare asymmetric z-columns (see DISQUALIFIED above): both-circle raise ~1e-8.
- Same-family c_j / q re-optimization: gains < 1e-6.

---

## RANKING & RECOMMENDATION

**Build Angle 1 first.** Reasons: (i) it is the only lever BMQS's own analysis points to
(the unsearched k>32 LLL breeding); (ii) the certificate machinery (`verify_vec.py`)
transfers with one concrete extension (add the |1-z|=1 circle); (iii) it stays inside
Flammang's exact, already-verified resultant-integrality rigor — no new validity argument,
no energy, no locus subtlety beyond "use both circles," which my pre-screen has already
pinned down. Risk is HIGH (historical gains ~5e-4 after big searches; the cheap dictionary
is exhausted, so the gain must come from genuinely deep columns), but the upside is a clean
record-break with a reproducible cert. Fall back to **Angle 2** only after Angle 1's
both-circle LP shows a value above the gate (then SOS tightens it); fall back to **Angle 3**
only after digesting BMRL confirms a distinct, transferable mechanism.

**The single hardest step (across all angles):** producing an integer column — bred by
high-degree (k>32) LLL seeded at μ*'s support — whose reduced cost is improving against the
**both-circle** dual AND that survives re-optimization (earns c > 0) AND raises the
**both-circle** certified min past 0.2487458. Everything cheap is exhausted and everything
asymmetric collapses on the second circle; the gain, if it exists, lives only in deep,
genuinely-new columns that pricing cannot cheaply reach.
