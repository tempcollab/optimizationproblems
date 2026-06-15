# R1 generative-explore — lifting the 82a first-variation theory from diagnostic to generative

Explorer: math-explorer, this run (2026-06-15). Task: NOT a bound-improvement round.
The user wants the first-variation paper (`constants/82a/upper_bound_paper.tex`) lifted
from a SCREENING test (`r_Q < log h` scores a given block) to a PREDICTIVE/GENERATIVE
principle that tells you WHICH block to build — ideally one from which the Grinsztajn
near-cancellation family R0,R2 is *derived* rather than diagnosed (paper Prop. 6 is
explicitly "explanatory, not generative", l.647).

"Number to beat" here = the diagnostic-only status quo. The deliverable is a
reviewer-verifiable theorem/principle with generative content, with a re-runnable check.

All probe scripts written to `constants/82a/certificate/scratch/probe{1..4}_R0R2.py`
(self-contained, numpy+sympy, ~1–4 min each). Numbers below reproduce the paper's
Table 2 (`firstvar_07_record_blocks.py`).

---

## 0. Triage — is the generative ask reachable, or is the honest result a sharper characterization?

**This constant's UPPER side is publication-complete for NUMERIC gains** (held
0.2538893183 frozen since R4; both Doche branches are reviewer-verified maximal firing
sets, R7/R8; record 0.2536331090 is Grinsztajn's, not ours). The R12–R28 triage docs
correctly declare numeric UPPER work DRY. **That is not this task.** This task is about
the THEORY paper, and the generative question has NOT been answered — Prop. 6 explicitly
concedes the criterion does not generate R0,R2.

Honest up-front verdict: **a fully generative principle that DERIVES R0,R2 from the
criterion alone is NOT reachable** (and the user's candidate framing (c) is dead — see
§2c). BUT a **genuine, reviewer-verifiable structural theorem is reachable**: a precise
characterization of the near-cancellation construction as a *coprime-sibling generator*
for the distinguished block, with the bridge engineered by an explicit magnitude
condition on Ω. This is a real contribution (it explains WHY the heuristic works and
turns it into a stated construction recipe), distinct from the paper's after-the-fact
diagnosis. Distinguish provable (the magnitude/degree/coprimality structure, all
re-runnable) from heuristic (that the recipe is *optimal* among generators).

---

## 1. The Grinsztajn near-cancellation mechanism — digested and probed

Source: Gri26 is **not an arXiv paper** — it is the GitHub repo
`github.com/maaxgrin/zhang-zagier-c82-bound` (commit cb88f92), certifying
`mu^ess(h_Z) <= 0.2536331090204145`. Its README gives the construction but **NO
derivation** of R0,R2: it calls them "perturbative factors", and the search is a
**finite-family heuristic** — 2048 squarefree denominators over {Q1,Q2 required;
optional R0,R2,P1..P9}, deg(Q)<=220, ranked, explicitly "not a proof of global
optimality." So R0,R2 were *posited by hand* and then validated by LP; the WHY is
exactly the gap this task targets. (Digest saved separately to `Gri26_digest.md`.)

The construction (paper eq. (R0R2), Appendix):
```
  R0 = primitive_part(Q1 - bridge*P8),   R2 = primitive_part(Q2 + bridge*P7),
  bridge = P1^5 * P2^5 * P4   (deg 5+5+4 = 14;  bridge*P8 deg 26;  bridge*P7 deg 26)
```
Q1,Q2 are the two deg-28 factors of Doche's distinguished block; P7=Q5 (deg 12), P9=Q6
(deg 16) are Flammang entries.

### WHY R0 fires — the mechanism, made precise (probes 1–4, reproduced)

The naive reading in the user prompt — "R0 is the best integer approximation that makes
|R0| small on Ω" — is **WRONG**, and the probes refute it cleanly. The true mechanism:

