# R7 — Ranked STRUCTURAL attack angles for C_82 (Zhang-Zagier ess. min)

Outliner, round 7 (DEPTH). Builds on the three R7 explorer reports
(`R7_explore_structure.md`, `R7_explore_analogous.md`, `R7_explore_polya.md`) and the
prior approach docs. NO more same-family q-tuning (user directive; well dry, R6 gained
1.8e-6). Every angle below aims STRICTLY past the held records.

## Spec review: required
(Angle 1 — the chosen build target — rests on a non-obvious feasibility claim: that a
NEW small-height admissible perturbing factor strictly lowers the family minimum past a
thin ~1e-4 margin. Worth a cheap outline review before the builder spends compute.
Angle 2 is genuinely novel machinery and would ALSO need review if promoted.)

## Targets to beat (verified, exact)
- UPPER bound: **0.2543309112** (held R6; was log 1.289735 = 0.25443677 [Doc01b]).
  Any admissible {P_m, Q_i} + one feasible q with a certified-from-above integral
  < 0.2543309112 is a record. NO optimality burden.
- LOWER bound: **0.2487458** (= log 1.282416 [Flammang F18]; registry 0.24874). Only
  REPRODUCED in R1, never beaten. A break needs m = min over the circle of the
  auxiliary function strictly > 0.2487458, rigorously certified.

True ess min lies in (0.2487, 0.2543); Doche conjectures it < log 1.2875274 = 0.25272.
Both sides are TRUNCATION-limited, not duality-gap-limited (BMQS Thm D, R7 polya report)
— so both are legitimately attackable, neither is RH-class.

================================================================================

## Angle 1 (TOP PICK — build this round): enrich the UPPER perturbing dictionary
### with ONE new small-height admissible factor Q_3 in X = z(1-z)

**Moves:** UPPER bound, aiming for < 0.2543309112 (any strict break banks a milestone;
realistic reach ~0.2540–0.2543 this round, with structural headroom to ~0.2527 over
several rounds if a genuinely smaller-height factor lands).

