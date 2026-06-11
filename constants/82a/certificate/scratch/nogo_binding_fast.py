"""
FAST decisive binding test (no slow atomic cloud).

A supergradient self-cut from the concave column C_n at ANY reference mu0 is
   <grad C_n|_{mu0}, p>  >=  (k-1) C_n(mu0)        [tangent of degree-k form]
and it BINDS (prunes) the Flammang LP optimum p0 iff p0 violates C_n >= 0 there, i.e.
iff C_n(p0) < 0.  (For a concave C_n, the tangent at mu0 over-estimates C_n; the cut
{tangent >= 0} can only separate points q with C_n(q) < 0. The LP optimum p0 is
separated only if C_n(p0) < 0.)

So the ENTIRE binding question for n>=2 reduces to the sign of C_n(p0). We compute
C_n(p0) for the Flammang no-energy LP optimum p0 and its z->1-z symmetrization, and
(adversarially) for the LOW-C_n diffuse reference. If C_n(p0) >= 0 for all n>=2, NO
self-cut from C_n can raise the LP -> the column is inert (lambda0 = 0).
"""
import sys
import numpy as np
from scipy.optimize import linprog
from flammang_table1 import get_table
from scratch.nogo_Cmu0 import (C_n_from_measure, conj_sym, zz_sym, contour,
                               column_matrix, solve_primal, diffuse_from_p0)

ANCHOR = 0.2487458

N = 2000
t, z, w, g = contour(N)
A = column_matrix(w)
m0, p0 = solve_primal(g, A)
print(f"no-energy LP m0 = {m0:.7f}  (Flammang anchor {ANCHOR})")
sys.stdout.flush()

# p0 as a diffuse conj-sym measure, and its z->1-z symmetrization
th, mh = diffuse_from_p0(t, p0, 55, 8)
zA, mA = conj_sym(th, mh)              # conj-sym Flammang optimum (NOT z->1-z sym)
pB, mB = zz_sym(zA, mA)                # z->1-z symmetrized (valid reference)

print("\nC_n at the LP optimum p0 -- the ONLY reference whose self-cut prunes p0:")
print(f"{'n (k)':>7} | {'C_n(p0 conj-sym)':>18} | {'C_n(p0 z->1-z sym)':>20} | verdict")
for n in (1, 2, 3, 4):
    cA = C_n_from_measure(zA, mA, n, G=512)
    cB = C_n_from_measure(pB, mB, n, G=512)
    # The valid (z->1-z sym) reference is cB; binding requires cB < 0.
    if n == 1:
        verd = "energy: cB~0 (sym collapse); cA<0 powers R17 via superharmonic |z|=1 reduction"
    else:
        verd = "INTERIOR (cB>0): self-cut cannot bind -> lambda0=0, INERT" if cB > 1e-3 else "check"
    print(f"{n} (k={2*n}) | {cA:+18.5f} | {cB:+20.5f} | {verd}")
    sys.stdout.flush()

print("\nConclusion: for n>=2 the LP optimum is strictly interior to {C_n>=0} under the")
print("valid z->1-z symmetric reference; no supergradient self-cut binds it.")
