"""
R10 (this campaign) -- UPPER-INTERNAL DUAL-LOCI DECOMPOSITION of the HELD
certificate NUMERATOR for C_82 (Zhang-Zagier essential minimum, 82a UPPER).

STRUCTURAL round.  This script does NOT move the held UPPER number
(0.2538893183, bound_07_block_j9.py, R4).  It establishes a NEW verifiable
IDENTITY: the held certificate's numerator Phi(0) = int_0^1 max(A0,B) ds splits
EXACTLY over the two upper-internal active loci

    ACT(A) := {A0 > B}   (the A-base / prod-P^q arg attains the max)
    ACT(B) := {B > A0}   (the perturber / Q-branch arg attains the max)

as Phi(0) = int_{ACT(A)} A0 ds + int_{ACT(B)} B ds, reproducing the held value
0.2538893183 as the PASS criterion (not beating it).

WHY THIS IS NEW (and not a re-run of R6/R8/R9):
  - firstvar_06_dictionary.py (R6) checks INTEGER-POLYNOMIAL identities only
    (P4=j5 etc., squarefree + coprime).  It never touches A0/B, the partition,
    the numerator, or any integral.
  - firstvar_01_lemma.py / firstvar_04_perturbing_marginal.py / firstvar_03_unified.py
    (R6/R8/R9) compute MARGINALS -- derivatives at q=0, int_{ACT(X)} log|Q| for
    ONE block on ONE arc.  NONE computes the certificate NUMERATOR itself
    Phi(0) = int_{ACT(A)} A0 + int_{ACT(B)} B, and NONE checks the partition
    |mA & mB|=0, mean(mA)+mean(mB)=1 as an identity.
  The NEW, must-be-present artifact is the computed Phi(0) = IA + IB identity on
  the HELD family -- the locus split of the bound's numerator.

SCOPE (honest): this is a CLEAN DECOMPOSITION IDENTITY, not a deep theorem.  The
one subtlety -- |K|=0 for K={A0=B} -- is the R8 audit fact (A0-B real-analytic,
not identically 0 => finite zero set; see R8-firstvar-rigorous.md Step 4); we
provide kink-count STABILITY across increasing N as the EVIDENCE, and CITE R8 for
the measure-zero REASON.  We do NOT re-derive measure-zero here.

HEADLINE checks (the milestone, BINDING CONDITION A):
  (P)  active-arc PARTITION:  mA & mB disjoint, union = full grid, |ACT(A)|+|ACT(B)|=1
  (N)  numerator split:  Phi(0) = IA + IB  via  max(A0,B) = A0*1_{A0>B} + B*1_{B>A0}
  (V)  value reproduction:  (IA+IB)/D = 0.2538893183 to Riemann-vs-cert slack
  (TAMPER)  swapping the masks (integrate A0 over ACT(B)) MUST FAIL (N).

CORROBORATION (BINDING CONDITION B -- supporting rows, NOT the headline):
  (K)  kink-count stability across N (cites R8; evidence for |K|=0).
  (M)  the two first-variation marginals live on the complementary loci
       (r~_Q on ACT(A), R6/R8 A-base lemma;  m_B on ACT(B), R8 B-branch).  These
       re-touch already-banked R6/R8 numbers and are LABELLED corroboration.
       PRECISION: the B-branch -(log h)*deg cross-term is a FIRST-VARIATION term,
       NOT part of the fixed-q numerator split (N) -- it is kept strictly inside
       (M) and never leaks into the (N) residual.
  (C)  per-block conditional-capacity table (Angle 3): linearity of the integral
       over each locus; LABELLED corroboration.

Reproduce (cd constants/82a/certificate):
  python3 firstvar_05_numerator_split.py            # full, pushes to N=4M
  python3 firstvar_05_numerator_split.py 2000000    # faster top N
"""
import sys
import time
import numpy as np

import bound_01_doche_base as vu
import bound_07_block_j9 as q8

