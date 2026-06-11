# R3 explore — borrowed / orthogonal LOWER-bound techniques for C_82a (Zhang-Zagier ess. min)

Explorer, round 3. Target to beat: **C_82 >= 0.2487458 = log(1.282416)** [Flammang F18, reviewer-verified R1].
Brief: survey the LITERATURE and ANALOGOUS height constants for a genuinely DIFFERENT lower-bound
technique (not the Smyth/Doche/Flammang single-variable auxiliary-function LP). Does NOT attempt the
improvement. Honors all hard constraints (no OSS energy/discriminant column, no w-products, no
asymmetric-z columns, no k>32 / lobe LLL, no integer-locus reduction, no BMRL transfer).

---

## TRIAGE HEADLINE (read first) — the honest finding

**Across the ENTIRE relevant literature, every method that lower-bounds an arithmetic height/measure
constant (Schur-Siegel-Smyth trace, Mahler measure, the house / Schinzel-Zassenhaus, the Faltings
ess-min, AND the Zhang-Zagier ess-min) is the SAME explicit auxiliary-function / integer-transfinite-
diameter linear program — Smyth's method.** I verified this directly against the primary sources
(see §1-§4). There is exactly ONE published technique in this whole family that genuinely beats that
LP, and it is the OSS log-energy / multivariate-integrality column (arXiv:2401.03252) — which is
**barred** for ZZ (user's four-mechanism no-go, R1). No SDP/SOS lower bound has ever beaten the LP for
any of these constants. No one has improved Flammang's 0.24874 for ZZ since 2018.

So the literature offers **no ready-made orthogonal lower-bound machine to borrow.** The two
genuinely-different ideas the brief asked me to probe (a coupled 2-variable (z,1-z) auxiliary function;
an SOS/SDP positivity certificate) are analyzed below — and the coupled-variable idea **collapses for a
provable structural reason** (the leading-coefficient obstruction, §5, freshly verified), while the
SOS route is a *certificate-tightening* of the SAME LP, not a new bound source (§6). This is an
honest, load-bearing negative for the outliner: the softest realistic shot is NOT a borrowed technique
but the continuum-SOS tightening of Flammang's own dual, scoped as a high-ceiling longshot.

---

## §1. Recent ZZ-specific work (2018-2026): has anyone beaten Flammang's 0.24874? NO.

- **Flammang [F18]** "On the Zhang-Zagier measure" (Int. J. Number Theory 14 (2018), 2663-2671;
  HAL hal-03295880, PDF on disk). RE-READ THE BODY this round (not just the digest). Confirmed: the
  record lower bound zeta(alpha) >= 1.282416 => C_82 >= log(1.282416) = 0.2487458 is Smyth's
  single-variable auxiliary function (eq 2.1) `f(z)=log+|z|+log+|1-z| - sum_j c_j log|Q_j(z(1-z))|`,
  Q_j in Z[z] but ALWAYS evaluated at w=z(1-z), c_j>0, via weighted integer transfinite diameter +
  LLL, k=5..32. **NEW detail the prior digest missed: F18 also proves (Thm 3, Thm 4) two-sided bounds
  on Z(alpha) in terms of the LENGTH L(alpha) and the MAHLER MEASURE M(alpha) of totally-positive
  integers** — but these are auxiliary inequalities of the SAME LP type (different weight function),
  not a new ess-min lower-bound mechanism, and they are stated only for the totally-positive subproblem
  (Thm 2: zeta>=2.352316), which is a different, much larger constant. No lower-bound lever there.

- **Morales [arXiv:2201.11174]** "Essential Minimum in Families of lines" (2022; PDF on disk, body read
  this round). Applies the Burgos Gil-Philippon-Rivera-Letelier-Sombra refinement of Fekete-Szego.
  **It produces ONLY UPPER bounds and density intervals** (Thm A: image of h_Z dense in
  [0.31944909, inf); his lower bounds are the WEAKER classical Zagier/Doche, he does not even cite
  Flammang). NO new lower-bound machinery. CLOSED as a transfer.

- **BMQS [arXiv:2601.18978]** (2026; digested + re-checked). Conceptual: the two classical methods are
  LP-DUAL with strong duality (Thm D), ess(h_g) computable in principle (Thm E). Quotes the WEAKER
  0.248247 lower bound, gives NO number/finite-LP/table for ZZ. Their own words: "the obtained
  algorithm is far from being practical." Confirms the lower side IS a semi-infinite LP and the gap is
  a TRUNCATION gap, not a duality gap — but offers nothing harvestable. CLOSED as a bound source.

- **OSS [arXiv:2401.03252]** "New Lower Bounds for the Schur-Siegel-Smyth Trace Problem" (Math. Comp.
  Aug 2024; PDF on disk). The ONE genuine post-LP advance in this family: "adds new constraints to
  Smyth's LP" = the multivariate/energy integrality columns (the `x1-x2` log-energy = discriminant).
  This is precisely the **barred** family. CLOSED by user directive.

Conclusion §1: nothing in the 2018-2026 ZZ-specific literature moves the lower bound past Flammang or
supplies a non-LP lower-bound mechanism.

## §2. Lower-bound methods for ANALOGOUS height constants — all the SAME LP

I surveyed the lower-bound machinery for the registry's cousin constants and the broader
height/measure literature. Verified against primary sources:

- **Schur-Siegel-Smyth trace problem** (totally-positive alg. integers, smallest trace/degree): SOTA
  1.80203 is OSS 2024 = Smyth's LP + the energy column. Pre-OSS SOTA (Wang-Wu-Wu, ~1.7931, 130
  polynomials) is the pure auxiliary-function LP. (Confirmed from OSS abstract + body.)
