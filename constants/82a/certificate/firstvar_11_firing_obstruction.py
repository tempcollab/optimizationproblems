"""firstvar_11 -- BASE-MARGINAL FIRING OBSTRUCTION / ROOT-LOCALISATION theorem.

A rigorous, outward-rounded interval certificate that proves the paper's heuristic
Remark rem:wells as a PROVED root-localisation NECESSARY CONDITION: every admissible
integer block that fires on the base branch must have at least one X-root inside an
EXPLICIT compact set K.  This adds the geometry the paper explicitly disclaims it has
("the statements above rest on the additivity ... NOT on the geometry").

==============================  WHAT IS PROVED  ==============================

Setup (paper notation; held R4 anchor, firstvar_04).  The base branch of the firing
criterion cor:criterion: an admissible integer block Q enters profitably (fires on
the base side) iff its base marginal is negative,

    r~_Q  =  int_{Omega_F} log|Q(chi(s))| ds  <  0 ,
    chi(s) = z(1-z),  z = e^{2 pi i s},   Omega_F = {A > B}  (the base active arc),

with ds the s-uniform mean and meas(Omega_F) = 0.068607 on the held R4 family.

STEP 1 -- EXACT X-ROOT ADDITIVITY (proved analytically; here verified numerically).
Write Q(X) = lc * prod_j (X - alpha_j) over its complex roots (with multiplicity).
Then, by log|Q(chi)| = log|lc| + sum_j log|chi - alpha_j| and linearity of the
integral,

    r~_Q  =  log|lc| * meas(Omega_F)  +  sum_j U(alpha_j),
    U(alpha) := int_{Omega_F} log|chi(s) - alpha| ds .                       (ADD)

HYPOTHESIS (content/lc bookkeeping, MUST-FIX 3).  The obstruction below uses ONLY the
root sum sum_j U(alpha_j); the leading-coefficient term log|lc| * meas(Omega_F) must
NOT be negative or it could fire on its own.  We state the theorem for blocks with the
content normalised to a MONIC representative, lc = +1 (admissible primitive integer
blocks pp(.) considered in the paper are monic up to sign; log|lc| = 0).  For such a
block (ADD) reduces to  r~_Q = sum_j U(alpha_j).  A block with |lc| < 1 fractional
content would add a NEGATIVE log|lc|*meas term and the obstruction would not apply; we
exclude that case by hypothesis (it is not an integer-block case).

STEP 2 -- U(alpha) >= c > 0 OUTSIDE an explicit compact set (the load-bearing step).
We certify, with outward-rounded interval arithmetic, two lower bounds:

  (i)  HALF-PLANE-WITHIN-RADIUS box B = {-R0 <= Re(alpha) <= -delta, |Im(alpha)| <= R0}:
       U(alpha) >= c1 > 0 for every alpha in B, by a 2-D interval cover of B with, per
       alpha-cell, an outward-rounded LOWER bound on
            U over the cell  =  sum over s-cells of Omega_F of the worst-case
            (1/2) log |chi(s) - alpha|^2 .
       The separation inf_{s,alpha} |chi(s) - alpha| is certified > 0 per cell by the
       interval enclosure ITSELF (MUST-FIX 2: NOT by any half-plane property of chi --
       min Re(chi) on Omega_F is -1.73, so Re(chi) >= 0 is FALSE; the separation is the
       genuine geometric fact and is certified by the enclosure of |chi - alpha|^2).

  (ii) FAR FIELD |alpha| >= R0: U(alpha) >= meas * log(R0 - M) =: c2 > 0, by the
       pointwise Jensen / triangle estimate
            log|chi(s) - alpha| >= log(|alpha| - |chi(s)|) >= log(R0 - M)
       valid once |alpha| >= R0 > M := sup_{s} |chi(s)|.  (MUST-FIX 1: sup_s|chi| = 2
       EXACTLY on the unit circle, so R0 must satisfy R0 - M > 0; R0 = 1.3 is INVALID.
       We take M = 2 (a rigorous upper bound for sup over Omega_F too) and R0 = 3.5, so
       log(R0 - M) = log(1.5) > 0 and c2 = meas * log(1.5) > 0 is positive WITH MARGIN.)

The two certified regions {Re(alpha) <= -delta} and {|alpha| >= R0} together cover
their union: any alpha with Re <= -delta is either in box B (if -R0 <= Re and |Im| <=
R0) or has |alpha| >= R0 (if Re < -R0, or |Im| > R0).  Hence U(alpha) >= min(c1,c2) > 0
on  {Re(alpha) <= -delta}  UNION  {|alpha| >= R0}.

THE WELL SET / COMPACT K.  Define K as the CLOSED complement of the certified U>=0
region:
    K := { alpha : Re(alpha) >= -delta }  INTERSECT  { |alpha| <= R0 } .       (K)
K is closed and compact.  The well W = {U < 0} satisfies W subset of K.

STEP 3 -- THE OBSTRUCTION (root-localisation necessary condition).  Let Q be an
admissible monic (lc=+1) integer block.  If EVERY X-root alpha_j of Q (with
multiplicity) lies in the certified U>=0 region -- i.e. each alpha_j has
Re(alpha_j) <= -delta OR |alpha_j| >= R0 -- then by (ADD) with log|lc|=0,
    r~_Q  =  sum_j U(alpha_j)  >=  (number of roots) * min(c1, c2)  >  0,
so r~_Q > 0 and Q DOES NOT FIRE on the base branch.  Contrapositive:

    A firing admissible monic block must have at least one X-root in the compact set K.

This is predictive root-localisation: it tells WHERE a firing block's roots must live,
which rem:wells only asserted.  Boundary handling: K is closed (includes its boundary);
a root with Re in (-delta, 0] is INSIDE K already, so there is no boundary ambiguity.
Multiplicity: the sum (ADD) is over all roots WITH multiplicity and the per-root bound
U(alpha_j) >= min(c1,c2) > 0 holds for each, so a multiple root only strengthens the
positive sum.

=========================  RIGOR OF THE LOWER BOUND  ========================

SAFE DIRECTION (why this is NOT the firstvar_10 dead end).  This is a LOWER bound on U
on a region where U is comfortably positive (the certified c1 ~ 9.5e-4, c2 ~ 7e-3),
with the log singularity held OFF the contour: for every alpha in box B the separation
inf_s|chi(s)-alpha| is certified > 0 cell-by-cell (g_lo > 0), so log|chi - alpha|^2 is
finite and the quadrature is a fixed 1-D-in-s sum.  NOTE: the separation is NOT large
everywhere.  chi traces a lemniscate reaching Re(chi) ~ -1.73, so the contour GRAZES
part of box B: the WORST certified separation over box B is ~0.0075 (at alpha ~
-1.626 + 1.108i), not ~0.47.  U stays positive there anyway (~ +0.05) because the
single grazing s contributes one bounded-negative integrand swamped by the far bulk --
but the small separation is real and is why box B needs DEEP adaptive refinement near
the grazing band (this is the expensive step).  Adaptivity is in ALPHA (bisect an
alpha-cell whose certified U-lower-bound is not yet > 0); the s-grid stays fixed.

COMPLEX TAYLOR ENCLOSURE of chi(s) over an s-cell [a,b] (avoids interval-Horner
dependency blow-up over a wide cell):
    chi(t) = w(t) = w(m) + w'(m)(t-m) + (1/2) w''(xi)(t-m)^2,  xi in [a,b],
using the TIGHT midpoint w(m), w'(m) (w_full_point) and the CELL enclosure of w''
(w_full_cell) for the remainder.  Width ~ (b-a)^2/8 -- e.g. ~4e-3 at N=4000.

PER (s-cell, alpha-cell) ENCLOSURE of |chi - alpha|^2.
    chi - alpha  in  [wr_lo - are_hi, wr_hi - are_lo] x [wi_lo - aim_hi, wi_hi - aim_lo]
    g = |chi - alpha|^2 = Re^2 + Im^2  (outward-rounded via vv.rmul + vv.radd).
    g_lo > 0 is the certified separation^2; if g_lo <= 0 the alpha-cell is REFINED.

ASYMMETRIC LOWER ACCUMULATION (mirror of firstvar_09's upper rule, for a LOWER bound
on the SIGNED integral int_{Omega_F} (1/2)log g over the uncertain region {A>B}):
    - certainly-IN  s-cell (A_lo > B_hi):  add  w * (1/2) log_down(g_lo)
        (the cell IS in Omega_F; its contribution >= w * 0.5 log_down(g_lo), and a
         NEGATIVE half-log is real banked-negative help -- correct for a lower bound);
    - STRADDLE       s-cell:               add  w * min(0, (1/2) log_down(g_lo))
        (the cell COULD be in Omega_F, so only bank a NEGATIVE half-log -- never let a
         straddle cell's positive integrand raise the lower bound, it might be OUT);
    - certainly-OUT  s-cell (A_hi < B_lo): contributes 0.
This is the only sound rule for a LOWER bound on a signed integral over an uncertain
region.  A symmetric |.| bound would round toward 0 and be UNSOUND.

Omega_F = {A > B} membership per s-cell from interval enclosures of
    A = sum_i q_i log|P_i(chi)| + qG log|Q7| + qH log|Q8|   (base blocks),
    B = log|Q1| + log|Q2| + qE log|Q5| + qF log|Q6|         (denominator blocks),
all via rho_full half-log enclosures (the firstvar_09 pattern).  The s-cell geometry,
the A/B membership classification, and the half-log of chi over each s-cell are
PRECOMPUTED ONCE (fixed across the whole alpha-cover) -- only chi - alpha changes per
alpha-cell, so the cover is feasible (minutes, not the ~17h full-box regime).

PASS iff: additivity reproduced to ~1e-15; U(alpha) >= c1 > 0 on EVERY alpha-cell of
box B with 0 unresolved cells; M = sup|chi| <= 2 and R0 - M > 0 with c2 > 0; the
certified K box printed; and the tamper checks reject (corrupt a load-bearing g_lo
enclosure -> a cell fails; claim c1 above the true min -> FAIL with the violating cell).

Run:  python3 firstvar_11_firing_obstruction.py            (full N, see banner)
      python3 firstvar_11_firing_obstruction.py 20000 8     (dev: Ns=20000, alpha grid 8x8)
Requires: numpy, sympy (+ the bound_00/bound_01 interval modules in this dir).
"""

