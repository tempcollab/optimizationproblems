# R7 DEPTH explore — analogous constants / transferable techniques for 82a

Constant 82a = essential minimum C_82 of the Zhang-Zagier height h_Z(alpha)=h(alpha)+h(1-alpha).
Verified bounds entering R7: LOWER 0.24874 [Flammang F18, Smyth auxiliary-function LP],
UPPER 0.2543309112 [this repo R6, Doche perturbed limit-point family]. Gap ~5.6e-3.

This round surveys constants that share the SAME machinery (Smyth auxiliary functions /
integer transfinite diameter / potential theory) and ranks a TECHNIQUE worth transferring.
NOT attempting the improvement.

================================================================================
RANKED FINDINGS (by transferability to 82a)
================================================================================

--------------------------------------------------------------------------------
#1  (HIGHEST)  Schur-Siegel-Smyth (SSS) trace problem  —  the ENERGY-CONSTRAINT method
    Orloski, Sardari, Smith, "New Lower Bounds for the SSS Trace Problem",
    arXiv:2401.03252 (2024).  PDF: literature/pdfs/sss_2401.03252.pdf, text /tmp/sss_2401.03252.txt.
    VERIFIED from the full PDF body (not abstract).
--------------------------------------------------------------------------------
The constant: lambda_SSS = liminf tr(alpha) over totally positive algebraic integers
(absolute trace). This is the CLOSEST cousin of 82a: both lower bounds come from
Smyth's 1984 auxiliary-function LP, both upper sides from limiting conjugate
distributions, and BMQS (arXiv:2601.18978) explicitly treat both as the same LP-duality
object. SSS history: Smyth 1.7719 -> ... -> Wang-Wu-Wu 2021 1.7931 -> OSS 2024 1.80203.

WHAT SMYTH'S METHOD IS (identical skeleton to Flammang's 82a lower bound):
  Limit measure mu of conjugates satisfies  int log|Q(x)| dmu >= 0  for every Q in Z[x]
  (because prod_i Q(alpha_i) is a nonzero integer => |.|>=1 => log>=0). Minimize int x dmu
  s.t. those constraints. Dual: maximize lambda_A s.t.  x >= lambda_A + sum_Q lambda_Q log|Q(x)|,
  lambda_Q >= 0.  For 82a, Flammang's f(z) = logmax(1,|z|)+logmax(1,|1-z|) - sum c_j log|Q_j(w)|
  is EXACTLY this dual auxiliary function (w=z(1-z); the resultant-integrality = int log|Q|dmu>=0).

THE NEW STRUCTURAL IDEA (the transferable one):
  OSS add a constraint Smyth/Flammang NEVER used — the *multivariate* integrality
  int log|Q(x1,...,xn)| dmu...dmu >= 0 for Q in Z[x1,...,xn] (proved valid in Orloski-
  Talebizadeh [OT23]). The decisive instance is Q(x1,x2) = x1 - x2, giving the
  LOGARITHMIC ENERGY constraint
        I(mu) := int log|x1 - x2| dmu(x1) dmu(x2) >= 0.
  Validity: prod_{i<j}(alpha_i-alpha_j)^2 = disc(P) is a nonzero integer, so |disc|>=1,
  hence the conjugate measure has I(mu) >= 0. This is a genuinely NEW, independent
  constraint on mu that the univariate columns log|Q(x)| cannot reproduce.
  Payoff: I(mu) is CONCAVE (Ahlfors), so strong duality holds; OSS get 1.80203 with only
  4 polynomials, versus Wang-Wu-Wu's 130. The bound jump (1.7931 -> 1.80203) is the
  largest single SSS improvement since 1984 — and it came from a STRUCTURAL constraint,
  not from breeding more/better polynomials. (Theorem 1.1: optimal mu is supported on a
  finite union of intervals with explicit density |p(x)|sqrt(|H(x)|)/prod|Q(x)|;
  solved numerically by gradient descent on the interval endpoints.)

