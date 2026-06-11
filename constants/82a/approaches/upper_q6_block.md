# 82a UPPER — second free-exponent perturbing block (Flammang Q6 = j15, deg 16)

Status: BUILT (R11), AWAITING REVIEW. Adds Q6=j15 on top of the held R10 Q5=j13.

## R11 BUILD RESULT (h = Q1*Q2 * Q5^qE * Q6^qF, Qa,Qb dropped i.e. qB=qC=0)
Builder claim (UNVERIFIED until reviewer signs off — do NOT write to `held`):
  CERTIFIED  log h <= **0.2540419719**  (vs held R10 0.2540639638; margin **2.199e-5**).
  q = (13.937341, 12.515102, 2.541409, 2.068537, 0.753965), qB=qC=0,
  qE = 0.891271 (Q5=j13), qF = 0.246614 (Q6=j15, NEW).
  D = max(sum q_i deg P_i = 59.198095, 56 + 0.891271*12 + 0.246614*16)
    = max(59.198095, 70.641076) = 70.641076 (perturb branch dominates).
  int_0^2pi G dt <= 112.7567758427; int_0^1 G ds <= 17.9457982425;
  17.9457982425 / 70.641076 = 0.254041971876 (hand-checked).
  Frontier FULLY RESOLVED: 0 unresolved, 669734 leaves, 6 refine rounds, ~326s.
  Reproduce: python3 constants/82a/certificate/verify_upper_q6.py certify \
    13.937341 12.515102 2.541409 2.068537 0.753965 0 0 0.891271 0.246614 200000 14 1e-10

Checks all PASS:
  - anchor 1 (qF=0): float (0.254063825491) + D (66.351056) + per-cell enclosure
    BIT-IDENTICAL (np.array_equal) to verify_upper_q5 at the held R10 (q,qB,qC,qE)
    => Q6 is a genuine free-exponent EXTENSION recovering the R10 held cert.
  - anchor 2 (qE=qF=0): recovers verify_upper_q4 held R9 ell=2 float
    (0.254265682393), D collapses to 64.4696.
  - anchor 3 (qB=qC=qE=qF=0): recovers Doche base h=Q1*Q2 to >=10 digits
    (0.254330800634), D collapses to 56.
  - admiss: deg Q6=16>0, Q6(0)=Q6(1)=1, squarefree (in fact irreducible);
    X & 1-X !| W=Q1*Q2*Q5*Q6 (deg 84); gcd(Q6, each of P1,P2,P4,P6,P8,Q1,Q2)=1;
    LOAD-BEARING inter-block gcd(Q6,Q5)=1 (True); full ell=4 grid also passes incl.
    gcd(Q6,Qa)=gcd(Q6,Qb)=1.
  - selftest_q6 (mpmath prec=160): 0/200 violations on the CHANGED integrand (B now
    has qF*log|Q6|), both caps; worst (cell_hi - true_int) = +2.619e-12 (flat) /
    +1.382e-17 (midpt), >=0 safe side.
  - tamper (bogus target 0.25404 below truth): BEATS=False, frontier resolved (the
    certified 0.2540419719 sits above 0.25404). No grid fallback faking a proof.
  - float conjecture 0.2540418523 sits just below the cert 0.2540419719 (correct
    outward direction; cert slack ~1.2e-7 as in prior rounds).

Q6 coeffs (Flammang Table 1 entry j=15, deg 16 in X=z(1-z), descending high->low):
  [1, -4, 10, -17, 26, -47, 119, -298, 592, -878, 963, -780, 464, -199, 59, -11, 1]
Ascending: [1,-11,59,-199,464,-780,963,-878,592,-298,119,-47,26,-17,10,-4,1].

## What would push it further
After j=15 the upper deg-12..16 well is nearly captured; among the 18 admissible
Flammang blocks only j=15 cleared the cert slack (runner-up j=19 gives only ~1.8e-6).
The next real gains are NOT more blocks of this family. Two roads:
  - a genuinely new small-Mahler-measure deg~12-20 block (LLL / lattice-reduction
    construction of an integer poly in X=z(1-z) with small sup on the contour), not
    from Flammang's lower-bound table;
  - PATH B (lower bound, the never-moved frontier): OSS log-energy / discriminant
    dual column (arXiv:2401.03252) added to Flammang's auxiliary-function LP. MULTI-
    STAGE; see spec_82a_j15.md PATH B note and lp-column-generation.md. Do NOT hand
    to one atomic builder.
