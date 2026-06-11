# R1 explore — non-energy lower-bound attack angles for C_82a (Zhang-Zagier ess. min)

Explorer: math-explorer, round 1 (the "Polya principles" relaunch). Task: survey, rank,
and report NON-OSS-energy lower-bound attack angles to raise C_82 past the genuine verified
record **Flammang [F18] 0.2487458 = log(1.282416)**. Does NOT attempt the improvement.

HARD CONSTRAINT honored: the OSS log-energy / discriminant-moment column is a PROVEN no-go
(run_state Goal Updates: four mechanisms, two structural proofs). NOTHING below uses an
energy/discriminant-moment angle. The disputed R12-R17 "held" values (0.25090..0.25240) ALL
rest on that single linearized self-cut and must be treated as suspect; the genuine verified
lower bar is 0.2487458.

---

## Triage: is this a good target? YES — tractable, not a famous-open-problem wall.

- This is a CONTINUOUS optimization constant with a reproducible certificate (Smyth
  auxiliary function + resultant-integrality), the AlphaEvolve-tractable kind. NOT
  integer/metamathematical, NOT an irrationality measure.
- It is NOT closed: verified lower 0.2487458 [F18], verified upper 0.2540419719 [this repo
  R11]; gap ~0.0053. BMQS Thm D (strong duality, re-confirmed from arXiv:2601.18978 this
  round) proves BOTH sides converge to the true C_82 — the gap is a TRUNCATION gap, not a
  duality gap, so neither side is blocked by a Millennium-class conjecture. Genuinely
  attackable.
- The lower side has NEVER moved by a legitimate method this run. Every lower "advance"
  (R12-R17) used the now-disqualified energy cut. So the lower bound is wide open for a
  genuinely different idea — exactly the brief.

## The decisive structural fact I re-confirmed this round (BMQS Theorem B / Thm 4.1)

BMQS prove the admissible-measure set is characterized EXACTLY by
  `int log|Q| dmu >= 0  for ALL Q in Z[x]`,  x = z the conjugate variable,
and that this is an iff (their Theorem B). Two consequences that drive the ranking below:

1. **The energy constraint `I(mu)>=0` is NOT an independent constraint** — BMQS state the
   potential characterization `U^mu<=0` is "not an independent constraint; it derives from
   the polynomial constraints." This is the structural reason the OSS self-cut on the
   |z|=1 circle (capacity 1) buys nothing rigorous, corroborating the user's no-go. Do not
   revisit it.

2. **Flammang uses ONLY columns `Q_j(w)` with `w = z(1-z)`** (verified directly:
   `certificate/flammang_table1.py` — all 24 entries are integer polynomials in w). But the
   BMQS/Smyth constraint family is over ALL `Q in Z[z]`, i.e. polynomials in the conjugate
   `z` itself. A polynomial in z that is NOT a pullback `Q(z(1-z))` of a w-polynomial is a
   GENUINELY INDEPENDENT, UNUSED, LINEAR dual column — and unlike the energy column it is an
   honest `int log|Q| dmu >= 0` column (resultant-integrality, the SAME rigor Flammang
   already has), with NO self-coupling, NO concavity subtlety, NO capacity trap. This is the
   single cleanest non-energy lever and the top of the ranked list.

---

## RANKED shortlist of non-energy lower-bound angles (most tractable first)

### ANGLE 1 (TOP) — Augment Flammang's LP with integer-polynomial columns in z (and in 1-z), not only in w = z(1-z).

WHAT IT IS. Flammang's auxiliary function is
  `f(z) = log+|z| + log+|1-z| - sum_j c_j log|Q_j(w)|`,  w=z(1-z),  Q_j in Z[w], c_j>=0.
Replace/extend the dictionary with the FULL Smyth class: add columns `-c log|R(z)|` and
`-c log|S(1-z)|` for integer polynomials R, S in Z[z] that are NOT functions of w alone.
Rigor is IDENTICAL to Flammang's existing chain: `prod_i R(alpha_i) = Res(P,R)` (resp.
`prod_i S(1-alpha_i) = ±Res(P,S(1-x))`) is a nonzero integer off a finite exception set, so
`log|.| >= 0` and the c-terms drop. So ANY such column is admissible with the same
finite-exception clause R1 already verified for the w-columns — no new validity machinery.

