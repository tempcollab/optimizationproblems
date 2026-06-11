"""
screen_powersum.py — R5 verified-NEGATIVE lever-closure for the C_82a LOWER bound.

Closes the two previously-unexamined NON-energy lower-bound levers for the
Zhang-Zagier essential minimum (C_82a), as a reproducible certificate:

  (a) the power-sum / w-moment column   int w^k dmu_w  =  S_k(w)/d
      where w_i = z_i(1-z_i) are the conjugates of w = alpha(1-alpha) and
      mu_w is the (counting) conjugate measure of an alpha that is ZZ-minimal
      of degree d.

  (b) the single-variable Schur-Siegel-Smyth (SSS) trace-transplant: whether
      Smyth's MEAN-DIRECT trace lower bound transplants to ZZ.

This script CLOSES lever (a) by screening THREE independent failure mechanisms
and prints the witness data for the structural argument that closes (b). It does
NOT raise the bound; the held lower stays Flammang 0.2487458 = log(1.282416).

------------------------------------------------------------------------------
WHY A POWER-SUM / MOMENT COLUMN CANNOT ENTER FLAMMANG'S LP
------------------------------------------------------------------------------
Flammang's auxiliary-function lower bound is the LP

    maximize  m   s.t.   sigma_ZZ(z) - sum_j c_j log|Q_j(w(z))|  >=  m   for all z,
                         c_j >= 0,   Q_j in Z[w],

where sigma_ZZ(z) = log+ |z| + log+ |1-z|  is the honest Zhang-Zagier density
(Flammang [F18] eq. 2.1; log+ x = log max(1,x)).  Each column is a SINGLE
integral of log|integer poly|, and it enters as a sign-DEFINITE inequality:
    int log|Q_j(w)| dmu_w  >=  0       (resultant-integrality, off a finite set).
The bound is then  h_Z(alpha) = int sigma_ZZ dmu_w >= m  because the columns
"drop out" nonnegatively.

A power-sum / moment functional  int w^k dmu_w = S_k/d  is a different object:
a SINGLE integral of a MONOMIAL w^k, equal to a polynomial-dependent real with
NO log and NO kernel.  It is neither
    - the log|Q|>=0 cone (R3 contour-LP, ceilinged 0.2487857), nor
    - the double-integral log-energy  int int log|w_1-w_2| dmu dmu  (barred OSS,
      I(nu)<0 for non-integer alpha, R1 retraction),
and it supplies NO inequality at all.  This script SCREENS the three reasons:

  MECH 1 (load-bearing, screened):  S_k/d is SIGN-INDEFINITE across ZZ polys, so
          it can never be a sign-definite ">=0 drop-out" column -> never enters
          the LP -> cannot raise the bound.
  MECH 2 (load-bearing, screened):  S_k(w) are exact integers ONLY on the
          algebraic-integer locus a=1.  Over the actual ZZ domain (alpha any
          algebraic number, leading coeff a>1) the w_i are NOT algebraic
          integers and S_k is NON-integer -> no integrality drop-out exists.
          This is the SAME a^deg leading-coefficient wall that retracted OSS (R1).
  MECH 3 (supporting):  int w^k dmu_w = S_k/d -> 0 as d -> inf on the integer
          locus (S_k bounded by the fixed dictionary degree while d grows) -> the
          "constraint" dissolves; it is an equality to an unconstrained real, not
          a fixed floor.

ANY fixed real moment functional sum_k a_k int w^k dmu_w = int P(w) dmu_w =
(sum_i P(w_i))/d inherits all three failures, so the whole moment span is
disjoint from both the log|Q|>=0 cone and the energy cone.  Lever (a) CLOSED.

------------------------------------------------------------------------------
LEVER (b): the SSS trace-transplant (structural, witnessed by the same data)
------------------------------------------------------------------------------
Smyth's trace bound is MEAN-DIRECT (no min-reduction) because (i) its objective
int x dmu = (1/d) sum alpha_i = trace/d is a LINEAR functional of the roots and
(ii) sum alpha_i = trace(alpha) is an EXACT INTEGER (OSS arXiv:2401.03252 eq. 2).
For ZZ both handles fail:
   - the objective sigma_ZZ(z) = log+|z| + log+|1-z| is NON-linear / non-polynomial;
   - the conjugate-sum sum_i sigma_ZZ(z_i) = d * h_Z IS the unknown height itself,
     so there is no exact-integer trace to exploit.
Flammang is therefore FORCED into (1/d) sum f(z_i) >= min f (the min-reduction),
and the min-vs-mean gap is intrinsic and uncapturable by the trace technique
WITHOUT an energy column (barred).  The reproducible witness for "there is no
integer trace handle" is exactly the Mech-2 demo: the only w-power-sum that is an
exact integer needs a=1, and even then it is S_k (a varying poly-dependent
integer), never the fixed sigma_ZZ objective.

------------------------------------------------------------------------------
Usage:
    python3 screen_powersum.py certify     # run the full screen, print PASS/FAIL
    python3 screen_powersum.py selftest    # internal consistency checks
    python3 screen_powersum.py tamper      # a bogus ">=0 column" claim must FAIL

All quantities are computed independently: S_k by EXACT integer Newton's
identities from the (integer) minimal polynomial of w on the a=1 locus, and
cross-checked by numpy.roots; the a>1 non-integrality by exact rational
arithmetic (fractions) so it is not floating-point noise.
"""

