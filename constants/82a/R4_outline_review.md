# R4 outline review — C_82a LOWER bound

Reviewed: `constants/82a/R4_outline.md` (against `R4_explore_gap.md`,
`R4_explore_methods.md`, `bmqs_2026_digest.md`, run_state R3 rules).
Target to beat: Flammang 0.2487458. No raise is proposed; the deliverable is a
verified-NEGATIVE milestone.

## Verdict: BUILD ANGLE 1 — but with one mandatory scope correction

Angle 1 is the right round to run and most of it is rigorously supportable. I
independently reproduced the two factual cores. **However, the outline's headline
"the only live lower-bound mechanism is DEAD" is OVERSTATED on its load-bearing
ground (δ→0).** The supportable claim is narrower: "the FR06 equidistribution route
is circular/capacity-1 inert, and no *cheap, screenable* min-vs-mean lever survives
this round." The build must be scoped to that, not to a blanket "route dead." Angles
2 and 3 are correctly dispositioned (do not build). Nothing barred/closed is proposed.

---

## Claim 1 (root-location correction) — CONFIRMED SOUND. Reproduce it; it is a real milestone.

I recomputed independently (fresh numpy, roots of Q_j(z(1-z)), distance to both
circles, sigma_ZZ = log+|z| + log+|1-z| averaged over conjugates):

```
 j  deg_w  max-dist-to-2-circles  mean-dist   mean sigma_ZZ
  5    4         0.0000              0.0000        0.2406
  8    8         0.0461              0.0173        0.2604
 13   12         0.0251              0.0187        0.2537
 15   16         0.0299              0.0127        0.2527
 17   16         0.0376              0.0151        0.2563
 23   22         0.0497              0.0207        0.2431
 24   22         0.2042              0.0315        0.2712
```

- Roots HUG the two circles (mean distance 0.013–0.034; max usually < 0.05). The
  |z| ∈ [0.5, 2.0] spread is exactly the outline's explanation: a root with |z|≈1.97
  has |1-z|≈1, i.e. it sits on the OTHER circle. There is no far-lemniscate mass.
- mean sigma_ZZ ≈ 0.24–0.27, NOT 0.44. Explorer B's 0.44 is the mean over the tiny
  deg-8 poly j=5 (I get 0.4376 there too) wrongly generalized.

**Explorer A is correct; Explorer B's lemniscate/0.44 story is wrong, and the R3
run_state Rule built on it must be retracted.** This correction is genuinely worth a
milestone and the `gap_diagnostic.py` artifact makes it reviewer-reproducible.

I also reproduced the FULL-aux-f numbers to the digit: circle-min f = **0.2487462**
(reproduces Flammang); per-poly (min_root f − circle-min) gaps j=15 +0.00985,
j=13 +0.00834, j=16 +0.00600, j=17 +0.00294, j=23 +0.00043, j=24 +0.00100 —
matching the outline. The min-vs-mean REFRAMING is correct.

## Claim 2 part A (FR06 circular + capacity-1) — SOUND. Build it as stated.

The FR06 Thm 3.1 defect is real and non-circular as a negative:
- The discrepancy error is Lip(f)·(π/d + (4h+C0 log(d+1)/d)^{1/2}); solving
  mean_ν f ≥ mean_λ f − Lip(f)(4h)^{1/2} for h gives no positive floor — the bounded
  quantity h sits inside the error. This is a rate statement (small h ⇒ near-equidist),
  not a floor generator. Correct.
- Target measure is λ_{S¹} (capacity 1), the locus where leverage vanishes. Correct.

This half is a legitimate, checkable verified-negative. Keep it.

## Claim 2 part B (δ→0 ⇒ route dead) — DEFECTIVE as written. MUST be downgraded.

This is the load-bearing flaw and the reason the verdict is "build with correction,"
not "build as-is." Three specific defects:

### Defect 1 — conflates the MIN gap with the MEAN gap (the mechanism uses the MEAN).
The lower-bound identity is h_Z(α) = (1/d) Σ_i f(α_i) ≥ circle-min + δ, where δ is the
gap on the **MEAN** of f over the conjugate measure, NOT the min. The outline's "δ→0"
evidence (j=17 +0.0029 … j=23 +0.0004) is the **min_root f − circle-min** column. The
**mean** gap does NOT collapse — from the same aux-poly-root proxy I get:

```
deg_w   mean-gap    min-gap
  12    +0.0062     +0.0025
  12    +0.0113     +0.0083
  16    +0.0143     +0.0099
  16    +0.0158     +0.0060
  16    +0.0076     +0.0029
  17    +0.0054     +0.0021
  22    +0.0090     +0.0004
  22    +0.0209     +0.0010
```

The mean gap stays +0.005 to +0.02 at the highest degrees — two orders above the
1.5e-4 threshold. The outline's central "δ shrinks below 5e-4" reads the wrong column.
A reader who only sees the min column would wrongly conclude the route is dead; the
quantity that actually feeds the bound is healthy in this data. **This must be fixed:
the diagnostic must report and discuss the MEAN gap, and the negative cannot rest on
the min gap shrinking.**

