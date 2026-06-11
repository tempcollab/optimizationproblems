# R7 DEPTH explore — the POTENTIAL-THEORY / Polya reframing of C_82 (Zhang-Zagier ess. min)

Explorer: math-explorer, round 7. Angle assigned by user: "Polya methods" / potential
theory / Arakelov framing. Question to answer concretely: can a potential-theoretic
reframing BEAT a record (upper 0.2543309112 held, lower 0.24874 held), or is it only
conceptual?

Verdict up front: **The potential-theory reframing is REAL and already fully formalized
in the literature (BMQS 2026) — but it is NOT a fresh source of slack. It is a RELABELING
of the exact same two LPs we are already running, and the key theorem (strong duality,
no gap) says the auxiliary-function value and the equilibrium-measure value converge to
the SAME number with NO structural slack between them. So the potential-theory framing
does not, by itself, expose a quantity the discrete LP misses. The slack that exists is
entirely in WHICH integer polynomials / WHICH measure you feed the (same) LP — i.e. the
search problem, not the framing. Conclusion: conceptual clarification, NOT a new lever
for a record break. Spend the build elsewhere (see "What this DOES tell us").**

---

## 1. The reframing IS already precise — and it is the BMQS paper

The user's three sub-questions are all answered, rigorously, by BMQS (arXiv:2601.18978,
"Closing the gap around the essential minimum of height functions with linear
programming", Burgos Gil–Menares–Qu–Sombra, March 2026). Re-read in full this round.
The digest at `literature/bmqs_2026_digest.md` had the LP-duality skeleton; this round I
confirmed the explicit potential-theory content:

- **Smyth/Flammang auxiliary-function method = the DUAL LP `D(g)`** (BMQS §1.3, §5):
  `D(g) = sup_{k, a_i>=0, P_i in Z[x]\{0}} inf_{z in C} ( g(z) - sum_i a_i log|P_i(z)| )`.
  Here `g` is the Zhang-Zagier Green function `g(z) = log+|z| + log+|1-z|`. This is
  EXACTLY Flammang's `f(z)` (our lower bound; `c_j = a_i`, `Q_j = P_i`). Confirmed:
  the inequality `h_g(alpha) >= inf_z (g - sum a_i log|P_i|)` is BMQS eq (1.3), "at the
  basis of Smyth's method [Smy81]." So our lower-bound machinery is verbatim the dual LP.

- **The equilibrium-measure / potential side = the PRIMAL LP `P(g)`** (BMQS §1.4–1.5, §6):
  `P(g) = inf { int g dmu : mu in P^Z_log(C) }`, where `P^Z_log(C)` is the set of
  conjugation-invariant probability measures mu with **`int log|Q| dmu >= 0` for all
  `Q in Z[x]\{0}`** (BMQS eq (1.4), the Smith–Orloski–Sardari characterization,
  [Smi24],[OS24]). This is the potential-theory object the user asked for:
  - The constraint `int log|Q| dmu >= 0 for all integer Q` is precisely the statement
    that mu is approximable by Galois orbits of algebraic integers (Fekete–Szegő–Rumely
    + Smith–Orloski–Sardari).
  - BMQS Theorem C: a measure mu lies in `P^Z_log(C)` whenever its **potential**
    `U^mu(z) = int log(1/|z-w|) dmu(w) <= 0` everywhere; such mu are exactly log-weak
    limits of **equilibrium measures of capacity-one compact sets** (`cap(K)=1`). The
    energy functional `I(mu) = int U^mu dmu` and the equilibrium measure `mu_K`
    (minimizer of energy on `P(K)`) are spelled out (BMQS §2, around char 22900).
  - So **Doche's upper bound = picking a specific admissible measure mu** (the limit
    distribution of the Galois conjugates of his perturbed-polynomial family) and
    evaluating `int g dmu`. The "limit point of the spectrum" h(q) we certify IS
    `exp(int g dmu_q)` for the family's equidistribution measure mu_q. This is the
    Arakelov / equidistribution framing the user named (Bilu equidistribution; the
    measure is the conjugate-distribution measure on the lemniscate/contour).

- **Strong duality, THE decisive fact** (BMQS Theorem D / Thm 6.5):
  `D(g) = ess(h_g) = P(g)`. The lower LP and the upper LP have **NO duality gap** and
  both equal the true essential minimum. (BMQS also derive Theorem A: the ess min is
  attained by a generic decreasing sequence of algebraic integers.)

So all three of the user's sub-questions resolve to: *yes, the potential-theory /
equilibrium-measure / Arakelov reframing exists and is exact — it is BMQS's primal
measure-LP, and it is dual to the auxiliary-function LP with strong duality.*

## 2. Why this does NOT expose slack the discrete LP misses (the crucial negative)

This is the heart of the user's question, and the answer is structural:

