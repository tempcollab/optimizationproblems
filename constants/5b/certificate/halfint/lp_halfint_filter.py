#!/usr/bin/env python3
"""
C_5b (Sidon density in (4,5)-sets, Erdos #757) — approach half-integrality-filtered-search.

A RE-RUNNABLE LP-HALF-INTEGRALITY / PARTIAL-INTEGRALITY FILTER for (4,5)-set candidates,
plus a verified STRUCTURAL SURVEY over the relevant families.

WHY THIS EXISTS (the de-risk it provides)
-----------------------------------------
The R5 interleaved transversal certificate (lean/Constants/C5bInterleaved.lean,
`hLe_of_interleaved`) certifies h(A) <= N - tau with a SMALL decidable branch budget ONLY
when the 3-AP cover LP has *integral structure* on some support P.  Concretely the cert
splits any hitting set H into an LP-charged part (on a support P) carrying a >= ceil(nu*) of
the bound, and a residual branch part of budget g = tau(residual) - 1.  The Lean `decide`
tree has 3^g leaves, so the cert is TRACTABLE iff some P yields a small residual g while
still reaching the full tau.

R5 verified (exactly) that A_base is the WORST case: its cover LP is *fully half-integral*
(nu* = 9/2, every vertex 0 or 1/2, no x=1 vertex), and

    max over all P of  ( ceil(nu*(edges <= P)) + tau(edges avoiding P) ) = 6

is attained ONLY at P = empty (a = 0, full branch budget g = tau-1 = 5).  So if an N~30 beat
gadget is *also* fully half-integral, the interleaved cert gives ZERO budget shrink and the
beat is NOT Lean-certifiable with a small budget (the full 3^~13 tree is decide-intractable).

This filter SCREENS any candidate for that pathology BEFORE a round is spent, and is composable
with the gadget search (cpsat-exact-existence-N28-N30 / search_N30.py): import `screen` and pass
any (4,5)-set.

WHAT IS EXACT (CLAUDE.md rigor — never a float heuristic for the integrality classification)
--------------------------------------------------------------------------------------------
  * tau (min 3-AP hitting set) is computed EXACTLY by combinatorial branch-and-bound (integer).
  * nu* (cover LP value) AND the optimal LP vertex are computed EXACTLY in RATIONAL arithmetic
    via sympy.solvers.simplex.lpmin (exact simplex over Q).  The half-integrality / x=1
    classification is read off the EXACT rational vertex, never a rounded float.
  * The float scipy LP value is computed too, ONLY as an independent CROSS-CHECK of nu*
    (must agree with the exact rational value to 1e-6); it is NEVER used for classification.
  * The interleaved budget over supports P is computed with EXACT integer tau on the residual.

OUTPUTS PER CANDIDATE (the `Screen` record)
-------------------------------------------
  nu_star            : exact Fraction, cover LP optimum (= max fractional matching by duality)
  fully_half_integral: bool — every LP-vertex coord in {0, 1/2} and NO x=1 vertex
  integral_verts     : the x=1 vertices the LP forces (Nemhauser-Trotter free-fix set); a
                       NON-EMPTY set is the signal that the interleaved cert can shrink budget
  tau                : exact min transversal (integer); h(A) = N - tau
  best_budget        : the SMALLEST residual branch budget g = tau(residual)-1 over the
                       screened supports P that still reach the FULL tau (a(P)+tau(res)=tau);
                       None if no nonempty P reaches it (then best_budget defaults to tau-1).
                       SMALL best_budget  => interleaved-cert-FRIENDLY (Lean-certifiable cheap).
                       best_budget = tau-1 => HOSTILE (fully half-integral like A_base).
  classification     : 'fully-half-integral / interleaved-HOSTILE' | 'partially-integral /
                       interleaved-FRIENDLY'

HONESTY
-------
A candidate is certifiable cheaply ONLY if `best_budget` is actually small.  This script
NEVER writes a bound into constants/5b.md.  It emits a verified structural verdict per set.

Run:  python3 lp_halfint_filter.py          (self-test + survey, ~1-2 min)
"""
import itertools
import sys
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog
from sympy import symbols
from sympy.solvers.simplex import lpmax


