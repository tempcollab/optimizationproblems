"""
R9 -- UNIFIED first-variation marginal: three-regime TOY verification.

This script isolates and exercises the load-bearing NEW pieces of the unified
first-variation theorem (T) in `approaches/R9-unified-firstvar.md`:

    log h(q) = Phi(q) / D(q),    Phi(q) = Phi0 + r*q,    D(q) = max(a0_A + sA*q, a0_B + sB*q)
    d+ log h /dq |_0 = (1/D)[ Phi+'(0) - log h * (dD/dq)+ ],   Phi+'(0)=r,  log h = Phi0/D,
    (dD/dq)+|_0 = max{ slope_i : arg_i attains D(0) }     (one-sided Danskin).

We do NOT need a live Doche family for this: Phi+'(0)=r is the inner-max derivative
(regime-INDEPENDENT, R8 DCT lemma -- depends only on the inner max, not the outer D),
and the only regime-dependent factor is (dD/dq)+, which is a 2-term affine-max
one-sided derivative. The toy stresses precisely that composition.

`r` plays the role of int_{ACT(X)} log|Q.chi| ds; `Phi0/D` plays the role of log h;
`sX = deg(Q)` for the side Q joins, the other slope 0; `a0_A, a0_B` the base D-args.

Three regimes, each row: closed-form (T) marginal vs a RIGHT finite difference of
Phi(q)/D(q). The TIE row additionally checks the LEFT FD differs (genuine one-sided kink).

Runtime: ~1 s (pure scalar arithmetic, no integrals, no certify).

Reproduce:  python3 verify_unified_firstvar.py
"""
import sys


def D_of(q, a0A, sA, a0B, sB):
    return max(a0A + sA * q, a0B + sB * q)


def logh_of(q, Phi0, r, a0A, sA, a0B, sB):
    return (Phi0 + r * q) / D_of(q, a0A, sA, a0B, sB)


def right_fd(Phi0, r, a0A, sA, a0B, sB, eps):
    """one-sided RIGHT finite difference (forward), the admissible q>=0 direction."""
    f0 = logh_of(0.0, Phi0, r, a0A, sA, a0B, sB)
    fp = logh_of(eps, Phi0, r, a0A, sA, a0B, sB)
    return (fp - f0) / eps


def left_fd(Phi0, r, a0A, sA, a0B, sB, eps):
    f0 = logh_of(0.0, Phi0, r, a0A, sA, a0B, sB)
    fm = logh_of(-eps, Phi0, r, a0A, sA, a0B, sB)
    return (f0 - fm) / eps


def dD_right(a0A, sA, a0B, sB):
    """one-sided Danskin: max of slopes over the ACTIVE index set at q=0."""
    D0 = max(a0A, a0B)
    active_slopes = []
    if abs(a0A - D0) < 1e-12:
        active_slopes.append(sA)
    if abs(a0B - D0) < 1e-12:
        active_slopes.append(sB)
    return max(active_slopes)


def dD_left(a0A, sA, a0B, sB):
    """left derivative of the max: min of active slopes (the other arg wins for q<0)."""
    D0 = max(a0A, a0B)
    active_slopes = []
    if abs(a0A - D0) < 1e-12:
        active_slopes.append(sA)
    if abs(a0B - D0) < 1e-12:
        active_slopes.append(sB)
    return min(active_slopes)


def closed_form(Phi0, r, a0A, sA, a0B, sB):
    """(T): (1/D)[ r - logh * (dD/dq)+ ]."""
    D0 = max(a0A, a0B)
    logh = Phi0 / D0
    return (r - logh * dD_right(a0A, sA, a0B, sB)) / D0


def closed_form_left(Phi0, r, a0A, sA, a0B, sB):
    D0 = max(a0A, a0B)
    logh = Phi0 / D0
    return (r - logh * dD_left(a0A, sA, a0B, sB)) / D0


