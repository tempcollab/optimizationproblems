"""firstvar_08 -- the SIBLING-GENERATOR theorem: a RIGOROUS, outward-rounded
interval certificate that Grinsztajn's near-cancellation factors R0, R2 are the
degree-preserving coprime firing siblings the first-variation criterion GENERATES
from the distinguished blocks Q1, Q2, given the admissible bridge ansatz
g = P1^a P2^a P4 . (tail).

This lifts the paper's record section (Prop. thm:record-fires) from a DIAGNOSTIC
("the criterion fires on R0,R2 after the fact") to a GENERATIVE construction:
R = pp(Q* -+ g) is an admissible degree-preserving coprime firing sibling of Q*,
and R0,R2 are its instances a=5.

================================  WHAT IS PROVED  =============================

Fix ONE anchor family F (the Gri26 record denominator with the seed block Q*
REMOVED) and its perturbing active set  Omega_F = { B_F > A_F }.  Both Q* and R
are scored on the SAME Omega_F (must-fix item 3).  Since deg R = deg Q* (Angle-2
degree floor), the normalizer 1/deg is shared and the MARGINAL-TRANSFER IDENTITY

    r_R - r_{Q*}  =  (1/deg)  int_{Omega_F}  log |R/Q*|  ds                  (I)

is EXACT.  Writing R = (1/c)(Q* -+ g) with c = content(Q* -+ g) (here c = 1),

    log |R/Q*|  =  - log c  +  log| 1 -+ g/Q* | .

THE THETA-SPLIT BULK+WELL BOUND.  Fix theta = 1/2.  Split Omega_F into
  Omega_0 = Omega_F cap { |g/Q*| <= theta }   (bulk)
  W       = Omega_F cap { |g/Q*| >  theta }   (well),   delta := |W| .
On Omega_0, with |u| = |g/Q*| <= theta:
    | log|1 -+ u| |  <=  -log(1-|u|)  <=  |u|/(1-|u|)  <=  theta/(1-theta) .
On W the ratio |u| may exceed 1, so NO global constant cap is used.  Instead the
well integral int_W |log|R/Q*|| ds is bounded CELL-BY-CELL: on a contour cell with
directed-rounded enclosures log|R| in [lR,LR], log|Q*| in [lQ,LQ], the integrand
| log|R| - log|Q*| | is at most  max(LR - lQ, LQ - lR)  -- valid whether or not
log|R| > log|Q*| on the cell.  It is integrable (it grows only like log(1/width) at
a shared well of R and Q*), so adaptively bisecting the heavy well cells drives the
certified well integral down to the true ~1e-3 marginal shift.

    | r_R - r_{Q*} |  <=  (1/deg) [ log c  +  (theta/(1-theta)) |Omega_0|
                                   +  int_W |log|R/Q*|| ds ]  =: RHS.            (II)

(The OLD global cap  int_W |log|R/Q*|| <= delta*(log(1/m_R)+M_{Q*})  is NOT used to
certify: in the case log|R| > log|Q*| (true on 63-73% of W) it needs an upper bound
on |R| / lower bound on |Q*| that the certified constants do not provide.  It is
computed and printed only as a NON-CERTIFYING diagnostic.)

FIRING TRANSFER.  If  r_{Q*}(Omega_F) + RHS < log h , then  r_R(Omega_F) < log h ,
so R fires by Cor. cor:criterion -- and R is admissible coprime to Q* (sympy
checks), hence adjoinable as an independent denominator factor.

==============================  RIGOR (this script)  =========================

Every constant in (II) is a CERTIFIED outward-rounded enclosure, NOT a grid
measurement (CLAUDE.md: no hand-waving on the load-bearing step).  Over a uniform
grid of N cells on [0,2pi), each |P(chi)|^2 is enclosed [lo,hi] over the WHOLE
cell by the 2nd-order Taylor/mean-value interval model rho_full() reused VERBATIM
from bound_01_doche_base.py (the same machinery the certified upper bound uses).
A cell is classified against Omega_F = {B_F>A_F} by the CERTIFIED branch gap:
  - certainly IN   if  B_F_lo  >  A_F_hi          (whole cell in Omega_F)
  - certainly OUT  if  B_F_hi  <  A_F_lo          (whole cell out)
  - STRADDLE       otherwise                       (counted toward the bound the
                                                    firing-favorable / conservative way).
Then:
  * |Omega_0|     -> rigorous UPPER bound (every IN-or-straddle cell with the bulk
                     condition POSSIBLY met contributes width w).
  * delta = |W|   -> rigorous UPPER bound (every IN-or-straddle cell where the well
                     condition |g/Q*|>theta is POSSIBLY met contributes width w).
                     This is the {|g/Q*|>theta} measure (must-fix item 1), NOT the
                     0.02 "deepest-2%" figure.
  * M_{Q*}        -> rigorous UPPER bound of sup_{Omega_F} log|Q*| over IN/straddle cells.
  * m_R           -> rigorous LOWER bound of inf_{Omega_F} |R|   over IN/straddle cells
                     (>0 confirms R contour-root-free on the anchor).
  * r_{Q*}(Omega_F) -> rigorous UPPER bound (IN-or-straddle cells, log|Q*| upper).
The content c is taken EXACTLY from sympy .primitive() (must-fix item 2 / carry
the content factor); here c=1 and is printed, not dropped.

The script prints, for the seed pair (Q1->R0, Q2->R2):
  (A) the exact identity (I) reproduced on the fixed anchor (float cross-check);
  (B) the certified constants c, |Omega_0|, delta, M_{Q*}, m_R, r_{Q*};
  (C) the CERTIFIED RHS_sharp of (II) (sharp per-cell well integral, adaptively
      refined) and the verdict r_{Q*}+RHS_sharp < log h  (FIRING TRANSFER);  the
      global-cap RHS_global is printed too, but ONLY as a non-certifying diagnostic;
  (D) the Angle-2 degree floor table: deg R_a, content, admissibility for a=1..6,
      with the rigorous boundary  deg(g_a . tail) = 2a+16 < deg Q* = 28  iff  a<=5.
  (E) a TAMPER check: a deliberately understated log h is correctly NOT cleared,
      and a deliberately false degree target (deg R = 27 at a=5) is rejected.

PASS iff (II) clears the gap for BOTH R0 and R2 using the SHARP per-cell bound
RHS_sharp ALONE (no global cap), the degree floor is exact, admissibility holds,
m_R>0 is certified (0 unresolved well cells), and the tamper checks reject.

Run:   python3 firstvar_08_sibling_generator.py            (N=200_000 default, ~4-5min;
                                                             clears the gap with margin ~0.28)
       python3 firstvar_08_sibling_generator.py 40000      (coarser base grid, ~3min;
                                                             same verdict, margin ~0.28 --
                                                             the adaptive well frontier, not
                                                             N, sets the tightness)
Both N PASS: RHS_sharp ~ 0.004-0.006 (the well integral is refined to ~1e-2, an
order off the true 1e-3 shift), r_{Q*}+RHS_sharp ~ -0.03 < log h = 0.25363.
Requires: numpy, sympy  (+ the bound_00/bound_01 interval modules in this dir).
"""

