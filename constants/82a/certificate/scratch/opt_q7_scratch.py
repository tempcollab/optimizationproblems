"""
SCRATCH (conjecture step): joint re-optimization of the full exponent vector for the
R11 family h=Q1*Q2*Q5^qE*Q6^qF EXTENDED by ONE new low-degree free perturbing block QG.

Objective (float midpoint Riemann sum of log h):
  A(s) = sum_i q_i log|P_i(chi)|             (Doche A-branch, DEGP=[1,1,4,8,8] for D)
  B(s) = log|Q1| + log|Q2| + qE log|Q5| + qF log|Q6| + qG log|QG|
  G    = max(A,B)
  D    = max( sum_i q_i*DEGP_i , 56 + qE*degQ5 + qF*degQ6 + qG*degQG )
  log h = mean(G)/D

We seed at the R11 optimum (q, qE, qF) with qG=0 (anchor recovers the record exactly),
and jointly re-optimize all of q1..q5, qE, qF, qG for several candidate low-degree
Flammang Table-1 blocks. Report which block + exponent vector drops log h most below
0.2540419719. This is a CONJECTURE search; the rigorous claim is the certificate.
"""
import numpy as np
from scipy.optimize import minimize
import verify_upper as vu
import flammang_table1 as ft

DEGP = np.array([1, 1, 4, 8, 8], float)

# R11 held optimum
R11_Q = np.array([13.937341, 12.515102, 2.541409, 2.068537, 0.753965])
R11_QE = 0.891271
R11_QF = 0.246614

Q5 = [1, -3, 8, -18, 36, -62, 97, -123, 114, -73, 31, -8, 1]          # j13 deg12
Q6 = [1, -4, 10, -17, 26, -47, 119, -298, 592, -878, 963, -780, 464, -199, 59, -11, 1]  # j15 deg16
DEG_Q5 = 12
DEG_Q6 = 16

# Precompute base/perturber values on a grid (float)
N = 400000
s = (np.arange(N) + 0.5) / N
z = np.exp(2j * np.pi * s)
chi = z * (1 - z)

def pv(c, x):
    r = np.zeros_like(x)
    for cc in c:
        r = r * x + cc
    return r

logP = np.array([np.log(np.abs(pv(vu.BASE[i], chi))) for i in range(5)])  # (5,N)
logQ1 = np.log(np.abs(pv(vu.Q1, chi)))
logQ2 = np.log(np.abs(pv(vu.Q2, chi)))
logQ5 = np.log(np.abs(pv(Q5, chi)))
logQ6 = np.log(np.abs(pv(Q6, chi)))


def make_obj(logQG, degQG):
    def obj(x):
        q = x[:5]
        qE, qF, qG = x[5], x[6], x[7]
        A = q @ logP
        B = logQ1 + logQ2 + qE * logQ5 + qF * logQ6 + qG * logQG
        G = np.maximum(A, B)
        D = max(q @ DEGP, 56 + qE * DEG_Q5 + qF * DEG_Q6 + qG * degQG)
        return np.mean(G) / D
    return obj


def optimize_block(name, QG_desc):
    QG = list(reversed(QG_desc))  # ascending? table is descending; pv wants descending->
    # pv expects coefficients high->low (Horner with descending). table desc IS high->low.
    QG_hi_lo = QG_desc
    degQG = len(QG_desc) - 1
    logQG = np.log(np.abs(pv(QG_hi_lo, chi)))
    obj = make_obj(logQG, degQG)

    x0 = np.concatenate([R11_Q, [R11_QE, R11_QF, 0.0]])
    base_val = obj(x0)  # anchor: qG=0 must recover ~0.25404
    bounds = [(0.01, 40)] * 5 + [(0, 10), (0, 10), (0, 10)]
    best = None
    for trial in range(6):
        if trial == 0:
            xs = x0.copy()
        else:
            xs = x0 * (1 + 0.15 * np.random.randn(8))
            xs[7] = abs(np.random.randn()) * 0.5
            xs = np.clip(xs, [b[0] for b in bounds], [b[1] for b in bounds])
        res = minimize(obj, xs, method='Nelder-Mead',
                       options=dict(maxiter=40000, xatol=1e-9, fatol=1e-12))
        if best is None or res.fun < best.fun:
            best = res
    return name, degQG, base_val, best.fun, best.x


if __name__ == "__main__":
    print(f"anchor (qG=0) recovers R11 family float: ", end="")
    obj0 = make_obj(np.zeros(N), 1)
    print(f"{obj0(np.concatenate([R11_Q,[R11_QE,R11_QF,0.0]])):.10f} (record ~0.25404185)")
    print()
    tab = ft._TABLE_DESCENDING
    # candidate low-degree blocks (skip j1,j2 trivial w, w-1; skip j13,j15 = Q5,Q6)
    cands = {
        "j3": tab[2][1],   # deg3
        "j4": tab[3][1],   # deg3
        "j5": tab[4][1],   # deg4
        "j6": tab[5][1],   # deg7
        "j7": tab[6][1],   # deg8
        "j8": tab[7][1],   # deg8
        "j9": tab[8][1],   # deg8
        "j11": tab[10][1], # deg11
        "j12": tab[11][1], # deg12
        "j14": tab[13][1], # deg13
        "j16": tab[15][1], # deg16
        "j17": tab[16][1], # deg16
        "j19": tab[18][1], # deg17
    }
    results = []
    for nm, desc in cands.items():
        try:
            r = optimize_block(nm, desc)
            results.append(r)
            print(f"{nm:4s} deg={r[1]:2d}  anchor(qG=0)={r[2]:.10f}  "
                  f"JOINT min={r[3]:.10f}  drop_vs_record={0.2540419719 - r[3]:+.3e}  "
                  f"qG*={r[4][7]:.4f}")
        except Exception as e:
            print(f"{nm}: ERROR {e}")
    print()
    results.sort(key=lambda x: x[3])
    print("=== best candidates (lowest float log h) ===")
    for nm, deg, base, fun, x in results[:5]:
        print(f"{nm:4s} deg={deg:2d}  min={fun:.10f}  margin_vs_record={0.2540419719-fun:+.3e}")
        print(f"     q={np.round(x[:5],6).tolist()} qE={x[5]:.6f} qF={x[6]:.6f} qG={x[7]:.6f}")
