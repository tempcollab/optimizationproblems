"""
Doche [Doc01b] RECORD-family limit-point objective h(q) for constant 82a.

Source: C. Doche, "Zhang-Zagier heights of perturbed polynomials",
J. Theor. Nombres Bordeaux 13 (2001) 103-110.  Polynomials and the best
parameter vector transcribed from the PDF figure images (pages 106, 109, 110;
the coefficient lists are bitmap images that pdfminer drops).  Each transcribed
polynomial's Zhang-Zagier height was cross-checked against the values Doche
prints, to 7+ digits (see verify_transcription() below).

Family (Doc01b proof, p.108-110): base polynomials P1,P2,P4,P6,P8 (a subset of
P1..P8, "forced by the search of the minimum of (9)") and a single perturbing
block Q(X) = Q1(X) * Q2(X) (each Q_i of degree 28, "chosen for their very small
height").  The limit-point measure (eq (9)) is

    h(q) = [ M( Q(z(1-z)) ) *
             exp( int_0^1 log+ | P1^q1 P2^q2 P4^q3 P6^q4 P8^q5 (chi(s)) / Q(chi(s)) | ds )
           ] ^ (2b / D(b)),
    D(b) = 2b * max( sum_m q_m deg_X P_m , deg_X Q ),
    chi(s) = e^{2 i pi s} (1 - e^{2 i pi s}).

Since h is independent of b (Doche), take b=1.  Writing the X-contour Mahler
measure as a single normalised integral exactly as in doche_hq.py:

    log h(q) = (1/D_max) * [ int_0^1 log|Q(chi(s))| ds
                            + int_0^1 log+ | (prod P_m^{q_m})(chi)/Q(chi) | ds ],
    D_max = max( sum_m q_m deg_X P_m , deg_X Q ).

CALIBRATION (Doc01b p.110):  h(13.1, 10.6, 3.2, 1.15, 0.24) = 1.289735 (record).
This module reproduces 1.289735 to 6 significant figures (verify_calibration()).

VALIDITY: identical to Doc01a (Lemmas 2,3,4,5): any admissible q makes log h(q)
a rigorous upper bound on C_82, no optimality of q needed.  Non-triviality
condition (4) holds (deg Q > 0; P's and Q are non-unit integer polynomials).
"""

import numpy as np

# Doc01b base polynomials in X (high-degree-first).  Names match Doc01b labels.
DB_P1 = [1, 0]                                   # X
DB_P2 = [-1, 1]                                  # 1 - X
DB_P4 = [1, -2, 4, -3, 1]                        # X^4-2X^3+4X^2-3X+1  (= Doc01a P3)
DB_P6 = [1, -3, 8, -16, 26, -27, 17, -6, 1]      # X^8-...+1, deg 8
DB_P8 = [1, -3, 7, -14, 30, -58, 96, -123, 114, -73, 31, -8, 1]  # deg 12 (= Doc01a P5)

# Perturbing factors (each degree 28 in X), Doc01b p.109.
DB_Q1 = [1, -7, 30, -97, 269, -679, 1612, -3618, 7646, -15180, 28457, -50741,
         86189, -138288, 206152, -279897, 339335, -360911, 331775, -260367,
         172556, -95554, 43677, -16221, 4786, -1084, 178, -19, 1]
DB_Q2 = [1, -7, 30, -96, 255, -586, 1212, -2360, 4573, -9148, 18749, -37783,
         71770, -124910, 195848, -273368, 335981, -359545, 331349, -260271,
         172542, -95553, 43677, -16221, 4786, -1084, 178, -19, 1]