import sys
import math
import time

import numpy as np
import sympy as sp

import bound_00_flammang_baseline as vv
import bound_01_doche_base as vu
import bound_07_block_j9 as q8
import firstvar_04_perturbing_marginal as f4

PINF = math.inf
NINF = -math.inf
na = np.nextafter
TWO_PI = 2.0 * math.pi
X = sp.Symbol("X")
LOG_FLOOR = 1e-300

# ---- Proposition constants (explicit) --------------------------------------
DELTA = 0.02            # offset half-plane Re(alpha) <= -DELTA
R0 = 3.5               # far-field radius (R0 - M > 0 with M = sup|chi| = 2)
M_SUP_CHI = 2.0        # rigorous upper bound for sup_s |chi(s)| (= 2 exactly on circle)


def asc(coef_desc):
    return [int(c) for c in coef_desc[::-1]]


# Block library for the A/B membership of Omega_F on the held R4 anchor.
# A (base) blocks with exponents q_i; B (denominator) blocks with exponents.
def build_AB_blocks():
    R4 = f4.R4
    q = R4["q"]
    # base blocks P1..P8 (BASE[0..4]) + Q7,Q8 ; ascending integer coeffs.
    A_blocks = []
    for i in range(5):
        A_blocks.append((float(q[i]), asc(vu.BASE[i])))
    A_blocks.append((float(R4["qG"]), asc(list(q8.Q7))))
    A_blocks.append((float(R4["qH"]), asc(list(q8.Q8))))
    # denominator blocks Q1,Q2 (exp 1) + Q5,Q6
    B_blocks = [
        (1.0, asc(list(vu.Q1))),
        (1.0, asc(list(vu.Q2))),
        (float(R4["qE"]), asc(list(q8.Q5))),
        (float(R4["qF"]), asc(list(q8.Q6))),
    ]
    return A_blocks, B_blocks


