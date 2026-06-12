"""
Driver: rigorously certify an UPPER bound on C_82 = log h(q) for a SINGLE chosen
admissible q in Doche's Doc01b limit-point family (base P1,P2,P4,P6,P8 + Q=Q1*Q2,
D = max(sum q_i deg P_i, 56)).

It reuses the EXISTING, reviewer-verified certificate harness in bound_01_doche_base.py
verbatim:
  - certify_maxAB(q, ...) : the outward-rounded max(A,B) quadrature enclosure
    (the same code that certified the R5 record q*).
  - a q-specific soundness selftest: the per-cell bound cell_int_maxAB must
    dominate the true int_cell max(A,B) dt (sampled at high precision via mpmath)
    on random cells, for THIS q (not just QSTAR).
Admissibility (Doche Lemma 5) is q-independent (it constrains only the polynomial
dictionary), so bound_01_doche_base.admissibility_check() certifies it once for all q.

Usage:
  python3 certify_q.py q1 q2 q3 q4 q5 [M0] [max_refine] [rem_cap]
Default M0=200000, max_refine=14, rem_cap=1e-10 (same as stageB).
The R5 record to beat is the CERTIFIED value 0.2543326887.
"""

import sys
import math
import numpy as np
import bound_01_doche_base as vu

RECORD_CERT = 0.2543326887   # R5 reviewer-verified CERTIFIED log h(q*)


def selftest_q(q, ntest=200, seed=11):
    """Soundness for THIS q: cell_int_maxAB(a,b,q) >= true int_cell max(A,B) dt."""
    import mpmath as mp
    import random
    mp.mp.prec = 140
    ASCmp = {nm: [int(c) for c in vu.ASC[nm]] for nm in vu.ASC}

    def G_exact(t):
        w = mp.e**(1j * mp.mpf(t)) - mp.e**(2j * mp.mpf(t))

        def lp(asc):
            v = mp.mpc(0)
            for c in reversed(asc):
                v = v * w + c
            return mp.log(abs(v))
        A = sum(mp.mpf(q[i]) * lp(ASCmp[nm])
                for i, nm in enumerate(["P1", "P2", "P4", "P6", "P8"]))
        B = lp(ASCmp["Q1"]) + lp(ASCmp["Q2"])
        return float(max(A, B))

    random.seed(seed)
    As, Bs = [], []
    for _ in range(ntest):
        c = random.uniform(0.001, 2 * math.pi - 0.001)
        wdt = 10 ** random.uniform(-6, -3.5)
        As.append(c)
        Bs.append(min(c + wdt, 2 * math.pi - 1e-9))
    A = np.array(As)
    B = np.array(Bs)
    worst = 0
    for cap, tag in [(0.0, "flat"), (1e-9, "midpt")]:
        cell_hi, refine = vu.cell_int_maxAB(A, B, np.asarray(q, float), cap)
        viol = 0
        for i in range(len(A)):
            K = 60
            ts = [A[i] + (B[i] - A[i]) * k / K for k in range(K + 1)]
            gs = [G_exact(t) for t in ts]
            true_int = (B[i] - A[i]) / K * (
                0.5 * gs[0] + 0.5 * gs[-1] + sum(gs[1:-1]))
            if cell_hi[i] < true_int - 1e-12:
                viol += 1
                if viol <= 5:
                    print(f"  [{tag}] VIOLATION cell[{A[i]:.5f},{B[i]:.5f}] "
                          f"hi={cell_hi[i]:.10f} < true~{true_int:.10f}")
        print(f"  selftest[{tag}]: {viol}/{ntest} violations  (MUST be 0)")
        worst += viol
    return worst == 0


if __name__ == "__main__":
    args = sys.argv[1:]
    q = np.array([float(args[i]) for i in range(5)])
    M0 = int(args[5]) if len(args) > 5 else 200000
    max_refine = int(args[6]) if len(args) > 6 else 14
    rem_cap = float(args[7]) if len(args) > 7 else 1e-10

    print(f"=== certify_q for q = {q.tolist()} ===")
    print(f"    M0={M0} max_refine={max_refine} rem_cap={rem_cap}")

    print("\n[float] q-independent calibration gate (Doche q -> 1.289735):")
    dq = [13.1, 10.6, 3.2, 1.15, 0.24]
    vcal = vu.float_value(q=dq)
    print(f"    float_value(Doche q) = {math.exp(vcal):.8f}  (Doche published 1.289735)")
    vq = vu.float_value(q=q.tolist())
    print(f"[float] log h(q) ~ {vq:.10f}  h ~ {math.exp(vq):.10f}   (CONJECTURE)")

    print("\n[admissibility] (Doche Lemma 5; q-independent)")
    vu.admissibility_check()

    print("\n[selftest_q] soundness of per-cell bound for THIS q")
    ok = selftest_q(q)
    print(f"    selftest passed: {ok}")

    print("\n[certify] rigorous max(A,B) quadrature enclosure")
    logh_hi, nbad, elapsed, n_leaf = vu.certify_maxAB(
        q, "q", RECORD_CERT, M0=M0, max_refine=max_refine,
        rem_cap=rem_cap, verbose=True)

    print("\n=== RESULT ===")
    print(f"  CERTIFIED  log h(q) <= {logh_hi:.10f}")
    print(f"  unresolved frontier cells = {nbad}  (MUST be 0 for a clean bound)")
    print(f"  R5 record (certified)     = {RECORD_CERT:.10f}")
    beats = (logh_hi < RECORD_CERT) and (nbad == 0)
    print(f"  beats R5 record (strict, frontier=0): {beats}")
    if beats:
        print(f"  margin below R5 record = {RECORD_CERT - logh_hi:.4e}")
    sys.exit(0 if (nbad == 0) else 1)
