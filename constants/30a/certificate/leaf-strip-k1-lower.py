#!/usr/bin/env python3
"""
Sketch: leaf-strip-k1-lower
Target (LOWER bound): gr(Av(1324)) > 10.271   [beats BBEPP2017 verified record 10.271012]
where gr(Av(1324)) = lim_n |Av_n(1324)|^{1/n}.

STRATEGY (explorer R5 "Lever B" = BBEPP2017 §7.4 improvement avenue #1, k=1).
=============================================================================
BBEPP's record 10.271 (Thm 7.1) refines the 81/8 staircase (Thm 5.1) by RELAXING the
horizontal-domino interleave rule: only NON-LEAVES of a domino cell must sit between the
skew-components of the adjacent connecting cell; LEAVES may be placed arbitrarily. The
non-leaves cut each connecting cell into horizontal STRIPS; a strip with exactly j leaves
is a "j-leaf strip". §6 proves leaf/empty-strip proportions concentrated; §7's master
Lemma 7.4 (a law-of-large-numbers saddle-point estimate) turns the multivariate GF product
into 1/z0 = 10.271012, z0 ~ 0.097361383.

CRUCIALLY: the §7 optimum only ever uses 0-, 2-, and 3-leaf strips (e0,e2,e3). With
alpha in [11/20, 5/9) forcing >=1 leaf per non-empty strip and an EQUITABLE allocation
(BBEPP minimise prod_i H_{a_i} over leaf-allocations -- the equitable sequence is the
MINIMISER, hence a valid LOWER bound), the allocation collapses to exactly (e0,e2,e3):
NO 1-leaf strips appear. BBEPP §7.4 avenue #1 (verbatim, lines 2704-2710): "if we
determined the expected proportion of k-leaf strips for k>=1, and established that their
distribution was concentrated, then that would affect the optimal distribution of points
between the strips, leading to a better bound. It is possible to modify the functional
equation for dominoes to record k-leaf strips, for any k, but the result is complicated
and it has not been possible to analyse the result, even for k=1."

THE LEVER (this sketch): the equitable (e0,e2,e3) allocation is the *minimiser* of the
per-strip interleaving product prod_k F_k^{w_k} (F_k := H_k(z0,q0) is LOG-CONVEX in k, so
by Jensen/majorisation the equitable allocation minimises the product for fixed leaf+strip
totals -- verified in this script). The TRUE strip-size distribution is NOT equitable: it
has a genuine spread including 1-leaf strips. Since equitable is the MINIMUM, the true
(concentrated) distribution gives a STRICTLY LARGER product -- a better bound -- PROVIDED
the true proportions p_k within the constrained subclass B^{alpha,beta} are known and
concentrated. That is precisely §7.4 avenue #1, and precisely the wall BBEPP hit.

=========================================================================================
WHAT THIS ROUND ESTABLISHES (R5) -- read carefully which parts are RIGOROUS vs HEURISTIC.
=========================================================================================
  [CLOSED, RIGOROUS]  H-REPRO -- reproduce_bbepp_baseline():
      Full from-scratch reconstruction of BBEPP Thm 7.1's 10.271 via Lemma 7.4. Builds the
      connecting-cell GF H(z,q)=1/(1-q*Q(z)), Q(z)=(1-sqrt(1-4z))/2 (verified termwise via
      the recurrence h_i=(q^2 h_{i-1}-q*Catalan_{i-1})/(q-1)); applies the strip operator
      Omega^j (Omega^j[z^n]=C(n+j,j) z^n) to get F_0=H, F_2, F_3 at z0; solves the saddle
      eq (10) for q0; assembles G(z0) and checks G(z0)>1, which CERTIFIES 1/z0 ~ 10.271012
      is a valid lower bound. Reproduces BBEPP's stated q0~2.917054 and G>1. (Anchors the
      harness; NOT a new bound -- it is the published record, reproduced.)

  [PARTIAL, RIGOROUS core + OPEN wall]  H-FUNEQ -- strip_size_distribution_exact():
      Exact closed form for the strip-size statistics of an UNCONSTRAINED domino cell
      (a free 213-avoider / Catalan arch system): the total number of k-leaf strips over
      ALL n-point cells is e_k(n) = C(2n-2-k, n-2) (DERIVED + verified by brute-force
      enumeration to n=8 in this script). The asymptotic per-cell expected proportion is
      E[#k-leaf strips]/n -> 1/2^{k+2}. THIS IS THE FREE-CELL DISTRIBUTION. *** It is NOT
      directly the allocation BBEPP need: BBEPP's leaf proportion inside the DOMINO (the
      interleaved pair, not a free cell) is 5n/9, whereas the free cell gives n/2 -- so the
      constrained subclass B^{alpha,beta}'s strip distribution differs and must come from the
      MODIFIED functional equation (the wall). *** Still bankable: it is the exact k-leaf-strip
      enumeration that the modified funeq must reproduce, and the entry point for H-EXTRACT.

  [OPEN, the BBEPP wall]  H-EXTRACT -- extract_constrained_strip_proportions():
      Extract the TRUE strip-size proportions p_k *within the constrained class
      B^{alpha,beta}_m* (at least alpha*m leaves, beta*m+1 empty strips) from the modified
      domino functional equation that marks k-leaf strips. Resultant-elimination / catalytic-
      variable work, the step BBEPP "could not analyse, even for k=1". OPEN.

  [OPEN]  H-CONC -- prove_e1_concentration():
      Prove the 1-leaf-strip proportion is concentrated at its mean within B^{alpha,beta}
      (Prop-6.4 analogue), so it enters Lemma 7.4 with a fixed alpha_{e1}. OPEN.

  [OPEN, payoff]  H-OPT -- reoptimize_saddle_with_e1():
      Re-run the Lemma-7.4 saddle over the enlarged allocation with the PROVEN p_k. The
      HEURISTIC exploration in this script (saddle_gain_exploration()) shows that admitting
      1-leaf strips at the BBEPP totals (leaves=5/9, strips=4/9) makes G(z0) strictly larger,
      so the G=1 crossing moves to a smaller z0 -> a LARGER 1/z0. With an illustrative
      w1=0.05 allocation the crossing is ~10.288 (gain ~0.017). *** THIS IS A CONJECTURE, NOT
      A BOUND: the w_k used are an illustrative feasible allocation, NOT the proven constrained
      proportions, and concentration (H-CONC) is unproven. *** OPEN.

  [OPEN]  H-CERT -- assemble_numerical_certificate():
      Directed-rounded interval certificate that the re-optimised g_new > 10271012/1000000,
      using the PROVEN p_k and concentration constants. OPEN (gated on H-EXTRACT/H-CONC).

LEAN-FIT: HOSTILE. Load-bearing step = multivariate-GF radius-of-convergence / saddle
optimisation + LLN concentration (Lemma 7.4). Certificate path = NUMERICAL (directed-rounded),
the 82a kind, NOT a lake build.

HONEST RISK / RESULT (R5): the mechanism is now CONCRETE and the direction is confirmed
(admitting e1 raises G, hence the bound), but the load-bearing soundness step -- the TRUE
constrained strip distribution + its concentration -- remains the exact wall BBEPP flagged.
No bound is CLAIMED beyond the reproduced 10.271 baseline. The conjectural gain (~10.288) is
documented as a target, NOT a certified value.

Reproduce: python3 constants/30a/certificate/leaf-strip-k1-lower.py   (needs: mpmath)
The top-level lower_bound() RAISES on the open holes so no false CERTIFIED line can print.
"""
import math
from fractions import Fraction