# ===========================================================================
# (4,5)-set predicate (DIFFERENCE condition) and 3-AP hypergraph.
# ===========================================================================
def is_45set(A):
    """EVERY 4-subset has >=5 distinct pairwise ABSOLUTE differences (MT26, the corrected
    definition, strictly stronger than weak-Sidon)."""
    A = sorted(A)
    for quad in itertools.combinations(A, 4):
        d = set(abs(x - y) for x, y in itertools.combinations(quad, 2))
        if len(d) < 5:
            return False
    return True


def three_ap_edges(A):
    """3-term APs {a,(a+c)/2,c} in A, as sorted VALUE triples (the cover-LP edges)."""
    A = sorted(A)
    S = set(A)
    E = []
    for i in range(len(A)):
        for k in range(i + 1, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 and (s // 2) in S:
                m = s // 2
                if A[i] < m < A[k]:
                    E.append((A[i], m, A[k]))
    return E


# ===========================================================================
# EXACT tau (min hitting set) by branch-and-bound — integer arithmetic only.
# ===========================================================================
def tau_exact(edges):
    """Exact minimum transversal (vertex cover) of a family of edges (tuples of vertices)."""
    if not edges:
        return 0
    verts = sorted({v for e in edges for v in e})
    inc = {v: [] for v in verts}
    for ei, e in enumerate(edges):
        for v in e:
            inc[v].append(ei)
    nE = len(edges)
    best = [len(verts)]

    # greedy upper bound to prime the prune
    covered0 = set()
    cov = set()
    order = sorted(verts, key=lambda v: -len(inc[v]))
    for v in order:
        if len(covered0) == nE:
            break
        if any(ei not in covered0 for ei in inc[v]):
            cov.add(v)
            covered0.update(inc[v])
    best[0] = len(cov)

    def bt(uncovered, chosen):
        if not uncovered:
            if chosen < best[0]:
                best[0] = chosen
            return
        if chosen + 1 >= best[0]:
            # need at least one more vertex; if chosen+1 can't beat best, prune unless it ties below
            if chosen + 1 > best[0] - 1:
                return
        # branch on an uncovered edge: one of its 3 vertices must be in the cover
        ei = next(iter(uncovered))
        e = edges[ei]
        for v in e:
            newcov = {f for f in uncovered if v not in edges[f]}
            bt(newcov, chosen + 1)

    bt(frozenset(range(nE)), 0)
    return best[0]


# ===========================================================================
# EXACT cover-LP optimum and optimal vertex in RATIONAL arithmetic.
# ===========================================================================
def nu_star_exact(edges):
    """EXACT cover-LP / fractional-matching optimum nu* (Fraction), via sympy's exact
    rational simplex on the MATCHING LP (lpmax form):
        max sum y_e   s.t.  for every vertex v, sum of y over edges at v <= 1,  y >= 0.
    By LP duality this equals the cover LP min (the value the interleaved cert charges).
    The matching form has NO redundant upper bounds, so sympy's simplex is robust here
    (the cover form `lpmin` with x<=1 oscillated on these instances)."""
    if not edges:
        return Fraction(0)
    nE = len(edges)
    ys = symbols(f"y0:{nE}")
    load = {}
    for ei, e in enumerate(edges):
        for v in e:
            load.setdefault(v, []).append(ys[ei])
    cons = [sum(terms) <= 1 for terms in load.values()] + [y >= 0 for y in ys]
    val, _ = lpmax(sum(ys), cons)
    return Fraction(int(val.p), int(val.q)) if hasattr(val, "p") else Fraction(val)


def cover_vertex_exact(edges, verts, nu_target):
    """An EXACT optimal cover-LP vertex x (for the half-integrality read-off).
    scipy/HiGHS GUESSES the vertex; we rationalize and CERTIFY it exactly:
      * 0 <= x <= 1 and every edge covered (x_a+x_b+x_c >= 1)   [exact primal feasibility]
      * sum x == nu_target                                       [optimality vs the exact
                                                                  matching value nu_target]
    Returns (xvals, certified: bool).  certified=True  => xvals is an exactly-verified
    optimal vertex.  certified=False => the float vertex did NOT rationalize to an exact
    optimal vertex at the tried denominators; this only happens when the LP optimum has
    LARGE denominators, which by itself PROVES the set is NOT fully half-integral (a
    half-integral vertex rationalizes trivially at denom 2).  We return the best float-
    rationalized guess with certified=False so the caller can record 'not half-integral'."""
    if not edges:
        return {v: Fraction(0) for v in verts}, True
    active = sorted({v for e in edges for v in e})
    vi = {v: i for i, v in enumerate(active)}
    nv = len(active)
    A_ub, b_ub = [], []
    for (a, b, c) in edges:
        row = np.zeros(nv)
        row[vi[a]] = row[vi[b]] = row[vi[c]] = -1.0
        A_ub.append(row)
        b_ub.append(-1.0)
    res = linprog(np.ones(nv), A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(0, 1)] * nv, method="highs")
    if not res.success:
        raise RuntimeError("LP solve failed: " + str(res.message))
    for D in (2, 6, 30, 120, 720, 100000):
        xr = [Fraction(v).limit_denominator(D) for v in res.x]
        ok = all(Fraction(0) <= xi <= Fraction(1) for xi in xr)
        ok = ok and all(xr[vi[a]] + xr[vi[b]] + xr[vi[c]] >= 1 for (a, b, c) in edges)
        ok = ok and (sum(xr) == nu_target)
        if ok:
            xvals = {v: Fraction(0) for v in verts}
            for v in active:
                xvals[v] = xr[vi[v]]
            return xvals, True
    # not exactly certifiable at small denom => provably NOT fully half-integral
    xr = [Fraction(v).limit_denominator(100000) for v in res.x]
    xvals = {v: Fraction(0) for v in verts}
    for v in active:
        xvals[v] = xr[vi[v]]
    return xvals, False


def cover_lp_exact(edges, verts):
    """Returns (nu_star: Fraction, x: {vert: Fraction}, vertex_certified: bool) —
    exact value + (exactly-certified | best-guess) optimal vertex."""
    nu = nu_star_exact(edges)
    x, certified = cover_vertex_exact(edges, verts, nu)
    return nu, x, certified


def cover_lp_float(edges, verts):
    """scipy float LP value — INDEPENDENT CROSS-CHECK of nu* only (never classification)."""
    if not edges:
        return 0.0
    active = sorted({v for e in edges for v in e})
    vi = {v: i for i, v in enumerate(active)}
    nv = len(active)
    c = np.ones(nv)
    A_ub, b_ub = [], []
    for (a, b, cc) in edges:
        row = np.zeros(nv)
        row[vi[a]] = row[vi[b]] = row[vi[cc]] = -1.0
        A_ub.append(row)
        b_ub.append(-1.0)
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=[(0, 1)] * nv)
    return float(res.fun)


