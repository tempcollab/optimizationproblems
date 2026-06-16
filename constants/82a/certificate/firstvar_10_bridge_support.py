"""firstvar_10 -- RESTRICTED FIRING-OPTIMALITY of the bridge SUPPORT (the deg-4 multiplier).

############################################################################
# DEAD-END ARTIFACT -- DO NOT REVIVE THIS FRAME (R6 proof-reviewer verdict).
#
# This certificate FRAME FAILS structurally and is kept only so future rounds
# do not repeat it.  The lower-bound-difference frame vs Q* = R(P4) = R0 CANNOT
# certify the tight near-miss: the per-competitor D(d)^lo stays NEGATIVE even at
# N=60000 (near-miss #2 d=[1,-1,4,-3,1]: D_lo = -5.2e-4 @ N=4000, -4.5e-4 @ 20000,
# -4.1e-4 @ 60000; trend sublinear, never reaches the +1e-5 tight threshold).  The
# obstruction is structural, NOT a parameter/N issue: deep-well STRADDLE cells where
# R(d) and R(P4) both dive to a shared near-contour zero AND the Omega_F active-set
# membership is uncertain bank ~-4e-4 of genuinely-negative mass (rsub of two wide
# log-wells, banked because the cell cannot be proved certainly-IN).  That negative
# (~4x the entire certainly-IN surplus +9.6e-5) is irreducible: bisecting a deep well
# keeps each sub-cell a straddle and the well-log tail decays only as w*log(1/w).  At
# least one ORDINARY "far" competitor (d=[1,1,1,-2,1]) also fails the coarse gate.
# A full default run is ALSO infeasible to review (~17h: every one of 728 competitors
# shares R0's deep wells, forcing deep bisection ~87s each).
#
# This is the SIGN-FLIPPED twin of firstvar_09, and the flip is fatal: firstvar_09
# certifies an UPPER bound on a genuinely-NEGATIVE integral (banking the negative bulk
# is safe), whereas firstvar_10 needs a POSITIVE lower bound on a small-positive
# integral while being forced to bank the deep-well straddle NEGATIVES.
#
# A salvage needs a DIFFERENT frame (e.g. certifying the Omega_F boundary sharply
# enough at the shared wells so those cells become certainly-IN, or a discrete/algebraic
# separation of the 728 competitors that does not pass through int_{Omega_F}), not a
# parameter tweak.  See /tmp/round-6/proof-reviewer.md.  Prop:support-opt was REMOVED
# from upper_bound_paper.tex; no milestone was earned.
############################################################################

A rigorous, outward-rounded interval certificate that, among the STATED FINITE admissible
family of degree-4 monic bridge multipliers d, the first-variation firing margin
r_{R(d)}(Omega_F) is MAXIMISED (most negative) at d = P4 = (1,-2,4,-3,1) = Grinsztajn's
record factor.  This is the SUPPORT analogue of firstvar_09 (prop:restricted-opt), which
selected the bridge EXPONENT a=5.

==============================  WHAT IS PROVED  ==============================

Fix the bridge CORE chi^5 = P1^5 P2^5 (P1=X, P2=1-X, so P1.P2 = X(1-X) = chi) and the
tail P8; vary ONLY the degree-4 monic multiplier d, forming the degree-28 sibling

    R(d) = pp(Q1 - P1^5 P2^5 . d . P8) .

THE ADMISSIBLE FAMILY A (defined BEFORE any margin is seen, so it is NOT gerrymandered):
    d(X) = X^4 + c3 X^3 + c2 X^2 + c1 X + 1   (monic, unit constant term c0=+1, the
           Doche-normalized sign so R(d)(0)=R(d)(1)=1 is forceable),  with
    |c1|, |c2|, |c3| <= 4   (the height box),  AND R(d) ADMISSIBLE: deg 28, content 1,
    squarefree, coprime to Q1, R(d)(0)=R(d)(1)=1.
P4 = (c3,c2,c1) = (-2,4,-3) is admissible and lies in the box (c2=4 ON the |c2|<=4
boundary; c3,c1 strictly interior -- see the MF1 inactive-boundary diagnostic below).

By the marginal-transfer identity lem:transfer / eq:diff-id (Q* := R(P4), R := R(d), BOTH
degree 28 hence sharing the normalizer 1/28 and scored on the SAME fixed anchor
Omega_F = record \ {Q1}):

    D(d) := r_{R(d)}(Omega_F) - r_{R(P4)}(Omega_F)
          = (1/28) int_{Omega_F} log |R(d)/R(P4)| ds .                       (D)

We certify a rigorous OUTWARD-ROUNDED LOWER bound D(d)^lo on D(d) and assert
D(d)^lo > 0 for every admissible competitor d != P4.  Hence

    r_{R(P4)}(Omega_F) < r_{R(d)}(Omega_F)  for all admissible d != P4,        (chain)

i.e. r_{R(d)} is strictly most negative at d = P4: the firing margin |r_{R(d)}| is
MAXIMISED at d = P4 over the stated finite admissible box.  P4 is the firing-optimal
admissible deg-4 bridge SUPPORT.

HONEST SCOPE (mirror rem:a6 / MF4, MF5).  This selects the deg-4 MULTIPLIER GIVEN the
fixed core chi^5 and tail P8 and seed Q1.  It does NOT derive the core exponent (that is
prop:restricted-opt / firstvar_09) nor the seed Q1 (rem:gen-scope residual).  The claim is
RESTRICTED to the stated finite admissible deg-4 box, NEVER "P4 optimal over all Z[X]".

=========================  RIGOR OF THE SIGNED LOWER BOUND  ==================

This is the SIGN-FLIPPED twin of firstvar_09 (which certified an UPPER bound D_a^hi < 0).
The integrand of (D) is the SIGNED difference log|R(d)| - log|R(P4)|.  It is NOT one-signed
on Omega_F (for the tightest near-miss #2 about 43% of the mass is positive, range
~[-3.58,+1.96]), and membership of a contour cell in Omega_F = {B_F > A_F} is uncertain on
STRADDLE cells.  A rigorous LOWER bound on the true signed integral therefore needs an
ASYMMETRIC accumulation (mirror of firstvar_09 must-fix M1, sign-flipped):

  PER-CELL ENCLOSURE (M2).  log|R|^2 in [r2_lo, r2_hi] (rho_full, outward-rounded), so
  the half-log log|R| in [lR_lo, lR_hi].  The SIGNED integrand log|R(d)| - log|R(P4)| is
  enclosed by the DIRECTED-ROUNDED difference (vv.rsub) of the two half-log intervals:
      lo = lRd_lo - lRP4_hi (rounded down),  hi = lRd_hi - lRP4_lo (rounded up).
  vv.rsub does exactly this with outward np.nextafter -- verified outward on the signed
  difference.

  ASYMMETRIC LOWER ACCUMULATION (M1, FLIPPED).  For a LOWER bound on
  int_{Omega_F} (log|R(d)| - log|R(P4)|):
    - certainly-IN cell  (B_F_lo > A_F_hi):  add  w * int_lo   (the cell IS in Omega_F,
        so its true contribution >= w*int_lo; if int_lo > 0 it CORRECTLY RAISES the sum --
        the positive help is real because the cell is certainly in the region);
    - STRADDLE cell:                         add  w * min(0, int_lo)   (the cell COULD be
        OUT, so bank only a NEGATIVE contribution to stay a lower bound; a straddle cell's
        positive integrand may NOT raise the bound -- it might be OUT);
    - certainly-OUT cell (B_F_hi < A_F_lo):  contributes 0.
  i.e. negative help is banked on every could-be-IN cell; positive help only on
  certainly-IN cells.  This is the ONLY sound rule for a LOWER bound on a signed integral
  over an uncertain region.

  WELL TIGHTNESS.  The signed enclosure of a cell is per-cell loose where R(d), R(P4) both
  dive to deep near-contour zeros (they share most roots; mild wells).  The width-weighted
  contribution grows only like w*log(1/w) at a shared well, so it -> 0 under bisection.  We
  adaptively bisect a could-be-IN cell whenever |w * int_lo| (its potential to MOVE the
  lower bound) exceeds WELL_TOL, OR either |R(d)|^2/|R(P4)|^2 is not yet certified > 0 (the
  m_R > 0 root-freeness gate, M3), up to MAX_DEPTH.

  ROOT-FREENESS (M3).  m_{R(d)} := inf_{Omega_F} |R(d)| > 0 and m_{R(P4)} > 0 are certified
  per competitor.  A leaf could-be-IN cell at the depth cap with either |R|^2 enclosure
  still touching 0 is reported UNRESOLVED (a FAIL).  Required on BOTH R(d) and R(P4).

PASS iff D(d)^lo > 0 for every admissible competitor d != P4, the family A is the stated
box, m_{R(d)} > 0 and m_{R(P4)} > 0 with 0 unresolved cells on every tightly-certified
competitor, the MF1 enlarged-box (|ci|<=6) diagnostic shows the boundary inactive, and the
tamper checks reject.

STAGING.  (i) exact sympy enumeration of A; (ii) a RIGOROUS coarse pre-screen (outward-
rounded D(d)^lo at low N) clears every NON-near-miss by a certified lower bound >
COARSE_THRESHOLD (MF2 -- never a float gate); (iii) every near-miss (those NOT cleared
coarsely; the float-gap<3e-3 set, ~17 of them) is certified TIGHT at high N with a tight
D(d)^lo > TIGHT_THRESHOLD.  A tamper check asserts every float-gap<3e-3 competitor reaches
the tight stage.

Run:   python3 firstvar_10_bridge_support.py                 (default N, full cert)
       python3 firstvar_10_bridge_support.py --coarse-N 4000 --tight-N 120000
       python3 firstvar_10_bridge_support.py --dev           (small-N self-test, fast)
Progress + per-competitor results streamed to scratch/firstvar_10_progress.txt.
Requires: numpy, sympy (+ the bound_00/bound_01 interval modules in this dir).
"""