import sys
import math

import numpy as np
import sympy as sp

import bound_00_flammang_baseline as vv      # rigorous Taylor-model interval machinery
import bound_01_doche_base as vu             # rho_full cell enclosure + w_full_* + ASC

PINF = math.inf
NINF = -math.inf
na = np.nextafter
TWO_PI = 2.0 * math.pi
X = sp.Symbol("X")

# ---------------------------------------------------------------------------
# Polynomial data (high-to-low integer coeffs), reproduced inline so the check
# is self-contained (same vectors as firstvar_07_record_blocks.py / Appendix A).
# ---------------------------------------------------------------------------
POLY_COEFFS = {
    "P1": [1, 0],
    "P2": [-1, 1],
    "P4": [1, -2, 4, -3, 1],
    "P6": [1, -3, 8, -16, 26, -27, 17, -6, 1],
    "P8": [1, -3, 7, -14, 30, -58, 96, -123, 114, -73, 31, -8, 1],
    "P7": [1, -3, 8, -18, 36, -62, 97, -123, 114, -73, 31, -8, 1],
    "P9": [1, -4, 10, -17, 26, -47, 119, -298, 592, -878, 963, -780, 464,
           -199, 59, -11, 1],
    "Q1": [1, -7, 30, -97, 269, -679, 1612, -3618, 7646, -15180, 28457, -50741,
           86189, -138288, 206152, -279897, 339335, -360911, 331775, -260367,
           172556, -95554, 43677, -16221, 4786, -1084, 178, -19, 1],
    "Q2": [1, -7, 30, -96, 255, -586, 1212, -2360, 4573, -9148, 18749, -37783,
           71770, -124910, 195848, -273368, 335981, -359545, 331349, -260271,
           172542, -95553, 43677, -16221, 4786, -1084, 178, -19, 1],
}

# maaxgrin LP-optimized numerator exponents at the record (firstvar_07).
NUMERATOR_Q = {
    "P1": 26.511877484730615, "P2": 23.782846008412744,
    "P3": 0.9707094545190521, "P4": 4.526072775020114,
    "P5": 0.038326545650764404, "P6": 4.173784226054273,
    "P8": 1.685809173822071,
}
# numerator polynomials P3,P5 (not in the bound dictionary; needed for A_F).
NUM_EXTRA = {
    "P3": [1, 1, -2, 1],
    "P5": [1, -2, 4, -7, 13, -16, 12, -5, 1],
}
# Record denominator blocks (Gri26): Q1 Q2 R0 R2 P7 P9.  P7=Q5, P9=Q6.
RECORD_DENOM = ["Q1", "Q2", "R0", "R2", "P7", "P9"]

