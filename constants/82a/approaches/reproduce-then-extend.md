# Approach: reproduce Flammang's certificate, then extend the polynomial set

Status: STAGE A DONE (round 1) — rigorous certificate built, awaiting reviewer.
        STAGE B attempted, NO record break (negative result, recorded below).
Moves: LOWER bound. Stage A target = re-certify 0.24874 (milestone). Stage B target = push m past 0.24874 (record break).

## RESULT (round 1, proof-builder)
STAGE A — DONE. Built a self-contained, re-runnable RIGOROUS certificate that
  min_{t in [0,pi]} g(t) >= 0.24874, hence C_82 >= 0.24874 (registry record),
for all algebraic integers outside the finite exception set E (roots of the
Q_j(z(1-z))). The bound is established by interval branch-and-bound (NOT a grid
min): 184,444 cells, max depth 9, ~30s, worst certified cell 0.2487400.
- Full Flammang Table 1 transcribed: 24 integer polynomials (degrees up to 22),
  NOT the 14 in the old doc — re-extracted j=15..24 from the PDF; loader ASSERTS
  every Q_j in Z[w]. The full set reproduces grid min 0.2487462 at t≈0.577 (the
  minimizer is at ~0.577, NOT 0.67; the function near-EQUIOSCILLATES across
  t∈[0.5,1.5], the LP-optimal Chebyshev signature).
- Singularities handled rigorously: the lower bound of g uses only an UPPER bound
  of |Q_j|^2 per cell (via a 2nd-order Taylor/mean-value model), which is finite
  even where |Q_j|->0; there -c_j log|Q_j|->+inf only HELPS. No blow-up, the
  minimizer sits clear of all Q_j zeros. (Closes outline-reviewer issues 1-4.)
- Artifacts: certificate/flammang_table1.py, certificate/verify_vec.py (run this),
  certificate/verify_flammang.py + verify_fast.py + fastiv.py (cross-checks),
  certificate/README.md (rigor chain). Soundness selftest: 0/400 violations vs
  high-precision mpmath. Reproduce: `python3 constants/82a/certificate/verify_vec.py`.

STAGE B — NO BREAK. Column generation (certificate/stageB_colgen.py) reproduced
  the LP optimum m*=0.2487464 at Flammang's 24-poly set (validates LP), extracted
  the dual measure mu* (support ~25 control points), and priced candidate integer
  polynomials by reduced cost r(Q)=sum_n mu*_n log|Q(w(t_n))|. Over dictionaries of
  low-degree integer polys, pairwise/triple products of the existing Q_j, and small
  perturbations (thousands of candidates): the most-negative reduced cost was
  ~ -1e-7 to -1e-9 (control-point noise level); adding the best column changed the
  LP optimum by ~2e-11. NO improving integer column exists within reach -> no
  record break. Consistent with Doche->Flammang gain being only 5e-4 after a large
  dedicated LLL search. To push further one must run Flammang's LLL/transfinite-
  diameter breeding at degrees k>32 (the genuine search Flammang stopped at), not a
  quick column-generation pass. See approaches/lp-column-generation.md for detail.

## Idea
Flammang's lower bound C_82 >= m, where
  f(z) = log max(1,|z|) + log max(1,|1-z|) - sum_{j} c_j log|Q_j(w)|,  w = z(1-z),
  m = min_{0<=t<=pi} f(e^{it}),   c_j > 0,  Q_j in Z[w].
Rigor: sum over conjugates + Res(P, Q_j(z(1-z))) is a nonzero integer => the c_j-terms drop,
leaving log zeta(alpha) >= m. So ANY admissible (Q_j, c_j) with a rigorously certified
min m gives a valid lower bound C_82 >= m. We do NOT need Flammang's exact c_j — we re-derive
our own via the LP. This is the load-bearing structural fact (see BMQS Thm D: this is the
dual problem D(g)).

## Stage A — reproduce (safe milestone)
1. Transcribe Table 1: the ~23 integer polynomials Q_j(w) (extracted, see below) and their
   floats c_j. Confirm each Q_j has integer coefficients (inspection) and that none divides
   the conjugate product trivially (the resultant-integer argument is exact algebra, cite it).
2. Evaluate m = min_{t in (0,pi)} f(e^{it}) on a fine grid; confirm m ~ 0.2487.
   (Sanity check done in round 1: 5 dominant terms alone give min 0.218 at t~0.70, climbing
   toward 0.2487 as the full set is added — machinery confirmed sound.)
3. RIGOROUS certification of the min (the hard step, see below): interval-arithmetic / 
   branch-and-bound on t in [0,pi] proving min f >= 0.248746. Artifact = a re-runnable script.

Deliverable A: script `certificate/verify_flammang.py` + a stored certificate file
(the polynomial table, the c_j, and the branch-and-bound interval enclosure of the min)
proving C_82 >= 0.248746. This alone is a reviewer-verifiable MILESTONE (reproduce-the-record).

## Stage B — extend (attempt a record break)
4. Re-solve Smyth's semi-infinite LP: variables c_j >= 0, maximize m subject to
   f(z) >= m at a dense set of control points t_n in (0,pi). scipy.optimize.linprog
   (maximize m = minimize -m, linear constraints log-max(...) - sum c_j log|Q_j| >= m).
   With Flammang's set this recovers m ~ 0.2487 (validates the LP).
