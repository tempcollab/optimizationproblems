# Approach `branching-transversal-cert`

**Direction:** UPPER bound on C_5b (machinery / prerequisite). Closes the integrality gap of
the fractional transversal lemma so that the tight `h(A) ≤ m` can be Lean-certified at a
`decide`-tractable cost — the universal prerequisite for any sub-`4/7` Lean certificate.

**The obstacle this angle exists to solve.** R3 built the fractional-matching lemma
`hLe_of_fracMatching` (`Constants.C5bTransversal`): a `decide`-checkable `O(|F|·N)` certificate
that bounds the minimum transversal `τ` of the 3-AP hypergraph by an LP-duality (fractional
matching) value `ν*`. But on the record gadget `A_base` the hypergraph has an **integrality
gap** `τ = 6 > ⌈ν*⌉ = 5`, so the fractional cert only proves `h(A_base) ≤ 9`, **not** the tight
`h(A_base) ≤ 8`. Any sub-`4/7` gadget at `N ≈ 30` needs the tight `h`-bound; the fractional
lemma may under-certify there. This approach replaces the fractional lower bound on `τ` by an
**exact branch-and-bound hitting-set lower bound**, reaching the integral `τ`.

## Status (R4): BUILT + (claim) VERIFIED-CLEAN — tight `h(A_base) ≤ 8` certified in Lean

New file `lean/Constants/C5bBranch.lean`, namespace `C5bBranch`. `lake build Constants.C5bBranch`
PASS (full `lake build` PASS). Zero `sorry`; `#print axioms` clean (details below).

### What compiled (claim — pending reviewer re-verification)

- `noTransLe : List ((ℤ×ℤ×ℤ)×ℕ) → ℕ → Bool` — structurally recursive branch-and-bound
  predicate. `noTransLe FW k = true` certifies **no vertex set of size `≤ k` hits every edge of
  `FW`**, i.e. `τ(FW) > k`. Recursion: `[] ↦ false`; `(_::_), 0 ↦ true`; else branch on the
  first edge's 3 vertices, `removeVertex` each (drop every edge through it), `AND` the three
  recursive verdicts at budget `k−1`.
- `removeVertex (v) (FW)` — `FW.filter (¬ memTriple v ·)`; drops every edge through `v`.
- `hitsAll_removeVertex_erase` — residual-hitting lemma: if `H` hits all of `FW` then
  `H.erase v` hits all of `removeVertex v FW` (surviving edges avoid `v`, so their witness
  vertex `≠ v` survives the erase). The subtle bookkeeping step the outliner flagged.
- `noTransLe_sound` — **soundness lemma**: `noTransLe FW k = true → ∀ H (Nodup) hitting FW,
  k < H.length`. Proof = strong induction on `k`; at each step `H` must contain a vertex `w` of
  the first edge, `H.erase w` hits the residual, IH gives `k−1 < |H.erase w| = |H|−1`.
- `hLe_of_branchCert` — **bridge**: with `A.Nodup`, `edgesOK A FW = true`, and a branching cert
  `noTransLe FW k = true`, every no-3-AP (avoiding) sublist `S ⊆ A` has
  `S.length ≤ A.length − k − 1`. Reuses the verified complement/cardinality split from
  `hLe_of_fracMatching`.
- Validation on `A_base`:
  - `Abase_branch_tau : noTransLe Abase_APs 5 = true` by kernel `decide` (364-node tree;
    worst case `3^5 = 243` leaves). Depends on **no axioms**.
  - `Abase_avoiders_le_8` — the **tight** `h(A_base) ≤ 8` (`τ ≥ 6`), via `hLe_of_branchCert`.
  - Tightness confirmed by `#eval`: `noTransLe Abase_APs 6 = false` (a size-6 transversal
    exists), so `τ = 6` exactly.

### Axioms (claim, reviewer to re-run `#print axioms`)

- `noTransLe_sound`, `hLe_of_branchCert`, `Abase_avoiders_le_8` →
  `[propext, Classical.choice, Quot.sound]` only — **no `sorryAx`, no `Lean.ofReduceBool`**
  (no `native_decide`, plain `decide` throughout, per the Lean encoding Rule).
- `Abase_branch_tau` → "does not depend on any axioms".

### Value claimed this round