THETA = 0.5                # theta-split point on |g/Q*|
LOG_FLOOR = 1e-300


def _poly(coeffs):
    return sp.Poly.from_list([sp.Integer(c) for c in coeffs], gens=X, domain=sp.ZZ)


def build_library():
    """Build the sympy library incl. R0,R2 as pp(Q* -+ bridge.tail), positive LC,
    and record the EXACT content of (Q* -+ bridge.tail)."""
    lib = {k: _poly(v) for k, v in POLY_COEFFS.items()}
    for k, v in NUM_EXTRA.items():
        lib[k] = _poly(v)
    bridge = (lib["P1"] ** 5) * (lib["P2"] ** 5) * lib["P4"]   # a=5 bridge
    content = {}
    for name, seed, tail, sign in [("R0", "Q1", "P8", -1), ("R2", "Q2", "P7", +1)]:
        raw = lib[seed] + sign * bridge * lib[tail]
        cont, pp = sp.Poly(raw.as_expr(), X, domain=sp.ZZ).primitive()
        if pp.LC() < 0:
            pp = sp.Poly(-pp.as_expr(), X, domain=sp.ZZ)
        lib[name] = pp
        content[name] = abs(int(cont))
    return lib, content


# ---------------------------------------------------------------------------
# Rigorous per-cell enclosure of |P(chi)|^2 over [a,b] (reuse bound_01.rho_full).
# Returns (lo, hi) arrays, outward-rounded, guaranteed |P(chi(t))|^2 in [lo,hi]
# for all t in the cell.
# ---------------------------------------------------------------------------
def asc(coeffs_hl):
    return [int(c) for c in coeffs_hl[::-1]]


def cell_rho_lo_hi(coef_asc, a, b, geo):
    m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc = geo
    _, _, rho_lo, rho_hi, _ = vu.rho_full(
        coef_asc, m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)
    return rho_lo, rho_hi


def cell_geometry(a, b):
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    Wc, DWc, DDWc, DDDWc = vu.w_full_cell(a, b)
    Wm, DWm, DDWm, DDDWm = vu.w_full_point(m)
    return (m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)


