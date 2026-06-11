# R2 — Ranked non-OSS attack lines for the C_82a LOWER bound

Outliner, round 2. Target to beat: **0.2487458 = log(1.282416)** [Flammang F18], the
genuine verified lower bar (the R14/R15/R17 OSS values 0.25090/0.25113/0.25240 were
RETRACTED in R1; do not treat them as the bar). Moving the **lower** bound.

All angles below are NON-OSS (no log-energy / discriminant-moment / ∫log|Q(z_i,z_j)|dμdμ
column, energy or otherwise — that whole avenue is proven dead and forbidden).

---

## CRITICAL CORRECTION to the explorer's framing of the integer-locus angle (read first)

The R2 explorer's headline (Angle #1) rests on the claim that "the +2 log|a|/d Weil
penalty pushes non-integers far above the target, so the ess-min lives on the a=1
locus, and a reduction lemma legitimizes a new dictionary." **I checked this
quantitatively and it is substantially wrong on two counts. The integer-locus reduction
is NOT the clean new lever the explorer advertised. Here is the corrected picture, which
re-ranks everything.**

### (i) The a-penalty does NOT push non-integers above the target.
The penalty is `(2 log a)/d`. For fixed a≥2 it → 0 as the degree d → ∞
(`2 log2 / d = 0.0139` at d=100, far below the 0.2487 target). The explorer's
"P=10x²−6x+1 has h_Z=2.30" is true but irrelevant: that polynomial has a=10 **and** d=2,
so its penalty `log10` is huge *because d is tiny*, not because a≥2 is intrinsically
costly. A primitive degree-100 polynomial with a=2 and all roots in the lens
`L = {|z|<1 and |1−z|<1}` would have `h_Z ≈ 2 log2/100 ≈ 0.014`. So if such polynomials
exist, they are non-integers sitting *far below* the target and the naive reduction is
simply false. (Verified by hand: §"Weil penalty" computations, this round.)

### (ii) Where the leading coefficient REALLY enters — and why the reduction is mostly unnecessary, and where needed is circular.
Write `Res(P,R) = a^{deg R} ∏_i R(α_i)` (standard resultant identity, a = lead coeff of P).
Re-deriving the full chain for an auxiliary function with w-columns `Q_j(w)` (weights c_j)
**and** asymmetric z-columns `R_k(z)` (weights d_k):

```
h_Z·d  =  Σ_i f(α_i) + 2 log a + Σ_j c_j log|Res(P,Q_j∘w)| + Σ_k d_k log|Res(P,R_k)|
                                                   − (Σ_k d_k·deg R_k)·log a
       ≥  d·min f + ( 2 − Σ_k d_k·deg R_k )·log a          [Res are integers ⇒ logs ≥ 0]
```

so

```
h_Z  ≥  min f  +  ( (2 − Σ_k d_k·deg R_k) / d )·log a .
```

Consequences (the load-bearing re-derivation of the round):

- **Pure w-columns (Σ_k = 0):** `h_Z ≥ min f + (2 log a)/d`. Valid for **ALL algebraic
  numbers**; a≥2 only *helps*. No integer restriction is needed and never was — Flammang's
  bound is already universal. (This is why the R1 LLL w-breeding was a legitimate, if
  inert, all-algebraic-numbers attack.)
- **Light asymmetric z-columns with `Σ_k d_k·deg R_k ≤ 2`:** the coefficient of `log a`
  is ≥ 0, so the bound is STILL valid for all algebraic numbers with **NO reduction lemma
  at all**. These are exactly the low-weight asymmetric columns — and R1 proved they
  collapse on the both-circle gate (+1.4e-8). So in the regime where no reduction is
  needed, the gate already kills them.
- **Heavy asymmetric z-columns with `Σ_k d_k·deg R_k > 2`:** only HERE does a≥2 hurt, and
  only here does one need to "restrict to a=1." But to discard the a≥2 case rigorously one
  must show every non-integer α with the offending weighted-degree has `h_Z` above the
  target — i.e. bound `h_Z` from below over non-integers — which is **the same problem we
  are trying to solve.** By (i) this is genuinely hard (capacity / integer-transfinite-
  diameter of the lens), not folklore. The explorer's "Northcott + a-penalty" hand-wave
  does not establish it; Northcott bounds the *number* of points of bounded height, it does
  not bound the height of non-integers below the target.

**Net:** the integer-locus reduction is either unnecessary (light columns — and those are
already killed by the both-circle gate) or, where it would be load-bearing (heavy columns),
as-hard-as-the-problem. The explorer's Angle #1 as stated does not open a new dictionary
for free. It is demoted below.

