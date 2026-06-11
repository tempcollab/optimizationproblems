# R8 triage — 82a (Zhang-Zagier ess. min): PATH A (upper Q4 block) vs PATH B (lower OSS energy stage-1)

Explorer: math-explorer, round 8. Task: decide which ONE atomic step is the softer,
most-exploitable target for R8, under two hard constraints —
(1) user wants STRUCTURAL gains, not "enormous effort for a tiny improvement" (R7 margin
was only 1.236e-5); (2) the builder CRASHES on multi-stage tasks, so the step must be ONE
atomic, self-contained unit. Triage only — no improvement attempted.

Current verified bounds: lower 0.24874 [F18] (only REPRODUCED, R1, never beaten);
upper held 0.2543185491 [this repo R7]. Doche-conjectured smallest limit point
~log 1.2875274 = 0.25272, so ~0.0016 of certified headroom remains below the upper record.

---

## RECOMMENDATION (decisive): PATH A — add a SECOND free-exponent perturbing block (Qb).

The single atomic step: in the R7 family (base {P1,P2,P4,P6,P8} + fixed Q1*Q2 + free Q3=Qa,
exponent qB), add ONE MORE free-exponent block **Q4 = Qb** (the deg-24 sibling of Qa,
already transcribed in `approaches/upper-bound-optimization.md` lines 39-41), with its own
exponent qC, then re-optimize the 7 exponents and certify with the R7 harness pattern.

I ran the float probe this round (the decisive new evidence):

```
R7 6-exp float (Qa only)         = 0.2543184416   (held R7 certified 0.2543185491)
re-optimized 6-exp (q-tuning)    = 0.2543184380   <- q-tuning gain only 3.6e-9 (DEAD)
+ Qb as 2nd free block (7-exp)   = 0.2542655469   <- qB=0.110, qC=0.253
DROP from the 2nd block          = 5.29e-5        <- ~4x the R7 gain, >> 1e-7 cert slack
```

This settles the user's two worries at once:
- **The upper well is NOT drying up — the OPPOSITE.** The second block gives a 5.3e-5 float
  drop, ~4x larger than R7's first-block gain (1.236e-5) and ~14000x larger than the now-dead
  q-tuning lever (3.6e-9). The structural lever (more blocks) is ACCELERATING, not diminishing.
  The 2nd block helps MORE than the 1st because Qb is a genuinely independent small-ZZ-height
  factor, not a refinement of Qa.
- **It is a genuine STRUCTURAL gain, not parameter polish** — a new admissible perturbing
  factor enlarging Doche's dictionary, exactly the lever every historical upper jump used
  (Doc01a 1.2916674 -> Doc01b 1.289735 came from a richer dictionary). And it clears the
  "tiny improvement" bar comfortably (5.3e-5 vs the 1.2e-5 R7 the user already flagged as small).

Why this is the SOFTER target (vs PATH B):
- **Atomic and crash-safe.** It reuses `verify_upper_q3.py` verbatim as a template; the edit
  is the SAME edit R7 already shipped, applied once more: append Qb to the B-branch with weight
  qC, extend D's perturbing branch to `56 + qB*24 + qC*24`, re-run anchor/selftest/admissibility.
  One file, one integrand change, one certify run (~3-4 min). The reviewer already verified this
  exact harness in R7. No new math machinery, no self-coupling, no multi-stage sequencing.
- **Rigor is EASY and already approved.** An upper bound is valid for ANY admissible (q,qB,qC>=0)
  with NO optimality burden (Doc01a Lemma 2 + Lemmas 3,4,5). The max(A,B) outward-rounded
  quadrature is reviewer-verified machinery.
- **Bankable null.** If for some reason the certified value doesn't clear held by the float
  margin, the round still logged a verified admissibility + anchor + re-run (a milestone-grade
  reproduction), and we learn the block is exhausted — no wasted heavy compute.

