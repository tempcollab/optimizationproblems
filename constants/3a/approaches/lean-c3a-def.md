# Sketch `lean-c3a-def` — scoped Lean DEFINITION of C_3a (de-risk the bridge)

## Strategy
The self-contained machine-checked Lean theorem `C_3a > 1.1771` has, per the R12 explorer, exactly
ONE uncached blocker: `C3aReal` is currently `opaque` in `lean-native-decide-smallmt`, so the
read-off `θ ≤ C3aReal` can only be an ASSUMED hypothesis (`ghr`). Everything else is already a
Lean theorem: the integer core (`native_decide`, θ>1.1771, hole-free), the log-algebra half
(`log-bridge`, cached), and the finite/counting half of the limit (`tensor-multiplicativity`,
cached).

This sketch is **definition-only and deliberately proves NO new bound**. It replaces the opaque
constant with a CONCRETE `sSup`-over-a-predicate definition `C3aRealDef`, and exposes the read-off
as named holes so the **reviewer can rule the definitional approach in/out cheaply** before the run
commits multiple rounds to the real-analysis read-off.

Borrows: `lean-native-decide-smallmt` (`theta`, `theta_gt` — the certified θ>1.1771), the cached
`tensor-multiplicativity` lemmas (`sumset`/`diffset`, `tensor_pow_*_card`), `log-bridge`.

## R21 BUILDER — `realizes_one` CLOSED sorry-free (the MAIN angle, fully discharged)

This round CLOSED the entire MAIN angle: the two load-bearing interval-cardinality lemmas
R1a/R1b AND all three `realizes_one` clause sub-goals, so `realizes_one : Realizes 1` and
`realizableSet_nonempty` are now sorry-FREE and axiom-clean. `lake build C3a` EXIT 0 (2970 jobs).

### Closed this round (6 lemmas, all `#print axioms = [propext, Classical.choice, Quot.sound]`, NO sorryAx)
- **`icc_setSum_eq`** (helper) — `setSum (Icc 0 n)(Icc 0 n) = Icc 0 (2n)` for `0 ≤ n`. The `⊇`
  half writes `z ∈ [0,2n]` as `min z n + (z − min z n)`, both summands in `[0,n]`; `Finset.ext` +
  `mem_image₂` + `mem_Icc` + `omega` on each membership. Pure finite ℤ-interval combinatorics.
- **`icc_setSum_card` (SUB-HOLE R1a)** — `|Icc 0 n + Icc 0 n| = (2n+1).toNat`. `rw [icc_setSum_eq,
  Int.card_Icc]; congr 1; omega` (`Int.card_Icc : #(Icc a b) = (b+1−a).toNat`, here `(2n+1−0).toNat`).
- **`icc_setDiff_eq`** (helper) — `setDiff (Icc 0 n)(Icc 0 n) = Icc (-n) n`. The `⊇` half writes
  `z ∈ [-n,n]` as `max z 0 − max (-z) 0`, both in `[0,n]`; same `Finset.ext`+`omega` shape.
- **`icc_setDiff_card` (SUB-HOLE R1b)** — `|Icc 0 n − Icc 0 n| = (2n+1).toNat`. Via `icc_setDiff_eq`
  + `Int.card_Icc` (`(n+1−(−n)).toNat = (2n+1).toNat`).
- **`icc_card`** (helper) — `|Icc 0 (n:ℤ)| = n+1` for `n : ℕ`, via `Int.card_Icc` + `omega`.
- **`realizes_one : Realizes 1`** (three clause sub-goals, all discharged) — witness
  `A n = B n = Finset.Icc 0 (n:ℤ)`, `K = 3`:
  * card→∞: rewrote `|A n| = (n:ℝ)+1` (via `icc_card` + `push_cast`), then
    `Filter.tendsto_atTop_add_const_right` ∘ `tendsto_natCast_atTop_atTop`.
  * clause (i): `filter_upwards`; `icc_setSum_card`+`icc_card` give `(2n+1).toNat ≤ 3·(n+1)`;
    `(2*(n:ℤ)+1).toNat = 2n+1` by `omega`, then `push_cast` + `nlinarith [Nat.cast_nonneg n]`
    (`2n+1 ≤ 3n+3` for `n ≥ 0`).
  * clause (ii): `filter_upwards`; `icc_setSum_card`/`icc_setDiff_card` give both cards `= (2n+1).toNat`;
    `Real.rpow_one` reduces `(·)^(1:ℝ)` and the goal closes by reflexivity (equality, not strict).
- **`realizableSet_nonempty`** — now sorry-free (it was already `⟨1, realizes_one⟩`; closes with
  `realizes_one`).

`#print axioms` confirmed all six are `[propext, Classical.choice, Quot.sound]` — NO `sorryAx`,
no `native_decide`, no `admit`/`axiom`. The two general interval helpers (`icc_setSum_eq`,
`icc_setDiff_eq`) are reusable (see Promotable below).

### Remaining holes (4 `sorry`, all multi-round real analysis — NOT gated this round)
- `ghr_upper` (line ~234) — the GHR2007 Thm-2 `4/3` structural cap (`realizableSet_bddAbove` is
  already reassembled sorry-free AROUND it: `⟨4/3, fun _ hc => ghr_upper hc⟩`). Mathlib lacks this
  specific bound; multi-round, deferred.
- B2 `griego_bounded_doubling` (~805), B3 `griego_diff_lower_bound` (~814), B4
  `griego_card_tendsto` (~822) — the floor-dilution doubling / θ-reconciliation / atTop packaging
  real-analysis residue. Untouched, as dispatched.