def run(eps=1e-7):
    print("=" * 96)
    print(f"R9 UNIFIED first-variation marginal -- three-regime TOY   eps={eps}")
    print("  log h = Phi/D, Phi=Phi0+r q, D=max(a0A+sA q, a0B+sB q); r ~ int_ACT log|Q|,")
    print("  sX=deg(Q) on the side Q joins; closed form (T) vs RIGHT finite difference.")
    print("=" * 96)

    # toy scalars chosen in the live regime: D ~ 60-72, Phi0 ~ 18, deg ~ 4-8 (cf. j9 deg 8).
    Phi0 = 18.28
    r = -0.41         # a FIRING value (int_ACT log|Q| < 0): tests sign too
    deg = 8.0         # block degree (slope of the joined arg)

    rows = []
    TOL = 1e-7

    # ---- Regime I: a > b  (A attains D). a0A=72, a0B=62. ----
    # I-A: block on A-side (the D-ATTAINING arg) -> A-attaining cross-term (NEW).
    rows.append(("I  a>b  A-side (A-attaining XTERM)", Phi0, r, 72.0, deg, 62.0, 0.0, "xterm"))
    # I-B: block on B-side (the LOSING arg) -> no cross-term.
    rows.append(("I  a>b  B-side (losing arg, no XT)", Phi0, r, 72.0, 0.0, 62.0, deg, "noxt"))

    # ---- Regime II: a < b (B attains D) -- the HELD family. a0A=61.66, a0B=72.00. ----
    # II-A: A-base block on the LOSING arg -> r~_Q, no cross-term (R6/R8).
    rows.append(("II a<b  A-side (losing arg = r~_Q)", Phi0, r, 61.66, deg, 72.00, 0.0, "noxt"))
    # II-B: B-perturber on the D-attaining arg -> m_B cross-term (R8).
    rows.append(("II a<b  B-side (D-attaining = m_B)", Phi0, r, 61.66, 0.0, 72.00, deg, "xterm"))

    # ---- Regime III: a = b (TIE). a0A=a0B=66. ----
    rows.append(("III a=b A-side (TIE, one-sided)", Phi0, r, 66.0, deg, 66.0, 0.0, "tie"))
    rows.append(("III a=b B-side (TIE, one-sided)", Phi0, r, 66.0, 0.0, 66.0, deg, "tie"))

    hdr = f"{'regime / side':<36}{'closed (T)':>14}{'rightFD':>14}{'|resid|':>12}  {'kind':<6} fires PASS"
    print(hdr)
    print("-" * len(hdr))
    all_ok = True
    for name, Phi0_, r_, a0A, sA, a0B, sB, kind in rows:
        cf = closed_form(Phi0_, r_, a0A, sA, a0B, sB)
        rfd = right_fd(Phi0_, r_, a0A, sA, a0B, sB, eps)
        resid = abs(cf - rfd)
        ok = resid < TOL
        fires = cf < 0
        all_ok = all_ok and ok
        print(f"{name:<36}{cf:>14.8f}{rfd:>14.8f}{resid:>12.2e}  {kind:<6} "
              f"{'YES' if fires else 'no':<5} {'PASS' if ok else 'FAIL'}")
    print("-" * len(hdr))

    # ---- explicit kink check at the tie: LEFT FD differs from RIGHT FD ----
    print()
    print("TIE one-sided kink (regime III): LEFT derivative differs from RIGHT derivative")
    print("-" * 96)
    a0A = a0B = 66.0
    kink_ok = True
    for side, sA, sB in (("A-side", deg, 0.0), ("B-side", 0.0, deg)):
        rfd = right_fd(Phi0, r, a0A, sA, a0B, sB, eps)
        lfd = left_fd(Phi0, r, a0A, sA, a0B, sB, eps)
        cf_r = closed_form(Phi0, r, a0A, sA, a0B, sB)        # right: cross-term present
        cf_l = closed_form_left(Phi0, r, a0A, sA, a0B, sB)   # left: no cross-term
        gap = abs(lfd - rfd)
        right_match = abs(cf_r - rfd) < TOL
        left_match = abs(cf_l - lfd) < TOL
        present = gap > 1e-3
        ok = right_match and left_match and present
        kink_ok = kink_ok and ok
        print(f"  TIE {side}: rightFD={rfd:.8f} (cf_right={cf_r:.8f}, match={right_match})")
        print(f"           leftFD ={lfd:.8f} (cf_left ={cf_l:.8f}, match={left_match})")
        print(f"           |leftFD-rightFD|={gap:.6f}  kink present(>1e-3)={present}  "
              f"{'PASS' if ok else 'FAIL'}")
    print("-" * 96)

    # ---- sanity: regime-II closed forms equal the live-engine formulas symbolically ----
    print()
    print("Sanity: regime-II rows reproduce the two reviewer-verified live marginals.")
    D0 = max(61.66, 72.00); logh = Phi0 / D0
    rA = r / D0                                  # r~_Q  = (1/D) int_{A>B} log|Q|
    mB = (r - logh * deg) / D0                   # m_B   = (1/D)[ int_{B>A} log|Q| - logh*deg ]
    cfA = closed_form(Phi0, r, 61.66, deg, 72.00, 0.0)
    cfB = closed_form(Phi0, r, 61.66, 0.0, 72.00, deg)
    okA = abs(cfA - rA) < 1e-12
    okB = abs(cfB - mB) < 1e-12
    print(f"  II A-side closed (T)={cfA:.10f}  vs  r~_Q=(1/D)r={rA:.10f}   match={okA}")
    print(f"  II B-side closed (T)={cfB:.10f}  vs  m_B=(1/D)[r-logh*deg]={mB:.10f}  match={okB}")
    sane_ok = okA and okB
    print("-" * 96)

    overall = all_ok and kink_ok and sane_ok
    print()
    print(f"RESULT: three-regime FD match = {'PASS' if all_ok else 'FAIL'}; "
          f"tie kink = {'PASS' if kink_ok else 'FAIL'}; "
          f"regime-II = live-marginal sanity = {'PASS' if sane_ok else 'FAIL'}")
    print(f"OVERALL: {'PASS' if overall else 'FAIL'}")
    return overall


if __name__ == "__main__":
    eps = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-7
    ok = run(eps)
    sys.exit(0 if ok else 1)