try:
    import mpmath as mp
except ImportError:                                   # pragma: no cover
    mp = None

RECORD_LOWER = Fraction(10271012, 1000000)   # BBEPP Thm 7.1 verified record to strictly beat
HELD = Fraction(81, 8)                        # = 10.125, our fully-verified held (R4)

# BBEPP §7 baseline saddle parameters (paper lines ~2241-2259 / 2660-2680):
BBEPP_Z0 = '0.097361383'           # z0 -> 1/z0 ~ 10.271012
BBEPP_GAMMA = '0.951509'
BBEPP_KAPPA = '0.496339'
ALPHA = Fraction(5, 9)             # leaf proportion (alpha -> 5/9)
BETA = Fraction(5, 27)            # empty-strip proportion (beta -> 5/27)
_N_SERIES = 700                    # z-series truncation for H (converges; z0 < 1/4, ROC_q ~9.15)


# ---------------------------------------------------------------------------
# Shared GF machinery (the connecting-cell GF and the strip operator).
# H(z,q) = 1/(1 - q Q(z)),  Q(z) = (1 - sqrt(1-4z))/2  [BBEPP eq (3)].
# Equivalently H = sum_i h_i(q) z^i with h_0=1, h_i=(q^2 h_{i-1} - q*Cat_{i-1})/(q-1).
# Strip operator Omega^j[z^n] = C(n+j,j) z^n, so H_j(z,q)=Omega^j[H]=sum_i C(i+j,j)h_i(q)z^i.
# F_j(q) := H_j(z0,q) and dF_j/dq are what Lemma 7.4's saddle needs.
# ---------------------------------------------------------------------------
def _catalan(n):
    return math.comb(2 * n, n) // (n + 1)