### Defect 2 — the "forced by BMQS convergence" mechanism does not establish δ→0.
The hard step (lines 78–86) cites BMQS Thm D: D(g) = ess(h_ZZ) = P(g), claiming the
dual-optimal measure's f-mean → circle-min, forcing δ→0. This is a non-sequitur.
Strong duality says the LP value EQUALS C_82 — but C_82 is exactly the unknown
(0.2487 ≤ C_82 ≤ 0.2540). Equality at the optimum tells you the optimal mean equals
ess(h), it does NOT tell you that ess(h) = circle-min. If the true C_82 were, say,
0.249, the dual-optimal mean would converge to 0.249, i.e. δ → +0.0003 > 1.5e-4, NOT
to 0. The BMQS digest itself states "no practical algorithm is known" and gives no
rate — so it cannot supply the "δ→0" the outline needs. **The BMQS handoff is a hard
step named without a working mechanism; it must be removed or restated as conjecture.**

### Defect 3 — sampling-artifact concern is real and not addressed.
The task flagged it correctly: the only sequence examined is Flammang's near-extremal
Table-1 polys, which are by construction the aux polynomials whose binding-lobe roots
push the min toward circle-min. These are NOT the minimal polynomials of actual
small-height ZZ numbers, and "min_root f → circle-min along THIS sequence" says
nothing about whether a different family of ZZ-minimal α keeps the mean gap bounded
below. The outline asserts "no degree-uniform δ is empirically supported" from a
single, self-selected sequence read on the wrong (min) column. That is a sampling
artifact, not an obstruction.

## What the build must change

1. **Downgrade the headline.** Not "the only live lower-bound mechanism is DEAD."
   The supportable claim is: *(a)* the run_state lemniscate/0.44 diagnosis is wrong
   and corrected (rigorous, reproducible); *(b)* the FR06 equidistribution route is
   circular + capacity-1 inert (rigorous); *(c)* no CHEAP, SCREENABLE min-vs-mean
   lever was found this round — the genuine min-vs-mean slack (mean gap +0.005–0.02)
   remains UNCAPTURED because the only known device to convert "conjugate mean exceeds
   circle min" into a uniform floor is an effective-equidistribution / height-
   independent-containment argument that does not exist. Frame it as
   **"no cheap lever found; the correct slack is identified but its capture is open,"**
   NOT "route closed."
2. **Report the MEAN gap** in `gap_diagnostic.py`, prominently, and stop resting any
   conclusion on the min-gap-shrinking trend. The min trend is a side observation, not
   the obstruction.
3. **Remove the BMQS-forces-δ→0 claim** (Defect 2) or label it explicitly as an
   unproven conjecture. Do not certify a negative on it.
4. **Do not claim degree-uniformity is empirically refuted** — one self-selected
   sequence read on the wrong column cannot refute it. State honestly that a
   degree-uniform mean floor is neither established nor refuted by this data; what is
   established is that the FR06 route cannot deliver it.
5. Keep the tamper/self-test harness; ensure "tamper" tests the genuinely load-bearing
   quantities (circle-min reproduction, FR06 substitution), not the unsupported δ→0
   trend.

## No barred/closed angle is proposed — confirmed
Angle 1 uses only: numpy root-finding, the committed Z[w] aux f, FR06 Thm 3.1 algebra,
BMQS duality (as context). It does NOT touch OSS energy / multivariate-integrality /
power-sum / resultant LP, contour-LP / Z[w] / SOS raise, asymmetric-z, k>32 LLL,
integer-locus, or BMRL. Angle 2 (finite-degree dodge) is correctly killed on the
definition of essential minimum — do not build. Angle 3 (coefficient-containment
lemma) is correctly scoped as longshot/gate-refuted — do not build unless a specific
coefficient constraint surfaces, which the data says it won't.

## Is the verified-NEGATIVE a real milestone or a numerical observation dressed up?
With the corrections above, YES it is a real milestone: parts (a) the corrected
root-location diagnosis and (b) the FR06 circularity are both rigorously checkable and
reviewer-reproducible (re-run `gap_diagnostic.py`; re-derive the FR06 substitution).
WITHOUT the corrections, the "route dead" claim is a numerical observation (one
sequence, wrong column, unsupported BMQS leap) dressed as a closure — and a reviewer
re-deriving the load-bearing step would correctly reject the "dead" verdict. The build
must ship the narrower, defensible claim.

## Per-role memory note
The lower-bound mechanism for 82a is `(1/d)Σf(α_i) ≥ circle-min + δ` with δ the MEAN
gap; a "shrinking gap" argument that reads min_root f instead of mean_root f is reading
the wrong column and understates δ by ~3x. The mean gap over Flammang Table-1 aux roots
stays +0.005–0.02 at deg 22.