WHY IT TRANSFERS TO 82a's LOWER BOUND (the concrete opening):
  The Zhang-Zagier conjugate measure ALSO satisfies I(mu) >= 0 for the SAME reason:
  the conjugates alpha_i are roots of an integer polynomial, so disc is a nonzero integer
  and int log|alpha_i - alpha_j| dmu dmu >= 0. Flammang's F18 auxiliary function uses ONLY
  the univariate columns log|Q_j(w)| (resultant integrality) — she does NOT use the
  energy/discriminant constraint (confirmed against literature/flammang_F18_digest.md).
  So the energy constraint I(mu) >= 0 is an UNUSED, independent dual column for 82a.
  Adding it to the Flammang/Smyth LP can only raise the lower-bound optimum m past 0.24874.
  The 82a integrand is on the circle w = e^{it}-e^{2it} (or two copies via z->1-z symmetry)
  rather than an interval in R+, so the OSS density formula is not verbatim, but the
  ABSTRACT step — "augment Smyth's int log|Q|dmu>=0 LP with the concave energy constraint
  int log|x1-x2|dmu dmu >= 0 and use strong duality" — carries over directly. This is the
  single most promising structural angle and is exactly the "Polya / potential-theory"
  reframing the user asked for.
  HARD STEP to flag for the outliner: the energy term couples mu to itself (the dual
  picks up an extra potential term lambda_0 * U_mu(x) in the auxiliary inequality, OSS
  Thm 1.1 line 3), so the certificate is no longer a pure 1-D min of a fixed f — one must
  certify the self-consistent (mu, support Sigma, lambda_0) solution. Tractable but new
  certificate machinery vs. the R1 branch-and-bound min-of-f.

--------------------------------------------------------------------------------
#2  (MEDIUM)  BMQS strong-duality framing — already on disk, now CONTEXTUALIZED by OSS
    Burgos Gil, Menares, Qu, Sombra, arXiv:2601.18978 (2026).
    Digest: literature/bmqs_2026_digest.md.
--------------------------------------------------------------------------------
BMQS prove (abstractly) that the Smyth lower-bound LP and the limit-distribution upper-bound
method are dual and satisfy strong duality, so they meet at C_82 — but give NO algorithm and
quote a WEAKER numeric bound. R1 correctly flagged it as non-constructive. NEW in R7: OSS
2401.03252 is the CONSTRUCTIVE realization of exactly the BMQS duality for the SSS cousin —
it shows the missing-algorithm gap BMQS lament is closed (for SSS) by adding the energy
constraint and doing gradient descent on the support. So BMQS + OSS together say: the energy
constraint is the right extra dual variable, and there is a working numerical scheme for it.
Transfer value: BMQS tells you the duality is exact for 82a; OSS tells you HOW to exploit it.

--------------------------------------------------------------------------------
#3  (MEDIUM, UPPER side)  Limit-points-of-Mahler-measure breeding — genetic-algorithm search
    Boyd-Mossinghoff "Small Limit Points of Mahler's Measure", Exp. Math. 14 (2005);
    extended by Sac-Epee, El Otmani, Maul, Rhin (2021) via genetic algorithms /
    missing-data restoration. (Not on arXiv in full; abstracts/PDF via Project Euclid.)
--------------------------------------------------------------------------------
Doche's 82a UPPER bound IS a small-limit-point construction (h(q)=Q1*Q2 from a multivariate /
perturbed family, a limit value of single-variable heights) — structurally the same object as
a Boyd-Mossinghoff small limit point of Mahler measure. Boyd-Mossinghoff found 48 two-variable
integer polynomials with measure in (1,1.37) by treating n-variable measures as limits of
fewer-variable ones; Sac-Epee et al. then GENETIC-ALGORITHM-bred new limit points beyond the
Boyd-Mossinghoff list. Transfer: replace Doche's HAND-tuned 5-poly family + manual q-search
with (a) a WIDER dictionary of small-height base/perturbing factors in X=z(1-z), and (b) a
genetic-algorithm / multistart global search over BOTH the discrete factor choice AND the
real exponents q. R5/R6 already did continuous q-tuning inside Doche's FIXED family (well now
dry, 1.8e-6 gain); the untried lever is ENLARGING/EVOLVING the family itself — new factors,
new limit-point families (3-variable perturbations, the x1-x2-x3+x4 analogue OSS mention as
future work). This is the upper-bound counterpart to enriching the dictionary.