(a) **Strong duality = no gap to exploit.** If there were slack BETWEEN the
    auxiliary-function value and the equilibrium-measure value at the optimum, that gap
    would be a free improvement. Theorem D says the gap is ZERO. The two framings give
    the SAME optimum. Reframing the lower-bound LP as a potential problem cannot produce
    a number larger than the LP's own value, because they are the two sides of one
    duality with no gap. The potential-theory dual is not a *sharper* bound; it is the
    *same* bound seen from the measure side.

(b) **The slack is in the search, and BMQS say so explicitly.** Both our finite bounds
    (Flammang 0.24874 lower, Doche/our 0.2543309 upper) are FINITE truncations: a finite
    set of integer polynomials (lower) / one explicit family-measure (upper). The gap
    between them (0.2487 vs 0.2543, width ~0.0056) is the truncation gap, not a duality
    gap. BMQS §1.7 state plainly: *"no practical algorithm is known to approximate them
    up to any arbitrary precision ... after a few iterations the methods reach a point
    where it is unclear how to continue, due to the enormous size of the search space and
    the lack of an efficient criterion to find the optimal direction"* and *"the obtained
    algorithm is far from being practical."* The potential-theory framing gives the
    OPTIMALITY CERTIFICATE structure (which measure is dual-optimal) but does NOT give
    the missing efficient search direction. It reorganizes the problem; it does not solve
    the bottleneck.

(c) **R1 column-generation already exploited the one operational consequence.** The
    sharpest practical use of the duality is: extract the dual measure mu* of the
    lower-bound LP and price candidate integer polynomials Q by reduced cost
    `r(Q) = int log|Q| dmu*` — a negative value means an improving column. That IS the
    potential-theoretic "find the optimal direction." R1's `stageB_colgen.py` did exactly
    this (see `approaches/lp-column-generation.md`): recovered mu* (support ~25 control
    points), priced thousands of integer polynomials, found best reduced cost ~ -1e-7
    (control-point noise), LP moved ~2e-11. **The potential-theory dual was already
    used, and it found no improving column within reach.** This is the operational
    cash-value of the whole reframing for the lower bound, and it is a NEGATIVE result.

## 3. The "Polya method" specifically — what it is and why it doesn't help here

"Polya's method" in this circle of problems = the integer-transfinite-diameter /
obstruction-polynomial technique (Polya's inequality `t_Z(K) <= t(K) = cap(K)` and its
refinements, used for the integer Chebyshev problem on [0,1] and for the
Schur–Siegel–Smyth trace problem). Checked against the literature (Borwein–Erdélyi–
Pritsker integer Chebyshev; Aguirre–Peral; Flammang's own trace-problem papers):

- The **weighted integer transfinite diameter** `t_{Z,phi}(C)` with weight
  `phi = (max(1,|z|) max(1,|1-z|))^{-1}` is the EXACT tool Flammang already uses to
  BREED her polynomials (digest `flammang_F18_digest.md` §"How polynomials are found":
  for each degree k she minimizes `sup_t |Q(v)R(v)| exp(...)` via LLL on Re/Im of trial
  values, k = 5..32). So Polya/transfinite-diameter IS the record method's generator,
  not an unused alternative. There is no orthogonal Polya contour-integral trick sitting
  unused — the record bound is already a transfinite-diameter construction.

- A Polya-type **contour-integral / resultant-positivity** argument (Hadamard
  three-circles, Jensen, resultant >= 1) is likewise already the rigor backbone:
  the load-bearing "the c_j terms drop because `Res(P, Q_j(z(1-z)))` is a nonzero integer
  hence `>= 1`" step (Flammang digest §"Key chain" 1–4) IS the resultant-positivity /
  product-formula argument. It is not a missed angle; it is the existing proof.

- The integer Chebyshev / Schur–Siegel–Smyth analogy (the constants sharing this
  machinery) tells us the SAME story: those bounds advance only by breeding better
  obstruction polynomials at higher degree via LLL, in tiny increments, with the same
  "no efficient search direction" wall. They offer no transplantable structural shortcut
  that Flammang/Doche didn't already import.

## 4. Can it BEAT a record? Concrete assessment

- **LOWER bound (0.24874):** NO, not via the reframing per se. The potential-theoretic
  dual is what column-generation already used (R1), and it found nothing. A real lower-
  bound gain still requires breeding NEW integer polynomials Q at degree k > 32 via
  Flammang's LLL/transfinite-diameter recipe (the compute-heavy search she stopped at) —
  this is a SEARCH task, and the potential-theory framing only tells you to score
  candidates by `int log|Q| dmu*` (which we already do). Tractable but heavy, uncertain,
  and the framing adds no leverage beyond the pricing rule already in `stageB_colgen.py`.

- **UPPER bound (0.2543309112 held):** NO new lever from potential theory directly. The
  upper bound is already `int g dmu` for an explicit admissible measure (Doche family).
  The potential-theory framing says: ANY conjugation-invariant mu with `int log|Q| dmu>=0`
  for all integer Q gives `C_82 <= int g dmu`. Two things follow, but neither is a clean
  win:
  - BMQS Theorem C gives an EASY admissibility test (`U^mu(z) <= 0` everywhere) and even
    examples of NON-compactly-supported admissible measures (Fubini–Study `mu_FS` with
    `U^{mu_FS}= -1/2 log(1+|z|^2) <= 0`). One could in principle search over a richer
    measure class than Doche's perturbed-polynomial family — e.g. equilibrium measures
    `mu_K` of capacity-one lemniscates `{|P|^{deg Q+1} = |Q|^{deg P}}` (the `mu_{P,Q}` of
    BMQS Thm 4.5, dense in `P^Z_log`). But computing `int g dmu_{P,Q}` for these is the
    SAME kind of contour integral we already certify, and there is no a-priori reason a
    generic lemniscate measure beats Doche's hand-optimized family. It widens the search
    space without pointing at a better point — exactly BMQS's "enormous search space, no
    efficient direction" wall.
  - **CAUTION (do not over-claim):** an admissible mu only gives an upper bound if it is
    genuinely in `P^Z_log` (the `int log|Q| dmu >= 0` constraint for ALL integer Q). The
    `U^mu <= 0` sufficient condition (Theorem C) is clean, but verifying it for a proposed
    new measure is itself a global potential-positivity check that needs rigor — and the
    Doche family already passes admissibility (Lemma 5) cheaply. So the reframing trades
    a known-admissible family for an unknown-admissible one with no value guarantee.

## 5. What this DOES tell us (steer for the outliner)

The reframing is not a build target, but it sharpens the triage:

1. **The lower–upper GAP (0.24874 ... 0.25433, width ~0.0056) is a TRUNCATION gap, not a
   duality gap.** Both sides provably converge to the same `C_82` (BMQS Thm D). So both
   sides are genuinely attackable in principle — neither is blocked by a famous open
   problem. This constant is a legitimate, tractable target (not RH-class). Good.

2. **The honest softer target remains the UPPER bound via the SAME Doche family or a
   richer admissible measure** — but R5/R6 already squeezed the same-family q-tuning to
   exhaustion (R6 gained only 1.8e-6; run_state RULE: "well is dry"). The real upper-side
   slack is in ENLARGING the dictionary {P_m, Q_i} (new small-height integer factors in
   X = z(1-z)), NOT in re-framing. That is a construction/search task. The potential-
   theory framing's only contribution there is the admissibility characterization (a
   convenience, not a lever).