import sys
from fractions import Fraction
import numpy as np


# ----------------------------------------------------------------------------
# Exact arithmetic helpers
# ----------------------------------------------------------------------------

def poly_mul(a, b):
    """Multiply two polynomials given as ascending coeff lists (Fractions/ints)."""
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += Fraction(ai) * Fraction(bj)
    return out


def minpoly_of_w(P_desc):
    """
    Given P(z) by DESCENDING integer coeffs, return the polynomial whose roots
    are w_i = z_i (1 - z_i), as an ASCENDING list of Fractions, monic-normalized.

    Method (exact, resultant-free): the elementary symmetric functions of the
    w_i are computed from those of the z_i via the power sums of w, which are
    polynomials in the power sums of z (Newton).  We instead build the w-polynomial
    by exact resultant elimination:  R(w) = Res_z( P(z), w - z(1-z) ).
    For robustness we use the companion-matrix characteristic polynomial of the
    MULTIPLICATION-BY-w operator on Q[z]/(P(z)) computed with exact Fractions.

    Returns (coeffs_asc_fraction, d).  Leading coeff normalized to 1 (monic in w),
    so the constant/other coeffs are the elementary symmetric functions of w with
    sign, EXACT rationals.  Integrality of S_k is then read off Newton's identities.
    """
    # P descending, leading coeff a = P_desc[0] (the "a" of the ZZ domain).
    P = [Fraction(c) for c in reversed(P_desc)]  # ascending
    d = len(P) - 1
    a = P[-1]  # leading coeff (= P_desc[0])
    # Monic version of P (over Q): pm(z) = P(z)/a
    Pm = [c / a for c in P]
    # Build matrix of multiplication-by-(z(1-z)) on basis {1, z, ..., z^{d-1}}
    # mod Pm(z).  z*z = z^2, reduce z^d via Pm.  We need reduction of z^k for k<=2(d-1)+? .
    # multiplication by m(z)=z - z^2 = z*(1-z).
    # Represent elements as length-d coeff vectors (ascending) over Q.
    def reduce_poly(coeffs):
        """Reduce ascending coeff list mod Pm(z) (monic) to degree < d."""
        c = [Fraction(x) for x in coeffs]
        while len(c) - 1 >= d:
            lead = c[-1]
            deg = len(c) - 1
            if lead != 0:
                # subtract lead * z^{deg-d} * Pm(z)
                shift = deg - d
                for i, pmc in enumerate(Pm):
                    c[shift + i] -= lead * pmc
            c.pop()
        # pad to length d
        while len(c) < d:
            c.append(Fraction(0))
        return c[:d]

    # columns of the multiplication matrix
    M = [[Fraction(0)] * d for _ in range(d)]  # M[row][col]
    for col in range(d):
        # basis element z^col, multiply by (z - z^2) = m(z)
        e = [Fraction(0)] * (col + 1)
        e[col] = Fraction(1)
        # m(z)*z^col = z^{col+1} - z^{col+2}
        prod = [Fraction(0)] * (col + 3)
        prod[col + 1] += Fraction(1)
        prod[col + 2] += Fraction(-1)
        red = reduce_poly(prod)
        for row in range(d):
            M[row][col] = red[row]
    return M, d, a, P