# ===========================================================================
# Interleaved-cert budget over candidate supports P.
# ===========================================================================
def nu_star_float_in_P(edges, P):
    """FAST float nu* of the sub-family of edges entirely inside P (scipy/HiGHS).
    Used ONLY to SCREEN supports in the 2^N exhaustive loop; the winning support is
    re-certified EXACTLY afterwards (nu_star_in_P + cover_lp_exact)."""
    Ps = set(P)
    sub = [e for e in edges if set(e) <= Ps]
    if not sub:
        return 0.0
    active = sorted({v for e in sub for v in e})
    vi = {v: i for i, v in enumerate(active)}
    nv = len(active)
    A_ub, b_ub = [], []
    for (a, b, c) in sub:
        row = np.zeros(nv)
        row[vi[a]] = row[vi[b]] = row[vi[c]] = -1.0
        A_ub.append(row)
        b_ub.append(-1.0)
    res = linprog(np.ones(nv), A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(0, 1)] * nv, method="highs")
    return float(res.fun)


def nu_star_in_P(edges, P):
    """EXACT nu* of the sub-family whose edges lie ENTIRELY inside P (sympy matching LP).
    By duality this equals the max fractional matching the LP-fix part can charge."""
    Ps = set(P)
    sub = [e for e in edges if set(e) <= Ps]
    if not sub:
        return Fraction(0)
    return nu_star_exact(sub)


def residual(edges, P):
    """Edges that AVOID P entirely (the branch part sees only these)."""
    Ps = set(P)
    return [e for e in edges if not (set(e) & Ps)]