**Why this is the lever (structure report, author's own voice):** every historical
upper-side jump came from a RICHER dictionary, never from finer q. Doc01a→Doc01b
(1.2916674→1.289735, ~2e-3 in measure) came ENTIRELY from moving to the X-variable to
"increase the number of perturbing factors" and adding P6,P8,Q2. Doche calls the
perturbing-factor choice "more arbitrary" and "we do not understand why it is so
important." The continuous optimum of the FIXED {P1,P2,P4,P6,P8,Q1·Q2} dictionary is
drained (R5/R6). The untouched lever is the dictionary itself.

**Skeleton:**
  1. Recover the EXACT held-record dictionary into one self-contained module: the five
     base polys {P1,P2,P4,P6,P8} and the two perturbing factors Q1, Q2 (in X) that
     `certify_q.py` already uses at D=56 — read them straight out of the existing
     verified harness, NOT re-transcribed from the PDF. CALIBRATION GATE: reproduce the
     held float log h(q)=0.2543308 at the R6 q before touching anything. — by reading
     `verify_upper.py`/`certify_q.py` + one float eval.
  2. Pick ONE candidate new perturbing factor Q_3(X): a small-ZZ-height integer poly in
     X whose roots cluster the z-images so log+|z|+log+|1-z| is small. Two cheap
     sources, in order of preference:
       (a) the degree-24 factors Qa, Qb already transcribed in
           `upper-bound-optimization.md` (lines 36–41) — Q1=Qa·Qb is the Doc01a
           calibration perturber; try Qa or Qb ALONE, or a known small-height
           sibling, as an INDEPENDENT third block (exploit Doche's ℓ>1: its own
           exponent q_6).
       (b) a small-height poly from the Flammang/Doche tabulated list whose X-roots
           sit near the active band — degree ≤ 32, integer coeffs.
     — by selecting from already-on-disk polynomials (no breeding this round).
  3. Check ADMISSIBILITY for {old} ∪ {Q_3}: Doche Lemma 5 / condition (4) — deg Q_3>0,
     Q_3(0)=Q_3(1)=1, gcd(P_i, Q_3)=1 for all five P_i, and the non-triviality
     prod P^n / prod Q^n ≠ ±1. This is q-INDEPENDENT and is a finite sympy check. — by
     the same `admiss` routine the harness already runs, extended to Q_3.
  4. Re-optimize q over the ENLARGED family (now 6 exponents: q1..q5 plus q6 on Q_3) by
     multistart Nelder-Mead/L-BFGS, seeded at the R6 optimum with q6=0 (which recovers
     the held value exactly, so the new optimum can ONLY go down or stay equal). Report
     the FLOAT min as a conjecture. — by scipy.
  5. IF the float min < 0.2543309112: certify it with the EXISTING reviewer-verified
     `certify_q.py` max(A,B) outward-rounded quadrature, with only the (positive)
     exponent vector and the Q-list extended. The bound is automatic for any admissible
     q. — by the in-hand harness.

**Hard step (single, gating):** *producing a Q_3 whose addition makes the continuous
optimum strictly drop below 0.2543309112.* Mechanism it works: adding an admissible
factor with its own free exponent strictly ENLARGES the family, so min h(q) can only
decrease or stay equal (seed q6=0 reproduces the held value); the new degree of freedom
will move it down unless Q_3 is orthogonal to the active band. Mechanism it can fail:
the margin is thin (~1e-4 below Doc01b, and the held value is nearly tight against the
family's float optimum), so a WEAK Q_3 (height not genuinely small, or roots off the
active band) buys nothing — then this round banks only a re-certification, not a break.

**Check (builder runs / reviewer reproduces):** one script that (a) prints the
calibration float 0.2543308 at R6 q (Q_3 off), (b) prints the new float optimum and q
(conjecture), (c) runs `certify_q.py` with the extended dictionary to print the rigorous
outward-rounded enclosure hi < 0.2543309112, (d) prints the sympy admissibility check for
Q_3. Reviewer re-runs the same harness (already verified in R5/R6) with the new inputs.

**Smallest ATOMIC first builder step (THE build for this round):**
> *Add exactly ONE candidate Q_3 (start with Qa from upper-bound-optimization.md as an
> independent third block), run the Lemma-5 admissibility check on it, then re-optimize q
> over the 6-exponent family seeded at the R6 point with q6=0, and report the float
> optimum.* — That is the whole atomic deliverable. Certification (step 5) only fires IF
> the float drops; if it doesn't, the round bankably reports "Qa does not improve;
> next candidate" and stops. No multi-stage breeding, no PDF transcription, one new poly.

================================================================================

## Angle 2 (HIGHEST STRUCTURAL UPSIDE, but NOT atomic this round):
### add the concave logarithmic-energy / discriminant constraint to the LOWER LP

**Moves:** LOWER bound, aiming for > 0.2487458. This is the OSS 2024 method
(arXiv:2401.03252) — the single largest Schur-Siegel-Smyth jump in 40 years
(1.7931→1.80203) — transferred to 82a's closest cousin.

**The idea:** Flammang's f(z) uses ONLY univariate columns log|Q_j(w)| (resultant
integrality). The conjugate measure μ of any ZZ algebraic integer ALSO satisfies the
MULTIVARIATE integrality constraint
        I(μ) := ∫∫ log|z₁ − z₂| dμ(z₁) dμ(z₂) ≥ 0,
valid because prod_{i<j}(α_i−α_j)² = disc(P) is a nonzero integer, so |disc| ≥ 1. This
is a genuinely NEW, independent dual column Flammang/Smyth never used (confirmed against
`flammang_F18_digest.md`). Adding it to the Smyth LP can only RAISE the lower optimum m.

**Skeleton:**
  1. State the energy constraint and its validity (disc-integrality) for the ZZ
     conjugate measure in the z-variable. — by the OSS/Orloski-Talebizadeh argument
     (cite OT23, OSS24).
  2. Augment Flammang's primal measure-LP with I(μ) ≥ 0; the dual auxiliary function
     gains a self-coupled potential term λ₀·U_μ(z) (OSS Thm 1.1). — by LP duality.
  3. Solve the self-consistent (μ, support Σ, λ₀) optimum (OSS: optimal μ supported on
     a finite union of arcs with explicit density; gradient descent on endpoints). — by
     numerical potential-theory solve.
  4. Certify the new m > 0.2487458 rigorously. — by a NEW certificate (see hard step).

