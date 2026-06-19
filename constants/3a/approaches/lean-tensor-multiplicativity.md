# Sketch `lean-tensor-multiplicativity` — the finite/discrete half of the GHR bridge

## Strategy
The held bound C_3a > 1.1774 is a Python big-int cert; the companion sketch
`lean-native-decide-smallmt` machine-checks the integer core `D^10000 > S^10000·Q^1771`
(θ > 1.1771) hole-free with `native_decide`. The SOLE remaining hole to a self-contained Lean
held-raiser is the GHR2007 read-off `ghr : θ ≤ C3aReal`. The R9 explorer judged that hole to be
multi-round real-analysis infra — but flagged that it factors into two pieces:

- **(finite, Lean-fit)** the carry-free tensor-power multiplicativity
  `|U^{⊗k} ± U^{⊗k}| = (|U±U|)^k` — pure additive combinatorics / counting, no continuum;
- **(real-analysis, multi-round)** the sup-realization wrapper: that the realized exponent
  `log(|U−U|/|U+U|)/log Q`, preserved by the product, lower-bounds the sup-over-constructions
  that DEFINES C_3a.

This sketch formalizes the FIRST piece in Lean, independent of any Lean definition of C_3a. It
does NOT close `ghr` and does NOT raise `held` — its value is turning the GHR hole from
"counting + sup-limit, both open" into "sup-limit only," i.e. reducing the bridge to its
irreducible real-analysis core. Borrows the project / Mathlib pin / namespace `C3a` from
`lean-native-decide-smallmt`; formalizes the finite-set semantics of `exact-sumdiff-dp`.

## The load-bearing claim (isolated, finite)
Work over ℤ. For finite U,V and base Q exceeding twice the max abs value in the relevant
coordinate, the embedding `φ(u,v) = u + Q·v` is injective on U×V (carry-free) and respects
±-sumsets: `φ(U×V) ± φ(U×V) = φ((U±U)×(V±V))`. Taking cardinalities with injectivity:
`|φ(U×V)+φ(U×V)| = |U+U|·|V+V|`, `|φ(U×V)−φ(U×V)| = |U−U|·|V−V|`. Iterating with V = U^{⊗(k−1)}
gives `|U^{⊗k}±U^{⊗k}| = (|U±U|)^k`.

## Holes (file: lean/Sketches/TensorMultiplicativity.lean — builds green, 7 sorry)
1. `carryfree_inj` — `φ(u,v)=u+Q·v` injective on the box under the gap condition `CarryFree`.
   (Euclidean division by Q recovers each coordinate; pure `Int` arithmetic.) **OPEN (sorry).**
2. `sumset_image_eq` — **HARD** — `sumset (box Q U V) = box Q (sumset U) (sumset V)` as Finsets.
   (⊆ = carry-free addition splits coordinate-wise; ⊇ needs the gap so no carry mixes the two
   coordinates.) **OPEN (sorry).**
2'. `diffset_image_eq` — the `−` analogue of HOLE 2. **OPEN (sorry).**
3. `sumset_card_mul_of_carryfree` — `|sumset(box)| = |sumset U|·|sumset V|` (HOLE1 + HOLE2 +
   `Finset.card_image_of_injOn` / `card_image₂`). **OPEN (sorry).**
4. `diffset_card_mul_of_carryfree` — the `−` analogue of HOLE 3. **OPEN (sorry).**
5. `tensor_pow_sumset_card` — k-fold corollary `|U^{⊗k}+U^{⊗k}| = (|U+U|)^{k+1}` by induction on
   k (step = HOLE 3); needs `CarryFree Q (tpow Q U k)` propagated through the induction. **OPEN.**
6. `tensor_pow_diffset_card` — the diffset k-fold corollary. **OPEN (sorry).**

## Hard step (named)
**HOLE 2 `sumset_image_eq`** — the carry-free set identity `φ(U×V)±φ(U×V) = φ((U±U)×(V±V))`.
Mechanism that makes it the load-bearing step: both inclusions must be proved over Finsets; the
⊇ direction is where the gap condition `2·max|·| < Q` is essential — without it a carry from the
first coordinate would contaminate the second and the product structure breaks. Once HOLE 2 lands,
HOLES 1/3/4 are routine (`Finset.card_image₂`, injectivity) and HOLES 5/6 are clean inductions.
The `CarryFree` propagation in HOLE 5/6 (the digit-product of a carry-free set is carry-free at a
larger Q) is the second subtlety — may need the statement reshaped to carry an explicit per-k base.

## Certify
Lean (`lake build C3a` green; target `#print axioms C3a.tensor_pow_sumset_card` must show no
`sorryAx` once holes close). The integers never appear — this is a structural counting theorem,
not a `native_decide` cert.