The genuine open question the explorer's instinct points at is narrower and stated as
Angle 2 below: **can the +2 log a/d bonus be banked to admit ONE heavy asymmetric column
whose a=1 both-circle min beats the target, with the a≥2 case covered by a bounded-degree
exceptional argument?** That needs the reduction only for *small d* (where the bonus is
large), and the exceptional set there is finite by Northcott — which is the one place
Northcott genuinely bites. That is the only non-circular version, and it is still risky.

---

## Angle 1 (TOP PICK) — Contour/measure-support tightening of the EXISTING both-circle relaxation, plus deep w-LLL re-screen with the corrected dual.
**Spec review: skip** (routine push on Flammang's verified machinery; rigor chain
identical to F18, no new validity claim — the all-algebraic-numbers validity is the
already-verified resultant-integrality argument).

**Moves: lower bound, aiming for > 0.2487458; realistic first gain +1e-4..+5e-4 if any.**

Mechanism / why it could beat the bar. The explorer's §1 says the discretized w-LP is
"exhaustively tight" (dense equioscillation, all 24 columns active). But "tight at the
fixed 24-column dictionary" is not "tight at the optimum over ℤ[w]": Flammang stopped her
integer-transfinite-diameter search at degree k≤32, an admitted compute limit, not a
theoretical ceiling. The slack, if any, is in deg-23..40 w-columns that her LLL pass and
R1's LLL pass (seeded at the single-circle dual) did not reach. The refinement here is to
(a) re-extract the dual μ* from a **higher-resolution continuum** solve (the equioscillation
band is the support; place control points adaptively at the ~12 lobes rather than uniformly),
and (b) seed Flammang's own weighted-integer-transfinite-diameter LLL recipe at that sharper
μ*, sweeping k=24..40 with several lattice scalings per k.

Skeleton:
1. Re-solve the Smyth LP at Flammang's 24 columns with adaptive control points clustered at
   the equioscillation lobes; confirm m* reproduces 0.2487464 and extract μ* — by scipy linprog
   (machinery exists: `stageB_colgen.py`, `lll_breed.py`).
2. Breed integer w-columns Q(w), deg k=24..40, by Flammang's transfinite-diameter/LLL recipe
   seeded at μ*'s lobes; price by reduced cost `∫log|Q| dμ*` — by LLL (extend `lll_breed.py`
   past k=40 with finer scalings).
3. Keep any column with reduced cost < −1e-5 (well above the −3.5e-14 R1 noise floor),
   add it, re-solve the LP, iterate (column generation) until no improving column.
4. Re-certify the final f with the existing interval-B&B `verify_vec.py` (single circle
   suffices — w-columns are z→1−z symmetric); confirm certified min > 0.2487458 + margin.

Hard step: producing a deg-23..40 w-column whose reduced cost against the sharpened μ* is
strictly improving AND that survives LP re-optimization with c>0 — because R1's k≤40 LLL pass
came back inert (best genuine reduced cost ≥ 0), so the only hope is that R1's *uniform-grid*
dual was slightly off the true equilibrium measure and a *lobe-adaptive* dual prices a column
that the uniform dual rounded to 0. This is a real but modest mechanism: a sharper μ* can flip
a marginally-positive reduced cost negative.

Where it collapses: if the lobe-adaptive μ* prices the same columns ≥0 as R1's uniform μ*
(very likely — the equilibrium measure is what it is, and R1 already swept 100+ columns/degree),
the lever is confirmed exhausted and the round logs an honest negative. This is the most likely
outcome; rank it top only because it is cheap, fully rigorous, and the one remaining unscreened
*depth* in the already-verified all-algebraic-numbers method.

Check: re-solve LP (m* > target + margin?); `verify_vec.py certify <target>` from scratch
(frontier=0, selftest 0 violations); tamper a target above the ceiling → must FAIL.

---

## Angle 2 (HIGH ceiling, HIGH risk) — Bank the (2 log a)/d bonus to admit ONE heavy asymmetric z-column, with the a≥2 case closed by a bounded-degree Northcott exceptional argument.
**Spec review: REQUIRED** (the validity rests on a non-obvious split of the a-penalty and a
finite-degree exceptional-set claim; the both-circle min must clear the gate on the a=1 locus,
which R1 pre-screening suggests it does not. Review before any compute.)

**Moves: lower bound, aiming for > 0.2487458.**