### Note on the claim (unchanged)
This is the CERT-PATH structural advance the outliner/reviewer described, NOT a held raise. Even
fully wired the bridge certifies θ>1.1771 < held 1.1781. `realizes_one` closing means `C3aRealDef`
is now provably NON-VACUOUS (`RealizableSet ≠ ∅`, so `sSup` is over a nonempty bounded-once-`ghr_upper`-
closes set) with the nonemptiness no longer a hole — a genuine structural step toward the
self-contained machine-checked C_3a bound, but the held NUMBER stays 1.1781.

### Promotable lemmas (R21, for reviewer to certify into `lemmas/`)
- `icc_setSum_eq` (C3aDef.lean ~L157) — `0 ≤ n → setSum (Icc 0 n)(Icc 0 n) = Icc 0 (2n)`. General
  ℤ-interval sumset identity. Axiom-clean `[propext, Classical.choice, Quot.sound]`, NO sorryAx.
- `icc_setDiff_eq` (C3aDef.lean ~L181) — `0 ≤ n → setDiff (Icc 0 n)(Icc 0 n) = Icc (-n) n`. General
  ℤ-interval diffset identity. Axiom-clean, NO sorryAx.
  Both are reusable (independent of all witness data) for any growing-interval realizability witness.

## R21 — DECOMPOSITION PLAN for `realizes_one` (main) + `realizableSet_bddAbove` (isolated)

The finite/discrete B1 layer is DONE+verified sorryAx-free (R20). The 5 remaining holes are all
hard real analysis. R21 attacks the two MOST SELF-CONTAINED of them, decomposed into named
sub-holes (the proven B1/an_separated playbook), keeping `lake build C3a` EXIT 0 (verified: 2970
jobs, no errors). Sub-hole line numbers are post-edit and current.

### Main angle — `realizes_one` (line 173) via the GROWING INTERVAL family (most likely actual closure)
Witness: `A n := B n := Finset.Icc (0:ℤ) n`. For this family all three `Realizes` clauses are
finite/algebraic:
  * `setSum (Icc 0 n)(Icc 0 n) = Icc 0 (2n)`,  card `= 2n+1`;
  * `setDiff (Icc 0 n)(Icc 0 n) = Icc (-n) n`,  card `= 2n+1`;
  * `|A n| = |Icc 0 n| = n+1`.
So clause (i) `2n+1 ≤ 3·(n+1)` holds with `K = 3`; clause (ii) `(2n+1)^1 = 2n+1 ≤ 2n+1` is
equality; `|A n| = n+1 → ∞`. This is the explorer's "fully Lean-fit, plausibly fully closable in
one round" candidate.

**Named sub-holes (the only `sorry` content of this angle):**
- **R1a `icc_setSum_card` (line 157)** — `|Icc 0 n + Icc 0 n| = 2n+1` for `0 ≤ n`. THE LOAD-BEARING
  finite step. Prove `setSum (Icc 0 n)(Icc 0 n) = Icc 0 (2n)` by `Finset.ext` + `mem_image₂` +
  `mem_Icc` (the `⊇` direction writes `z ∈ [0,2n]` as `min z n + (z − min z n)`, both parts in
  `[0,n]`), then `Nat.card_Icc` for the count. Stated returning `(2*n+1).toNat` to keep the card a
  `ℕ`.
- **R1b `icc_setDiff_card` (line 165)** — `|Icc 0 n − Icc 0 n| = 2n+1` for `0 ≤ n`. Same shape:
  `setDiff (Icc 0 n)(Icc 0 n) = Icc (-n) n` (`z ∈ [-n,n]` is `a − b`, `a = max z 0`, `b = max (-z) 0`).
- **`realizes_one` body (line 173)** — three small `sorry` sub-goals (card→∞ via `Nat.card_Icc` +
  `tendsto_atTop`; clause (i) `2n+1 ≤ 3(n+1)` via the two card lemmas + `omega`/`push_cast`; clause
  (ii) `rpow_one` + the card equality). These wire R1a/R1b into the predicate; once R1a/R1b close
  they are pure plumbing. (Builder may collapse `realizes_one` to one assembly once R1a/R1b land.)

**Hard step:** R1a `icc_setSum_card` — the interval-sumset identity `setSum (Icc 0 n)(Icc 0 n) =
Icc 0 (2n)`. Pure finite ℤ-interval combinatorics, no continuum, no construction — Lean-fit. The
`⊇` direction (every point of `[0,2n]` is a representable sum) is the only non-trivial half.

### Alternative angle (same file, also green) — `realizableSet_bddAbove` (line 198), `ghr_upper` ISOLATED
`realizableSet_bddAbove` is now REASSEMBLED `sorry`-free as `⟨4/3, fun _ hc => ghr_upper hc⟩`. ALL
the hardness is isolated into the single documented sub-hole:
- **`ghr_upper` (line 191)** — `Realizes c → c ≤ 4/3`, the [GHR2007, Theorem 2] structural upper
  bound `|A−B| ≤ |A+B|^{4/3+o(1)}` under bounded doubling. Mathlib has Plünnecke–Ruzsa
  (`Mathlib.Combinatorics.Additive.PluenneckeRuzsa`) but NOT this specific GHR bound — a substantial
  multi-round formalization. Left as ONE clearly-named `sorry`; the structural `BddAbove` plumbing is
  closed around it. This angle is a structural advance (Elo lift, plumbing closed) even though
  `ghr_upper` itself is hard real analysis — it isolates the irreducible core, matching Route A of
  the explorer's decomposition.

**Recommendation to the builder:** attack R1a/R1b/`realizes_one` first (the genuinely closable
interval angle) — a HOLE actually closed this round. `ghr_upper`/`realizableSet_bddAbove` is already
structurally advanced (plumbing closed, hard core isolated) by this edit; it needs no further work
unless `ghr_upper` is attempted. Per R19/R20 lesson: STOP and report the moment R1a/R1b + `realizes_one`
are green — do NOT run trailing rebuild/verification passes.