3. **For the LOWER bound, the only real path remains Flammang-style LLL breeding at
   k>32** — and the potential-theory dual gives the (already-implemented) pricing rule
   to score bred candidates. So a lower-bound round = "run the heavy LLL breeder, price
   by `int log|Q| dmu*`, re-solve LP, re-certify." Heavy, uncertain, but structurally
   the only door, and the framing at least tells the builder exactly how to score.

4. **Do NOT spend a build on a "potential-theory reformulation" as if it were a new
   method.** It is the existing method in different clothes; strong duality forecloses a
   free gain. The user's instinct to consider it was worth verifying — and the verified
   answer is "already done, no gap." Bank that and move the build to a concrete
   construction/search angle.

## 6. Sources verified this round
- BMQS arXiv:2601.18978 — re-read §1.1–1.7 (intro), §1.3 (Smyth lower = dual LP),
  §1.4–1.5 (Smith–Orloski–Sardari char. (1.4), potential, Theorem C equilibrium measures),
  §2 (energy / equilibrium-measure definitions), §5–6 (strong duality Theorem D). PDF
  `literature/pdfs/bmqs2601.18978.pdf`, extracted via pdfminer (99231 chars). Confirms the
  potential-theory primal-LP and the no-gap strong duality.
- Flammang [F18] digest (`flammang_F18_digest.md`) — confirms the lower bound's generator
  IS the weighted integer transfinite diameter (= Polya method), k=5..32, LLL.
- Doche [Doc01b] digest (`doche_doc01b_digest.md`) — confirms the upper bound IS an
  equidistribution-measure integral `int g dmu_q` (the Arakelov/equidistribution framing).
- Web cross-check: integer-Chebyshev / transfinite-diameter literature (Borwein–Pritsker,
  Aguirre–Peral) and Arakelov equilibrium-measure literature confirm the machinery and the
  "obstruction polynomial / LLL" search wall are the same across the analogous constants.

## 7. One-line idea (noted, NOT attempted, per role)
IF a lower-bound round is run: breed integer polynomials Q in w=z(1-z) at degree 33–48
via Flammang's weighted-transfinite-diameter LLL near the active equioscillation band
(t in [0.5,1.5]), score by reduced cost `int log|Q| dmu*` against the R1 dual measure,
add improving columns, re-solve the LP, re-certify the new min by branch-and-bound. This
is the ONLY structural door the potential-theory analysis leaves open, and it is a search,
not a reframing.