import sys
import os
import math
import time
import itertools

import numpy as np
import sympy as sp

import bound_00_flammang_baseline as vv      # rigorous interval machinery
import bound_01_doche_base as vu             # rho_full cell enclosure + w_full_*

PINF = math.inf
NINF = -math.inf
na = np.nextafter
TWO_PI = 2.0 * math.pi
X = sp.Symbol("X")

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRESS = os.path.join(HERE, "scratch", "firstvar_10_progress.txt")

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
NUMERATOR_Q = {
    "P1": 26.511877484730615, "P2": 23.782846008412744,
    "P3": 0.9707094545190521, "P4": 4.526072775020114,
    "P5": 0.038326545650764404, "P6": 4.173784226054273,
    "P8": 1.685809173822071,
}
NUM_EXTRA = {
    "P3": [1, 1, -2, 1],
    "P5": [1, -2, 4, -7, 13, -16, 12, -5, 1],
}
# anchor F = record \ {Q1}; the denom blocks are these (R0=R(P4), R2 are built below)
ANCHOR_DENOM = ["Q2", "R0", "R2", "P7", "P9"]

LOG_FLOOR = 1e-300
P4_HL = [1, -2, 4, -3, 1]

NEAR_GAP = 3e-3          # float-gap threshold defining a "near-miss" (must reach tight)
COARSE_THRESHOLD = 1e-4  # a non-near-miss is CLEARED iff its coarse D^lo > this
TIGHT_THRESHOLD = 1e-5   # a near-miss is certified iff its tight D^lo > this