Mechanism. From the corrected identity, a single asymmetric z-column `−d_R log|R(z)|` of
degree r with weight d_R gives
`h_Z ≥ min_{both circles} f + ((2 − d_R·r)/d) log a`.
Split by degree d of α:
- **Small d (d ≤ D_0):** finitely many α by Northcott once h_Z is below the target +1; here
  the a≥2 penalty `(2 − d_R r)/d · log a` is the LARGEST (small d), and one can simply
  *enumerate* the finite exceptional set of low-degree non-integers and verify each has
  h_Z above the target directly. This is the one place Northcott genuinely bites — and it is
  rigorous and reproducible (a finite computation).
- **Large d (d > D_0):** the penalty coefficient `(2 − d_R r)/d` → 0; if it is the *negative*
  side (heavy column, d_R r > 2), the deficit is at most `(d_R r − 2)/d · log a`. For this to
  stay below the margin one needs an explicit upper bound on `log a` in terms of d for
  near-minimal α — i.e. a Mahler-measure/length bound `log a ≤ (something)·d` valid on the
  near-minimal locus. **This is the hard, possibly-fatal step.**

Skeleton:
1. Re-derive the split bound `h_Z ≥ min_bothcircles f + ((2 − Σ d_k deg R_k)/d) log a` — by the
   resultant identity above (already done this round, reproducible).
2. Re-solve the BOTH-circle LP (|z|=1 ∪ |1−z|=1) admitting asymmetric z-columns; find a column
   (or small set) whose a=1 both-circle certified min exceeds the target by a margin
   ε > 0 — by scipy linprog (machinery: extend `stageB_colgen.py` to both circles).
3. Bound the large-d deficit: prove `(d_R r − 2)/d · log a < ε` for all near-minimal α of degree
   d > D_0 — by an explicit `log a` vs d bound on the near-minimal locus (Mahler-measure/length).
4. Close the small-d exceptional set by direct enumeration (finite, Northcott).
5. Certify the a=1 both-circle min with B&B extended to both circles.

Hard step (load-bearing, likely fatal — two of them):
- **(2)** the a=1 both-circle min beats the target. R1's both-circle pre-screen showed
  asymmetric z-columns collapse to +1.4e-8 *even at a=1* (they lower f on |1−z|=1 as much as
  they raise it on |z|=1). The banking trick does NOT change this — it only addresses a≥2.
  So step 2 inherits the same wall. **The both-circle gate is the real obstruction and the
  banking trick does not touch it.** Unless a genuinely new heavy column clears the gate
  (which R1 found none did), this dies at step 2.
- **(3)** the `log a ≤ c·d` bound on the near-minimal locus. There is no obvious reason a
  near-minimal non-integer cannot have a moderately large leading coefficient; this needs a
  real theorem.

Where it collapses: at step 2 (both-circle gate, the same wall as R1) with high probability;
secondarily at step 3 (unproven `log a` bound). Pre-screen step 2 with a ~2 min both-circle
linprog BEFORE any reduction work — if no admissible heavy z-column clears the a=1 gate by a
margin exceeding the projected large-d deficit, abandon. **Do not let the builder spend compute
on the reduction lemma until the both-circle gate is shown to be clearable.**

Check: both-circle LP value; the finite small-d enumeration; the `log a` bound derivation;
B&B over both circles.

---

## Angle 3 (MEDIUM, transferable technique) — Smyth integer-transfinite-diameter / integer-Chebyshev refinement of the column search, not the LP.
**Spec review: skip** (it is Flammang's own method machinery, no new validity claim; it is a
better *search* for ℤ[w] columns, which is fully covered by the verified resultant-integrality
rigor).

**Moves: lower bound, aiming for > 0.2487458; realistic gain ≤ +5e-4 (capped by the ℂ[w]
equioscillation ceiling).**

