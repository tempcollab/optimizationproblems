/-
  Sketch `lean-c3a-def` — SCOPED DEFINITION-ONLY sketch for the C_3a sup object.

  PURPOSE (per R12 math-explorer §3, §6): de-risk the Lean bridge (direction 1) by isolating
  its SOLE remaining uncached piece — a reviewer-certifiable Lean DEFINITION of C_3a as the
  registry's sup-over-constructions exponent — into its own narrow sketch, BEFORE sinking
  multiple rounds into the read-off. Two of the four pieces of a self-contained machine-checked
  `C_3a > 1.1771` are already cached Lean lemmas (`log-bridge`, `tensor-multiplicativity`); the
  integer core is hole-free (`lean-native-decide-smallmt`). The only blocker is that `C3aRealDef`
  is currently `opaque`, so the read-off `θ ≤ C3aRealDef` can only be an ASSUMED hypothesis. This
  sketch replaces the opaque constant with a CONCRETE `sSup`-over-a-predicate definition and
  leaves the read-off (membership of the Griego tensor family in that predicate) as documented
  `sorry` holes.

  THE REVIEWER'S JOB FOR THIS SKETCH is to certify the DEFINITION is faithful to the registry
  constant — NOT to certify a bound. A wrong/too-weak `def C3aRealDef` (e.g. a sup that is trivially
  ≥ anything, or one whose predicate does not match the registry semantics) makes any downstream
  theorem VACUOUS or non-faithful — strictly worse than the honest opaque hypothesis we have now.
  So this sketch deliberately proves NO new bound; it only puts a candidate definition + its
  faithfulness commentary on the table for an in/out ruling.

  ===========================================================================================
  THE REGISTRY / [GHR2007] DEFINITION — verified against the source PDF (R12).

  [GHR2007, Theorem 1 / inequality (5), Funct. Approx. 37(1):175–186] defines the lower-bound
  exponent exactly as:

      C_3a = sup { θ : ∃ K > 1, ∃ c(K) > 0, there exist ARBITRARILY LARGE pairs of finite
                   integer sets (A, B) with
                       (i)  |A + B| ≤ K · |A|              ("doubling": |A+B| ≪ |A|)
                       (ii) |A − B| ≥ c(K) · |A + B|^θ     (cleared "≫", |A−B| ≫ |A+B|^θ) }.

  BOTH clauses are genuine and load-bearing. Clause (i) — the BOUNDED-DOUBLING constraint with a
  FIXED constant K independent of the family index — was DROPPED in the R11 draft of this sketch;
  the R12 outline-reviewer flagged that this enlarges the realizable set so the sup can EXCEED
  C_3a (an inflated, non-faithful constant). This revision RESTORES clause (i). See the verbatim
  PDF transcription in the commentary `approaches/lean-c3a-def.md` (lines 528–584, "|A+B| ≤ K|A|
  and |A−B| ≥ c(K)|A+B|^θ").

  ===========================================================================================
  WHY THE WITNESS IS A TWO-SET COMPOSITE, NOT `A = B = U^{⊗k}` (the R11 collapse, corrected).

  The R11 draft used A = B = U^{⊗k} (the bare tensor power). That family does NOT satisfy clause
  (i): with B = A = U^{⊗k}, |A + B| = |U+U|^k and |A| = |U|^k, so the doubling ratio
  |A+B|/|A| = (|U+U|/|U|)^k → ∞ — it is UNBOUNDED, so no fixed K works and the bare-tensor family
  is NOT a registry witness. (A + A is never smaller than A, so |A+A| ≤ K|A| with fixed K fails
  for any genuinely growing set.) This is exactly why the doubling clause cannot be dropped: with
  it, the bare-tensor family is correctly EXCLUDED; the registry witness is a different object.

  The ACTUAL [GHR2007, Lemma p.4] witness that realizes θ = 1 + log(d/s)/log q is the COMPOSITE

        Bₖ := U^{⊗k}   (the digit-tensor power; |Bₖ| = |U|^k, |Bₖ±Bₖ| = |U±U|^k),
        Aₖ := [1, Lₖ] ∪ ⋃_{i=1}^{mₖ} (aᵢ + Bₖ),    mₖ = ⌊qᵏ/sᵏ⌋ ≈ (q/s)·…,   Lₖ = ⌊3qᵏ/(2(K−1))⌋,

  with the shifts aᵢ chosen separated (aᵢ − aⱼ ∉ Bₖ − Bₖ) so the translates and the interval are
  disjoint in sums/differences. GHR compute |Aₖ + Bₖ| = mₖ·sᵏ + t and |Aₖ − Bₖ| = mₖ·dᵏ + t with
  t = |[1,Lₖ] + Bₖ|, and choosing mₖ ≈ qᵏ/sᵏ, Lₖ ≈ qᵏ/(K−1) dilutes the doubling to the FIXED
  bound |Aₖ + Bₖ| ≤ K|Aₖ| (clause (i) HOLDS), while |Aₖ − Bₖ| ≥ (qd/s)^k ≥ c(K)·|Aₖ+Bₖ|^θ with
  θ = 1 + log(d/s)/log q (clause (ii)). The cached `tensor_pow_*_card` lemmas supply exactly the
  Bₖ-cardinalities (|U±U|^k) that this computation rests on; the dilution by the interval + m
  translates is the additional combinatorial wrapper, the genuine remaining content of HOLE B.

  CONSEQUENCE FOR FAITHFULNESS: the corrected predicate `Realizes` below quantifies over TWO sets
  A,B with the doubling clause, so `RealizableSet ⊆ {registry-realizable}` ⟹ `C3aRealDef ≤ C_3a`
  (the SAFE direction for a lower bound), and the 4/3 structural cap applies honestly. The Griego
  family is a member via the GHR composite Aₖ (NOT the bare tensor), so the definition is
  non-vacuous and the held bound flows through it. Both R12-reviewer faithfulness objections
  (dropped doubling; A=B collapse) are dissolved.

  ===========================================================================================
  WHAT THIS SKETCH PROVIDES (all build green; bound-claims are HOLES, documented `sorry`):
    * `Realizes c` — the FAITHFUL predicate "c is a realizable sum-difference exponent": a
      sequence of pairs (A n, B n) of finite integer sets, sizes → ∞, a FIXED doubling bound
      `|A n + B n| ≤ K·|A n|` eventually, and the cleared `|A n + B n|^c ≤ |A n − B n|` eventually.
    * `C3aRealDef : ℝ := sSup { c | Realizes c }` — the registry sup, CONCRETE (no longer opaque).
    * `realizes_one` / `realizableSet_bddAbove` — side facts (nonempty + bounded by the 4/3 cap)
      so `C3aRealDef` is not a junk `sSup`. HOLES (documented `sorry`).
    * `griego_realizes : Realizes theta` — the membership of the GHR composite of the Griego
      tensor family. HOLE B (the read-off; uses cached `tensor-multiplicativity` + the dilution
      wrapper). Documented `sorry`.
    * `c3a_ge_theta : theta ≤ C3aRealDef` — discharges what `lean-native-decide-smallmt` currently
      ASSUMES, by `le_csSup` from `griego_realizes`. One line modulo HOLE B.

  None of these raise `held`; they convert the opaque `C3aRealDef` + assumed `ghr` into a concrete,
  FAITHFUL definition + a NAMED membership hole, so the reviewer can rule the definitional approach
  in/out.
-/

import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Data.Finset.NAry
import Mathlib.Order.CompleteLattice.Basic
import Mathlib.Tactic
import Sketches.NativeDecideSmallMT   -- provides `C3a.theta` and `C3a.theta_gt` (the certified θ > 1.1771)
import Sketches.TensorMultiplicativity  -- provides `C3a.sumset`/`C3a.diffset` and the cached tensor-power card lemmas

namespace C3a

open Real Finset

/-- The two-set sumset `A + B` and diffset `A − B` as `Finset ℤ` (`image₂`), matching the
    cached one-set `sumset`/`diffset` (= `setSum S S` / `setDiff S S`). -/
def setSum (A B : Finset ℤ) : Finset ℤ := Finset.image₂ (· + ·) A B
def setDiff (A B : Finset ℤ) : Finset ℤ := Finset.image₂ (· - ·) A B

/-- A real exponent `c` is REALIZABLE — the FAITHFUL [GHR2007, ineq. (5)] predicate (R12 fix:
    the bounded-doubling clause (i) restored). There is a sequence of PAIRS of finite integer
    sets `(A n, B n)` such that:

      * `|A n| → ∞`  (the "arbitrarily large" quantifier, as `Filter.Tendsto … atTop atTop`);
      * there is a FIXED real constant `K` with `|A n + B n| ≤ K · |A n|` eventually
        (clause (i), the bounded doubling `|A+B| ≪ |A|` — K independent of n);
      * `|A n + B n| ^ c ≤ |A n − B n|` eventually
        (clause (ii), the cleared Vinogradov `|A−B| ≫ |A+B|^c`, the implicit constant c(K)
        absorbed into "eventually").

    Faithful direction: every `Realizes`-witness is a registry (GHR ineq. (5)) witness, so
    `RealizableSet ⊆ {registry-realizable c}` and hence `C3aRealDef ≤ C_3a` — the SAFE direction
    for a lower bound (it under-estimates C_3a, so a bound against `C3aRealDef` still bounds
    C_3a). -/
def Realizes (c : ℝ) : Prop :=
  ∃ A B : ℕ → Finset ℤ, ∃ K : ℝ,
    Filter.Tendsto (fun n => ((A n).card : ℝ)) Filter.atTop Filter.atTop ∧
    (∀ᶠ n in Filter.atTop, ((setSum (A n) (B n)).card : ℝ) ≤ K * ((A n).card : ℝ)) ∧
    (∀ᶠ n in Filter.atTop,
      ((setSum (A n) (B n)).card : ℝ) ^ c ≤ ((setDiff (A n) (B n)).card : ℝ))

/-- The set of realizable exponents. -/
def RealizableSet : Set ℝ := { c | Realizes c }

/-- **C_3a, defined.** The registry sup-over-constructions exponent, as a concrete `sSup`
    (replacing the `opaque C3aRealDef` of `lean-native-decide-smallmt`). -/
noncomputable def C3aRealDef : ℝ := sSup RealizableSet

/-- The realizable set is nonempty: `c = 1` is realizable. Witness (GHR baseline, [GHR2007]
    `θ₀ > 1.14465 ≥ 1` so `1` is realizable): the family realizing the elementary exponent has
    bounded doubling and `|A−B| ≥ |A+B|^1`. HOLE: needs a concrete witness family `(A n, B n)`
    with all three conditions (the GHR composite at the trivial exponent, or any explicit
    bounded-doubling family with `|A−B| ≥ |A+B|`). Documented `sorry`. -/
theorem realizes_one : Realizes 1 := by
  sorry

theorem realizableSet_nonempty : RealizableSet.Nonempty :=
  ⟨1, realizes_one⟩

/-- The realizable set is bounded above by the structural [GHR2007, Theorem 2] cap `4/3` (the
    proven upper bound on C_3a, now applicable HONESTLY because the doubling clause is restored —
    the 4/3 bound is proved for the CONSTRAINED constant). This makes `sSup RealizableSet` a
    genuine real (not `sSup ∅ = 0` and not an unbounded junk sup). HOLE: needs the GHR2007
    upper-bound theorem `|A−B| ≤ |A+B|^{4/3+o(1)}` under bounded doubling. Documented `sorry`. -/
theorem realizableSet_bddAbove : BddAbove RealizableSet := by
  sorry

/- ============================================================================================
    HOLE B — THE READ-OFF — now SPLIT into four named sub-holes (R14 revision, per R14
    math-explorer §5). `griego_realizes` is NOT one monolithic `sorry`; it is ASSEMBLED from the
    four lemmas below, so a builder can close the FINITE/combinatorial sub-hole (B1) — the genuine
    Lean-tractable load-bearing content — while leaving the three real-analysis sub-holes (B2/B3/B4)
    documented. This converts a single opaque hole into a structured proof skeleton where progress
    is visible at the sub-lemma granularity.

    THE WITNESS FAMILY. `theta` is the certified real exponent from `NativeDecideSmallMT`
    (θ > 1.1771). The realizing family is the GHR COMPOSITE of the Griego tensor power:

        bk n := U^{⊗n}                                  (Bₙ := tpow Q U n; cardinalities cached),
        ak n := [1, Lₙ] ∪ ⋃_{i=1}^{mₙ} (aᵢ + bk n),     mₙ = ⌊qⁿ/sⁿ⌋,  Lₙ = ⌊qⁿ/(K−1)⌋,

    with shifts aᵢ separated so the mₙ translates and the interval are pairwise sum/diff-disjoint
    (aᵢ − aⱼ ∉ Bₙ − Bₙ). The four sub-holes below are exactly the four obligations of
    [GHR2007, Lemma p.4] for this composite. To keep the sketch GREEN and let the builder reshape
    the witness as its computation dictates, the family is presented through ABSTRACT counting
    parameters (the cardinalities the four sub-holes connect), not a single frozen `def` — the
    builder pins the concrete `ak`/`bk` when it closes B1.
    ============================================================================================ -/

/- ============================================================================================
    R14 BUILDER (B1 CLOSE) — the FINITE/COMBINATORIAL disjoint-union counting machinery.

    These helpers formalise the genuine load-bearing finite content of GHR's composite count
    (`|Aₙ ± Bₙ| = mₙ·|Bₙ±Bₙ| + tₙ`): the sum/diff of a one-coordinate translate is the translate
    of the sum/diff (so it has the SAME cardinality), and the count over a DISJOINT union of `mₙ`
    such translates plus an interval piece ADDS (`Finset.card_biUnion` + `card_union_of_disjoint`).
    All sorry-FREE — this is the Lean-fit heart B1 reduces to. (Mirrors the `tr`/`box` pattern of
    `lean-tensor-multiplicativity`; uses only `Finset` counting, no real analysis.)
    ============================================================================================ -/

/-- The one-coordinate translate `c + A` of a Finset (`image (c + ·)`). -/
def tr (c : ℤ) (A : Finset ℤ) : Finset ℤ := A.image (c + ·)

/-- `setSum` of a translate is the translate of the `setSum` (pure ring algebra:
    `(c + a) + y = c + (a + y)`). -/
theorem setSum_tr (c : ℤ) (A B : Finset ℤ) :
    setSum (tr c A) B = (setSum A B).image (c + ·) := by
  ext z
  simp only [setSum, tr, mem_image₂, mem_image]
  constructor
  · rintro ⟨x, ⟨a, ha, rfl⟩, y, hy, rfl⟩
    exact ⟨a + y, ⟨a, ha, y, hy, rfl⟩, by ring⟩
  · rintro ⟨w, ⟨a, ha, y, hy, rfl⟩, rfl⟩
    exact ⟨c + a, ⟨a, ha, rfl⟩, y, hy, by ring⟩

/-- `setDiff` of a translate is the translate of the `setDiff`. -/
theorem setDiff_tr (c : ℤ) (A B : Finset ℤ) :
    setDiff (tr c A) B = (setDiff A B).image (c + ·) := by
  ext z
  simp only [setDiff, tr, mem_image₂, mem_image]
  constructor
  · rintro ⟨x, ⟨a, ha, rfl⟩, y, hy, rfl⟩
    exact ⟨a - y, ⟨a, ha, y, hy, rfl⟩, by ring⟩
  · rintro ⟨w, ⟨a, ha, y, hy, rfl⟩, rfl⟩
    exact ⟨c + a, ⟨a, ha, rfl⟩, y, hy, by ring⟩

/-- A translate's `setSum` has the SAME cardinality (translation is injective). -/
theorem setSum_tr_card (c : ℤ) (A B : Finset ℤ) :
    (setSum (tr c A) B).card = (setSum A B).card := by
  rw [setSum_tr, card_image_of_injective _ (add_right_injective c)]

/-- A translate's `setDiff` has the SAME cardinality. -/
theorem setDiff_tr_card (c : ℤ) (A B : Finset ℤ) :
    (setDiff (tr c A) B).card = (setDiff A B).card := by
  rw [setDiff_tr, card_image_of_injective _ (add_right_injective c)]

/-- `setSum` distributes over a `∪` in the first argument. -/
theorem setSum_union (A A' B : Finset ℤ) :
    setSum (A ∪ A') B = setSum A B ∪ setSum A' B := by
  simp only [setSum]
  ext z; simp only [mem_image₂, mem_union]
  constructor
  · rintro ⟨x, (hx | hx), y, hy, rfl⟩
    · exact Or.inl ⟨x, hx, y, hy, rfl⟩
    · exact Or.inr ⟨x, hx, y, hy, rfl⟩
  · rintro (⟨x, hx, y, hy, rfl⟩ | ⟨x, hx, y, hy, rfl⟩)
    · exact ⟨x, Or.inl hx, y, hy, rfl⟩
    · exact ⟨x, Or.inr hx, y, hy, rfl⟩

/-- `setDiff` distributes over a `∪` in the first argument. -/
theorem setDiff_union (A A' B : Finset ℤ) :
    setDiff (A ∪ A') B = setDiff A B ∪ setDiff A' B := by
  simp only [setDiff]
  ext z; simp only [mem_image₂, mem_union]
  constructor
  · rintro ⟨x, (hx | hx), y, hy, rfl⟩
    · exact Or.inl ⟨x, hx, y, hy, rfl⟩
    · exact Or.inr ⟨x, hx, y, hy, rfl⟩
  · rintro (⟨x, hx, y, hy, rfl⟩ | ⟨x, hx, y, hy, rfl⟩)
    · exact ⟨x, Or.inl hx, y, hy, rfl⟩
    · exact ⟨x, Or.inr hx, y, hy, rfl⟩

/-- `setSum` distributes over a `biUnion` in the first argument. -/
theorem setSum_biUnion {ι : Type*} [DecidableEq ι] (s : Finset ι) (f : ι → Finset ℤ) (B : Finset ℤ) :
    setSum (s.biUnion f) B = s.biUnion (fun i => setSum (f i) B) := by
  simp only [setSum]
  ext z; simp only [mem_image₂, mem_biUnion]
  constructor
  · rintro ⟨x, ⟨i, hi, hx⟩, y, hy, rfl⟩; exact ⟨i, hi, x, hx, y, hy, rfl⟩
  · rintro ⟨i, hi, x, hx, y, hy, rfl⟩; exact ⟨x, ⟨i, hi, hx⟩, y, hy, rfl⟩

/-- `setDiff` distributes over a `biUnion` in the first argument. -/
theorem setDiff_biUnion {ι : Type*} [DecidableEq ι] (s : Finset ι) (f : ι → Finset ℤ) (B : Finset ℤ) :
    setDiff (s.biUnion f) B = s.biUnion (fun i => setDiff (f i) B) := by
  simp only [setDiff]
  ext z; simp only [mem_image₂, mem_biUnion]
  constructor
  · rintro ⟨x, ⟨i, hi, hx⟩, y, hy, rfl⟩; exact ⟨i, hi, x, hx, y, hy, rfl⟩
  · rintro ⟨i, hi, x, hx, y, hy, rfl⟩; exact ⟨x, ⟨i, hi, hx⟩, y, hy, rfl⟩

/-- **The GHR composite count, SUM side (general, sorry-free).** If the `mₙ = |shifts|` translate
    sumsets `setSum (aᵢ + B) B` are pairwise disjoint AND disjoint from the interval piece
    `setSum I B`, then `|(I ∪ ⋃ᵢ (aᵢ + B)) + B| = |shifts|·|B+B| + |I+B|`. This is exactly the GHR
    additive identity `|Aₙ + Bₙ| = mₙ·sⁿ + t`, here at the cardinality level via `card_biUnion` +
    `card_union_of_disjoint` + the translation invariance `setSum_tr_card`. -/
theorem setSum_card_decompose
    {ι : Type*} [DecidableEq ι] (shifts : Finset ι) (a : ι → ℤ) (I B : Finset ℤ)
    (hpair : ∀ i ∈ shifts, ∀ j ∈ shifts, i ≠ j →
        Disjoint (setSum (tr (a i) B) B) (setSum (tr (a j) B) B))
    (hint : Disjoint (setSum I B) (shifts.biUnion (fun i => setSum (tr (a i) B) B))) :
    (setSum (I ∪ shifts.biUnion (fun i => tr (a i) B)) B).card
      = shifts.card * (sumset B).card + (setSum I B).card := by
  rw [setSum_union, setSum_biUnion, card_union_of_disjoint hint, card_biUnion hpair]
  have hc : ∀ i ∈ shifts, (setSum (tr (a i) B) B).card = (sumset B).card := by
    intro i _; rw [setSum_tr_card]; rfl
  rw [Finset.sum_congr rfl hc, Finset.sum_const, smul_eq_mul]
  ring

/-- **The GHR composite count, DIFF side (general, sorry-free).** -/
theorem setDiff_card_decompose
    {ι : Type*} [DecidableEq ι] (shifts : Finset ι) (a : ι → ℤ) (I B : Finset ℤ)
    (hpair : ∀ i ∈ shifts, ∀ j ∈ shifts, i ≠ j →
        Disjoint (setDiff (tr (a i) B) B) (setDiff (tr (a j) B) B))
    (hint : Disjoint (setDiff I B) (shifts.biUnion (fun i => setDiff (tr (a i) B) B))) :
    (setDiff (I ∪ shifts.biUnion (fun i => tr (a i) B)) B).card
      = shifts.card * (diffset B).card + (setDiff I B).card := by
  rw [setDiff_union, setDiff_biUnion, card_union_of_disjoint hint, card_biUnion hpair]
  have hc : ∀ i ∈ shifts, (setDiff (tr (a i) B) B).card = (diffset B).card := by
    intro i _; rw [setDiff_tr_card]; rfl
  rw [Finset.sum_congr rfl hc, Finset.sum_const, smul_eq_mul]
  ring

/-- The base set `U` (Griego digit set) and carry-free base `Qbase` from the certified point. The
    concrete numeric literals come from the scan row; left as documented witness-data holes (the
    actual Griego digit set is large but explicit). The carry-free property is what the cached
    tensor lemmas require. HOLE (carry-free witness data). -/
def Ubase : Finset ℤ := sorry
def Qbase : ℤ := sorry
theorem Ubase_carryfree : CarryFree Qbase Ubase := sorry

/-- The dilution data: the interval `[1,Lₙ]` and the `mₙ` separated shifts `aᵢ`, indexed over a
    `Finset` of cardinality `mₙ`. Left as documented witness-data holes (the explicit shift choice
    realising the separation `aᵢ − aⱼ ∉ Bₙ − Bₙ` is the genuine uncached combinatorial choice). -/
def an_interval (n : ℕ) : Finset ℤ := sorry
def an_index (n : ℕ) : Finset ℕ := sorry
def an_shift (n : ℕ) : ℕ → ℤ := sorry

/-- **The composite witness sets, now PINNED to the GHR composite shape** (no longer opaque):
    `bk n = U^{⊗n}` (the cached tensor power) and
    `ak n = [1,Lₙ] ∪ ⋃ᵢ (aᵢ + bk n)` (interval ∪ separated translates).
    Pinning the SHAPE (not the numeric data) is what makes the finite count `griego_disjoint_union_count`
    provable from the general decomposition lemmas above; only the disjointness of the pieces (which
    needs the separation choice) stays a documented hole. -/
def bk (n : ℕ) : Finset ℤ := tpow Qbase Ubase n
def ak (n : ℕ) : Finset ℤ :=
  an_interval n ∪ (an_index n).biUnion (fun i => tr (an_shift n i) (bk n))

/-- **SUB-HOLE B1a — the disjointness of the GHR pieces (NEW documented sub-hole, the genuine
    UNCACHED combinatorial content).** The `mₙ` translate images and the interval piece are
    pairwise disjoint in BOTH sums and diffs, because the shifts are chosen separated
    (`aᵢ − aⱼ ∉ Bₙ − Bₙ`, and the interval placed past the translates). This is exactly the
    separation argument GHR establish for the composite; it depends on the explicit shift choice
    `an_shift`, so it is left documented `sorry`. (Once an explicit `an_shift` is pinned, this is a
    finite pigeonhole/range argument — but it is NOT supplied by any cached lemma.) -/
theorem griego_ak_disjoint (n : ℕ) :
    (∀ i ∈ an_index n, ∀ j ∈ an_index n, i ≠ j →
        Disjoint (setSum (tr (an_shift n i) (bk n)) (bk n))
                 (setSum (tr (an_shift n j) (bk n)) (bk n))) ∧
    Disjoint (setSum (an_interval n) (bk n))
             ((an_index n).biUnion (fun i => setSum (tr (an_shift n i) (bk n)) (bk n))) ∧
    (∀ i ∈ an_index n, ∀ j ∈ an_index n, i ≠ j →
        Disjoint (setDiff (tr (an_shift n i) (bk n)) (bk n))
                 (setDiff (tr (an_shift n j) (bk n)) (bk n))) ∧
    Disjoint (setDiff (an_interval n) (bk n))
             ((an_index n).biUnion (fun i => setDiff (tr (an_shift n i) (bk n)) (bk n))) := by
  sorry

/-- **SUB-HOLE B1 — the finite/combinatorial disjoint-union count (LOAD-BEARING, CLOSED R14).**
    The GHR additive identity, now PROVED sorry-free: from the disjointness B1a + the general
    decomposition lemmas `setSum_card_decompose`/`setDiff_card_decompose` + the cached
    `tensor_pow_sumset_card`/`tensor_pow_diffset_card` (for `|Bₙ±Bₙ| = |U±U|^(n+1)`), with
    `mₙ = |an_index n|`, `tₙ = |[1,Lₙ] ± Bₙ|`:

        |ak n + bk n| = mₙ · |U+U|^(n+1) + tₙ,    |ak n − bk n| = mₙ · |U−U|^(n+1) + tₙ.

    INTERMEDIATE-STATEMENT FIX (R14), two changes, both forced by the actual Lean objects:
    (1) exponent `^ n → ^ (n+1)`: with `bk n = U^{⊗n} = tpow Qbase Ubase n` the cached card lemma
        gives `|U±U|^(n+1)` (the `tpow … n` convention has `n+1` factors).
    (2) the interval piece is carried as TWO witnesses `tsum = |[1,Lₙ]+Bₙ|`, `tdiff = |[1,Lₙ]−Bₙ|`
        rather than one shared `tₙ`: GHR's single `t` additionally uses `|I+B| = |I−B|` for the long
        interval, which is a SEPARATE finite fact (not part of the disjoint-union count). Keeping
        them separate makes B1 exactly the count that the decomposition lemmas prove, with no
        smuggled interval-symmetry; the `tsum = tdiff` reconciliation is deferred to B3. -/
theorem griego_disjoint_union_count :
    ∀ n : ℕ, ∃ mn tsum tdiff : ℕ,
      (setSum (ak n) (bk n)).card = mn * (sumset Ubase).card ^ (n + 1) + tsum ∧
      (setDiff (ak n) (bk n)).card = mn * (diffset Ubase).card ^ (n + 1) + tdiff := by
  intro n
  obtain ⟨hpS, hintS, hpD, hintD⟩ := griego_ak_disjoint n
  refine ⟨(an_index n).card, (setSum (an_interval n) (bk n)).card,
          (setDiff (an_interval n) (bk n)).card, ?_, ?_⟩
  · -- SUM side
    have hdec :=
      setSum_card_decompose (an_index n) (an_shift n) (an_interval n) (bk n) hpS hintS
    have hcard : (sumset (bk n)).card = (sumset Ubase).card ^ (n + 1) := by
      simpa [bk] using tensor_pow_sumset_card Qbase Ubase Ubase_carryfree n
    calc (setSum (ak n) (bk n)).card
        = (an_index n).card * (sumset (bk n)).card
            + (setSum (an_interval n) (bk n)).card := by rw [ak]; exact hdec
      _ = (an_index n).card * (sumset Ubase).card ^ (n + 1)
            + (setSum (an_interval n) (bk n)).card := by rw [hcard]
  · -- DIFF side
    have hdec :=
      setDiff_card_decompose (an_index n) (an_shift n) (an_interval n) (bk n) hpD hintD
    have hcard : (diffset (bk n)).card = (diffset Ubase).card ^ (n + 1) := by
      simpa [bk] using tensor_pow_diffset_card Qbase Ubase Ubase_carryfree n
    calc (setDiff (ak n) (bk n)).card
        = (an_index n).card * (diffset (bk n)).card
            + (setDiff (an_interval n) (bk n)).card := by rw [ak]; exact hdec
      _ = (an_index n).card * (diffset Ubase).card ^ (n + 1)
            + (setDiff (an_interval n) (bk n)).card := by rw [hcard]

/-- **SUB-HOLE B2 — the doubling-dilution inequality (real-analysis, DOCUMENTED).**
    A FIXED `K` with `|ak n + bk n| ≤ K · |ak n|` eventually: the interval `[1,Lₙ]` of length
    `Lₙ ≈ qⁿ/(K−1)` dominates `|ak n|` enough to cap the doubling ratio independent of `n`. Floor-
    function real-arithmetic estimate over `mₙ, Lₙ, sⁿ, qⁿ`. Left documented `sorry`. -/
theorem griego_bounded_doubling :
    ∃ K : ℝ, ∀ᶠ n in Filter.atTop,
      ((setSum (ak n) (bk n)).card : ℝ) ≤ K * ((ak n).card : ℝ) := by
  sorry

/-- **SUB-HOLE B3 — the diff lower bound / θ reconciliation (DOCUMENTED).**
    `|ak n + bk n|^θ ≤ |ak n − bk n|` eventually, with θ = 1 + log(D/S)/log Q. Chains B1's counts
    with the cached `log_bridge` algebra (`d^B > s^B q^A ⟹ θ > 1 + A/B`) to land the cleared
    Vinogradov exponent. Left documented `sorry`. -/
theorem griego_diff_lower_bound :
    ∀ᶠ n in Filter.atTop,
      ((setSum (ak n) (bk n)).card : ℝ) ^ theta ≤ ((setDiff (ak n) (bk n)).card : ℝ) := by
  sorry

/-- **SUB-HOLE B4 — the `Filter.atTop` size→∞ packaging (DOCUMENTED).**
    `|ak n| → ∞`: the cardinalities grow with `n` (the interval `[1,Lₙ]` alone has `Lₙ → ∞`).
    Tendsto plumbing over the floor-indexed family. Left documented `sorry`. -/
theorem griego_card_tendsto :
    Filter.Tendsto (fun n => ((ak n).card : ℝ)) Filter.atTop Filter.atTop := by
  sorry

/-- HOLE B, REASSEMBLED from B1–B4: the Griego composite family realizes `theta`. This proof is
    `sorry`-FREE once B1–B4 close — it just packages the four obligations into the `Realizes`
    predicate. (B1 supplies the cardinality structure B2/B3 consume; here we wire the three
    `Realizes` conjuncts to B4/B2/B3.) -/
theorem griego_realizes : Realizes theta := by
  obtain ⟨K, hK⟩ := griego_bounded_doubling
  exact ⟨ak, bk, K, griego_card_tendsto, hK, griego_diff_lower_bound⟩

/-- Discharges what `lean-native-decide-smallmt` currently ASSUMES as `ghr : theta ≤ C3aRealDef`:
    once `theta` is realized, it is ≤ the sup of realizable exponents by `le_csSup`
    (using `realizableSet_bddAbove`). One line modulo HOLE B. -/
theorem c3a_ge_theta : theta ≤ C3aRealDef :=
  le_csSup realizableSet_bddAbove (show theta ∈ RealizableSet from griego_realizes)

/-- ============================================================================================
    The faithful top theorem with C_3a now CONCRETE (no `opaque`, no assumed `ghr` hypothesis):
    C_3a > 1.1771. Holds modulo the documented holes above (`griego_realizes` is the load-bearing
    one). When those close, this is a self-contained machine-checked record beat over the registry
    sup definition. -/
theorem c3a_lower_bound_def : (11771 : ℝ) / 10000 < C3aRealDef :=
  lt_of_lt_of_le theta_gt c3a_ge_theta

end C3a
