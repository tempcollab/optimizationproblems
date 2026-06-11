# Approach R7 — all-duals structural closure of the asymmetric-Z[z]-column leak

## Status
VERIFIED-NEGATIVE structural closure (builder-claimed, awaiting reviewer). NO raise:
held stays Flammang [F18] 0.2487458; Status none. This seals the last FORMAL gap R3
left on the lower side — the asymmetric integer columns R(z), R in Z[z]\{0}, that sit
OUTSIDE the Z[w] span R3 ceilinged.

## What this closes, and why it is distinct
R3 (ceiling_primal.py) capped the contour/auxiliary-function method over the
breeding-saturated **Z[w]** dictionary at C = 0.2487857. But R3's ceiling formally
covered only auxiliary functions in the SPAN of Z[w] columns (functions of w=z(1-z)).
An **asymmetric** integer column -c*log|R(z)|, R in Z[z] NOT a polynomial in w, c>=0,
lies OUTSIDE that span. R2 closed those columns only NUMERICALLY (both-circle LP screen
to deg 40, optimal weight ~1e-8). This round upgrades that finite numerical screen to an
**all-duals theorem**: every asymmetric column reduces by an EXACT symmetrization identity
to a Z[w] column already covered by R3 — for EVERY feasible dual, no column list, no
degree cutoff, no sampled dual.

- **vs R2:** R2 screened a finite batch of asymmetric columns against a finite dual to
  deg 40 (c_R ~ 1e-8, numerical). This proves STRUCTURALLY (exact identity) that EVERY
  asymmetric column collapses to (1/2) int log|S(w)| dmu_sym, S=R(z)R(1-z) in Z[w]; it
  NEVER needs the asymmetric deg-40 LLL screen — it eliminates the direction by an
  identity. (Removes the SEPARATE R2 asymmetric uncertainty.)
- **vs R3:** R3 ceilinged the LOADED Z[w] dictionary; asymmetric Z[z] columns were outside
  R3's span. This supplies the missing lemma that they reduce INTO the Z[w] span, making
  the R3 ceiling formally apply to all of Z[x]. (The missing lemma R3 did not cover.)
- **vs R6:** R6 closed the Galois-symmetric MEAN-functional route ("symmetric => power
  sums + log-energy OR height"); that dichotomy provably does NOT apply to asymmetric
  columns. This closes exactly that gap, by a DIFFERENT mechanism (z<->1-z symmetrization
  of the dual).

## The theorem (three exact lemmas + the weak-duality closure)
Let sigma_ZZ(z)=log+|z|+log+|1-z| [Flammang eq 2.1], T(z)=1-z (an involution),
F = BMQS feasible primal class (conjugation-invariant prob. measures mu with
int log|Q| dmu >= 0 for ALL Q in Z[x]\{0}).

- **Lemma 1 (sigma_ZZ T-invariant).** sigma_ZZ(1-z) = log+|1-z| + log+|z| = sigma_ZZ(z).
  One-line substitution; verified to machine zero over 2000 plane points (selftest S1).

- **Lemma 2 (F is T-symmetrizable).** T maps Z[x]\{0} bijectively onto itself (Q(1-z) in
  Z[x]\{0}; binomial expansion keeps integer coeffs; T involution). So the constraint
  family {int log|Q| dmu >= 0 : Q in Z[x]} is **T-invariant**: for mu in F,
  int log|Q| d(T_*mu) = int log|Q(1-z)| dmu >= 0 because Q(1-z) in Z[x] and mu satisfies
  the constraint for ALL of Z[x] — Q(1-z) included. Index set closed under T ⟹ pushing
  forward PERMUTES the constraints, never creates a violated one. Hence T_*mu in F; by
  convexity mu_sym=(mu+T_*mu)/2 in F is T-symmetric; by Lemma 1
  int sigma_ZZ dmu_sym = int sigma_ZZ dmu. So **P = P_sym** (infimum attained within the
  T-symmetric subclass — at the level of INFIMA, no attainment / weak-* compactness used).

- **Lemma 3 (R(z)R(1-z) in Z[w] — invariant theory, a THEOREM).** Z[z] is a free rank-2
  module over Z[w], w=z(1-z), with basis {1, 1-2z}; (1-2z)^2 = 1-4w. For any P in Z[z],
  reduce mod (z^2-z+w): P = A(w) + B(w)(1-2z), A,B in Z[w]. T sends 1-2z |-> -(1-2z), so
  P(1-z) = A(w) - B(w)(1-2z). Thus **P T-invariant <=> B=0 <=> P in Z[w]**. S(z):=R(z)R(1-z)
  IS T-invariant (T swaps the factors) ⟹ S in Z[w] with INTEGER coefficients. QED.
  The script proves this on a GENERIC degree-6 poly (T flips the z-coefficient of the
  remainder, so T-invariance forces it to 0), then exhibits the reduction on a batch; the
  symbolic batch is a CHECK, not the proof.

- **All-duals mechanism.** Against ANY T-symmetric mu_sym, phi(z)=log|R(z)|-log|R(1-z)|
  has phi(1-z)=-phi(z), and int phi dmu_sym = int phi(1-z) dmu_sym = -int phi dmu_sym
  forces int phi dmu_sym = EXACTLY 0. Hence
  int log|R(z)| dmu_sym = (1/2) int log|R(z)R(1-z)| dmu_sym = (1/2) int log|S(w)| dmu_sym,
  S in Z[w]. The asymmetric column contributes EXACTLY a Z[w] column's value. (No sampling,
  all duals.)