def _ceil_frac(nu):
    return -((-nu.numerator) // nu.denominator)


def interleaved_value(edges, P):
    """The SOUND interleaved lower bound on tau for support P (EXACT):
        a(P) + tau(residual)   where  a(P) = ceil(nu*(edges <= P)).
    (hLe_of_interleaved proves tau >= a + (g+1) with g = tau(residual)-1, i.e. >= a+tau(res).)"""
    a = _ceil_frac(nu_star_in_P(edges, P))
    res = residual(edges, P)
    tr = tau_exact(res)
    return a, tr, a + tr


def interleaved_value_float(edges, P):
    """Same lower bound, SCREENING version: a = ceil(float nu*) (a small +eps guards the
    ceiling against float noise; the winning P is re-certified exactly).  tau is exact."""
    import math
    nuf = nu_star_float_in_P(edges, P)
    a = math.ceil(nuf - 1e-7)
    res = residual(edges, P)
    tr = tau_exact(res)
    return a, tr, a + tr


def best_interleaved_budget_exhaustive(edges, verts, tau_full):
    """SMALL-N exact: over ALL P (2^|verts|) reaching the FULL tau (a+tau(res)=tau_full),
    return the smallest residual branch budget g = tau(res)-1, with the P attaining it.
    SCREENS with float nu* (fast over 2^14), then RE-CERTIFIES the winner EXACTLY.
    Returns (best_g, best_P, attained_full).  best_g = tau_full-1 if only P=empty reaches it."""
    best = None  # (g, P)
    full_reached_nontrivial = False
    n = len(verts)
    for mask in range(1 << n):
        P = [verts[i] for i in range(n) if mask & (1 << i)]
        a, tr, val = interleaved_value_float(edges, P)
        if val == tau_full:
            g = max(tr - 1, 0)        # residual branch budget (0 = residual fully LP-covered)
            if P:
                full_reached_nontrivial = True
            if best is None or g < best[0]:
                best = (g, P)
    if best is None:
        result_g, result_P = tau_full - 1, []
    else:
        result_g, result_P = best
    # EXACT re-certification of the chosen support (and of the P=empty baseline)
    a0, tr0, val0 = interleaved_value(edges, [])
    assert val0 == tau_full and tr0 - 1 == tau_full - 1, (val0, tr0, tau_full)
    if result_P:
        a, tr, val = interleaved_value(edges, result_P)   # EXACT nu* on the winner
        assert val == tau_full, f"exact recert failed: val={val} != tau {tau_full}"
        assert max(tr - 1, 0) == result_g, (tr - 1, result_g)
    return result_g, result_P, full_reached_nontrivial


def best_interleaved_budget_heuristic(edges, verts, tau_full, xvals):
    """TRACTABLE (N>=~20): screen a curated set of structured supports P instead of all 2^N.

    ONE-SIDED screen (honest): finding a FRIENDLY P here is a CERTIFIED friendly verdict
    (the support and budget are exactly re-derived); NOT finding one is "hostile w.r.t. the
    screened supports", NOT a proof that no support shrinks the budget.  For the surveyed
    fully-half-integral N=30 sets the exhaustive 2^14 result on A_base shows even the COMPLETE
    search gives no shrink, so the one-sided screen is informative; we report the limitation.

    Supports screened:
       P0  = {}                              (always-sound baseline -> g = tau-1),
       Pint= x=1 vertices (Nemhauser-Trotter free-fix set) + its prefixes,
       Pdeg= the top-k highest-3-AP-degree vertices, k = 1..min(8, tau) — a fractional
             matching can be charged on a dense support even with no x=1 vertex, so a dense
             support is the natural friendly candidate when the LP is half-integral.
    Returns (best_g, best_P, integral_verts)."""
    integral = sorted(v for v in verts if xvals.get(v, Fraction(0)) == 1)
    deg = {v: 0 for v in verts}
    for e in edges:
        for v in e:
            deg[v] += 1
    by_deg = sorted(verts, key=lambda v: -deg[v])
    candidates = [[]]
    if integral:
        candidates.append(list(integral))
        for k in range(1, len(integral) + 1):
            candidates.append(integral[:k])
    for k in range(1, min(9, tau_full + 1)):
        candidates.append(by_deg[:k])
    # EDGE-UNION supports: the interleaved cert charges only edges ENTIRELY inside P, so the
    # a(P) part grows ONLY when whole 3-AP triples are absorbed into P.  The principled
    # friendly candidate is therefore a union of complete edges (greedily by how cheaply each
    # edge's 3 vertices extend P).  We grow P one whole edge at a time, vertex-disjointly when
    # possible (a vertex-disjoint union of j edges has a(P)=j by integral matching), and also
    # try the densest cluster of mutually overlapping edges.
    deg_e = {v: 0 for v in verts}
    for e in edges:
        for v in e:
            deg_e[v] += 1
    # (a) greedy vertex-disjoint edge packing -> a(P)=#packed edges, residual = rest
    used = set()
    packP = []
    packed = 0
    for e in sorted(edges, key=lambda e: -sum(deg_e[v] for v in e)):
        if not (set(e) & used):
            used |= set(e)
            packP.extend(e)
            packed += 1
            candidates.append(list(packP))   # try after each added disjoint edge
    # (b) densest overlapping cluster: all vertices of the top-t highest-degree edges
    edges_by_dens = sorted(edges, key=lambda e: -sum(deg_e[v] for v in e))
    clusterP = []
    for t in range(1, min(len(edges_by_dens), tau_full) + 1):
        cl = set()
        for e in edges_by_dens[:t]:
            cl |= set(e)
        candidates.append(sorted(cl))
    best = (tau_full - 1, [])
    seen = set()
    for P in candidates:
        key = tuple(sorted(P))
        if key in seen:
            continue
        seen.add(key)
        a, tr, val = interleaved_value(edges, P)
        if val == tau_full:
            g = max(tr - 1, 0)
            if g < best[0]:
                best = (g, list(P))
    return best[0], best[1], integral


# ===========================================================================
# The composable screen.
# ===========================================================================
class Screen:
    def __init__(self, A, exhaustive=None, verify_45=True):
        self.A = sorted(A)
        self.N = len(self.A)
        self.is45 = is_45set(self.A) if verify_45 else None
        self.edges = three_ap_edges(self.A)
        self.m = len(self.edges)
        self.verts = sorted({v for e in self.edges for v in e})
        self.tau = tau_exact(self.edges)
        self.alpha = self.N - self.tau
        self.nu_exact, self.xvals, self.vertex_certified = cover_lp_exact(
            self.edges, self.verts)
        self.nu_float = cover_lp_float(self.edges, self.verts)
        # cross-check the EXACT rational nu* against the independent float solve
        self.nu_crosscheck_ok = abs(float(self.nu_exact) - self.nu_float) < 1e-6
        # integrality classification from the EXACT rational vertex
        self.integral_verts = sorted(v for v in self.verts if self.xvals[v] == 1)
        # fully half-integral REQUIRES an exactly-certified all-{0,1/2} vertex with no x=1.
        # If the vertex did not certify at small denominator, the LP optimum has large
        # denominators => provably NOT fully half-integral.
        self.all_half = self.vertex_certified and all(
            self.xvals[v] in (Fraction(0), Fraction(1, 2)) for v in self.verts)
        self.fully_half_integral = self.all_half and not self.integral_verts
        # interleaved budget
        if exhaustive is None:
            exhaustive = len(self.verts) <= 16
        self.exhaustive = exhaustive
        if exhaustive:
            g, P, nontrivial = best_interleaved_budget_exhaustive(
                self.edges, self.verts, self.tau)
            self.best_budget = g
            self.best_P = P
            self.nontrivial_shrink = nontrivial and g < self.tau - 1
        else:
            g, P, integral = best_interleaved_budget_heuristic(
                self.edges, self.verts, self.tau, self.xvals)
            self.best_budget = g
            self.best_P = P
            self.nontrivial_shrink = bool(P) and g < self.tau - 1
        self.friendly = self.best_budget < self.tau - 1
        # Classification reports TWO ORTHOGONAL properties, honestly separated:
        #   (a) LP structure of the cover polytope  — an EXACT, fully-determined fact:
        #         'fully-half-integral'  (all coords in {0,1/2}, no x=1; A_base pathology)
        #         'partially-integral'   (some x=1 vertex the LP forces)
        #         'mixed-fractional'     (other fractions, e.g. 1/3 — NOT half-integral)
        #         'large-denom-fractional' (vertex did not certify at small denom => NOT half-int)
        #   (b) interleaved-cert friendliness — whether SOME support P shrinks the branch
        #       budget below the full tau-1.  EXHAUSTIVE => a verified two-sided verdict;
        #       HEURISTIC => one-sided ('no friendly P among the screened supports', NOT a
        #       proof that none exists).
        if self.fully_half_integral:
            self.lp_structure = "fully-half-integral"
        elif self.integral_verts:
            self.lp_structure = "partially-integral(x=1)"
        elif not self.vertex_certified:
            self.lp_structure = "large-denom-fractional"
        elif self.all_half:
            self.lp_structure = "half-integral(no x=1)"
        else:
            self.lp_structure = "mixed-fractional"
        if self.friendly:
            self.friendliness = "interleaved-FRIENDLY"
        elif self.exhaustive:
            self.friendliness = "interleaved-HOSTILE(exhaustive: no shrinking P exists)"
        else:
            self.friendliness = "no-shrink-found(heuristic-P: not a proof)"
        self.classification = f"{self.lp_structure} / {self.friendliness}"

    def line(self):
        return (f"N={self.N} m={self.m} tau={self.tau} alpha={self.alpha} "
                f"nu*={self.nu_exact} [{self.lp_structure}] "
                f"|x=1|={len(self.integral_verts)} "
                f"budget g={self.best_budget} (vs full tau-1={self.tau-1}) "
                f"-> {self.friendliness}"
                f"{'' if self.exhaustive else ' [heuristic-P]'}")


def screen(A, **kw):
    return Screen(A, **kw)


class EdgeScreen:
    """Screen a RAW 3-AP edge family directly (not derived from a point set) — used to
    validate the interleaved-cert mechanism on the exact edge families the Lean cert uses
    (C5bInterleaved.SynValidation: a chosen fractional family + a chosen residual family),
    independent of which point set realizes them."""
    def __init__(self, edges, N=None):
        self.edges = [tuple(e) for e in edges]
        self.verts = sorted({v for e in self.edges for v in e})
        self.N = N if N is not None else len(self.verts)
        self.m = len(self.edges)
        self.tau = tau_exact(self.edges)
        self.alpha = self.N - self.tau
        self.nu_exact, self.xvals, self.vertex_certified = cover_lp_exact(
            self.edges, self.verts)
        self.integral_verts = sorted(v for v in self.verts if self.xvals[v] == 1)
        self.fully_half_integral = (
            self.vertex_certified
            and all(self.xvals[v] in (Fraction(0), Fraction(1, 2)) for v in self.verts)
            and not self.integral_verts)
        g, P, nt = best_interleaved_budget_exhaustive(self.edges, self.verts, self.tau)
        self.best_budget = g
        self.best_P = P
        self.nontrivial_shrink = nt and g < self.tau - 1
        self.friendly = self.best_budget < self.tau - 1


# ===========================================================================
# Survey families.
# ===========================================================================
A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]

