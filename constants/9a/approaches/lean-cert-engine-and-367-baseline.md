# lean-cert-engine-and-367-baseline

## Idea

Formalize the `C_7^⊠n` independent-set list-certificate engine in Lean and Lean-verify the
existing record 367-set in `C_7^⊠5`, reproducing the verified lower bound
`367^(1/5) ≈ 3.2578` [PS2018] as a search-immune, machine-checked certificate. This is the
machinery foundation every future beat (368+ in `C_7^⊠5`, 113+ in `C_7^⊠4`, …) rides on —
NOT a bound move.

## Status — BUILT, axiom-clean, `lake build`-verified (R13, this builder)

The full engine + graph bridge + verified 367 certificate type-checks and is axiom-audited.

### What type-checks (all in `lean/Constants/`)

- **Engine** (`C9.lean`): `cdist` (cyclic distance on ℕ mod 7), `confusable` (≤1),
  `indepPair` (some coord cyclic-dist ≥2, short-circuiting `List.any` over `zip`),
  `allPairsIndep : List (List ℕ) → Bool` (structural-recursion pairwise, short-circuits),
  and `allPairsIndep_iff` (matches `List.Pairwise`). No `Finset.powerset` — the OOM route
  is avoided exactly per the 5b lesson.
- **Graph bridge** (`C9Graph.lean`): `C7 : SimpleGraph (Fin 7)` (the genuine 7-cycle), the
  `n`-fold strong power `C7pow n`, `confusable_iff_C7conf` (the Bool predicate matches the
  actual graph adjacency-or-equality), `indepPair_imp_not_adj` (an indep pair ⇒ NON-adjacent
  in `C7pow n`), and the assembly `isNIndepSet_of_cert` (a valid `decide`-checked list cert
  of distinct length-`n` entries-`<7` words ⇒ a genuine `IsNIndepSet S.length` in `C7pow n`,
  via injectivity of the word→vector reader on valid words).
- **Verified 367 set** (`C9Cert367.lean`): `S367` = the explicit 367 codewords transcribed
  verbatim from the [PS2018] Appendix; `S367_indep : allPairsIndep S367 = true` by plain
  kernel `decide` (C(367,2)=67,161 pairs, ~77 s, **no axioms, no native_decide**);
  `alpha_C7pow5_ge_367 : (C7pow 5).IsNIndepSet 367 …` (so `α(C_7^⊠5) ≥ 367`); `rpow_367_gt`
  (`367^(1/5) > 3.2578`, fully proven); and `theta_C7_ge_baseline` / `theta_C7_gt_3_2578`
  (under the named bridge hypothesis `ThetaGeFromIndep`).

### Axiom footprint (audited via `#print axioms`)

- `S367_indep`: **does not depend on any axioms** (pure `decide`).
- `alpha_C7pow5_ge_367`, `isNIndepSet_of_cert`, `rpow_367_gt`, `theta_C7_*`:
  `[propext, Classical.choice, Quot.sound]` only.
- `indepPair_imp_not_adj`, `allPairsIndep_iff`, `confusable_iff_C7conf`: `[propext, Quot.sound]`.
- No `sorryAx`, no `Lean.ofReduceBool` (native_decide), no added axiom anywhere.

### Value claimed (CLAIM, pending reviewer verification)

Machine-checked (Lean) **lower bound baseline `Θ(C_7) ≥ 367^(1/5) > 3.2578`**, conditional
only on the explicitly-named Shannon-capacity bridge `ThetaGeFromIndep` (the honest trust
boundary; Mathlib has no `Θ`). Table value to beat: `367^(1/5) ≈ 3.2578` [PS2018].
**This REPRODUCES the record — it does NOT beat it.** `constants/9a.md` and `current.md`
left untouched (no improved value written).

## The 367-set is NOT a clean orbit (orbit-reduction folded-in finding)

The reviewer flagged, and the [PS2018] paper (Section 3, verified from the PDF) confirms:
the 367-set R is `M ∪ I`, where M (327 words) is the floored/translated Z_382 orbit image
with conflicting words removed (steps (i)–(iv): add (40,123,40,123,40) mod 382, map each
letter `i ↦ ⌊i/54.5⌋` into Z_7, delete words confusable with another), and I (40 words) is
a separately Gurobi-computed extension (step (v)). So R is NOT a single cyclic orbit, and
the orbit-reduction `C(N,2) → N−1` accelerator does **not** apply to R. It proved
**unnecessary**: plain kernel `decide` on the full C(367,2) check is tractable (~77 s) with
the short-circuiting `List` encoding. The orbit reduction stays a registered angle for any
future genuinely-orbit-structured construction (e.g. a fresh single-orbit beat attempt).

## How to push it further

- **The bound MOVE (separate live angles, not this slug):**
  - `symmetry-guided-search-c7-5-368`: find α(C_7^⊠5) ≥ 368 (richer multi-orbit ansatz /
    local search seeded from the 367 set). Hard, static since 2018. Any survivor is
    certified by THIS engine in ~minutes (`S368_indep := by decide` + `isNIndepSet_of_cert`).
  - `c7-4-improvement-113`: push α(C_7^⊠4) from 108 toward 113 (smallest space, 2401 verts);
    feasibility uncertain. Same engine certifies (set `n := 4`).
- **Tighten the trust boundary:** the only non-formalized link is `ThetaGeFromIndep`. A full
  Mathlib formalization of `Θ(G) = sup_n α(G^⊠n)^(1/n)` (define the strong product `⊠`, the
  independence number as a `sSup` over the finite vertex set, prove rpow-monotonicity of the
  sup) would discharge it and make the baseline fully axiom-boundary-free. Substantial but
  pure machinery; a good next-round increment if staying on the foundation.
- **Generalize the engine** to certify in `C_7^⊠6` (1196+ target) — the engine is already
  `n`-generic; only the explicit word list and the `decide` cost change.

## Certificate

`constants/9a/certificate/README.md` (build target, axiom audit, reproduction steps),
`constants/9a/certificate/verify_367.py` (independent Python cross-check, byte-identical
word list). Build target: `lake build Constants.C9Cert367`.