### The single named hard step (PATH A)
**Admissibility of the enlarged dictionary W = Q1*Q2*Qa*Qb and the anchor recovery.**
Concretely the builder must verify, BEFORE trusting the optimum: (i) Doche Lemma 5 / condition
(4) for W=Q1*Q2*Qa*Qb — deg>0, W(0)=W(1)=1, each factor squarefree, and the FULL pairwise
gcd grid `gcd(Qb, P_i)=1` (all five P_i), `gcd(Qb,Q1)=gcd(Qb,Q2)=gcd(Qb,Qa)=1`; (ii) the
qC=0 ANCHOR must reproduce the held R7 float 0.2543184416 to >=10 digits (proves Qb is a genuine
free-exponent extension, not a broken-integrand artifact); (iii) re-run the mpmath selftest on
the CHANGED integrand (B now includes qC*log|Qb|) on both branches. This is the same gating
checklist R7 passed; the only NEW risk is if Qa and Qb share a common factor (they are distinct
deg-24 polys, so gcd(Qa,Qb) must be confirmed =1 — a 1-line sympy check). The float probe
already strongly suggests it clears (5.3e-5 drop), but admissibility, not the value, is the gate.

NOTE — a smaller-height Q4 might beat Qb: Qa,Qb have ZZ-height ~1.2905, ABOVE the limit point;
Doche conjectures the smallest limit point < 1.2875274. A smaller-height integer factor in
X=z(1-z) (deg ~28-32 from the Doche/Flammang small-height tables) could help even more, but
Qb is the SAFE, already-transcribed, sibling-of-Qa choice with a probed 5.3e-5 drop — recommend
Qb for R8 (one atomic step), defer the smaller-height search to a later round.

---

## PATH A assessment (asked: headroom + is a 2nd block / better Q3 non-trivial?)
- **Headroom:** held 0.2543185491 vs conjectured ~0.25272 => ~0.0016 of certified room. The
  well is far from dry. After this Qb step (float ~0.25427) there is still ~0.0015 left.
- **Is a 2nd free block non-trivial?** YES — probed 5.3e-5 float drop (see table above), the
  largest single-step structural gain on this constant so far. Strongly recommended.
- **Better Q3 candidate instead?** Re-optimizing the existing 6-exp family is dead (3.6e-9).
  A different/smaller-height FIRST block is plausible but unprobed; the 2nd-block route is the
  surest atomic win with the asset (Qb) already in hand.
- **Most promising concrete admissible block to try:** Q4 = Qb (deg 24, the sibling of Qa),
  because it is independent of Qa (distinct coefficients), already transcribed, of comparably
  small ZZ-height, and the probe shows it adds a real 5.3e-5 drop on top of Qa.

## PATH B assessment (asked: is OSS energy stage-1 ALONE one atomic builder task?)
PATH B = add the multivariate log-energy / discriminant dual column
`I(mu)=int int log|z1-z2| dmu dmu >= 0` (valid: disc(P) is a nonzero integer) to Flammang's
Smyth dual LP — the OSS arXiv:2401.03252 trick that gave the biggest SSS jump in 40 years, and
the only technique that could ever RAISE the never-beaten lower bound 0.24874.

- **What stage-1 would produce:** a candidate dual (lambda_0 on the energy column, c_j on the
  log|Q_j| columns, the binding measure mu*) and a NUMERICAL estimate of whether the augmented
  LP optimum exceeds 0.24874 — a CONJECTURE, not a certified bound.
- **Is stage-1 alone atomic / crash-safe? NO — it is NOT cleanly atomic, for two reasons:**
  1. **The energy term self-couples mu** (OSS Thm 1.1: the dual auxiliary inequality gains a
     potential term `lambda_0 * U_mu(z)` where `U_mu(z)=int log|z-w| dmu(w)`). So even the
     "conjecture-LP" is no longer a finite linear program in fixed columns — it is a self-
     consistent (mu, support Sigma, lambda_0) fixed-point that OSS solve by gradient descent on
     interval ENDPOINTS, with the optimal density `|p(x)|sqrt|H(x)|/prod|Q(x)|`. Setting this up
     for the 82a geometry (mu lives on the contour w=e^{it}-e^{2it}, NOT an interval in R+) is
     itself a multi-piece task: derive the contour analogue of the OSS density, discretize the
     self-coupled stationarity, and iterate. That is exactly the kind of multi-stage build that
     crashed the builder in R2-R4.
  2. **The 82a contour is not the OSS interval** — the OSS density formula is "not verbatim"
     (R7_explore_analogous flagged this). Adapting it is novel derivation, not a column add.