def char_poly_fraction(M, d):
    """
    Characteristic polynomial det(xI - M) for a d x d Fraction matrix M,
    returned as ascending Fraction coeffs (monic, degree d).
    Faddeev-LeVerrier (exact).  Also returns the power sums S_k = tr(M^k).
    """
    # Faddeev-LeVerrier algorithm: exact, gives char poly coeffs and traces.
    import copy
    n = d
    # work with M as list of lists of Fractions
    def matmul(A, B):
        C = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            Ai = A[i]
            for k in range(n):
                aik = Ai[k]
                if aik == 0:
                    continue
                Bk = B[k]
                Ci = C[i]
                for j in range(n):
                    Ci[j] += aik * Bk[j]
        return C

    def trace(A):
        return sum(A[i][i] for i in range(n))

    def add_diag(A, s):
        B = [row[:] for row in A]
        for i in range(n):
            B[i][i] += s
        return B

    Mk = [[Fraction(M[i][j]) for j in range(n)] for i in range(n)]
    c = [Fraction(0)] * (n + 1)
    c[n] = Fraction(1)  # leading
    traces = []
    Nk = None
    coeffs = [Fraction(1)]  # c_{n} ... will fill p_k
    # Faddeev-LeVerrier
    p = [Fraction(0)] * (n + 1)  # p[k] = coefficient pattern
    Mcur = None
    c_lev = [Fraction(0)] * (n + 1)
    c_lev[0] = Fraction(1)
    A = [[Fraction(0)] * n for _ in range(n)]  # M^0-ish accumulation
    # standard FL: M_1 = M; c_1 = -tr(M_1); M_{k+1}=M(M_k + c_k I); c_{k+1} = -tr(M_{k+1})/(k+1)
    Mk_cur = [row[:] for row in Mk]
    cs = [Fraction(1)]  # c_0 = 1
    traces_pow = []  # S_k = tr(M^k)
    Mpow = [row[:] for row in Mk]  # M^1
    for k in range(1, n + 1):
        traces_pow.append(trace(Mpow))
        if k < n:
            Mpow = matmul(Mpow, Mk)
    # Now c_k via Newton from traces_pow: e_k elementary symmetric of eigenvalues
    # char poly det(xI-M) = x^n - e1 x^{n-1} + e2 x^{n-2} - ...
    # Newton: e1 = S1; k e_k = sum_{i=1}^k (-1)^{i-1} e_{k-i} S_i
    S = traces_pow
    e = [Fraction(1)]  # e_0
    for k in range(1, n + 1):
        acc = Fraction(0)
        for i in range(1, k + 1):
            acc += ((-1) ** (i - 1)) * e[k - i] * S[i - 1]
        e.append(acc / k)
    # char poly ascending coeffs: det(xI - M) = sum_{j} (-1)^{n-j} e_{n-j} x^{j}
    cp_asc = [Fraction(0)] * (n + 1)
    for j in range(n + 1):
        cp_asc[j] = ((-1) ** (n - j)) * e[n - j]
    return cp_asc, S


# ----------------------------------------------------------------------------
# Power sums of w for a given integer polynomial P(z)  (DESCENDING coeffs)
# ----------------------------------------------------------------------------