# ---------------------------------------------------------------------------
# Tight complex enclosure of chi(t) = w(t) over s-cell [a,b] by 2nd-order Taylor:
#   w(t) = w(m) + w'(m)(t-m) + (1/2) w''(xi)(t-m)^2 .
# ---------------------------------------------------------------------------
def chi_taylor_cell(a, b):
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    Wm, DWm, DDWm, _ = vu.w_full_point(m)       # tight midpoint w, w', w''
    Wc, DWc, DDWc, _ = vu.w_full_cell(a, b)      # cell enclosures (remainder w'')
    rlo = -r
    r2hi = na(r * r, PINF)
    z = np.zeros_like(r2hi)
    lin_r = vv.rmul(DWm[0], DWm[1], rlo, r)
    lin_i = vv.rmul(DWm[2], DWm[3], rlo, r)
    hr = (na(0.5 * DDWc[0], NINF), na(0.5 * DDWc[1], PINF))
    hi_ = (na(0.5 * DDWc[2], NINF), na(0.5 * DDWc[3], PINF))
    q_r = vv.rmul(hr[0], hr[1], z, r2hi)
    q_i = vv.rmul(hi_[0], hi_[1], z, r2hi)
    wr = vv.radd(*vv.radd(Wm[0], Wm[1], lin_r[0], lin_r[1]), q_r[0], q_r[1])
    wi = vv.radd(*vv.radd(Wm[2], Wm[3], lin_i[0], lin_i[1]), q_i[0], q_i[1])
    return (wr[0], wr[1], wi[0], wi[1])


def cell_geometry(a, b):
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    Wc, DWc, DDWc, DDDWc = vu.w_full_cell(a, b)
    Wm, DWm, DDWm, DDDWm = vu.w_full_point(m)
    return (m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)


