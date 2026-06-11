## 82a  (C_82a: essential minimum of the Zhang-Zagier height h_Z(alpha)=h(alpha)+h(1-alpha))

DEPTH exploration of the LOWER bound via the OSS log-energy / discriminant dual column (PATH B). The lower bound has NEVER moved this run; it is tied at the verified record 0.24874 [Flammang F18]. This report says concretely how Flammang's bound is built, exactly how the energy column enters, what it can realistically deliver, and a stage-atomic plan. It does NOT attempt the improvement.

- Current bounds: lower = 0.2487458 = log(1.282416) [F18, Flammang 2018; reviewer-verified R1, rigorous interval B&B in verify_vec.py], upper = 0.2540419719 [this repo R11].
- Softer target (this run's directive): the LOWER bound. Not because it is numerically softer (it is harder — the energy column self-couples), but because it is the higher-ceiling, more NOVEL, more publishable target: a lower-bound move would be the first since Flammang 2018 and the first transfer of the OSS energy method off the real line, whereas the upper side is exhausted marginal nibbling (R5->R11 total ~4e-4).

### 1. How Flammang's 0.2487458 lower bound is built (the dual-LP / auxiliary-function structure)

Flammang [F18] is Smyth's auxiliary-function method, which BMQS Thm D identifies as the DUAL LP `D(g)`. The pieces, in our variables:

- Variable: `w = z(1-z)`. The Zhang-Zagier Green function is `g(z) = log+|z| + log+|1-z|` (log+ = log max(1,.)).
- Auxiliary function (F18 eq 2.1):
  `f(z) = log max(1,|z|) + log max(1,|1-z|) - sum_{j=1..J} c_j log|Q_j(w)|`,
  with `c_j > 0` real and `Q_j in Z[w]` (J ~ 24 integer polynomials in w, Table 1, degrees up to 22).
- The rigor chain (digest flammang_F18_digest.md, verified R1):
  1. Sum over the d conjugates: `sum_i f(alpha_i) >= d * m`, where `m = inf f` over the relevant domain.
  2. `log M(alpha)M(1-alpha) >= d*m + sum_j c_j * log| prod_i Q_j(alpha_i(1-alpha_i)) |`.
  3. `prod_i Q_j(alpha_i(1-alpha_i)) = Res(P, Q_j(z(1-z)))` is a NONZERO INTEGER (det of an integer matrix) when P does not divide `Q_j(z(1-z))`; hence its `|.| >= 1`, so `log|.| >= 0` and every `c_j` term DROPS (uses `c_j >= 0`).
  4. Therefore `log zeta(alpha) = (1/d) log Z(alpha) >= m`, i.e. `C_82 >= m`.
- The minimum: f is harmonic off small disks around roots of the Q_j, so its min is on `|z|=1` or `|1-z|=1`; by z->1-z symmetry, reduce to `C = {|z|=1}`, i.e. `w(t) = e^{it} - e^{2it}`, `0 <= t <= pi`. So `m = inf_{t in [0,pi]} f(w(t))` — a 1-D min over the circle.
- The search (NOT the rigor): the `c_j` are the optimum of a semi-infinite LP `max m s.t. f(w(t)) >= m for all t, c_j >= 0`, discretized at control points. The Q_j are bred by weighted integer transfinite diameter + LLL on Re/Im of trial values at control points, "k from 5 to 32 successively."
- THE TRUNCATION THAT LIMITS IT: the dual LP uses ONLY the univariate columns `log|Q_j(w)| >= 0` (resultant integrality). It does not use any multivariate / energy constraint. Flammang stopped breeding at degree k <= 32. There is no duality gap (BMQS Thm D); the gap to ~0.2527 (Doche's conjectured next spectrum point) is a TRUNCATION gap — too few / too-low-degree columns. R1 column generation on her fixed dictionary found best reduced cost ~ -1e-7 (control-point noise): her dictionary is LP-optimal among cheap univariate columns. So "more univariate columns" is a dry, heavy, uncertain lever — the well Flammang already drained.

### 2. The OSS energy column: how it enters as a NEW independent dual column Flammang never used

OSS (Orloski-Sardari-Smith, arXiv:2401.03252) added to Smyth's SSS LP the multivariate integrality (Orloski-Talebizadeh [OT23]):
  `int...int log|Q(x1,...,xn)| dmu...dmu >= 0` for every `Q in Z[x1,...,xn]`.
The decisive instance is `Q(x1,x2) = x1 - x2`, the LOGARITHMIC ENERGY
  `I(mu) := int int log|x1 - x2| dmu(x1) dmu(x2) >= 0`.
Validity: `prod_{i<j}(alpha_i - alpha_j)^2 = disc(P)` is a nonzero integer, so `|disc| >= 1`, hence the conjugate measure has `I(mu) >= 0`. This is genuinely INDEPENDENT of the univariate columns `int log|Q(x)| dmu >= 0` (energy couples two copies of mu; no finite univariate column reproduces it).

For 82a this transfers VERBATIM at the validity level: the ZZ conjugates `alpha_i` are roots of an integer polynomial P, so `disc(P)` is a nonzero integer and `I(mu) >= 0` for the ZZ conjugate measure too. Flammang F18 does NOT use it (her dual has only univariate columns). So `I(mu) >= 0` is an UNUSED, independent dual column for 82a's lower bound. Adding it can only RAISE the LP optimum m past 0.24874 (more constraints on the primal mu => larger inf int g dmu => larger dual optimum).

HOW IT ENTERS THE DUAL (the self-coupling, made concrete). OSS handle the non-linearity (`I(mu)` is quadratic in mu) by using that `I(mu)` is CONCAVE (Ahlfors, OSS eq 6/Lemma 2.3), so `I(mu) >= 0` is equivalent to the family of LINEAR inequalities (OSS eq 8):
  `int (2 U_{mu_i}(x) - I(mu_i)) dmu >= 0` for every measure mu_i with `I(mu_i) >= 0`,
where `U_mu(x) = int log|x - z| dmu(z)` is the logarithmic potential. The dual then maximizes lambda s.t. (OSS eq 9, specialized to the active mu_i = mu_A at the optimum):
  `[objective integrand] >= lambda + sum_Q lambda_Q log|Q(x)| + lambda_0 (2 U_{mu_A}(x) - I(mu_A))`, lambda_Q, lambda_0 >= 0.
At the optimum `I(mu_A)=0`, so the extra term is `lambda_0 * 2 U_{mu_A}(x)`. THIS is the self-coupling: the dual auxiliary function now contains the potential `U_{mu_A}(x)` of the very measure mu_A that the primal produces. The certificate is no longer "min of a FIXED f" — it is a self-consistent fixed point `(mu_A, support Sigma, lambda_0, {lambda_Q})`.

THE 82a SPECIALIZATION (what is genuinely new vs OSS, and is the hard part):
  - OSS objective integrand is `x` (the trace), on `R+`. For 82a the objective integrand is the ZZ Green function `g(z) = log+|z| + log+|1-z|`, and the active domain is the CONTOUR `w(t) = e^{it} - e^{2it}, t in [0,pi]` (or equivalently a curve in the w-plane), NOT an interval in R+. So:
    * `mu` lives on a curve in C (the conjugate-distribution measure pushed to w), not on a finite union of real intervals.
    * The OSS density formula `|p(x)| sqrt(|H(x)|) / prod|Q(x)|` (which assumes mu on a union of real intervals with the objective = x) does NOT carry over verbatim. The endpoints-of-intervals parametrization is replaced by a parametrization of arcs of the contour.
    * The potential `U_mu(x)` must be evaluated for x on the same contour, against mu on that contour. The variable in which energy is most natural is z (where disc(P) lives), while Flammang's columns live in w = z(1-z); the energy `int log|z1 - z2| dmu dmu` is in z, the columns `log|Q_j(w)|` in w. One must keep both and the change of variables `w = z(1-z)` straight (a 2-to-1 map; z and 1-z give the same w — the z->1-z symmetry is exactly this).

CLEAN WAY TO HANDLE THE SELF-COUPLING (concrete options, in order of tractability):
  (a) ALTERNATING / FIXED-POINT solve (cleanest for stage-1 conjecture). Discretize mu on N nodes on the contour. Iterate: (i) given current mu^(k), form the LINEAR cut `int (2 U_{mu^(k)}(x) - I(mu^(k))) dmu >= 0` and add it as ONE extra column to the existing Flammang LP (`solve_lp` in stageB_colgen.py already builds `max m s.t. sum c_j log|Q_j| + m <= log+|w|`); (ii) re-solve the LP for `(m, c_j, lambda_0)` and recover the new primal dual measure mu^(k+1) (the LP marginals, already extracted in stageB_colgen.py); (iii) repeat until mu stabilizes. This is exactly OSS eq 8 used as a cutting-plane / column on the SELF measure. This is convex (concavity of I => the cut family is valid) so it converges to the true augmented-LP optimum; the value m at convergence is the stage-1 CONJECTURE. NB the potential `U_{mu^(k)}(x_n) = sum_p mu^(k)_p log|x_n - z_p|` is a dense NxN matrix-vector product — cheap (N ~ a few thousand).
  (b) CONVEX reformulation a la OSS Prop 2.1 (cleaner but heavier): solve the primal `min int g dmu s.t. int log|Q_j| dmu >= 0, I(mu) >= 0` directly as a convex QP in the node weights mu (objective linear, energy constraint is a concave quadratic `mu^T L mu >= 0` with L_{pq} = log|z_p - z_q|, a NEGATIVE-definite-ish kernel => the FEASIBLE set is convex). cvxpy with the constraint `mu^T L mu >= 0` written as a convex constraint (since I is concave, `I(mu) >= 0` is a convex constraint) gives mu_A and the duals lambda_0, lambda_Q directly. This avoids hand-rolling the fixed point.
  Either way, stage-1 output is a NUMERICAL CONJECTURE for m_energy; it is a bound ONLY after stage-2 rigor.

### 3. Realistic numerical ceiling — how much could the energy column raise 0.24874?

Quantitative analogy with SSS (the closest cousin, same machinery):
  - In SSS the energy column gave the biggest jump in 40 years, but the magnitude is modest in absolute terms: Wang-Wu-Wu 2021 (130 univariate polys) reached 1.7931; OSS WITH the energy column reached 1.80203 — a jump of ~0.0089, about +0.50% of the constant, achieved with only 4 polynomials. Crucially the energy column let 4 polys beat 130 — it captured what would otherwise need a huge univariate dictionary.
  - But note Siegel (1945) already used `Nr >= 1` AND `disc >= 1` (i.e. the energy at the crudest level) to get 1.7336 from Schur's 1.6487 — so a large part of the energy content is ALREADY implicitly in any good univariate-LP bound. OSS's gain is the INCREMENT of the exact energy constraint over a strong univariate LP, ~0.0089 on a constant of size ~1.8, i.e. relative ~+0.5%.

Transfer estimate for 82a (a BOUND on the plausible gain, not a promise):
  - Optimistic-but-honest scaling: a comparable RELATIVE gain (~+0.5%) on 0.2487458 would be ~ +0.0012, landing near ~0.2500 — which would close roughly 1/4 of the current gap (0.2487 -> 0.2540, width 0.0053) in one structural step. That would be a genuinely publishable first lower-bound move.
  - Pessimistic floor: the gain could be much smaller. Flammang's univariate dictionary is already very rich (24 polys to degree 22, vs SSS Wang-Wu-Wu's 130 lower-degree ones), so more of the energy content may already be captured implicitly than in the SSS comparison; and 82a's contour geometry is harder, so the OSS density structure may not realize its full strength. A realistic LOWER end is ~+1e-4 to +3e-4 (similar order to the Doche->Flammang univariate gain of 5e-4), which would still be a verified milestone but a small one.
  - HONEST CEILING: the lower bound cannot exceed the true constant, and the upper bound caps the room at ~0.2540 (current) / ~0.2527 (Doche's conjectured next spectrum point). So the most the energy column could ever buy on the lower side is ~0.0053 (to the current upper) — but realistically expect +1e-4 to +1.2e-3, with the SSS-analogy midpoint ~+5e-4 to +1e-3. ANY strict, certified raise above 0.2487458 is a first-of-run, novel result.
  - KEY UNCERTAINTY to resolve in stage-1 BEFORE building stage-2: run the augmented LP and see the actual `m_energy`. If `m_energy - 0.2487458 < ~1e-5` the column is not worth the heavy stage-2 certificate; pivot. If it is `> ~1e-4`, proceed.

### 4. Concrete multi-stage plan (atomic, so a builder does not crash)

The energy column self-couples mu, so this is genuinely multi-stage. Keep each stage one atomic builder task; do NOT hand the whole thing as one task (rounds 2/3/4/8 crashed on multi-stage builds; per-role NEVER rule).

STAGE 0 (outliner planning, with Bash — cheap, no milestone): set up the discretized objects. Nodes `z_n = e^{it_n}` on `t in [0,pi]`, `w_n = z_n(1-z_n)`, objective `g_n = log+|z_n| + log+|1-z_n|` (= log+|w_n| effectively on this contour, the Flammang integrand), the Flammang columns matrix `A[n,j] = log|Q_j(w_n)|` (reuse `logabsQ` from stageB_colgen.py), and the energy kernel `L[n,p] = log|z_n - z_p|` (the potential is in z, where disc lives — this is the load-bearing modeling choice). Sanity: confirm the existing univariate LP reproduces m* ~ 0.2487458 (stageB_colgen.py already does this).

STAGE 1 (one atomic builder task — produces a CONJECTURE, no milestone yet): build the AUGMENTED conjecture-LP = Flammang's LP + the energy constraint, via the alternating/fixed-point scheme (option (a) in section 2), OR the convex QP (option (b)). Output: candidate value `m_energy` and the self-consistent `(mu_A, lambda_0, {c_j})`. Deliverable is a script `energy_lp.py` + the conjectured `m_energy`. WHAT WOULD CRASH A BUILDER (keep these out of stage 1): do NOT also try to make it rigorous; do NOT try to derive the OSS closed-form density on the contour; do NOT try z->1-z folding cleverness — just discretize, solve, report. Hard step inside stage 1: getting the potential term sign/normalization right (`2 U_mu(x) - I(mu)`, with `I(mu)=0` at the optimum) and confirming the LP value strictly exceeds 0.2487458 on a FINE grid (still only a conjecture). Gate: if `m_energy - 0.2487458` does not clear ~1e-4 with margin, STOP and report — do not proceed to stage 2.

STAGE 2 (SEPARATE atomic builder task, only if stage-1 clears the gate — produces the milestone): turn the conjecture into a RIGOROUS reproducible certificate. The template is OSS Proposition 6.1 (its "Validity of Results" section), adapted to the contour:
  - Fix rational/float `(lambda_0, c_j)` and the support arcs from stage 1; the certified bound is `m_energy - (slack)`, where OSS take a deliberate small haircut `lambda - delta*lambda_0*log(R)` (their `log(18)`; for us R = max |x| on the contour). This haircut is what makes the self-coupled bound rigorous without certifying mu_A exactly.
  - The load-bearing rigorous step: certify `g(w(t)) >= m_certified + sum_j c_j log|Q_j(w(t))| + lambda_0 * 2 U_{mu_A}(w-arg)` for ALL t (not just grid), by the SAME interval branch-and-bound used in verify_vec.py — EXTENDED so the integrand carries the extra potential term `2 U_{mu_A}(.)` evaluated with outward rounding (a sum of `log|x - z_p|` over the fixed nodes z_p, each interval-enclosed). The resultant-integrality drop-out for the c_j terms is UNCHANGED (Flammang's argument, R1-verified); the energy term's validity is `I(mu) >= 0` from disc being a nonzero integer (state it with the same finite-exception clause).
  - WHAT WOULD CRASH A BUILDER (keep out of stage 2): do NOT re-solve the LP here; do NOT let mu_A be variable — it is FIXED from stage 1, the cert only checks the fixed dual auxiliary inequality holds everywhere with outward rounding. The cert is again "min over the contour of a FIXED function" — exactly the verify_vec.py shape, just with one extra (interval-enclosed) potential term. That keeps it atomic.

STAGE 3 (reviewer): reproduce the interval B&B with the added potential term, re-derive the energy-validity (disc integer) and the resultant drop-out independently, confirm `m_certified > 0.2487458` strictly. Milestone iff strict.

WHERE THE SINGLE HARDEST STEP IS: stage-2's rigorous enclosure of the potential term `U_{mu_A}` over the contour together with the haircut bookkeeping — because U_mu has logarithmic singularities where x approaches a node z_p (the same `log|x - z_p|` kink that already needs care in verify_vec.py near roots of Q_j). The verify_vec.py machinery already handles log-kinks of `log|Q_j(w)|` rigorously (per role-memory R4 notes on the cell_int_upper kink branch); the U_mu term is structurally identical (a sum of log-distance kinks) so the existing discipline extends — but it is the place a careless enclosure goes vacuous. Flag to the builder: mirror verify_vec.py's "only ever an UPPER bound on the subtracted term" discipline for the potential term.

### Where the slack is (summary)
- Flammang's dual uses ONLY univariate columns and only k<=32; the energy/discriminant constraint `I(mu)>=0` is an entirely UNUSED, independent, concave dual column. This is the one structural lever on the lower bound that is NOT the dry "breed more univariate polys" search. It is the direct analogue of the move that gave SSS its biggest jump in 40 years.

### Angles to try (concrete, ranked)
1. (TOP) The energy column via the alternating/cutting-plane scheme (stage-1 above) — add `int(2U_mu - I(mu))dmu >= 0` as a self-consistent cut to the existing Flammang LP. Cleanest path to a stage-1 conjecture; reuses stageB_colgen.py's `solve_lp` + dual extraction almost verbatim (just one extra column whose entries are `2 U_{mu^(k)}(w_n)`).
2. The convex-QP reformulation (cvxpy, option (b)) — solve the primal `min int g dmu s.t. univariate columns + I(mu)>=0` directly; gives mu_A and lambda_0 in one shot. Heavier dependency (cvxpy) but no hand-rolled fixed point. Good cross-check on angle 1.
3. The higher multivariate column `Q(x1,x2,x3,x4) = x1 - x2 - x3 + x4` (OSS name it as future work) — a second, even more independent energy-type column. Only after the simple `x1-x2` energy column is shown to help; otherwise premature.

### Dead ends (do NOT retry)
- Univariate column generation on Flammang's fixed 24-poly dictionary: R1 found best reduced cost ~ -1e-7 (control-point noise), LP moved ~2e-11. Drained (run_state Rules; per-role NEVER).
- Same-family q-tuning / any UPPER-bound Flammang-block nibble: explicitly de-scoped by the R11 user redirect (not publishable); not a lower-bound move at all.
- Pure potential-theory "reframing" as a standalone method: R7 verified it is the SAME two LPs (BMQS strong duality, no gap) — relabeling buys nothing. The energy column is DIFFERENT: it is a new CONSTRAINT, not a reframing.
- Handing the whole energy campaign as ONE builder task: the self-coupling makes it multi-stage; an atomic builder crashes (per-role NEVER, R8/R10). Split exactly as stages 1 and 2 above, each atomic.

### Digests saved this round
- /home/agentuser/repo/constants/82a/literature/R11_explore_lower_energy.md (this report, copied to the literature folder for future rounds).
- (existing, re-read this round and confirmed accurate: flammang_F18_digest.md, R7_explore_analogous.md, R7_explore_polya.md, bmqs_2026_digest.md; OSS source pdfs/sss_2401.03252.pdf — Theorem 1.1, eqs 6-9, Proposition 2.1, Proposition 6.1 read in full from the body.)