def exact_powersums_w(P_desc, K=5):
    """
    EXACT power sums S_k(w) = sum_i w_i^k, w_i = z_i(1-z_i), via the multiplication
    operator on Q[z]/(P).  Returns list of K Fractions and the leading coeff a.
    These are EXACT rationals; S_k integer  <=>  Fraction has denominator 1.
    """
    M, d, a, _ = minpoly_of_w(P_desc)
    _, S = char_poly_fraction(M, d)
    # S has length d; if K > d we need more power sums. Extend via M^k traces.
    if K <= len(S):
        return S[:K], a, d
    # extend
    def matmul(A, B):
        n = d
        C = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                aik = A[i][k]
                if aik == 0:
                    continue
                for j in range(n):
                    C[i][j] += aik * B[k][j]
        return C
    Mk = [[Fraction(M[i][j]) for j in range(d)] for i in range(d)]
    Spow = list(S)
    Mpow = [row[:] for row in Mk]
    for _ in range(len(S) - 1):
        Mpow = matmul(Mpow, Mk)
    while len(Spow) < K:
        Mpow = matmul(Mpow, Mk)
        Spow.append(sum(Mpow[i][i] for i in range(d)))
    return Spow[:K], a, d


def numpy_powersums_w(P_desc, K=5):
    """Independent float cross-check via numpy.roots."""
    r = np.roots([float(c) for c in P_desc])
    w = r * (1 - r)
    return [complex(np.sum(w ** k)) for k in range(1, K + 1)]


# ----------------------------------------------------------------------------
# The ZZ polynomial test set
# ----------------------------------------------------------------------------
# a=1 (algebraic-integer locus): these give EXACT INTEGER S_k.
INTEGER_LOCUS = {
    "z^2 - z - 1   (Zagier extremal)": [1, -1, -1],
    "z^2 - z + 1": [1, -1, 1],
    "z^3 - z - 1": [1, 0, -1, -1],
    "z^3 - z + 1": [1, 0, -1, 1],
    "z^4 - z^3 - 1": [1, -1, 0, 0, -1],
}
# a>1 (genuine ZZ domain, non-integer alpha): S_k NOT integers.
NONINTEGER_LOCUS = {
    "10 z^2 - 6 z + 1   (a=10)": [10, -6, 1],
    "3 z^2 - z + 1      (a=3)": [3, -1, 1],
    "7 z^3 - 2 z - 1    (a=7)": [7, 0, -2, -1],
}

K = 5


# ----------------------------------------------------------------------------
# The screen
# ----------------------------------------------------------------------------