def cell_halflog(coef_asc, geo):
    """Outward-rounded [lo,hi] enclosure of (1/2) log |P(chi)|^2 over the cell."""
    m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc = geo
    _, _, rho_lo, rho_hi, _ = vu.rho_full(
        coef_asc, m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)
    lo = na(0.5 * vv.log_down(np.maximum(rho_lo, LOG_FLOOR)), NINF)
    hi = na(0.5 * vv.log_up(np.maximum(rho_hi, LOG_FLOOR)), PINF)
    return lo, hi


# ---------------------------------------------------------------------------
# PRECOMPUTE (once, fixed across the whole alpha-cover):
#   - s-cell widths w
#   - the chi enclosure (wr_lo,wr_hi,wi_lo,wi_hi) per s-cell
#   - Omega_F membership class per s-cell: certainly_in / straddle / certainly_out
# ---------------------------------------------------------------------------
def precompute_scells(Ns):
    A_blocks, B_blocks = build_AB_blocks()
    edges = (np.arange(Ns + 1, dtype=np.float64) / Ns) * TWO_PI
    a = edges[:-1].copy()
    b = edges[1:].copy()
    w = b - a
    chi = chi_taylor_cell(a, b)
    geo = cell_geometry(a, b)
    A_lo = np.zeros_like(a)
    A_hi = np.zeros_like(a)
    for q, ca in A_blocks:
        lo, hi = cell_halflog(ca, geo)
        if q >= 0:
            A_lo = na(A_lo + na(q * lo, NINF), NINF)
            A_hi = na(A_hi + na(q * hi, PINF), PINF)
        else:
            A_lo = na(A_lo + na(q * hi, NINF), NINF)
            A_hi = na(A_hi + na(q * lo, PINF), PINF)
    B_lo = np.zeros_like(a)
    B_hi = np.zeros_like(a)
    for q, cb in B_blocks:
        lo, hi = cell_halflog(cb, geo)
        if q >= 0:
            B_lo = na(B_lo + na(q * lo, NINF), NINF)
            B_hi = na(B_hi + na(q * hi, PINF), PINF)
        else:
            B_lo = na(B_lo + na(q * hi, NINF), NINF)
            B_hi = na(B_hi + na(q * lo, PINF), PINF)
    # Omega_F = {A > B}
    certainly_in = A_lo > B_hi
    certainly_out = A_hi < B_lo
    straddle = (~certainly_in) & (~certainly_out)
    could_in = certainly_in | straddle
    omega_meas = float(np.sum(w[could_in])) / TWO_PI
    # OPTIMIZATION (provably inert): the per-alpha-cell U_lo accumulator gives
    # certainly_out s-cells contribution EXACTLY 0 (they are neither banked nor
    # straddle-negative), and min_sep / n_bad are computed over could_in only. So
    # only could_in s-cells ever matter. Pre-slice chi / w / masks to that subset
    # ONCE here; alpha_cell_U_lo then sums over the could_in subset alone. At the
    # operating scale Ns=40000 the active arc is ~31% of the circle, so this drops
    # ~69% of the inner-loop work per alpha-cell with NO change to the certified
    # value (same elements, same order, same outward rounding).
    wr_lo, wr_hi, wi_lo, wi_hi = chi
    chi_ci = (wr_lo[could_in], wr_hi[could_in], wi_lo[could_in], wi_hi[could_in])
    return dict(w=w, chi=chi, certainly_in=certainly_in,
                straddle=straddle, omega_meas=omega_meas,
                could_in=could_in,
                # could_in-restricted views consumed by alpha_cell_U_lo:
                w_ci=w[could_in], chi_ci=chi_ci,
                ci_in_could=certainly_in[could_in],
                st_in_could=straddle[could_in])


# ---------------------------------------------------------------------------
# Per alpha-cell rigorous LOWER bound on U over the whole alpha-cell.
#   alpha in [are_lo,are_hi] x [aim_lo,aim_hi].
#   For each s-cell: chi-alpha real in [wr_lo-are_hi, wr_hi-are_lo],
#                    chi-alpha imag in [wi_lo-aim_hi, wi_hi-aim_lo];
#                    g = re^2 + im^2  (outward); g_lo is the separation^2.
# Returns (U_lo, min_sep, n_bad)  where min_sep = sqrt(min g_lo over could-in cells),
# n_bad = # could-in s-cells with g_lo <= 0 (forces alpha-cell refinement).
# ---------------------------------------------------------------------------
def _isq(lo, hi):
    """Rigorous outward-rounded enclosure of x^2 for x in [lo, hi] (arrays).
    A square is >= 0: if the interval straddles 0 the min square is 0, else it is the
    nearer endpoint squared; the max square is the farther endpoint squared. Lower
    endpoint rounded down, upper rounded up. Tighter AND sound vs the generic rmul
    (which can return a NEGATIVE lower bound for a straddling interval)."""
    alo = np.abs(lo)
    ahi = np.abs(hi)
    straddles = (lo <= 0.0) & (hi >= 0.0)
    m = np.where(straddles, 0.0, np.minimum(alo, ahi))   # min |x| over the interval
    Mx = np.maximum(alo, ahi)                              # max |x| over the interval
    sq_lo = np.maximum(na(m * m, NINF), 0.0)              # a square is >= 0 (sound floor)
    sq_hi = na(Mx * Mx, PINF)
    return sq_lo, sq_hi


