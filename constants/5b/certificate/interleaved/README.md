# Interleaved (fix-then-branch) transversal certificate — C_5b

Machine-checked Lean machinery for the **budget-shrinking** transversal lower bound
`τ(FW_frac ∪ FW_res) ≥ a + (g + 1)` (hence `h(A) ≤ N − a − g − 1`), where a fractional
certificate carries `a` of the bound on a support `P` and the branch-and-bound certifies the
rest only on the **residual** family (edges avoiding `P`) with budget `g`.

This is the genuinely-interleaved version that the R4 `max`-hybrid (`hLe_of_hybrid`) was NOT:
the hybrid took the plain `min` of the two independent bounds and left the branch budget at the
full `τ`; here the branch sees only the residual, so `3^g` stays tiny when the LP has an
integral component.

## Lean source / build target

- File: `lean/Constants/C5bInterleaved.lean`
- Build: `cd lean && lake build Constants.C5bInterleaved`  (or the default `Constants` target,
  globs `Constants.+`).  Build PASS, no warnings.

## Theorems

- `C5bInterleaved.hLe_of_interleaved` — the interleaved soundness lemma. Load-bearing new
  content: the disjoint residual attribution. An arbitrary hitting set `H` of the combined
  family is partitioned `(H ∩ P) ⊎ (H \ P)`; the fractional load lemma forces `|H ∩ P| ≥ a`
  (off-`P` vertices carry zero listed load), and the residual-hitting argument feeds
  `noTransLe_sound` to force `|H \ P| ≥ g + 1`. No double counting. Every step inside the
  formalization. Supporting lemmas proved here:
  `vertexLoad_zero_of_notInP`, `loadSum_filterP`, `frac_lb_on_P`, `res_hitsAll_filter`.
  Reuses `C5bTransversal.totalW_le_loadSum`, `C5bBranch.noTransLe_sound`,
  `C5bBranch.hitsAll_removeVertex_erase`.

- `C5bInterleaved.SynValidation.Asyn_avoiders_le_8` — the mechanism FIRES: a synthetic
  4-AP instance with fractional value `a = 2` and residual branch budget `g = 1` (3 leaves)
  certifies `τ = 4`, branching only `g = 1` instead of the full `3`.

- `C5bInterleaved.BaseValidation.Abase_avoiders_le_8_interleaved` — `A_base` in the degenerate
  `P = ∅` form (`a = 0`, `g = 5`), soundly re-deriving the tight `h(A_base) ≤ 8`.

## Axiom check (clean)

```
lake env lean <importing-file>   -- #print axioms
'C5bInterleaved.hLe_of_interleaved'                       : [propext, Classical.choice, Quot.sound]
'C5bInterleaved.SynValidation.Asyn_avoiders_le_8'         : [propext, Classical.choice, Quot.sound]
'C5bInterleaved.BaseValidation.Abase_avoiders_le_8_interleaved' : [propext, Classical.choice, Quot.sound]
```

No `sorryAx`, no `Lean.ofReduceBool` (no `native_decide`). Gold-standard.

## HONEST finding — `A_base` is half-integral, no budget shrink there

`check_interleaved_cert.py` re-derives (exact LP + exact `τ`, no heuristics):

- `A_base`'s 3-AP cover LP is **fully half-integral** (`ν* = 4.5`, every vertex `0` or `1/2`),
  with **no** integral (`x = 1`) vertex — so Nemhauser–Trotter fixing is vacuous, and there
  is no forced vertex (143 distinct minimum covers).
- `max_{P ⊆ A} ( ⌈ν*(edges in P)⌉ + τ(edges avoiding P) ) = 6`, attained **only** at `P = ∅`
  (`a = 0`, full branch budget `g = 5`).

So the milestone "g = 1 on A_base" is **mathematically not achievable** for the sound
support-disjoint interleaving: A_base is a worst-case half-integral instance. The lemma is
nonetheless built, fully proven, and sound; its budget-shrink is exhibited on `A_syn` and is
expected to fire on an `N ≈ 30` gadget that has an integral LP component. This is a real,
reusable Lean increment plus a precise characterization of where it does and does not help.

## Re-check script

```
python3 constants/5b/certificate/interleaved/check_interleaved_cert.py
```
Verifies (A) the synthetic mechanism (`a=2 + g=1 ⇒ τ=4`, budget-shrink) and (B) the A_base
half-integral degeneracy (`max_P = 6` only at `P=∅`).

## Sources

- [MT26] Ma & Tang, arXiv:2602.23282 (Lemma 2.3, Thm 1.5).
- LP-fix-then-branch for `d`-Hitting-Set / Nemhauser–Trotter half-integrality:
  arXiv:2308.05974, arXiv:2506.24114, arXiv:1811.09429.
