# Lean certificate record — `lean-tensor-multiplicativity`

- **Lake project:** `constants/3a/lean/` (Lean v4.31.0; Mathlib pinned to the `v4.31.0` tag, rev
  `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`). Sketch file
  `constants/3a/lean/Sketches/TensorMultiplicativity.lean`, imported via the C3a lib glob.
- **Build target:** `lake build C3a`. **R9: EXIT 0, 2969 jobs, ZERO warnings** (no `sorry`,
  no unused-variable, no lints). `Build completed successfully (2969 jobs).`

## R9 — ALL 7 declared holes CLOSED, sorry-free

This sketch formalizes the finite/discrete half of the GHR bridge: carry-free tensor-power
multiplicativity of the sum/diff-set counts. All objects are `Finset ℤ`; no `native_decide`,
no integers literals, no continuum — a pure additive-combinatorics counting theorem.

- **Top theorems (HOLE-FREE, machine-checked):**
  - `C3a.tensor_pow_sumset_card (Q U) (hcf : CarryFree Q U) :`
    `∀ k, (sumset (tpow Q U k)).card = (sumset U).card ^ (k+1)`
  - `C3a.tensor_pow_diffset_card (Q U) (hcf : CarryFree Q U) :`
    `∀ k, (diffset (tpow Q U k)).card = (diffset U).card ^ (k+1)`
  i.e. `|U^{⊗(k+1)} ± U^{⊗(k+1)}| = |U±U|^(k+1)` for the base-Q digit-tensor power.

- **The 7 holes, all closed:**
  1. `carryfree_inj` — `emb Q (u,v)=u+Q·v` injective on `U ×ˢ V` (via general engine `emb_injOn`).
  2. `sumset_image_eq` (the flagged HARD step) — `sumset (box Q U V) = box Q (sumset U) (sumset V)`.
     Proved UNCONDITIONAL (no gap needed) by `Finset.ext` + `mem_image₂`/`mem_image`/`mem_product`
     and the ring identity `(u₁+Q·v₁)+(u₂+Q·v₂)=(u₁+u₂)+Q·(v₁+v₂)`.
  2'. `diffset_image_eq` — the `−` analogue, same proof.
  3. `sumset_card_mul_of_carryfree` — `|sumset(box)| = |sumset U|·|sumset V|`; `sumset_image_eq`
     then `card_image_of_injOn` (injectivity from `emb_injOn` + `sumset_bound`) + `card_product`.
  4. `diffset_card_mul_of_carryfree` — the `−` analogue.
  5. `tensor_pow_sumset_card` — induction on `k`, step = HOLE 3.
  6. `tensor_pow_diffset_card` — induction on `k`, step = HOLE 4.

- **`#print axioms` (verbatim, R9 — NO `sorryAx` on any):**
  - `C3a.tensor_pow_sumset_card` → `[propext, Classical.choice, Quot.sound]`
  - `C3a.tensor_pow_diffset_card` → `[propext, Classical.choice, Quot.sound]`
  - `C3a.sumset_image_eq` → `[propext, Classical.choice, Quot.sound]`
  - `C3a.diffset_image_eq` → `[propext, Classical.choice, Quot.sound]`
  - `C3a.carryfree_inj` → `[propext, Classical.choice, Quot.sound]`
  - `C3a.sumset_card_mul_of_carryfree` → `[propext, Classical.choice, Quot.sound]`
  - `C3a.diffset_card_mul_of_carryfree` → `[propext, Classical.choice, Quot.sound]`
  Only Mathlib's standard axioms — no native_decide axiom, no `sorryAx`, no smuggled axiom.

- **Intermediate-statement reshapes (all faithful — recorded for the reviewer):**
  1. `CarryFree Q U := 0 < Q ∧ ∀ a∈U, ∀ b∈U, 2·|a+b|<Q ∧ 2·|a-b|<Q` — `0 < Q` lifted to a
     top-level conjunct (was nested inside the ∀, which vacuously failed when `U=∅`, blocking the
     `0<Q` extraction). Strictly equivalent for nonempty U; correct (not weaker) for empty U.
  2. `sumset_image_eq` / `diffset_image_eq` dropped BOTH `CarryFree` hypotheses — the SET identity
     is unconditional ring algebra; the gap enters only at the cardinality step.
  3. `sumset_card_mul_of_carryfree` / `diffset_card_mul_of_carryfree` dropped `hcfV` (the second
     factor's carry-freeness) — injectivity of `emb` on `(U±U) ×ˢ (V±V)` needs only the FIRST
     coordinate (U±U) to fit one digit, i.e. only `CarryFree Q U`. This is what makes HOLE 5/6's
     induction need NO carry-freeness of the tower `tpow Q U k` (the "second subtlety" dissolves).

- **Holes remaining:** NONE in this sketch. It does NOT close `ghr` and does NOT raise `held`
  (held stays the verified Python cert C_3a > 1.1774). Its value: it discharges the finite,
  Lean-fit half of the GHR bridge, reducing the `ghr` hole from "counting + sup-limit, both open"
  to "sup-limit only" (the irreducible real-analysis sup-realization wrapper).

- **Promotable:** `tensor_pow_sumset_card` and `tensor_pow_diffset_card` (general over base set `U`
  and base `Q`, sorry-free, axiom-clean) — proposed for `constants/3a/lemmas/`.