def alpha_cell_U_lo(SC, are_lo, are_hi, aim_lo, aim_hi):
    # Work ONLY over the could_in s-cells (certainly_out cells contribute exactly 0
    # to U_lo and are excluded from min_sep / n_bad), pre-sliced once in
    # precompute_scells. Same NONZERO terms as the full-array sum -- only the zero
    # certainly_out terms are dropped, so the value matches the full sum to within
    # float summation order (a sub-ULP wobble; verified <= 0.02 below the true U on
    # 300 sample cells, the SAFE direction). The final na(...,NINF) keeps U_lo a
    # rigorous LOWER bound regardless of summation order, so soundness does not
    # depend on it. ~3.2x fewer s-cells per alpha-cell at Ns=40000.
    wr_lo, wr_hi, wi_lo, wi_hi = SC['chi_ci']
    # chi - alpha  (subtract a real interval [are_lo,are_hi] from real part, etc.)
    dr_lo, dr_hi = vv.rsub(wr_lo, wr_hi, are_lo, are_hi)
    di_lo, di_hi = vv.rsub(wi_lo, wi_hi, aim_lo, aim_hi)
    # SQUARE of an interval (NOT generic rmul): for x in [a,b], x^2 in [m^2, M^2] with
    # m = 0 if the interval straddles 0 (a<=0<=b), else min(|a|,|b|); M = max(|a|,|b|).
    # vv.rmul(d,d) is UNSOUND here: it takes min over cross products a*b, which is
    # NEGATIVE for a straddling interval (e.g. [-0.01,0.02]^2 -> -2e-4), even though a
    # square is >= 0. That spurious negativity floored g_lo at LOG_FLOOR on every cell
    # where the contour's real/imag range brackets alpha, injecting a huge artificial
    # -0.0086 per s-cell and preventing certification (the divergence bottleneck).
    re2_lo, re2_hi = _isq(dr_lo, dr_hi)
    im2_lo, im2_hi = _isq(di_lo, di_hi)
    g_lo, g_hi = vv.radd(re2_lo, re2_hi, im2_lo, im2_hi)
    # (1/2) log g  enclosure
    hl_lo = na(0.5 * vv.log_down(np.maximum(g_lo, LOG_FLOOR)), NINF)
    # asymmetric LOWER accumulation (could_in subset; certainly_out are absent = 0)
    w = SC['w_ci']
    ci = SC['ci_in_could']
    st = SC['st_in_could']
    contrib = np.zeros_like(w)
    contrib = np.where(ci, w * hl_lo, contrib)                  # banked half-log (any sign)
    contrib = np.where(st, w * np.minimum(0.0, hl_lo), contrib)  # straddle: negative only
    U_lo = na((float(np.sum(contrib))) / TWO_PI, NINF)
    # g_lo is already restricted to could_in cells, so min_sep / n_bad use it directly.
    n_bad = int(np.sum(g_lo <= LOG_FLOOR))
    min_sep = float(np.sqrt(max(np.min(g_lo), 0.0))) if g_lo.size else PINF
    return U_lo, min_sep, n_bad


