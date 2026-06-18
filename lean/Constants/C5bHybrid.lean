import Mathlib
import Constants.C5bTransversal
import Constants.C5bBranch

/-!
# C_5b : HYBRID transversal certificate — `max` of the fractional and branching τ-bounds

This file composes the two independent, already-verified soundness lemmas for the minimum
transversal `τ` of the 3-AP hypergraph `H(A)`:

* `C5bTransversal.hLe_of_fracMatching` — the **fractional-matching / LP-duality** lower bound
  on `τ`, cheap (`O(|F|·N)`) but with an integrality gap (only `τ ≥ ⌈ν*⌉`);
* `C5bBranch.hLe_of_branchCert` — the **branch-and-bound** lower bound on `τ`, exact (reaches
  the integral `τ`) but with cost `O(3^budget)`.

Both bound the SAME quantity `τ(H(A))`, and `h(A) ≤ N − τ`.  Each lemma, applied to a no-3-AP
(Sidon) sublist `S ⊆ A`, yields an upper bound on `|S|`:

* fractional gives `|S| ≤ m_frac` (where `D·(N − m_frac − 1) < T`, i.e. `m_frac = N − ⌈T/D⌉`);
* branching gives `|S| ≤ N − k_branch − 1`.

The **hybrid bound is the minimum of the two `|S|`-upper-bounds**, equivalently `h(A) ≤
N − max(τ_frac, τ_branch)`.  This file states and proves that composition
(`hLe_of_hybrid`) and validates it on the record gadget `A_base`.

## HONEST SCOPE — exactly what is and is NOT proven (read this)

This is the **`max` composition**, NOT a true interleaving.  Concretely:

* What IS proven: `S.length ≤ min(m_frac, N − k_branch − 1)` for any `S` avoiding the listed
  APs, given a fractional certificate (params `D, m_frac, FW_frac`) AND a branching
  certificate (params `k_branch, FW_branch`).  This is a sound lower bound `τ ≥
  max(τ_frac, τ_branch)` on the *same* min-transversal.  The proof is a one-line `min`/`omega`
  over the two independent soundness results — it is *trivially valid* and adds no new trust.

* What is NOT proven (the deferred step): this does **not** knock the fractional residual
  down before branching.  In a genuinely-interleaved certificate one would (i) take the
  fractional dual support, (ii) contract the edges it already covers, and (iii) run the
  branch-and-bound only on the *residual* family, so the branch budget shrinks to
  `(τ − ⌈ν*⌉)` (typically 1–2) instead of the full `τ` (≈ 12–13 at `N = 30`).  The `max`
  composition here still requires the branching certificate to certify the *full* `τ` on its
  own — its budget is unchanged.  So **this file does NOT by itself make the branching
  budget small at `N ≈ 30`**: that is the further interleaving step (see the approach doc).

In short: the `max` is a sound, simple first version that lets a *single* call certify
`h(A) ≤ N − max(τ_frac, τ_branch)` (picking up whichever certificate is tighter), but the
N≈30 *scaling* property — a tiny branch budget — is the interleaved version still to be built.

## Validation on `A_base` (the `max` picks up the branch bound)

`Abase_avoiders_le_8_hybrid` : with the fractional cert (`τ ≥ 5`, `h ≤ 9`) AND the branching
cert (`τ ≥ 6`, `h ≤ 8`) both supplied, the hybrid `min` yields the tight `h(A_base) ≤ 8`.
The `max` correctly prefers the branch bound (`τ = 6`) over the fractional one (`⌈ν*⌉ = 5`),
exactly as designed.  By `decide` / `omega`, zero added axioms beyond the imported lemmas.

Source of the structural facts: Ma & Tang, arXiv:2602.23282 (Feb 2026), **[MT26]**.
-/

namespace C5bHybrid

open C5bTransversal C5bBranch

/-! ## The hybrid soundness lemma (`max` of the two τ-lower-bounds)

Given a fractional-matching certificate (parameters `D`, `m_frac`, family `FW_frac`) AND a
branching certificate (budget `k_branch`, family `FW_branch`), every sublist `S ⊆ A` that
avoids BOTH listed families has length `≤ min (m_frac) (N − k_branch − 1)`.