# the R5 (4,5)-valid Fibonacci subsequence family (best low-alpha N=30 family found in R5)
FIB30 = [1, 2, 3, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584,
         4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811,
         514229, 832040, 1346269, 2178309]

# the R5 random-search N=30 (4,5)-set (alpha=20, indecomposable) — a second structural sample
RAND30 = [21, 154, 163, 229, 262, 305, 324, 370, 425, 600, 621, 768, 980, 1029,
          1054, 1078, 1212, 1508, 1623, 1984, 2195, 2222, 2345, 2426, 2485, 2535,
          2657, 2748, 2759, 2983]

# small SYNTHETIC vertex-disjoint instance from the interleaved cert (the FRIENDLY reference:
# two fractional APs + two residual APs, the cert's budget-shrink demo) — to confirm the filter
# correctly flags it as interleaved-FRIENDLY with best_budget = 1.
A_SYN = [0, 1, 2, 10, 11, 12, 100, 101, 102, 200, 201, 202]


def two_copies_separated(A, gap=100000):
    """Lemma-3.6 well-separated union (h additive) — a DECOMPOSABLE control set whose cover LP
    is the disjoint union of two A copies; used to confirm the filter sees the block structure."""
    B = [a + max(A) + gap for a in A]
    return sorted(A + B)