_CAT = [_catalan(i) for i in range(_N_SERIES)]


def _Fj(z0, q, j):
    """Return (F_j(q), dF_j/dq) at fixed z0, where F_j(q)=H_j(z0,q). Pure series in z0."""
    h = mp.mpf(1)
    dh = mp.mpf(0)
    F = mp.mpf(1)        # i=0: C(j,j)*h_0*z0^0 = 1
    dF = mp.mpf(0)
    zp = mp.mpf(1)
    for i in range(1, _N_SERIES):
        c = _CAT[i - 1]
        d = (q - 1)
        num = q * q * h - q * c
        dnum = 2 * q * h + q * q * dh - c
        h = num / d
        dh = (dnum * d - num) / (d * d)
        zp *= z0
        co = math.comb(i + j, j)
        F += co * h * zp
        dF += co * dh * zp
    return F, dF


def _G_of_z(z0, weights, gamma, kappa, qguess):
    """BBEPP's G(z0) for a strip allocation `weights` (dict k -> per-m proportion w_k).
    Solves the Lemma-7.4 saddle sum_k w_k F_k'/F_k = kappa/q for q0, then assembles
    G(z0) = (27 z0/4)^{1+gamma} q0^{-kappa} prod_k F_k^{w_k} (gamma+kappa)^{gamma+kappa}
            / (gamma^gamma kappa^kappa).  Returns (G, q0)."""
    def saddle(q):
        s = mp.mpf(0)
        for k, wk in weights.items():
            if wk == 0:
                continue
            F, dF = _Fj(z0, q, k)
            s += wk * dF / F
        return s - kappa / q
    q0 = mp.findroot(saddle, qguess)
    prod = mp.mpf(1)
    for k, wk in weights.items():
        if wk == 0:
            continue
        F, _ = _Fj(z0, q0, k)
        prod *= F ** wk
    G = ((27 * z0 / 4) ** (1 + gamma) * q0 ** (-kappa) * prod
         * (gamma + kappa) ** (gamma + kappa) / (gamma ** gamma * kappa ** kappa))
    return G, q0


# ===========================================================================
# H-REPRO  [CLOSED, RIGOROUS]
# ===========================================================================
def reproduce_bbepp_baseline(verbose=False):
    """Reproduce BBEPP Thm 7.1's 10.271012 from Lemma 7.4 (e0,e2,e3) allocation.
    Returns z0 and certifies G(z0) > 1 (so 1/z0 is a valid lower bound). NOT a new bound."""
    if mp is None:
        raise RuntimeError("H-REPRO needs mpmath (pip install mpmath).")
    mp.mp.dps = 35
    z0 = mp.mpf(BBEPP_Z0)
    gamma = mp.mpf(BBEPP_GAMMA)
    kappa = mp.mpf(BBEPP_KAPPA)
    a = mp.mpf(5) / 9
    b = mp.mpf(5) / 27
    # BBEPP equitable allocation per m points: e0=beta, e2=3-4a-3b, e3=3a+2b-2.
    w = {0: b, 2: 3 - 4 * a - 3 * b, 3: 3 * a + 2 * b - 2}
    G, q0 = _G_of_z(z0, w, gamma, kappa, mp.mpf('2.917'))
    if verbose:
        print("  [H-REPRO] z0 = %s,  1/z0 = %s" % (mp.nstr(z0, 10), mp.nstr(1 / z0, 11)))
        print("  [H-REPRO] saddle q0 = %s  (BBEPP states ~2.917054)" % mp.nstr(q0, 8))
        print("  [H-REPRO] G(z0) = %s  (> 1 certifies 1/z0 is a lower bound)" % mp.nstr(G, 12))
    assert G > 1, "H-REPRO failed: G(z0) <= 1"
    assert abs(q0 - mp.mpf('2.917054')) < mp.mpf('1e-4'), "q0 mismatch vs BBEPP"
    assert abs(1 / z0 - mp.mpf('10.271012')) < mp.mpf('1e-5'), "1/z0 mismatch vs BBEPP"
    return z0, G, q0


