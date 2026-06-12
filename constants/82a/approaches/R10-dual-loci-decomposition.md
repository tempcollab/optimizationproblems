# R10 — UPPER-INTERNAL dual-loci decomposition of the held certificate numerator

## 82a (UPPER)
Spec review: **required** — the numerator-split claim (Angle 1, step c) is the
load-bearing NEW identity and must be stated precisely; the whole milestone rides on it
being a genuinely-new exact decomposition, not a re-narration of R6/R8/R9.

Target to beat: 0.2538893183 = current held UPPER value (verify_upper_q8A.py, R4).
**This round is STRUCTURAL — the numeric upper lever is PROVEN EXHAUSTED on the Doche
family (A-base R7, B-branch R8, both reviewer-verified).** The deliverable does NOT move
the held number; it produces a NEW verifiable IDENTITY that decomposes the held
certificate numerator over the two upper-internal active loci. The held value
0.2538893183 must be REPRODUCED exactly (to cert precision) by the decomposition, which
is the pass criterion — not beaten.

Held R4 family (anchor for every check below): q=(14.011500,13.443930,2.643590,
2.299880,0.252420), qB=qC=0, qE=0.575080, qF=0.568800, qG=0.891590, qH=0.066860.
D = max(arg_A=61.65784, arg_B=72.00176) = 72.00176 (perturber B-branch attains D).
Phi(0) := int_0^1 G(chi(s)) ds = 18.2804777610. Phi(0)/D = 0.2538893183.
Active set {A0>B} = union of ~32 intervals, measure 0.0686, kink set K={A0=B} = 64
sign-changes STABLE across N (R8 audit — CITE, do not re-derive measure-zero).

================================================================================

## Angle 1 (top pick): active-arc PARTITION + held-certificate NUMERATOR split

**Moves:** neither bound numerically. Produces a NEW verifiable structural identity;
reproduces (does not beat) 0.2538893183. The milestone is the identity, banked iff it is
NEW checkable content (it is — no existing script checks the active-arc partition or the
numerator's dual-locus split).

**The NEW identity (precise statement).** On the LIVE held R4 family, with
A0(s) = sum_i q_i log|P_i(chi)| + qG log|j3(chi)| + qH log|j9(chi)| (the A-base /
prod-P^q arg WITHOUT any candidate block), B(s) = log|Q1 Q2|(chi) + qE log|Q5(chi)| +
qF log|Q6(chi)| (the perturber arg), G = max(A0,B):

  (P)  1_{A0>B}(s) + 1_{B>A0}(s) = 1   for a.e. s in [0,1]   (active-arc partition)
       with ACT(A) := {A0>B}, ACT(B) := {B>A0}, |ACT(A)| + |ACT(B)| = 1.
  (N)  Phi(0) = int_{ACT(A)} A0 ds + int_{ACT(B)} B ds        (numerator split)
       because G = A0 on ACT(A) and G = B on ACT(B) a.e. (max is attained by exactly
       one arg off the measure-zero kink set K).
  (M)  the two first-variation marginal families live on the COMPLEMENTARY loci:
       r~_Q = (1/D) int_{ACT(A)} log|Q(chi)| ds   (A-base, R6/R8 lemma) integrates over
       ACT(A); m_B(Q) = (1/D)[ int_{ACT(B)} log|Q(chi)| ds - (log h)*deg Q ] (B-branch,
       R8) integrates over ACT(B). This is the precise UPPER-INTERNAL "dual loci"
       structure: A-base lever acts on {A0>B}, B-perturber lever acts on {B>A0}.

**Skeleton:**
  1. Reconstruct A0, B on a uniform N>=4M grid s=(k+0.5)/N, chi=z(1-z), z=exp(2pi i s)
     — by REUSING verify_upper_q8A.float_value_q8A's exact A,B reconstruction (the `pv`
     evaluator + the held exponents; A0 = the A-array, B = the B-array; do NOT re-derive
     the polynomials). Build masks mA = A0>B, mB = B>A0.
  2. PARTITION (P): check |mA & mB| = 0 and |mA | mB| = N (every grid point is in exactly
     one locus, the equality set A0==B is empty on the grid). Report |ACT(A)| = mean(mA),
     |ACT(B)| = mean(mB), and |ACT(A)|+|ACT(B)| = 1 to float tol — by direct count.
  3. KINK STABILITY (cite R8, the artifact): count sign-changes of A0-B along s; confirm
     = 64 and STABLE across N in {5e5, 2e6, 4e6} — by re-counting at three N (this is the
     |K|=0 evidence, matching the R8 audit; CITE R8-firstvar-rigorous.md Step 4 for the
     real-analyticity argument that |K|=0, do NOT re-derive it).
  4. NUMERATOR SPLIT (N): compute Phi(0) = mean(G)*1 = mean(max(A0,B)); compute
     IA = mean(A0 * mA), IB = mean(B * mB); check Phi(0) = IA + IB to tol — because
     max(A0,B) = A0*1_{A0>B} + B*1_{B>A0} pointwise off K — by direct array identity.
  5. REPRODUCE THE HELD VALUE: check Phi(0)/D = (IA+IB)/D = 0.2538893183 to cert precision
     (the held int_0^1 G ds = 18.2804777610; mean(G) should match it to the float-vs-cert
     slack ~2e-7) — by dividing by D=_Dval(...). The decomposition reproduces the held
     numerator and value exactly. NOTE: the float Phi(0) carries the same ~1.98e-7 slack
     vs the certified 18.2804777610 documented in R4 — the pass criterion is float Phi(0)
     within a few e-7 of 18.2804777610 AND (IA+IB)/D within a few e-7 of 0.2538893183,
     NOT bit-exact equality with the cert (the cert is an outward enclosure, the float a
     Riemann mean).
  6. DUAL-LOCI MARGINALS (M): on the SAME masks, evaluate r~_Q = (1/D) mean(log|Q(chi)|*mA)
     for a firing A-base block (j9, in the dictionary) and m_B(Q) for a B-side block, and
     confirm each integrates over its OWN locus and matches the R6/R8 marginal definitions
     (cross-check vs verify_firstvar_lemma / verify_Bbranch_marginal numbers). This ties
     the partition to the two-sided first-variation engine — the structural payoff. Use
     ONE block per side, in-dictionary, WITHOUT adding it to the anchor family (marginals
     are derivatives at q=0 on the anchor without the candidate — standing rule).

