"""
ROUTE 3 VALIDITY (EXACT, rigorous): prove the 4-point product is an INTEGER
and characterize its zero structure via exact symmetric-function / resultant
computation, not numerics.

Define the symmetric quantity over the d roots a_1..a_d of monic P in Z[x]:
    PROD'  =  PROD_{(i,j,k,l) : factor != 0}  (a_i - a_j - a_k + a_l)

Approach: build R(y) = PROD_{i,j,k,l} (y - (a_i-a_j-a_k+a_l)), a polynomial in y
with INTEGER coefficients (symmetric in roots -> Z), via a resultant tower.
Then the full product PROD_{all tuples}(a_i-a_j-a_k+a_l) = (-1)^{d^4} R(0).
That is exactly 0 because of the diagonal tuples. So we factor out the y-power:
R(y) = y^{Z} * Rred(y), and the NONZERO product is (-1)^{deg} Rred(0), an integer.
"""
import sympy as sp

x, y, u, v, s = sp.symbols('x y u v s')


def four_point_R(P):
    """Return R(y) = prod over all 4-tuples (y - (a_i - a_j - a_k + a_l)) with
    integer coeffs, by composing resultants. a_i roots of P(x).
    Strategy: let D1 = a_i - a_j ranges over differences (resultant gives
    A(u)=prod_{i,j}(u-(a_i-a_j))); D2 = a_k - a_l same poly A(v) with
    a_k-a_l => but we need a_i-a_j-a_k+a_l = (a_i-a_j)-(a_l-a_k) ... careful with signs.
    x1-x2-x3+x4 = (a_i - a_j) + (a_l - a_k). Both (a_i-a_j) and (a_l-a_k) range over
    the SAME difference set roots of A. So R(y)=prod over pairs (p,q) of roots of A
    of (y-(p+q)) = Res_p( A(p), Res_q(A(q), y-p-q) )."""
    Pp = sp.Poly(P, x)
    # A(u) = prod_{i,j} (u-(a_i-a_j)) = Res_x( P(x), <poly in (x'=x-u)> )
    # standard: Res_x(P(x), P(x+u)) wrt x gives prod_{i,j}(... )? Let's build directly:
    # differences poly: A(u) = Res_x(P(x), Q(x)) where roots are a_i-a_j.
    # Res_x(P(x), P(x+u)) = prod_{i,j}( (a_i) - (a_j - u) )? Use sympy resultant.
    Px = sp.Poly(P, x)
    Pxu = sp.Poly(P.subs(x, x + u), x)
    A_u = sp.resultant(Px, Pxu, x)            # poly in u, roots a_i - a_j
    A_u = sp.Poly(sp.expand(A_u), u)
    # Now R(y) = prod over (p,q) roots of A of (y-(p+q)).
    # = Res_p( A(p), B(p) ) where B has roots q with y-p-q=0 => q=y-p.
    # prod_q (y-p-q) over roots q of A = A_eval at? Actually prod_q ((y-p)-q) = A(y-p)
    # up to leading coeff. Since A monic-ish: prod_q (s - q) = A(s)/lc(A).
    Au_poly = A_u
    lc = Au_poly.LC()
    # R(y) = prod_p [ A(y-p)/lc ]  over roots p of A
    #      = (1/lc^{deg A}) * Res_p( A(p), A(y-p) )   [as poly in p]
    Ap = sp.Poly(A_u.as_expr(), u)                       # A(p), variable u=p
    A_ymp = sp.Poly(sp.expand(A_u.as_expr().subs(u, y - u)), u)  # A(y-p), var u=p
    Rres = sp.resultant(Ap, A_ymp, u)                    # poly in y
    Ry = sp.expand(Rres / lc**A_u.degree())
    return sp.Poly(sp.nsimplify(Ry), y), A_u


for name, P in [('x^2-x-1', x**2 - x - 1),
                ('z^2-z+1 (symmetric)', x**2 - x + 1),
                ('x^3-x-1', x**3 - x - 1)]:
    Ry, Au = four_point_R(P)
    d = sp.Poly(P, x).degree()
    # factor out y^Z
    Z = Ry.as_poly(y).all_coeffs()
    coeffs = Ry.all_coeffs()
    # multiplicity of y=0 root:
    rev = list(reversed(coeffs))
    z_mult = 0
    while z_mult < len(rev) and rev[z_mult] == 0:
        z_mult += 1
    Rred = sp.Poly(rev[z_mult:][::-1], y) if z_mult < len(rev) else None
    nonzero_prod = (-1)**Rred.degree() * Rred.all_coeffs()[-1] if Rred else None
    print(f"\n{name}: d={d}")
    print(f"  deg R(y) = {Ry.degree()} (= d^4 = {d**4})")
    print(f"  y=0 multiplicity (count of zero factors) = {z_mult}")
    print(f"  nonzero product (-1)^deg * Rred(0) = {nonzero_prod}")
    print(f"  is integer: {nonzero_prod.is_integer}")
    if nonzero_prod != 0:
        J = float(sp.log(abs(nonzero_prod)) / d**4)
        print(f"  J(nu) = {J:+.6f}")