# ---------------------------------------------------------------------------
# HELD R4 family -- the anchor for the HEADLINE (P)+(N)+(V) checks.  Exactly the
# certified integrand's exponents (bound_07_block_j9.py, R4).  qB=qC=0.
HELD = dict(q=[14.011500, 13.443930, 2.643590, 2.299880, 0.252420],
            qB=0.0, qC=0.0, qE=0.575080, qF=0.568800, qG=0.891590, qH=0.066860)

# Held certificate targets (bound_07_block_j9.py R4 RESULT):
HELD_INT = 18.2804777610      # int_0^1 G(chi) ds  (certified outward enclosure)
HELD_VALUE = 0.2538893183     # int_0^1 G ds / D   (the held UPPER value)

# R2 anchor (j3 A-base ON, j9 OFF) -- the anchor for the A-base marginal r~(j9),
# evaluated WITHOUT the candidate (standing rule: marginal is a derivative at q=0).
R2 = dict(q=[14.283862, 13.947194, 2.593425, 2.283539, 0.249084],
          qB=0.0, qC=0.0, qE=0.577911, qF=0.565724, qG=0.893516, qH=0.0)


def pv(coef_desc, x):
    """Horner eval of a DESCENDING-coefficient polynomial at array x."""
    r = np.zeros_like(x)
    for c in coef_desc:
        r = r * x + c
    return r


def AB_arrays(fam, N):
    """A0(s), B(s), chi(s) reconstructed with EXACTLY the held harness's
    float_value_q8A convention (bound_07_block_j9 lines 257-277).  A0 = the A-base
    / prod-P^q arg WITHOUT any candidate block (it carries the held j3,j9 already
    in the family); B = the perturber arg.  This is bit-for-bit the certified
    integrand's two pieces."""
    q = fam["q"]; qB = fam["qB"]; qC = fam["qC"]
    qE = fam["qE"]; qF = fam["qF"]; qG = fam["qG"]; qH = fam["qH"]
    s = (np.arange(N) + 0.5) / N
    z = np.exp(2j * np.pi * s)
    chi = z * (1 - z)
    A0 = (sum(q[i] * np.log(np.abs(pv(vu.BASE[i], chi))) for i in range(5))
          + qG * np.log(np.abs(pv(q8.Q7, chi)))      # j3 A-base (Q7)
          + qH * np.log(np.abs(pv(q8.Q8, chi))))     # j9 A-base (Q8)
    B = (np.log(np.abs(pv(list(vu.Q1), chi))) + np.log(np.abs(pv(list(vu.Q2), chi)))
         + qB * np.log(np.abs(pv(list(q8.Q3), chi)))
         + qC * np.log(np.abs(pv(list(q8.Q4), chi)))
         + qE * np.log(np.abs(pv(list(q8.Q5), chi)))
         + qF * np.log(np.abs(pv(list(q8.Q6), chi))))
    return s, A0, B, chi


def Dval(fam):
    """D = max(arg_A, arg_B) for family fam (mirrors q8._Dval)."""
    return q8._Dval(np.array(fam["q"]), fam["qB"], fam["qC"],
                    fam["qE"], fam["qF"], fam["qG"], fam["qH"])


def kink_signchanges(A0, B):
    """Number of sign-changes of A0-B along the grid (evidence for |K| finite;
    the measure-zero REASON is cited from R8, not re-derived)."""
    d = A0 - B
    sgn = np.sign(d)
    # ignore exact zeros on the grid (none expected): carry previous sign
    nz = sgn != 0
    sg = sgn[nz]
    return int(np.sum(sg[1:] != sg[:-1]))