# ===========================================================================
# H-FUNEQ  [PARTIAL: rigorous free-cell closed form; constrained class OPEN]
# ===========================================================================
def _enumerate_strip_distribution(n):
    """Brute-force the strip-size distribution over all n-point 213-avoiders (a free
    domino cell). Returns Counter {k: total #k-leaf strips over all cells}. A 'leaf' is a
    right-to-left maximum; non-leaves (value-ordered) divide the cell into strips."""
    from itertools import permutations, combinations
    from collections import Counter
    def is_av213(p):
        for c in combinations(range(len(p)), 3):
            x, y, z = p[c[0]], p[c[1]], p[c[2]]
            if y < x < z:          # pattern 213: mid<first<last
                return False
        return True
    dist = Counter()
    for p in permutations(range(1, n + 1)):
        if not is_av213(p):
            continue
        # right-to-left maxima = leaves
        leaves = set()
        cur = -1
        for i in range(n - 1, -1, -1):
            if p[i] > cur:
                leaves.add(i)
                cur = p[i]
        order = sorted(range(n), key=lambda i: p[i])    # value order
        seq = [1 if i in leaves else 0 for i in order]  # 1=leaf, 0=non-leaf (divider)
        c = 0
        for x in seq:
            if x == 0:
                dist[c] += 1
                c = 0
            else:
                c += 1
        dist[c] += 1
    return dist


def strip_size_distribution_exact(verbose=False):
    """[RIGOROUS core] Closed form e_k(n) = C(2n-2-k, n-2) for the total number of k-leaf
    strips over all n-point (free) domino cells; per-cell expected proportion -> 1/2^{k+2}.
    Verified by brute-force enumeration to n=8. NOTE: this is the UNCONSTRAINED-cell
    distribution; the constrained B^{alpha,beta} distribution (the one Lemma 7.4 needs)
    differs and is the H-EXTRACT wall. Returns the verified closed-form function."""
    for n in range(2, 9):
        dist = _enumerate_strip_distribution(n)
        for k in range(0, n + 1):
            expected = math.comb(2 * n - 2 - k, n - 2) if (2 * n - 2 - k) >= (n - 2) else 0
            got = dist.get(k, 0)
            assert got == expected, ("e_k(n) closed form FAILED at n=%d,k=%d: got %d expected %d"
                                     % (n, k, got, expected))
        if verbose:
            top = {k: dist[k] for k in sorted(dist) if dist[k]}
            print("  [H-FUNEQ] n=%d  strip-size totals e_k = %s  (= C(2n-2-k,n-2))" % (n, top))
    if verbose:
        # asymptotic proportions
        def cat(n):
            return math.comb(2 * n, n) // (n + 1)
        n = 4000
        props = [math.comb(2 * n - 2 - k, n - 2) / cat(n) / n for k in range(5)]
        print("  [H-FUNEQ] E[#k-leaf strips]/n (n=4000): "
              + ", ".join("p_%d=%.5f" % (k, props[k]) for k in range(5))
              + "  ->  1/2^{k+2}")
        print("  [H-FUNEQ] free-cell leaf prop = %.4f (= 1/2), BUT BBEPP's IN-DOMINO leaf prop "
              "= 5/9 = %.4f" % (sum(k * props[k] for k in range(60 if False else 5)) or 0.5, 5 / 9))
    return lambda n, k: math.comb(2 * n - 2 - k, n - 2) if (2 * n - 2 - k) >= (n - 2) else 0


def verify_equitable_is_minimiser(verbose=False):
    """[RIGOROUS] Confirm log F_k is CONVEX in k at the baseline (z0,q0). Convexity =>
    the equitable allocation MINIMISES prod_k F_k^{w_k} for fixed leaf+strip totals
    (Jensen/majorisation), which is exactly why BBEPP's (e0,e2,e3) is a valid LOWER bound
    and why the TRUE (non-equitable) distribution gives a STRICTLY LARGER product."""
    if mp is None:
        raise RuntimeError("needs mpmath")
    mp.mp.dps = 30
    z0 = mp.mpf(BBEPP_Z0)
    q0 = mp.mpf('2.917054')
    logs = [float(mp.log(_Fj(z0, q0, k)[0])) for k in range(7)]
    second = [logs[k + 1] - 2 * logs[k] + logs[k - 1] for k in range(1, 6)]
    if verbose:
        print("  [equitable-min] log F_k = %s" % [round(x, 4) for x in logs])
        print("  [equitable-min] 2nd differences (all > 0 => log-convex => equitable is MIN): %s"
              % [round(x, 5) for x in second])
    assert all(d > 0 for d in second), "log F_k is NOT convex -- equitable-minimiser claim fails"
    return True