- **Weak-duality closure (F5; NO strong duality / NO BMQS Thm D / NO attainment).** Any
  valid dual lower bound L = inf_z(sigma_ZZ - sum_j c_j log|Q_j|), c_j>=0, Q_j in Z[x],
  satisfies for EVERY feasible primal mu:
  L <= int(sigma_ZZ - sum_j c_j log|Q_j|) dmu <= int sigma_ZZ dmu (uses c_j>=0 AND
  int log|Q_j| dmu >= 0). Take mu = R3's symmetric feasible mu_hat at objective 0.2487857.
  Then L <= 0.2487857 whether or not the dual uses asymmetric columns.

## Two-warrant scoping (load-bearing honesty — mirrors R3; this is NOT "exact, zero residual")
The closure is a CONJUNCTION of two warrants, exactly like R3:

- **(a) [THIS BUILD, exact]** the symmetrization identity: every asymmetric column
  -c*log|R(z)| reduces against any T-symmetric dual to -c*(1/2)*log|S(w)|, S=R(z)R(1-z) in
  Z[w]. Lemmas 1-3 + the antisymmetric-residual identity are EXACT (all duals). This
  REMOVES the separate R2 asymmetric uncertainty.
- **(b) [INHERITED from R3 warrant (b), NUMERICAL, NOT a theorem]** the surviving integral
  int log|S(w)| dmu_sym must be >= 0 for an ARBITRARY S in Z[w] — and S need NOT be one of
  the 300 loaded columns. mu_hat (hence mu_sym) is interval-certified feasible only against
  the 300 LOADED columns (warrant a). Feasibility against ALL of Z[w] is the R3
  breeding-saturation (LLL to deg 40, no column prices below LP noise), a finite numerical
  screen, NOT a theorem.

**HONEST CLAIM:** the asymmetric-Z[x] leak is RIGOROUSLY REDUCED to the already-ceilinged
Z[w] question. It is NOT an independent "all-duals exact, attainment-free" closure; it
inherits R3 warrant (b) exactly once, on the Z[w] side. No NEW numerical screen, and no
SEPARATE asymmetric uncertainty, remains.

## Where the structure lands on the ACTUAL R3 object (warrant a, concretely)
On ceiling_muhat.json the loaded columns are Q_j(w), w=z(1-z), which is T-invariant
(verified max|w - w(1-z)| = 3.1e-16 over the atoms). So the symmetrization is CLEAN against
the loaded set: T_*mu_hat and mu_sym=(mu_hat+T_*mu_hat)/2 satisfy every one of the 300
columns with the SAME margin (+8.818e-5) and the SAME objective (0.2487856346). This is the
numerical witness that the symbolic theorem's hypotheses hold on the actual R3 certificate —
NOT a re-screen of columns. Extension to all of Z[w] is warrant (b).

## Reproduce
    python3 constants/82a/certificate/close_asymmetric.py            # CERTIFIED
    python3 constants/82a/certificate/close_asymmetric.py selftest   # soundness (S1-S3)
    python3 constants/82a/certificate/close_asymmetric.py tamper     # bogus inputs FAIL
certify: [C1] Lemma 3 (generic + batch), [C2] antisym residual = 0, [C3] preservation on
ceiling_muhat.json. tamper: (T1) asymmetric measure makes the residual nonzero (-0.015,
so [C2] is not trivially 0); (T2) a FAKE R(z)^2 (not R(z)R(1-z)) leaves a z-term and is
rejected as not in Z[w].

## What would push it further (and why it won't, on the lower side)
This is the LAST formal gap on the lower side. With it, the R3 Z[w] ceiling applies to the
FULL Z[x] dual (symmetric AND asymmetric columns). The only residue outside every closed
span is the p-adic / non-archimedean local-height longshot (toolless; effective version
caps 0.2406 < Flammang). A genuine lower-side raise is not reachable with known tools; the
pushable frontier is the UPPER bound (held 0.2540419719, R11).