- **Absolute trace / Ω-measure** (Flammang-Rhin, arXiv:2401.12951, 2024 — Rhin's R(alpha) question):
  explicit auxiliary functions + recursive polynomial search. Same LP. (Abstract verified.)
- **House / Schinzel-Zassenhaus** (Flammang, Rhin; Pritsker arXiv:2101.06710 "House symmetric about the
  unit circle"): "explicit auxiliary functions that depend on generalizations of the integer
  transfinite diameter," Chebyshev-type building blocks. Same LP family. (Search-confirmed.)
- **Mahler measure / Lehmer-type lower bounds** (Flammang-Rhin "Integer transfinite diameter and
  polynomials with small Mahler measure"): integer transfinite diameter again. Same LP.
- **Faltings ess-min** [BMRL, arXiv:1609.00071]: SAME Smyth real-section method; its only novelty is
  Koebe-distortion of the modular-curve hyperbolic Green function, irrelevant to ZZ's elementary
  Green function. ALREADY DIGESTED + CLOSED (R2). Do not re-attempt.

**Load-bearing triage fact:** the "Chebyshev-style / integer-transfinite-diameter / Amoroso-Habsieger /
resolvent-positivity" approaches the brief named as candidate borrows are NOT distinct from Flammang's
method — they ARE her method (F18 eq 2.1 is literally `tied to t_{Z,phi}` of the lemniscate contour,
F18 §2.2). The integer transfinite diameter IS the auxiliary-function LP in another language; "borrowing
it" buys nothing new. There is no published lower-bound technique for any of these constants that is
both (a) distinct from Smyth's LP and (b) not the barred energy column.

## §3. Is there an SOS/SDP lower bound that has BEATEN an LP for an analogous constant? NO.

I searched the SOS/SDP + arithmetic-height literature specifically. Finding: the SOS/Putinar/Parrilo
machinery is well-developed for polynomial optimization, and SOS is used to *rigorously validate* (via
rational rounding) auxiliary functions found computationally — but **there is no instance where an
SOS/moment-SDP lower bound beats the auxiliary-function LP for the trace problem, Mahler measure, the
house, or any ZZ-type constant.** The reason is structural (§6): the auxiliary-function LP is itself
already the tightest *linear* relaxation in the chosen dictionary; SOS over the same dictionary can at
most recover the continuum optimum the discretized LP approximates, and Flammang's LP is empirically
equioscillation-tight (24 active columns; per role-memory R2). SOS does NOT add new arithmetic content
(the energy/discriminant integrality) the way OSS's column does. So SOS is a *certificate form*, not a
new bound source — confirming the Angle-3 framing from R1/R2.

## §4. The COUPLED two-variable (z, 1-z) auxiliary function — does the w=z(1-z) collapse lose info?

This is the brief's deepest question and the only genuinely-novel structural idea. **Answer: the
w=z(1-z) reduction is NOT a free modeling choice that throws information away — it is FORCED by the
integrality (drop-out) step, and a genuine coupled (z,1-z) column is provably inadmissible for ZZ over
all algebraic numbers.** Freshly verified this round (§5). This both (i) explains WHY the asymmetric-z
screens collapsed (R1/R2) and (ii) shows the coupled formulation is not a new lever — it is the same
wall, derived from the other side.

## §5. The leading-coefficient obstruction (FRESH verification — the load-bearing structural fact)

Flammang's drop-out step (F18 §2.1) needs `prod_i Q_j(alpha_i(1-alpha_i))` to be a NONZERO INTEGER.
The resultant identity is `Res(P, Q(z(1-z))) = a^{deg_z Q(z(1-z))} * prod_i Q(alpha_i(1-alpha_i))`,
where `a` = leading coeff of the minimal polynomial P. So
`prod_i Q(alpha_i(1-alpha_i)) = Res(P, Q(z(1-z))) / a^{deg}` — the resultant is an integer, but the
quotient by `a^deg` is an integer ONLY when `a=1` (algebraic integer).

VERIFIED numerically this round (sympy, P=10z^2-6z+1, the standard non-integer ZZ input, a=10):
- `Res(P, z(1-z)) = 5`, `deg_z = 2`, so `prod_i (alpha_i(1-alpha_i)) = 5/100 = 1/20 = 0.05 < 1`
  => `log|.| = log(0.05) < 0`. **Flammang's "the c_j term drops out (>=0)" FAILS here.**
- Even the simplest column. A genuinely-coupled / asymmetric column is worse: for R(z)=z,
  `prod_i alpha_i = 1/a = 0.1 < 1`, `log < 0`.

CONSEQUENCES (load-bearing for the outliner):
1. **Flammang's Theorem 1 is correctly stated for algebraic INTEGERS only.** The bound C_82 >= 0.24874
   is legitimate as a bound on the ess-min over ALL algebraic numbers because the ess-min is REALIZED
   on integers: a non-integer alpha carries a `+2 log|a|/d` Weil penalty in h_Z (verified: P=10z^2-6z+1
   has h_Z = 2.30, vs ess-min ~0.249 — nowhere near). So the lower bound is valid; the integrality is
   what makes the auxiliary-function drop-out work, and it works *because* the near-minimal locus is a=1.
2. **A coupled (z,1-z) column that is NOT a function of w gives a `prod = Res / a^{deg}` that is < 1
   for non-integer alpha** => it does NOT drop out, it makes the bound WORSE. To use it you must FIRST
   exclude non-integers — and that is the **integer-locus reduction**, which is a HARD CONSTRAINT
   (barred): the `2 log a/d` penalty -> 0 as deg -> inf, so excluding non-integers is as-hard-as-the-
   problem (run_state, R2). **The w=z(1-z) form is exactly the symmetric subalgebra in which the
   `a^{deg}` factor is absorbed by the resultant being a perfect integer for ALL algebraic numbers** —
   that is the *whole point* of the reduction, not a loss of information.
3. This is the SAME wall the R1/R2 both-circle screens hit from the numerical side: asymmetric-z
   columns get LP weight ~0 and collapse on the second circle (~1e-8). The LP "knows" they don't drop
   out cleanly. The coupled-variable reformulation does not escape it — it re-derives it.

**Net on §4/§5: the coupled 2-variable auxiliary function is NOT new slack.** It is barred (it reduces
to the integer-locus reduction, a hard constraint) and structurally identical to the closed
asymmetric-z lever. Do NOT propose it.

## §6. The one remaining non-barred lever — continuum SOS/moment certificate of Flammang's OWN dual

This is the only candidate the screens did not touch and that is NOT on the barred list. It is NOT a
borrowed technique and NOT a new bound source — it is a tighter CERTIFICATE of the same LP:

- **Load-bearing step:** certify `g(w(t)) - sum_j c_j log|Q_j(w(t))| - m >= 0` for ALL t in [0,pi]
  (continuum, not discretized control points) as a trigonometric/rational positivity condition, via
  Fejer-Riesz / Putinar SOS, letting the SOLVER pick the c_j jointly with the SOS multipliers. The log
  terms are handled by affine minorants on each arc (introducing the Q_j as auxiliary variables).
- **Known to beat an LP for an analogous constant? NO** (§3). SOS adds no arithmetic content; it can
  only recover the continuum LP optimum the discretized LP approximates.
- **Feasibility for ZZ: LOW ceiling, real work.** Role-memory R2: Flammang's LP is equioscillation-
  tight (all 24 columns active, dense Chebyshev optimum across t in [0.49,2.83]), so C[w] is
  near-saturated to deg ~22 — even the real-coefficient continuum optimum is ~0.2487, so SOS likely
  recovers ~0.24874, NOT a beat. The affine-minorant slack on the log terms can swamp the +1e-4 gate.
  And a numerical SDP is a CONJECTURE — a rigorous rational/interval SOS is needed for a bound.
- **Verdict:** the highest-ceiling NON-barred shot, but a longshot; scope it as "tighten the
  discretized LP to the continuum and SEE if any slack remains," with the honest prior that the LP is
  already tight so the expected outcome is recovery (~0.24874), not a raise. If the outliner wants a
  build, gate it: numerically solve the continuum SOS FIRST and check the value clears 0.2487458 + 1e-4
  with margin BEFORE any rigorous-certificate compute. If it lands at ~0.24874, STOP (honest negative).

---

## SUMMARY for the outliner

- **No borrowable orthogonal lower-bound technique exists in the literature.** Every analogous-constant
  lower bound (trace, Mahler, house, Faltings, ZZ) is Smyth's auxiliary-function / integer-transfinite-
  diameter LP. The only genuine post-LP advance is the OSS energy column — BARRED. SOS/SDP has never
  beaten the LP for any of these.
- **The coupled 2-variable (z,1-z) auxiliary function is NOT new slack** — it is barred (reduces to the
  integer-locus reduction via the `a^{deg}` leading-coeff obstruction, freshly verified: P=10z^2-6z+1
  gives `prod = 1/20 < 1`, drop-out fails) and structurally identical to the closed asymmetric-z lever.
  The w=z(1-z) reduction is FORCED by integrality, not a loss of information. Do NOT propose it.
- **The only non-barred remaining lever** is the continuum SOS/moment certificate of Flammang's own
  single-variable dual (§6) — high ceiling in principle, but the LP is equioscillation-tight so the
  realistic outcome is recovery (~0.24874), not a raise. A longshot; gate it on a cheap numerical
  pre-solve before any rigorous build.
- **Honest bottom line:** the lower side of 82a is *very hard* — the cheap and medium in-method levers
  are all closed (R1/R2), the energy column is barred, and the literature has no orthogonal mechanism.
  The continuum-SOS longshot is the only non-barred shot, with a low expected payoff. If the outliner
  judges the lower side stalled, the verified-progress alternative is a clean reproducible NEGATIVE
  (continuum-SOS recovers but does not beat 0.24874), which is still a logged milestone — or a
  user-sanctioned pivot to the pushable UPPER side (held 0.2540419719, R11).

## Dead ends confirmed this round (do NOT retry)
- OSS log-energy / discriminant / multivariate-integrality column (any form): barred (user no-go).
- Coupled (z,1-z) / asymmetric-z / non-w columns: leading-coeff obstruction (`prod = Res/a^deg < 1`
  for non-integer alpha) => drop-out fails => reduces to the BARRED integer-locus reduction; also the
  both-circle gate kills them numerically (R1/R2, ~1e-8). Re-verified structurally this round.
- Integer transfinite diameter / Chebyshev / Amoroso-Habsieger "as a borrowed method": these ARE
  Flammang's method (F18 §2.2), not distinct.
- Morales Fekete-Szego (arXiv:2201.11174): upper/density only, no lower-bound mechanism. CLOSED.
- BMRL Faltings transfer: same Smyth method, modular-curve-specific. CLOSED (R2).
- w-products, k>32 / lobe LLL, integer-locus reduction: barred / closed (R1/R2).

## Digests saved this round
- /home/agentuser/repo/constants/82a/literature/R3_borrow_survey.md (copy of this report, for reuse).
- Updated reading: Flammang F18 body (Thms 2-4: length/Mahler/totally-positive auxiliary inequalities,
  same LP type — noted, not a lever); Morales 2201.11174 body (upper/density only); OSS abstract
  (confirms energy column = "new constraints to Smyth's LP", barred); Flammang-Rhin trace/house and
  Pritsker house-symmetric (all same auxiliary-function LP); fresh sympy verification of the
  `prod = Res/a^{deg} < 1` leading-coeff obstruction for the coupled-column inadmissibility.

## Sources (verified against primary text this round)
- Flammang [F18], hal-03295880 (PDF on disk) — Thm 1 (record), eq 2.1, §2.2 transfinite diameter,
  Thms 2-4. https://hal.science/hal-03295880v1/document
- Morales [arXiv:2201.11174] (PDF on disk) — Thm A upper/density, no Flammang lower bound.
  https://arxiv.org/pdf/2201.11174
- BMQS [arXiv:2601.18978] (PDF on disk) — strong duality, no ZZ number. https://arxiv.org/pdf/2601.18978
- OSS [arXiv:2401.03252] — energy column = "new constraints to Smyth's LP", barred for ZZ.
  https://arxiv.org/abs/2401.03252
- Flammang-Rhin [arXiv:2401.12951] — absolute-trace auxiliary functions, same LP.
  https://arxiv.org/abs/2401.12951
- Pritsker [arXiv:2101.06710] — house symmetric about unit circle, auxiliary functions / transfinite
  diameter. https://arxiv.org/pdf/2101.06710
- BMRL [arXiv:1609.00071] — Faltings ess-min, same Smyth method (CLOSED R2). https://arxiv.org/abs/1609.00071