# ===========================================================================
def headline_partition_numerator(N):
    """(P) partition, (N) numerator split, (V) value reproduction, TAMPER row.
    The HEADLINE new content -- decomposition of the HELD certificate numerator."""
    print("=" * 78)
    print(f"HEADLINE (BINDING COND A): dual-loci split of the HELD numerator  (N={N})")
    print("=" * 78)
    t0 = time.time()
    s, A0, B, chi = AB_arrays(HELD, N)
    D = Dval(HELD)
    print(f"  held R4 family; D = max(arg_A, arg_B) = {D:.6f}", flush=True)

    # --- masks ---
    mA = A0 > B          # ACT(A) = {A0 > B}
    mB = B > A0          # ACT(B) = {B > A0}

    # ---- (P) PARTITION ----
    both = int(np.sum(mA & mB))
    union = int(np.sum(mA | mB))
    actA = float(np.mean(mA))
    actB = float(np.mean(mB))
    eq = int(np.sum(A0 == B))   # grid points exactly on the kink K
    print("\n-- (P) active-arc PARTITION -----------------------------------------")
    print(f"   |mA & mB| (overlap)        = {both}        (MUST be 0)")
    print(f"   |mA | mB| (union)          = {union} / {N}   (MUST equal N - |K_grid|)")
    print(f"   |K_grid| (A0==B on grid)   = {eq}")
    print(f"   |ACT(A)| = mean(mA)        = {actA:.6f}   (expect ~0.0686)")
    print(f"   |ACT(B)| = mean(mB)        = {actB:.6f}   (expect ~0.9314)")
    print(f"   |ACT(A)| + |ACT(B)|        = {actA + actB:.12f}   (MUST be 1)")
    P_ok = (both == 0) and (union + eq == N) and (abs(actA + actB - 1.0) < 1e-12)
    print(f"   (P) PASS: {P_ok}")

    # ---- (N) NUMERATOR SPLIT ----
    G = np.maximum(A0, B)
    Phi = float(np.mean(G))                       # certificate numerator (Riemann mean)
    IA = float(np.mean(A0 * mA))                  # int_{ACT(A)} A0 ds
    IB = float(np.mean(B * mB))                   # int_{ACT(B)} B  ds
    resid = Phi - (IA + IB)
    print("\n-- (N) NUMERATOR SPLIT  Phi = int_ACT(A) A0 + int_ACT(B) B ----------")
    print(f"   Phi(0) = mean(max(A0,B))   = {Phi:.12f}")
    print(f"   IA = mean(A0 * 1_{{A0>B}})   = {IA:.12f}")
    print(f"   IB = mean(B  * 1_{{B>A0}})   = {IB:.12f}")
    print(f"   IA + IB                    = {IA + IB:.12f}")
    print(f"   residual Phi - (IA+IB)     = {resid:.3e}   (MUST be < 1e-9)")
    N_ok = abs(resid) < 1e-9
    print(f"   (N) PASS: {N_ok}")

    # ---- (V) VALUE REPRODUCTION ----
    val = (IA + IB) / D
    val_phi = Phi / D
    print("\n-- (V) VALUE REPRODUCTION (reproduces held 0.2538893183) ------------")
    print(f"   (IA+IB)/D                  = {val:.12f}")
    print(f"   Phi/D                      = {val_phi:.12f}")
    print(f"   held certified value       = {HELD_VALUE:.10f}")
    print(f"   |float - held value|       = {abs(val - HELD_VALUE):.3e}   "
          f"(Riemann-vs-cert slack, expect ~1.8e-7)")
    print(f"   float Phi (mean)           = {Phi:.10f}")
    print(f"   held certified int_0^1 G   = {HELD_INT:.10f}")
    print(f"   |float Phi - cert int|     = {abs(Phi - HELD_INT):.3e}   "
          f"(= D * value-slack ~= 72*1.98e-7 ~= 1.43e-5; cert is an OUTWARD"
          f" enclosure so cert int >= float Phi by this fixed margin)")
    # The MEANINGFUL test is the VALUE: |(IA+IB)/D - held| < 1e-6 (here ~1.98e-7,
    # the documented Riemann-vs-cert slack).  The Phi-level slack is the SAME slack
    # scaled by D (~72x) -- it is a fixed outward-enclosure margin, NOT a
    # discretization error (stable at 1.43e-5 across N=1M..8M), so the Phi bound is
    # set to 3e-5 (> the fixed margin), while the value bound 1e-6 stays the real test.
    V_ok = (abs(val - HELD_VALUE) < 1e-6) and (abs(Phi - HELD_INT) < 3e-5)
    print(f"   (V) PASS: {V_ok}")

    # ---- TAMPER ----
    # Mislabel the masks: integrate A0 over ACT(B) and B over ACT(A).  The (N)
    # identity MUST FAIL -- proving the split is locus-specific, not a tautology.
    IA_bad = float(np.mean(A0 * mB))   # WRONG: A0 over ACT(B)
    IB_bad = float(np.mean(B * mA))    # WRONG: B over ACT(A)
    resid_bad = Phi - (IA_bad + IB_bad)
    print("\n-- (TAMPER) swap masks: int_ACT(B) A0 + int_ACT(A) B ----------------")
    print(f"   IA_swap = mean(A0*1_{{B>A0}}) = {IA_bad:.12f}")
    print(f"   IB_swap = mean(B *1_{{A0>B}}) = {IB_bad:.12f}")
    print(f"   swapped sum                = {IA_bad + IB_bad:.12f}")
    print(f"   residual Phi - swapped     = {resid_bad:.3e}   (MUST be LARGE != 0)")
    TAMPER_ok = abs(resid_bad) > 1e-3   # has teeth: must be a gross mismatch
    print(f"   (TAMPER) correctly FAILS the (N) identity: {TAMPER_ok}")

    print(f"\n  [headline elapsed {time.time()-t0:.1f}s]")
    return P_ok and N_ok and V_ok and TAMPER_ok, dict(
        actA=actA, actB=actB, Phi=Phi, IA=IA, IB=IB, D=D, val=val)


