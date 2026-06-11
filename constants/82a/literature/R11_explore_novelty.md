# R11 DEPTH explore — NOVELTY / publishability scan for 82a

Question driving this round (user, R11): our R5->R11 upper-bound nibbles
(Doche/Flammang free-exponent blocks, total gain ~4e-4, gap still ~0.0053) are NOT a
publishable contribution. What WOULD be a genuinely novel, publishable advance on
C_82, and which untried technique is most likely to deliver it? Does NOT attempt the
improvement.

## 0. State of the art is unchanged — confirmed by a fresh 2026 scan
- SOTA lower 0.24874 [Flammang F18, 2018]; SOTA upper now 0.25404 (this repo, was
  Doche 0.25444). Gap ~0.0053. This IS the genuine frontier.
- Morales 2022 ("Essential Minimum in Families of lines", arXiv:2201.11174) treats
  the ZZ height directly but does NOT improve it: its Fekete-Szego (BMPRS) method
  gives only a weaker DENSITY interval, mu_ess(hZ) <= 0.31944909 (Thm A). Explicitly:
  "Our contribution does not improve Doche's theorem." So no hidden better bound
  exists in the recent literature. The 0.24874..0.25404 gap is real.
- BMQS 2026 (arXiv:2601.18978): pure duality/computability, quotes the WEAKER
  Zagier/Doche numbers, no algorithm, no new bound. Conceptual only (already digested).

## 1. What a referee would count as a publishable advance (ranked novelty x feasibility)

The R5->R11 family-enrichment is unpublishable for a precise reason: it is the SAME
Doche limit-point machine (1 valid q in an admissible dictionary -> one explicit
integral), just with more perturbing factors. No new idea, the gap barely moves, and
the lower bound — the harder, more interesting side — never moves at all.

Ranked candidate contributions:

(a) **A new LOWER-bound TECHNIQUE that moves 0.24874 for the first time.**
    NOVELTY: high (the lower bound has been stuck at the Smyth/Flammang
    auxiliary-function method since 1980; Flammang 2018 is the last word). FEASIBILITY:
    medium — there is now a concrete, published, transferable technique for the closest
    cousin (OSS energy method, below). A first-ever improvement of the ZZ lower bound by
    a genuinely new constraint is squarely paper-worthy even if the numeric gain is
    modest. **TOP pick on novelty x feasibility.**

(b) **A unified two-sided primal-dual converging scheme** that brackets C_82 to many
    digits, exploiting BMQS strong duality (no duality gap). NOVELTY: very high — would
    be the first PRACTICAL realization of BMQS for ZZ, directly "closing the gap" the
    way the user wants. FEASIBILITY: medium-low for many digits, but a partial result
    (both bounds tightened in one coherent scheme) is already publishable. The Fekete
    converse (Orloski-Sardari arXiv:2304.10021, below) is exactly this scheme realized
    for SSS and is the template. **2nd pick; highest ceiling.**

