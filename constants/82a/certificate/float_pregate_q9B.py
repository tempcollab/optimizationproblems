"""
R8 FLOAT PRE-GATE for a NEW B-PERTURBER block (q9B family).

Clones verify_upper_q8A.float_value with a THIRD perturber block Q9B carried at
exponent qJ >= 0 on the B-branch (alongside Q5,Q6).  Q9B adds qJ*log|Q9B| to B AND
qJ*deg(Q9B) to arg_B (which ATTAINS D).  Joint Nelder-Mead re-opt of all exponents at
high N, seeded from the held R4 point.

GATE (run_state Rule, outline step 5): require an N-STABLE joint drop >= 5e-6 below the
held 0.2538893183 (>= ~25-40x the ~1.2-2.0e-7 cert slack) AND qJ* > 0 before any certify.

The screen (screen_Bbranch*.py) found NO firing-AND-admissible B-perturber: every
admissible block has m_B > 0 (dry).  This gate is run on the LEAST-DRY admissible block
to CONFIRM the lever is dry (qJ* -> 0, drop ~ 0).  A firing-but-inadmissible block (j5,
the reviewer's X4-X3-X+1, etc.) is NOT a valid certificate input -- it violates the
construction's coprimality/Q(0)=Q(1)=1, so a "drop" it produces is not a valid bound.

Reproduce:  python3 float_pregate_q9B.py <block> [Nopt] [Neval]
            block = comma-separated DESCENDING coeffs, e.g. 1,-1,1  (X^2-X+1)
"""
import sys
import numpy as np
from scipy.optimize import minimize

import verify_upper as vu
import verify_upper_q8A as q8

HELD = 0.2538893183   # TRUE held verified upper (R4). NEVER a stale/superseded target.

R4_q = [14.011500, 13.443930, 2.643590, 2.299880, 0.252420]
R4_qE, R4_qF, R4_qG, R4_qH = 0.575080, 0.568800, 0.891590, 0.066860


def pv(c, x):
    r = np.zeros_like(x)
    for cc in c:
        r = r * x + cc
    return r


def make_eval(Q9B, N):
    """f(theta)=log h for q9B family, Q9B a NEW B-perturber (descending). theta =
    (q1..q5, qE, qF, qG, qH, qJ). Q9B adds qJ*log|Q9B| to B and qJ*deg to arg_B."""
    deg9 = len(Q9B) - 1
    s = (np.arange(N) + 0.5) / N
    z = np.exp(2j * np.pi * s)
    chi = z * (1 - z)
    logP = [np.log(np.abs(pv(vu.BASE[i], chi))) for i in range(5)]
    logQ1 = np.log(np.abs(pv(vu.Q1, chi)))
    logQ2 = np.log(np.abs(pv(vu.Q2, chi)))
    logQ5 = np.log(np.abs(pv(q8.Q5, chi)))
    logQ6 = np.log(np.abs(pv(q8.Q6, chi)))
    logj3 = np.log(np.abs(pv(q8.Q7, chi)))
    logj9 = np.log(np.abs(pv(q8.Q8, chi)))
    logQ9B = np.log(np.abs(pv(Q9B, chi)))
    DEGP = vu.DEGP

    def f(theta):
        q = theta[:5]; qE, qF, qG, qH, qJ = theta[5:]
        if min(theta) < -1e-9:
            return 10.0
        A = (q[0]*logP[0]+q[1]*logP[1]+q[2]*logP[2]+q[3]*logP[3]+q[4]*logP[4]
             + qG*logj3 + qH*logj9)
        B = logQ1 + logQ2 + qE*logQ5 + qF*logQ6 + qJ*logQ9B
        G = np.maximum(A, B)
        argA = float(np.dot(q, DEGP)) + qG*q8.DEG_Q7 + qH*q8.DEG_Q8
        argB = vu.DEGQ + qE*q8.DEG_Q5 + qF*q8.DEG_Q6 + qJ*deg9
        D = max(argA, argB)
        return float(np.mean(G)) / D
    return f


def main():
    blockname = sys.argv[1] if len(sys.argv) > 1 else '1,-1,1'
    Nopt = int(sys.argv[2]) if len(sys.argv) > 2 else 400_000
    Neval = int(sys.argv[3]) if len(sys.argv) > 3 else 4_000_000
    Q9B = [int(x) for x in blockname.split(',')]
    deg = len(Q9B) - 1
    print("=" * 90)
    print(f"R8 FLOAT PRE-GATE q9B  block={Q9B} deg={deg}  Nopt={Nopt} Neval={Neval}")
    print(f"HELD (R4 verified upper) = {HELD:.10f}")
    print("=" * 90, flush=True)

    x0 = np.array(R4_q + [R4_qE, R4_qF, R4_qG, R4_qH, 0.0])
    fopt = make_eval(Q9B, Nopt)
    base = fopt(x0)
    print(f"base log h at R4 point (qJ=0), Nopt: {base:.10f}", flush=True)

    res = minimize(fopt, x0, method='Nelder-Mead',
                   options=dict(maxiter=6000, maxfev=6000, xatol=1e-7, fatol=1e-11))
    print(f"opt log h (Nopt={Nopt}): {res.fun:.10f}  qJ*={res.x[9]:.6f}", flush=True)

    feval = make_eval(Q9B, Neval)
    val_hi = feval(res.x)
    base_hi = feval(x0)
    drop = HELD - val_hi
    print(f"\nAt N={Neval} (stable eval):")
    print(f"  base (qJ=0)         = {base_hi:.10f}")
    print(f"  re-optimized log h  = {val_hi:.10f}")
    print(f"  qJ* (new B-exp)     = {res.x[9]:.6f}")
    print(f"  drop below HELD     = {drop:.4e}")
    GATE = 5e-6
    passed = (drop >= GATE) and (res.x[9] > 1e-6)
    print(f"\n  FLOAT GATE (>= {GATE:.0e}, qJ*>0): "
          f"{'PASS' if passed else 'FAIL (sub-gate / dry)'}")
    print("=" * 90)
    return passed, drop, res.x


if __name__ == "__main__":
    main()
