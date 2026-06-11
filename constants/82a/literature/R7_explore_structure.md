# R7 DEPTH explore: proof-STRUCTURE dissection of both 82a record bounds

Goal of this round (per R6 user redirect): stop marginal q-tuning in Doche's single
limit-point family; dissect the PROOF STRUCTURE of both record bounds, find the
structural slack, name the softer target and the single most exploitable opening and
its gating hard step. Does NOT attempt the improvement.

Sources read in full this round: Doc01a (`doche_spectrum_doc01a.pdf`, 32k chars) —
the construction the upper bound rests on; Doc01b (`doche_perturbed_doc01b.pdf`) —
the record upper bound; Flammang F18 (`flammang_zz_hal.pdf`) — the record lower
bound; cross-checked against the three prior digests + R6 approach docs.

Current verified bounds: **lower 0.24874** [F18] (we only REPRODUCED it, R1) ·
**upper held 0.2543309112** [this repo R6] (was 0.25443677 = log 1.289735 [Doc01b]).
True ess min lies in (0.24875, 0.25433); Doche conjectures it is below
log 1.2875274 = 0.25272, i.e. the upper record is structurally ~0.0016 above the
suspected truth, the lower record ~0.004 below it.

---

## (a) UPPER bound — anatomy of Doche's limit-point construction (h = Q1*Q2, D=56)

### The machine (Doc01a §4, Lemma 2 + condition (4); Doc01b §2 instantiates it)
The whole upper bound is ONE explicit formula. Pick base polys P_1..P_k(X) and
perturbing polys Q_1..Q_{ℓ+1}(X) in X = z(1-z), integer coeffs, with deg Q_{ℓ+1}>0
and the non-triviality **condition (4)**:
  prod P_m^{n_m} / prod Q_m^{n_{k+m}}  ≠ ±1  for all exponent tuples.
Then for any q ∈ R_+^{k+ℓ} the value
  h(q) = exp( 2b·f(q) / D ),   D = 2b·max( Σ q_m deg P_m , deg Q_{ℓ+1} + Σ q_{k+m} deg Q_m )
is, by Lemma 2 (Mahler measure of the n-th "perturbation" via Riemann sums) PLUS
Lemmas 3,4,5 (turning the limit polynomial into an honest sequence of irreducible
integer polynomials), a genuine **limit point** of the ZZ spectrum V. So
**log h(q) is a valid upper bound on C_82 for ANY admissible q — no optimality
needed.** f(q) is a single integral over s ∈ [0,1] of a log+ of the family value
(the t-integral collapses by Jensen).

### WHY the record uses {P1,P2,P4,P6,P8} + Q = Q1·Q2, and what D=56 is
- The base-poly SELECTION {P1,P2,P4,P6,P8} (out of P1..P8) is, in Doche's own words,
  "forced by the search of the minimum of (9)" — i.e. it is the subset that the q-min
  picks out; the others get q_m → 0. NOT a deep structural choice.
- The PERTURBING choice Q1, Q2 is, Doche says verbatim, **"more arbitrary"**: he took
  them "according to their very small height and also because a product of P_i's
  divides Q1 − Q2" (the resultant heuristic — small ZZ measure correlates with small
  resultant Res(P, P_i) = ±1, and P ± Q1·∏P_i are then good candidates). He adds
  "we do not understand why it is so important."
- D = 56 is just the value of the normalizing degree at the record q for this fixed
  dictionary (it is NOT a tuned parameter; it is determined by which max-branch wins
  and the polynomial degrees). It is NOT a cap — it is an output.

### What CAPS the construction (the real structural ceiling)
1. **One perturbing block, hand-chosen.** The record uses a SINGLE perturbing factor
   Q1·Q2 (ℓ effectively small). Doche's framework explicitly allows ℓ+1 perturbing
   polynomials Q_1..Q_{ℓ+1} with their OWN exponents q_{k+1..k+ℓ}. He never exploited
   ℓ>1 with multiple INDEPENDENT small-height perturbers — the record is the ℓ→single-
   block corner of his own family.
2. **Manual q-search.** Doche minimized h(q) "by successive attempts" / "many
   attempts" — a hand search, not a solver. We already drained the continuous optimum
   of HIS fixed dictionary (R5→R6: float optimum ≈ 0.2543308, certified 0.2543309112;
   further q-tuning < 1e-6). That well is dry **for this dictionary**, confirmed.
3. **Dictionary depth, not q, is the lever.** The gain Doc01a→Doc01b (1.2916674 →
   1.289735, ~2e-3 in measure) came ENTIRELY from a richer dictionary (moving to the
   X-variable so "we can increase the number of perturbing factors", and adding
   P6,P8,Q2), NOT from finer q. This is the decisive structural fact: **every past
   jump on the upper side came from enriching the admissible polynomial dictionary,
   never from optimizing q in a fixed one.** We have only ever done the latter.