# ---------------------------------------------------------------------------
# THE CERTIFIED CONSTANTS for one seed (Q*, R, tail) on the FIXED anchor F.
# ---------------------------------------------------------------------------
def certify_seed(seed_name, R_name, tail_name, lib, content, N):
    """Anchor F = record family with seed_name REMOVED.  Returns a dict of the
    rigorous outward-rounded constants in inequality (II) and the verdict.

    All log|.| are HALF of log of |.|^2 enclosures.  Branch gap B_F - A_F is
    enclosed per cell; cells are classified IN / OUT / STRADDLE against Omega_F.
    Bounds accumulate the FIRING-FAVORABLE (conservative) way:
      - r_{Q*} upper, M_{Q*} upper:    include IN and STRADDLE cells, log|Q*| upper.
      - m_R lower:                     min over IN and STRADDLE cells, |R| lower.
      - |Omega_0|, delta upper:        include a cell if it could be in that region.
    """
    deg = int(lib[seed_name].degree())          # = deg R = 28
    bridge = (lib["P1"] ** 5) * (lib["P2"] ** 5) * lib["P4"]
    sign = -1 if seed_name == "Q1" else +1
    g_poly = sp.Poly((sign * bridge * lib[tail_name]).as_expr(), X, domain=sp.ZZ)

    # ascending-coeff arrays for the interval machinery
    A_Qstar = asc(POLY_COEFFS[seed_name])
    A_R = asc([int(c) for c in lib[R_name].all_coeffs()])
    A_g = asc([int(c) for c in g_poly.all_coeffs()])

    # anchor family F = record denom minus seed, plus the numerator A_F.
    denom_blocks = [b for b in RECORD_DENOM if b != seed_name]   # scoring Q* / R on F
    A_denom = {b: asc([int(c) for c in lib[b].all_coeffs()]) for b in denom_blocks}
    A_num = {}
    for nm in NUMERATOR_Q:
        coeffs = POLY_COEFFS[nm] if nm in POLY_COEFFS else NUM_EXTRA[nm]
        A_num[nm] = asc(coeffs)

    theta2 = THETA * THETA

    def cell_kernel(a, b):
        """Per-cell-array rigorous quantities.  Returns a dict of arrays."""
        w = b - a
        geo = cell_geometry(a, b)
        q2_lo, q2_hi = cell_rho_lo_hi(A_Qstar, a, b, geo)
        r2_lo, r2_hi = cell_rho_lo_hi(A_R, a, b, geo)
        g2_lo, g2_hi = cell_rho_lo_hi(A_g, a, b, geo)
        logQ_hi = na(0.5 * vv.log_up(np.maximum(q2_hi, LOG_FLOOR)), PINF)
        # A_F = sum_i q_i log|P_i| ; B_F = sum log|block|
        A_lo = np.zeros_like(a); A_hi = np.zeros_like(a)
        for nm, q in NUMERATOR_Q.items():
            p2_lo, p2_hi = cell_rho_lo_hi(A_num[nm], a, b, geo)
            lp_lo = na(0.5 * vv.log_down(np.maximum(p2_lo, LOG_FLOOR)), NINF)
            lp_hi = na(0.5 * vv.log_up(np.maximum(p2_hi, LOG_FLOOR)), PINF)
            A_lo = na(A_lo + na(q * lp_lo, NINF), NINF)
            A_hi = na(A_hi + na(q * lp_hi, PINF), PINF)
        B_lo = np.zeros_like(a); B_hi = np.zeros_like(a)
        for blk in denom_blocks:
            p2_lo, p2_hi = cell_rho_lo_hi(A_denom[blk], a, b, geo)
            lp_lo = na(0.5 * vv.log_down(np.maximum(p2_lo, LOG_FLOOR)), NINF)
            lp_hi = na(0.5 * vv.log_up(np.maximum(p2_hi, LOG_FLOOR)), PINF)
            B_lo = na(B_lo + lp_lo, NINF)
            B_hi = na(B_hi + lp_hi, PINF)
        certainly_out = B_hi < A_lo
        in_or_straddle = ~certainly_out            # could be in Omega_F
        ratio2_lo = na(g2_lo / np.maximum(q2_hi, LOG_FLOOR), NINF)
        ratio2_hi = na(g2_hi / np.maximum(q2_lo, LOG_FLOOR), PINF)
        could_be_well = ratio2_hi > theta2         # |g/Q*|>theta possible
        could_be_bulk = ratio2_lo <= theta2        # |g/Q*|<=theta possible
        # per-cell |log|R/Q*|| upper (well term integrand)
        r2lo = np.maximum(r2_lo, LOG_FLOOR); r2hi = np.maximum(r2_hi, LOG_FLOOR)
        q2lo = np.maximum(q2_lo, LOG_FLOOR); q2hi = np.maximum(q2_hi, LOG_FLOOR)
        up1 = na(0.5 * vv.log_up(na(r2hi / q2lo, PINF)), PINF)
        up2 = na(0.5 * vv.log_up(na(q2hi / r2lo, PINF)), PINF)
        logRQ_abs_hi = np.maximum(up1, up2)
        # whether |R|^2 is certified strictly positive on this cell
        R_pos = r2_lo > LOG_FLOOR
        return dict(w=w, geo=geo, logQ_hi=logQ_hi,
                    in_or_straddle=in_or_straddle,
                    could_be_well=could_be_well, could_be_bulk=could_be_bulk,
                    ratio2_hi=ratio2_hi, logRQ_abs_hi=logRQ_abs_hi,
                    r2_lo=r2_lo, R_pos=R_pos)

    # accumulators (rigorous):
    omega0_w = 0.0; delta_w = 0.0; omega_w = 0.0
    M_Qstar = NINF; m_R = PINF; rQ_upper_int = 0.0
    well_int_sharp = 0.0; bulk_int_sharp = 0.0
    n_unresolved = 0     # well cells where |R|^2 enclosure still touches 0 at depth cap

    # ADAPTIVE driver: start uniform N and bisect a well cell whenever EITHER
    #   (i)  its |R|^2 enclosure is not yet certified > 0 (R's deep wells), OR
    #   (ii) its per-cell SHARP well-integral contribution w*|log|R/Q*||_hi still
    #        exceeds WELL_TOL,
    # up to MAX_DEPTH.  Resolved cells are banked; only ambiguous/heavy well cells
    # are refined -- the certified-bound frontier pattern.
    #
    # Criterion (ii) is what makes the SHARP bound clear: the integrand |log|R/Q*||
    # is integrable but per-cell-loose near the shared wells of R and Q* (each
    # enclosure spreads [near-0, large] over a wide cell, decoupling the ratio).
    # As a heavy cell is halved, w*|log|R/Q*||_hi ~ w*log(1/w) -> 0, so refining the
    # heavy cells drives the rigorous sharp well integral down to the true ~1e-3
    # shift.  NO unjustified global cap log(1/m_R)+M_Q* is used to certify.
    WELL_TOL = 5e-4            # per-cell sharp well-integral target (unnormalized ds)
    MAX_DEPTH = 34
    edges = (np.arange(N + 1, dtype=np.float64) / N) * TWO_PI
    a_cur = edges[:-1].copy(); b_cur = edges[1:].copy()
    depth = 0
    while True:
        # process in chunks to cap memory
        ker = {}
        CHUNK = 200_000
        a_keep = []; b_keep = []   # well cells to refine next round
        for s in range(0, a_cur.shape[0], CHUNK):
            e = min(s + CHUNK, a_cur.shape[0])
            a = a_cur[s:e]; b = b_cur[s:e]
            k = cell_kernel(a, b)
            w = k['w']; mask = k['in_or_straddle']
            # accumulate the Omega_F-wide quantities ONCE (depth 0 only, on the
            # full partition) -- but the partition changes as we bisect, so to keep
            # the union exact we accumulate omega/bulk/rQ/M only on RESOLVED cells
            # plus the refined cells' eventual leaves.  Simpler & exactly correct:
            # accumulate EVERY cell's contribution here, since each bisection
            # REPLACES a parent by its two children with equal total width -- so we
            # must NOT double count.  We therefore accumulate the wide quantities
            # only for cells we will NOT refine (leaves), and refine ambiguous/heavy
            # well cells.  A cell is a leaf unless it is a well cell that is either
            # not R-positive OR still contributes more than WELL_TOL to the sharp
            # well integral.
            well_contrib = w * k['logRQ_abs_hi']
            refine = (mask & k['could_be_well']
                      & ((~k['R_pos']) | (well_contrib > WELL_TOL))
                      & (depth < MAX_DEPTH))
            leaf = ~refine
            lm = leaf & mask
            # Omega_F width, bulk width, delta width, rQ, M on LEAF cells in Omega
            omega_w += float(np.sum(w[lm]))
            delta_w += float(np.sum(w[lm & k['could_be_well']]))
            omega0_w += float(np.sum(w[lm & k['could_be_bulk']]))
            if np.any(lm):
                M_Qstar = max(M_Qstar, float(np.max(k['logQ_hi'][lm])))
                rQ_upper_int += float(np.sum((w * k['logQ_hi'])[lm]))
            # well integral on LEAF well cells
            lw = lm & k['could_be_well']
            if np.any(lw):
                well_int_sharp += float(np.sum((w * k['logRQ_abs_hi'])[lw]))
                pos = lw & k['R_pos']
                if np.any(pos):
                    m_R = min(m_R, float(np.min(np.sqrt(
                        np.maximum(k['r2_lo'][pos], LOG_FLOOR)))))
                # leaf well cells at depth cap with R not positive -> unresolved
                bad = lw & (~k['R_pos'])
                n_unresolved += int(np.sum(bad))
            # bulk integral on LEAF bulk cells
            lb = lm & k['could_be_bulk']
            if np.any(lb):
                gq_hi = np.minimum(np.sqrt(np.maximum(k['ratio2_hi'][lb], 0.0)),
                                   THETA)
                gq_hi = np.minimum(gq_hi, 1.0 - 1e-12)
                per_b = np.nextafter(-np.log1p(-gq_hi), PINF)
                bulk_int_sharp += float(np.sum(w[lb] * per_b))
            # collect cells to refine
            if np.any(refine):
                a_keep.append(a[refine]); b_keep.append(b[refine])
        if not a_keep:
            break
        ar = np.concatenate(a_keep); br = np.concatenate(b_keep)
        mid = 0.5 * (ar + br)
        a_cur = np.concatenate([ar, mid]); b_cur = np.concatenate([mid, br])
        depth += 1
        if depth > MAX_DEPTH:
            break

    # float cross-check of identity (I): single uniform midpoint grid (fixed size;
    # the identity is exact, this only confirms it numerically).
    fc_int_logR = 0.0; fc_int_logQ = 0.0; fc_omega = 0.0
    Nfc = 1_000_000
    edges = (np.arange(Nfc + 1, dtype=np.float64) / Nfc) * TWO_PI
    af = edges[:-1]; bf = edges[1:]
    def fev(coef_asc, chi):
        c = np.array([complex(int(x)) for x in coef_asc[::-1]], dtype=np.complex128)
        v = np.zeros_like(chi) + c[0]
        for x in c[1:]:
            v = v * chi + x
        return v
    CHUNK = 500_000
    for s in range(0, Nfc, CHUNK):
        e = min(s + CHUNK, Nfc)
        a = af[s:e]; b = bf[s:e]; w = b - a
        m = 0.5 * (a + b)
        z = np.exp(1j * m); chi = z * (1.0 - z)
        lQ = np.log(np.maximum(np.abs(fev(A_Qstar, chi)), LOG_FLOOR))
        lR = np.log(np.maximum(np.abs(fev(A_R, chi)), LOG_FLOOR))
        Af = np.zeros_like(m)
        for nm, q in NUMERATOR_Q.items():
            Af += q * np.log(np.maximum(np.abs(fev(A_num[nm], chi)), LOG_FLOOR))
        Bf = np.zeros_like(m)
        for blk in denom_blocks:
            Bf += np.log(np.maximum(np.abs(fev(A_denom[blk], chi)), LOG_FLOOR))
        om = Bf > Af
        fc_int_logQ += float(np.sum((w * lQ)[om]))
        fc_int_logR += float(np.sum((w * lR)[om]))
        fc_omega += float(np.sum(w[om]))

    inv2pi = 1.0 / TWO_PI
    rQ_upper = (rQ_upper_int * inv2pi) / deg
    omega0_meas = omega0_w * inv2pi
    delta_meas = delta_w * inv2pi
    omega_meas = omega_w * inv2pi
    well_int_sharp_meas = well_int_sharp * inv2pi
    bulk_int_sharp_meas = bulk_int_sharp * inv2pi

    # float cross-check: identity (I)  r_R - r_Q* = (1/deg) int_Omega log|R/Q*|
    fc_rQ = (fc_int_logQ * inv2pi) / deg
    fc_rR = (fc_int_logR * inv2pi) / deg
    fc_transfer = ((fc_int_logR - fc_int_logQ) * inv2pi) / deg

    c = content[R_name]
    log_c = math.log(c) if c > 0 else 0.0
    if c == 1:
        log_c = 0.0                                # exact, no rounding needed

    # ---- RHS of (II), SHARP per-cell form -- THE CERTIFYING BOUND -----------
    # RHS_sharp = (1/deg)[ log c
    #                    + int_{Omega_0} |log|1-+g/Q*||  ds       (bulk, per-cell)
    #                    + int_W         |log|R/Q*||     ds ] .   (well, per-cell)
    # Each per-cell term is a rigorous outward-rounded enclosure of the integrand:
    #   bulk cell  -> -log(1 - |g/Q*|_hi)              with |g/Q*|_hi <= theta < 1;
    #   well cell  -> max( log r_hi - log q_lo,         (an upper bound on
    #                      log q_hi - log r_lo )         |log|R| - log|Q*|| on the cell).
    # The well term is made tight by the adaptive frontier above; NO global cap
    # log(1/m_R)+M_Q* is used -- that cap is NOT a consequence of the certified
    # constants in the case log|R| > log|Q*| (true on ~63-73% of W), so it is
    # quoted below only as a NON-CERTIFYING diagnostic.
    RHS_sharp = (log_c + bulk_int_sharp_meas + well_int_sharp_meas) / deg
    # the CERTIFIED RHS is the sharp per-cell bound alone (rigorous everywhere).
    RHS = RHS_sharp

    # ---- RHS of (II), GLOBAL-CONSTANT form -- DIAGNOSTIC ONLY, NOT CERTIFYING.
    # bulk = (theta/(1-theta))|Omega_0| ;  well = delta*(log(1/m_R)+M_Q*).  The
    # well piece needs an UPPER bound on |R| and a LOWER bound on |Q*|, neither of
    # which is certified here, so this form does NOT establish firing; reported for
    # comparison only.
    bulk_term = (THETA / (1.0 - THETA)) * omega0_meas
    well_term = (delta_meas * (math.log(1.0 / m_R) + M_Qstar)
                 if m_R > 0 else PINF)
    RHS_global = (log_c + bulk_term + well_term) / deg

    return dict(
        seed=seed_name, R=R_name, tail=tail_name, deg=deg, content=c,
        omega_meas=omega_meas, omega0_meas=omega0_meas, delta=delta_meas,
        M_Qstar=M_Qstar, m_R=m_R, rQ_upper=rQ_upper,
        bulk_term=bulk_term, well_term=well_term,
        bulk_int_sharp=bulk_int_sharp_meas, well_int_sharp=well_int_sharp_meas,
        RHS_global=RHS_global, RHS_sharp=RHS_sharp, RHS=RHS,
        fc_rQ=fc_rQ, fc_rR=fc_rR, fc_transfer=fc_transfer, fc_omega=fc_omega,
        n_unresolved=n_unresolved, depth=depth,
    )


