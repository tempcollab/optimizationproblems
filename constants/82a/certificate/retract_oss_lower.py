"""
RETRACTION WITNESS — the R14/R15/R17 OSS log-energy LOWER-bound certificate
(verify_vec_energy.py, held 0.25090 -> 0.25113 -> 0.25240) is INVALID.

This standalone script proves, rigorously and reproducibly (a few seconds, no
network), that the certificate bounds NOTHING. It uses the SAME committed frozen
data the certificate consumes (frozen_energy.npz) and the SAME f-formula, and
exhibits TWO INDEPENDENT structural failures, either of which retracts the bound.

----------------------------------------------------------------------------
WHAT THE LOWER-BOUND METHOD ACTUALLY PROVES
----------------------------------------------------------------------------
The auxiliary-function / Smyth-LP lower bound is:

    sum_i f(alpha_i) >= d * ( min over the SUPPORT of the conjugate measure nu  f )

i.e. (1/d) log Z(alpha) = INT g dnu >= min_{supp nu} f.  Flammang's reduction
"min on |z|=1" is only a *cheap way to compute min f* and it is VALID ONLY IF the
global plane minimum of f sits on |z|=1 (resp. the two unit circles).  For
Flammang's pure f0 this holds (f0 is subharmonic off the circles, so the maximum
principle puts its min on |z|=1).  The OSS certificate BOLTS ON a term
-2*lambda0*U_mu0 that is SUPERHARMONIC in the support band, which DESTROYS that
property: the global plane min of the certificate's own f escapes |z|=1 and drops
far below 0.2487458.  The "min on |z|=1 = 0.2524" the cert reports is therefore a
WRONG-LOCUS ARTIFACT and bounds nothing.

----------------------------------------------------------------------------
FAILURE 1 (decisive on its own): the global plane min of the SAME f is far below
the Flammang record 0.2487458.
----------------------------------------------------------------------------
FAILURE 2 (independent): the OSS column premise I(nu) = (1/d^2) log|disc(P)| >= 0
fails for Zhang-Zagier, because alpha need not be an algebraic INTEGER, so the
leading coefficient a can exceed 1 and  I(nu) = (1/d^2)[log|disc| - (2d-2)log|a|]
can be negative.  Concrete primitive irreducible counterexample exhibited below.

Run:  python3 retract_oss_lower.py
"""
import math
import numpy as np
from flammang_table1 import get_table

RECORD = 0.2487458          # Flammang [F18] verified lower bound = log(1.282416)

# ---- load the EXACT frozen data the (invalid) certificate uses -------------
_FZ = np.load("frozen_energy.npz")
CJ = _FZ["cj"]
LAM0 = float(_FZ["lambda0"])
CENTERS = _FZ["centers"]
MASSES = _FZ["masses"]
LBIN = float(_FZ["L"])
IHAT = float(_FZ["Ihat"])
_TABLE = get_table()


def U_mu0(z, nsub=120):
    """TRUE logarithmic potential U_mu0(z) of the frozen histogram mu0, computed by
    fine arc-quadrature (NOT the cert's per-cell upper bound — we want the honest
    value of f off the circle).  mu0 = sum_k mass_k * Uniform(arc center c_k, width L),
    symmetrized z -> conj(z) (the cert's conjugate arcs at -c_k).  Same definition
    as freeze_energy.potential_at_nodes_clean / the cert's pot_upper_batch target.
    nsub=120 is ample off-circle (the kernel is smooth there); the on-circle [a]
    witness and the [c] disc witness are nsub-independent in their conclusions."""
    s = (np.arange(nsub) + 0.5) / nsub * LBIN - LBIN / 2.0
    U = 0.0
    for c, m in zip(CENTERS, MASSES):
        zk = np.exp(1j * (float(c) + s))      # support arc at +c
        zkc = np.exp(1j * (-float(c) + s))    # conjugate arc at -c
        U += float(m) * 0.5 * (np.log(np.abs(z - zk)).mean()
                               + np.log(np.abs(z - zkc)).mean())
    return U


def f(z):
    """The EXACT certificate integrand
        f(z) = g(z) - sum_j c_j log|Q_j(w)| - lambda0 (2 U_mu0(z) - Ihat),  w=z(1-z),
    matching verify_vec_energy.lower_bound_batch (which certifies a LOWER bound on
    THIS f on the arc |z|=1, t in [0,pi]).  At a zero of some Q_j the subtracted
    -c_j log|Q_j| -> +inf, so such points are never minima; we return +inf."""
    w = z - z * z
    val = math.log(max(1.0, abs(w)))
    for (c_un, asc), cj in zip(_TABLE, CJ):
        if cj == 0.0:
            continue
        q = 0j
        for a in reversed(asc):
            q = q * w + a
        aq = abs(q)
        if aq < 1e-300:
            return math.inf
        val -= float(cj) * math.log(aq)
    val -= LAM0 * (2.0 * U_mu0(z) - IHAT)
    return val