- **Claim (machinery, Lean-checked):** a reusable, zero-`sorry`, plain-`decide` branching
  transversal certificate that certifies the **integral / tight** `h(A) ≤ N − k − 1` for any
  point list `A` and any branching cert `noTransLe FW k = true`, at `O(3^k)` tree cost.
  Validated on `A_base` re-deriving the tight `h(A_base) ≤ 8` (`τ = 6`), closing the R3
  integrality gap (fractional reached only `h ≤ 9`).
- **No bound improvement** this round — still `held = 4/7`, not beaten. This is the recorded
  PRIORITY bound-mover *prerequisite* (run_state Next(R4)), not the beat.

## Trust boundary / honest scope

- This file certifies `h(A_base) ≤ 8` for the *finite* set `A_base` only. `A_base` already has
  the record value `4/7`; re-deriving it does not beat the record. The point is the *method*:
  the tight bound now comes from a scalable transversal route (`decide` on a small tree)
  instead of `C(14,9)` enumeration.
- The bridge to the actual constant `c*` (Thm 1.5, `c* = inf f(n)/n`) is the explicit
  `MTThm15` hypothesis in `Constants.C5b`; this file does not assume it.
- **The genuine remaining risk is `N = 30` scaling.** A standalone branching cert at `N = 30`
  needs budget ≈ 12–13, worst-case `3^13 ≈ 1.6M` leaves — at the edge of plain `decide`. This
  is exactly what the sibling `hybrid-fractional-plus-branch` mitigates (use the fractional
  lemma to knock the budget down first, then branch only the small integral−fractional
  residual). That hybrid composition is a separate build.

## Concretely what would push it further

1. **Hybrid composition (sibling slug `hybrid-fractional-plus-branch`).** Compose
   `hLe_of_fracMatching` (cheap `τ ≥ ⌈ν*⌉`) with `hLe_of_branchCert` (top up by the residual)
   via `τ ≥ max(fractional, branching)`, keeping the branch budget tiny at `N = 30`. The
   `noTransLe` predicate + `noTransLe_sound` + `hLe_of_branchCert` here are the importable
   interface for that build.
2. **Edge-ordering / pruning for larger budgets.** `noTransLe` currently picks the *first*
   edge. A most-constrained-edge-first ordering (off-Lean, `decide` follows the same tree)
   shrinks the real tree by orders of magnitude — important once budget grows past ~8.
3. **The `N = 30` gadget search (off-Lean, exact α).** A single indecomposable 30-point
   (4,5)-set with `h = 17` (`17/30 ≈ 0.5667 < 4/7`); then certify `is45setB` (in
   `Constants.C5b`) for the (4,5)-property and `noTransLe`/`hLe_of_branchCert` here (or the
   hybrid) for `h ≤ 16`. The two compose into a sub-`4/7` Lean certificate.

## For the next (hybrid) builder — importable interface

```
import Constants.C5bBranch
open C5bBranch
-- predicate:        noTransLe : List ((ℤ×ℤ×ℤ)×ℕ) → ℕ → Bool
-- soundness:        noTransLe_sound (k FW H) : H.Nodup → noTransLe FW k = true →
--                       hitsAll H FW → k < H.length
-- bridge (h-bound): hLe_of_branchCert (hA hedges hcert hS hSsub hSavoid) :
--                       S.length ≤ A.length - k - 1
-- removeVertex, hitsAll_removeVertex_erase are exported too.
-- (hitsAll, edgesOK, avoidsAll, tripleInA_mem come from C5bTransversal, re-`open`ed.)
```

## Files

- `lean/Constants/C5bBranch.lean` — the branching machinery + A_base validation (compiles, no
  `sorry`, axioms `{propext, Classical.choice, Quot.sound}` only; `Abase_branch_tau` axiom-free).
- `constants/5b/certificate/branching/README.md` — reviewer reproduction instructions.
- `constants/5b/certificate/branching/check_branch_cert.py` — numerical re-check (mirrors
  `noTransLe`, independent exact-`τ` cross-check).

## Source

Ma & Tang, arXiv:2602.23282 (Feb 2026) [MT26], Lemma 2.3 (Sidon ⟺ no 3-AP), Theorem 1.5
(`c* = inf_n f(n)/n`). Branch-and-bound hitting-set lower bound: standard.