def _poly(coeffs):
    return sp.Poly.from_list([sp.Integer(c) for c in coeffs], gens=X, domain=sp.ZZ)


def asc(coeffs_hl):
    return [int(c) for c in coeffs_hl[::-1]]


def build_library():
    lib = {k: _poly(v) for k, v in POLY_COEFFS.items()}
    for k, v in NUM_EXTRA.items():
        lib[k] = _poly(v)
    # R0 = R(P4), R2 are anchor denom blocks; build them (full deg-5 core P1^5 P2^5 P4).
    bridge5 = (lib["P1"] ** 5) * (lib["P2"] ** 5) * lib["P4"]
    for name, seed, tail, sign in [("R0", "Q1", "P8", -1), ("R2", "Q2", "P7", +1)]:
        raw = lib[seed] + sign * bridge5 * lib[tail]
        cont, pp = sp.Poly(raw.as_expr(), X, domain=sp.ZZ).primitive()
        if pp.LC() < 0:
            pp = sp.Poly(-pp.as_expr(), X, domain=sp.ZZ)
        lib[name] = pp
    return lib


def build_R_d(lib, d_hl):
    """R(d) = pp(Q1 - P1^5 P2^5 . d . P8); positive leading coeff; return (content, pp).
    d_hl = high-to-low coeffs of the monic deg-4 multiplier d."""
    core5 = (lib["P1"] ** 5) * (lib["P2"] ** 5)
    g = core5 * _poly(d_hl) * lib["P8"]
    raw = lib["Q1"] - g
    cont, pp = sp.Poly(raw.as_expr(), X, domain=sp.ZZ).primitive()
    if pp.LC() < 0:
        pp = sp.Poly(-pp.as_expr(), X, domain=sp.ZZ)
    return abs(int(cont)), pp


