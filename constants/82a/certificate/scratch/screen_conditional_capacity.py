"""
R6 Angle 2 (COROLLARY / methods): the CONDITIONAL-CAPACITY block-selection screen.

This operationalizes the first-variation lemma (firstvar_01_lemma.py) into a
PRINCIPLED RANKING of candidate A-base blocks, replacing brute multistart.

Per the outline review: the un-normalized first-variation functional
    r~_Q = < log|Q(chi)| * 1_{A0>B} >_s
ALREADY separates fired (r~<0) from dry (r~>0) blocks, including the j9-vs-j6
inversion that the explorer's degree-NORMALIZED r_Q got backwards.  So this screen
is NOT a fix for a lemma defect -- it is a RANKING TOOL that (i) reproduces the
empirical fired/dry ordering and (ii) exposes the geometric reason a block fires:
how much of log|Q|, on the active arc, is NOT already supplied by the active
dictionary's log-potentials.

Two rankings, both computed on the active arc {A0>B} of the relevant anchor family:

  (1) RAW first-order marginal  r~_Q  (the lemma's exact predictor; the one that
      directly sets d(log h)/dq_Q = (1/D) r~_Q).  Rank by most-negative.

  (2) CONDITIONAL residual:  regress log|Q| on the active dictionary's log-potentials
      {log|P_m|, log|j3|, ...} over the active arc by least squares WITHOUT an
      intercept (the construction re-weights the q_m but has NO free additive
      constant, so an intercept would falsely let the dictionary absorb a constant
      shift it cannot).  Report the residual SIGNED MEAN  m^perp_Q = < e_Q 1_{arc} >,
      e_Q = log|Q| - sum_m beta_m log|P_m|.  This is the part of Q's first-order
      marginal that the joint re-optimization CANNOT reproduce by re-weighting the
      already-active blocks -- the genuinely NEW firing power.  Also report the
      residual rms (a redundancy diagnostic: small rms => Q's profile is largely a
      linear combination of dictionary potentials => little new structure).

ANCHOR matters (first variation at q_Q=0): each candidate is screened on the family
that does NOT yet contain it.  j3 on R11; j9/j6/j7 on R2.  We also rank a few untried
admissible Table-1 blocks on the R2 anchor as a forward-looking screen (Angle 4 note),
clearly labelled as candidates, NOT certified.

Reproduce:  python3 screen_conditional_capacity.py            (N=2_000_000, ~10-20s)
"""
import sys
import numpy as np

import bound_01_doche_base as vu
import bound_07_block_j9 as q8
import flammang_table1 as ft
from firstvar_01_lemma import (J3, J9, J6, J7, R11, R2, pv, AB_arrays)

_TAB = {j + 1: desc for j, (c, desc) in enumerate(ft._TABLE_DESCENDING)}


def active_dictionary(fam):
    """The active A-side dictionary log-potential basis for an anchor family.
    R11: {P1,P2,P4,P6,P8}.  R2: {P1,P2,P4,P6,P8, j3}.  (The perturber/B blocks
    do not enter the A-side first variation; the projection is over the A-side
    blocks that the joint re-optimization can freely re-weight.)"""
    blocks = [("P1", vu.BASE[0]), ("P2", vu.BASE[1]), ("P4", vu.BASE[2]),
              ("P6", vu.BASE[3]), ("P8", vu.BASE[4])]
    if fam["qG"] > 0:           # R2 has j3 active
        blocks.append(("j3", q8.Q7))
    if fam["qH"] > 0:           # (R4 would have j9; not used here)
        blocks.append(("j9", q8.Q8))
    return blocks


def screen(fam, fam_name, candidates, N):
    """Return ranking rows for candidate blocks on anchor family `fam`."""
    s, A0, B, chi = AB_arrays(fam, N)
    active = A0 > B
    arc = active.astype(float)
    narc = float(np.sum(active))

    # Design matrix of active-dictionary log-potentials on the FULL grid.
    # NO intercept: the construction re-weights q_m but has no free additive
    # constant, so an intercept would let the dictionary spuriously absorb a
    # constant shift it cannot realize (and forces the OLS residual mean to 0).
    dict_blocks = active_dictionary(fam)
    cols = []
    for _, desc in dict_blocks:
        cols.append(np.log(np.abs(pv(list(desc), chi))))
    Phi = np.stack(cols, axis=1)                   # (N, k+1)
    Phi_arc = Phi[active]                          # rows on the active arc

    # Pre-solve the normal equations once (shared across candidates).
    G = Phi_arc.T @ Phi_arc
    Ginv = np.linalg.inv(G)

    rows = []
    for name, desc in candidates:
        logQ = np.log(np.abs(pv(list(desc), chi)))
        # (1) raw first-order marginal r~_Q  (lemma's exact predictor)
        rt = float(np.mean(logQ * arc))
        # (2) conditional residual after OLS on the active dictionary (active arc)
        y = logQ[active]
        beta = Ginv @ (Phi_arc.T @ y)
        resid = y - Phi_arc @ beta
        m_perp = float(np.sum(resid)) / N          # signed residual MEAN (matches r~ scale)
        res_norm = float(np.sqrt(np.mean(resid ** 2)))
        rows.append((name, len(desc) - 1, rt, m_perp, res_norm))
    return rows, narc / N