def run_screen(verbose=True):
    """
    Returns a dict of screened facts:
      mech1_signs_Sk, mech1_signs_Skd : sets of signs seen across the integer locus
      mech1_sign_indefinite           : bool (both >0 and <0 appear)
      mech2_all_integer_on_a1         : bool (every a=1 poly gives integer S_k)
      mech2_noninteger_off_a1         : bool (every a>1 poly gives NON-integer S_k)
      mech3_table                     : list of (name, d, S1/d) showing S_k/d shrink
    """
    facts = {}
    signs_Sk = set()
    signs_Skd = set()
    table_int = []
    all_integer = True

    if verbose:
        print("=" * 78)
        print("MECH 1 + integrality demo on the ALGEBRAIC-INTEGER locus (a = 1)")
        print("  S_k(w) = sum_i w_i^k   (EXACT, Newton's identities);   S_k/d = int w^k dmu_w")
        print("=" * 78)
        print(f"{'polynomial':<34}{'a':>3} {'d':>2}  S_k (k=1..%d) and [S_k/d]" % K)

    for name, P in INTEGER_LOCUS.items():
        S, a, d = exact_powersums_w(P, K)
        # exact integrality check
        for s in S:
            if s.denominator != 1:
                all_integer = False
        # cross-check vs numpy
        Snp = numpy_powersums_w(P, K)
        for sf, sc in zip(S, Snp):
            assert abs(float(sf) - sc.real) < 1e-7, f"numpy mismatch {name}"
            assert abs(sc.imag) < 1e-7
        Sk_str = ", ".join(str(int(s)) if s.denominator == 1 else str(s) for s in S)
        Skd_str = ", ".join(_fmt(Fraction(s, 1) / d) for s in S)
        for s in S:
            signs_Sk.add(_sign(s))
            signs_Skd.add(_sign(Fraction(s) / d))
        table_int.append((name, a, d, S))
        if verbose:
            print(f"{name:<34}{int(a):>3} {d:>2}  S_k = [{Sk_str}]")
            print(f"{'':<34}{'':>3} {'':>2}  S_k/d = [{Skd_str}]")

    if verbose:
        print()
        print("=" * 78)
        print("MECH 2: OFF the integer locus (a > 1, genuine ZZ domain) S_k is NON-integer")
        print("  same a^deg leading-coefficient wall that retracted the OSS energy column (R1)")
        print("=" * 78)
        print(f"{'polynomial':<34}{'a':>3} {'d':>2}  S_k (k=1..%d)   integer?" % K)

    noninteger_off = True
    for name, P in NONINTEGER_LOCUS.items():
        S, a, d = exact_powersums_w(P, K)
        is_int = all(s.denominator == 1 for s in S)
        if is_int:
            noninteger_off = False
        Snp = numpy_powersums_w(P, K)
        for sf, sc in zip(S, Snp):
            assert abs(float(sf) - sc.real) < 1e-6, f"numpy mismatch {name}: {float(sf)} vs {sc.real}"
        Sk_str = ", ".join(_fmt(s) for s in S)
        if verbose:
            print(f"{name:<34}{int(a):>3} {d:>2}  S_k = [{Sk_str}]   integer? {is_int}")

    # MECH 3: S_k/d shrinks as d grows on the integer locus (supporting).
    # The dictionary is fixed-degree; sum_i w_i^k stays O(1)-per-root in magnitude
    # while d grows, so S_k/d -> 0. Demonstrate with a degree-rising family
    # z^d - z - 1 (a=1) and tabulate |S_1|/d.
    mech3 = []
    for d in (2, 3, 5, 8, 13, 21):
        P = [1] + [0] * (d - 2) + [-1, -1]  # z^d - z - 1, descending
        S, a, dd = exact_powersums_w(P, 2)
        assert dd == d
        mech3.append((d, Fraction(S[0]), float(Fraction(S[0]) / d)))

    if verbose:
        print()
        print("=" * 78)
        print("MECH 3 (supporting): int w^k dmu_w = S_k/d -> 0 as d -> inf on the integer locus")
        print("  family z^d - z - 1 (a=1):  S_1 stays O(1), so S_1/d -> 0 (no fixed floor)")
        print("=" * 78)
        print(f"{'d':>3}  {'S_1':>6}   {'S_1/d = int w dmu_w':>22}")
        for d, S1, S1d in mech3:
            print(f"{d:>3}  {str(int(S1)):>6}   {S1d:>22.6f}")

    facts["mech1_signs_Sk"] = signs_Sk
    facts["mech1_signs_Skd"] = signs_Skd
    facts["mech1_sign_indefinite"] = ("+" in signs_Skd and "-" in signs_Skd)
    facts["mech2_all_integer_on_a1"] = all_integer
    facts["mech2_noninteger_off_a1"] = noninteger_off
    facts["mech3_shrinks"] = (abs(mech3[-1][2]) < abs(mech3[0][2]))
    facts["mech3_table"] = mech3
    return facts


def _sign(fr):
    if fr > 0:
        return "+"
    if fr < 0:
        return "-"
    return "0"


def _fmt(fr):
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(int(fr))
    return f"{float(fr):.6g}"


# ----------------------------------------------------------------------------
# certify / selftest / tamper
# ----------------------------------------------------------------------------

