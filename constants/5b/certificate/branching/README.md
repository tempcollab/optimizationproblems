# Branching transversal certificate — C_5b (round 4)

**What this certifies (machinery sub-goal):** a *tight, scalable* Lean-checked transversal
lower bound that closes the integrality gap left by the fractional certificate of
`Constants.C5bTransversal`. It re-derives `h(A_base) ≤ 8` (the record value, `τ = 6` exactly)
through a `decide`-tractable branch-and-bound hitting-set certificate, instead of the
`C(14,9)` enumeration. **It does NOT by itself beat the record `4/7`** — it removes the
blocker (the fractional lemma stalled at `h ≤ 9`, since `ν* = 4.5 < τ = 6`) so that a future
indecomposable `N ≈ 30` gadget can be Lean-certified `h ≤ 16` once one is found.

## Authoritative certificate (Lean)

- File: `lean/Constants/C5bBranch.lean`, namespace `C5bBranch`.
- Build: from `lean/`, `lake build Constants.C5bBranch` (or full `lake build`). PASS.
- Key declarations:
  - `noTransLe : List ((ℤ×ℤ×ℤ)×ℕ) → ℕ → Bool` — the branch-and-bound predicate;
    `noTransLe FW k = true` certifies `τ(FW) > k` (no vertex set of size `≤ k` hits all edges).
  - `noTransLe_sound` — soundness: `noTransLe FW k = true → ∀ Nodup hitting set H, k < |H|`.
  - `hLe_of_branchCert` — bridge: with `edgesOK A FW` and `noTransLe FW k = true`, every
    no-3-AP (avoiding) sublist `S ⊆ A` has `|S| ≤ |A| − k − 1` (reuses the complement /
    cardinality split of `hLe_of_fracMatching`).
  - `C5bBranch.Validation.Abase_branch_tau : noTransLe Abase_APs 5 = true` — the load-bearing
    `decide` (364-node tree). Depends on **no axioms**.
  - `C5bBranch.Validation.Abase_avoiders_le_8` — the tight `h(A_base) ≤ 8`.

## Reproduce

```
cd lean
lake build Constants.C5bBranch        # PASS
lake env lean /dev/stdin <<'EOF'
import Constants.C5bBranch
open C5bBranch
#print axioms noTransLe_sound
#print axioms hLe_of_branchCert
#print axioms C5bBranch.Validation.Abase_branch_tau
#print axioms C5bBranch.Validation.Abase_avoiders_le_8
EOF
```

Expected axioms (verified round 4):
- `noTransLe_sound`, `hLe_of_branchCert`, `Abase_avoiders_le_8` →
  `[propext, Classical.choice, Quot.sound]` (Mathlib-standard; **no `sorryAx`, no
  `Lean.ofReduceBool`** — i.e. no `native_decide`).
- `Abase_branch_tau` → "does not depend on any axioms" (pure kernel `decide`).

## Numerical re-check (aid, not the certificate)

```
python3 constants/5b/certificate/branching/check_branch_cert.py
```

Reproduces in plain Python: the 12 APs are genuine, `noTransLe(APS,5)=True`,
`noTransLe(APS,6)=False`, the 364-node tree size, an *independent* exact min-transversal
`τ = 6` (witness `{0,136,200,243,272,323}`), and the tight `h ≤ N − τ = 14 − 6 = 8`.

## Trust boundary

- The branching predicate's soundness is fully formalized (`noTransLe_sound`) — no `sorry`,
  no smuggled hypothesis. The hard step (every transversal must hit the first unhit edge; the
  3-vertex branch is a complete case split; erasing the chosen vertex preserves hitting of the
  residual; budget decrements) is the induction in `noTransLe_sound`, with the residual-hitting
  step isolated in `hitsAll_removeVertex_erase`.
- `hLe_of_branchCert` reuses the *already-verified* complement/cardinality split from
  `C5bTransversal.hLe_of_fracMatching`.
- The bridge to the actual constant `c*` (Thm 1.5, `c* = inf f(n)/n`) is the explicit
  `MTThm15` hypothesis in `Constants.C5b` — NOT assumed in this file. This file only certifies
  `h(A_base) ≤ 8` for the finite set `A_base`.

Source: Ma & Tang, arXiv:2602.23282 (Feb 2026) [MT26], Lemma 2.3 (Sidon ⟺ no 3-AP).
B&B hitting-set lower bound: standard.
