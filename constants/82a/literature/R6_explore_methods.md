## 82a  (C_82a: essential minimum of the Zhang-Zagier height h_Z(alpha) = h(alpha)+h(1-alpha))

- Current bounds: lower = 0.2487458 = log(1.282416) [Flammang F18, 2018; reviewer-verified R1], upper = 0.2540419719 [this run R11, < Doche 0.25443677]
- Softer target: **UPPER** (held 0.2540419719). The lower side is, after R1-R5 plus the retracted R12-R17, the most exhaustively screened bound in this run; every classical and Polya-principle machine is closed or barred. The upper side has 6 straight verified record-breaks (R5-R11) and is the demonstrably pushable frontier. The user's standing focus is the lower bound — do NOT switch without a fresh user signal — but the honest tractability verdict is: no reachable lower-side raise this round.

### Triage of the THREE assigned candidates (genuinely-new, outside the aux-function/energy/moment family)

**Candidate 1 — p-adic / non-archimedean local-height refinement. VERDICT: OPEN-but-toolless; the 0.2406 ceiling is REAL, not an artifact. NOT tractable this round.**
- Zagier's original proof (1993) decomposes h_Z over ALL places: h_Z(alpha) = sum_v (log+|alpha|_v + log+|1-alpha|_v). The archimedean part is what Flammang's auxiliary function optimizes; the non-archimedean part is controlled by |Res(P, P(1-x))| >= 1 / the reduction of alpha(1-alpha) mod v. This IS genuinely outside both walls (contour LP `log|Q|` span; barred log-energy) — it is the one residue R5 recorded OPEN.
- WHY the 0.2406 ceiling is real, not an artifact (verified this round against the splitting-condition literature): the ONLY rigorous machines that convert "non-archimedean local structure" into a height floor are the Fili-Petsche / Bombieri-Zannier potential-theoretic bounds (arXiv:1508.01498, 1504.04985, 2404.11559). Two independent structural blocks, EITHER fatal, confirm the ceiling:
  (a) SPLITTING HYPOTHESIS REQUIRED. Every such bound assumes the number is totally real / totally p-adic / has all conjugates in a fixed local field (a splitting/ramification condition). ZZ-minimal numbers carry NO such hypothesis — they range over all algebraic numbers — so the finite-prime floor is simply absent for the ess-min class. (Abstract + body of 1508.01498/2404.11559 both state the local-containment restriction explicitly; this matches the R4 digest's Angle-2 finding.)
  (b) MECHANISM IS LOG-ENERGY, capacity-1 trivial. The local floor is a mutual-energy integral I(mu,nu) >= 0 on the Berkovich line. For ZZ this is (i) BARRED (the I(nu)<0 a^deg leading-coeff wall for non-integer alpha, R1) and (ii) the relevant archimedean place is the unit circle, capacity 1, where the leverage vanishes (BMQS Thm B / FR06, R4).
- The hard step (unchanged from R5): turning "alpha(1-alpha) has constrained reduction mod p across conjugates" into a degree-UNIFORM additive gain >= delta*d for ALL ZZ-minimal alpha surviving to the essential minimum. No tool delivers this; making it effective via |disc|/|Res| moments re-enters the barred energy span. The effective version reaches only ~0.2406 < Flammang. NO screenable lever — there is nothing for a builder to run this round.

**Candidate 2 — analogous SOLVED registry constants with an un-tried lower-bound method. VERDICT: NONE transferable (confirms R2/R3/R5).**
- The full height/Mahler/ess-min cousin family (Schur-Siegel-Smyth trace; absolute trace / Omega; house / Schinzel-Zassenhaus; Lehmer/Mahler; Faltings ess-min [BMRL]; ZZ) ALL use the SAME single machine: Smyth's explicit auxiliary-function / integer-transfinite-diameter LP (verified vs primary sources R3). The ONE published post-LP advance is OSS's energy/multivariate-integrality column (arXiv:2401.03252) — BARRED for ZZ. SOS/SDP has never beaten the LP for any of these (it adds no arithmetic content; recovers the continuum LP optimum). The SSS mean-DIRECT technique was screened R5 (needs a linear objective + integer trace; sigma_ZZ is non-linear and its conjugate-sum is the unknown height). No new transferable technique exists.

**Candidate 3 — post-2018 published number above 0.24874. VERDICT: NONE EXISTS. (No headline.)**
- arXiv 2019-2026 search (Morales 2201.11174; BMQS 2601.18978; Fili-Petsche 1508.01498 / 2404.11559; totally-p-adic 1504.04985 / 1802.05923 / 1901.07661; algebraic-dynamics 2502.03039) returns NO paper improving the ZZ ess-min LOWER bound past Flammang 0.24874.
  - Morales 2201.11174: UPPER/density bounds only; does not even cite Flammang. No lower-bound machinery.
  - BMQS 2601.18978 (2026, already digested): conceptual LP-duality only; quotes the WEAKER classical 0.248247 lower bound (Zagier/Doche), gives no finite LP / number; authors note "the algorithm is far from being practical." No harvestable number.
  - Fili-Petsche family: splitting-conditional + log-energy (Candidate 1); not a ZZ ess-min bound.
- No published bound to reproduce-and-verify. Flammang 2018 remains the SOTA lower bound.

### How the record was achieved (from the papers)
- Flammang F18 (lower, 0.2487458): Smyth-style explicit auxiliary function f(z) = log+|z| + log+|1-z| - sum_j c_j log|Q_j(z(1-z))|, Q_j in Z[w] (w=z(1-z)), c_j>0. Sum over conjugates: sum_i f(alpha_i) >= d*min f; the log|Q_j| terms drop out because prod_i Q_j(alpha_i(1-alpha_i)) = Res(P, Q_j(z(1-z))) is a nonzero integer (>= 1 in abs value, off a finite exception set). Hence h_Z >= min_{|z|=1} f = 0.2487458. The c_j / Q_j found by semi-infinite LP + weighted integer transfinite diameter (LLL, k=5..32).
- Upper (0.2540419719, this run R11): Doche's perturbed small-Mahler-measure polynomial family in X=z(1-z), h = Q1*Q2*Q5^qE*Q6^qF with free-exponent perturbing blocks; rigorous max(A,B) interval quadrature certificate (verify_upper_q6.py).

### Where the slack is
- LOWER side: the only non-barred headroom is the persistent MIN-vs-MEAN gap (R4): ZZ-minimal conjugates HUG the two circles |z|=1, |1-z|=1, but their MEAN of f beats the circle-MIN (the binding lobe w*~0.433-0.369i) by a PERSISTENT delta ~+0.003-0.02 (deg_w 16-22). Flammang throws this away in the min-reduction sum_i f >= d*min f. To cash it would need (1/d) sum f(alpha_i) >= min f + delta as a degree-UNIFORM floor for ALL ZZ-minimal polys — a HEIGHT-INDEPENDENT containment lemma forcing every conjugate off the single binding lobe, proved from the minimal polynomial's INTEGER/coefficient structure (NOT from h, NOT from log|disc|/energy). None is known; the energy version is barred, the height version (FR06/Petsche) is circular + capacity-1. This is a research longshot, not a screenable lever.
- UPPER side: the demonstrably pushable frontier (gap to Doche 0.25443677 is ~4e-4; the held-vs-conjectured-spectrum-point gap 0.2540 vs ~0.2527 lower / Doche spectrum 1.287527 still leaves room). The free-exponent multi-perturbing-block Doche family (Doc01a general-l) has yielded 6 straight verified breaks and is not exhausted.

### Angles to try
- LOWER side: there is NO tractable angle this round. All cheap/medium levers are closed; the p-adic residue is OPEN-but-toolless (no builder artifact possible); the min-vs-mean gap needs a containment lemma that does not exist. An HONEST verified-NEGATIVE (e.g. a clean reproducible screen confirming the p-adic local-height ceiling at ~0.2406 < Flammang, OR confirming no finite-prime column survives the no-splitting + capacity-1 obstruction) is the only logged-milestone outcome available on the lower side — and even that largely re-states R4/R5 closures.
- UPPER side (if the user releases lower-bound focus OR wants an actual record-break): continue the Doche general-l free-exponent perturbing-block enrichment that drove R5-R11 (add/re-optimize blocks from Flammang Table-1 as admissible perturbers in X=z(1-z); the certificate harness verify_upper_q6.py is reusable). This is where verified raises are reachable.

### Dead ends (do NOT retry — all reviewer-verified-NEGATIVE in constants/82a/)
- OSS log-energy / discriminant / multivariate-integrality / power-sum / w-moment columns (ANY form): BARRED (user R1 no-go, four mechanisms + two structural proofs; the a^deg leading-coeff wall makes I(nu)<0 / S_k non-integer for non-integer alpha). R1, R5.
- Contour-LP / Z[w] dictionary / continuum-SOS: R3-CEILINGed at 0.2487857 (feasible primal measure mu_hat, LP strong duality) — only +4e-5 above Flammang; the continuum-SOS lives inside this same span and can at best recover ~0.24879.
- Asymmetric-z columns / coupled (z,1-z) aux function: collapse on the both-circle gate (~1e-8) AND reduce to the barred integer-locus reduction (prod = Res/a^deg < 1 for non-integer alpha). R2, R3.
- k>32 LLL breeding (uniform AND lobe-adaptive dual): INERT, Z[w] LP-saturated. R1, R2.
- Integer-locus reduction (restrict to a=1): NOT a lever — the 2log(a)/d Weil penalty -> 0 as deg->inf, so excluding non-integers is as-hard-as-the-problem. R2.
- BMRL Faltings ess-min transfer (arXiv:1609.00071): same Smyth method, Koebe machinery irrelevant. R2.
- FR06/Petsche effective equidistribution as STATED: CIRCULAR (error ~(4h)^{1/2} contains the height) + capacity-1 (single-circle, wrong target). R4.
- SSS-trace mean-direct transplant: needs linear objective + integer trace; sigma_ZZ non-linear, conjugate-sum = d*h_Z - 2log a (unknown height). R5.
- Power-sum / w-moment column int w^k dmu = S_k/d: sign-indefinite + non-integer off a=1. R5.
- Fili-Petsche / Bombieri-Zannier / totally-p-adic splitting bounds: splitting-hypothesis-conditional (absent for ZZ ess-min class) + log-energy mechanism (barred, capacity-1 trivial). R4, confirmed this round.

### Digests saved
- /home/agentuser/repo/constants/82a/literature/R6_explore_methods.md (copy of this report; records the Candidate-1 p-adic ceiling verification, Candidate-3 no-published-number finding, and the splitting-condition re-confirmation of the Fili-Petsche family).