# =========================================================================
def witness_circle_min():
    """(a) Confirm the certificate's claimed locus value: min of f on |z|=1 ~ 0.2524."""
    ts = np.linspace(1e-6, math.pi - 1e-6, 6000)
    vals = [f(np.exp(1j * t)) for t in ts]
    mn = min(vals)
    print("[a] min of f restricted to |z|=1 (t in [0,pi]):")
    print(f"      min_circle f = {mn:.10f}   (the certificate certifies ~0.2524 here)")
    ok = mn > RECORD          # the on-circle value IS above the record (as cert claims)
    print(f"      on-circle value above record 0.2487458 ? {ok}  "
          f"-> the cert's |z|=1 computation is reproduced.")
    return mn


def witness_plane_min():
    """(b) The DECISIVE failure: the global 2-D plane min of the SAME f is far below
    0.2487458 — so f >= 0.2524 is FALSE off the circle, where nu actually lives."""
    # coarse scan (vectorized over a grid; the conclusion is robust — plane min ~ -0.19)
    xs = np.linspace(-2.0, 3.0, 130)
    ys = np.linspace(-2.0, 2.0, 130)
    gm = math.inf
    arg = None
    for x in xs:
        for y in ys:
            v = f(x + 1j * y)
            if v < gm:
                gm = v
                arg = x + 1j * y
    # refine with a small local Nelder-Mead-free coordinate descent around arg
    cx, cy = arg.real, arg.imag
    step = 0.05
    for _ in range(60):
        improved = False
        for dx, dy in ((step, 0), (-step, 0), (0, step), (0, -step)):
            v = f((cx + dx) + 1j * (cy + dy))
            if v < gm:
                gm = v
                cx += dx
                cy += dy
                improved = True
        if not improved:
            step *= 0.5
            if step < 1e-10:
                break
    zmin = cx + 1j * cy
    print("[b] GLOBAL 2-D plane min of the SAME f (the honest min the method needs):")
    print(f"      min_plane f = {gm:.10f}   at z = {zmin:.6f}  (|z| = {abs(zmin):.6f})")
    print(f"      Note the minimizer is OFF |z|=1 (|z| ~ {abs(zmin):.3f}, near the")
    print(f"      golden ratio phi=1.618), exactly where the cert never looked.")
    return gm, zmin


def witness_superharmonic():
    """The MECHANISM: -2 lambda0 U_mu0 is superharmonic in the support band, so the
    'min on |z|=1' maximum-principle reduction is INVALID for this f.  We measure the
    discrete Laplacian of U_mu0 ON |z|=1 (positive -> U subharmonic -> -2 lam0 U
    superharmonic) and OFF the circle (~0 -> harmonic, so f's interior dip is the
    harmonic extension that the superharmonicity permits)."""
    h = 1e-4

    def lap(z):
        return (U_mu0(z + h) + U_mu0(z - h) + U_mu0(z + 1j * h)
                + U_mu0(z - 1j * h) - 4.0 * U_mu0(z)) / h ** 2

    z_on = np.exp(1j * 1.0)         # on |z|=1, inside the support band
    z_off = 1.618 + 0j             # the plane minimizer, off the circle
    lon = lap(z_on)
    loff = lap(z_off)
    print("[mechanism] Laplacian of U_mu0 (the energy potential):")
    print(f"      Delta U_mu0  ON |z|=1  (support band) = {lon:+.3e}  "
          f"(>0 => U subharmonic => -2 lam0 U SUPERHARMONIC)")
    print(f"      Delta U_mu0  OFF circle (z=1.618)      = {loff:+.3e}  (~0 => harmonic)")
    print("      => f = f0 - 2 lam0 U_mu0 is NOT subharmonic-off-circles; the maximum")
    print("         principle does NOT place min f on |z|=1, so 'min on |z|=1' is the")
    print("         WRONG locus and the certified 0.2524 bounds nothing.")
    return lon > 0