--------------------------------------------------------------------------------
#4  (LOWER, supporting)  Integer Chebyshev / integer transfinite diameter — LLL breeding
    Flammang-Rhin-Smyth "integer transfinite diameter of intervals" JTNB 9 (1997);
    Pritsker, Habsieger; "Applications of Integer/Semi-Infinite Programming to the
    Integer Chebyshev Problem" arXiv:1804.05985.
--------------------------------------------------------------------------------
This is the engine BEHIND Flammang's polynomial generation: she breeds the Q_j for the 82a
lower bound via the weighted integer transfinite diameter, doing LLL on Re/Im of trial
polynomial values at control points (k=5..32). The integer-Chebyshev literature has newer
generators — semi-infinite + integer programming (arXiv:1804.05985) and generalized
Gorshkov-Wirsing polynomials — that produce better small-sup-norm integer polynomials than
plain LLL. Transfer: a stronger column generator for the Flammang LP (breed Q_j at depth k>32
with IP/SDP-aided selection rather than LLL alone). NOTE: R1 column-generation already showed
Flammang's set is LP-optimal over cheap dictionaries; the gain needs genuinely new high-degree
columns, which is what these generators provide. Lower priority than #1 because it is the SAME
"more/better columns" lever that gave only 5e-4 over a huge search — whereas #1 adds a NEW
constraint type. Best used as a COMPLEMENT to #1, not instead of it.

--------------------------------------------------------------------------------
#5  (LOW / context only)  Potential energy inequalities (Hunter/Siegel refinements)
    Cherubini-Yatsyna "Potential energy of totally positive algebraic integers",
    arXiv:2202.05235. PDF: literature/pdfs/potential_energy_2202.05235.pdf.
--------------------------------------------------------------------------------
Proves Hunter-type inequalities relating potential energy E = sum_{i<j}(x_i-x_j)^2, power
sums, and the discriminant for totally positive integers. It is the SAME energy/discriminant
object OSS exploit, but packaged as fixed-n elementary inequalities (Siegel/Hunter Lagrange-
multiplier style), not an LP constraint. Confirms the energy-vs-discriminant link is a live,
correct tool, but offers no new LP machinery for 82a beyond what #1 already gives. Context only.

================================================================================
BOTTOM LINE FOR THE OUTLINER
================================================================================
- SOFTER SIDE remains the UPPER bound numerically (R5/R6 broke it; #3 is the way to push it
  further STRUCTURALLY, by evolving the family, not q-polishing — q-polishing is dry per
  run_state rule).
- But the HIGHEST-LEVERAGE STRUCTURAL transfer is #1 on the LOWER bound: add the concave
  logarithmic-energy constraint  I(mu)=int log|x1-x2|dmu dmu >= 0  (valid because disc is a
  nonzero integer) to Flammang's Smyth-LP. It is an UNUSED independent dual column, gave the
  biggest SSS jump in 40 years for the closest cousin, and is precisely the potential-theory
  reframing the user requested. Hard step: the self-coupled certificate (extra lambda_0*U_mu(x)
  term) — no longer a pure 1-D min-of-fixed-f.
- DEAD ENDS already on disk (do not retry): same-family q-tuning (dry, R6 1.8e-6); pricing
  cheap polynomial dictionaries against the Flammang dual (R1, no improving column);
  single-small-height-alpha as an upper bound (a spectrum point, not a bound).

Digests saved this round:
- literature/pdfs/sss_2401.03252.pdf  (Orloski-Sardari-Smith 2024 — the energy-constraint method)
- literature/pdfs/potential_energy_2202.05235.pdf  (Cherubini-Yatsyna — energy/discriminant inequalities)
- this file (R7_explore_analogous.md)