WHY IT IS UNUSED SLACK. The w = z(1-z) substitution is a 2-to-1 fold (z and 1-z share a w);
it FORCES every column to be symmetric under z->1-z. Flammang's whole dictionary therefore
lives in the z->1-z-symmetric subalgebra. Columns in z alone (e.g. cyclotomic Phi_n(z),
small-Mahler-measure factors, Lehmer-type polynomials, or LLL-bred integer polynomials in z
clustered near where f is smallest) reach OUTSIDE that subalgebra and can separate the two
local minima of f that the symmetric columns must treat together. The minimizer of f
near-equioscillates across t in [0.5,1.5] (R1 stage A); a z-asymmetric column can push down
on one lobe without the symmetric coupling. This is structurally the analogue of how OSS beat
a 130-polynomial univariate dictionary with 4 columns — but here the new columns are STILL
honest `int log|Q| dmu>=0` columns (just in a richer variable), so NONE of the energy no-go
applies.

HARD STEP (named). Finding integer polynomials R(z) (or S(1-z)) with strictly improving
reduced cost `int log|R(z)| dmu*` against the LP dual measure mu* AND that survive
re-optimization (earn c_R>0) AND that raise the certified min m past 0.2487458. The R1
column-generation NEGATIVE result was confined to the w-variable / cheap products — it never
priced z-only columns. So the search space is genuinely new. The reduced-cost pricing
machinery (`stageB_colgen.py`) extends verbatim: just evaluate `log|R(z_n)|` on the contour
instead of `log|Q(w_n)|`.

ROOM ESTIMATE. Moderate-to-good. The Doche-conjectured next spectrum point is
~log(1.2875274)=0.25272, so up to ~+0.004 of headroom exists in principle before the
suspected truth. A first z-column gain is more likely in the +1e-4..+1e-3 band (the
Doche->Flammang univariate gain was +5e-4 after a big search; a structurally new column class
could do comparably or better in one step). ANY strict certified raise is a first legitimate
lower-bound move of the run. CERTIFICATE IS THE EASY PART: the verify_vec.py interval
branch-and-bound transfers with ZERO new machinery — it already certifies `min_t f` for a sum
of `-c_j log|Q_j(w(t))|` terms; adding `-c log|R(z(t))|` terms is the same log-kink discipline
in the same code. No self-coupling, no potential term, no haircut. This is the cleanest
tractable door.

### ANGLE 2 (HIGH) — Push Flammang's own LLL / weighted-integer-transfinite-diameter breeding past k=32, mu*-guided.

WHAT IT IS. Flammang generated her Q_j by the weighted integer transfinite diameter: for each
degree k=5..32 she found an integer R minimizing `sup_t |Q(v)R(v)| exp(-(r+k)/(2t) log+|v|)`
via LLL on Re/Im of trial values at control points near the active minima, keeping factors
with c_j>0. She STOPPED at k=32 — a COMPUTE limit, not a theoretical one (digest
flammang_F18_digest.md). Extend to k=33..48, but SEED the LLL control points at the LP dual
measure mu*'s support (the binding band, active minimum t~0.577) instead of her hand-placed
"near least local minima" heuristic — BMQS explicitly name "the lack of an efficient criterion
to find the optimal direction" as the bottleneck, and pricing against mu* IS that criterion.

WHY IT IS SLACK. This is the lever EVERY past lower-side jump used (it is the record method's
own generator), and the only one Flammang demonstrably left unfinished (k>32). It stays
entirely in the resultant-integrality rigor — no energy, no new validity argument.

HARD STEP (named). The LLL breeding at k>32 is heavy and uncertain: the historical payoff of
"more/better w-columns" was small (~5e-4 for a large search), and R1 column-generation showed
the EXISTING dictionary is LP-optimal over cheap products — so a gain needs genuinely deep new
columns that only the LLL breeder produces, run at higher degree than anyone has. The risk is
returning a null (Flammang's set may be near-optimal in w up to high k). Certificate is again
the easy verify_vec.py extension.

ROOM ESTIMATE. Low-to-moderate (+1e-5..+5e-4), high variance. Best run as a COMPLEMENT to
Angle 1 (breed in z AND in w), not alone — the structurally new variable (Angle 1) is more
likely to pay than more depth in the same variable.

### ANGLE 3 (MEDIUM, highest ceiling, heaviest) — A genuine semi-infinite-LP / moment-SDP positivity certificate for the augmented dual, solved as one convex program.

WHAT IT IS. Cast the lower bound as the BMQS dual `D(g) = sup_{c>=0, columns} inf_z (g - sum
c_j log|Q_j|)` and solve it as a POSITIVITY certificate rather than a discretized LP at fixed
control points. Concretely: parametrize z = e^{it} on the contour, write `g(w(t)) - sum_j c_j
log|Q_j(w(t))| - m >= 0` as a trigonometric-polynomial / rational positivity condition, and
certify it by a sum-of-squares (SOS) / moment-SDP relaxation (Putinar/Fejer-Riesz on the
circle). The auxiliary function's transcendental pieces (log+, log|Q|) are handled by
introducing the polynomial factors as auxiliary variables and bounding the log terms by their
supporting affine minorants on each arc (a standard trick), turning the certificate into a
finite SDP whose feasibility PROVES `m`. This replaces the discretize-then-interval-B&B
pipeline with a single exact certificate and — crucially — lets the SOLVER choose the c_j
jointly with the positivity multipliers, which can find a better m than the
discretized-control-point LP that Flammang and R1 both used.

WHY IT IS SLACK. Flammang's c_j come from a DISCRETIZED semi-infinite LP (finitely many
control points); the true semi-infinite optimum can be strictly larger, and the control-point
discretization is exactly where R1's reduced costs hit the ~1e-7 "noise floor." A genuine SOS
certificate over the continuum removes that noise floor and may extract the last bit of the
existing dictionary's value, then guide which new column to add. This is the
positivity-certificate / Polya-style reformulation the brief asks for, done HONESTLY (no
energy term).