(c) **A from-scratch upper construction with a STRUCTURAL (not numeric) improvement** —
    e.g. a new limit-point FAMILY (not just more factors in Doche's), or proving Doche's
    conjectured smallest limit point <= 1.2875274. NOVELTY: medium. FEASIBILITY: medium.
    Less interesting than (a)/(b) because the upper side is already "soft" and our 0.25404
    is close to Doche's conjectured truth ~0.25272 — limited headroom and the method is
    not new. Marginal-publishability.

(d) **Pinning the exact value.** Not feasible — BMQS show the constant is computable but
    "far from practical"; no closed form is known or conjectured. Off the table.

VERDICT: the publishable play is (a) and/or (b), BOTH on the lower/two-sided side, BOTH
delivered by the same new machinery (logarithmic-energy / Fekete-converse). The upper
side is a dead end for novelty.

## 2. Analogous-constant technique survey — what produced REAL jumps, and transferability

The ZZ ess-min, the Schur-Siegel-Smyth (SSS) trace, integer Chebyshev / integer
transfinite diameter, and Mahler/Lehmer all share the Smyth auxiliary-function /
potential-theory machinery. The decisive recent jumps:

### SSS trace problem — the LOG-ENERGY constraint (Orloski-Sardari-Smith, arXiv:2401.03252, 2024)
- The single biggest SSS lower-bound jump since 1984: 1.784 -> **1.80203**, with only
  4 polynomials (vs Wang-Wu-Wu 2021's 130).
- THE IDEA: Smyth's LP uses only univariate columns int log|Q(x)| dmu >= 0 (valid
  because prod_i Q(alpha_i) is a nonzero integer). OSS ADD the MULTIVARIATE integrality
  column for Q(x1,x2)=x1-x2: the logarithmic ENERGY
       I(mu) = int int log|x1-x2| dmu dmu >= 0
  (valid because disc(P) = prod_{i<j}(alpha_i-alpha_j)^2 is a nonzero integer, |disc|>=1).
  I(mu) is CONCAVE (Ahlfors) => strong duality holds for the augmented program.
- THE CERTIFICATE (their Theorem 1.1 — the load-bearing object): the optimal mu_A is
  supported on a finite union of intervals Sigma with I(mu_A)=0, and the dual auxiliary
  inequality is NOT Smyth's pure 1-D inequality but a SELF-COUPLED one:
       x  >=  lambda_A + sum_{Q in A} lambda_Q log|Q(x)| + lambda_0 * U_{mu_A}(x),
       U_mu(x) = int log|x-z| dmu(z)   (logarithmic potential of mu),
  with int log|Q| dmu_A = 0 whenever lambda_Q != 0, and density
       f(x) = |p(x)| sqrt(|H(x)|) / prod_{lambda_Q != 0} |Q(x)|.
  Solved by gradient descent on the interval endpoints. The extra lambda_0*U_mu term is
  exactly what a pure-Flammang LP cannot express.

### Quantitative converse of Fekete (Orloski-Sardari, arXiv:2304.10021, 2023) — the UPPER / unified side
- Companion paper. Gives an explicit-measure UPPER bound for SSS: 1.898 -> **1.8216**.
- THE IDEA (Thm 1.12): for a measure mu with logarithmic energy I(mu), the number of
  irreducible monic integer polys of degree ~n with n roots distributed ~mu is
       ~ exp( n^2/2 * I(mu) + ... ).
  So a measure with I(mu) < 0 (negative energy) is NOT approximable by Galois orbits;
  a measure with I(mu) >= 0 (an "arithmetic measure") IS. This makes the BMQS primal
  P(g) = inf_{arithmetic mu} int g dmu CONSTRUCTIVE: you build explicit equilibrium-type
  measures with computable energy and read off int g dmu as an upper bound — NO
  hand-tuned polynomial families (no Doche-style Q-breeding).
- Thm 1.5 (their LP-duality): primal (min int x dmu s.t. potential + I(mu)>=0
  constraints) and dual (explicit dual measures nu_A with computable energy) have
  Lambda_A = lambda_A — strong duality. As the polynomial family A grows, the upper
  Lambda_A and the lower lambda_A close on lambda_SSS MONOTONICALLY from both sides.
- THIS IS candidate (b) made real: a single primal-dual scheme that drives BOTH bounds
  together, exactly the BMQS no-gap object, with a working numerical method (gradient
  descent on interval endpoints).

### Integer Chebyshev / transfinite diameter, Mahler/Lehmer
- Engine BEHIND Flammang's Q_j generation (weighted integer transfinite diameter, LLL,
  k<=32). Newer generators (semi-infinite + integer programming, arXiv:1804.05985;
  generalized Gorshkov-Wirsing) make better small-sup-norm integer polynomials — a
  STRONGER COLUMN GENERATOR for the same LP. This is the "more/better columns" lever:
  R1 showed Flammang's existing set is LP-optimal over cheap dictionaries (reduced cost
  ~-1e-7 = noise); only genuinely deeper columns help, and the historical payoff of that
  lever was small (~5e-4 for a huge search). LOWER priority — it does not add a NEW
  constraint type, so it is not the novel idea. Best as a complement, not the headline.

## 3. The single most promising untried technique (for the outliner)

**Add the logarithmic-ENERGY dual column I(mu) = int int log|z1-z2| dmu dmu >= 0 to
Flammang's Smyth-LP for the ZZ lower bound — the OSS energy method (arXiv:2401.03252),
realized via the self-coupled Theorem-1.1 certificate.**

Why this is THE pick:
- It is a GENUINELY NEW constraint for 82a. Flammang F18 uses ONLY univariate columns
  int log|Q(w)| dmu >= 0; she NEVER uses the energy/discriminant column (confirmed
  against flammang_F18_digest.md). The ZZ conjugates are roots of an integer poly, so
  disc is a nonzero integer and I(mu) >= 0 holds verbatim. It is an UNUSED, independent
  dual column that can ONLY RAISE the lower bound past 0.24874.
- It is the EXACT technique that delivered the biggest cousin-constant jump in 40 years,
  with a published, concrete certificate structure (the lambda_0*U_mu self-coupled dual
  inequality + the |p|sqrt|H|/prod|Q| density + gradient descent on endpoints).
- It is precisely the "Polya / potential-theory" reframing the user asked for, AND it
  dovetails with candidate (b): the Fekete-converse companion (arXiv:2304.10021) gives
  the matching constructive UPPER side, so the SAME energy machinery yields a unified
  two-sided scheme. Strong, paper-worthy story: "first improvement of the ZZ lower
  bound since Flammang, by importing the OSS energy constraint; combined with the
  constructive Fekete-converse upper measure, a unified primal-dual bracket."

