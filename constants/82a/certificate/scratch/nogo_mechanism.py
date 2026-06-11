"""
STRUCTURAL MECHANISM of the no-go.

C_n(mu) = INT log|S| d(rho^{*n}),  rho = mu ⊛ (-mu)  (symmetric difference measure,
real-positive-definite-Fourier).  S = sum of n iid difference draws.

CLAIM (the one-line reason): C_n(mu) is monotonically INCREASING in n, and for n>=2
it has a strictly positive value on every measure with bounded "spread" because the
n-fold self-convolution rho^{*n} pushes mass outward (the typical |S| grows like
sqrt(n)*std(rho)), so log|S| > 0 dominates. C_n<0 is only reachable as n=1 (single
difference, can be tiny) OR by collapsing mu to a near-atom at one point (excluded
exception corner z in {0,1}) so that ALL differences ~ 0.

This script demonstrates:
 (1) Monotonicity in n: C_1 < C_2 < C_3 < C_4 for every fixed reference measure.
 (2) The "spread" mechanism: define sigma^2 = INT |S|^2 d(rho^{*n}) = n * Var_rho.
     By Jensen on the (concave) log of |S|^2, C_n = (1/2)INT log|S|^2 d(rho^{*n}); as
     n grows, |S|^2 concentrates around n*Var and log(n*Var)/2 -> +inf, so C_n -> +inf.
 (3) Negative C_n needs Var_rho small, i.e. mu near an atom -> z in {0,1} corner.

We tabulate for several symmetric measures: C_n and the variance of rho (= 2*Var_mu),
showing C_n tracks (1/2)log(n*Var) and is >=0 once n*Var >~ 1.
"""
import numpy as np
from scratch.nogo_Cmu0 import (C_n_from_measure, conj_sym, zz_sym,
                               uniform_t_sym, shaped_t_sym)


def var_rho(pts, ms):
    """Var of the symmetric difference measure rho = mu ⊛ (-mu): mean 0,
    Var = E|x_a - x_b|^2 = 2 (E|x|^2 - |E x|^2) = 2 Var_mu (over complex)."""
    mean = (ms * pts).sum()
    var_mu = (ms * np.abs(pts - mean) ** 2).sum()
    return 2.0 * var_mu


if __name__ == "__main__":
    measures = {
        'uniform-t sym': uniform_t_sym(200),
        'concentrated sym': shaped_t_sym(200, 'concentrated'),
        'spread sym': shaped_t_sym(200, 'spread'),
        'bimodal sym': shaped_t_sym(200, 'bimodal'),
    }
    print("Monotonicity C_1<C_2<C_3<C_4 and the spread mechanism (vr = Var of rho):\n")
    print(f"{'measure':<20} {'vr':>7} | " + "  ".join(f"C_{n}" for n in (1,2,3,4))
          + " | " + "  ".join(f"½ln({n}vr)" for n in (1,2,3,4)))
    for name, (pts, ms) in measures.items():
        vr = var_rho(pts, ms)
        Cs = [C_n_from_measure(pts, ms, n, G=512) for n in (1, 2, 3, 4)]
        pred = [0.5 * np.log(n * vr) for n in (1, 2, 3, 4)]
        mono = "MONO-UP" if all(Cs[i] < Cs[i+1] for i in range(3)) else "NOT-MONO"
        print(f"{name:<20} {vr:7.3f} | " + "  ".join(f"{c:+.3f}" for c in Cs)
              + " | " + "  ".join(f"{p:+.3f}" for p in pred) + f"  {mono}")

    print("\nThe approximation C_n ~ (1/2) ln(n * Var_rho) is the spreading law:")
    print("  - For n>=2 and any NON-degenerate (diffuse) measure, n*Var_rho > 1, so C_n>0.")
    print("  - C_n<0 needs Var_rho < 1/n, i.e. mu collapsing to a near-atom (Var->0),")
    print("    which lands on the excluded {0,1} corner (z^2-z exception set).")

    # Show: as a measure concentrates toward z=1, Var_rho -> 0 and C_n -> -inf,
    # but that is the excluded atom.
    print("\nConcentration sweep: mass fraction f at node t0=0.05 (z~1), rest uniform:")
    K = 30
    t_half = (np.arange(K) + 0.5) / K * (np.pi / 2)
    unif = np.ones(K) / K
    spike = np.zeros(K); spike[0] = 1.0
    for f in (0.0, 0.3, 0.5, 0.7, 0.9):
        q = (1 - f) * unif + f * spike
        z, m = conj_sym(t_half, q / q.sum()); pts, ms = zz_sym(z, m)
        vr = var_rho(pts, ms)
        Cs = [C_n_from_measure(pts, ms, n, G=384) for n in (1, 2, 3, 4)]
        print(f"  f={f:.1f}: Var_rho={vr:.4f} | " + "  ".join(f"C_{n}={c:+.3f}" for n,c in zip((1,2,3,4),Cs)))