# Base-polynomial dictionary for the record family, in the exponent order
# (q1,q2,q3,q4,q5) <-> (P1,P2,P4,P6,P8).
DB_PS = [DB_P1, DB_P2, DB_P4, DB_P6, DB_P8]
# Perturbing block Q = Q1 * Q2 (degree 56 in X) given AS A LIST OF FACTORS.
# IMPORTANT: never multiply Q1*Q2 into a single degree-56 coefficient list and
# Horner-evaluate it -- the product has integer coefficients up to ~6e11 and a
# deg-56 Horner sum on the chi contour suffers catastrophic cancellation (the
# log|Q| value is then wrong by ~10).  Always evaluate log|Q(chi)| as the SUM of
# log|Q1(chi)| + log|Q2(chi)| over the two stable degree-28 factors.
DB_QFACTORS = [DB_Q1, DB_Q2]
DEG_Q = sum(len(f) - 1 for f in DB_QFACTORS)   # = 56


def deg(c):
    return len(c) - 1


def _eval(c, x):
    return np.polyval(c, x)


def chi_grid(N):
    s = (np.arange(N) + 0.5) / N
    e = np.exp(2j * np.pi * s)
    return e * (1.0 - e)


def log_h(q, Ps=DB_PS, Qfactors=DB_QFACTORS, N=2_000_000):
    """
    log h(q) over the Doc01b record family (float midpoint Riemann sum).

    Limit measure (Doc01b eq (9)) :
        log h(q) = (1/D_max) int_0^1 log max( |prod_m P_m(chi)^{q_m}| , |Q(chi)| ) ds
        D_max = max( sum_m q_m deg_X P_m , deg_X Q ),   Q = prod of Qfactors.
    (int log max == int [log|Q| + log+|prodP^q/Q|], the Jensen-reduced form.)
    """
    q = np.asarray(q, dtype=float)
    assert len(q) == len(Ps)
    chi = chi_grid(N)
    log_prodP = np.zeros(len(chi))
    sum_qdegP = 0.0
    for qi, c in zip(q, Ps):
        log_prodP += qi * np.log(np.abs(_eval(c, chi)))
        sum_qdegP += qi * deg(c)
    log_Q = np.zeros(len(chi))
    deg_Q = 0
    for f in Qfactors:
        log_Q += np.log(np.abs(_eval(f, chi)))
        deg_Q += deg(f)
    Dmax = max(sum_qdegP, deg_Q)
    return np.mean(np.maximum(log_prodP, log_Q)) / Dmax


def h(q, **kw):
    return np.exp(log_h(q, **kw))


def verify_transcription(verbose=True):
    """Cross-check each transcribed polynomial's ZZ height vs Doche's printed value."""
    def zeta(c):
        r = np.roots(c); d = len(c) - 1; s = 0.0
        for X0 in r:
            z = (1 + np.sqrt(1 - 4 * X0)) / 2
            s += max(0, np.log(abs(z))) + max(0, np.log(abs(1 - z)))
        return np.exp(s / d)
    checks = [("P4", DB_P4, 1.2720196), ("P6", DB_P6, 1.297431163),
              ("P8", DB_P8, 1.289442541), ("Q1", DB_Q1, 1.288275594),
              ("Q2", DB_Q2, 1.288646007)]
    ok = True
    for name, c, tgt in checks:
        v = zeta(c)
        good = abs(v - tgt) < 1e-6
        ok = ok and good
        if verbose:
            print(f"H({name}) = {v:.9f}  (Doche {tgt})  {'OK' if good else 'MISMATCH'}")
    return ok


def verify_calibration(N=16_000_000, verbose=True):
    """Reproduce Doche's record h(13.1,10.6,3.2,1.15,0.24) = 1.289735."""
    q = [13.1, 10.6, 3.2, 1.15, 0.24]
    val = h(q, N=N)
    target = 1.289735
    rel = abs(val - target) / target
    if verbose:
        print(f"h(13.1,10.6,3.2,1.15,0.24) [converged] = {val:.9f}")
        print(f"Doche record (Doc01b p.110)            = {target}")
        print(f"relative difference                    = {rel:.2e}")
        print("agrees to 6 sig figs:", f"{val:.6g}" == f"{target:.6g}")
    return val, rel


if __name__ == "__main__":
    print("--- transcription check ---")
    verify_transcription()
    print("--- record calibration ---")
    verify_calibration()