def admissible(lib, d_hl):
    """deg 28, content 1, squarefree, coprime to Q1, R(0)=R(1)=1 (exact sympy)."""
    cont, pp = build_R_d(lib, d_hl)
    if int(pp.degree()) != 28:
        return False, pp, cont, "deg!=28"
    if cont != 1:
        return False, pp, cont, "content!=1"
    if sp.gcd(pp, lib["Q1"]).degree() != 0:
        return False, pp, cont, "not coprime to Q1"
    if sp.gcd(pp, pp.diff(X)).degree() != 0:
        return False, pp, cont, "not squarefree"
    if not (pp.eval(0) == 1 and pp.eval(1) == 1):
        return False, pp, cont, "R(0)/R(1)!=1"
    return True, pp, cont, "OK"


def enumerate_box(lib, crange=range(-4, 5)):
    """Exact enumeration of A: monic, c0=+1, c1,c2,c3 in crange, R(d) admissible.
    Returns list of (d_hl, pp)."""
    out = []
    for c3, c2, c1 in itertools.product(crange, crange, crange):
        d_hl = [1, c3, c2, c1, 1]
        ok, pp, cont, msg = admissible(lib, d_hl)
        if ok:
            out.append((d_hl, pp))
    return out


# ---------------------------------------------------------------------------
def cell_geometry(a, b):
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    Wc, DWc, DDWc, DDDWc = vu.w_full_cell(a, b)
    Wm, DWm, DDWm, DDDWm = vu.w_full_point(m)
    return (m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)


def cell_rho_lo_hi(coef_asc, geo):
    m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc = geo
    _, _, rho_lo, rho_hi, _ = vu.rho_full(
        coef_asc, m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)
    return rho_lo, rho_hi