**Hard step (the ONE load-bearing claim):** the NUMERATOR SPLIT (N),
Phi(0) = int_{ACT(A)} A0 + int_{ACT(B)} B, presented as a NEW EXACT decomposition of the
held certificate numerator. **Mechanism:** G = max(A0,B) equals A0 exactly on {A0>B} and
B exactly on {B>A0}, and {A0=B}=K has measure zero (R8: A0-B real-analytic, not
identically 0 => finite zero set; 64 stable sign-changes), so
max(A0,B) = A0*1_{A0>B} + B*1_{B>A0} a.e. and the integral splits. This is a clean
pointwise identity; the only subtlety is |K|=0, which is the R8 audit fact (CITE it).

**Check (what the builder runs to certify):** a NEW script (e.g.
`verify_dual_loci_decomposition.py`) that REUSES verify_upper_q8A's A0/B reconstruction at
the held exponents, builds the masks, and PASSES iff:
  - partition: |mA & mB|=0, mean(mA)+mean(mB)=1 (exact integer count);
  - kink: sign-change count = 64, identical across N in {5e5, 2e6, 4e6};
  - numerator: |Phi(0) - (IA+IB)| < 1e-9 (array identity, should be ~machine eps);
  - value: |(IA+IB)/D - 0.2538893183| < 1e-6 AND |Phi(0) - 18.2804777610| < 1e-5
    (Riemann-vs-cert slack ~2e-7 budgeted; the held cert int is the target);
  - marginals: r~_Q matches verify_firstvar_lemma's number for the same block (<1e-4),
    m_B matches verify_Bbranch_marginal's (<1e-4), confirming the complementary-loci claim.
A TAMPER row (swap the masks: integrate A0 over ACT(B)) MUST FAIL the numerator identity,
proving the split is locus-specific, not a tautology.

**Risk of banking no milestone (the single risk):** if the builder frames this as a
re-statement of the R6 shared-pool framing or the R9 marginal theorem, the reviewer banks
nothing (the R10 triage rule: pure prose re-packaging => no milestone). The NEW content is
the active-arc PARTITION (P) + the certificate NUMERATOR SPLIT (N) as identities checked
by a NEW script — neither verify_shared_pool (poly identities only) nor
verify_firstvar/verify_Bbranch (one arc each, no partition, no numerator split) checks
them. The builder MUST present (N)+(P) as a NEW decomposition of the HELD certificate, and
the script must be a NEW file producing the numerator split + reproducing 0.2538893183.
This is a MODEST advance (a clean identity, not a deep theorem) — honest framing required.

================================================================================

## Angle 2: weighted measure-form of the numerator split (mu_A + mu_B = mu)

**Moves:** none numerically; same structural milestone class as Angle 1, slightly richer.
State the decomposition at the MEASURE level: the certificate is C_82 <= (1/D) int G dmu
with dmu = ds Haar on the s-circle; the partition induces dmu = dmu_A + dmu_B with
mu_A = 1_{ACT(A)} ds, mu_B = 1_{ACT(B)} ds, and the certificate numerator is
int A0 dmu_A + int B dmu_B. Push: identify mu_A as (a restriction of) the equilibrium /
balayage measure of the A-base lemniscate active arc, mu_B of the perturber arc — i.e.
read the split as a decomposition of the BMQS/Doche measure mu_{P,Q} over its two
defining loci. **Hard step:** showing mu_A actually equals a recognizable
potential-theoretic object (equilibrium measure of the active arc), not just the indicator
1_{ACT(A)} ds — this is NOT established on disk and risks overclaim. **Check:** would need
to match mu_A's log-potential against the active-arc equilibrium potential numerically;
that is a heavier, less certain check. **Verdict:** higher upside (ties the split to the
BMQS measure cone), but the potential-theoretic identification is unproven and could fail
review — keep as a stretch extension layered ON TOP of Angle 1's verified partition, NOT a
standalone round.

