"""
R7 FLOAT PRE-GATE for a THIRD A-base block (q9A family).

Clones bound_07_block_j9.float_value_q8A with a THIRD A-base block Q9 carried at
exponent qI >= 0 alongside j3 (qG) and j9 (qH).  Joint Nelder-Mead re-optimization of
all 10 exponents (q1..q5, qE, qF, qG, qH, qI) at high N, seeded from the held R4 point.

GATE (run_state Rule, outline step 5): require an N-STABLE joint drop >= 5e-6 below the
held 0.2538893183 (>= ~25-40x the ~1.2-2.0e-7 cert slack) before any certify.

This is the saturation probe: it measures the BEST realized drop the design lever can
deliver from a given firing block.  Even the strongest firing-AND-coprime block reachable
on R4 (j16, r~=-0.0052) is fed here to bound the lever -- if it does not clear 5e-6, the
A-base lever is confirmed dry and no certify is run.

Reproduce:  python3 float_pregate_q9A.py <block> [Nopt] [Neval]
            block in {j16,j17,j20} (table firing-coprime) or a custom desc.
"""
import sys
import numpy as np
from scipy.optimize import minimize

import bound_01_doche_base as vu
import bound_07_block_j9 as q8
import flammang_table1 as ft

HELD = 0.2538893183   # GUARDRAIL 2: the TRUE held verified upper (R4). Overwrites stale.

# held R4 exponent point (10 exponents, qI for the new 3rd block seeded at 0)
R4_q = [14.011500, 13.443930, 2.643590, 2.299880, 0.252420]
R4_qE, R4_qF, R4_qG, R4_qH = 0.575080, 0.568800, 0.891590, 0.066860

BLOCKS = {
    'j16': list(ft._TABLE_DESCENDING[15][1]),
    'j17': list(ft._TABLE_DESCENDING[16][1]),
    'j20': list(ft._TABLE_DESCENDING[19][1]),
}


def pv(c, x):
    r = np.zeros_like(x)
    for cc in c:
        r = r * x + cc
    return r


def make_eval(Q9, N):
    """Return f(theta) = log h for the q9A family with 3rd A-base block Q9 (descending),
    theta = (q1..q5, qE, qF, qG, qH, qI). D re-evaluated with the extra A-base degree."""
    deg9 = len(Q9) - 1
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
    logQ9 = np.log(np.abs(pv(Q9, chi)))
    DEGP = vu.DEGP

    def f(theta):
        q = theta[:5]; qE, qF, qG, qH, qI = theta[5:]
        if min(theta) < -1e-9:
            return 10.0
        A = (q[0]*logP[0]+q[1]*logP[1]+q[2]*logP[2]+q[3]*logP[3]+q[4]*logP[4]
             + qG*logj3 + qH*logj9 + qI*logQ9)
        B = logQ1 + logQ2 + qE*logQ5 + qF*logQ6
        G = np.maximum(A, B)
        argA = float(np.dot(q, DEGP)) + qG*q8.DEG_Q7 + qH*q8.DEG_Q8 + qI*deg9
        argB = vu.DEGQ + qE*q8.DEG_Q5 + qF*q8.DEG_Q6
        D = max(argA, argB)
        return float(np.mean(G)) / D
    return f


def main():
    blockname = sys.argv[1] if len(sys.argv) > 1 else 'j16'
    Nopt = int(sys.argv[2]) if len(sys.argv) > 2 else 400_000
    Neval = int(sys.argv[3]) if len(sys.argv) > 3 else 4_000_000
    Q9 = BLOCKS.get(blockname)
    if Q9 is None:
        Q9 = [int(x) for x in blockname.split(',')]
    print("=" * 90)
    print(f"R7 FLOAT PRE-GATE q9A  block={blockname} deg={len(Q9)-1}  Nopt={Nopt} Neval={Neval}")
    print(f"HELD (R4 verified upper, GUARDRAIL 2) = {HELD:.10f}")
    print("=" * 90)

    x0 = np.array(R4_q + [R4_qE, R4_qF, R4_qG, R4_qH, 0.0])
    fopt = make_eval(Q9, Nopt)
    base = fopt(np.array(R4_q + [R4_qE, R4_qF, R4_qG, R4_qH, 0.0]))
    print(f"base log h at R4 point (qI=0), Nopt: {base:.10f}", flush=True)

    res = minimize(fopt, x0, method='Nelder-Mead',
                   options=dict(maxiter=6000, maxfev=6000, xatol=1e-7, fatol=1e-11))
    print(f"opt log h (Nopt={Nopt}): {res.fun:.10f}  qI*={res.x[9]:.6f}", flush=True)

    # re-evaluate the optimum at high N (the N-stable claim)
    feval = make_eval(Q9, Neval)
    val_hi = feval(res.x)
    base_hi = feval(np.array(R4_q + [R4_qE, R4_qF, R4_qG, R4_qH, 0.0]))
    drop = HELD - val_hi
    print(f"\nAt N={Neval} (stable eval):")
    print(f"  base (qI=0)         = {base_hi:.10f}")
    print(f"  re-optimized log h  = {val_hi:.10f}")
    print(f"  qI* (new block exp) = {res.x[9]:.6f}")
    print(f"  drop below HELD     = {drop:.4e}")
    GATE = 5e-6
    passed = (drop >= GATE) and (res.x[9] > 1e-6)
    print(f"\n  FLOAT GATE (>= {GATE:.0e}, qI*>0): {'PASS' if passed else 'FAIL (sub-gate / dry)'}")
    print("=" * 90)
    return passed, drop, res.x


if __name__ == "__main__":
    main()