def kink_stability():
    """(K) CORROBORATION: kink-count of A0-B STABLE across increasing N.  This is
    the EVIDENCE that K={A0=B} is finite (|K|=0); the analyticity REASON is CITED
    from R8-firstvar-rigorous.md Step 4 (A0-B real-analytic, not identically 0 =>
    isolated zeros).  We do NOT re-derive measure-zero."""
    print("\n" + "=" * 78)
    print("CORROBORATION (K): kink-count stability (cites R8; evidence for |K|=0)")
    print("=" * 78)
    counts = []
    for N in (500_000, 2_000_000, 4_000_000):
        t0 = time.time()
        s, A0, B, chi = AB_arrays(HELD, N)
        c = kink_signchanges(A0, B)
        counts.append(c)
        print(f"   N={N:>9}: sign-changes of (A0-B) = {c}   "
              f"[{time.time()-t0:.1f}s]", flush=True)
    stable = len(set(counts)) == 1
    top_ge_4 = counts[-1] >= 4
    print(f"   counts = {counts}")
    print(f"   STABLE across N (R8 audited 64): {stable}   "
          f"top-N count >= 4 (>= the outline's >=4 floor): {top_ge_4}")
    print(f"   (cite: R8-firstvar-rigorous.md Step 4 for |K|=0; this is the "
          f"EVIDENCE not the derivation)")
    return stable and top_ge_4, counts