Mechanism. Flammang ties her column set to the **weighted integer transfinite diameter**
t_{Z,φ}(C) of the contour C={w=e^{it}−e^{2it}} with weight φ=(max(1,|z|)max(1,|1−z|))^{−1}.
The lower bound she can reach equals (heuristically) −log t_{Z,φ}. Her LLL search is one way to
approximate the optimal integer polynomial; modern integer-Chebyshev solvers (Pritsker-style
semidefinite / LP-relaxed integer transfinite diameter, or Flammang's own later "explicit
auxiliary functions" machinery for the integer transfinite diameter of intervals) can sometimes
find better integer polynomials than vanilla LLL. The idea: replace the LLL inner loop with a
genuine integer-transfinite-diameter optimizer over the lemniscate contour, which may surface a
deg-25..35 ℤ[w] column LLL missed.

Skeleton:
1. Reproduce the weighted integer transfinite diameter setup on C; confirm the current 24-column
   value matches Flammang's reachable bound — by transfinite-diameter quadrature.
2. Run an integer-Chebyshev / IP-aided generator (LP relaxation + branch over the leading few
   integer coefficients) to produce candidate ℤ[w] columns minimizing `sup_C |Q(w)|·φ^{deg}`.
3. Price/add/re-solve as in Angle 1; certify with `verify_vec.py`.

Hard step: the IP-aided generator finds a ℤ[w] column with reduced cost < −1e-5 that LLL
(R1, k≤40) missed — because IP can explore non-LLL-reduced integer vectors near the equilibrium
support. Mechanism it might work: LLL only returns short vectors of one lattice basis; the
transfinite-diameter optimum need not be LLL-short.

Where it collapses: the §1 equioscillation says ℂ[w] is essentially saturated to degree ~22, so
even the *real-coefficient* optimum over ℂ[w] is near 0.2487; integer columns cannot beat the
real relaxation. The ceiling here is low (the explorer is right that ℂ[w] is near-saturated).
Worth it only as a stronger version of Angle 1's step 2, not standalone. Demote below Angle 1.

Check: same as Angle 1.

---

## Ranking and recommendation

**Build Angle 1 first.** It is fully rigorous (Flammang's verified all-algebraic-numbers
chain, no new validity claim, `Spec review: skip`), cheap (~minutes of linprog + LLL), and it
is the one remaining unscreened *depth* in the established method: a lobe-adaptive dual + LLL
sweep to k=40 that R1's uniform-grid pass may have narrowly missed. Most likely it confirms the
ℤ[w] dictionary is exhausted (honest negative, no milestone), but it is the correct cheap shot
to take before anything heavier.

**Fall back to Angle 3** (IP-aided integer-Chebyshev column search) if Angle 1's LLL is inert —
it is the same low-risk, fully-rigorous lane with a stronger search engine, but the ℂ[w]
equioscillation ceiling caps its upside.

**Hold Angle 2 (the integer-locus / a-penalty-banking line) as the only HIGH-ceiling shot, but
gate it hard.** It is the sole route to a genuinely NEW (asymmetric, non-ℂ[w]) column, but the
corrected analysis shows its real obstruction is the **both-circle gate at a=1** — exactly the
wall R1 proved (+1.4e-8) — which the a-penalty banking does NOT relieve. **Before any builder
compute on the reduction lemma, run the ~2-min both-circle linprog pre-screen** (per-role rule
from R1): admit a basket of asymmetric z-columns up to weighted-degree ~6, re-solve over both
circles at a=1, and check whether ANY clears the target by a margin exceeding the projected
large-d deficit. If it does not (the expected outcome), Angle 2 is closed without the heavy
reduction work. Only if the pre-screen surfaces a heavy column that clears the a=1 gate does the
reduction lemma (small-d Northcott enumeration + large-d `log a ≤ c·d` bound) become worth
building — and then it needs full outline review.

**The single hardest step across all angles:** finding ANY admissible column (w or asymmetric z)
that raises the honest min — single circle for w, BOTH circles for asymmetric z — strictly past
0.2487458. Everything cheap and symmetric is verified exhausted (R1: ℤ[w] LLL ≥0 reduced cost,
~3.5e-14; both-circle asymmetric collapse +1.4e-8). The integer-locus reduction does NOT enlarge
the admissible class for free; the both-circle gate is the real frontier and it is unbroken.

## R2 BUILD RESULT (proof-builder) — both screens INERT/COLLAPSED, no raise

Built two decisive cheap screens; both are clean reproducible NEGATIVES (no bound raise).
Verified bar unchanged: Flammang [F18] 0.2487458. held lower stays 0.2487458.

### SCREEN A (Angle 2 both-circle pre-screen) — VERDICT: COLLAPSED-ON-SECOND-CIRCLE.
`certificate/screen_a_zcolumn.py` (re-runnable, ~1 min).
- Anchor: single-circle Flammang LP reproduces m* = 0.2487464129 (bar 0.2487458, slack ~1.6e-6).
- Added each of 17 genuinely-asymmetric integer z-columns -d·log|R(z)| (R∈Z[z], NOT in w;
  confirmed asymmetric: |log|R|| differs by 1.6..47 between |z|=1 and |1-z|=1) to the 24
  w-columns and solved the BOTH-CIRCLE LP (constraints enforced on both arcs, one shared aux f).
- EVERY asymmetric z-column gets optimal weight d ≈ 0 (max 8e-8); the LP raise is +1.3e-8..+2.4e-8,
  three orders below the +1e-5 gate (consistent with R1's +1.4e-8). Basket of all 17 together:
  0 active z-cols, raise +1.6e-8. The LP REFUSES to use any asymmetric column.
- MANDATORY plane-min check (corrected σ): the honest σ is the Zhang-Zagier density
  σ_ZZ(z)=log max(1,|z|)+log max(1,|1-z|) (Flammang eq 2.1), NOT log max(1,|w|) — they agree
  only on |z|=1. With σ_ZZ: (a) Flammang pure-w f has global PLANE min 0.248785 (z=1.14-0.99j)
  = circle min 0.248746 to grid resolution 3.9e-5 → plane-min ON circles, anchor SOUND.
  (b) FORCING d=0.05 on z²-1 drops the plane min to 0.199 and the circle min to 0.194 — both far
  below the bar. This is the mechanism: any asymmetric column lowers f on the second circle as much
  as it raises it on the first, so the LP zeroes it out and banking ((log a)/d, exactly 0 at a=1)
  is orthogonal to the gate. Angle 2 is dead at step 2, as the outline review predicted.

### SCREEN B (Angle 1 lobe-adaptive dual + deep w-LLL re-screen) — VERDICT: INERT.
`certificate/screen_b_lobe_lll.py` (re-runnable, ~3 min).
- Re-solved the LP on a LOBE-ADAPTIVE grid (14560 control points clustered at the equioscillation
  lobes / lowest-8%-slack band t∈[0.486,2.845]), extracting a sharper dual mu_lobe (distinct from
  R1's uniform-grid dual). m_lobe = 0.2487463515.
- Re-priced (i) 20147 cheap integer w-columns and (ii) deep LLL-bred columns k=24..40 (5 lattice
  scalings each) against mu_lobe. Best reduced cost across ALL columns: -5.56e-7 (a high-degree
  product col), within LP noise, ABOVE the -1e-5 gate. LLL columns: best -1e-13 (pure noise).
- DECISIVE accumulation test: added ALL 144 negative-reduced-cost cheap columns and re-solved —
  m_new = 0.24874634, a raise of -1.1e-8 (i.e. NONE; the -5e-7 costs are discretization artifacts
  that vanish on re-optimization). Z[w] is LP-saturated to deg ~40 against the lobe dual too.
- This CLOSES the lobe-adaptive-dual lever, distinct from R1's uniform-dual closure (different dual,
  same conclusion). The equilibrium measure is what it is.

### What would push it further (honest)
Both cheap forward levers are now closed. The both-circle gate for asymmetric z-columns is a
genuine structural wall (f symmetric on the w-part forces equal-and-opposite movement across the
two arcs). The ONLY remaining non-OSS upside lives in HEAVY machinery the screens did not touch:
a moment-SOS/SDP positivity certificate over the CONTINUUM that could in principle find a
real-coefficient aux function the discretized LP's fixed dictionary misses — but the §1
equioscillation evidence (all 24 columns active, dense Chebyshev optimum) suggests C[w] is
near-saturated to deg ~22, capping that too. No cheap shot remains.

## Dead ends (do NOT retry — confirmed this round and prior)
- Asymmetric z-columns (single OR basket) on the both-circle LP at a=1: weight→0, raise +1.6e-8,
  far below gate; plane-min DEMO shows forced z-weight collapses f to 0.194 on the second circle
  (R2 screen_a_zcolumn.py). Banking the (log a)/d bonus is orthogonal (=0 at a=1). CLOSED.
- Lobe-adaptive dual + deep LLL/cheap w-column re-screen k≤40: best reduced cost -5.56e-7 within
  noise, vanishes on LP re-optimization (raise -1.1e-8 with all 144 negatives added). Z[w]
  LP-saturated to deg 40 against the lobe dual (R2 screen_b_lobe_lll.py). CLOSED.
- ANY OSS log-energy / discriminant-moment / multivariate ∫log|Q(z_i,z_j)|dμdμ column
  (energy OR non-energy): proven no-go (user's four mechanisms + R1's two structural defects).
- BMRL Faltings closing technique: digested R2 — same Smyth method, modular-curve-specific
  Koebe machinery inapplicable. CLOSED.
- Bare/light asymmetric z-columns as standalone slack: both-circle collapse +1.4e-8 (R1), and
  the integer-locus reduction does not help them (they are the Σ d_k deg R_k ≤ 2 regime where
  no reduction is even needed — the gate, not validity, kills them).
- Symmetrized R(z)R(1−z): reduces to a ℤ[w] column (R1 review B.3); inside the exhausted dict.
- k≤40 LLL w-breeding on the UNIFORM-grid dual (R1 inert); same-family c_j re-optimization (<1e-6).
- The explorer's "a-penalty pushes non-integers above target" reduction AS STATED: false
  (penalty → 0 as d → ∞; corrected this round).