### The load-bearing HARD STEP the outliner must plan around (do NOT hand as one builder task)
The energy term self-couples mu: the dual auxiliary inequality is no longer a pure 1-D
min of a FIXED f, it is
     g_ZZ(z) >= lambda_0 + sum_Q lambda_Q log|Q(w)| + lambda_E * U_mu(z),
where g_ZZ(z) = log^+|z| + log^+|1-z| (the ZZ Green-function integrand) and U_mu is the
potential of the as-yet-unknown optimal mu. So the certificate is a self-consistent
fixed point (mu, support Sigma, lambda_E), not the R1 branch-and-bound min-of-fixed-f.
Two further 82a-specific complications vs SSS:
 (i) the ZZ measure lives on the contour w = e^{it} - e^{2it} (or two copies via
     z -> 1-z), NOT an interval in R+, so the OSS density f = |p|sqrt|H|/prod|Q| is not
     verbatim — Sigma is an arc/curve, not a union of real intervals.
 (ii) the variable is w = z(1-z); the energy is in z (the conjugates), so the
     change-of-variable z->w must be tracked in the potential term.

### How to sequence it (per the run_state R8/R10 anti-crash rule)
Do NOT give a builder the whole self-coupled certificate as one task. Split:
 - STAGE 1 (conjecture-LP, outliner+builder, outline-reviewed): build the augmented LP
   on a FIXED finite column set {existing Flammang Q_j} PLUS the single energy column,
   solve the self-consistent (mu, lambda_E) numerically (gradient descent on support
   endpoints / arc parametrization, OSS Section 6 recipe). Output is a CANDIDATE lower
   value > 0.24874 — a CONJECTURE, not a milestone. Check it actually exceeds 0.24874 by
   >> cert slack BEFORE going further.
 - STAGE 2 (separate atomic builder): turn the candidate (lambda_0, {lambda_Q},
   lambda_E, mu) into a RIGOROUS certificate — verify the self-coupled inequality holds
   on the contour by interval/branch-and-bound with outward rounding (extend the
   R1 verify_vec.py harness with the U_mu potential term), with the finite-exception
   (resultant-zero) clause. Reviewer verifies Stage 2 only.

## 4. Secondary / fallback angles (if energy method stalls at Stage 1)
- Constructive Fekete-converse UPPER measure (arXiv:2304.10021) as a standalone: build
  an explicit arithmetic measure on the ZZ contour with computable int g_ZZ dmu < 0.25404.
  Lower novelty than the lower-bound energy play but still a new (measure-theoretic, not
  Doche-family) upper method. Could pair with Stage 1 for the two-sided story.
- Stronger column generator (IP/SDP, arXiv:1804.05985) to breed Flammang Q_j at k>32 —
  same-method "more columns" lever, modest expected gain, NOT novel. Last resort only.

## Dead ends already burned (do NOT retry) — confirmed this round
- Same-family q-tuning (R5->R6, gain <1e-6) and adding yet more Doche/Flammang
  free-exponent perturbing blocks (R7->R11): these are the UNPUBLISHABLE nibbles the
  user flagged. STOP. (run_state rule.)
- LP column-generation on Flammang's FIXED 24-poly set / cheap dictionaries (R1):
  reduced cost ~-1e-7 = noise. No improving univariate column.
- Morales 2022 Fekete-Szego density method: gives only 0.319, does NOT beat Doche.
- BMQS as a route to a number: non-constructive, weaker quoted bounds.
- Potential-theory reframing as a STANDALONE method (R7): BMQS strong duality means
  reframing gives the SAME number — the gap is a TRUNCATION gap. The energy constraint
  is novel because it REDUCES truncation (a new column type), not because it reframes.

## Digests saved this round
- this file: constants/82a/literature/R11_explore_novelty.md (novelty/publishability
  scan; ranks the 4 publishable-contribution candidates; names the OSS energy method as
  the single most promising untried technique with its Thm-1.1 certificate structure and
  a crash-safe 2-stage plan).
- constants/82a/literature/pdfs/morales_2201.11174.pdf (downloaded; confirms Morales
  does NOT improve the ZZ bounds — only a 0.319 density interval).
- (already on disk from R7) pdfs/sss_2401.03252.pdf = OSS energy method, the source for
  the recommended technique; the Thm-1.1 self-coupled certificate is excerpted above.
- NOTE: the Fekete-converse companion arXiv:2304.10021 (Orloski-Sardari, the
  constructive UPPER/unified side) is NOT yet on disk — fetch + digest it in Stage 1 if
  candidate (b) is pursued.