- **Potential gain:** large IN PRINCIPLE (first-ever lower-bound break; could move toward 0.252),
  but HIGH variance and the stage-1 deliverable is only a conjecture (no milestone-grade verified
  advance this round — the reviewer logs milestones for VERIFIED advances, and a conjecture-LP
  numeric is not one).
- **Verdict on PATH B:** the right BIG play eventually, but it does NOT decompose into a single
  crash-safe atomic builder task for R8. It needs an outliner to first split it (contour-density
  derivation | self-coupled LP solve | certificate) with an outline-review up front. Hand it to
  the builder as one task and it crashes. DEFER.

---

## RANKED RECOMMENDATION
1. **PATH A — add Q4=Qb as a second free-exponent block (DO THIS R8).** Atomic, crash-safe,
   reuses the R7-approved harness, probed 5.3e-5 float drop (4x R7, structural not polish,
   clears the "tiny improvement" bar), valid-for-any-admissible-q so rigor is easy. Hard step =
   admissibility of W=Q1*Q2*Qa*Qb + qC=0 anchor + selftest on the changed integrand.
2. **PATH B — OSS energy stage-1 (DEFER).** Highest ceiling (only lower-bound lever ever), but
   NOT atomic: the energy column self-couples mu (potential term) and the OSS density is for an
   interval not the 82a contour, so even "stage 1" is multi-piece. Will crash an atomic builder.
   Needs a dedicated outliner split + outline-review across several rounds; stage-1 output is only
   a conjecture (no verified milestone). Save for a planned multi-round campaign, not R8.

## The ONE atomic step for the outliner to plan around
Extend `verify_upper_q3.py` to a 7-exponent family by appending **Q4 = Qb** (deg-24 sibling of
Qa) as a second free-exponent perturbing block with exponent qC: B-branch
`+= qC*log|Qb|`, `D = max(sum q_i deg P_i, 56 + qB*24 + qC*24)`; re-optimize (q1..q5,qB,qC)
seeded at (R7 q, qB, qC=0); verify admissibility of W=Q1*Q2*Qa*Qb (Doche Lemma 5 + cond (4),
full gcd grid incl. gcd(Qa,Qb)=1), confirm the qC=0 anchor recovers the held R7 float to >=10
digits, re-run the mpmath selftest on the changed integrand, then run the outward-rounded
max(A,B) quadrature to certify the new upper bound. Target: strictly below held 0.2543185491
(float probe lands ~0.2542655).

## The named hard step
Admissibility / anchor gate of the enlarged dictionary W = Q1*Q2*Qa*Qb — specifically the full
pairwise-coprimality grid (including the NEW gcd(Qa,Qb)=1 check between the two free blocks),
W(0)=W(1)=1, each factor squarefree, plus the qC=0 anchor reproducing the held R7 float to >=10
digits. If admissibility holds (probe says the value clears), the certificate is the same
reviewer-verified R7 machinery.

## Dead ends (do not retry)
- Same-family q-tuning of the R7 6-exponent family: probed this round, gain 3.6e-9. DEAD.
- Same-family q-tuning of the R6 5-exponent family: R5->R6 gained 1.8e-6. DEAD (run_state rule).
- LP column-generation on Flammang's fixed 24-poly set / cheap dictionaries: R1, best reduced
  cost ~-1e-7 (noise). DEAD.
- Potential-theory "reframing" as a standalone method: BMQS strong duality => no gap to harvest
  (R7_explore_polya). It only relabels the same LP.
- Bounding C_82 by a single small-height alpha: a spectrum POINT, not a bound on the ess min.

## Digest saved this round
- This file: `constants/82a/literature/R8_explore_triage.md` (PATH A vs PATH B atomic-tractability
  triage; decisive float probe of the 2nd free block Qb -> 5.3e-5 drop; recommendation PATH A).
