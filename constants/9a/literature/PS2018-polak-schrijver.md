# Digest: Polak & Schrijver, "New lower bound on the Shannon capacity of C7 from circular graphs" (arXiv:1808.07438)

**Result.** Independent set of size **367 in C_7^5** ⇒ Θ(C_7) ≥ 367^(1/5) > 3.2578.
Previous record 350 (Mathew–Östergård 2017, stochastic search). Upper bound is
Lovász ϑ(C_7) < 3.3177 (closed form ϑ(C_n)= n cos(π/n)/(1+cos(π/n))).

**Method (construction, not SDP).**
- Work in circular graph C_{k,n}: vertex set Z_n, adjacency iff cyclic distance < k.
  Homomorphism property: C_{k',n'} → C_{k,n} iff n'/k' ≤ n/k; α and Θ depend only on n/k.
- Prop 2.1: S = { t·(1,7,7²,7³,7⁴) | t ∈ Z_382 } ⊆ Z_382^5 is independent in C_{108,382}^5
  (size 382). Found by computer searching the family {t·(1,q,...,q^{d-1})|t∈Z_n} for
  n≥350, d=5 with n/k(n,d,q) close to 7/2.
- Since 382/108 > 7/2 this doesn't map directly to C_7^5. They ADAPT it: shift by a
  word, divide letters by 54.5 (floor) to land in Z_7, remove conflicting words
  (→ M, size 327), then solve a small max-independent-set ILP (Gurobi) on a 71-vertex,
  85-edge residual graph to add 40 words ⇒ R = 367.

**Verified gap on the sub-quantity α(C_7^5): 367 (lower) — 401 (Lovász ϑ^5 upper, ⌊ϑ^5⌋).**
Table of known α(C_7^d): d=1:3, d=2:10, d=3:33, d=4:108–115, d=5:367–401.

**Slack / how loose.**
- They did NOT do an exhaustive search; 367 came from ONE adapted circular construction
  + a small local ILP. They report: tried many shift words / division factors, found no
  set of size ≥368; a local search showed no 3-out/4-in swap improves R. So 367 is a
  strong local optimum of THIS construction, but the global α(C_7^5) ≤ 401 is unproven
  to be < 368.
- Remark 3.1: same family gives α(C_5^{11}) ≥ 4009 — shows the {t·(1,q,...)} family is a
  general engine for circular-graph independent sets.

**Difficulty of beating it this run.**
- Beating Θ(C_7) ≥ 367^(1/5) requires either (a) α(C_7^5) ≥ 368 (authors searched hard,
  found nothing — and even +1 only moves Θ from 3.25785 to 3.25856), or (b) α(C_7^6) ≥
  1340 (=ceil(367^(6/5))≈1339.7) — but α(C_7^6) is far below this and uncomputed; 7^6 =
  117649 vertices, a huge search. Both are hard for a single numpy/scipy run.
- The check is reviewer-cheap (verify an explicit independent set), but FINDING a better
  one is the obstacle. Lovász ϑ upper bound is already an exact SDP value — not movable
  without new theory (it would require ϑ < current value, impossible since ϑ is exact).