## R19 — numeric witness-data holes CLOSED → the entire finite B1 layer is now sorryAx-FREE

**Closed this round (7 witness-data holes at C3aDef.lean:302–324, all in the finite B1 layer):**
- `Ubase : Finset ℤ := {0, 2, 3, 4, 5, 6, 7, 8, 9, 10}` — the Griego per-column 10-element digit set
  (drop digit `1`, max digit 10), the verified-held base alphabet.
- `Qbase : ℤ := 41` — **NOT 21.** This is the load-bearing finding (verified by the outliner AND the
  outline-reviewer). The cached `CarryFree Q U := 0 < Q ∧ ∀ a b ∈ U, 2·|a+b| < Q ∧ 2·|a−b| < Q`
  (TensorMultiplicativity.lean:95–96) requires BOTH conjuncts. For max digit 10, max `|a+b| = 20`, so
  the sum conjunct needs `2·20 = 40 < Q` ⟹ Q ≥ 41. Q=21 FAILS at a=b=10 (`2·|10+10| = 40 ≮ 21`) — a
  FALSE predicate that `decide` cannot discharge. The held Python cert's `b=21 = 2·max+1` is correct
  for ITS single-column digit-packing injectivity (carries never cross columns, only `|a−b| < Q`
  matters per column); the cached Lean chain proves a STRONGER box-injectivity that also needs sums
  in-digit, hence `Q = 41`. Every downstream structural lemma is parametric in `Qbase`, so 21→41 breaks
  nothing in the B1 scaffolding; only the deferred B3 numeric tie-in of the tensor sumset/diffset to
  `theta` cares (B3 is multi-round real analysis, untouched).
- `Ubase_carryfree : CarryFree Qbase Ubase` — discharged `⟨by decide, by decide⟩` over the 10-element
  set (≤100 pairs, tiny integers). **`#print axioms` = `[propext, Quot.sound]` — fully axiom-clean, NO
  sorryAx, NO native_decide.** (`decide`, not `native_decide` — operands tiny, kernel-checked.)
- `maxUbase : ℤ := 10`; `Ubase_range : 0 ≤ maxUbase ∧ ∀ u ∈ Ubase, 0 ≤ u ∧ u ≤ maxUbase` — discharged
  `⟨by decide, by decide⟩`. **`#print axioms` = `[propext, Quot.sound]` — axiom-clean, NO sorryAx.**
- `mnData : ℕ → ℕ := fun _ => 1` and `negLoData : ℕ → ℤ := fun n => -(2 * maxbk maxUbase Qbase n + 1)`
  — type-correct CLOSED forms consumed only by SHAPE downstream (`an_separated`/`interval_union_disjoint_*`
  are proved parametrically). The NUMERIC dilution content (`mₙ = ⌊qⁿ/sⁿ⌋`, real band bottom) stays
  deferred to B2/B3 — pinned the shape ONLY, proved no inequality about these values (that is B2/B3).

**Effect — last sorryAx source removed from the finite B1 layer.** With the witness data pinned, the
B1-layer lemmas that previously traced their sorryAx ONLY to these witness sorries are now FULLY
axiom-clean (verified via a throwaway `AxCheck.lean` `#print axioms`, deleted after):
- `an_separated` — `[propext, Classical.choice, Quot.sound]` — **NO sorryAx.**
- `griego_ak_disjoint` (B1a) — `[propext, Classical.choice, Quot.sound]` — **NO sorryAx.**
- `griego_disjoint_union_count` (B1) — `[propext, Classical.choice, Quot.sound]` — **NO sorryAx.**

The entire finite/discrete B1 layer (tensor-multiplicativity → tpow_elem_range → an_separated →
griego_ak_disjoint → griego_disjoint_union_count) is now sorryAx-free. `lake build C3a` EXIT 0 (2970
jobs). The 5 remaining `sorry` are exactly the multi-round real-analysis residue: `realizes_one` (140),
`realizableSet_bddAbove` (151), B2 `griego_bounded_doubling` (717), B3 `griego_diff_lower_bound` (726),
B4 `griego_card_tendsto` (733).

