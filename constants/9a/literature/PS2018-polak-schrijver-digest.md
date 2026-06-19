# C_9 = Θ(C_7) — literature digest (scout, R12)

## The constant
C_9 = Shannon capacity of the 7-cycle, Θ(C_7) = sup_n α(C_7^⊠n)^(1/n).
- **Lower bound (movable side):** 367^(1/5) ≈ 3.2578 [PS2018]. Comes from an explicit
  independent set of size 367 in C_7^⊠5.
- **Upper bound (FIXED, analytic):** Lovász theta ϑ(C_7) ≈ 3.3177 [L1979]. This is a fixed
  number (SDP value of a specific graph); not improvable by combinatorial search and
  Lean-hostile to re-derive. Note: it is NOT known whether Θ(C_7)=ϑ(C_7).
- Gap lower→upper ≈ 0.0598.
- Prior lower-bound chain: 3 (trivial) → 343^(1/5)≈3.2141 [BMRRST1971] → 108^(1/4)≈3.2237
  [VZ2002] → 350^(1/5)≈3.2271 [MO2017] → **367^(1/5)≈3.2578 [PS2018]**.

## How the record (367 in C_7^⊠5) was achieved — [PS2018], arXiv:1808.07438
- Polak & Schrijver, "New lower bound on the Shannon capacity of C_7 from circular graphs"
  (IPL 143, 2019).
- Construction: the set {t·(1,7,7²,7³,7⁴) mod 382 | t ∈ Z_382} ⊆ Z_382^5 is independent in
  the 5th strong power of the **circular graph** C_{108,382}; this maps to a size-367
  independent set in C_7^⊠5. Found by **computer search guided by the circular-graph
  symmetry** (a cyclic/group-orbit ansatz cut the search to a structured family). Record has
  stood since 2018 — unchanged through the June-2026 literature (AIMS 2026 survey
  math-11-01-111 discusses related graphs T(7,6) but reports no new Θ(C_7) bound).
- α(C_7^⊠4)=108 (best known, VZ2002 lower; whether exact is the bottleneck for the n=4 route).

## Adjacency / certification structure (verified in Python by scout)
- C_7 vertices = Z_7. Two vertices i,j are **confusable (adjacent-or-equal)** iff cyclic
  distance min(|i−j|,7−|i−j|) ≤ 1. α(C_7)=3 (e.g. {0,2,4}) — reproduced.
- Strong product C_7^⊠n: codewords u,v ∈ Z_7^n are **adjacent** iff in EVERY coordinate k,
  u_k and v_k are confusable. An **independent set** = a set of codewords s.t. every distinct
  pair has SOME coordinate with cyclic distance ≥ 2.
- **Certifying "S is an independent set of size ≥ N"** is a pure finite check: a list of N
  codewords in (Fin 7)^n, plus the decidable pairwise condition
  ∀ distinct u,v ∈ S, ∃k, cyclicdist(u_k,v_k) ≥ 2. **Fully Lean-fit** — decidable enumeration
  over a finite explicit list, no continuum. This is the gold-standard Lean target: the
  bound becomes a machine-checked theorem α(C_7^⊠n) ≥ N hence Θ(C_7) ≥ N^(1/n).
- N^(1/n) > record is an algebraic inequality (N^7 > record^7·... — rational power compare),
  Mathlib-provable.

## Tractability — HONEST
- Verifying a GIVEN set is trivially Lean-fit and cheap. The bottleneck is **finding a set
  that beats 367 in C_7^⊠5** (or a competitive set in C_7^⊠6/7). This has resisted search
  since 2018; Polak–Schrijver already exploited the circular-graph symmetry. A brute or
  naive ILP over C_7^⊠5 (7^5 = 16807 vertices, independence-number ILP) is large but the
  RECORD-SEEKING search is the hard, possibly-fruitless part — NOT a guaranteed round-sized
  win.
- n=6: 7^6 = 117649 vertices; α target to beat would be 367^(6/5) ≈ 367·367^(1/5)≈... a
  set of size ⌈3.2578^6⌉=1196+ in C_7^⊠6 beats the lower bound. Larger search, even harder.
- The certificate is easy; the discovery is hard and historically static.
