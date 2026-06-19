# C_9 = Θ(C_7) — tracking file

## Status
none

(Reviewer sets `improved` only on a verified record-beat. This round REPRODUCES the record
as a machine-checked Lean certificate — it does NOT beat it.)

## Bounds
table: 3.2578 (= 367^(1/5), verified record lower bound, [PS2018], 367-elem indep set in C_7^⊠5) · held: 3.2578 (= 367^(1/5)) — EQUALS the record, NOT a beat; the value WE have now independently Lean-verified (machine-checked, axiom-clean) via the C_7^⊠n cert engine, gap to record 0 (we match, do not exceed). Movable target = LOWER bound; a beat needs α(C_7^⊠5) ≥ 368 (368^(1/5) ≈ 3.25964) or α(C_7^⊠4) ≥ 113 (≈ 3.26039). Upper bound ϑ(C_7) ≈ 3.3177 [L1979].

## Progress log
- R13 (pivot to 9a; effectively round 1): VERIFIED the Lean cert-engine + 367-baseline
  (slug lean-cert-engine-and-367-baseline). Whole-tree `lake build` PASS (8573 jobs,
  Lean+Mathlib v4.31.0); `lean/Constants/{C9,C9Graph,C9Cert367}.lean`. Load-bearing fact
  `S367_indep : allPairsIndep S367 = true` proven by PURE kernel `decide` over C(367,2)=67,161
  pairs — `#print axioms` shows it DEPENDS ON NO AXIOMS (no `native_decide`/`ofReduceBool`/
  `sorryAx`). Reviewer INDEPENDENTLY re-derived the independence in Python directly from the
  Lean `S367` source list: 0/67,161 confusable pairs, 367 distinct length-5 words in [0,6].
  Graph faithfulness verified: `C7` is the genuine 7-cycle (each vertex degree 2; 0~1,0~6
  adjacent, 0~2,0~3 not), `confusable_iff_C7conf` ties the Bool predicate to the actual
  adjacency-or-equality, `C7pow n` is the correct strong-power adjacency, and
  `isNIndepSet_of_cert` soundly bridges a valid decide-checked list cert to a genuine
  `IsNIndepSet` in `C7pow 5` ⇒ α(C_7^⊠5) ≥ 367. `rpow_367_gt : 367^(1/5) > 3.2578` proven in
  Lean (and confirmed < 3.26, honestly inside the gap, NOT reaching the 368-threshold). The
  Shannon-capacity sup step `α(C_7^⊠n) ≥ N → Θ ≥ N^(1/n)` is carried as the explicitly-named
  bridge hypothesis `ThetaGeFromIndep` (Mathlib has no Θ) — an honest, standard named boundary
  carrying only the trivial sup ≥ member step; the hard combinatorial step is fully formalized.
  All load-bearing lemmas axiom-clean ([propext,Classical.choice,Quot.sound] at most; the
  decide is axiom-free). REPRODUCES 3.2578, NO bound move. constants/9a.md untouched. Cert:
  constants/9a/certificate/README.md.