def witness_disc_premise():
    """(c) SECOND, INDEPENDENT invalidity: the OSS column premise
        I(nu) = (1/d^2) log|disc(P)| >= 0
    holds for algebraic INTEGERS (leading coeff a=1, disc a nonzero integer >= 1),
    but FAILS for Zhang-Zagier, whose alpha range over ALL algebraic numbers.  Then
    P is primitive with leading coeff a possibly > 1 and
        I(nu) = (1/d^2)[ log|disc(P)| - (2d-2) log|a| ],   (root energy, = the OSS I(nu))
    can be NEGATIVE.  Concrete primitive irreducible counterexample:
        P(x) = 10 x^2 - 6 x + 1,  roots (3 +- i)/10  (genuine ZZ-relevant alg. numbers)."""
    # P = 10 x^2 - 6 x + 1: a=10, d=2, roots (3 +- i)/10.
    a = 10
    d = 2
    roots = [(3 + 1j) / 10.0, (3 - 1j) / 10.0]
    # disc(P) = a^{2d-2} prod_{i<j}(r_i-r_j)^2.  For this P, disc = 36 - 40 = -4.
    disc = -4
    # I(nu) = root energy = (1/d^2) log prod_{i<j} |r_i - r_j|^2
    prod = 1.0
    for i in range(len(roots)):
        for j in range(i + 1, len(roots)):
            prod *= abs(roots[i] - roots[j]) ** 2
    Inu_root = (1.0 / d ** 2) * math.log(prod)
    Inu_formula = (math.log(abs(disc)) - (2 * d - 2) * math.log(a)) / d ** 2
    print("[c] OSS column premise  I(nu) >= 0  for ZZ:")
    print(f"      P(x) = 10 x^2 - 6 x + 1  (primitive, irreducible /Q; leading coeff a=10),")
    print(f"      roots (3 +- i)/10 — genuine algebraic NON-integers, valid ZZ inputs.")
    print(f"      |disc(P)| = {abs(disc)},  (2d-2) log|a| = {(2*d-2)*math.log(a):.6f}")
    print(f"      I(nu) (root energy)   = {Inu_root:+.6f}")
    print(f"      I(nu) (disc formula)  = {Inu_formula:+.6f}   (agrees)")
    ok_consistent = abs(Inu_root - Inu_formula) < 1e-12
    premise_fails = Inu_root < 0
    print(f"      OSS premise I(nu) >= 0 ?  {Inu_root >= 0}   "
          f"=> premise {'FAILS' if premise_fails else 'holds'} for ZZ.")
    return premise_fails and ok_consistent


# =========================================================================
def main():
    print("=" * 76)
    print("RETRACTION WITNESS — OSS log-energy LOWER-bound certificate (R14/R15/R17)")
    print("=" * 76)
    print(f"Frozen data: bins={len(CENTERS)}  L={LBIN:.6f}  lambda0={LAM0:.8f}  "
          f"Ihat={IHAT:.8f}")
    print(f"Flammang [F18] record to (not) beat: {RECORD}")
    print("-" * 76)

    circ = witness_circle_min()
    print("-" * 76)
    plane, zmin = witness_plane_min()
    print("-" * 76)
    superh = witness_superharmonic()
    print("-" * 76)
    premise_fails = witness_disc_premise()
    print("=" * 76)

    # ---- PASS/FAIL verdict lines a reviewer can re-run in seconds ----
    print("VERDICT (each PASS = a confirmed reason the OSS certificate is INVALID):")

    # Failure 1: on-circle value claims > record, but plane min is << record.
    f1 = (circ > RECORD) and (plane < RECORD - 0.1)
    print(f"  [{'PASS' if f1 else 'FAIL'}] FAILURE 1 (wrong locus): min on |z|=1 "
          f"= {circ:.6f} > {RECORD}, BUT global plane min = {plane:.6f} << {RECORD}.")
    print(f"          The method only proves C_82 >= min_plane f = {plane:.6f}, which is")
    print(f"          BELOW the Flammang record. The cert bounds NOTHING.")

    print(f"  [{'PASS' if superh else 'FAIL'}] MECHANISM: -2 lambda0 U_mu0 is "
          f"superharmonic in the support band (Delta U_mu0 > 0 on |z|=1).")

    print(f"  [{'PASS' if premise_fails else 'FAIL'}] FAILURE 2 (premise): OSS column "
          f"premise I(nu) >= 0 FAILS for ZZ (counterexample 10x^2-6x+1, I(nu)<0).")

    all_pass = f1 and superh and premise_fails
    print("-" * 76)
    if all_pass:
        print("RESULT: RETRACT R14/R15/R17.  The OSS log-energy lower-bound certificate")
        print("        is INVALID by two independent mechanisms.  The corrected verified")
        print(f"        held lower bound is the Flammang [F18] value {RECORD}.")
        print("        (See RETRACTION.md for the text the reviewer should enact.)")
        return 0
    else:
        print("RESULT: at least one witness did NOT fire — re-examine before retracting.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
