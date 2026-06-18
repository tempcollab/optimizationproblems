# C_5b — AP-transversal certificate machinery (R3, slug `floorplus1-transversal-N30`)

**Status:** machinery sub-goal — the reusable transversal soundness lemma, fully proven in
Lean, validated on the record gadget `A_base`. Does NOT beat the record (and does not even
re-derive the tight `h(A_base)=8` — see the integrality-gap note). It delivers the
load-bearing certificate format for any future `N≥21` `h`-upper-bound, where the
`C(N,m+1)` subset enumeration is hopeless.

**Type:** Lean-fit. The check is `lake build Constants.C5bTransversal` + `#print axioms`
(type-checking IS the reproduction). A companion numerical re-check script is provided.

## What is certified (Lean, `lean/Constants/C5bTransversal.lean`, namespace `C5bTransversal`)

The **transversal soundness lemma** (load-bearing, no `sorry`, no smuggled axiom):

```
theorem hLe_of_fracMatching
    {A : List ℤ} {FW : List ((ℤ × ℤ × ℤ) × ℕ)} {D m : ℕ}
    (hA : A.Nodup)
    (hedges : edgesOK A FW = true)          -- every listed edge is a genuine 3-AP inside A
    (hload  : loadOK A FW D = true)          -- every point of A carries total weight ≤ D
    (hT     : D * (A.length - m - 1) < totalW FW)   -- fractional matching value > N−m−1
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ A)
    (hSavoid : avoidsAll S FW = true) :      -- S avoids (does not fully contain) every edge
    S.length ≤ m
```

Mathematical content (LP-duality / hitting-set, [MT26] Lemma 2.3 supplies Sidon ⟺ no 3-AP):
a no-3-AP (Sidon) subset `S` avoids every AP, so `A \ S` is a **transversal** of the
3-AP-hypergraph. A fractional matching `FW` (weights `w_e`, per-vertex load `≤ D`, total
`T`) lower-bounds the minimum transversal by `T/D` (each edge is hit, so its weight is
counted at least once — proved by the list double-counting `totalW_le_loadSum`). Hence
`|A\S| ≥ T/D`, i.e. `|S| ≤ N − T/D`. The cost is `O(|F|·N)`, **not** `C(N, m+1)`.

Supporting fully-proven lemmas: `single_edge_charge`, `totalW_le_loadSum` (double-counting
core), `loadSum_le`, `tripleInA_mem`.

### Validation on `A_base` (namespace `C5bTransversal.Validation`)

- `Fcert_base` — a fractional-matching certificate over the **twelve** 3-term APs of
  `A_base`, denominator `D = 6`, total `T = 27` (so `ν* = 27/6 = 4.5`).
- `Fcert_base_edgesOK : edgesOK Abase Fcert_base = true`  — `decide`, zero axioms.
- `Fcert_base_loadOK : loadOK Abase Fcert_base 6 = true`   — `decide`, zero axioms.
- `Fcert_base_total  : totalW Fcert_base = 27`             — `decide`.
- `Abase_avoiders_le_9 : … → S.length ≤ 9` — the lemma fired end-to-end: every sublist of
  `A_base` avoiding all twelve APs has length `≤ 9` (a Sidon subset avoids them all, so
  `h(A_base) ≤ 9` by the transversal route).

## HONEST scope note — the integrality gap (why this validates `h ≤ 9`, not the tight `h ≤ 8`)

The tight value is `h(A_base) = 8` (`τ = 6`), proved zero-axiom in `Constants.C5b` by the
`C(14,9)` enumeration. But the **fractional** matching value of A_base's AP-hypergraph is
only `ν* = 4.5`, and `4.5` is the *exact* LP optimum (re-verified by the script). So
`τ = 6 > ⌈ν*⌉ = 5` — an integrality gap. Pure LP-duality (this lemma) therefore certifies
only `h ≤ 9`, **not** the tight `h ≤ 8`. The lemma is correct and reusable; closing the last
unit needs an *integral* transversal certificate (a branching / odd-set strengthening). That
is the next sub-goal, recorded in `approaches/floorplus1-transversal-N30.md`.

## How the reviewer re-establishes it

Lean (gold standard):
```
cd /home/agentuser/repo/lean
source $HOME/.elan/env
lake build Constants.C5bTransversal      # or full: lake build
```
Then axioms (must show no `sorryAx`, no `Lean.ofReduceBool`/`native_decide`):
```
cat > AxCheckT.lean <<'EOF'
import Constants.C5bTransversal
open C5bTransversal
#print axioms hLe_of_fracMatching
#print axioms totalW_le_loadSum
open C5bTransversal.Validation
#print axioms Abase_avoiders_le_9
EOF
lake env lean AxCheckT.lean
rm AxCheckT.lean
```
Numerical re-check (the certificate's finite inputs + the integrality gap):
```
python3 constants/5b/certificate/transversal/check_transversal_cert.py
```

## Verified output (R3)

`lake build Constants.C5bTransversal` → `Build completed successfully` (~17s module).
`#print axioms`:
```
'C5bTransversal.hLe_of_fracMatching'        depends on axioms: [propext, Classical.choice, Quot.sound]
'C5bTransversal.totalW_le_loadSum'          depends on axioms: [propext, Quot.sound]
'C5bTransversal.Validation.Fcert_base_edgesOK' does not depend on any axioms
'C5bTransversal.Validation.Fcert_base_loadOK'  does not depend on any axioms
'C5bTransversal.Validation.Abase_avoiders_le_9' depends on axioms: [propext, Classical.choice, Quot.sound]
```
No `sorryAx`, no `Lean.ofReduceBool` — only the three standard Mathlib foundational axioms.

## Source

Ma & Tang, "Largest Sidon subsets in weak Sidon sets", arXiv:2602.23282 (Feb 2026), [MT26]
(Lemma 2.3). LP-duality hitting-set bound: standard (König/LP relaxation of vertex cover).