**Held NOT affected.** This is a structural advance, not a held raise. Even fully wired the bridge
certifies θ>1.1771 (the native_decide core's m=140 literal) < held 1.1781. The top-level
`c3a_lower_bound_def : (11771:ℝ)/10000 < C3aRealDef` and `C3aRealDef`/the native_decide integer core
are UNTOUCHED (git diff confirms only the witness-data block changed, 26 ins / 17 del in C3aDef.lean).

**Parse fix:** removed two stale `/-- … -/` doc-comment blocks that were left orphaned above the
witness defs (two stacked doc comments before a decl is a parse error in Lean 4.31).

**Remaining holes / blockers** (all multi-round real analysis — do NOT gate a round on them):
- B2 `griego_bounded_doubling` (717): ∃ fixed K, |A+B| ≤ K·|A| eventually — floor-dilution real
  arithmetic over mₙ, Lₙ, sⁿ, qⁿ (where mnData/negLoData must BE the real Griego counts and satisfy an
  inequality — genuine analysis, not a finite check).
- B3 `griego_diff_lower_bound` (726): |A+B|^θ ≤ |A−B| eventually — chains cached `log_bridge`, but
  needs the tensor-limit identification of θ with log(D/S)/log Q; this is where Ubase's sumset/diffset
  ties to `theta`. Real analysis.
- B4 `griego_card_tendsto` (733): |A|→∞, Filter.atTop packaging — hardest.
- `realizes_one` (140), `realizableSet_bddAbove` (151): needs the GHR2007 4/3 upper-bound theorem.

**Promotable lemmas:** none new this round. `Ubase_carryfree`/`Ubase_range` are axiom-clean but are
SKETCH-SPECIFIC witness data (about the concrete Ubase/Qbase/maxUbase defs), not reusable general
lemmas, so they are not cache candidates. (`box_elem_range`/`maxbk_nonneg` already promoted R18.)

## R18 — `an_separated` CLOSED (the residual construction obligation of B1a)

**Closed this round (3 R18 holes, sorry-free on their own path):**
- `box_elem_range` — the `box`/`emb` step element-range bound (`U⊆[0,maxU] ∧ V⊆[0,maxV] ∧ 0≤Q ⟹
  box Q U V ⊆ [0, maxU+Q·maxV]`). **Axiom-clean `[propext, Classical.choice, Quot.sound]`, NO sorryAx
  — fully general, PROMOTABLE.**
- `tpow_elem_range` — the induction on the `tpow` recursion (`tpow Qbase Ubase n ⊆ [0, maxbk maxU
  Qbase n]`), carrying the base bound `hbase` parametrically. Mirrors `tensor_pow_sumset_card`.
  `[propext, sorryAx, …]` where sorryAx traces ONLY to the witness-data sorries (`Ubase`/`Qbase`).
- `an_separated` — assembled from the above plus the helpers `setSum_bk_within`/`setDiff_bk_within`
  (WithinDiam windows `[0,2·maxbk]` / `[−maxbk,maxbk]`), `an_shift_spacing` (AP gap `|i−j|·(2·maxbk+1)
  > 2·maxbk`), `an_shift_nonneg`, and `interval_union_disjoint_sum`/`_diff` (interval band placed
  strictly below all translate windows). Proof TERM sorry-free; sorryAx via documented witness data
  only. `griego_ak_disjoint` (B1a) is now fully reassembled from `an_separated` + the cached spacing
  lemmas → B1a→B1 is a sorry-free chain modulo numeric data.

**Witness-data shapes PINNED this round** (only the numeric counts stay `sorry`): the AP
`an_shift n i = i·(2·maxbk maxUbase Qbase n + 1)`, `an_index n = range (mnData n)`,
`an_interval n = Icc (negLoData n) (−(2·maxbk n + 1))` (band below all translates). New documented
witness sorries added for the numeric data: `maxUbase : ℤ`, `Ubase_range : 0≤maxUbase ∧ Ubase⊆
[0,maxUbase]`, `mnData : ℕ→ℕ`, `negLoData : ℕ→ℤ`. The `maxbk` closed-form def moved up before the
witness block (single def; the later duplicate removed).

**Intermediate-statement note (mine):** `tpow_elem_range`'s `hmaxU : 0 ≤ maxU` hypothesis turned out
unnecessary for the bound itself (the base case only needs `hbase`, the step only needs `0 ≤ Qbase`),
so it was dropped — `maxbk_nonneg` (which DOES need `0≤maxU`) is a separate helper used by the
spacing lemma. This is a faithful tightening, not a weakening: the conclusion is unchanged.

**Build:** `lake build C3a` EXIT 0, 2970 jobs. `#print axioms`: `box_elem_range`/`maxbk_nonneg` clean;
all other R18 lemmas + `an_separated` show sorryAx tracing ONLY to documented witness data. No
native_decide/admit/axiom smuggled (grep-clean). Top-level `c3a_lower_bound_def` and `C3aRealDef :=
sSup RealizableSet` UNTOUCHED.

**Remaining holes (next gaps):** witness data `Ubase`/`Qbase`/`Ubase_carryfree`/`maxUbase`/
`Ubase_range`/`mnData`/`negLoData` (numeric — the explicit Griego digit set + dilution counts; a
finite check once pinned, but large); B2 `griego_bounded_doubling` (floor-dilution doubling algebra),
B3 `griego_diff_lower_bound` (log-bridge θ reconciliation), B4 `griego_card_tendsto` (Filter.atTop
sup packaging); `realizes_one`, `realizableSet_bddAbove` (4/3 cap). B2/B3/B4 are the multi-round
real-analysis residue — do NOT gate a round on them.

**Claimed value (clearly a CLAIM until hole-free):** still θ>1.1771 (the native_decide integer-core
literals), NOT held 1.1781. This round advances the CERT PATH structurally; it does not move the held
number. Even fully wired the bridge certifies 1.1771, which is BELOW the verified held 1.1781 — so
this is not a held-raiser, it is the path to a self-contained machine-checked C_3a bound.

**Promotable lemmas:** `box_elem_range`, `maxbk_nonneg` (both axiom-clean general — see Promotable
line at the very bottom).

## R12 — FAITHFULNESS FIX (this round's deliverable)

The R12 outline-reviewer's load-bearing finding: the R11 draft predicate **dropped the doubling
clause `|A+B| ≪ |A|`** and used `A = B` single-family witnesses. Dropping a constraint enlarges the
realizable set, so the sup could EXCEED C_3a — making `c3a_lower_bound_def` a statement about an
inflated, non-faithful constant. This round restores the doubling clause in the right asymptotic
sense and switches to the faithful two-set form, verified against the [GHR2007] source.

### The exact [GHR2007] definition (verified against the PDF, R12)
Extracted `https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf` with `pdfminer` (saved nowhere
binary — text only). The constant is **inequality (5) / Theorem 1** (PDF text lines 520–600,
640–720):

> Theorem 1. Let K > 1 be a real number. There exist a real number θ₀ > 1.14465 and two sets of
> integers A and B **arbitrarily large** such that `|A+B| ≤ K|A|` (7) and `|A−B| ≥ (2(K−1)/3K)^{5/4} |A+B|^{θ₀}`.
>
> (5):  `|A| = n`, `|A+B| ≤ K|A|`  and  `|A−B| ≥ c(K)|A+B|^θ`,  where `c(K) > 0`.

So, exactly:

    C_3a = sup { θ : ∃ K > 1, ∃ c(K) > 0, arbitrarily large finite (A,B) with
                 (i)  |A+B| ≤ K·|A|              (the doubling |A+B| ≪ |A|, FIXED K)
                 (ii) |A−B| ≥ c(K)·|A+B|^θ       (cleared |A−B| ≫ |A+B|^θ) }.

BOTH clauses are genuine. K is a **fixed** constant for the witnessing family (independent of the
family index n) — that is the precise sense of `≪`. This is what the R11 draft dropped.

### Why the witness is a TWO-SET composite, NOT the bare tensor power `A=B=U^{⊗k}`
This is the crux the reviewer asked to pin down. The R11 draft's `A = B = U^{⊗k}` **violates clause
(i)**: with `A = B = U^{⊗k}`, `|A+B| = |U+U|^k`, `|A| = |U|^k`, so the doubling ratio is
`(|U+U|/|U|)^k → ∞` — UNBOUNDED, no fixed K works. (Generally `|A+A| ≥ |A|`, so `|A+A| ≤ K|A|` with
fixed K fails for any growing set.) So the bare tensor family is correctly **excluded** by the
restored clause — confirming the clause is load-bearing, not cosmetic.

The actual [GHR2007, Lemma p.4–5] witness realizing `θ = 1 + log(d/s)/log q` (PDF lines 1405–1700)
is the **composite**:

    Bₖ := U^{⊗k}   (the digit-tensor power; |Bₖ| = |U|^k, |Bₖ ± Bₖ| = |U±U|^k = s^k / d^k),
    Aₖ := [1, Lₖ] ∪ ⋃_{i=1}^{mₖ} (aᵢ + Bₖ),   mₖ = ⌊qᵏ/sᵏ⌋,   Lₖ = ⌊3qᵏ/(2(K−1))⌋,

with shifts aᵢ separated (`aᵢ − aⱼ ∉ Bₖ − Bₖ`) so translates + interval are sum/diff-disjoint.
GHR compute `|Aₖ + Bₖ| = mₖ·sᵏ + t`, `|Aₖ − Bₖ| = mₖ·dᵏ + t`, `t = |[1,Lₖ]+Bₖ|`, and with
`mₖ ≈ qᵏ/sᵏ`, `Lₖ ≈ qᵏ/(K−1)` the doubling is DILUTED to the FIXED bound `|Aₖ+Bₖ| ≤ K|Aₖ|`
(clause (i) HOLDS) while `|Aₖ−Bₖ| ≥ (qd/s)^k ≥ c(K)·|Aₖ+Bₖ|^θ` (clause (ii)). The cached
`tensor_pow_*_card` lemmas supply exactly the Bₖ-cardinalities the computation rests on; the
dilution wrapper (m translates + interval) is the additional combinatorics — the genuine remaining
content of HOLE B `griego_realizes`.

**Conclusion:** with the doubling clause restored and the witness understood as the GHR composite,
(a) `RealizableSet ⊆ {registry-realizable}` ⟹ `C3aRealDef ≤ C_3a` (the SAFE direction for a lower
bound), (b) the 4/3 structural cap applies honestly, and (c) the Griego family IS a member (via the
composite, not the bare tensor), so the definition is non-vacuous and the held bound flows through
it. Both R12-reviewer objections (dropped doubling; A=B collapse) are dissolved.

## The definition now on the table (corrected)
```lean
def setSum (A B : Finset ℤ) : Finset ℤ := Finset.image₂ (· + ·) A B
def setDiff (A B : Finset ℤ) : Finset ℤ := Finset.image₂ (· - ·) A B

def Realizes (c : ℝ) : Prop :=
  ∃ A B : ℕ → Finset ℤ, ∃ K : ℝ,
    Filter.Tendsto (fun n => ((A n).card : ℝ)) Filter.atTop Filter.atTop ∧
    (∀ᶠ n in Filter.atTop, ((setSum (A n) (B n)).card : ℝ) ≤ K * ((A n).card : ℝ)) ∧   -- clause (i)
    (∀ᶠ n in Filter.atTop,
      ((setSum (A n) (B n)).card : ℝ) ^ c ≤ ((setDiff (A n) (B n)).card : ℝ))            -- clause (ii)

noncomputable def C3aRealDef : ℝ := sSup { c | Realizes c }
```
- Two sets `A n, B n` (matches the registry's two-set form, removes the A=B-collapse worry).
- Clause (i): a SINGLE fixed `K` (`∃ K`, outside the `∀ᶠ n`) bounds `|A n + B n| ≤ K|A n|` eventually
  — the bounded-doubling `≪` in the right asymptotic sense.
- Clause (ii): the cleared `≫` (constant c(K) absorbed into "eventually").

## Holes (all documented `sorry`, build GREEN — `lake build C3a` EXIT 0, 2970 jobs)
Exactly 3 `sorry` (warnings at `C3aDef.lean:139,150,169`):
- `realizes_one : Realizes 1` — nonemptiness witness. Needs a concrete bounded-doubling family with
  `|A−B| ≥ |A+B|^1` (the GHR composite at the trivial exponent, or any explicit such family).
  Feeds `realizableSet_nonempty`.
- `realizableSet_bddAbove : BddAbove RealizableSet` — bounded by the [GHR2007, Theorem 2] structural
  cap `4/3` (the proven upper bound), now applicable HONESTLY because the doubling clause is restored
  (the 4/3 bound is proved for the constrained constant). Makes `sSup` a genuine real. Needs the
  GHR2007 upper-bound theorem.
- `griego_realizes : Realizes theta` — **HOLE B, the load-bearing read-off**: the Griego family
  realizes θ via the GHR COMPOSITE witness (Bₖ = U^{⊗k} + the m-translate/interval dilution).
  Uses cached `tensor_pow_*_card` (for the Bₖ cardinalities) + the dilution combinatorics + the
  θ = 1+log(D/S)/log Q reconciliation.

Then (one line each, modulo the holes, no new `sorry`):
- `c3a_ge_theta : theta ≤ C3aRealDef` — `le_csSup realizableSet_bddAbove griego_realizes`.
- `c3a_lower_bound_def : 11771/10000 < C3aRealDef` — `lt_of_lt_of_le theta_gt c3a_ge_theta`.

## `#print axioms` (R12, recorded)
- `c3a_lower_bound_def` → `[propext, sorryAx, Classical.choice, Quot.sound,
  Q_gt_one._native…, S_pos._native…, griego_140_265_int_cert._native…]`. The `sorryAx` is honest —
  it traces ONLY to the 3 declared read-off holes; the `native_decide` axioms are the legitimate
  integer-core ones from `lean-native-decide-smallmt`. **No custom `axiom`, no smuggled hard step.**
- `c3a_ge_theta`, `realizableSet_nonempty` → `[propext, sorryAx, Classical.choice, Quot.sound]`
  (sorryAx via the holes only).

## What this round closed / what remains
- **CLOSED this round (the reviewer's requested fix):** the faithfulness defect. The doubling clause
  `|A+B| ≤ K·|A|` is restored with a fixed K, the predicate is two-set (no A=B collapse), and the
  definition is now provably a faithful UNDER-estimate of C_3a (`C3aRealDef ≤ C_3a`). The Griego
  family's membership route is pinned down concretely (the GHR composite, with the doubling-dilution
  computation spelled out and tied to the cached tensor-power cardinalities). The definition is
  non-vacuous. This was a *definitional* fix — no Lean lemma newly proved beyond keeping the
  assembly green; the deliverable is the corrected, reviewer-rulable definition + faithfulness
  argument.
- **REMAINS (3 holes):** `realizes_one`, `realizableSet_bddAbove`, `griego_realizes` (HOLE B). HOLE
  B is multi-round (the dilution combinatorics + the limit packaging); the other two need the GHR
  upper bound and a baseline witness. None attempted to close this round — this is the scoped
  definition-only de-risking step, as dispatched.

## Claim
NO held raise — this is a definitional de-risking step (explicitly NOT a bound claim). `held` stays
the verified Python value C_3a > 1.1776 (R11). The CLAIM of this sketch is only that the *definition*
is now faithful (a lower-bound under-estimate of the registry C_3a), pending the reviewer's in/out
ruling. When the 3 holes close in later rounds, `c3a_lower_bound_def` becomes a self-contained
machine-checked `C_3a > 1.1771` over the concrete registry definition.

## What would push it further
1. Close `griego_realizes` (HOLE B): formalize the GHR composite Aₖ = [1,Lₖ] ∪ ⋃(aᵢ+Bₖ), prove the
   doubling and the diff-set bounds from the cached `tensor_pow_*_card` + interval/translate counting,
   and package the `k→∞` realization (`Filter.atTop`). Biggest lever; multi-round.
2. Close `realizableSet_bddAbove`: formalize (or assume as a clearly-named hypothesis) the
   [GHR2007, Theorem 2] 4/3 upper bound under bounded doubling.
3. Close `realizes_one`: any explicit bounded-doubling family with `|A−B| ≥ |A+B|` (e.g. an
   arithmetic progression pair) suffices.

## R14 — B1 CLOSED (the finite/combinatorial disjoint-union count)

This round's deliverable: **sub-hole B1 (`griego_disjoint_union_count`) is now proved sorry-FREE**,
together with a reusable, fully-axiom-clean finite combinatorics toolkit. `lake build C3a` EXIT 0
(2970 jobs); `#print axioms` confirms the split below.

### What I closed (sorry-free, `[propext, Classical.choice, Quot.sound]`, NO sorryAx)
The genuine load-bearing finite content of the GHR composite count, added to `C3aDef.lean`:
- `tr`, `setSum_tr`/`setDiff_tr` (sum/diff of a one-coordinate translate = translate of the
  sum/diff — pure ring algebra), `setSum_tr_card`/`setDiff_tr_card` (a translate's sum/diff has the
  SAME cardinality — translation injective);
- `setSum_union`/`setDiff_union`, `setSum_biUnion`/`setDiff_biUnion` (distributivity over `∪`/`biUnion`);
- **`setSum_card_decompose` / `setDiff_card_decompose`** — the GHR additive identity at the
  cardinality level: for pairwise-disjoint translate images + a disjoint interval piece,
  `|(I ∪ ⋃ᵢ(aᵢ+B)) ± B| = mₙ·|B±B| + |I±B|`, via `Finset.card_biUnion` + `card_union_of_disjoint` +
  `setSum/Diff_tr_card`. These two are the reusable heart and are **promotable** (see below).

`#print axioms setSum_card_decompose` / `setDiff_card_decompose` / the four `*_tr_card`/`*_biUnion`
helpers: all `[propext, Classical.choice, Quot.sound]` — sorryAx-free.

### B1 itself — `griego_disjoint_union_count`, proved sorry-free
`#print axioms griego_disjoint_union_count` → `[propext, sorryAx, Classical.choice, Quot.sound]`.
The proof TERM is sorry-free; the `sorryAx` enters ONLY via the explicitly-named hypotheses/data it
consumes (`griego_ak_disjoint` (B1a) + the witness data `Ubase`/`Qbase`/`Ubase_carryfree`/
`an_interval`/`an_index`/`an_shift`). No smuggled axiom; the count derivation is real.

### Two intermediate-statement fixes (my job, recorded)
1. **Exponent `^ n → ^ (n+1)`.** With `bk n = U^{⊗n} = tpow Qbase Ubase n`, the cached
   `tensor_pow_sumset_card` gives `|U±U|^(n+1)` (the `tpow … n` convention has `n+1` factors). The
   planned B1 exponent `^ n` was off by one; the true, provable statement is `^ (n+1)`.
2. **One shared `tₙ` → two witnesses `tsum`, `tdiff`.** GHR's single interval term `t` additionally
   relies on `|I+B| = |I−B|` for the long interval — a SEPARATE finite fact, not part of the
   disjoint-union count. Carrying `tsum = |[1,Lₙ]+Bₙ|` and `tdiff = |[1,Lₙ]−Bₙ|` separately makes B1
   exactly the count the decomposition lemmas prove, with no smuggled interval-symmetry; the
   `tsum = tdiff` reconciliation is deferred to B3.

Also: `bk`/`ak` are no longer opaque `sorry` defs — `bk n := tpow Qbase Ubase n` and
`ak n := an_interval n ∪ (an_index n).biUnion (fun i => tr (an_shift n i) (bk n))` are now PINNED to
the GHR composite shape. This pinning is what made B1 provable; only the disjointness of the pieces
(which needs the separation choice) stays a hole.

### Holes remaining (12 documented `sorry`, all build GREEN)
- **B1a `griego_ak_disjoint` (line 330) — NEW named sub-hole exposed by closing B1.** The pairwise
  disjointness of the `mₙ` translate images + the interval piece, in both sums and diffs. This is the
  genuine *uncached* combinatorial content (GHR's separation `aᵢ−aⱼ ∉ Bₙ−Bₙ`), depending on the
  explicit shift choice. Finite once `an_shift` is pinned, but no cached lemma supplies it. BLOCKER:
  needs an explicit `an_shift`/`an_interval`/`an_index` construction + a range/pigeonhole disjointness
  proof — substantial but strictly finite; the natural next builder target.
- **Witness data (lines 302–311):** `Ubase`/`Qbase`/`Ubase_carryfree` (the Griego digit set + base +
  carry-free property), `an_interval`/`an_index`/`an_shift` (the dilution data). Documented holes —
  the explicit numeric/shift literals.
- **B2 `griego_bounded_doubling` (392), B3 `griego_diff_lower_bound` (401), B4 `griego_card_tendsto`
  (409)** — the three real-analysis sub-holes (floor-dilution doubling; θ-reconciliation via cached
  `log_bridge` + the `tsum=tdiff` interval-symmetry; atTop sup packaging). Left documented, NOT scoped
  this round (multi-round analysis infra, as planned).
- **Pre-existing:** `realizes_one` (139), `realizableSet_bddAbove` (150).

`griego_realizes` (assembled from B2/B3/B4), `c3a_ge_theta`, `c3a_lower_bound_def` are unchanged and
still assemble; B1's exponent/witness reshape did not touch them (the assembly routes through B2/B3/B4,
not B1 — B1 is the finite content B3 will consume).

## Claim
NO held raise — this is structural Lean progress only (B1 closed). `held` stays the verified Python
value C_3a > 1.1779 (R13). Even fully closed, the wired bridge certifies only θ>1.1771 (the B-side
reads `NativeDecideSmallMT`), not the held 1.1779. The claim of this round is solely that the
load-bearing finite combinatorial sub-hole B1 is now a real sorry-free Lean derivation (depending only
on the documented B1a + witness-data holes), and that two general axiom-clean counting lemmas are
available for reuse.

## R15 — B1a SPACING LEMMAS CLOSED (`setSum_tr_pair_disjoint` / `setDiff_tr_pair_disjoint`)

This round's deliverable: **the two general spacing lemmas the outliner factored out of B1a are now
proved sorry-free and axiom-clean**, and `griego_ak_disjoint` (B1a) is consequently reassembled with
its proof TERM sorry-free (the only `sorryAx` it now carries traces solely to the residual
`an_separated` hole it legitimately consumes). `lake build C3a` EXIT 0 (2969 jobs).

### What I closed (sorry-free, `#print axioms = [propext, Classical.choice, Quot.sound]`, NO sorryAx)
- **`setSum_tr_pair_disjoint`** (line ~365): if every element of `setSum B B` lies in `[lo, lo+diam]`
  and the shift gap `diam < |c − c'|`, then `setSum (tr c B) B` and `setSum (tr c' B) B` are disjoint.
  Proof: `setSum_tr` rewrites both to `image (c+·) (setSum B B)`; `Finset.disjoint_left` gives a common
  `c+w = c'+w'` with `w,w' ∈ [lo,lo+diam]`; `abs_le` + `omega` derive `|c−c'| ≤ diam`, contradicting
  `hgap` via `linarith`. Pure ℤ interval arithmetic — no construction needed.
- **`setDiff_tr_pair_disjoint`** (line ~380): the `setDiff` analogue, identical proof via `setDiff_tr`.

`#print axioms` (recorded via a throwaway `Sketches/AxCheck.lean`, since deleted):
```
'C3a.setSum_tr_pair_disjoint'  depends on axioms: [propext, Classical.choice, Quot.sound]
'C3a.setDiff_tr_pair_disjoint' depends on axioms: [propext, Classical.choice, Quot.sound]
'C3a.griego_ak_disjoint'       depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
```
The `griego_ak_disjoint` `sorryAx` is honest: the reassembly proof term is sorry-free; the `sorryAx`
enters ONLY through the named `an_separated` obligation it `obtain`s. (R14-style: a discharged proof
that consumes a documented sub-hole shows `sorryAx` tracing only to that hole.)

### Intermediate-statement note (NOT required this round)
The two spacing lemmas as planned (`WithinDiam (B±B) lo diam ∧ diam < |c−c'| ⟹ Disjoint …`) are
exactly true and provable as stated — no reshape needed. The one small Lean adjustment vs the plan's
suggested tactic path: `abs_lt` does NOT fire on `diam < |w'−w|` (it matches `|·| < ·`, abs on the
LHS), so I instead prove `|c−c'| ≤ diam` via `rw [abs_le]; constructor <;> omega` (omega uses the
membership equality `c+w = c'+w'` plus the two `WithinDiam` bounds) and close with `linarith`.

### Holes remaining after R15 (13 documented `sorry`, all build GREEN)
- **`an_separated` (line ~414) — the residual construction obligation** (the harder, uncached half of
  B1a). NOT closed this round, by plan. BLOCKER: it asserts the existence of the diameters AND the
  shift-spacing `diam < |aᵢ−aⱼ|` AND the interval-vs-union disjointness for the *concrete* witness data
  `an_shift`/`an_index`/`an_interval` — but those are themselves `sorry` defs (lines 309–311). There is
  nothing to compute the spacing from until the witness data is pinned. Closing it needs (a) pinning
  `an_shift n i = i·(2·maxbk n + 1)` (an AP) and `an_interval n` below all translates, and (b) a new
  `maxbk` element-range bound on `bk n = tpow Qbase Ubase n` (provable by induction on the box/emb
  carry-free digit structure). That `maxbk` lemma + the witness-data pinning is the natural next
  sub-target. NOT attempted this round (it is the larger, construction-bearing half, and depends on the
  Ubase/Qbase witness data which is also still a hole).
- **Witness data:** `Ubase`/`Qbase`/`Ubase_carryfree` (302–304), `an_interval`/`an_index`/`an_shift`
  (309–311) — the explicit Griego digit set + base + carry-free property + dilution data.
- **B2/B3/B4** (`griego_bounded_doubling`, `griego_diff_lower_bound`, `griego_card_tendsto`) — the
  three real-analysis sub-holes. Multi-round; not scoped.
- **Pre-existing:** `realizes_one` (140), `realizableSet_bddAbove` (151).

`griego_ak_disjoint` (B1a) and `griego_disjoint_union_count` (B1) are unchanged in statement and still
green; B1a is now a sorry-free reassembly modulo `an_separated`.

## Status
R15: B1a spacing lemmas `setSum_tr_pair_disjoint`/`setDiff_tr_pair_disjoint` CLOSED sorry-free
(`[propext, Classical.choice, Quot.sound]`); `griego_ak_disjoint` reassembled sorry-free modulo the
residual `an_separated` hole. `lake build C3a` EXIT 0 (2969 jobs). 13 documented `sorry`
(`an_separated` is now the load-bearing residual of B1a; witness data; B2/B3/B4; realizes_one;
bddAbove). No smuggled axiom. No `held` raise — structural only; even fully wired the bridge certifies
θ>1.1771, below the held 1.1779.
File: `lean/Sketches/C3aDef.lean`.

(Superseded: the R14 "12 documented sorry" status — B1a's spacing lemmas now closed, `an_separated`
named as the residual.)

## Promotable lemmas
**R15 — flag for certification** (proved sorry-free this round in `lean/Sketches/C3aDef.lean`,
`#print axioms = [propext, Classical.choice, Quot.sound]`, general — not sketch glue):
- `setSum_tr_pair_disjoint` (line ~365): `WithinDiam (setSum B B) lo diam → diam < |c − c'| →
  Disjoint (setSum (tr c B) B) (setSum (tr c' B) B)`.
- `setDiff_tr_pair_disjoint` (line ~380): the `setDiff` analogue.
  Both: a shift gap strictly exceeding the diameter of the sum/diffset ⟹ the two translate images are
  disjoint. Reusable for any composite/AP-dilution disjointness argument.

**R14 — flag for certification** (still pending, all `[propext, Classical.choice, Quot.sound]`):
- `setSum_card_decompose` / `setDiff_card_decompose` (lines ~271/285) — the disjoint-union GHR
  additive count `|(I ∪ ⋃ᵢ(aᵢ+B)) ± B| = |shifts|·|B±B| + |I±B|` under pairwise + interval
  disjointness. The reusable heart of any composite-dilution count.
- Supports: `setSum_tr_card` / `setDiff_tr_card` (translate cardinality-invariance),
  `setSum_union`/`setDiff_union`, `setSum_biUnion`/`setDiff_biUnion` (sum/diff distributivity),
  `setSum_tr`/`setDiff_tr` (translate-pushout). All sorry-free, axiom-clean.

(The earlier R12 "None this round" note is superseded.)

## Promotable lemmas (R18, for reviewer to certify into `lemmas/`)
- `box_elem_range` (C3aDef.lean ~L468) — `0≤Q ∧ U⊆[0,maxU] ∧ V⊆[0,maxV] ⟹ box Q U V ⊆ [0, maxU+Q·maxV]`.
  Element-range bound for the carry-free `box`/`emb` step. Axiom-clean `[propext, Classical.choice,
  Quot.sound]` (NO sorryAx). General (no witness data).
- `maxbk_nonneg` (C3aDef.lean ~L482) — `0≤maxU ∧ 0≤Q ⟹ 0 ≤ maxbk maxU Q n`. Axiom-clean
  `[propext, Classical.choice, Quot.sound]` (NO sorryAx). General; depends on the `maxbk` closed-form
  def (also general). Reusable element-range nonnegativity for the digit-tensor tower bound.