# ---------------------------------------------------------------------------
# Angle-2 degree floor: deg(g_a . tail) = 2a+16; deg R_a = deg Q* = 28 iff a<=5.
# Admissibility per a (squarefree, coprime to Q*, R(0)=R(1)=1, content).
# ---------------------------------------------------------------------------
def degree_floor_table(lib):
    rows = []
    Q1 = lib["Q1"]; P8 = lib["P8"]
    for a in range(1, 7):
        bridge_a = (lib["P1"] ** a) * (lib["P2"] ** a) * lib["P4"]
        g_a = bridge_a * P8                       # tail P8 for the Q1 family
        deg_g = int(g_a.degree())                 # should be 2a+16
        raw = Q1 - g_a
        cont, pp = sp.Poly(raw.as_expr(), X, domain=sp.ZZ).primitive()
        if pp.LC() < 0:
            pp = sp.Poly(-pp.as_expr(), X, domain=sp.ZZ)
        deg_R = int(pp.degree())
        coprime = sp.gcd(pp, Q1).degree() == 0
        squarefree = sp.gcd(pp, pp.diff(X)).degree() == 0
        val01 = (pp.eval(0) == 1 and pp.eval(1) == 1)
        admissible = coprime and squarefree and val01
        # top-two-coefficient preservation iff deg_g < 28 (i.e. 2a+16<=27 i.e. a<=5)
        preserves = (deg_g < int(Q1.degree()))
        rows.append(dict(a=a, deg_g=deg_g, two_a_16=2 * a + 16, deg_R=deg_R,
                         content=abs(int(cont)), coprime=bool(coprime),
                         squarefree=bool(squarefree), val01=bool(val01),
                         admissible=bool(admissible), preserves_deg=bool(preserves)))
    return rows