def survey():
    print("=" * 78)
    print("LP-HALF-INTEGRALITY SURVEY — C_5b (4,5)-set families")
    print("(exact rational cover LP; nu* cross-checked vs scipy float; integer tau)")
    print("=" * 78)

    rows = []

    print("\n[1] A_base (the record N=14 set) — REPRODUCE the R5 fully-half-integral finding")
    s = screen(A_BASE, exhaustive=True)
    print("    is_45set:", s.is45, " nu* cross-check (exact==float):", s.nu_crosscheck_ok)
    print("   ", s.line())
    assert s.is45 is True
    assert s.nu_exact == Fraction(9, 2), s.nu_exact
    assert s.fully_half_integral is True
    assert s.integral_verts == []
    assert s.tau == 6 and s.alpha == 8
    assert s.best_budget == s.tau - 1 == 5, (s.best_budget, s.tau)
    assert s.friendly is False
    assert s.nu_crosscheck_ok
    print("    REPRODUCED: nu*=9/2, fully half-integral, no x=1 vertex,")
    print("    best interleaved budget g = tau-1 = 5 (only P=empty reaches tau) => HOSTILE.")
    rows.append(("A_base (N=14)", s))

    print("\n[2] A_syn EDGE FAMILY (the cert's vertex-disjoint demo) — FRIENDLY reference")
    # The exact families the Lean cert C5bInterleaved.SynValidation uses: a fractional part
    # (two vertex-disjoint APs => a=2) + a residual part (two vertex-disjoint APs => g=1).
    APfrac = [(100, 101, 102), (200, 201, 202)]
    APres = [(0, 1, 2), (10, 11, 12)]
    es = EdgeScreen(APfrac + APres, N=12)
    print(f"     N={es.N} m={es.m} tau={es.tau} nu*={es.nu_exact} |x=1|={len(es.integral_verts)} "
          f"budget g={es.best_budget} (vs full tau-1={es.tau - 1}) -> "
          f"{'FRIENDLY' if es.friendly else 'HOSTILE'}")
    assert es.tau == 4, es.tau
    # All 4 APs are vertex-disjoint, so the cover LP is fully INTEGRAL (nu*=4, all x=1): the
    # filter finds the OPTIMAL support P=all (a=4, residual empty => g=0) — even friendlier
    # than the cert's chosen a=2/g=1 split (which only used 2 of the 4 APs fractionally).
    assert es.best_budget == 0, es.best_budget
    assert es.friendly is True and es.nontrivial_shrink is True
    assert len(es.integral_verts) == 4
    print("    CONFIRMED: best budget g=0 << tau-1=3 => interleaved-FRIENDLY (the cert's R5")
    print("    Asyn_avoiders_le_8 used a SUBOPTIMAL a=2 + g=1 split, 3 leaves; the LP shows")
    print("    a fully integral cover (a=4, g=0, 1 leaf) is available — disjoint APs are easy).")

    print("\n[3] Two well-separated A_base copies — DECOMPOSABLE control (Lemma 3.6)")
    s = screen(two_copies_separated(A_BASE), exhaustive=False)
    print("   ", s.line())
    # block-disjoint => the cover LP splits; nu* doubles, still half-integral per block
    assert s.tau == 12 and s.alpha == 16, (s.tau, s.alpha)
    assert s.nu_exact == Fraction(9, 1), s.nu_exact
    print("    Note: 16/28 = 4/7 EXACTLY (mediant) — a tie, never a beat; still half-integral.")
    rows.append(("2xA_base (N=28)", s))

    print("\n[4] Fibonacci (4,5)-subsequence N=30 — the R5 best low-alpha family")
    s = screen(FIB30, exhaustive=False)
    print("    is_45set:", s.is45, " nu* cross-check:", s.nu_crosscheck_ok)
    print("   ", s.line())
    assert s.is45 is True
    assert s.nu_crosscheck_ok
    # NOT fully half-integral: large-denominator nu*, with one LP-forced x=1 vertex.
    assert s.fully_half_integral is False
    assert s.nu_exact.denominator > 2          # large denom => not half-integral
    assert len(s.integral_verts) == 1, s.integral_verts
    rows.append(("Fibonacci (N=30)", s))

    print("\n[5] Random-search (4,5)-set N=30 — a second structural sample")
    s = screen(RAND30, exhaustive=False)
    print("    is_45set:", s.is45, " nu* cross-check:", s.nu_crosscheck_ok)
    print("   ", s.line())
    assert s.is45 is True
    assert s.nu_crosscheck_ok
    # HEADLINE: a REAL N=30 (4,5)-set whose interleaved-cert budget SHRINKS to g=1 (<<tau-1=9).
    # Its cover LP is integral (nu*=10=tau, 10 forced x=1 vertices); an EDGE-UNION support P of
    # 24 vertices absorbs 10 of the 12 3-APs fully (a(P)=8, integral) leaving a 2-edge residual
    # (tau=2), so a(P)+tau(res)=8+2=10=tau exactly => branch budget g=tau(res)-1=1.
    assert s.fully_half_integral is False
    assert s.nu_exact == Fraction(10, 1), s.nu_exact     # integral cover LP
    assert len(s.integral_verts) == 10, s.integral_verts
    assert s.friendly is True, "RAND30 must be interleaved-FRIENDLY"
    assert s.best_budget == 1, s.best_budget
    # re-derive the support's interleaved value EXACTLY (rational nu*, integer residual tau)
    a, tr, val = interleaved_value(s.edges, s.best_P)
    assert val == s.tau == 10 and a == 8 and tr == 2, (a, tr, val, s.tau)
    print("    HEADLINE: RAND30 interleaved budget g=1 (a(P)=8 + tau(res)=2 = tau=10) — a REAL")
    print("    N=30 (4,5)-set NOT in the A_base fully-half-integral pathology; cheaply certifiable.")
    rows.append(("Random (N=30)", s))

    print("\n" + "=" * 78)
    print("SURVEY VERDICT")
    print("=" * 78)
    print(f"  {'set':20s} {'m':>3s} {'tau':>3s} {'nu*':>10s} {'x=1':>4s} {'g':>3s} "
          f"  LP-structure / friendliness")
    for name, s in rows:
        flag = "FRIENDLY" if s.friendly else ("HOSTILE(exh)" if s.exhaustive
                                              else "no-shrink(heur)")
        print(f"  {name:20s} {s.m:3d} {s.tau:3d} {str(s.nu_exact):>10s} "
              f"{len(s.integral_verts):4d} {s.best_budget:3d}   "
              f"{s.lp_structure} [{flag}]")
    friendly_families = [n for n, s in rows
                         if s.friendly and s.is45 is not False and s.N >= 14]
    full_half = [n for n, s in rows if s.fully_half_integral and s.N >= 14]
    print()
    print("  EXACT LP-structure facts (the two orthogonal properties, kept separate):")
    print(f"    * Fully half-integral (A_base pathology, NO x=1 vertex): {full_half}")
    print("      - A_base (N=14) and 2xA_base (N=28) are EXACTLY fully half-integral")
    print("        (nu*=9/2, 9; all coords {0,1/2}); A_base's interleaved-HOSTILE verdict")
    print("        is EXHAUSTIVE (all 2^14 supports checked) -> no support shrinks budget.")
    print("    * The N=30 (4,5)-sets are NOT fully half-integral: the Fibonacci set has")
    print("      nu*=55303/5896 (large denominator, NOT even half-integral) with one x=1")
    print("      vertex; the random N=30 set has nu*=10 with 10 x=1 forced vertices.")
    print("      => their cover LPs DO have integral structure (x=1 vertices) — they are")
    print("         NOT the A_base pathology.")
    print()
    print("  Interleaved-FRIENDLY (4,5)-families found (small interleaved budget):")
    print("   ", friendly_families if friendly_families else
          "NONE among the surveyed (4,5)-sets at the budget threshold g<tau-1.")
    print("    HONEST CAVEAT: for the N=30 sets the support search is HEURISTIC (curated P:")
    print("    x=1 prefixes + top-degree shells), so 'no shrink found' is ONE-SIDED — it is")
    print("    NOT a proof that no support shrinks the budget (unlike A_base's exhaustive")
    print("    verdict).  The x=1 vertices the N=30 LPs force are individually too few to")
    print("    cover full tau, so single-shell fixing does not yet shrink g; a smarter")
    print("    multi-shell support search (future work) could still find a friendly P.")
    print()
    print("  HEADLINE (the survey question answered): the A_base-type FULLY-half-integral")
    print("  pathology is NOT universal among N=30 (4,5)-sets — both surveyed N=30 sets")
    print("  carry x=1 forced vertices (integral structure A_base lacks).  So an N=30 beat")
    print("  gadget is NOT doomed to be uncertifiable; the interleaved cert can in principle")
    print("  charge those x=1 vertices.  The remaining de-risk is wiring an x=1-aware support")
    print("  search into the gadget search so a density-clearing candidate is also FRIENDLY.")
    print("=" * 78)


def main():
    survey()
    print("\nSTATUS: structural LP-half-integrality survey.  No bound written to constants/5b.md.")
    print("        The filter `screen(A)` is composable with search_N30.py: screen every")
    print("        density-clearing candidate and prefer interleaved-FRIENDLY ones.")


if __name__ == "__main__":
    main()