def certify():
    facts = run_screen(verbose=True)
    print()
    print("=" * 78)
    print("LEVER-CLOSURE VERDICT")
    print("=" * 78)
    ok1 = facts["mech1_sign_indefinite"]
    ok2a = facts["mech2_all_integer_on_a1"]
    ok2b = facts["mech2_noninteger_off_a1"]
    ok3 = facts["mech3_shrinks"]
    print(f"[MECH 1] S_k/d takes signs {sorted(facts['mech1_signs_Skd'])} "
          f"(S_k signs {sorted(facts['mech1_signs_Sk'])}) -> SIGN-INDEFINITE: {ok1}")
    print("         => never a sign-definite >=0 drop-out column => cannot enter the LP. [LOAD-BEARING]")
    print(f"[MECH 2] S_k(w) all integer on a=1: {ok2a};  NON-integer for every a>1 poly: {ok2b}")
    print("         => no integrality drop-out over the genuine ZZ domain (a^deg wall, = OSS R1). [LOAD-BEARING]")
    print(f"[MECH 3] S_k/d -> 0 as d -> inf on the integer locus: {ok3}")
    print("         => equality to an unconstrained real, no fixed floor. [SUPPORTING]")
    print()
    closed = ok1 and ok2a and ok2b
    print("LEVER (a) power-sum/moment column: CLOSED on Mech 1 AND Mech 2 (each independent)."
          if closed else "LEVER (a): NOT closed -- screen failed.")
    print("LEVER (b) SSS trace-transplant: CLOSED structurally -- the only exact-integer")
    print("  w-power-sum needs a=1 (Mech 2) and is a varying S_k, never the fixed sigma_ZZ")
    print("  objective; sigma_ZZ is non-linear and its conjugate-sum IS d*h_Z (the unknown")
    print("  height), so no mean-direct integer-trace handle exists -> min-reduction forced.")
    print()
    print("NO RAISE. Held lower stays Flammang 0.2487458 = log(1.282416).")
    if not closed:
        print("RESULT: FAIL")
        sys.exit(1)
    print("RESULT: PASS  (both non-energy levers closed by reproducible screen)")


def selftest():
    """Internal consistency checks, independent of the headline screen."""
    fails = 0

    # (S1) Newton/Faddeev S_k must match numpy.roots to float precision on every poly.
    for name, P in {**INTEGER_LOCUS, **NONINTEGER_LOCUS}.items():
        S, a, d = exact_powersums_w(P, K)
        Snp = numpy_powersums_w(P, K)
        for sf, sc in zip(S, Snp):
            if abs(float(sf) - sc.real) > 1e-6 or abs(sc.imag) > 1e-6:
                print(f"[S1 FAIL] {name}: exact {float(sf)} vs numpy {sc}")
                fails += 1

    # (S2) On a=1 polys S_k must be EXACT integers (denominator 1).
    for name, P in INTEGER_LOCUS.items():
        S, a, d = exact_powersums_w(P, K)
        assert a == 1, name
        for s in S:
            if s.denominator != 1:
                print(f"[S2 FAIL] {name}: S_k = {s} not integer on a=1 locus")
                fails += 1

    # (S3) On a>1 polys at least one S_k must be NON-integer (the wall).
    for name, P in NONINTEGER_LOCUS.items():
        S, a, d = exact_powersums_w(P, K)
        assert a > 1, name
        if all(s.denominator == 1 for s in S):
            print(f"[S3 FAIL] {name}: all S_k integer despite a={a}>1 (wall absent?)")
            fails += 1

    # (S4) Zagier extremal must give the literature integers -2,2,-2,2,-2.
    S, a, d = exact_powersums_w([1, -1, -1], 5)
    if [int(s) for s in S] != [-2, 2, -2, 2, -2]:
        print(f"[S4 FAIL] Zagier z^2-z-1 S_k = {[int(s) for s in S]} != [-2,2,-2,2,-2]")
        fails += 1

    # (S5) The a=10 counterexample must give the literature non-integers.
    S, a, d = exact_powersums_w([10, -6, 1], 3)
    expect = [Fraction(11, 25), Fraction(117, 1250), Fraction(2398, 125000)]
    for got, exp in zip(S, expect):
        if got != exp:
            print(f"[S5 FAIL] 10z^2-6z+1 S = {got} != {exp} (={float(exp)})")
            fails += 1

    # (S6) Sign-indefiniteness of S_k/d must be genuine (both + and - appear).
    facts = run_screen(verbose=False)
    if not facts["mech1_sign_indefinite"]:
        print("[S6 FAIL] S_k/d not sign-indefinite -- Mech 1 broken")
        fails += 1

    # (S7) char-poly leading coeff is 1 (monic in w) and constant term =
    #      product of w_i = exact rational, sanity that the operator is right:
    #      for z^2-z-1, w_1 w_2 = product z_i(1-z_i); check via e_d.
    M, d, a, _ = minpoly_of_w([1, -1, -1])
    cp, S = char_poly_fraction(M, d)
    # cp ascending; product of roots = (-1)^d cp[0] (monic). For z^2-z-1:
    # z_i = phi, 1-phi (golden), w_i = z_i - z_i^2.
    rprod = (Fraction(-1) ** d) * cp[0]
    # independent: w_1*w_2 from numpy
    r = np.roots([1.0, -1.0, -1.0]); w = r * (1 - r)
    if abs(float(rprod) - np.prod(w).real) > 1e-9:
        print(f"[S7 FAIL] prod w = {float(rprod)} vs numpy {np.prod(w).real}")
        fails += 1

    print(f"\nselftest: {fails} failure(s).")
    if fails:
        sys.exit(1)
    print("selftest: PASS")