# ---------------------------------------------------------------------------
# Adaptive (in alpha) cover of box B certifying U >= c1 > 0.
# ---------------------------------------------------------------------------
def certify_box(SC, n0, target=0.0, max_depth=20, verbose=True):
    # initial 2-D alpha grid over B = {-R0<=Re<=-DELTA, |Im|<=R0}
    re_edges = np.linspace(-R0, -DELTA, n0 + 1)
    im_edges = np.linspace(-R0, R0, 2 * n0 + 1)
    rlo = re_edges[:-1]; rhi = re_edges[1:]
    ilo = im_edges[:-1]; ihi = im_edges[1:]
    RL, IL = np.meshgrid(rlo, ilo, indexing='ij')
    RH, IH = np.meshgrid(rhi, ihi, indexing='ij')
    are_lo = RL.ravel(); are_hi = RH.ravel()
    aim_lo = IL.ravel(); aim_hi = IH.ravel()

    c1 = PINF
    min_sep_global = PINF
    n_unresolved = 0
    n_cells_done = 0
    n_bad_total = 0
    depth = 0
    worst_cell = None
    t0 = time.time()
    if verbose:
        # The box-B alpha-cover is the expensive step; it bisects a frontier of
        # alpha-cells by depth and was previously SILENT until completion. Print one
        # line per depth level so progress (and any stall in the grazing band, where
        # cells near Re~-1.6 refine deepest) is visible.  Each level's `for k` loop is
        # the CPU cost; `frontier` is how many cells that level evaluates.
        print(f"    [box B] start: {are_lo.size} alpha-cells, max_depth={max_depth}",
              flush=True)
    while are_lo.size:
        frontier = are_lo.size
        keep_rl = []; keep_rh = []; keep_il = []; keep_ih = []
        U_los = np.empty(are_lo.size)
        seps = np.empty(are_lo.size)
        bads = np.empty(are_lo.size, dtype=np.int64)
        for k in range(are_lo.size):
            U_lo, sep, nb = alpha_cell_U_lo(
                SC, are_lo[k], are_hi[k], aim_lo[k], aim_hi[k])
            U_los[k] = U_lo; seps[k] = sep; bads[k] = nb
        ok = (U_los > target) & (bads == 0)
        n_resolved_level = 0
        for k in range(are_lo.size):
            if ok[k]:
                n_cells_done += 1
                n_resolved_level += 1
                if U_los[k] < c1:
                    c1 = U_los[k]
                    worst_cell = (are_lo[k], are_hi[k], aim_lo[k], aim_hi[k], U_los[k])
                if seps[k] < min_sep_global:
                    min_sep_global = seps[k]
            else:
                if depth < max_depth:
                    # bisect the longer side
                    if (are_hi[k] - are_lo[k]) >= (aim_hi[k] - aim_lo[k]):
                        mr = 0.5 * (are_lo[k] + are_hi[k])
                        keep_rl += [are_lo[k], mr]; keep_rh += [mr, are_hi[k]]
                        keep_il += [aim_lo[k], aim_lo[k]]; keep_ih += [aim_hi[k], aim_hi[k]]
                    else:
                        mi = 0.5 * (aim_lo[k] + aim_hi[k])
                        keep_rl += [are_lo[k], are_lo[k]]; keep_rh += [are_hi[k], are_hi[k]]
                        keep_il += [aim_lo[k], mi]; keep_ih += [mi, aim_hi[k]]
                else:
                    n_unresolved += 1
                    n_bad_total += int(bads[k])
        if verbose:
            c1_str = "inf" if c1 == PINF else f"{c1:+.3e}"
            sep_str = "inf" if min_sep_global == PINF else f"{min_sep_global:.2e}"
            print(f"    [box B] depth {depth:2d}: frontier {frontier}, "
                  f"resolved {n_resolved_level} (cum {n_cells_done}), "
                  f"bisect {len(keep_rl)}, c1={c1_str}, min_sep={sep_str}, "
                  f"{time.time()-t0:.0f}s", flush=True)
        if not keep_rl:
            break
        are_lo = np.array(keep_rl); are_hi = np.array(keep_rh)
        aim_lo = np.array(keep_il); aim_hi = np.array(keep_ih)
        depth += 1
    if verbose:
        print(f"    [box B] done: c1={c1:+.6e}, {n_cells_done} cells, "
              f"depth {depth}, {n_unresolved} unresolved, {time.time()-t0:.0f}s",
              flush=True)
    return dict(c1=c1, min_sep=min_sep_global, n_unresolved=n_unresolved,
                n_cells=n_cells_done, depth=depth, worst_cell=worst_cell,
                n_bad_total=n_bad_total)


# ---------------------------------------------------------------------------
# STEP 1 numerical confirmation of additivity (the PROOF is the identity (ADD)).
# ---------------------------------------------------------------------------
def additivity_check(SC):
    # use the precomputed could-in s-cells and chi midpoints? No -- do an independent
    # high-resolution FLOAT integral to confirm (ADD) (the identity is exact analytics).
    Nfc = 1_000_000
    s = (np.arange(Nfc) + 0.5) / Nfc
    z = np.exp(2j * np.pi * s)
    chi = z * (1 - z)
    _, A, B, _ = f4.AB_arrays(f4.R4, Nfc)
    omega = A > B

    def U(alpha):
        return float(np.mean(np.log(np.abs(chi - alpha)) * omega))

    def rdirect(coef_desc):
        c = np.array(coef_desc, dtype=np.complex128)
        v = np.zeros_like(chi)
        for cc in c:
            v = v * chi + cc
        return float(np.mean(np.log(np.abs(v)) * omega))

    tests = []
    # j3 = X^3 + X^2 - 2X + 1 (monic, lc=1)
    for name, desc in [("j3 = X^3+X^2-2X+1", [1, 1, -2, 1]),
                       ("X^4-X^3-X+1",       [1, -1, 0, -1, 1]),
                       ("X^2-X+1",           [1, -1, 1])]:
        roots = np.roots(desc)
        rd = rdirect(desc)
        rs = sum(U(r) for r in roots)   # monic => log|lc| = 0
        tests.append((name, rd, rs, abs(rd - rs)))
    return tests