**Hard step (single, gating):** *the certificate is no longer a pure 1-D min of a fixed
f.* The energy term couples μ to itself, so the dual inequality carries an extra
potential term λ₀·U_μ(z); one must certify the self-consistent triple (μ, Σ, λ₀), not
just min over the circle of a frozen auxiliary function. The R1 branch-and-bound
min-of-f harness does NOT cover this — it is genuinely new rigor machinery, and U_μ
itself is only known numerically from the descent. This is why it is NOT this round's
build: it is multi-stage and would crash an atomic builder.

**Why not this round (despite top upside):** violates the atomic-step constraint. It is
a 3–4 round program (formalize the constraint + adapt OSS density solve + build a NEW
self-consistent certificate the reviewer can reproduce). Sequence it AFTER Angle 1, and
when it is built, break it into atomic stages: (R_a) implement the OSS energy-augmented
LP and report the NON-rigorous m gain as a conjecture only; (R_b) build + verify the
self-consistent certificate. Mark Spec review REQUIRED when it is promoted — the dual
potential term and its certificate are the load-bearing novelty.

**Estimate / risk:** if the SSS payoff ratio transfers even partially, this is the only
angle that could move the lower bound by ~1e-3 (toward ~0.2497+), dwarfing any upper
nibble. RISK: the 82a integrand lives on the lemniscate contour w=e^{it}−e^{2it} (two
z-copies via z↔1−z), not an interval in R+, so the OSS closed-form density is not
verbatim and the certificate is the unsolved part. High upside, high rigor risk, not
atomic — hence ranked #2 for SEQUENCING, #1 for ultimate leverage.

================================================================================

## Angle 3 (FALLBACK if Angle 1's Qa is dry): evolve the upper family by SEARCH
### genetic / multistart over BOTH the discrete factor set AND q (Boyd-Mossinghoff)

**Moves:** UPPER bound, < 0.2543309112. Same harness as Angle 1, but instead of one
hand-picked Q_3, run a small global search over a candidate POOL of small-height integer
factors in X (the Boyd-Mossinghoff / Sac-Epee genetic-breeding analogue for small
limit points of Mahler measure), selecting the factor subset and q jointly.

**Hard step:** keeping condition (4)/Lemma 5 admissibility across the evolving subset
(Doche's "prod P_i | (Q_new − Q_old)" resultant heuristic keeps it clean), and the
search not being so wide it never converges. **Check:** identical to Angle 1 (extended
`certify_q.py`). **Atomic first step:** none cleaner than Angle 1's single-Qa test — this
is Angle 1 widened, so only escalate to it if a few hand-picked Q_3 candidates each fail
to drop the float. Lower priority because it is more setup for the same atomic payoff,
and the same q-search machinery already exists.

================================================================================

## RANKING and recommendation

**Build Angle 1 this round.** It is the only angle whose FIRST concrete step is small,
self-contained, and bankable under the atomic-step constraint: add ONE polynomial,
check admissibility (finite sympy), re-optimize q seeded to recover the held value,
report the float. It reuses the EXACT reviewer-verified `certify_q.py` harness with only
the inputs changed (lowest rigor/reproducibility risk of any angle — the back end is
already approved twice). It is the lever that produced every past upper-side jump, the
bound is automatic for any admissible q (zero optimality burden), and there is documented
structural headroom (~0.0016) below the current record. Even if Qa is orthogonal and the
float doesn't drop, the round bankably narrows the dictionary search and re-certifies.

**Angle 2 is the bigger prize but cannot be the build this round** — its certificate is
new, self-coupled potential-theory machinery that is inherently multi-stage and would
crash an atomic builder (R2–R4 over-reach history). It is the right NEXT major program:
sequence it after Angle 1, split into a conjecture-LP stage and a certificate stage, and
send it through outline-review when promoted.

**Angle 3** is Angle 1 widened into a search; fall back to it only if several hand-picked
Q_3 candidates each fail to move the float optimum.

Dead ends NOT re-ranked (already burned, per the explorer reports + run_state rules):
same-family q-tuning (R5/R6, dry); LP column-gen on Flammang's fixed/cheap dictionaries
(R1, no improving column); single-small-height-α as an upper bound (a spectrum point);
pure potential-theory reframing as a method (BMQS strong duality => no free gap).