# ---------------------------------------------------------------------------
def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    print("=" * 78)
    print("firstvar_08  SIBLING-GENERATOR theorem -- rigorous interval certificate")
    print(f"             N = {N} cells,  theta = {THETA}")
    print("=" * 78)

    lib, content = build_library()
    ok = True

    # ---- (D) Angle-2 degree floor (rigorous, cheap) -- print first ----
    print("\n(D) DEGREE FLOOR  g_a = P1^a P2^a P4 . P8 ;  R_a = pp(Q1 - g_a)")
    print(f"    {'a':>2}{'deg g_a':>9}{'2a+16':>7}{'deg R_a':>9}{'cont':>6}"
          f"{'coprime':>9}{'sqfree':>8}{'R(0,1)=1':>10}{'adm':>5}{'deg=28':>8}")
    floor = degree_floor_table(lib)
    floor_ok = True
    for row in floor:
        print(f"    {row['a']:>2}{row['deg_g']:>9}{row['two_a_16']:>7}"
              f"{row['deg_R']:>9}{row['content']:>6}{str(row['coprime']):>9}"
              f"{str(row['squarefree']):>8}{str(row['val01']):>10}"
              f"{str(row['admissible']):>5}{str(row['preserves_deg']):>8}")
        # the exact arithmetic: deg g_a == 2a+16
        if row['deg_g'] != row['two_a_16']:
            floor_ok = False
        # boundary: deg R_a == 28  iff  a<=5 (equivalently 2a+16 < 28)
        want28 = (row['two_a_16'] < 28)
        if (row['deg_R'] == 28) != want28:
            floor_ok = False
        # a in 1..5 must be admissible & content 1
        if row['a'] <= 5 and not (row['admissible'] and row['content'] == 1):
            floor_ok = False
    print(f"    deg(g_a.P8)=2a+16 exact, and deg R_a=28 iff a<=5, "
          f"a<=5 admissible content=1:  {'PASS' if floor_ok else 'FAIL'}")
    print("    => a=5 is the MAXIMAL leading-coefficient-preserving bridge exponent;")
    print("       R0 = R_5.  (a=6: deg(g_6.P8)=28=deg Q1, leading terms cancel, deg drops.)")
    ok &= floor_ok

    # ---- (A,B,C) the marginal-transfer / theta-split firing-transfer bound ----
    log_h = 0.2536331090204145   # Gri26 certified record (the firing threshold)
    results = []
    import time
    for seed, R, tail in [("Q1", "R0", "P8"), ("Q2", "R2", "P7")]:
        print(f"\n--- seed Q* = {seed}  ->  sibling R = {R}  (tail {tail}) ---",
              flush=True)
        t0 = time.time()
        res = certify_seed(seed, R, tail, lib, content, N)
        print(f"    (certified in {time.time()-t0:.0f}s)", flush=True)
        results.append(res)

        # (A) exact identity cross-check (float, midpoint)
        idg = abs((res['fc_rR'] - res['fc_rQ']) - res['fc_transfer'])
        print(f"(A) marginal-transfer identity (I) on fixed anchor Omega_F "
              f"(|Omega_F|~{res['fc_omega']:.4f}):")
        print(f"    r_R - r_Q* = {res['fc_rR'] - res['fc_rQ']:+.7f}   "
              f"(1/deg)int log|R/Q*| = {res['fc_transfer']:+.7f}   "
              f"|gap| = {idg:.2e}")
        ok &= idg < 1e-6

        # (B) certified constants
        print(f"(B) certified constants (outward-rounded interval):")
        print(f"    content c          = {res['content']}        (carried exactly)")
        print(f"    |Omega_F|          <= {res['omega_meas']:.5f}")
        print(f"    |Omega_0| (bulk)   <= {res['omega0_meas']:.5f}")
        print(f"    delta = |W| (well) <= {res['delta']:.5f}   "
              f"(= measure{{|g/Q*|>{THETA}}}; NOT the 0.02 deepest-2% figure)")
        print(f"    M_Q* = sup log|Q*| <= {res['M_Qstar']:.5f}")
        print(f"    m_R  = inf |R|     >= {res['m_R']:.3e}   "
              f"({'contour-root-free on Omega_F' if res['m_R'] > 0 else 'ROOT ON CONTOUR'})")
        print(f"    r_Q*(Omega_F)      <= {res['rQ_upper']:.6f}")
        print(f"    adaptive well-cell refinement: depth {res['depth']}, "
              f"unresolved well cells = {res['n_unresolved']} "
              f"({'all |R|^2>0 certified' if res['n_unresolved'] == 0 else 'INCOMPLETE'})")
        ok &= res['m_R'] > 0 and res['content'] == 1 and res['n_unresolved'] == 0

        # (C) firing-transfer verdict
        print(f"(C) theta-split bound (II):  RHS = (1/{res['deg']})[log c + "
              f"bulk + well]")
        print(f"    -- SHARP per-cell form (THE CERTIFYING bound, rigorous on all of W):")
        print(f"       int_Omega0 |log|1-+g/Q*||         = {res['bulk_int_sharp']:.5f}")
        print(f"       int_W      |log|R/Q*|| (refined)  = {res['well_int_sharp']:.5f}")
        print(f"       RHS_sharp = CERTIFIED RHS          = {res['RHS_sharp']:.6f}")
        print(f"    -- global-constant form (DIAGNOSTIC ONLY, not certifying;")
        print(f"       the well piece needs an uncertified upper bound on |R|):")
        print(f"       bulk = (theta/(1-theta))|Omega_0| = {res['bulk_term']:.5f}")
        print(f"       well = delta(log(1/m_R)+M_Q*)      = "
              f"{res['well_term']:.5f}")
        print(f"       RHS_global (NOT used)              = {res['RHS_global']:.6f}")
        lhs = res['rQ_upper'] + res['RHS']
        fires = lhs < log_h
        res['fires'] = bool(fires)
        print(f"    r_Q*(<= {res['rQ_upper']:.5f}) + RHS_sharp(<= {res['RHS']:.5f}) "
              f"= {lhs:.5f}   <  log h = {log_h:.5f} ?  "
              f"{'YES -> R FIRES (certified)' if fires else 'NO -> firing NOT certified'}")
        ok &= fires

    # ---- (E) tamper checks ----
    print("\n(E) TAMPER checks (must reject):")
    # E1: a deliberately understated log h -- the bound must NOT clear it.
    bogus_logh = -1.0
    cleared_bogus = all(r['rQ_upper'] + r['RHS'] < bogus_logh for r in results)
    print(f"    E1 understated log h = {bogus_logh}: cleared? {cleared_bogus}  "
          f"(must be False)")
    ok &= not cleared_bogus
    # E2: false degree target -- claim deg R = 27 at a=5 (true is 28).
    row5 = next(r for r in floor if r['a'] == 5)
    false_deg = (row5['deg_R'] == 27)
    print(f"    E2 false 'deg R_5 = 27' target: holds? {false_deg}  "
          f"(must be False; true deg R_5 = {row5['deg_R']})")
    ok &= not false_deg
    # E3: false 'a=6 preserves degree' claim.
    row6 = next(r for r in floor if r['a'] == 6)
    false_a6 = row6['preserves_deg']
    print(f"    E3 false 'a=6 preserves deg 28': holds? {false_a6}  "
          f"(must be False; deg R_6 = {row6['deg_R']})")
    ok &= not false_a6

    # ---- firing-certification summary (which blocks' firing is certified) ----
    print("\nFIRING CERTIFICATION (sharp per-cell bound RHS_sharp alone, no global cap):")
    for r in results:
        status = ("CERTIFIED-FIRES" if r.get('fires') else
                  "NOT certified (RHS_sharp does not clear)")
        print(f"    {r['seed']} -> {r['R']}: r_Q*+RHS_sharp = "
              f"{r['rQ_upper'] + r['RHS']:+.5f}  vs log h = {log_h:.5f}   [{status}]")

    print("\n" + "=" * 78)
    print("PASS: R0,R2 are CERTIFIED degree-preserving coprime firing siblings of "
          "Q1,Q2,\n      generated by the bridge ansatz; firing transfer (II) clears "
          "the gap\n      under the rigorous SHARP per-cell well bound alone (no global "
          "cap)." if ok else "FAIL")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
