"""
R7 float objective: Doche Doc01b record family ENLARGED by a free-exponent third
perturbing block Q3 (entering the perturbing side with its own exponent qB), while
Q1*Q2 remains the FIXED distinguished block Q_{l+1} (exponent 1).

Doc01b perturbing side (Doche eq before line 1160, general l):
    perturbing product  =  Q_{l+1} * prod_{m<=l} Q_m^{q_{k+m}}
    D = 2b * max( sum_m q_m deg P_m ,  deg Q_{l+1} + sum_{m<=l} q_{k+m} deg Q_m )
Here Q_{l+1} = Q1*Q2 (deg 56, exponent 1, FIXED) and the single free block is
Q3 = Qa (deg 24, exponent qB).  At qB=0 this is IDENTICALLY the held R6 family.

    log h(q, qB)
      = (1/Dmax) * int_0^1 log max( |prod_m P_m(chi)^{q_m}| ,
                                    |Q1(chi)| |Q2(chi)| |Q3(chi)|^{qB} ) ds
    Dmax = max( sum_m q_m deg P_m ,  56 + qB * deg Q3 ),
    chi(s) = e^{2 i pi s}(1 - e^{2 i pi s}).

Validity (Doc01a Lemmas 2,3,4,5): any admissible (q, qB>=0) makes log h a true
limit point of the ZZ spectrum, hence an upper bound on C_82.  Admissibility of
W = Q1*Q2*Q3 verified separately (deg 80>0, W(0)=W(1)=1, Q3 squarefree, all gcds 1).

This module is a FLOAT objective only (midpoint Riemann sum) for the search; the
rigorous certificate is verify_upper_q3.py::certify_maxAB_q3.
"""

import numpy as np

# Doc01b base polynomials in X (high->low), identical to doche_hq_b / verify_upper.
DB_P1 = [1, 0]
DB_P2 = [-1, 1]
DB_P4 = [1, -2, 4, -3, 1]
DB_P6 = [1, -3, 8, -16, 26, -27, 17, -6, 1]
DB_P8 = [1, -3, 7, -14, 30, -58, 96, -123, 114, -73, 31, -8, 1]
DB_Q1 = [1, -7, 30, -97, 269, -679, 1612, -3618, 7646, -15180, 28457, -50741,
         86189, -138288, 206152, -279897, 339335, -360911, 331775, -260367,
         172556, -95554, 43677, -16221, 4786, -1084, 178, -19, 1]
DB_Q2 = [1, -7, 30, -96, 255, -586, 1212, -2360, 4573, -9148, 18749, -37783,
         71770, -124910, 195848, -273368, 335981, -359545, 331349, -260271,
         172542, -95553, 43677, -16221, 4786, -1084, 178, -19, 1]
# Q3 = Qa (Doc01a calibration perturber, deg 24, H = 1.290471208).
DB_Q3 = [1, -6, 24, -77, 217, -546, 1252, -2647, 5195, -9457, 15898, -24521,
         34402, -43345, 48207, -46413, 37963, -25934, 14558, -6596, 2357, -642,
         126, -16, 1]

DB_PS = [DB_P1, DB_P2, DB_P4, DB_P6, DB_P8]
DEGP = np.array([1, 1, 4, 8, 8])
DEG_Q12 = 56               # deg(Q1*Q2), the fixed distinguished block
DEG_Q3 = len(DB_Q3) - 1    # = 24


def _eval(c, x):
    return np.polyval(c, x)


def chi_grid(N):
    s = (np.arange(N) + 0.5) / N
    e = np.exp(2j * np.pi * s)
    return e * (1.0 - e)


def log_h(q, qB=0.0, N=2_000_000):
    """log h over the 6-exponent family (float midpoint Riemann sum).

      A(s) = sum_m q_m (1/2)log|P_m(chi)|^2     (= sum_m q_m log|P_m(chi)|)
      B(s) = log|Q1(chi)| + log|Q2(chi)| + qB*log|Q3(chi)|
      log h = (1/Dmax) * mean_s max(A, B),  Dmax = max(sum q_m deg P_m, 56+qB*24).
    """
    q = np.asarray(q, dtype=float)
    assert len(q) == 5
    chi = chi_grid(N)
    A = np.zeros(len(chi))
    sum_qdegP = 0.0
    for qi, c, dg in zip(q, DB_PS, DEGP):
        A += qi * np.log(np.abs(_eval(c, chi)))
        sum_qdegP += qi * dg
    B = (np.log(np.abs(_eval(DB_Q1, chi)))
         + np.log(np.abs(_eval(DB_Q2, chi)))
         + qB * np.log(np.abs(_eval(DB_Q3, chi))))
    Dmax = max(sum_qdegP, DEG_Q12 + qB * DEG_Q3)
    return np.mean(np.maximum(A, B)) / Dmax


def h(q, qB=0.0, **kw):
    return np.exp(log_h(q, qB=qB, **kw))


if __name__ == "__main__":
    # Anchor: qB=0 must reproduce the held R6 float ~0.2543308.
    qR6 = [11.73584, 8.77354, 2.44938, 1.55411, 0.53442]
    v0 = log_h(qR6, qB=0.0, N=16_000_000)
    print(f"anchor qB=0, q=R6: log h = {v0:.10f}  (held float ~0.2543308)")