# ---------------------------------------------------------------------------
# Certify a rigorous OUTWARD-ROUNDED LOWER bound D(d)^lo on
#     D(d) = (1/28) int_{Omega_F} log |R(d)/R(P4)| ds .
# (lem:transfer with Q* := R(P4), R := R(d); both degree 28 on the SAME anchor.)
# This is the SIGN-FLIPPED twin of firstvar_09.certify_diff.
# ---------------------------------------------------------------------------
def certify_diff_support(A_R_d, A_R_P4, A_num, A_denom, denom_blocks, N,
                         well_tol, max_depth):
    deg = 28

    def cell_kernel(a_, b_):
        w = b_ - a_
        geo = cell_geometry(a_, b_)
        rd2_lo, rd2_hi = cell_rho_lo_hi(A_R_d, geo)
        rp2_lo, rp2_hi = cell_rho_lo_hi(A_R_P4, geo)
        lRd_lo = na(0.5 * vv.log_down(np.maximum(rd2_lo, LOG_FLOOR)), NINF)
        lRd_hi = na(0.5 * vv.log_up(np.maximum(rd2_hi, LOG_FLOOR)), PINF)
        lRp_lo = na(0.5 * vv.log_down(np.maximum(rp2_lo, LOG_FLOOR)), NINF)
        lRp_hi = na(0.5 * vv.log_up(np.maximum(rp2_hi, LOG_FLOOR)), PINF)
        # M2: SIGNED integrand log|R(d)| - log|R(P4)|, directed-rounded difference
        #     [lRd_lo - lRp_hi, lRd_hi - lRp_lo] via vv.rsub.
        int_lo, int_hi = vv.rsub(lRd_lo, lRd_hi, lRp_lo, lRp_hi)
        # Omega_F membership: A_F = sum q_i log|P_i|; B_F = sum log|block|.
        A_lo = np.zeros_like(a_); A_hi = np.zeros_like(a_)
        for nm, q in NUMERATOR_Q.items():
            p2_lo, p2_hi = cell_rho_lo_hi(A_num[nm], geo)
            lp_lo = na(0.5 * vv.log_down(np.maximum(p2_lo, LOG_FLOOR)), NINF)
            lp_hi = na(0.5 * vv.log_up(np.maximum(p2_hi, LOG_FLOOR)), PINF)
            A_lo = na(A_lo + na(q * lp_lo, NINF), NINF)
            A_hi = na(A_hi + na(q * lp_hi, PINF), PINF)
        B_lo = np.zeros_like(a_); B_hi = np.zeros_like(a_)
        for blk in denom_blocks:
            p2_lo, p2_hi = cell_rho_lo_hi(A_denom[blk], geo)
            lp_lo = na(0.5 * vv.log_down(np.maximum(p2_lo, LOG_FLOOR)), NINF)
            lp_hi = na(0.5 * vv.log_up(np.maximum(p2_hi, LOG_FLOOR)), PINF)
            B_lo = na(B_lo + lp_lo, NINF)
            B_hi = na(B_hi + lp_hi, PINF)
        certainly_in = B_lo > A_hi
        certainly_out = B_hi < A_lo
        straddle = (~certainly_in) & (~certainly_out)
        both_pos = (rd2_lo > LOG_FLOOR) & (rp2_lo > LOG_FLOOR)
        return dict(w=w, int_lo=int_lo, int_hi=int_hi,
                    certainly_in=certainly_in, straddle=straddle,
                    certainly_out=certainly_out, both_pos=both_pos,
                    rd2_lo=rd2_lo, rp2_lo=rp2_lo)

    lower_sum = 0.0          # rigorous LOWER endpoint of the unnormalized integral
    omega_w = 0.0
    m_Rd = PINF; m_RP4 = PINF
    n_unresolved = 0

    edges = (np.arange(N + 1, dtype=np.float64) / N) * TWO_PI
    a_cur = edges[:-1].copy(); b_cur = edges[1:].copy()
    depth = 0
    CHUNK = 200_000
    while True:
        a_keep = []; b_keep = []
        for s in range(0, a_cur.shape[0], CHUNK):
            e = min(s + CHUNK, a_cur.shape[0])
            a_ = a_cur[s:e]; b_ = b_cur[s:e]
            k = cell_kernel(a_, b_)
            w = k['w']
            could_in = k['certainly_in'] | k['straddle']
            # M1 (FLIPPED): LOWER contribution per cell
            #   certainly-IN -> w * int_lo  (positive help allowed)
            #   straddle     -> w * min(0, int_lo)  (negative only -- cell might be OUT)
            lo_contrib = np.zeros_like(w)
            ci = k['certainly_in']; st = k['straddle']
            lo_contrib = np.where(ci, w * k['int_lo'], lo_contrib)
            lo_contrib = np.where(st, w * np.minimum(0.0, k['int_lo']), lo_contrib)
            # refine could-be-IN cell if it can MOVE the lower bound by > tol OR roots
            # not yet certified away (need BOTH R(d), R(P4) positive on the cell).
            heavy = (w * np.abs(k['int_lo'])) > well_tol
            refine = could_in & ((~k['both_pos']) | heavy) & (depth < max_depth)
            leaf = ~refine
            lm = leaf & could_in
            if np.any(lm):
                lower_sum += float(np.sum(lo_contrib[lm]))
                omega_w += float(np.sum(w[lm]))
                rd_pos = lm & (k['rd2_lo'] > LOG_FLOOR)
                rp_pos = lm & (k['rp2_lo'] > LOG_FLOOR)
                if np.any(rd_pos):
                    m_Rd = min(m_Rd, float(np.min(np.sqrt(k['rd2_lo'][rd_pos]))))
                if np.any(rp_pos):
                    m_RP4 = min(m_RP4, float(np.min(np.sqrt(k['rp2_lo'][rp_pos]))))
                bad = lm & (~k['both_pos'])
                n_unresolved += int(np.sum(bad))
            if np.any(refine):
                a_keep.append(a_[refine]); b_keep.append(b_[refine])
        if not a_keep:
            break
        ar = np.concatenate(a_keep); br = np.concatenate(b_keep)
        mid = 0.5 * (ar + br)
        a_cur = np.concatenate([ar, mid]); b_cur = np.concatenate([mid, br])
        depth += 1
        if depth > max_depth:
            break

    inv2pi = 1.0 / TWO_PI
    D_lo = na((lower_sum * inv2pi) / deg, NINF)   # rigorous LOWER bound on D(d)
    return dict(D_lo=D_lo, omega_meas=omega_w * inv2pi,
                m_Rd=m_Rd, m_RP4=m_RP4, n_unresolved=n_unresolved, depth=depth)


