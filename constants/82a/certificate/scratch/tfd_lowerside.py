"""tfd_lowerside.py — the lower-side (Flammang) parallel.

Flammang's auxiliary function: f(z)=log+|w| - sum_j c_j log|Q_j(w)|, minimized over the
FULL contour C={|z|=1} (t in [0,pi] by symmetry); columns chosen by weighted integer
transfinite diameter with weight phi=(max(1,|z|)max(1,|1-z|))^{-1} = exp(-g(z)).

Parallel functional to the upper-side r_Q: define, on the lower side, the average
log-potential of Q's roots against the BINDING/min-locus measure of f.  Concretely,
at the Flammang optimum f attains its min on a sub-locus L_min of the contour; the
LP complementary slackness makes ACTIVE columns (c_j>0) satisfy a stationarity
relation analogous to r_Q=logh.  We check the qualitative parallel:
  (i) the Flammang active columns (c_j>0) cluster their weighted-potential value, while
  (ii) the weight phi=exp(-g) is the lower-side analog of the upper-side measure mu_act.

We compute, for each Flammang column Q_j, the WEIGHTED contour average
  s_j := (1/deg Q_j) INT_C log|Q_j(w)| dmu_low ,  dmu_low = (the binding measure),
and look at whether the active (c_j>0) columns share a common level — the lower-side
analog of r_Q=logh.  We use the Flammang equilibrium binding measure approximated by
the sub-level set {f < min f + eps} as the dual measure support.
"""
import numpy as np
import flammang_table1 as ft

T = ft.get_table()


def pv(coef_hl, x):
    r = np.zeros_like(x, dtype=complex)
    for c in coef_hl:
        r = r * x + c
    return r


def contour_half(N):
    t = (np.arange(N) + 0.5) / N * np.pi      # t in [0,pi] (symmetry-reduced)
    z = np.exp(1j * t)
    w = z * (1 - z)
    return t, z, w


def f_flammang(N):
    t, z, w = contour_half(N)
    g = np.log(np.maximum(1.0, np.abs(w)))    # log+|w| = g on |z|=1
    aux = g.copy()
    for c, asc in T:
        hl = asc[::-1]
        aux = aux - c * np.log(np.abs(pv(hl, w)))
    return t, z, w, g, aux


if __name__ == "__main__":
    N = 400_000
    t, z, w, g, aux = f_flammang(N)
    mmin = aux.min()
    print(f"Flammang min f = {mmin:.7f}  (record lower bound 0.2487458)")
    # binding sub-locus: where f is within eps of its min
    for eps in (1e-3, 3e-3, 1e-2):
        msk = aux < mmin + eps
        print(f"  sublevel f<min+{eps}: mass-frac {msk.mean():.4f}  "
              f"t-range t~{t[msk].min():.3f}..{t[msk].max():.3f}")

    # lower-side analog of r_Q: weighted contour average against the binding measure.
    # Use the dual binding measure approximated by the equilibrium of the min-locus.
    # As a QUALITATIVE parallel: compute (1/deg) INT_C log|Q_j| * w_phi dt with
    # w_phi = exp(-g) (Flammang's weight) NORMALIZED, for each column, and see whether
    # ACTIVE columns (c_j>0) sit lower than the trivial level (the transfinite-diameter
    # extremizer property: active columns are the small-norm ones).
    phi = np.exp(-g)
    phi /= phi.mean()
    print("\nidx  c_j         deg  s_j=(1/deg)INT log|Q| phi dt   active(c>1e-6)")
    rows = []
    for i, (c, asc) in enumerate(T):
        hl = asc[::-1]; deg = len(asc) - 1
        if deg == 0:
            continue
        sj = np.mean(phi * np.log(np.abs(pv(hl, w)))) / deg
        rows.append((i, c, deg, sj))
        print(f"{i:3d}  {c:.3e}  {deg:3d}   {sj:+.6f}   {'ACTIVE' if c>1e-6 else 'tiny'}")
    rows = np.array([(r[1], r[3], 1.0 if r[1] > 1e-4 else 0.0) for r in rows])
    act = rows[:, 2] > 0.5
    print(f"\nactive (c_j>1e-4) columns: s_j mean {rows[act,1].mean():+.5f} "
          f"std {rows[act,1].std():.5f}  ;  tiny-c columns s_j mean "
          f"{rows[~act,1].mean():+.5f}")