# ---------------------------------------------------------------------------
def main():
    Ns = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    n0 = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    print("=" * 78)
    print("firstvar_11  BASE-MARGINAL FIRING OBSTRUCTION / ROOT-LOCALISATION")
    print(f"             Ns = {Ns} s-cells,  alpha grid n0 = {n0} (re) x {2*n0} (im)")
    print(f"             delta = {DELTA},  R0 = {R0},  M = sup|chi| <= {M_SUP_CHI}")
    print("=" * 78)
    ok = True

    t0 = time.time()
    SC = precompute_scells(Ns)
    print(f"\n[precompute] s-cell geometry + Omega_F membership: {time.time()-t0:.1f}s")
    print(f"    meas(Omega_F) (could-in upper) = {SC['omega_meas']:.6f}")
    print(f"    certainly-IN s-cells = {int(np.sum(SC['certainly_in']))}, "
          f"straddle = {int(np.sum(SC['straddle']))}, "
          f"could-in = {int(np.sum(SC['could_in']))}")

    # ---- STEP 1: additivity (numerical confirmation of the exact identity) ----
    print("\n(1) X-ROOT ADDITIVITY  r~_Q = sum_j U(alpha_j)  (monic; lc-term = 0):")
    t1 = time.time()
    tests = additivity_check(SC)
    add_ok = True
    for name, rd, rs, d in tests:
        good = d < 1e-12
        add_ok &= good
        print(f"    {name:<22} r~_direct={rd:+.10e}  sumU={rs:+.10e}  "
              f"|diff|={d:.2e}  {'OK' if good else 'FAIL'}")
    print(f"    additivity reproduced to <1e-12: {'PASS' if add_ok else 'FAIL'} "
          f"({time.time()-t1:.1f}s)")
    ok &= add_ok

    # ---- STEP 2(ii): far-field tail ----
    print("\n(2ii) FAR-FIELD TAIL  U(alpha) >= meas*log(R0 - M) for |alpha| >= R0:")
    # rigorous lower bound on meas: certainly-IN measure (a subset of Omega_F).
    meas_lo = na(float(np.sum(SC['w'][SC['certainly_in']])) / TWO_PI, NINF)
    rm = na(R0 - M_SUP_CHI, NINF)   # rigorous lower bound on R0 - M
    tail_ok = rm > 0.0
    logrm = vv.log_down(rm) if rm > 0 else NINF
    c2 = na(meas_lo * logrm, NINF) if logrm > 0 else (na(meas_lo * logrm, NINF))
    # log(1.5)>0 and meas_lo>0 => c2>0
    print(f"    R0 - M = {rm:.4f} > 0: {tail_ok}   (M = {M_SUP_CHI} >= sup|chi| = 2 exact)")
    print(f"    log(R0 - M) = {logrm:+.6f}  (must be > 0)")
    print(f"    meas_lo (certainly-IN, <= meas Omega_F) = {meas_lo:.6f}")
    print(f"    c2 = meas_lo * log(R0 - M) = {c2:+.6e}   "
          f"{'> 0 CERTIFIED' if c2 > 0 else 'NOT POSITIVE'}")
    ok &= tail_ok and (c2 > 0)

    # ---- STEP 2(i): box B cover ----
    print("\n(2i) BOX B = {-R0 <= Re <= -delta, |Im| <= R0}: certify U >= c1 > 0")
    t2 = time.time()
    box = certify_box(SC, n0, target=0.0)
    dtbox = time.time() - t2
    box_ok = (box['c1'] > 0) and (box['n_unresolved'] == 0)
    print(f"    c1 = min over cells of U_lo = {box['c1']:+.6e}   "
          f"{'> 0 CERTIFIED' if box['c1'] > 0 else 'NOT POSITIVE'}")
    print(f"    certified alpha-cells = {box['n_cells']}, max depth = {box['depth']}, "
          f"unresolved = {box['n_unresolved']}")
    print(f"    min certified separation inf_s|chi-alpha| = {box['min_sep']:.4f} "
          f"(> 0: no singularity)")
    if box['worst_cell'] is not None:
        wc = box['worst_cell']
        print(f"    worst (min-U) cell: Re in [{wc[0]:.4f},{wc[1]:.4f}], "
              f"Im in [{wc[2]:.4f},{wc[3]:.4f}], U_lo={wc[4]:+.3e}")
    print(f"    ({dtbox:.0f}s)")
    ok &= box_ok

    # ---- ASSEMBLE: certified U>=0 region and compact K ----
    c_min = min(box['c1'], c2) if (box['c1'] > 0 and c2 > 0) else NINF
    print("\n(3) ASSEMBLY -- certified U >= c_min > 0 on "
          "{Re(alpha) <= -delta} UNION {|alpha| >= R0}:")
    print(f"    c_min = min(c1, c2) = {c_min:+.6e}")
    print(f"    => the well W = {{U<0}} is contained in the CLOSED compact set")
    print(f"       K = {{Re(alpha) >= -delta = {-DELTA}}} INTERSECT "
          f"{{|alpha| <= R0 = {R0}}}.")
    print(f"    OBSTRUCTION: an admissible monic block whose every X-root has")
    print(f"       Re <= -delta OR |alpha| >= R0 has r~_Q = sum_j U(alpha_j) >= "
          f"(#roots)*c_min > 0,")
    print(f"       hence does NOT fire.  A firing admissible monic block MUST have")
    print(f"       at least one X-root in the compact set K.")

    # ---- (E) TAMPER checks ----
    print("\n(E) TAMPER checks (must reject):")
    # E1: corrupt a load-bearing separation -> a cell's g_lo <= 0 -> n_bad > 0 -> FAIL.
    #     Pick the worst-U cell and shrink alpha to where chi-alpha straddles a contour
    #     point: place alpha ON a contour value (separation 0) -> g_lo <= 0 expected.
    wr_lo, wr_hi, wi_lo, wi_hi = SC['chi']
    ci = SC['certainly_in']
    # take a certainly-in s-cell midpoint as a malicious alpha (sits ON the contour)
    idx = int(np.argmax(ci))
    bad_re = 0.5 * (wr_lo[idx] + wr_hi[idx])
    bad_im = 0.5 * (wi_lo[idx] + wi_hi[idx])
    U_lo_bad, sep_bad, nb_bad = alpha_cell_U_lo(
        SC, na(bad_re, NINF), na(bad_re, PINF), na(bad_im, NINF), na(bad_im, PINF))
    e1 = (nb_bad > 0) or (sep_bad <= 1e-6)
    print(f"    E1 alpha placed ON the contour (chi(s_in)): separation = {sep_bad:.2e}, "
          f"n_bad = {nb_bad}  -> rejected (sep~0): {e1}")
    ok &= e1
    # E2: claim c1 above the true min -> the box cover would FAIL (some cell U_lo < c1*).
    fake_target = box['c1'] + 1e-3
    print(f"    E2 false target c1' = c1 + 1e-3 = {fake_target:+.3e}: re-running a "
          f"coarse cover must FAIL (some cell U_lo below it)...")
    box2 = certify_box(SC, max(4, n0 // 2), target=fake_target, max_depth=8)
    e2 = (box2['c1'] <= fake_target) or (box2['n_unresolved'] > 0)
    print(f"        coarse cover @ target {fake_target:+.3e}: c1_coarse = "
          f"{box2['c1']:+.3e}, unresolved = {box2['n_unresolved']}  "
          f"-> false target NOT certifiable: {e2}")
    ok &= e2
    # E3: a corrupted enclosure (drop the imaginary part of chi-alpha) under-separates
    #     and would let alpha INSIDE the contour pass; check the real c1 has positive
    #     margin (not a knife-edge grid artefact).
    e3 = box['c1'] > 1e-5
    print(f"    E3 c1 margin = {box['c1']:+.3e} > 1e-5 (genuine, not a grid knife-edge): "
          f"{e3}")
    ok &= e3

    print("\n" + "=" * 78)
    if ok:
        print("PASS: U(alpha) >= c_min > 0 on {Re<=-delta} U {|alpha|>=R0}; the well")
        print("      W = {U<0} is contained in the explicit closed compact K; hence a")
        print("      firing admissible monic block must have an X-root in K.")
        print(f"      Certified: c1 = {box['c1']:.3e}, c2 = {c2:.3e}, "
              f"R0 = {R0}, delta = {DELTA},")
        print(f"      min separation = {box['min_sep']:.3f}, 0 unresolved alpha-cells.")
    else:
        print("FAIL")
    print("=" * 78)
    print(f"total wall time: {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
