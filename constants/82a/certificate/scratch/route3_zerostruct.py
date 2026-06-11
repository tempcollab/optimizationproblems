"""
Characterize ALL zero factors of Q=x1-x2-x3+x4 over root-tuples, and pin down
the 'nontrivial' zeros (no index equality) for sqrt2+sqrt3 -- these are the real
question for validity (do they form a finite exception set, or can they make the
WHOLE nonzero product vanish for some ZZ poly?).

a_i - a_j - a_k + a_l = 0  <=>  a_i + a_l = a_j + a_k.

Trivial (always-present) zeros: i=j & k=l ; i=k & j=l ; i=l & j=k (the last gives
a_i+a_j = a_j+a_i trivially? check). These come from the additive structure and
exist for EVERY polynomial -> they are the y^Z factor we remove. They do NOT
threaten validity (we just drop them; the constraint is on the reduced product).

Nontrivial zeros: a_i+a_l = a_j+a_k with the index pattern NOT one of the trivial
ones -- happens only for special fields (e.g. when sums of conjugates coincide).
These are extra zero factors but as long as at least ONE factor is nonzero the
reduced product is a nonzero integer. The constraint J(nu) >= 0 holds as long as
|reduced product| >= 1, i.e. nonzero integer. Verify the reduced product is never
forced to 0 by ALL factors vanishing (that would need every a_i+a_l=a_j+a_k, i.e.
all conjugate-sums equal => P has a very degenerate form).
"""
import sympy as sp
from itertools import product

x = sp.symbols('x')


def analyze(P, tol=1e-9):
    roots = [complex(r) for r in sp.Poly(P, x).nroots(n=50)]
    d = len(roots)
    trivial = 0
    nontrivial = 0
    nonzero = 0
    for i, j, k, l in product(range(d), repeat=4):
        v = roots[i] - roots[j] - roots[k] + roots[l]
        if abs(v) < tol:
            # trivial index patterns: (i=j,k=l), (i=k,j=l), (i=l,j=k)
            triv = (i == j and k == l) or (i == k and j == l) or (i == l and j == k)
            if triv:
                trivial += 1
            else:
                nontrivial += 1
        else:
            nonzero += 1
    return d, trivial, nontrivial, nonzero


print("=" * 78)
print("Zero structure of Q = x1-x2-x3+x4  (a_i+a_l = a_j+a_k)")
print("=" * 78)
print(f"{'poly':<34}{'d':>3}{'trivial-0':>11}{'nontriv-0':>11}{'nonzero':>9}")
tests = {
    'x^2-x-1': x**2 - x - 1,
    'z^2-z+1 (symmetric)': x**2 - x + 1,
    'x^3-x-1': x**3 - x - 1,
    'x^4-x-1': x**4 - x - 1,
    'x^4-10x^2+1 (Q(sqrt2,sqrt3))': x**4 - 10*x**2 + 1,
    'x^4-5x^2+5 (cyclotomic-ish)': x**4 - 5*x**2 + 5,
    'x^2-x (excluded)': x**2 - x,
}
for name, P in tests.items():
    d, tr, nt, nz = analyze(P)
    print(f"{name:<34}{d:>3}{tr:>11}{nt:>11}{nz:>9}")

print()
print("Trivial-zero count formula check: for d roots, #(i=j,k=l)=d^2, #(i=k,j=l)=d^2,")
print("#(i=l,j=k)=d^2, minus overlaps. Overlaps where two patterns coincide:")
print("  all three coincide when i=j=k=l: d tuples (counted 3x).")
print("  Inclusion-exclusion expected trivial-zero count:")
for d in (2, 3, 4):
    # |A|+|B|+|C| - pairwise + triple
    A = d*d  # i=j,k=l
    B = d*d  # i=k,j=l
    C = d*d  # i=l,j=k
    # A&B: i=j,k=l,i=k,j=l => i=j=k=l? i=j,i=k =>i=j=k; k=l =>all eq: d
    AB = d
    AC = d
    BC = d
    ABC = d
    total = A+B+C - AB-AC-BC + ABC
    print(f"  d={d}: predicted trivial zeros = {total}")