Note the two certificates may use *different* edge families `FW_frac`, `FW_branch` (both must
be genuine AP families inside `A`); `S` is required to avoid both.  In the intended
application both are (sub)families of the full 3-AP family of `A`, so a genuinely no-3-AP set
avoids both automatically. -/
theorem hLe_of_hybrid
    {A : List ℤ}
    {FW_frac FW_branch : List ((ℤ × ℤ × ℤ) × ℕ)}
    {D m_frac k_branch : ℕ}
    (hA : A.Nodup)
    -- fractional certificate
    (hedges_f : edgesOK A FW_frac = true)
    (hload_f : loadOK A FW_frac D = true)
    (hT_f : D * (A.length - m_frac - 1) < totalW FW_frac)
    -- branching certificate
    (hedges_b : edgesOK A FW_branch = true)
    (hcert_b : noTransLe FW_branch k_branch = true)
    -- the Sidon candidate
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ A)
    (hSavoid_f : avoidsAll S FW_frac = true)
    (hSavoid_b : avoidsAll S FW_branch = true) :
    S.length ≤ min m_frac (A.length - k_branch - 1) := by
  -- the two independent upper bounds on `|S|`
  have hfrac : S.length ≤ m_frac :=
    hLe_of_fracMatching hA hedges_f hload_f hT_f hS hSsub hSavoid_f
  have hbranch : S.length ≤ A.length - k_branch - 1 :=
    hLe_of_branchCert hA hedges_b hcert_b hS hSsub hSavoid_b
  -- the hybrid bound is the minimum (= `h(A) ≤ N − max(τ_frac, τ_branch)`)
  exact le_min hfrac hbranch

/-! ## Validation on the record gadget `A_base`

We feed BOTH the fractional certificate `Fcert_base` (from `C5bTransversal`, `τ ≥ 5`) and the
branching certificate `Abase_APs` / `noTransLe … 5` (from `C5bBranch`, `τ ≥ 6`) into the
hybrid lemma.  The `min` resolves to `min 9 8 = 8`, i.e. the `max` of the τ-bounds prefers the
*branch* value `τ = 6` over the fractional `⌈ν*⌉ = 5`. -/

namespace Validation

open C5bTransversal.Validation C5bBranch.Validation

/-- **Hybrid validation (tight).**  With both certificates supplied, the hybrid lemma forces
every sublist of `A_base` that avoids both listed AP families to have length `≤ 8`.

This demonstrates the `max` composition picking up the strictly-better branch bound: the
fractional cert alone gives `≤ 9`, the branch cert gives `≤ 8`, and `min 9 8 = 8`. -/
theorem Abase_avoiders_le_8_hybrid
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ C5bTransversal.Validation.Abase)
    (hSavoid_f : avoidsAll S Fcert_base = true)
    (hSavoid_b : avoidsAll S Abase_APs = true) :
    S.length ≤ 8 := by
  -- fractional `hT`: 6 * (14 - 9 - 1) = 6*4 = 24 < 27 = totalW
  have hT_f : (6 : ℕ) * (C5bTransversal.Validation.Abase.length - 9 - 1) < totalW Fcert_base := by
    rw [C5bTransversal.Validation.Abase_length, Fcert_base_total]; omega
  -- the branching family edges live in `Abase` (same 14 points); supply edgesOK over `Abase`.
  -- `C5bBranch.Validation.Abase` is defeq to `C5bTransversal.Validation.Abase` (re-export),
  -- so `Abase_APs_edgesOK : edgesOK C5bBranch.Validation.Abase Abase_APs = true` applies.
  have hedges_b : edgesOK C5bTransversal.Validation.Abase Abase_APs = true :=
    Abase_APs_edgesOK
  have h := hLe_of_hybrid
    (A := C5bTransversal.Validation.Abase)
    (FW_frac := Fcert_base) (FW_branch := Abase_APs)
    (D := 6) (m_frac := 9) (k_branch := 5)
    C5bTransversal.Validation.Abase_nodup
    Fcert_base_edgesOK Fcert_base_loadOK hT_f
    hedges_b Abase_branch_tau
    hS hSsub hSavoid_f hSavoid_b
  -- `min 9 (14 - 5 - 1) = min 9 8 = 8`
  rw [C5bTransversal.Validation.Abase_length] at h
  simpa using h

end Validation

end C5bHybrid
