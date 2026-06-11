"""tfd_setup.py — shared numerics for the integer-transfinite-diameter investigation.

Loads the held R11 upper-bound family (h=Q1*Q2*Q5^qE*Q6^qF), builds the contour
w(t)=z(1-z) on |z|=1, the A/B branches, the active set {B>A}, and the active-arc
measure mu_act.  All pure float numerics for grounding the structural theorem.
"""
import numpy as np
import verify_upper as vu
import verify_upper_q6 as vq6

# Held R11 optimum
Q = np.array([13.937341, 12.515102, 2.541409, 2.068537, 0.753965])
QE = 0.891271   # exponent of Q5 (deg 12)
QF = 0.246614   # exponent of Q6 (deg 16)
D = vq6._Dval(Q, 0.0, 0.0, QE, QF)        # = 70.641076
LOGH = 0.2540419719                       # held certified upper value

# base / block polynomials (high->low coeff lists in X=z(1-z))
BASE = vu.BASE                            # [P1,P2,P4,P6,P8]
DEGP = vu.DEGP
Q1, Q2 = vu.Q1, vu.Q2
Q5, Q6 = vq6.Q5, vq6.Q6
DEG_Q5, DEG_Q6 = vq6.DEG_Q5, vq6.DEG_Q6


def pv(coef_hl, x):
    """Horner eval of a high->low coeff list at array x."""
    r = np.zeros_like(x, dtype=complex)
    for c in coef_hl:
        r = r * x + c
    return r


def contour(N):
    """t-grid on [0,2pi), w-values, A(t), B(t)."""
    t = (np.arange(N) + 0.5) / N * 2 * np.pi
    z = np.exp(1j * t)
    w = z * (1 - z)
    A = sum(Q[i] * np.log(np.abs(pv(BASE[i], w))) for i in range(5))
    B = (np.log(np.abs(pv(Q1, w))) + np.log(np.abs(pv(Q2, w)))
         + QE * np.log(np.abs(pv(Q5, w)))
         + QF * np.log(np.abs(pv(Q6, w))))
    return t, w, A, B


def active_mask(N):
    t, w, A, B = contour(N)
    return t, w, (B > A)


def logh_value(N=4_000_000):
    t, w, A, B = contour(N)
    G = np.maximum(A, B)
    return np.mean(G) / D


def r_of_Q(coef_hl, degQ, N=4_000_000):
    """r_Q = (1/degQ)*(1/2pi) INT_{B>A} log|Q(w(t))| dt  (uniform-in-t active mean)."""
    t, w, A, B = contour(N)
    act = B > A
    lq = np.log(np.abs(pv(coef_hl, w)))
    # (1/2pi) INT_act lq dt  =  mean over all t of (lq * 1_act) * 2pi /(2pi) ...
    # discretized: sum over active cells * (dt) / (2pi) = mean(lq*1_act)*N*(2pi/N)/(2pi)
    #            = mean(lq[act])* (frac active)
    integral = np.mean(np.where(act, lq, 0.0))   # = (1/2pi) INT_act lq dt
    return integral / degQ


def active_fraction(N=4_000_000):
    t, w, A, B = contour(N)
    return np.mean(B > A)


def _table():
    """Print Table 1 of upper_bound_paper.tex: r_Q per Flammang block at the record
    family.  Reproduces the normalized active potential r_Q = (1/deg)(1/2pi)INT_{B>A}
    log|Q(w)| dt and its gap to log h.  Run:  python3 scratch/tfd_setup.py"""
    from flammang_table1 import _TABLE_DESCENDING as T
    N = 400_000
    print(f"record family log h = {LOGH};  active fraction = {active_fraction(N):.4f}")
    print(f"{'block':8} {'deg':>3} {'r_Q':>10} {'r_Q - log h':>13}  status")
    # show the paper's selected rows in order, then the full sorted list
    sel = {19: 'improving direction', 13: 'active (Q5, r_Q=log h)',
           15: 'active (Q6, r_Q=log h)', 12: 'near-tight', 7: 'inactive',
           9: 'inactive', 3: 'inactive', 6: 'inactive'}
    for idx in [19, 13, 15, 12, 7, 9, 3, 6]:
        coef = T[idx - 1][1]; deg = len(coef) - 1
        r = r_of_Q(coef, deg, N)
        print(f"j{idx:<7} {deg:>3} {r:>10.6f} {r-LOGH:>+13.2e}  {sel[idx]}")
    print("\n(full table, all 24 blocks, sorted by r_Q):")
    rows = sorted(((idx, len(c)-1, r_of_Q(c, len(c)-1, N))
                   for idx, (_, c) in enumerate(T, 1)), key=lambda x: x[2])
    for idx, deg, r in rows:
        print(f"  j{idx:<3} deg{deg:>3}: r_Q={r:.6f}  diff={r-LOGH:+.2e}")


if __name__ == "__main__":
    _table()