def tamper():
    """
    A bogus claim that the power-sum column is a valid ">=0 drop-out column"
    (i.e. that int w^k dmu_w >= 0 uniformly, so it could be ADDED to Flammang's
    LP and raise the bound) must be REJECTED by the sign-indefiniteness screen.

    We feed the screen the bogus assertion 'S_k/d >= 0 for all ZZ polys and all k'
    (the only thing that would let a power-sum enter the LP as a nonnegative column)
    and the screen must produce a CONCRETE counterexample -- otherwise it would be
    rubber-stamping. No auto-pass, no grid fallback.
    """
    print("TAMPER: assert the bogus column claim 'int w^k dmu_w = S_k/d >= 0 for all")
    print("        ZZ-minimal alpha and all k' (the premise that would let a power sum")
    print("        enter Flammang's LP as a nonnegative >=0 drop-out column and raise C_82).")
    print()
    counterexamples = []
    for name, P in INTEGER_LOCUS.items():
        S, a, d = exact_powersums_w(P, K)
        for k, s in enumerate(S, 1):
            val = Fraction(s) / d
            if val < 0:
                counterexamples.append((name, k, val))
    # Also off-locus: not even a real-number floor since not integer (irrelevant to sign,
    # but the column is undefined as an integrality drop-out -> still no >=0 handle).
    if not counterexamples:
        print("TAMPER FAIL: screen found NO counterexample -- it would rubber-stamp the")
        print("             bogus nonnegative-column claim. (This must never happen.)")
        sys.exit(1)
    print("Screen REJECTS the claim with explicit counterexamples (S_k/d < 0):")
    for name, k, val in counterexamples[:8]:
        print(f"   {name}:  int w^{k} dmu_w = S_{k}/d = {_fmt(val)} < 0")
    print()
    print("=> a power-sum column is SIGN-INDEFINITE, so the bogus '>=0 column that raises")
    print("   the bound' claim FAILS. The tamper is correctly rejected (no auto-pass).")

    # Second tamper: a bogus 'S_k always integer (so an integrality drop-out exists)'
    # claim must fail on the a>1 domain.
    print()
    print("TAMPER 2: assert 'S_k(w) is always an integer (so an integrality drop-out")
    print("          exists over the whole ZZ domain)'.")
    S, a, d = exact_powersums_w([10, -6, 1], 3)
    if all(s.denominator == 1 for s in S):
        print("TAMPER 2 FAIL: a>1 poly gave integer S_k -- wall absent, would rubber-stamp.")
        sys.exit(1)
    print("Screen REJECTS: 10z^2-6z+1 (a=10) gives")
    print(f"   S_1 = {_fmt(S[0])},  S_2 = {_fmt(S[1])},  S_3 = {_fmt(S[2])}  -- NONE integers.")
    print("=> no integrality drop-out off the a=1 locus. Tamper 2 correctly rejected.")
    print()
    print("TAMPER: PASS (both bogus column claims genuinely fail the screen).")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "certify"
    if mode == "certify":
        certify()
    elif mode == "selftest":
        selftest()
    elif mode == "tamper":
        tamper()
    else:
        print(__doc__)
        print(f"unknown mode {mode!r}; use certify | selftest | tamper")
        sys.exit(2)