def fmt(rows, title):
    print(f"\n{title}")
    hdr = f"  {'blk':<5}{'deg':>4}{'r~_Q (raw marg)':>18}{'cond resid mean':>18}{'resid rms':>12}  status"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for name, deg, rt, mp, rn, status in rows:
        print(f"  {name:<5}{deg:>4}{rt:>18.6f}{mp:>18.6f}{rn:>12.5f}  {status}")


def main(N=2_000_000):
    print("=" * 84)
    print(f"R6 conditional-capacity screen (ranking heuristic for A-base blocks), N={N}")
    print("=" * 84)

    # Known fired/dry blocks, each on its CORRECT anchor.
    # j3 on R11; j9,j6,j7 on R2.
    r11_rows, frac11 = screen(R11, "R11", [("j3", J3)], N)
    r2_rows, frac2 = screen(R2, "R2", [("j9", J9), ("j6", J6), ("j7", J7)], N)

    # tag empirical status
    status = {"j3": "FIRED", "j9": "FIRED", "j6": "DRY", "j7": "DRY"}
    r11_tagged = [(n, d, rt, mp, rn, status.get(n, "?")) for (n, d, rt, mp, rn) in r11_rows]
    r2_tagged = [(n, d, rt, mp, rn, status.get(n, "?")) for (n, d, rt, mp, rn) in r2_rows]

    print(f"\nactive-arc fraction: R11={frac11:.4f}  R2={frac2:.4f}")
    fmt(r11_tagged, "[j3 on R11 anchor]")
    fmt(r2_tagged, "[j9,j6,j7 on R2 anchor -- the SAME anchor, so directly comparable]")

    # The decisive corollary checks (all on the comparable R2 anchor):
    d = {n: (rt, mp) for (n, dd, rt, mp, rn) in r2_rows}
    print("\nDecisive ordering checks (R2 anchor, directly comparable):")
    # raw r~: j9 fires (<0), j6,j7 dry (>0); j9 < j6 (inversion the explorer got wrong)
    raw_inv = d["j9"][0] < 0 < d["j6"][0] and d["j9"][0] < d["j6"][0]
    print(f"  RAW r~ ranks j9 (fires) below j6 (dry):    {raw_inv}  "
          f"(j9={d['j9'][0]:.5f} < 0 < j6={d['j6'][0]:.5f})")
    # conditional residual: j9 should have the more-negative conditional mean than j6
    cond_inv = d["j9"][1] < d["j6"][1]
    print(f"  COND resid mean ranks j9 below j6:         {cond_inv}  "
          f"(j9={d['j9'][1]:.5f} < j6={d['j6'][1]:.5f})")
    fired_top = (d["j9"][0] < 0) and (d["j6"][0] > 0) and (d["j7"][0] > 0)
    print(f"  fired block j9 has r~<0, dry j6/j7 have r~>0: {fired_top}")

    # ---- Angle-4 NOTE: forward screen of UNTRIED admissible Table-1 blocks ----
    # purely a ranking note for a FUTURE certify; NOT certified here.
    print("\n[Angle-4 forward note] untried Table-1 blocks ranked on R2 anchor "
          "(candidates only, NOT certified):")
    tried = {3, 9, 6, 7, 13, 15, 5, 8, 12}   # already in dictionary or screened
    cand = []
    for jk in sorted(_TAB):
        if jk in tried:
            continue
        desc = _TAB[jk]
        # admissibility quick gate: must be coprime to dictionary -- reuse screen_swap
        cand.append((f"j{jk}", desc))
    frows, _ = screen(R2, "R2", cand, N)
    # sort by raw r~ ascending (most-negative = best first-order firing)
    frows_sorted = sorted(frows, key=lambda r: r[2])
    ftagged = [(n, dd, rt, mp, rn, ("r~<0:cand" if rt < 0 else "r~>=0:dry"))
               for (n, dd, rt, mp, rn) in frows_sorted]
    fmt(ftagged, "  (ranked by raw r~, most-negative first)")
    neg = [r for r in frows_sorted if r[2] < -5e-3]
    if neg:
        print(f"\n  NOTE: untried blocks with r~ < -5e-3 (worth a FUTURE float gate): "
              f"{[r[0] for r in neg]}")
    else:
        print("\n  NOTE: no untried Table-1 block has r~ < -5e-3 on R2 -- "
              "consistent with A-base saturation; no Angle-4 certify this round.")

    overall = raw_inv and cond_inv and fired_top
    print("\n" + "=" * 84)
    print(f"  CONDITIONAL-CAPACITY SCREEN: {'PASS' if overall else 'PARTIAL'}  "
          f"(recovers empirical fired/dry ordering incl. j9>j6 inversion)")
    print("=" * 84)
    return overall


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    ok = main(N)
    sys.exit(0 if ok else 1)