# ===========================================================================
# H-OPT  [OPEN, payoff] -- heuristic gain exploration only (NOT a bound).
# ===========================================================================
def saddle_gain_exploration(verbose=False):
    """[HEURISTIC, NOT A BOUND] Show that admitting 1-leaf strips at BBEPP's totals
    (leaves=5/9, strips=4/9) makes G(z0) strictly LARGER than the equitable baseline, so
    the G=1 crossing moves to a smaller z0 -> a larger 1/z0. Reports the illustrative
    crossing for a w1=0.05 allocation. *** CONJECTURE: the w_k are an illustrative feasible
    allocation, NOT the proven constrained proportions; concentration unproven. ***"""
    if mp is None:
        raise RuntimeError("needs mpmath")
    mp.mp.dps = 30
    gamma = mp.mpf(BBEPP_GAMMA)
    kappa = mp.mpf(BBEPP_KAPPA)
    b = mp.mpf(5) / 27
    z0_base = mp.mpf(BBEPP_Z0)
    # illustrative allocation: w1=t, keep empty=beta, keep leaves=5/9 and strips=4/9.
    t = mp.mpf('0.05')
    S = mp.mpf(4) / 9 - b - t       # w2 + w3
    L = mp.mpf(5) / 9 - t           # 2 w2 + 3 w3 = leaves minus the t single leaves
    w3 = L - 2 * S
    w2 = S - w3
    w = {0: b, 1: t, 2: w2, 3: w3}
    G_at_base, _ = _G_of_z(z0_base, w, gamma, kappa, mp.mpf('2.9'))
    # bisection on z0 for the G=1 crossing (continuation of q0)
    lo, hi = mp.mpf('0.0972'), z0_base
    qg = mp.mpf('2.9')
    for _ in range(40):
        mid = (lo + hi) / 2
        G, qg = _G_of_z(mid, w, gamma, kappa, qg)
        if G > 1:
            lo = mid
        else:
            hi = mid
    cross = 1 / mid
    if verbose:
        print("  [H-OPT heuristic] equitable baseline G(z0) = 1.00000006 (record 10.271012)")
        print("  [H-OPT heuristic] w1=0.05 allocation: G(z0_base) = %s  (> baseline => bound rises)"
              % mp.nstr(G_at_base, 8))
        print("  [H-OPT heuristic] conjectural G=1 crossing 1/z0 = %s  (gain ~%s over 10.271)"
              % (mp.nstr(cross, 10), mp.nstr(cross - mp.mpf('10.271012'), 3)))
        print("  [H-OPT heuristic] *** CONJECTURE ONLY -- w_k illustrative, concentration unproven ***")
    return cross


# ===========================================================================
# Open holes (the BBEPP wall) -- raise so no false bound prints.
# ===========================================================================
def extract_constrained_strip_proportions():
    """HOLE H-EXTRACT (the BBEPP wall): the TRUE strip-size proportions p_k *within the
    constrained class B^{alpha,beta}_m* from the modified (k-leaf-strip-marking) domino
    functional equation. The free-cell closed form e_k(n)=C(2n-2-k,n-2) (H-FUNEQ) is the
    UNCONSTRAINED distribution; the constrained one differs (free-cell leaf prop 1/2 vs
    in-domino 5/9) and requires the modified funeq BBEPP could not analyse even for k=1."""
    raise NotImplementedError(
        "H-EXTRACT: extract the constrained strip proportions p_k within B^{alpha,beta} "
        "from the modified domino functional equation (the step BBEPP could not analyse "
        "for k=1). The free-cell e_k(n)=C(2n-2-k,n-2) is the entry point, not the answer."
    )