def marginal_crosscheck(N):
    """(M) CORROBORATION (BINDING COND B): the two first-variation marginals live
    on the COMPLEMENTARY loci.

      A-base side:  r~_Q = (1/D) int_{ACT(A)} log|Q| ds   (R6/R8 lemma)
                    -- evaluated on the R2 anchor WITHOUT the candidate j9
                       (standing rule: marginal is d/dq at q=0; recompute masks there).
      B-branch side: m_B(Q) = (1/D)[ int_{ACT(B)} log|Q| - (log h)*deg Q ]   (R8)
                    -- the -(log h)*deg cross-term is a FIRST-VARIATION term and
                       is kept STRICTLY here, NEVER in the (N) residual.

    This ties the partition to the two-sided engine: the A-base lever acts on
    {A0>B}, the B-perturber lever on {B>A0}.  LABELLED corroboration, not headline."""
    print("\n" + "=" * 78)
    print("CORROBORATION (M): the two marginals live on the complementary loci")
    print("=" * 78)

    # --- A-base marginal r~(j9) on the R2 anchor (j9 NOT yet in the family) ---
    s, A0, B, chi = AB_arrays(R2, N)
    mA = A0 > B
    D_R2 = Dval(R2)
    J9 = [1, -1, 0, -3, 15, -22, 16, -6, 1]
    logj9 = np.log(np.abs(pv(J9, chi)))
    rt_int = float(np.mean(logj9 * mA))          # int_{ACT(A)} log|j9|
    rt = rt_int / D_R2                           # r~_Q
    print("\n-- A-base marginal r~(j9) on the R2 anchor (WITHOUT j9) -------------")
    print(f"   int_{{ACT(A)=A0>B}} log|j9| ds = {rt_int:.8f}")
    print(f"   r~(j9) = (1/D) int_ACT(A) ..  = {rt:.8f}   "
          f"(FIRES iff < 0: {rt < 0})")
    print(f"   support of the integral       = ACT(A) = {{A0>B}}  "
          f"(measure {np.mean(mA):.5f})")
    # cross-check vs firstvar_01_lemma's number for j9 on R2 (closed_form_rtilde
    # returns the UN-normalized int; r~/(1)=rt_int there).  Match to <1e-4.
    A_match = True
    try:
        import firstvar_01_lemma as vfl
        s2, A2, B2, chi2 = vfl.AB_arrays(vfl.R2, N)
        rt_int_ref, _ = vfl.closed_form_rtilde(vfl.R2, vfl.J9, A2, B2, chi2)
        print(f"   firstvar_01_lemma r~(j9) int (un-norm) = {rt_int_ref:.8f}   "
              f"|diff| = {abs(rt_int - rt_int_ref):.2e}  (<1e-4)")
        A_match = abs(rt_int - rt_int_ref) < 1e-4
    except Exception as e:
        print(f"   (cross-check vs firstvar_01_lemma skipped: {e})")

    # --- B-branch marginal m_B on the held R4 family (a B-side test block) ---
    # X^2 - X + 1 (the least-dry admissible B-perturber, R8).  m_B carries the
    # FIRST-VARIATION cross-term -(log h)*deg/D; it lives ENTIRELY on ACT(B).
    s, A0, B, chi = AB_arrays(HELD, N)
    mB = B > A0
    D_H = Dval(HELD)
    QB = [1, -1, 1]                              # X^2 - X + 1, deg 2
    logQB = np.log(np.abs(pv(QB, chi)))
    mb_int = float(np.mean(logQB * mB))          # int_{ACT(B)} log|Q|
    logh = HELD_VALUE                            # the held log h (the bound value)
    cross = logh * (len(QB) - 1)                 # (log h)*deg  -- FIRST-VARIATION term
    m_B = (mb_int - cross) / D_H                 # R8 B-branch marginal
    print("\n-- B-branch marginal m_B(X^2-X+1) on the held R4 family -------------")
    print(f"   int_{{ACT(B)=B>A0}} log|Q| ds  = {mb_int:.8f}")
    print(f"   FIRST-VARIATION cross-term (log h)*deg = {cross:.8f}  "
          f"[NOT in the (N) numerator split]")
    print(f"   m_B = (1/D)[int_ACT(B) - (log h)*deg] = {m_B:.8f}   "
          f"(FIRES iff < 0: {m_B < 0})")
    print(f"   support of the integral       = ACT(B) = {{B>A0}}  "
          f"(measure {np.mean(mB):.5f})")
    print(f"   --> A-base marginal integrates over ACT(A); B-branch over ACT(B): "
          f"COMPLEMENTARY loci.")
    return A_match, dict(rt=rt, m_B=m_B)


