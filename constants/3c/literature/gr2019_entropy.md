# Digest: Green & Ruzsa, "On the arithmetic Kakeya conjecture of Katz and Tao" (arXiv:1712.02108, Period. Math. Hungar. 2019) [GR2019]

## What it provides
The paper establishes the **equivalence of five formulations** of the arithmetic Kakeya /
sum-difference conjecture, including the **Shannon-entropy formulation** used to attain all
known lower bounds on C_3b, C_3c. It is the reference that legitimizes converting an
entropy ratio of finite (X,Y) into a genuine SD-exponent lower bound.

Entropy form (general slope set {r_j}): the constant is the smallest C such that
  H(X-Y) <= C * sup_j H(X + r_j Y)   for all finite-range X,Y.
For C_3c the slopes are r ∈ {0,1,2,∞}, i.e. the denominators are H(X), H(Y), H(X+Y),
H(X+2Y) (slope ∞ corresponds to projecting onto Y).

## What it does NOT provide
- No explicit extremal constructions and no numerical lower bounds for C_3c — it is a
  reformulation/equivalence paper. ("We neither discuss nor make progress on partial
  results towards any of Conjectures 1-5.") Best known ε for the related conjecture there
  is governed by α^3 - 4α + 2 = 0, ε ≈ 0.67513 — NOT the 3c value.

## Why it matters for the attack
- It is the rigor anchor: it guarantees that maximizing the finite entropy ratio α(P)
  over finite supports converges to C_3c, so any feasible P with α(P) > 1.67473389 is a
  valid record-beating lower bound.
- The upper bound side C_3c <= 1.75 = 2 - 1/4 comes from Katz-Tao [KT1999] (a structural
  sum-difference inequality), not from entropy; it is a clean theoretical value, not a
  numerical optimization target. The softer (attackable, numerical) side is the LOWER bound.