HARD STEP (named). Encoding the log+ and log|Q| terms in an SOS/moment framework without
losing tightness: the affine-minorant linearization of the logs introduces slack that can
swamp the +1e-4 gate; getting a TIGHT, rigorous SOS certificate of `g - sum c_j log|Q_j| >= m`
on the circle is real work (and cvxpy/SDP solvers give floating answers that themselves need
rational rounding + interval verification to be a proof). Higher novelty, higher ceiling,
heaviest build. Best AFTER Angle 1 has shown the augmented-dictionary LP value clears the gate
— then use SOS to certify it tightly.

ROOM ESTIMATE. Uncertain; the ceiling is the full truncation gap, but the realistic first
gain is whatever the continuum-LP extracts over the discretized one (could be small if
Flammang's discretization was already fine). Treat as the "make the certificate exact and
joint" layer on top of Angle 1, not a standalone bound source.

### ANGLE 4 (MEDIUM, transferable-technique) — Transfer the Faltings ess-min closing technique (BMRL) / the Smyth-trace explicit-resolvent style.

WHAT IT IS. The ledger flags the Faltings stable-height essential minimum as analogous, near
closed at -0.748629 <= mu_ess <= -0.748622 [BMRL, Burgos Gil-Menares-Rivera-Letelier, Math.
Comp. 2018]. BMRL closed that gap to 6 digits. Read BMRL in full (NOT on disk yet) to extract
WHICH technique did it: the Faltings ess-min is also a height-function ess-min in the BMQS
framework, so its near-closure is the closest worked example of driving BOTH bounds together
with a non-energy method. The transferable candidate is their explicit equilibrium-measure /
Green-function quadrature on the relevant curve (the Faltings Green function on the modular
curve) — an analytic construction, not an energy-moment LP.

HARD STEP (named). Establishing that the BMRL closing technique is genuinely a DIFFERENT
mechanism from Flammang's (and not just the same Smyth LP), and that its curve-specific
analytic input has a Zhang-Zagier analogue. This is a literature-read gating step before any
build — it may turn out BMRL is the same auxiliary-function machinery (then it transfers
nothing new), or it may expose a genuinely different convergent scheme.

ROOM ESTIMATE. Unknown until BMRL is digested; flagged because a method that closed an
analogous ess-min to 6 digits is exactly the kind of transferable lever the brief wants, and
it is the one analogous constant that was actually CLOSED. LOW confidence, but high value if it
pans out. Fetch + digest BMRL before committing a build.

### ANGLE 5 (LOW / context) — Richer auxiliary FORM: two-variable / non-product weight.

Smyth-type methods on sibling constants have gained from auxiliary terms beyond a single
`sum c_j log|Q_j(w)|` — e.g. a second transfinite-diameter weight, or a positive combination
of two weights. Flammang uses the single weight `phi = (max(1,|z|)max(1,|1-z|))^{-1}` in the
single variable w. A richer auxiliary form (a second weight, or columns in BOTH z and w
simultaneously — which subsumes Angle 1) is the most general non-energy generalization.
Lowest priority because it is the least concrete and Angle 1 already captures its most
promising special case (z-columns). Note only.

---

## Primal vs dual (the brief's explicit sub-question)

- The lower bound IS the DUAL (auxiliary function / the `c_j`). The PRIMAL is the conjugate
  measure mu (BMQS `P(g)`). For a LOWER bound, the dual is where the action is: constructing a
  better auxiliary function (more/richer columns) directly raises m. The primal's role is
  diagnostic — the LP dual measure mu* tells you WHICH new column to breed (reduced-cost
  pricing, Angles 1-2). There is NO separate "construct extremal small-height numbers" route
  to a LOWER bound: small-height numbers give UPPER-bound spectrum points, not lower bounds.
  So all lower-bound angles are dual-side; the primal mu* is the search compass, not a bound
  source.

## Levers in the Smyth/Flammang/Doche method that are NOT exhausted (brief sub-question 1)

1. **Variable of the columns** — only w=z(1-z) used; z and 1-z columns are unused (ANGLE 1).
   THE main unexhausted lever.
2. **Column degree** — Flammang stopped at k=32 (ANGLE 2).
3. **Search direction for breeding** — transfinite-diameter heuristic vs mu*-reduced-cost
   pricing (Angles 1-2; BMQS's named "missing criterion").
4. **Certificate form** — discretized control-point LP vs continuum SOS/moment certificate
   (ANGLE 3).
5. **Contour/weight choice** — single product weight vs richer (ANGLE 5; mostly subsumed by 1).
EXHAUSTED: same-dictionary q/c re-optimization (R1: LP moved ~2e-11), cheap w-product/
perturbation columns (R1: reduced cost ~1e-7 noise). Do not retry these.

## Dead ends — do NOT retry

- **OSS log-energy / discriminant-moment column / any I(mu)>=0 self-cut** — PROVEN no-go
  (user, run_state: four mechanisms, two structural proofs; corroborated this round by BMQS
  Thm B = the energy constraint is NOT independent of the log|Q| columns, and the |z|=1
  circle is capacity 1 so the cut is inert/zero after haircut). The disputed R12-R17 "held"
  values rest entirely on this and are suspect. Do not propose anything energy/moment-based.
- **Univariate column-generation on Flammang's FIXED 24-poly w-dictionary / cheap products /
  +-1 perturbations** (R1): best reduced cost ~-1e-7 (control-point noise), LP moved ~2e-11.
  Drained IN THE w-VARIABLE. (Angle 1's novelty is the z-variable, which was never priced.)
- **Same-family c_j / q re-optimization** (R1, R5-R6, R8): gains <1e-6. Dry.
- **Potential-theory "reframing" as a standalone method** (R7): BMQS strong duality => no gap
  to harvest; relabeling the same two LPs buys nothing. (Angle 3 is DIFFERENT: it is a tighter
  CERTIFICATE of the same dual, not a reframing for free value.)
- **Bounding C_82 by a single small-height alpha**: a spectrum POINT, not a lower bound. And
  small-height numbers bound the UPPER side, never the lower.
- **BMQS as a route to a number**: non-constructive, no finite LP, quotes a WEAKER lower
  (0.248247) than F18. Conceptual only (re-confirmed from arXiv:2601.18978 this round).
- **Handing a multi-stage self-coupled certificate as ONE builder task** (R8/R10 crashes) —
  N/A for Angles 1-2 (single-stage, no self-coupling); relevant only if Angle 3/4 is taken.

## Sources read / re-confirmed this round

- BMQS arXiv:2601.18978 (full HTML, re-fetched this round): D(g)/P(g) definitions, Theorem D
  strong duality, Theorem B (admissible-measure characterization = `int log|Q| dmu>=0` for ALL
  Q in Z[x], iff) — the load-bearing fact that (i) the energy constraint is NOT independent
  (corroborates the no-go) and (ii) z-variable columns are the unused independent lever.
- Flammang [F18] digest (flammang_F18_digest.md) + certificate/flammang_table1.py — confirmed
  ALL 24 columns are in w=z(1-z) only; the z-variable is unused.
- Prior explores R7 (polya/analogous/structure), R8 (triage), R11 (lower-energy/novelty) —
  re-read; their TOP recommendation (OSS energy) is now disqualified, but their structural
  dissection (Flammang seams 1-3, the resultant-integrality rigor chain, mu*-pricing machinery)
  is reused above and is sound.
- Disputed approach docs (oss-log-energy-lower.md, current.md R12-R17 log) — read to identify
  exactly what is disqualified (the single linearized self-cut at a frozen mu0) and to keep
  every angle above strictly clear of it.

## To fetch next round (not on disk; flagged for the outliner/builder)

- BMRL (Burgos Gil-Menares-Rivera-Letelier, "On the essential minimum of Faltings' height,"
  Math. Comp. 87 (2018)) — for ANGLE 4: the one analogous ess-min that was CLOSED to 6 digits;
  digest WHICH technique closed it before committing a build there.