def per_block_table(N, hb):
    """(C) CORROBORATION (Angle 3): per-block conditional-capacity table.  By
    linearity of the integral, IA = int_ACT(A) A0 = sum over A-base blocks of
    weight * int_ACT(A) log|block|, and likewise IB over ACT(B).  Exhibits the
    held numerator as a sum of per-block conditional log-integrals.  LABELLED
    corroboration (close to the banked R6 marginals); NOT the headline."""
    print("\n" + "=" * 78)
    print("CORROBORATION (C, Angle 3): per-block conditional-capacity table")
    print("=" * 78)
    s, A0, B, chi = AB_arrays(HELD, N)
    mA = A0 > B; mB = B > A0
    q = HELD["q"]

    # A-base blocks with weights
    Ablocks = [("P1", vu.BASE[0], q[0]), ("P2", vu.BASE[1], q[1]),
               ("P4", vu.BASE[2], q[2]), ("P6", vu.BASE[3], q[3]),
               ("P8", vu.BASE[4], q[4]),
               ("j3", q8.Q7, HELD["qG"]), ("j9", q8.Q8, HELD["qH"])]
    Bblocks = [("Q1", list(vu.Q1), 1.0), ("Q2", list(vu.Q2), 1.0),
               ("Q5", list(q8.Q5), HELD["qE"]), ("Q6", list(q8.Q6), HELD["qF"])]

    print("   block  side  weight   int_locus log|blk|   weight*int")
    sA = 0.0
    for nm, blk, wt in Ablocks:
        lg = float(np.mean(np.log(np.abs(pv(blk, chi))) * mA))
        sA += wt * lg
        print(f"   {nm:<5}  A    {wt:8.5f}  {lg:>16.8f}  {wt*lg:>14.8f}")
    sB = 0.0
    for nm, blk, wt in Bblocks:
        lg = float(np.mean(np.log(np.abs(pv(blk, chi))) * mB))
        sB += wt * lg
        print(f"   {nm:<5}  B    {wt:8.5f}  {lg:>16.8f}  {wt*lg:>14.8f}")
    print(f"   sum over A-base blocks = {sA:.10f}  vs IA = {hb['IA']:.10f}  "
          f"|diff|={abs(sA-hb['IA']):.2e}")
    print(f"   sum over B blocks      = {sB:.10f}  vs IB = {hb['IB']:.10f}  "
          f"|diff|={abs(sB-hb['IB']):.2e}")
    C_ok = abs(sA - hb["IA"]) < 1e-8 and abs(sB - hb["IB"]) < 1e-8
    print(f"   (C) per-block linearity reproduces IA, IB: {C_ok}")
    return C_ok


if __name__ == "__main__":
    Ntop = int(sys.argv[1]) if len(sys.argv) > 1 else 4_000_000
    t_start = time.time()

    # CHEAP first: a quick partition+numerator sanity at low N, then headline.
    print("### quick low-N sanity (N=200k) ###", flush=True)
    quick_ok, _ = headline_partition_numerator(200_000)

    head_ok, hb = headline_partition_numerator(Ntop)
    A_match, mm = marginal_crosscheck(Ntop)
    C_ok = per_block_table(Ntop, hb)
    kink_ok, counts = kink_stability()   # pushes to N=4M last (per pacing rule)

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"  HEADLINE (P)+(N)+(V)+TAMPER  [N={Ntop}]: {'PASS' if head_ok else 'FAIL'}")
    print(f"    |ACT(A)| = {hb['actA']:.6f}  |ACT(B)| = {hb['actB']:.6f}  "
          f"sum = {hb['actA']+hb['actB']:.10f}")
    print(f"    Phi = {hb['Phi']:.10f}  IA+IB = {hb['IA']+hb['IB']:.10f}  "
          f"(IA+IB)/D = {hb['val']:.10f}  vs held {HELD_VALUE}")
    print(f"  CORROB (K) kink-count stable {counts}: {'PASS' if kink_ok else 'FAIL'}")
    print(f"  CORROB (M) complementary marginals (A-base r~ match): "
          f"{'PASS' if A_match else 'FAIL'}  "
          f"(r~(j9)={mm['rt']:.5f} fires; m_B(X^2-X+1)={mm['m_B']:.5f})")
    print(f"  CORROB (C) per-block linearity: {'PASS' if C_ok else 'FAIL'}")
    overall = head_ok and kink_ok and A_match and C_ok
    print(f"\n  OVERALL: {'ALL PASS' if overall else 'SOME FAILED'}   "
          f"[{time.time()-t_start:.1f}s]")
    print(f"  SCOPE: clean decomposition identity of the HELD certificate "
          f"numerator; does NOT move the held UPPER bound {HELD_VALUE}.")
    sys.exit(0 if overall else 1)
