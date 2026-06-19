# C_9 = Θ(C_7) — certificate: Lean-verified 367-baseline in C_7^⊠5

This certificate REPRODUCES the existing verified record lower bound
`Θ(C_7) ≥ 367^(1/5) > 3.2578` [PS2018] as a machine-checked Lean theorem. It does **NOT**
beat the record — it is the search-immune machinery foundation (engine + soundness bridge
+ verified explicit 367-set) that any future beat rides on.

## What is established (all `lake build`-clean, axiom-audited)

The decidable independent-set certificate engine for `C_7^⊠n` plus the Lean-verification of
the explicit Polak–Schrijver size-367 independent set in `C_7^⊠5`:

- `C_7 = Z_7`, two letters confusable iff cyclic distance `min(|i-j|,7-|i-j|) ≤ 1`.
- Codewords are pairwise independent iff SOME coordinate has cyclic distance `≥ 2`.
- A valid pairwise-independent list of distinct length-5 codewords is a genuine independent
  set in the strong-power graph `C_7^⊠5`, so `α(C_7^⊠5) ≥ 367`.
- Under the Shannon-capacity bridge `Θ(G) = sup_n α(G^⊠n)^(1/n)`, this gives
  `Θ(C_7) ≥ 367^(1/5) > 3.2578`.

## Lean files (in `lean/Constants/`)

- `C9.lean` — the engine: `cdist`, `confusable`, `indepPair`, the short-circuiting
  `allPairsIndep : List (List ℕ) → Bool`, and `allPairsIndep_iff` (matches `List.Pairwise`).
- `C9Graph.lean` — the graph bridge: `C7 : SimpleGraph (Fin 7)`, the strong power
  `C7pow n`, `confusable_iff_C7conf`, `indepPair_imp_not_adj`, and the assembly
  `isNIndepSet_of_cert` (a valid `decide`-checked list cert ⇒ `IsNIndepSet` in `C7pow n`).
- `C9Cert367.lean` — the explicit 367-codeword set `S367` (verbatim from the [PS2018]
  Appendix), the kernel `decide` certificate `S367_indep`, the applied soundness
  `alpha_C7pow5_ge_367 : (C7pow 5).IsNIndepSet 367 …`, the rpow comparison `rpow_367_gt`
  (`367^(1/5) > 3.2578`), and the bridge theorems `theta_C7_ge_baseline` /
  `theta_C7_gt_3_2578` (under the named hypothesis `ThetaGeFromIndep`).

## How to re-establish (reviewer)

```
cd lean
PATH="$HOME/.elan/bin:$PATH" lake build Constants.C9Cert367   # ~77s, builds clean
```

Axiom audit (must show no `sorryAx`, no `Lean.ofReduceBool`/`native_decide`):

```
PATH="$HOME/.elan/bin:$PATH" lake env lean <<'EOF'
import Constants.C9Cert367
open C9
#print axioms S367_indep            -- "does not depend on any axioms"
#print axioms alpha_C7pow5_ge_367    -- [propext, Classical.choice, Quot.sound]
#print axioms theta_C7_gt_3_2578     -- [propext, Classical.choice, Quot.sound]
EOF
```

Observed axiom footprint:
- `S367_indep` : **no axioms** (pure kernel `decide`, C(367,2)=67,161 pairs, ~77s, NO `native_decide`).
- `alpha_C7pow5_ge_367`, `theta_C7_ge_baseline`, `theta_C7_gt_3_2578`, `isNIndepSet_of_cert`,
  `rpow_367_gt` : `[propext, Classical.choice, Quot.sound]` only.
- `indepPair_imp_not_adj`, `allPairsIndep_iff`, `confusable_iff_C7conf` : `[propext, Quot.sound]`.

No `sorry`, no `native_decide`, no added axioms anywhere on the load-bearing path.

## Independent Python cross-check

`verify_367.py` — parses the same 367 words and re-checks pairwise independence under the
C_7^⊠5 confusability relation (0 confusable pairs, 367 distinct words). Re-run:

```
python3 constants/9a/certificate/verify_367.py
```

The Lean `S367` list is byte-identical to the list this script verifies (checked).

## Trust boundary (honest)

The Shannon-capacity supremum step `α(C_7^⊠n) ≥ N → Θ(C_7) ≥ N^(1/n)` is carried as the
explicitly-named hypothesis `ThetaGeFromIndep` (Mathlib has no `Θ`), the analogue of the
5b `MTThm15` boundary — visible in the theorem signature, NOT smuggled as an axiom. The
graph-theoretic content (confusability matches the actual `SimpleGraph` adjacency, the
cert is a genuine independent set, `α ≥ 367`) and the rpow comparison are FULLY formalized
with no `sorry`.

## Source

[PS2018] Sven Polak, Alexander Schrijver, "New lower bound on the Shannon capacity of C_7
from circular graphs", IPL 143 (2019), 37–40, arXiv:1808.07438. The 367-set is the set R
of Section 3, listed explicitly in the Appendix. PDF:
`constants/9a/literature/pdfs/ps2018.pdf`.

NOTE on the orbit-reduction angle: the [PS2018] 367-set R is NOT a clean single Z_382
orbit — it is `M ∪ I` where M (327 words) is the floored/translated orbit image with
conflicting words removed, and I (40 words) is a separately-computed extension (paper
Section 3, steps (i)–(v)). Hence the cyclic-orbit reduction does NOT apply to R, and is
unnecessary: plain kernel `decide` on the full C(367,2) check is tractable (~77s) with the
short-circuiting `List` encoding. The orbit reduction remains a registered angle for any
future genuinely-orbit-structured construction.