### Is the construction near a genuine extremal? — NO, it leaves a lot on the table.
- Doche himself: smallest KNOWN single height 1.2875274 (= 0.25272) is already BELOW
  the record limit point 1.289735 (= 0.25444→our 0.25433). He conjectures the smallest
  limit point is < 1.2875274. So there is **~0.0016 of certified headroom below our
  current upper record** before even reaching the suspected truth — the construction is
  structurally loose, not extremal.
- The conjecture machinery (Doc01a §5): the spectrum's early points D1,D2,D3,D4 of the
  RELATED measure M(α)M(1/(1-α))M(1-1/α) obey a clean recursive nesting
  (D2 = D1^3 - X^2, D3 = D2^2 - X^2 D1^3, ...). "No such connections were found for
  H(α)" — i.e. the SECOND nontrivial ZZ limit point is genuinely unknown and likely
  comes from a deeper/new small-height polynomial NOT in Doche's six. This is exactly
  the "richer dictionary" slack, said in the author's own voice.

---

## (b) LOWER bound — anatomy of Flammang's auxiliary function (F18)

### The machine (F18 §2; Smyth method)
  f(z) = log max(1,|z|) + log max(1,|1-z|) − Σ_{j=1..J} c_j log|Q_j(w)|,  w = z(1-z),
  c_j > 0 real, Q_j ∈ Z[w]. Summing over conjugates + the **resultant-integrality**
  step (∏_i Q_j(α_i(1-α_i)) = Res(P, Q_j(z(1-z))) is a nonzero integer ≥ 1 in abs
  value when P ∤ Q_j(z(1-z)), so log|·| ≥ 0 and the c_j terms drop) gives
  log ζ(α) = (1/d) log Z(α) ≥ m := min_{0≤t≤π} f(v), v = e^{it} - e^{2it}.
  Record: m = log 1.282416 = 0.2487458 (finite-exception set: roots of
  (z²-z)(z²-z+1)·Φ10(z)·Φ10(1-z)). We reproduced this rigorously in R1.

### Where the slack is — three structural seams
1. **Dictionary depth k ≤ 32 (the real seam).** The c_j come from a semi-infinite LP
   at a FIXED set {Q_j}; re-solving the LP only moves the last digits (R1 column-gen
   confirmed: best reduced cost ≈ -1e-7 = control-point noise, LP optimum moved ~2e-11).
   The slack is entirely in WHICH Q_j are present. Flammang GENERATES new Q_j by one
   recipe only: weighted integer-transfinite-diameter LLL — for each k she finds an
   integer R(z)=Σ a_l z^l minimizing sup_t |Q(v)R(v)|·exp(-(r+k)/(2t)·log max(1,|v|))
   via LLL on Re/Im linear forms at control points v_n near the active minima, keeps
   factors R_j that earn c_j>0, and **"takes k from 5 to 32 successively."** She
   stopped at k=32 (a COMPUTE limit, not a theoretical one). Higher k = deeper integer
   polynomials = a genuinely larger dictionary she never reached.
2. **Control-point / measure-support choice.** The LLL targets control points "near
   the least local minima of f" — a heuristic placement. The DUAL of the LP is exactly
   BMQS's primal: a probability measure μ* on the binding control points (R1 extracted
   it; support ~25 points across the flat band, active minimum t ≈ 0.577). A column
   generated by pricing against the ACTUAL μ* (reduced cost ∫ log|Q| dμ*) is a sharper
   direction than Flammang's transfinite-diameter heuristic — a criterion BMQS
   explicitly note is "missing." R1 tried this within cheap dictionaries (products,
   perturbations, deg≤4) and found nothing; the UNTRIED part is pricing the *LLL-bred
   deep-k* candidates against μ*.
3. **Single weight ϕ, single variable w.** Flammang uses the one weight
   ϕ = (max(1,|z|)max(1,|1-z|))^{-1} and works in w = z(1-z). Smyth-style methods on
   sibling constants (Schur-Siegel-Smyth trace, totally-real measure) have gained from
   richer auxiliary terms (e.g. adding log|R(z)| terms with R in a SECOND variable, or
   a positive combination of two transfinite-diameter weights). Flammang did not try a
   second polynomial variable or a non-product weight here.

### What Flammang did NOT try that a from-scratch auxiliary function could
- **Push k beyond 32** with the same LLL recipe (pure compute extension — the most
  direct, lowest-novelty lever; R1 already named it as the bottleneck).
- **μ*-guided column generation seeding the LLL** (use the LP dual to choose WHERE to
  breed, instead of the transfinite-diameter heuristic) — combines seam 1 and 2.
- **A second auxiliary variable / extra weighted term** (richer f than the single
  Σ c_j log|Q_j(w)|) — highest novelty, least certain.

---

## VERDICT: softer structural target, single most exploitable opening, gating step

### Softer target: the UPPER bound. (Same conclusion as R2, now structurally justified.)
Reasons grounded in the proof structure, not just the numeric gap:
- **The upper bound is valid for ANY admissible q — zero optimality burden.** A new
  admissible dictionary + ONE feasible q with a certified-from-above integral < 0.25433
  is a record. No LP optimum, no min-over-circle certificate of optimality is needed.