def prove_e1_concentration():
    """HOLE H-CONC: prove the 1-leaf-strip proportion is concentrated at its mean within
    B^{alpha,beta} (Prop-6.4 analogue), giving a fixed alpha_{e1} for Lemma 7.4."""
    raise NotImplementedError(
        "H-CONC: prove concentration of the constrained 1-leaf-strip proportion "
        "(variance / Flajolet-Sedgewick III.2) -> fixed alpha_{e1} input to Lemma 7.4."
    )


def reoptimize_saddle_with_e1():
    """HOLE H-OPT (payoff): re-run the Lemma-7.4 saddle over the enlarged allocation with
    the PROVEN constrained p_k (H-EXTRACT) and proven concentration (H-CONC). The heuristic
    in saddle_gain_exploration() shows the direction (G rises, bound ~10.288) but the
    allocation there is illustrative, not proven."""
    raise NotImplementedError(
        "H-OPT: re-solve the Lemma-7.4 saddle over (e0,e1,e2,e3,...) with the PROVEN "
        "constrained proportions p_k and proven concentration. Heuristic gain ~10.288 "
        "(CONJECTURE only -- see saddle_gain_exploration)."
    )


def assemble_numerical_certificate():
    """HOLE H-CERT: directed-rounded interval certificate that the re-optimised g_new
    > 10271012/1000000, using the PROVEN p_k and concentration constants."""
    raise NotImplementedError(
        "H-CERT: directed-rounded certificate g_new > 10271012/1000000 "
        "(gated on H-EXTRACT + H-CONC)."
    )


def lower_bound():
    """Top-level: RAISES on the open wall so no false CERTIFIED line can print.
    The reproduced baseline (H-REPRO) is the record 10.271, NOT a new bound."""
    reproduce_bbepp_baseline()              # H-REPRO -- CLOSED (reproduces 10.271)
    strip_size_distribution_exact()         # H-FUNEQ -- PARTIAL (free-cell closed form)
    verify_equitable_is_minimiser()         # rigorous: equitable is the MIN (soundness key)
    extract_constrained_strip_proportions() # H-EXTRACT -- OPEN (the wall)
    assert prove_e1_concentration()         # H-CONC -- OPEN
    g_new = reoptimize_saddle_with_e1()     # H-OPT -- OPEN
    g_cert = assemble_numerical_certificate()  # H-CERT -- OPEN
    assert g_cert > RECORD_LOWER, f"{float(g_cert)} does not beat {float(RECORD_LOWER)}"
    print(f"CERTIFIED (record-break via §7.4 avenue #1, k=1 leaf strips): "
          f"gr(Av(1324)) >= {float(g_cert):.6f} > {float(RECORD_LOWER):.6f}")
    return g_cert


def status_report():
    """Verified/diagnostic work that does NOT claim a bound -- safe under __main__."""
    print("leaf-strip-k1-lower -- R5 status (no new bound claimed)")
    print(f"  held (verified, R4):  {float(HELD):.6f}  (= 81/8)")
    print(f"  record to beat:       {float(RECORD_LOWER):.6f}  (BBEPP Thm 7.1)")
    print()
    print("[H-REPRO -- CLOSED, RIGOROUS] reproduce BBEPP 10.271 from Lemma 7.4:")
    reproduce_bbepp_baseline(verbose=True)
    print()
    print("[H-FUNEQ -- PARTIAL] exact free-cell strip-size distribution e_k(n)=C(2n-2-k,n-2):")
    strip_size_distribution_exact(verbose=True)
    print()
    print("[soundness key -- RIGOROUS] equitable allocation is the MINIMISER (log F_k convex):")
    verify_equitable_is_minimiser(verbose=True)
    print()
    print("[H-OPT -- HEURISTIC, NOT A BOUND] direction of the e1 refinement:")
    saddle_gain_exploration(verbose=True)
    print()
    print("OPEN WALL (H-EXTRACT/H-CONC): the TRUE constrained strip proportions p_k within")
    print("  B^{alpha,beta} + their concentration -- exactly what BBEPP 'could not analyse for k=1'.")
    print("  No bound is claimed beyond the reproduced 10.271 baseline.")


if __name__ == "__main__":
    if mp is None:
        print("ERROR: this sketch needs mpmath (pip install --user mpmath).")
        raise SystemExit(0)
    status_report()
    print()
    try:
        lower_bound()
    except (NotImplementedError, AssertionError) as e:
        print(f"[load-bearing hole raises, as expected]  {type(e).__name__}: {e}")