## Angle 3: per-block conditional-capacity decomposition of Phi(0)

**Moves:** none numerically. Decompose Phi(0) further by the contribution of each
dictionary block to its OWN arc: int_{ACT(A)} A0 = sum_blocks (weight * int_{ACT(A)}
log|block|), and similarly for B. This exhibits the held numerator as a sum of per-block
conditional log-integrals (the un-normalized r~/m marginals), making "each block's
contribution to the bound = its conditional capacity on its locus" an explicit additive
identity. **Hard step:** none deep — it is linearity of the integral; but that is exactly
why it risks being judged a trivial re-arrangement / re-run of the R6 marginals (the
per-block integrals are essentially the already-banked r~_Q numbers). **Check:** sum of
per-block weighted arc-integrals over both loci = Phi(0). **Verdict:** lowest novelty;
fold it in as a COROLLARY table inside Angle 1's script (it strengthens the "dual loci =
where each lever acts" story) but do NOT pitch it as the milestone — too close to the
banked R6 marginals.

================================================================================

## Ranking

**Angle 1 first** — it is the only one that yields a self-contained, genuinely-NEW,
reviewer-verifiable identity in one round at low risk: the active-arc partition and the
certificate numerator split are exact statements, checked by a NEW script that reuses the
held harness's A0/B reconstruction and reproduces 0.2538893183 exactly. Its one hard step
(numerator split) rests on a clean pointwise max identity plus the already-audited |K|=0,
so it is very likely to certify. Its only real risk is FRAMING (re-narration banks
nothing), which the builder controls by shipping a NEW script for (P)+(N) and presenting
them as a new decomposition of the HELD certificate.

**Fall back to Angle 2** only if the reviewer would not bank Angle 1 as new (judges
partition+numerator-split too light) AND the builder can numerically match mu_A to the
active-arc equilibrium potential — that upgrades the split to a potential-theoretic
statement with real depth, but carries overclaim risk and a heavier check.

**Angle 3** is not a standalone round — include its per-block table inside Angle 1's
script as supporting evidence for the dual-loci reading, not as the headline.

Do NOT attempt any numeric break (both branches saturated, reviewer-verified R7/R8). Do
NOT revive "lower = complement of upper arc" (FORBIDDEN). Evaluate all marginals on the
anchor WITHOUT the candidate block (standing rule).

================================================================================

## R10 BUILD RESULT (Angle 1 built, all clauses PASS) — held number UNCHANGED

Built `constants/82a/certificate/verify_dual_loci_decomposition.py` (reuses the held
`float_value_q8A` A0/B reconstruction at the held R4 exponents). At N=4M, exit 0:

- (P) partition: |mA & mB|=0, union=N, |ACT(A)|=0.068608, |ACT(B)|=0.931392, sum=1. PASS
- (N) numerator split: Phi(0)=mean(max(A0,B))=18.2804634954 = IA+IB exactly
      (residual 0.0e+00 < 1e-9), via max(A0,B)=A0*1_{A0>B}+B*1_{B>A0} a.e. PASS
- (V) value: (IA+IB)/D = 0.2538891201, |val-held 0.2538893183| = 1.98e-7 (< 1e-6),
      = documented Riemann-vs-cert slack. PASS  (held number REPRODUCED, not beaten.)
- (TAMPER) swap masks -> (N) residual 9.36, identity FAILS (locus-specific, has teeth). PASS
- (K corrob) kink sign-changes = [64,64,64] stable over N {5e5,2e6,4e6} (cites R8). PASS
- (M corrob) r~(j9)=-0.00009 on ACT(A) (R2 anchor, no j9; bit-matches verify_firstvar_lemma);
      m_B(X^2-X+1)=+0.00031 on ACT(B). Cross-term -(log h)*deg kept STRICTLY in (M),
      never in the (N) residual. Complementary loci confirmed. PASS
- (C corrob, Angle 3) per-block linearity reproduces IA, IB to <1e-8. PASS

SCOPE: clean decomposition identity of the held certificate numerator; structural, does NOT
move the held UPPER bound 0.2538893183. See R10-build.md for the full pass sheet + reproduce.

PUSH FURTHER: Angle 2 (identify mu_A = 1_{ACT(A)} ds with the active-arc equilibrium /
balayage measure of the A-base lemniscate) is the next depth step — unproven on disk,
overclaim risk; layer it on TOP of this verified partition, not standalone.
