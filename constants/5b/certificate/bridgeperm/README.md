# C_5b certificate — decidable bridge, permutation-invariance half (R9)

**Slug:** `bridge-perm-invariance-half`.  **No bound move** (Lean-machinery round).
Deliverable: a `lake build`-PASS, axiom-clean set of verified theorems that supply the
**permutation-invariance half** of the decidable bridge
`is45setB l = true → Is45 l.toFinset`, wiring the R8 cap lemma
(`C5bCap.m_le_n_sub_2`, which consumes the abstract `Is45`) toward the concrete engine
predicate `C5b.is45setB`.

## Lean artifact

- File: `lean/Constants/C5bBridgePerm.lean` (auto-included by the `Constants` lib glob
  `Constants.+` in `lean/lakefile.toml` — no lakefile edit needed).
- Build target: `lake build Constants.C5bBridgePerm` (full `lake build` also passes).
- Mathlib pinned at `v4.31.0`.

## Theorems banked (all sorry-free)

| theorem | statement |
|---|---|
| `countDistinct_eq_dedup_length` | `countDistinct l = l.dedup.length` |
| `countDistinct_perm` | `l.Perm l' → countDistinct l = countDistinct l'` |
| `diffSym` | `((x-y).natAbs : ℤ) = ((y-x).natAbs : ℤ)` |
| `diffs6_perm_swap_ab/_bc/_cd` | each adjacent transposition gives `(diffs6 …).Perm (diffs6 …)` |
| `diffs4B_swap_ab/_bc/_cd` | `diffs4B` invariant under each generator swap |
| `pdiffs_perm` | compositional pairwise-diff list is `List.Perm`-invariant |
| `pdiffs_four` | `(pdiffs [a,b,c,d]).Perm (diffs6 a b c d)` |
| **`diffs4B_perm4`** | `[a,b,c,d].Perm [a',b',c',d'] → diffs4B a b c d = diffs4B a' b' c' d'` (all 24 orderings) |
| **`is45setB_to_Is45`** | the assembled bridge, **modulo** the named hypothesis `hcomplete : CombosComplete l` |

`CombosComplete l` is the **single explicit named trust boundary** (a `Prop`, not an
axiom, not a `sorry`) — exactly the `MTThm15` style.  It is the `combos`-completeness fact
("every 4 pairwise-distinct points of `l.toFinset` appear in some order as a member of
`combos l 4`"), proved separately in `C5bCombos.lean` by the sibling builder; leaving it as
a visible hypothesis lets the two halves compose next round.

## Reproduce

```
cd lean
lake build Constants.C5bBridgePerm        # PASS (~50s incremental, full build ~ from cache)
```

Axiom check (must show only `[propext, Classical.choice, Quot.sound]` or fewer; NO
`sorryAx`, NO `Lean.ofReduceBool`):

```
cat > /tmp/ax.lean <<'EOF'
import Constants.C5bBridgePerm
open C5bBridgePerm
#print axioms countDistinct_perm
#print axioms diffs4B_perm4
#print axioms is45setB_to_Is45
EOF
lake env lean /tmp/ax.lean
```

Recorded output (R9):

```
'C5bBridgePerm.countDistinct_perm' depends on axioms: [propext, Classical.choice, Quot.sound]
'C5bBridgePerm.diffs4B_perm4'      depends on axioms: [propext, Classical.choice, Quot.sound]
'C5bBridgePerm.pdiffs_perm'        depends on axioms: [propext, Quot.sound]
'C5bBridgePerm.is45setB_to_Is45'   depends on axioms: [propext, Classical.choice, Quot.sound]
```

## Independent re-check of the perm-invariance claim

`python3 check_perm_invariance.py` brute-forces that `diffs4B` is constant across all 24
orderings of its four arguments — on hand-picked anchors (including a genuine (4,5)-quadruple
from A_base and the FACT1-forbidden `{0,14,21,28}`) and 50 000 random distinct quadruples.
Expected: `ALL PASS`, with both True and False outcomes covered.  Cross-checked against the
Lean `#eval`s of the same quadruples (true/true/true and false/false), which agree.

## What this does NOT establish

- It does **not** prove `CombosComplete l` (the `combos`-completeness fact) — that is the
  sibling slug `bridge-combos-completeness-half` (`C5bCombos.lean`).
- It does **not** move the bound.  The end-to-end `is45setB → Is45` (with `CombosComplete`
  discharged) and the `Abase` corollary `m = 12 = 14 − 2` are a later-round one-line assembly.
