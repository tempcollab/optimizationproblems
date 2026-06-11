# Digest: Flammang [F18] "On the Zhang-Zagier measure" (Int. J. Number Theory 14 (2018), 2663-2671)

Source PDF: constants/82a/literature/pdfs/flammang_zz_hal.pdf (HAL hal-03295880v1). Extracted text /tmp/flam.txt.

## What it achieves (the RECORD lower bound)
Theorem 1: For any algebraic integer alpha NOT a root of (z^2-z)(z^2-z+1)*phi_10(z)*phi_10(1-z),
  zeta(alpha) >= 1.282416,
where zeta(alpha) = Z(alpha)^{1/deg} is the *absolute* Zhang-Zagier measure, Z(alpha)=M(alpha)M(1-alpha).
Since h_Z(alpha) = log zeta(alpha), this is the lower bound
  C_82 >= log(1.282416) = 0.2487458...  ==> rounded to 0.24874 in the registry. CONFIRMED.

(Doche's previous best was zeta >= 1.281777, log = 0.2482474 = 0.24824. Flammang improves it slightly.)

## The method (Smyth-style explicit auxiliary function + integer transfinite diameter)
Auxiliary function (eq 2.1), with w = z(1-z):
  f(z) = log max(1,|z|) + log max(1,|1-z|) - sum_{j=1..J} c_j * log|Q_j(z(1-z))|
where c_j > 0 are reals and Q_j in Z[w] (nonzero integer polynomials in w).

Key chain (the rigor):
1. Sum over conjugates: sum_i f(alpha_i) >= m*d  where m = min over the relevant domain of f.
2. This gives  log M(alpha)M(1-alpha) >= m*d + sum_j c_j * log| prod_i Q_j(alpha_i(1-alpha_i)) |.
3. The product prod_i Q_j(alpha_i(1-alpha_i)) = Res(P(z), Q_j(z(1-z))) is a NONZERO INTEGER
   (determinant of an integer matrix), provided P does not divide Q_j(z(1-z)).
   Hence log| ... | >= 0, so the c_j terms are >= 0 and drop out.
4. Therefore  (1/d) log Z(alpha) = log zeta(alpha) >= m.  So C_82 >= m.

The minimum m: since f is harmonic away from small disks around roots of the Q_j, the min of f
is attained on |z|=1 or |1-z|=1; by the z->1-z symmetry it suffices to minimize on C={|z|=1},
i.e. on v = e^{it} - e^{2it}, 0<=t<=pi. m = inf_{0<=t<=pi} f.

## How the polynomials/coefficients are found (NOT part of the rigor, just the search)
- Given a current set {Q_1,...,Q_J}, SEMI-INFINITE LINEAR PROGRAMMING (Smyth's LP) optimizes the
  c_j to maximize m (the constraint f(z) >= m on the domain becomes infinitely many linear
  constraints in the c_j; discretized at control points).
- To ENLARGE the polynomial set: link to the weighted integer transfinite diameter
  t_{Z,phi}(C) with weight phi = (max(1,|z|)max(1,|1-z|))^{-1}. For several k, search a new
  integer polynomial R(z)=sum a_l z^l of degree k minimizing sup_t |Q(v)R(v)| exp(-(r+k)/(2t)*...).
  Since R(v) is complex, split into Re/Im and apply LLL to those linear forms. Control points
  v_n = e^{it_n}-e^{2it_n} chosen near the least local minima of f.
- Keep factors R_j of R that get nonzero c_j after re-optimization; drop Q_j that drop to c_j=0.
- "We take k from 5 to 32 successively" to reach the Theorem 1 constant.

## The certificate (what a reviewer reproduces)
Table 1 of the paper lists ~24 polynomials Q_j (in w) with explicit FLOATING-POINT coefficients c_j
(12 decimal digits). First few:
  c_1 = 0.233410801570, Q_1 = w
  c_2 = 0.181822930849, Q_2 = w - 1
  c_3 = 0.001206393184, Q_3 = w^3 + w^2 - 2w + 1
  ... up to degree-22 polynomials in w.
(Full list at /tmp/flam.txt lines ~584-610; high-degree ones span many lines.)

To VERIFY the bound 0.24874 one must:
 (a) confirm each Q_j in Z[w] (integer coeffs) -- yes by inspection;
 (b) compute m = min_{0<=t<=pi} [ log max(1,|w|) - sum_j c_j log|Q_j(w)| ], w = e^{it}-e^{2it},
     and check m >= log(1.282416) = 0.248746.  This is a 1-D minimization; rigorous version needs
     an interval/branch-and-bound certificate that the min over t is >= the claimed value.
 (c) The integrality (resultant >=1) step is an exact algebra fact, not numeric.

## Slack / how to push it
- The c_j are floats from an LP at a FIXED polynomial set; re-running the LP at higher precision
  changes m only in the last digits.
- Real slack = a BETTER / LARGER set of polynomials Q_j (the search space is "enormous", per BMQS).
  Flammang stopped at k<=32; Doche's spectrum point at 1.287527 (=> 0.252723) is conjecturally the
  true next value, so there is room between 0.248746 (proved) and ~0.2527 (conjectured) on the
  lower side IF a better auxiliary function can be found.
- The improvement Doche->Flammang was only 0.24824 -> 0.24874 (5e-4) after a big search; gains are
  small and search-driven.