**(M1) R0 is a coprime SIBLING of Q1, not a small-on-Ω polynomial.**
- `mean log|R0| = 7.107` vs `mean log|Q1| = 7.092` on the full contour — R0 is *the same
  size* as Q1 (its Mahler measure is essentially Q1's), NOT small.
- `r_Q(R0) cand-free = -0.0688` ≈ `r_Q(Q1) = -0.0702` (probe 1; matches paper Table 2
  exactly). R0 fires because it inherits Q1's firing strength, NOT because |R0| is small.
- gcd(R0,Q1) = 0 (coprime), R0 irreducible, squarefree, R0(0)=R0(1)=1 — a fully
  admissible NEW perturbing block (probe 3). So R0 is a *fresh, independent copy* of the
  best block, usable alongside Q1 in the denominator (deg(Q) goes 56 → 56+28+28+... ).

**(M2) R0 inherits Q1's root-cloud / well structure on Ω.** Probe 2: R0's 6 roots
nearest the active locus sit 0.0039–0.0076 from it (Q1's: 0.0019–0.0022); both put
14 of 28 roots inside the lemniscate. R0 hugs the active locus almost as tightly as Q1.

**(M3) The bridge is ENGINEERED to be negligible on the bulk of Ω but comparable in
Q1's deep wells — that is the whole trick.** Probe 3:
- On Ω (97% measure): `mean log|Q1| = 7.296`, `mean log|bridge*P8| = 4.139` — so
  `|Q1| / |bridge*P8| ~ exp(3.16) ~ 23x`. R0 = Q1 − bridge*P8 ≈ Q1 on the bulk → it
  copies Q1's firing.
- In the deepest 2% wells of |Q1| (where |Q1| is tiny): `mean log|Q1| = -13.86`,
  `mean log|bridge*P8| = -12.84` — ratio `|bridge*P8|/|Q1| ~ 3.65 > 1`. Here the bridge
  *dominates* and moves the roots, so R0's wells land at slightly different points than
  Q1's → R0 becomes **coprime** to Q1 while staying locus-hugging.

So the bridge `P1^5 P2^5 P4` is a *root-displacement device*: small enough on the active
bulk to leave Q1's firing intact, large enough in Q1's deepest wells to perturb those
roots into a new, coprime, admissible polynomial.

**(M4) The exponent 5 and the degree-28 preservation are forced.** Probe 4: among
siblings `Q1 − P1^a P2^a P4 · tail`, a∈{3,4,5} all keep deg = 28 (bridge*P8 deg 26 < 28,
so R0 keeps Q1's top two coefficients and degree exactly) and give near-identical r_Q;
a=6 jumps the degree to 27 and r_Q worsens (well above). So **a=5 is the largest bridge
exponent that preserves deg 28** (= deg Q1), i.e. the strongest admissible displacement
that still copies Q1's leading behaviour. R2 is the same construction on Q2 with a sign
flip and tail P7 (chosen so R2 is coprime to R0: different tail → different deep-well
perturbation).

**One-line generative reading (the kernel of the result):** *R0 is the degree-preserving,
coprime sibling of the distinguished block Q1 obtained by subtracting an integer
"bridge" that is exponentially small on the active bulk of Ω yet comparable in Q1's deep
wells; the criterion fires on R0 because it inherits Q1's reduced cost while being a
genuinely new admissible block.* This is constructive: given Q1, the bridge family
`{P1^a P2^a P4 · P_tail}` with a maximal subject to deg-preservation GENERATES siblings.

---

## 2. Where the first-variation theory CAN be lifted — three framings ranked

### (a) [TOP PICK] r_Q-minimization as block DESIGN, via the coprime-sibling generator
**Rank 1 — the only framing with reachable rigorous content this run.**

The provable statement is NOT "r_Q minimization has a closed-form minimizer" (it does
not — that is the WITD primal, which R7 proved is a hard sparse integer problem). The
provable statement is the **generator structure §1 (M1–M4)**: 
> *Theorem (sibling generator).* Let Q* be a perturbing block firing on family F (r_{Q*}
> < log h). Let `g ∈ Z[X]` ("bridge") satisfy (i) deg g < deg Q*, (ii) `|g(χ(s))| <
> |Q*(χ(s))|` on a full-measure subset of Ω (so `R := Q* ∓ g` is r_R ≈ r_{Q*} firing),
> and (iii) gcd(R, Q*) = 1, R squarefree, R(0)=R(1)=1. Then R is an admissible firing
> block coprime to Q*, adjoinable as an independent denominator factor. The Grinsztajn
> R0,R2 are the instance Q*=Q1,Q2, g = P1^5 P2^5 P4 · P{8,7}.

**Hard step (load-bearing):** proving `r_R = r_{Q*} + O(small)` from condition (ii)
rigorously — i.e. that `∫_Ω log|Q* ∓ g| ≈ ∫_Ω log|Q*|` when |g|<|Q*| on Ω. This is a
`log|1 ∓ g/Q*|` expansion controlled by `|g/Q*|` on Ω; the deep-well region (where
|g|>|Q*|) must be shown to contribute O(measure × bounded) since R is contour-root-free
(min|R∘χ| > 0, audited 1e-2-class). This is a clean, re-runnable analytic lemma — the
reviewer re-derives the `log|1∓g/Q*|` bound and checks the deep-well measure numerically.

**Is r_Q minimization a closest-vector / Diophantine problem with explicit structure?**
PARTIALLY. The *generator* (sibling construction) is explicit and constructive. The
*global* r_Q-minimization over all Z[X] is NOT — R7 already proved (73,845 originals →
0 firing; cheapest coprime original factor w²−w+1 has r̃=+0.013 > best firing margin
−0.005) that it is a sparse, knife-edge integer lattice problem with NO closed-form
minimizer. So the honest claim is: **the sibling generator is a constructive SUBROUTINE
that produces firing blocks from an existing firing block; it is not a solution to the
unconstrained r_Q-min.** That is exactly the generative content the paper lacks, and it
is reachable.

### (b) Second-variation / "steepest block" reading
**Rank 2 — interesting but the hard step is likely not one-round-rigorous.**
Among degree-d admissible blocks, which coefficient-space direction most decreases
log h? The first variation is linear (`r̃_Q`), so "steepest" = most-negative r̃_Q, which
is just framing (a) again. A genuine second-variation reading would explain the
saturation/knife-edge (R7's "single ±1 flip swings r̃ by +0.06") via the Hessian of
log|Q| in coefficient space restricted to Ω — but this is the conditional-capacity
residual already computed in R6 (`screen_conditional_capacity.py`), and turning it into
a *generative* rule (not just a ranking) is the open WITD-residual problem. **Hard step:**
showing the Hessian/residual SELECTS the sibling construction — not obviously true and
not obviously one-round. Use only as a corollary if (a) leaves room.

### (c) [DEAD] Potential-theoretic / equilibrium generative rule
**Rank 3 — REFUTED. Do not resurrect.** The paper's Remark "Not a transfinite-diameter
problem" (l.709) and R7 both kill this: the equilibrium measure of Ω has constant
potential ≈0.524 on its support, well above log h=0.254, so Ω's measure is NOT the
equilibrium measure and log h is NOT its Robin constant. R7 proved the load-bearing
direction FAILS: firing integer roots sit strictly inside the unit disk (|ζ|∈[0.43,0.79])
and cannot reach the deepest U^ν wells; the integer inf sits strictly ABOVE the
continuous −log d_∞. **The "roots track the deep wells of the potential" rule is false
for the INTEGER problem.** The sibling generator (a) is the corrected reading: R0's roots
do NOT chase new deep wells — they COPY Q1's roots (which are themselves not at the
equilibrium wells). Any builder who reopens the equilibrium/WITD equality is repeating a
proven-dead angle.

---

## 3. Which framing yields a RIGOROUS, reviewer-verifiable theorem in one round

**Framing (a), the sibling-generator theorem.** It is the only one with (i) a stated
construction (not just a screen), (ii) a re-runnable check (probes 1–4 already
reproduce every number; the new lemma's deep-well-measure bound is a numpy integral),
and (iii) a re-derivable load-bearing step (the `log|1∓g/Q*|` expansion on Ω). The
reviewer can independently: reconstruct R0,R2 from Q1,Q2 and the bridge; confirm
r_R ≈ r_{Q*}; confirm the |g|<|Q*|-on-Ω vs comparable-in-wells magnitude split (probe 3);
confirm coprimality/admissibility (sympy, probe 3); and re-derive the analytic bound.

**Scope honesty for the builder (mandatory):** the theorem is a GENERATOR (produces a
firing block from a given one), NOT a global solver of r_Q-min and NOT a derivation of
R0,R2 "from the criterion with no input." The input is Q1 (the distinguished block) plus
the bridge ansatz; the theorem proves the construction yields an admissible firing
sibling and EXPLAINS the magnitude-engineering (M3) and degree-preservation (M4) that the
Grinsztajn heuristic stumbled onto. Stated that way it is a real, defensible contribution
that closes the "explanatory, not generative" gap — partway: from "diagnoses R0,R2" to
"derives the family R0,R2 belong to, given the distinguished block."

---

## 4. Honest assessment — what is provable vs heuristic

**Provable (reachable this run, all re-runnable):**
- R0,R2 are admissible firing blocks coprime to Q1,Q2 (sympy — done, probe 3).
- The magnitude split (M3): |bridge·P8| ≪ |Q1| on the active bulk, comparable in the
  deep wells (numpy integrals — done, probe 3).
- Degree preservation (M4): a=5 is the maximal bridge exponent keeping deg 28; siblings
  with a≤5 inherit r_Q(Q1) (probe 4).
- The sibling-generator lemma `r_R = r_{Q*} + (deep-well correction)`, given a clean
  `log|1∓g/Q*|` analytic bound (the one new derivation the builder must write).

**Heuristic only (label as such, do NOT certify):**
- That the bridge `P1^5 P2^5 P4` is *optimal* among generators (Gri26's own search is a
  finite-family heuristic; no global optimality).
- That the generator produces the BEST firing siblings (it produces admissible ones;
  ranking them is the WITD residual, open).
- Any claim that the criterion alone, with no Q1 input, predicts R0,R2 (false — it needs
  the distinguished block as seed).

**The honest deliverable** is exactly the user's fallback: *"firing blocks of the record
family are the degree-preserving coprime siblings of the distinguished block, generated
by a bridge that is exponentially small on the active bulk of Ω."* This is a sharpened,
structural, GENERATIVE characterization (a stated construction recipe), strictly stronger
than the paper's current after-the-fact diagnosis, and it is reviewer-verifiable. It will
not beat the Grinsztajn record numerically (and need not — the task is theory).

---

## Dead ends — do NOT retry (with why)
- **Equilibrium/transfinite-diameter generative rule (framing c):** REFUTED by paper
  Remark l.709 + R7 (integer roots strictly inside disk, can't reach U^ν wells; integer
  inf strictly above −log d_∞). Roots do NOT track potential wells in the integer problem.
- **"R0 is small on Ω" reading:** WRONG — R0 is the same size as Q1 (mean log|R0|=7.11);
  it fires by inheriting Q1's reduced cost, not by being small (probes 1,3).
- **Global r_Q-minimization as the generative principle:** R7 proved it is a sparse
  knife-edge integer lattice problem, maximal firing set within reach, no closed form.
  The generator (a) is a SUBROUTINE, not a solver — do not over-claim it solves r_Q-min.
- **A non-Doche mu_{P,Q} upper construction (BMQS density):** R1/R12–R28 DRY (strong
  duality pins the optimum to the saturated Doche cone). Not a generative lever.
- **Numeric UPPER break:** both branches saturated (R7/R8); float gate fails at 2.94e-6.
  The task is theory, not a break — do not chase one.

## Digests saved
- `constants/82a/literature/Gri26_digest.md` — the Grinsztajn record: source (GitHub repo,
  not arXiv), construction (R0R2 + 2048-denominator finite-family heuristic search),
  values, and the explicit statement that R0,R2 have no published derivation.
- `constants/82a/literature/R1-generative-explore.md` — this report.
- Probe scripts: `certificate/scratch/probe{1,2,3,4}_R0R2.py` (reproduce §1 numbers).
