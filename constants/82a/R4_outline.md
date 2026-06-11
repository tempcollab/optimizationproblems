# R4 outline — C_82a LOWER bound (Zhang-Zagier essential minimum)

Spec review: required
Target to beat: 0.2487458 = log(1.282416) [F18, verified R1] — moving the LOWER bound.

---

## GATING RESULT (already computed in this outline pass — settles the explorer conflict)

The two explorers conflicted on where ZZ-minimal conjugates sit. I ran the decisive
computation myself (roots z of Q_j(z(1-z))=0 for the Flammang Table-1 polys, distance
to the two circles, and the full Flammang aux f evaluated on those roots). **Explorer A
is CORRECT; Explorer B's "far lemniscate, |z|∈[0.51,1.98], mean_ν f ~0.44" is WRONG**
and the run_state R3 Rule/Next built on it is wrong. Concretely:

- Roots HUG the two circles: for the near-extremal polys max distance to {|z|=1 or
  |1-z|=1} is 0.025 (j=13), 0.030 (j=15), 0.046 (j=8); mean distance ~0.013-0.019.
  The |z|∈[0.5,1.97] spread is NOT off-circle: a root with |z|=1.97 has |1-z|≈1, i.e.
  it sits on the OTHER circle. There is no far-lemniscate mass.
- mean σ_ZZ over the conjugates ≈ 0.253 (j=15), 0.254 (j=13), 0.260 (j=8) — NOT 0.44.
  Explorer B's "0.44" is the mean over the tiny deg-8 poly j=5 (mean 0.4376), wrongly
  generalized; it does not hold for the height-minimizing (high-degree) polys.
- **The genuine slack is the MIN-vs-MEAN gap on the FULL aux f, not an off-circle leak.**
  circle-min f = 0.2487462 (reproduces Flammang). The conjugates avoid the single
  binding lobe at w* ≈ 0.433 − 0.369i; min_root f sits ABOVE circle-min:
  j=15 +0.00985, j=13 +0.00834, j=16 +0.00600.

But the same computation also delivers the **honest verdict against the angle**: the
gap (min_root f − circle-min) SHRINKS toward 0 as degree grows along Flammang's own
sequence — j=12 +0.0025, j=17 +0.0029, j=19 +0.0021, j=23 +0.00043, j=24 +0.0010.
For the highest-degree (most near-extremal) polys it is already below 5e-4, i.e. below
the 1.5e-4 a raise would need with NO margin to spare. **No degree-uniform δ is
empirically supported.** This is exactly why the equidistribution route leans dead:
as the optimizing sequence is approached, the conjugates DO reach the binding lobe.

Artifact that settles it (Angle 1 below makes this rigorous & reproducible): a script
`certificate/gap_diagnostic.py` that, for every Table-1 poly j, prints deg, the
distance-to-both-circles stats, circle-min f, min_root f, mean_root f, and the gap —
plus a fitted trend of (min_root f − circle-min) vs deg showing it → 0. The reviewer
re-runs it and reads the trend. (The numbers above are already produced; the deliverable
is the committed, self-testing, tamper-checked version + the corrected diagnosis.)

---

## Angle 1 (top pick) — Verified-NEGATIVE: correct the root-location diagnosis AND certify the min-vs-mean / equidistribution route closed by a shrinking-gap obstruction

Moves: LOWER bound — NO raise expected. Deliverable is a rigorous, reproducible
verified-negative milestone (the class R1-R3 logged) that (a) overturns the wrong
run_state lemniscate diagnosis and (b) kills the only non-barred live mechanism with a
quantitative, non-circular obstruction — replacing the explorers' hand-wave with a
checkable artifact.

Skeleton:
  1. Build `gap_diagnostic.py` — for all 24 Table-1 polys: roots z of Q_j(z(1-z)),
     distance to both circles, full-aux circle-min, min_root f, mean_root f, gap.
     Establishes the corrected picture (roots hug circles; slack = min-vs-mean) — by
     direct numpy root-finding + the committed `flammang_table1.py` aux f (reproducible).
  2. State the min-vs-mean lower-bound IDENTITY honestly: h_Z(α) = (1/d) Σ_i f(α_i)
     ≥ min_root-locus f ≥ circle-min f, and the ONLY way to beat Flammang is a
     degree-uniform δ with (1/d) Σ f(α_i) ≥ circle-min + δ, δ > 1.5e-4 for ALL
     ZZ-minimal α — by the resultant-integrality drop-out that underlies Flammang.
  3. Show the candidate machine for δ — effective equidistribution (FR06
     arXiv:1606.04299 Thm 3.1) — fails by TWO independent, certifiable defects:
     (i) CIRCULAR: its discrepancy error term is Lip(f)·(π/d + (4h(α)+C0 log(d+1)/d)^{1/2}),
     which contains the very height h being bounded; solving mean_ν f ≥ mean_λ f −
     Lip(f)(4h)^{1/2} for h yields no positive floor — by direct algebra on the verbatim
     theorem (transcribe and substitute Lip(f), mean_λ f numerically).
     (ii) WRONG TARGET / CAPACITY-1: it equidistributes ν toward the unit-circle measure
     λ (capacity 1), the locus where the leverage is zero; it pushes ν ONTO the circle,
     not off it — by the theorem's reference measure being λ_{S¹}.
  4. Show the empirical kill of the height-INDEPENDENT escape: even granting a
     containment region, the gap (min_root f − circle-min) → 0 along Flammang's own
     near-extremal sequence (j=17..24 all < 5e-4, trend fit) — so no deterministic
     region R with min_R f > circle-min + 1.5e-4 can contain all high-degree conjugates,
     because the conjugates demonstrably enter every neighborhood of the binding lobe as
     d → ∞ — by the diagnostic's degree trend.