5. Breed NEW integer polynomials Q_j that lift the ACTIVE local minimum (the t* where f is
   smallest after the LP). Two sub-routes:
   (5a) LLL on Re/Im of trial polynomial values at control points near t* (Flammang's own
        weighted-transfinite-diameter recipe — extend her k<=32 search to higher degree /
        more control points / different starting factor).
   (5b) Cheaper: enumerate small-coefficient integer polynomials in w of degree up to ~24,
        score each by the marginal LP improvement (reduced cost / column generation), add the
        best, re-solve. This is the LP "column-generation" view — directly targets the binding
        constraint, which is exactly the "which direction to search" bottleneck BMQS/Doche flag.
6. Re-solve the LP with the enlarged set; if m_new > 0.248746, rigorously re-certify the new
   min (Stage A step 3 machinery on the new f). Record break.

Deliverable B: enlarged polynomial set + c_j + a fresh branch-and-bound certificate for the
new, larger m. Only goes into current.md `held` if the min is rigorously certified.

## HARDEST step (named)
Rigorous certification that min_{t in [0,pi]} f(e^{it}) >= target.
- Mechanism: f is real-analytic on (0,pi) except at the t where some Q_j(w(t)) = 0 (there
  -c_j log|Q_j| -> +infty, so those points HELP and can be excluded by small guard intervals).
  Between zeros, bound f below on each subinterval via interval arithmetic on the explicit
  expression: enclose w(t)=e^{it}-e^{2it}, enclose each |Q_j(w)| from below/above, enclose the
  log-max terms; subdivide (branch-and-bound) any interval whose lower bound dips below target.
  Use `mpmath`/interval or a Taylor/Lipschitz bound on f' to bound the per-interval variation.
- Why it should hold: the min is a smooth interior min at an isolated t*; away from it f rises,
  and near the Q_j zeros f -> +infty, so the inf is a clean finite interior minimum that
  branch-and-bound resolves in finitely many subdivisions. This is standard for Smyth-type
  auxiliary functions (Flammang/Rhin-Wu do exactly this certification in related papers).
- Risk: implementation effort in interval arithmetic; the float min is trivial, the *proof*
  is the work. Mitigation: a Lipschitz/derivative-bound grid certificate (bound |f'| on each
  cell, evaluate f at cell center, certify center - L*halfwidth >= target) is simpler than full
  interval AA and sufficient for a reviewer.

## Check the builder runs
- `verify_flammang.py`: load (Q_j, c_j), assert integer Q_j, compute branch-and-bound lower
  bound of min f, print it, assert >= 0.248746. Reviewer re-runs and re-derives the drop-out
  of the c_j terms from the resultant-integrality fact.
- For Stage B: same script on the enlarged set, plus the LP solve log showing m_new.

## Extracted Table 1 polynomials (Q_j in w, from flammang_zz_hal.pdf)
c_1=0.233410801570  Q_1 = w
c_2=0.181822930849  Q_2 = w-1
c_3=0.001206393184  Q_3 = w^3+w^2-2w+1
c_4=0.000374649587  Q_4 = w^3-4w^2+3w-1
c_5=0.005894024785  Q_5 = w^4-2w^3+4w^2-3w+1
c_6=0.000183896015  Q_6 = 2w^7-5w^6+6w^5+2w^4-11w^3+11w^2-5w+1
c_7=0.000078343816  Q_7 = w^8-2w^7+4w^6-7w^5+13w^4-16w^3+12w^2-5w+1
c_8=0.002193099635  Q_8 = w^8-3w^7+8w^6-16w^5+26w^4-27w^3+17w^2-6w+1
c_9=0.000147754755  Q_9 = w^8-w^7-3w^5+15w^4-22w^3+16w^2-6w+1
c_10=0.000000733657 Q_10 = 2w^10-4w^9+6w^8-13w^7+40w^6-78w^5+91w^4-66w^3+30w^2-8w+1
c_11=0.000165661820 Q_11 = w^11-w^10-w^9+5w^8-13w^7+40w^6-78w^5+91w^4-66w^3+30w^2-8w+1
c_12=0.000048632149 Q_12 = w^12-3w^11+7w^10-14w^9+30w^8-58w^7+96w^6-123w^5+114w^4-73w^3+31w^2-8w+1
c_13=0.000256750154 Q_13 = w^12-3w^11+8w^10-18w^9+36w^8-62w^7+97w^6-123w^5+114w^4-73w^3+31w^2-8w+1
c_14=0.000495658299 Q_14 = w^13+w^12-7w^11+22w^10-56w^9+134w^8-265w^7+384w^6-393w^5+283w^4-142w^3+48w^2-10w+1
NOTE: c_15..c_23 are degree-16/17/20/22 polynomials whose coefficient lists wrap across PDF
lines; the builder MUST re-extract them carefully from flammang_zz_hal.pdf (text around the
"Table 1" region, IDX ~11820 in extract_text output) and validate by re-deriving m ~ 0.2487.
The full set is required to reach 0.2487; the 14 above give a smaller m.

## Spec review: not required
(Routine reproduce-then-push on the existing record method; the structural rigor is settled by
BMQS Thm D and Flammang. Outline-reviewer optional.)