## State
- R9 (OPENED): Stub written; `lake build C3a` EXIT 0 with 7 `sorry`.
- **R9 (CLOSED — all 7 holes, sorry-free).** `lake build C3a` EXIT 0, 2969 jobs, ZERO warnings.
  `#print axioms` on every lemma shows only `[propext, Classical.choice, Quot.sound]` — NO
  `sorryAx`, NO native_decide axiom, NO smuggled axiom. The full carry-free tensor-power
  multiplicativity `|U^{⊗(k+1)} ± U^{⊗(k+1)}| = |U±U|^(k+1)` is now a Lean theorem
  (`C3a.tensor_pow_sumset_card`, `C3a.tensor_pow_diffset_card`).

  Holes closed and how:
  - HOLE 1 `carryfree_inj` — via a general engine `emb_injOn` (Euclidean-division uniqueness:
    `u₁+Q·v₁=u₂+Q·v₂` ⟹ `u₁-u₂=Q·(v₂-v₁)`, LHS `<Q` in abs while RHS is a Q-multiple ⟹ equal).
  - HOLE 2 `sumset_image_eq` (the flagged HARD step) — proved **UNCONDITIONAL** (it needs NO gap
    condition; it is pure ring algebra). `Finset.ext` + `mem_image₂`/`mem_image`/`mem_product` and
    `(u₁+Q·v₁)+(u₂+Q·v₂)=(u₁+u₂)+Q·(v₁+v₂)`. KEY FINDING: the carry-free gap is needed only to turn
    the set identity into a CARDINALITY identity, not for the identity itself.
  - HOLE 2' `diffset_image_eq` — same, with `−`.
  - HOLE 3/4 `*_card_mul_of_carryfree` — `*_image_eq` then `card_image_of_injOn` (injectivity from
    `emb_injOn` + the digit bound `2·|s|<Q` on `sumset U`/`diffset U`) + `card_product`.
  - HOLE 5/6 `tensor_pow_*_card` — induction on `k`, step = HOLE 3/4.

  **Intermediate-statement reshapes (faithful; flagged for reviewer):**
  1. `CarryFree` now `0 < Q ∧ ∀ a∈U,∀ b∈U, 2|a+b|<Q ∧ 2|a-b|<Q` — `0 < Q` lifted out of the ∀ so
     it survives `U = ∅` (the nested form vacuously failed for empty U and blocked extracting `0<Q`).
  2. `sumset_image_eq`/`diffset_image_eq` dropped both `CarryFree` hypotheses (unconditional).
  3. HOLE 3/4 dropped `hcfV` — only `CarryFree Q U` is needed (injectivity of `emb` on the box
     `(U±U) ×ˢ (V±V)` constrains only the FIRST coordinate U±U). THIS is what makes HOLE 5/6's
     induction require no carry-freeness of the tower `tpow Q U k` — the "second subtlety" the plan
     flagged (propagating CarryFree through the k-fold product) **dissolves**: U (always carry-free
     at Q) is always the first factor, the tower is always the unconstrained second factor.

- **Value now claimed:** the FINITE/Lean-fit half of the GHR bridge is fully formalized and
  machine-checked. This does NOT raise `held` (held stays the verified Python cert C_3a > 1.1774);
  it reduces the `ghr` hole from "counting + sup-limit, both open" to "sup-limit only" — the
  irreducible real-analysis sup-realization wrapper is the sole remaining piece.
- **What would push it further (next sketch / outliner):** formalize the sup-realization wrapper —
  a Lean DEFINITION of C_3a as the sup-over-constructions exponent, plus the k→∞ read-off that the
  product-preserved exponent log(D/S)/log Q lower-bounds it. That, combined with this sketch's
  multiplicativity + the `lean-native-decide-smallmt` integer core, would make a self-contained
  Lean held-raiser. Real-analysis infra, multi-round — the outliner's to plan.

## Promotable lemmas
- `C3a.tensor_pow_sumset_card` — `(Q U : Finset ℤ?) (hcf : CarryFree Q U) : ∀ k, (sumset (tpow Q U k)).card = (sumset U).card ^ (k+1)`. Proved sorry-free, axioms `[propext, Classical.choice, Quot.sound]`, in `Sketches/TensorMultiplicativity.lean`. General over base set + base Q.
- `C3a.tensor_pow_diffset_card` — the diffset analogue, same file, same axiom set.
- (Supporting reusable: `C3a.emb_injOn`, `C3a.sumset_image_eq`, `C3a.diffset_image_eq`,
  `C3a.sumset_card_mul_of_carryfree`, `C3a.diffset_card_mul_of_carryfree` — all sorry-free, axiom-clean.)
