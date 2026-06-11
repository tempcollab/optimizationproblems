"""
ROUTE 3 — VALIDITY of the 4-point moment column
  Q(x1,x2,x3,x4) = x1 - x2 - x3 + x4

J(nu) = INT^4 log|x1-x2-x3+x4| dnu^4
      = (1/d^4) log| PROD_{i,j,k,l} (a_i - a_j - a_k + a_l) |

where a_1..a_d are the conjugates (roots of the min poly P). The product is
symmetric in the roots => rational; roots are algebraic integers => the product is
a RATIONAL INTEGER. Question: is it NONZERO (off a finite exception set), and which
index tuples force a zero factor?
"""
import sympy as sp
from itertools import product

x = sp.symbols('x')


def conj_set(P):
    return [complex(r) for r in sp.Poly(P, x).nroots(n=50)]


def classify(roots, tol=1e-9):
    """For all d^4 index tuples, count how many give a zero factor and group
    those zeros by the index-equality PATTERN."""
    d = len(roots)
    nzero = 0
    pattern_counts = {}
    prod = 1.0 + 0j
    for i, j, k, l in product(range(d), repeat=4):
        v = roots[i] - roots[j] - roots[k] + roots[l]
        if abs(v) < tol:
            nzero += 1
            # classify which equalities among (i,j,k,l) caused it
            pat = []
            if i == j: pat.append("i=j")
            if i == k: pat.append("i=k")
            if i == l: pat.append("i=l")
            if j == k: pat.append("j=k")
            if j == l: pat.append("j=l")
            if k == l: pat.append("k=l")
            key = tuple(pat) if pat else ("NONTRIVIAL(no index eq)",)
            pattern_counts[key] = pattern_counts.get(key, 0) + 1
        else:
            prod *= v
    return nzero, pattern_counts, prod


print("=" * 84)
print("ROUTE 3 VALIDITY: 4-point product PROD (a_i - a_j - a_k + a_l)")
print("Q = x1 - x2 - x3 + x4   (OSS future-work column)")
print("=" * 84)

tests = {
    'x^2-x-1 (golden)': x**2 - x - 1,
    'x^3-x-1': x**3 - x - 1,
    'x^4-x-1': x**4 - x - 1,
    'z^2-z+1 (z->1-z SYMMETRIC)': x**2 - x + 1,
    'z^2-z (excluded factor)': x**2 - x,
    'x^2-3x+1': x**2 - 3*x + 1,
    'x^3-2 (irreducible)': x**3 - 2,
    'x^4-10x^2+1 (sqrt2+sqrt3)': x**4 - 10*x**2 + 1,
}

for name, P in tests.items():
    roots = conj_set(P)
    d = len(roots)
    nzero, pats, prod = classify(roots)
    nfac = d**4
    print(f"\n{name}")
    print(f"  d={d}  #4-tuples={nfac}  #zero-factors={nzero}")
    print(f"  zero-pattern breakdown:")
    for key, cnt in sorted(pats.items(), key=lambda kv: -kv[1]):
        print(f"     {cnt:5d}  caused by {key}")
    if nzero < nfac:
        rounded = round(prod.real)
        print(f"  NONZERO product = {prod.real:.6f} + {prod.imag:.2e}i  -> nearest int {rounded}, err {abs(prod.real-rounded):.2e}")
        import math
        if abs(prod) > 0:
            J = math.log(abs(prod)) / d**4
            print(f"  J(nu) = (1/d^4) log|product| = {J:+.6f}")
