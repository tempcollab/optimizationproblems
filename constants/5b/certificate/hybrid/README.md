# Hybrid transversal certificate — reproduction (C_5b, round 4)

Lean lemma `C5bHybrid.hLe_of_hybrid` composing the two independent, already-verified
lower bounds on the minimum AP-transversal `τ` of the 3-AP hypergraph `H(A)`:

- `C5bTransversal.hLe_of_fracMatching` — fractional / LP-duality (cheap, integrality gap);
- `C5bBranch.hLe_of_branchCert` — branch-and-bound (exact, `O(3^budget)` cost).

The hybrid takes the **max of the two τ-lower-bounds** (equivalently the **min of the two
`|S|`-upper-bounds**), so a single call certifies `h(A) ≤ N − max(τ_frac, τ_branch)`.

## What this IS and is NOT (honest scope)

- IS: a sound `max` composition — `S.length ≤ min(m_frac, N − k_branch − 1)`. One-line
  `le_min` over the two soundness results; trivially valid, no new trust.
- IS NOT: a true interleaving. The branching certificate still has to certify the **full**
  `τ` on its own (its budget is unchanged). This file does **not** knock the fractional
  residual down before branching, so it does **not** by itself make the branch budget small
  at `N ≈ 30`. That residual-knockdown is the deferred interleaving step (see the approach
  doc). MACHINERY only — does **not** beat the record `4/7`; it re-derives the *known*
  `h(A_base) = 8`.

## Files

- `lean/Constants/C5bHybrid.lean` — the lemma + `A_base` validation (built by `lake build`,
  the `Constants` lib globs `Constants.+`).
- `check_hybrid_cert.py` — independent numerical re-check of the arithmetic the Lean lemma
  relies on (the two τ-bounds and that `max` prefers the branch bound on `A_base`).

## Reproduce the Lean check (gold standard — type-checking IS the certificate)

```
cd lean
export PATH="$HOME/.elan/bin:$PATH"
lake build Constants.C5bHybrid     # PASS, 11s incremental
```

Axioms (must show no `sorryAx`, no `Lean.ofReduceBool`):

```
cat > /tmp/axcheck.lean <<'EOF'
import Constants.C5bHybrid
open C5bHybrid
#print axioms hLe_of_hybrid
#print axioms C5bHybrid.Validation.Abase_avoiders_le_8_hybrid
EOF
lake env lean /tmp/axcheck.lean
```

Expected (both):
```
depends on axioms: [propext, Classical.choice, Quot.sound]
```

## Key theorems

| name | statement |
|---|---|
| `C5bHybrid.hLe_of_hybrid` | given a fractional cert (`D, m_frac, FW_frac`) AND a branching cert (`k_branch, FW_branch`), any `Nodup S ⊆ A` avoiding both families has `S.length ≤ min m_frac (A.length − k_branch − 1)` |
| `C5bHybrid.Validation.Abase_avoiders_le_8_hybrid` | on `A_base`: `min 9 8 = 8` — the `max` of the τ-bounds picks the branch `τ = 6`, giving the tight `h(A_base) ≤ 8` |

## Numerical sanity (independent)

```
python3 constants/5b/certificate/hybrid/check_hybrid_cert.py
```

Reproduces, from scratch in Python: the 12 APs of `A_base`; the fractional value
`ν* = T/D = 27/6 = 4.5 → ⌈ν*⌉ = 5 → h ≤ 9`; the exact min-transversal `τ = 6 → h ≤ 8`; and
that `max(5, 6) = 6`, so the hybrid h-bound is `14 − 6 = 8`, matching the Lean `min 9 8 = 8`.
