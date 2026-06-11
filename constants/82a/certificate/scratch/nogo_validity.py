"""
NO-GO / balanced signed-sum hierarchy — VALIDITY of the moment columns.

For a sign vector s = (s_1,...,s_k), s_i in {+1,-1}, BALANCED means sum s_i = 0.
Define the signed-sum moment column

    C_{Q_S}(nu) = INT...INT log| sum_i s_i x_i | dnu(x_1)...dnu(x_k)
                = (1/d^k) log | PROD_{i_1,...,i_k} ( sum_m s_m a_{i_m} ) |

where a_1..a_d are the conjugates of alpha (roots of the minimal poly P, monic
in Z[x], so the a_i are algebraic integers).

VALIDITY CLAIM (to confirm/refute):
  the inner product PROD over all index tuples (i_1,...,i_k) of (sum_m s_m a_{i_m})
  is a RATIONAL INTEGER, and is NONZERO off a finite exception set; hence its
  absolute value is >= 1, so log|.| >= 0, so C_{Q_S}(nu) >= 0.

This script:
 (1) Confirms the product is an integer (symmetric in roots => rational; algebraic
     integers => integer) for k=2,4,6 over several P.
 (2) Characterizes the TRIVIAL zero index-patterns (factors forced to 0 for every P
     by the additive/cancellation structure) vs the genuinely-vanishing reduced
     product.
 (3) Checks the reduced (nonzero-factor) product is a nonzero integer (|.|>=1).

Balanced is the right family: for UNBALANCED s (sum s_i != 0) the linear form is
NOT translation invariant, and a translate x -> x + c shifts sum s_i x_i by
(sum s_i) c, so the form is not even fixed under the field's Galois/affine
symmetries the way the energy is. We focus on balanced.
"""
import sympy as sp
import numpy as np
from itertools import product
import math

x = sp.symbols('x')


def conj_set(P, prec=60):
    return [complex(r) for r in sp.Poly(P, x).nroots(n=prec)]


def signed_product(roots, s, tol=1e-9):
    """PROD over all d^k index tuples of (sum_m s_m a_{i_m}).
    Returns (n_zero, reduced_product, trivial_zero_count, nontrivial_zero_count).
    A factor is 'trivially zero' if the index tuple admits a sign-respecting
    pairing of EQUAL indices that cancels: i.e. the multiset of (index, sign)
    cancels. We detect trivial by: the factor is identically zero as a function of
    the roots, which (for generic roots) means the tuple's signed index-incidence
    vector is zero: for each index value v, sum of signs s_m over positions m with
    i_m = v is 0 for ALL v. That is the structural always-zero set."""
    d = len(roots)
    k = len(s)
    n_zero = 0
    triv = 0
    nontriv = 0
    log_abs = 0.0          # accumulate log|red| to avoid overflow
    phase = 1.0 + 0j       # accumulate unit phase
    for tup in product(range(d), repeat=k):
        val = sum(s[m] * roots[tup[m]] for m in range(k))
        if abs(val) < tol:
            n_zero += 1
            # structural-zero test: signed incidence per index value == 0
            incid = {}
            for m in range(k):
                incid[tup[m]] = incid.get(tup[m], 0) + s[m]
            if all(v == 0 for v in incid.values()):
                triv += 1
            else:
                nontriv += 1
        else:
            log_abs += math.log(abs(val))
            phase *= val / abs(val)
    return n_zero, log_abs, phase, triv, nontriv


def balanced_sign_vectors(k):
    """All balanced sign vectors of length k (sum = 0), up to global sign &
    coordinate permutation we just return canonical reps with first half +."""
    if k % 2 != 0:
        return []
    half = k // 2
    # canonical: s_1=+1; choose positions of the remaining (half-1) +1's among k-1
    from itertools import combinations
    reps = []
    for plus_pos in combinations(range(1, k), half - 1):
        s = [-1] * k
        s[0] = 1
        for p in plus_pos:
            s[p] = 1
        reps.append(tuple(s))
    return reps


if __name__ == "__main__":
    tests = {
        'x^2-x-1 (golden)': x**2 - x - 1,
        'z^2-z+1 (z->1-z sym)': x**2 - x + 1,
        'x^3-x-1': x**3 - x - 1,
        'x^4-x-1': x**4 - x - 1,
        'x^4-10x^2+1 (Q(r2,r3))': x**4 - 10*x**2 + 1,
        'x^3-2': x**3 - 2,
    }

    for k in (2, 4, 6):
        sign_reps = balanced_sign_vectors(k)
        print("=" * 90)
        print(f"k = {k}   balanced sign patterns (canonical reps): {sign_reps}")
        print("=" * 90)
        for sname, s in [("|".join('+' if v > 0 else '-' for v in sr), sr) for sr in sign_reps]:
            print(f"\n  sign pattern s = {sname}")
            for pname, P in tests.items():
                roots = conj_set(P)
                d = len(roots)
                if d**k > 70000:   # keep brute force cheap; skip huge
                    continue
                n_zero, log_abs, phase, triv, nontriv = signed_product(roots, s)
                nfac = d**k
                if n_zero < nfac:
                    # nearest integer test in log domain: |red| should be a positive
                    # integer; check log_abs is close to log(round) and phase ~ +-1 real.
                    val_abs = math.exp(log_abs) if log_abs < 30 else float('inf')
                    nearest = round(val_abs) if val_abs < 1e15 else None
                    Jval = log_abs / d**k
                    # integer check: real-rational (phase real to ~tol) and |red|>=1
                    phase_im = abs(phase.imag)
                    if nearest is not None:
                        err = abs(val_abs - nearest)
                        intflag = "INT-OK" if (err < 1e-5 or err < 1e-4 * val_abs) and phase_im < 1e-5 else f"INT?err={err:.2e},Im={phase_im:.1e}"
                    else:
                        intflag = f"|red|=e^{log_abs:.2f} (huge, Im={phase_im:.1e})"
                    print(f"     {pname:<26} d={d} fac={nfac:5d} zero={n_zero:5d} "
                          f"(triv={triv} nontriv={nontriv}) log|red|={log_abs:8.3f} "
                          f"{intflag}  J={Jval:+.5f}")
                else:
                    print(f"     {pname:<26} d={d} ALL FACTORS ZERO (degenerate)")
