# CJS12 — Claesson, Jelínek, Steingrímsson

"Upper bounds for the Stanley-Wilf limit of 1324 and other layered patterns."
arXiv:1111.5736; JCTA 119 (2012). PDF: `pdfs/cjs12.pdf`.

## Result A: L(1324) ≤ 16 (Corollary 5) — the merge bound

- **Lemma 3 (merge).** Every (σ⊕1⊕τ⊕1⊕ρ)-avoider is a *merge* of a (σ⊕1⊕ρ)-avoider and
  a (τ)-avoider (split the permutation into two colour classes). For 1324 = 1⊕(213)... the
  upshot: every 1324-avoider is a **merge of a 132-avoider and a 213-avoider**.
- **Lemma 4 (the key inequality).** If every permutation of class C is a merge of one from A
  (growth α) and one from B (growth β), then **√γ ≤ √α + √β** (γ = gr(C)). Proof: an
  n-point merge is chosen by selecting which k of n positions/values go to the first part,
  giving the C(n,k)^2 factor; the √ comes from the dominant balanced term.
- With A = B = Av(132), α = β = 4: √L(1324) ≤ √4 + √4 = 4 ⟹ **L(1324) ≤ 16**.
- **Why it is loose:** the merge of *arbitrary* 132- and 213-avoiders vastly overcounts
  1324-avoiders (the merge ignores the cross-constraint between the two colour classes). The
  √-superadditivity is tight only if the two parts are independent — they are not.

## Result B (conditional): L(1324) ≤ e^{π√(2/3)} ≈ 13.001954 (Theorem 17)

- For a pattern τ, S^k_n(τ) = #{τ-avoiders of length n with exactly k inversions}.
- **Proven base case (132).** Columns of the inversion triangle of Av(132) ARE weakly
  increasing in n and eventually constant; the eventual value of column k is p(k) (#integer
  partitions of k). Since p(k) < ρ^√k with **ρ = e^{π√(2/3)}** (Lemma 12, a classical
  Hardy–Ramanujan-type bound), summing over k ≤ C(n,2) gives the 132 growth rate.
- **Conjecture 13 (Increasing columns).** For all n,k: **S^k_n(1324) ≤ S^k_{n+1}(1324)** —
  i.e. the inversion-distribution columns for 1324-avoiders are weakly increasing in n.
  Verified numerically (small triangle reproduced on p.~9 of the PDF), unproven.
- **Theorem 17.** If Conjecture 13 holds, the eventual column values are bounded analogously
  and L(1324) ≤ ρ = e^{π√(2/3)} ≈ 13.001954. (Lemma 14: a 1324-avoider with k < n−1
  inversions decomposes as ⊕ of 132- and 213-blocks; Prop 15, Lemma 16 control the columns.)

**ATTACKABLE SUB-PIECE.** Conjecture 13 is a clean, purely combinatorial monotonicity
statement about a finite triangle of counts — exactly the kind of statement that could have a
finite/inductive certifiable proof. Proving even a *weakened* form (e.g. S^k_n ≤ S^k_{n+1}
for k bounded, plus an independent tail bound) could yield an unconditional upper bound
below 13.5. Each column is *eventually constant* and CJS identify the limiting value, so the
open part is the approach to the limit, not the limit itself.

## Lean-fit assessment
- Result A (16) is fully algebraic: the √-superadditivity (Lemma 4) is an elementary
  C(n,k)^2 counting inequality + a limit — **Lean-fit in principle** but the value 16 is far
  from the record, so not a target on its own. The *inequality* √γ ≤ √α+√β is a reusable
  lemma if any sketch builds an improved merge.
- Result B's conditional bound is gated on Conjecture 13 (discrete monotonicity) + the
  partition bound p(k) < e^{π√(2/3)·√k} (classical, provable). If Conj 13 (or a usable
  weakening) were certified, the resulting upper bound would be a **discrete/algebraic**
  argument — **Lean-fit**, and would beat 13.5. The partition asymptotic ρ = e^{π√(2/3)} is
  a transcendental but standard constant.