- **The rigor harness already exists and is reviewer-verified** (`verify_upper.py`
  max(A,B) outward-rounded quadrature; `certify_q.py` driver). A richer dictionary
  changes only the (P_m, Q_i) inputs and the admissibility check (Doche condition (4)
  / Lemma 5, which is q-INDEPENDENT) — the certificate code transfers directly.
- **Every historical upper-side jump came from a richer dictionary**, and Doche's own
  text flags the perturbing-factor choice as "arbitrary" with ~0.0016 certified
  headroom below our record before the suspected truth. The structural slack is real
  and named by the author.
- The LOWER bound's only real seam (k>32 LLL breeding) is a heavy, uncertain
  compute search whose historical payoff was tiny (Doc01a→F18 lower moved only ~5e-4
  after a big search) and whose rigor harness (min-over-circle interval B&B) is the
  HARDER one to drive to a strict break. It is the secondary target.

### Single most exploitable opening:
**Enrich the perturbing dictionary in Doche's limit-point family — add one or more
NEW small-height integer perturbing factors Q_3 (and/or a second independent
perturbing block, exploiting ℓ>1) in the variable X = z(1-z), keeping condition (4) /
Lemma 5, then re-optimize q over the LARGER family and certify with the existing
`verify_upper.py` harness.** This is the lever that produced every past upper jump,
the harness is in hand, and the bound is automatic for any admissible q.

Concretely the new factor(s) should be small-ZZ-height integer polynomials in X whose
ROOTS cluster the z-images to make log+|z|+log+|1-z| small (e.g. the degree-28..32
small-height polynomials Doche/Flammang already tabulate, or LLL-bred ones), chosen so
that a product of the P_i divides Q_new − Q_old (Doche's resultant heuristic) to keep
condition (4) clean.

### The hard step that GATES it (single, named):
**Producing a NEW admissible perturbing factor Q_new whose addition actually LOWERS
the continuous optimum of h(q) below the current 0.2543309112, while keeping
condition (4) / Doche Lemma 5 (deg>0, Q(0)=Q(1)=1, gcd(P_i,Q)=1) intact.**
- Mechanism it works: adding an admissible factor with its own exponent strictly
  enlarges the family, so min h(q) can only go DOWN or stay equal; the question is
  whether a reachable small-height Q_new makes it strictly down past the thin margin.
- Why it might fail / the risk: the margin to beat is now small (~1e-4 below Doc01b,
  and the float family optimum is nearly tight against the certified value), so a
  WEAK new factor buys nothing; the new factor must be genuinely small-height and
  resultant-compatible. The breeding of such a factor (small ZZ height in X, deg
  ~28-48, condition-(4)-compatible) is the heavy, uncertain part — it is the upper-side
  analogue of the lower-side k>32 LLL search, but with a far easier rigor/certification
  back end.
- Tractability note for the outliner: the FIRST atomic step is cheap and bankable —
  TRANSCRIBE/recover the exact Q1, Q2 (the perturbing factors of Doc01b's record
  family; Doc01b shows them as formula IMAGES that pdfminer dropped, but Doc01a gives
  Qα, Qβ explicitly, lines 1246-1256 of /tmp/doc01a_full.txt, already in
  `upper-bound-optimization.md`), then test adding ONE candidate Q_3 from the known
  small-height list and re-optimize. Keep the builder task to a SINGLE new factor per
  round (R5 over-reach rule).

---

## Dead ends already burned (do NOT retry)
- **Same-family q-tuning** (R5→R6): the continuous optimum of the FIXED {P1,P2,P4,P6,P8,
  Q1·Q2} dictionary is essentially reached (float ≈0.2543308, certified 0.2543309112,
  gains <1e-6). Dry. NEVER spend a round here again (run_state rule).
- **Bounding C_82 by a single small-height α** (e.g. the 1.2875274 polynomial): a
  single height is a spectrum POINT, not a bound on the essential minimum. Useless.
- **LP column-generation on Flammang's FIXED 24-poly set / cheap dictionaries** (R1):
  best reduced cost ≈ -1e-7 (control-point noise), LP optimum moved ~2e-11. The
  reachable dictionary (products, ±1 perturbations, deg≤4) contains no improving
  integer column. Only DEEP-k LLL-bred columns could help, and that is the heavy
  uncertain lower-side search — secondary at best.
- **BMQS (arXiv:2601.18978)** as a route to a number: pure duality/computability,
  quotes a WEAKER lower (0.248247) than F18's 0.24874, explicitly "far from practical,"
  no finite recipe. Conceptual only; no bound to harvest.

## Digests saved this round
- This file: `constants/82a/literature/R7_explore_structure.md` (proof-structure
  dissection of both bounds; upper = softer target with named opening + gating step).
- Full extracted texts cached at /tmp (doc01a_full.txt, doc01b_full.txt, flam_full.txt)
  — re-derivable from the PDFs in `literature/pdfs/` via pdfminer if needed.