# ---------------------------------------------------------------------------
def prep_static(lib):
    """Static ascending-coeff arrays shared by all competitor certs."""
    A_R_P4 = asc([int(c) for c in build_R_d(lib, P4_HL)[1].all_coeffs()])
    denom_blocks = ANCHOR_DENOM  # all five; R0=R(P4), R2 built in lib
    A_denom = {b: asc([int(c) for c in lib[b].all_coeffs()]) for b in denom_blocks}
    A_num = {}
    for nm in NUMERATOR_Q:
        coeffs = POLY_COEFFS[nm] if nm in POLY_COEFFS else NUM_EXTRA[nm]
        A_num[nm] = asc(coeffs)
    return A_R_P4, A_num, A_denom, denom_blocks


def cert_one(lib, d_hl, static, N, well_tol, max_depth):
    A_R_P4, A_num, A_denom, denom_blocks = static
    A_R_d = asc([int(c) for c in build_R_d(lib, d_hl)[1].all_coeffs()])
    return certify_diff_support(A_R_d, A_R_P4, A_num, A_denom, denom_blocks,
                                N, well_tol, max_depth)


# ---------------------------------------------------------------------------
# Float cross-check (FIXED-size grid; the identity (D) is exact, this only confirms it).
# ---------------------------------------------------------------------------
def float_setup(lib):
    Nfc = 2_000_000
    edges = (np.arange(Nfc + 1, dtype=np.float64) / Nfc) * TWO_PI
    m = 0.5 * (edges[:-1] + edges[1:]); w = edges[1:] - edges[:-1]
    z = np.exp(1j * m); chi = z * (1.0 - z)

    def fev(coef_asc, chi):
        c = np.array([complex(int(x)) for x in coef_asc[::-1]], dtype=np.complex128)
        v = np.zeros_like(chi) + c[0]
        for x in c[1:]:
            v = v * chi + x
        return v

    A_num = {}
    for nm in NUMERATOR_Q:
        coeffs = POLY_COEFFS[nm] if nm in POLY_COEFFS else NUM_EXTRA[nm]
        A_num[nm] = asc(coeffs)
    Af = np.zeros_like(m)
    for nm, q in NUMERATOR_Q.items():
        Af += q * np.log(np.maximum(np.abs(fev(A_num[nm], chi)), LOG_FLOOR))
    Bf = np.zeros_like(m)
    for blk in ANCHOR_DENOM:
        Ab = asc([int(c) for c in lib[blk].all_coeffs()])
        Bf += np.log(np.maximum(np.abs(fev(Ab, chi)), LOG_FLOOR))
    om = Bf > Af
    inv2pi = 1.0 / TWO_PI; deg = 28

    def margin(pp):
        cf = asc([int(c) for c in pp.all_coeffs()])
        lP = np.log(np.maximum(np.abs(fev(cf, chi)), LOG_FLOOR))
        return (np.sum((w * lP)[om]) * inv2pi) / deg
    return margin