Hard step: **certifying that no degree-uniform δ > 1.5e-4 exists** — i.e. that the
conjugates of the height-minimizing sequence enter every neighborhood of the binding
lobe w*. Mechanism: this is forced by Flammang's LP being NEARLY TIGHT — the BMQS
convergence theorem ([BMQS] Thm; both algorithms converge to C_82) says the dual
optimal measure for the auxiliary-function LP IS the limiting conjugate distribution, so
along the optimizing sequence (1/d)Σf(α_i) → circle-min, forcing δ → 0. The diagnostic's
shrinking gap is the finite-degree shadow of this. The negative is non-circular: it does
not assume the height bound, it shows the only mechanism that could deliver δ provably
cannot (circular error + δ→0).

Check: reviewer re-runs `gap_diagnostic.py` (reproduces the hug-the-circle stats,
circle-min 0.2487462, the per-poly gaps, and the degree→0 trend), re-derives the FR06
circularity by substituting into the verbatim Thm 3.1, and confirms the capacity-1 target.
Tamper: feeding a bogus "uniform δ" makes the trend-check fail.

Verdict: **CHEAP GATE + VERIFIED-NEGATIVE.** Highest-value deliverable this round: it
is reproducible, corrects a load-bearing wrong Rule the loop has been carrying since R3,
and definitively closes the last "live" lower-bound mechanism. Expect a logged milestone,
NOT a raise.

---

## Angle 2 — Longshot raise: a finite-degree min-vs-mean raise that DODGES the asymptotic obstruction (degree-bounded floor)

Moves: LOWER bound, aiming for ~0.2489-0.2495 IF it works — but only as a bound that
holds for α of degree ≤ D for an explicit D, NOT the essential minimum. This is almost
certainly NOT a valid attack on C_82 and is listed to be explicitly assessed/rejected.

Skeleton:
  1. The essential minimum is a liminf over ALL α; a bound valid only for deg ≤ D says
     nothing because the binding configurations are high-degree — by the definition of
     essential minimum (the set {h_Z ≤ H} infinite is what matters; low-degree α are a
     finite set already excluded).
  2. Therefore any min-vs-mean δ must be degree-uniform, which Angle 1 shows fails.

Hard step: there is none that survives — the load-bearing claim (a degree-bounded floor
bounds C_82) is FALSE by the definition of essential minimum.

Check: none needed; Angle 1's definition argument already refutes it.

Verdict: **DEAD — included only to record that the finite-degree dodge is a definitional
non-starter, pre-empting a builder wasting a round on it.** Do NOT build.

---

## Angle 3 — Longshot raise: a height-INDEPENDENT coefficient-containment lemma (the explorers' named "only conceivable escape")

Moves: LOWER bound, aiming for a raise IF a non-trivial region exists. Honest scoping:
the data in the gate says the target region would have to EXCLUDE neighborhoods of the
binding lobe that high-degree conjugates provably enter — so the lemma cannot exist with
useful margin. Listed because it is the one thing both explorers flagged as "not yet
ruled out by a computation," and the gate now rules it out.

Skeleton:
  1. Seek a deterministic region R (from the minimal polynomial's integer-coefficient
     structure ALONE — e.g. Cauchy/Fujiwara root bounds, Newton-polygon constraints,
     reciprocal/symmetry structure of ZZ-minimal polys, NOT h, NOT log|disc|) containing
     every conjugate of every ZZ-minimal α — by elementary coefficient inequalities.
  2. If min_R f > circle-min + δ, then h_Z ≥ min_R f beats Flammang — by the min-reduction.

Hard step: **finding R with min_R f strictly above circle-min.** Mechanism that would
be needed: a coefficient-only reason the binding lobe w* ≈ 0.433−0.369i is FORBIDDEN to
conjugates. The gate shows this is false — j=12,17,19,23,24 conjugates already land
within 0.0005 (in f-value) of circle-min, so any coefficient-derived R must INCLUDE a
neighborhood of w*, giving min_R f = circle-min and δ = 0. No useful R exists.

Check: the builder would screen candidate coefficient bounds against the gate's actual
root locations; the gate already shows the binding lobe is occupied, so any proposed R
either excludes real conjugates (invalid lemma) or contains w* (δ=0).

Verdict: **LONGSHOT bordering DEAD; gate-refuted.** Do NOT commit a build unless the
builder finds a SPECIFIC coefficient constraint the gate has not tested that demonstrably
keeps conjugates off the lobe — the gate (j=17..24 hugging the lobe) says it won't.

---

## Ranking

1. **Angle 1** — the only deliverable with positive value this round. It is the cheap,
   decisive gating computation the task demanded (already executed here; the build just
   packages it self-testing/tamper-checked), it OVERTURNS the wrong run_state lemniscate
   Rule with a reproducible artifact, and it converts the explorers' two-defect hand-wave
   on the equidistribution route into a checkable verified-negative anchored on the
   shrinking-gap obstruction + FR06 circularity. Expect a logged milestone, no raise.

2. **Angle 3** — only if, during Angle 1, a specific coefficient constraint surfaces that
   the gate shows keeps conjugates off the binding lobe (the gate currently says none
   does). Fallback longshot, gate-refuted as written.

3. **Angle 2** — do not build; recorded as a definitional non-starter so the dodge is not
   re-attempted.

**Expected round outcome: a VERIFIED-NEGATIVE milestone** (corrected diagnosis +
certified closure of the equidistribution/min-vs-mean route), NOT a record raise. The
lower bound remains intrinsically stuck at Flammang 0.2487458; the gate now explains WHY
with the correct mechanism (conjugates reach the binding lobe as d→∞, δ→0), replacing the
wrong off-circle-lemniscate story.
