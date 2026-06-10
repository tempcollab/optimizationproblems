# Digest: Ma–Tang 2026, "Largest Sidon subsets in weak Sidon sets" (arXiv:2602.23282)

## What it is
C_5b = largest c s.t. every (4,5)-set of size n (every 4-subset has >=5 distinct
differences) contains a Sidon set of size c*n. Proves 9/17 <= C_5b <= 4/7.
(Erdős problem #757.)

## Reduction
- Build A.P.-hypergraph H(A): edges = 3-term APs in A. Sidon subsets = independent
  sets, so h(A)=α(H(A)). For (4,5)-sets, H(A) is **linear** (edges meet in <=1 vertex)
  and **F_7-free** (no forbidden 7-vertex config), with m_H <= n_H - 2.
- Characterization: C_5b = inf_{n>=1} f(n)/n (limit exists).

## Upper bound 4/7 (explicit construction — the attackable side)
- A single 14-element (4,5)-set:
  A_base = {0,136,200,243,246,249,272,286,298,323,400,528,596,1056}.
- Computer-verified: all C(14,4)=1001 four-subsets have >=5 distinct differences;
  largest Sidon subset has size 8. So f(14) <= 8 => C_5b <= 8/14 = 4/7.
- This is the ONLY witness for the upper bound. Any (4,5)-set of size n with largest
  Sidon subset < (4/7)n would beat it. Brute-force / SAT / local search over small
  integer sets is directly applicable.

## Lower bound 9/17 (transversal estimate)
- Henning–Yeo transversal bound (Thm 5.3): for 3-uniform linear F_7-free H,
  17 τ(H) <= 5 n_H + 3 m_H. With m_H <= n_H-2: 17τ <= 8 n_H, so τ <= (8/17)n,
  α = n - τ >= (9/17)n. Authors say this is "stronger but still not tight."

## Where the slack is / tractability
- Gap 9/17=0.5294 ... 4/7=0.5714 (~4.2%). Both sides are finite-combinatorial.
- UPPER side: a single better small (4,5)-set instance beats 4/7 — purely a search +
  exact-check problem (numpy/itertools, fully reproducible). Most construction-friendly.
- LOWER side: needs a sharper transversal inequality for linear F_7-free 3-graphs with
  m<=n-2 — a proof, harder to do in one run.