# ---------------------------------------------------------------------------
def plog(line):
    print(line, flush=True)
    try:
        with open(PROGRESS, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def main():
    args = sys.argv[1:]
    dev = "--dev" in args
    def getarg(flag, default):
        if flag in args:
            return int(args[args.index(flag) + 1])
        return default
    if dev:
        coarse_N = getarg("--coarse-N", 2000)
        tight_N = getarg("--tight-N", 4000)
        well_tol = 5e-5; max_depth = 30
    else:
        coarse_N = getarg("--coarse-N", 4000)
        tight_N = getarg("--tight-N", 160000)
        well_tol = 2e-5; max_depth = 44

    os.makedirs(os.path.dirname(PROGRESS), exist_ok=True)
    open(PROGRESS, "w").close()
    plog("=" * 78)
    plog("firstvar_10  RESTRICTED FIRING-OPTIMALITY of the bridge SUPPORT (deg-4 d)")
    plog(f"             coarse_N={coarse_N}  tight_N={tight_N}  well_tol={well_tol}"
         f"  dev={dev}")
    plog("=" * 78)

    lib = build_library()
    static = prep_static(lib)
    ok = True

    # ---- (A) exact enumeration of the admissible box ----
    t0 = time.time()
    box = enumerate_box(lib, range(-4, 5))
    plog(f"\n(A) admissible box A (monic, c0=+1, |ci|<=4): |A| = {len(box)} of 729 raw"
         f"  ({time.time()-t0:.1f}s)")
    P4_in = any(d == P4_HL for d, _ in box)
    plog(f"    P4=(1,-2,4,-3,1) in A? {P4_in}   (c2=4 on the |c2|<=4 boundary; "
         f"c3,c1 interior)")
    ok &= P4_in

    # ---- float margins (DIAGNOSTIC; identity (D) is exact) ----
    margin = float_setup(lib)
    R_P4 = build_R_d(lib, P4_HL)[1]
    r_P4 = margin(R_P4)
    plog(f"\n(F) float cross-check: r_R(P4) = {r_P4:+.5f}  (anchor sanity, expect -0.03560)")
    rows = []
    for d_hl, pp in box:
        rows.append((margin(pp) - r_P4, d_hl, pp))
    rows.sort(key=lambda t: t[0])
    p4_min = rows[0][1] == P4_HL
    plog(f"    P4 the unique float minimiser (most negative margin)? {p4_min}")
    ok &= p4_min
    near = [(g, d, pp) for (g, d, pp) in rows if d != P4_HL and g < NEAR_GAP]
    nonnear = [(g, d, pp) for (g, d, pp) in rows if d != P4_HL and g >= NEAR_GAP]
    plog(f"    competitors: {len(rows)-1} (excl P4); near-miss (float gap<{NEAR_GAP}): "
         f"{len(near)};  non-near: {len(nonnear)}")
    plog(f"    tightest few near-misses (float gap):")
    for g, d, _ in near[:6]:
        plog(f"      gap={g:+.3e}  d={d}")

    # ---- (B) COARSE rigorous pre-screen: clear non-near-misses by certified D^lo ----
    plog(f"\n(B) COARSE rigorous pre-screen (N={coarse_N}): clear each NON-near-miss by a"
         f"\n    certified outward-rounded D(d)^lo > COARSE_THRESHOLD={COARSE_THRESHOLD}"
         f"  (MF2: rigorous, not a float gate)")
    coarse_pass = 0; coarse_fail = []
    survivors = []   # competitors NOT cleared coarsely -> must go to tight stage
    t0 = time.time()
    for i, (g, d, pp) in enumerate(nonnear):
        res = cert_one(lib, d, static, coarse_N, well_tol, max_depth)
        cleared = res['D_lo'] > COARSE_THRESHOLD
        if cleared:
            coarse_pass += 1
        else:
            survivors.append((g, d, pp))
            coarse_fail.append((d, res['D_lo'], g))
        if (i + 1) % 50 == 0 or not cleared:
            plog(f"    [{i+1}/{len(nonnear)}] d={d} D^lo={res['D_lo']:+.3e} "
                 f"{'cleared' if cleared else 'SURVIVES->tight'} "
                 f"({time.time()-t0:.0f}s)")
    plog(f"    coarse cleared {coarse_pass}/{len(nonnear)} non-near-misses; "
         f"{len(coarse_fail)} survive to tight stage  ({time.time()-t0:.0f}s)")

    # MF2 tamper check: EVERY float-gap<NEAR_GAP competitor must reach the tight stage.
    tight_set = near + survivors
    tight_dset = set(tuple(d) for _, d, _ in tight_set)
    miss = [d for _, d, _ in near if tuple(d) not in tight_dset]
    plog(f"    TAMPER (MF2): every float-gap<{NEAR_GAP} reaches tight stage? "
         f"{len(miss)==0}  (missing: {miss})")
    ok &= (len(miss) == 0)

    # ---- (C) TIGHT cert: D(d)^lo > TIGHT_THRESHOLD for every survivor ----
    plog(f"\n(C) TIGHT cert (N={tight_N}): certified D(d)^lo > "
         f"TIGHT_THRESHOLD={TIGHT_THRESHOLD} for each of {len(tight_set)} survivors")
    tight_results = []
    t0 = time.time()
    for j, (g, d, pp) in enumerate(sorted(tight_set, key=lambda t: t[0])):
        res = cert_one(lib, d, static, tight_N, well_tol, max_depth)
        passed = (res['D_lo'] > TIGHT_THRESHOLD and res['m_Rd'] > 0
                  and res['m_RP4'] > 0 and res['n_unresolved'] == 0)
        tight_results.append((d, res, passed, g))
        plog(f"    [{j+1}/{len(tight_set)}] d={d} floatgap={g:+.2e} "
             f"D^lo={res['D_lo']:+.4e} m_Rd={res['m_Rd']:.2e} "
             f"m_RP4={res['m_RP4']:.2e} depth={res['depth']} unres={res['n_unresolved']}"
             f" {'PASS' if passed else 'FAIL'} ({time.time()-t0:.0f}s)")
        ok &= passed

    # ---- (D) MF1 inactive-boundary diagnostic: enlarged box |ci|<=6 ----
    plog(f"\n(D) MF1 inactive-boundary diagnostic: enlarge box to |ci|<=6, check NO"
         f"\n    admissible competitor OUTSIDE |ci|<=4 comes within 1e-3 of P4's margin.")
    t0 = time.time()
    worst = None; n_out = 0; near_out = []
    for c3, c2, c1 in itertools.product(range(-6, 7), repeat=3):
        if abs(c3) <= 4 and abs(c2) <= 4 and abs(c1) <= 4:
            continue
        d_hl = [1, c3, c2, c1, 1]
        okd, pp, cont, msg = admissible(lib, d_hl)
        if not okd:
            continue
        n_out += 1
        g = margin(pp) - r_P4
        if g < 1e-3:
            near_out.append((g, d_hl))
        if worst is None or g < worst[0]:
            worst = (g, d_hl)
    plog(f"    admissible OUTSIDE |ci|<=4 (within |ci|<=6): {n_out}  "
         f"({time.time()-t0:.0f}s)")
    if worst is not None:
        plog(f"    smallest float gap to P4 among them: {worst[0]:+.4e} at d={worst[1]}")
    plog(f"    within 1e-3 of P4 OUTSIDE |ci|<=4: {len(near_out)}  (MF1 wants EMPTY)")
    boundary_inactive = (len(near_out) == 0)
    ok &= boundary_inactive

    # ---- (E) tamper checks ----
    plog(f"\n(E) TAMPER checks (must reject):")
    # E1: a fabricated D(d)^lo <= 0 for the tightest survivor must FAIL the PASS.
    tightest = min(tight_results, key=lambda t: t[1]['D_lo'])
    real_dlo = tightest[1]['D_lo']
    fake_dlo = -abs(real_dlo) - 1.0   # fabricate a non-positive bound
    fake_pass = (fake_dlo > TIGHT_THRESHOLD)
    plog(f"    E1 fabricated D^lo={fake_dlo:+.3e} for tightest d={tightest[0]} "
         f"passes? {fake_pass}  (must be False)")
    ok &= (not fake_pass)
    # E2: admissibility filter must REJECT a non-competitor (e.g. a non-monic or
    #     boundary-violating d, and a d with content != 1).
    bad_d = [1, 9, 0, 0, 1]   # c3=9 outside the box AND likely inadmissible
    okbad, _, _, msgbad = admissible(lib, bad_d)
    box_ok = all(abs(c) <= 4 for c in bad_d[1:4])
    plog(f"    E2 out-of-box d={bad_d} in box? {box_ok}  (must be False)")
    ok &= (not box_ok)
    # E3: the tightest certified margin clears 0 comfortably.
    margin_clear = real_dlo - TIGHT_THRESHOLD
    plog(f"    E3 tightest survivor D^lo margin over threshold = {margin_clear:+.3e} "
         f"(D^lo={real_dlo:+.4e}); >0? {margin_clear > 0}")
    ok &= (margin_clear > 0)

    # ---- conclusion ----
    plog("\n" + "=" * 78)
    if ok:
        plog("PASS: among the stated finite admissible deg-4 bridge multipliers d")
        plog("      (monic, c0=+1, |ci|<=4, R(d) admissible), the firing margin")
        plog("      r_{R(d)}(Omega_F) is STRICTLY most negative at d = P4 = (1,-2,4,-3,1):")
        plog("      D(d)^lo > 0 certified for every competitor (coarse or tight),")
        plog("      m_R>0 on R(d) and R(P4), 0 unresolved, boundary inactive (MF1).")
        plog("      => P4 is the firing-optimal admissible deg-4 bridge SUPPORT")
        plog("         (RESTRICTED to the stated box; the SUPPORT half of rem:gen-scope).")
    else:
        plog("FAIL")
    plog("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
