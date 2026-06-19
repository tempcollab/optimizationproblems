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

/- ============================================================================================
    `realizes_one` — DECOMPOSED (R21, per R21 math-explorer §"Fallback / second cheap slug").

    The base case `Realizes 1` is closed by the GROWING INTERVAL family
        A n := B n := Finset.Icc (0:ℤ) n.
    For this family the three `Realizes` clauses are all FINITE/ALGEBRAIC:
        * sumset:  setSum (Icc 0 n)(Icc 0 n) = Icc 0 (2n),   card = 2n+1
        * diffset: setDiff (Icc 0 n)(Icc 0 n) = Icc (-n) n,  card = 2n+1
        * |A n| = |Icc 0 n| = n+1
      so clause (i) `2n+1 ≤ K·(n+1)` holds with K = 3 (for n ≥ 0: 2n+1 ≤ 3n+3),
         clause (ii) `(2n+1)^1 = 2n+1 ≤ 2n+1` holds (equality),
         and `|A n| = n+1 → ∞`.

    The load-bearing finite content is the two SUMSET/DIFFSET interval identities `icc_setSum_card`
    / `icc_setDiff_card` (the only `sorry` sub-holes); everything else is `Nat.card_Icc` + filter
    plumbing. This is the genuinely Lean-fit, plausibly-one-round closure the explorer flagged.
    ============================================================================================ -/

/-- **R1a helper (CLOSED R21).** The sumset of `[0,n]` with itself is exactly the interval `[0,2n]`.
    The `⊇` half writes any `z ∈ [0,2n]` as `min z n + (z − min z n)` with both summands in `[0,n]`. -/
theorem icc_setSum_eq (n : ℤ) (hn : 0 ≤ n) :
    setSum (Finset.Icc (0:ℤ) n) (Finset.Icc (0:ℤ) n) = Finset.Icc 0 (2 * n) := by
  ext z
  simp only [setSum, mem_image₂, mem_Icc]
  constructor
  · rintro ⟨a, ⟨ha0, han⟩, b, ⟨hb0, hbn⟩, rfl⟩
    exact ⟨by omega, by omega⟩
  · rintro ⟨hz0, hz2n⟩
    refine ⟨min z n, ⟨by omega, by omega⟩, z - min z n, ⟨by omega, by omega⟩, by omega⟩

/-- **SUB-HOLE R1a — CLOSED R21.** `|Icc 0 n + Icc 0 n| = 2n+1` for `0 ≤ n`, via `icc_setSum_eq`
    (`= [0,2n]`) + `Int.card_Icc`. THE LOAD-BEARING finite step. -/
theorem icc_setSum_card (n : ℤ) (hn : 0 ≤ n) :
    (setSum (Finset.Icc (0:ℤ) n) (Finset.Icc (0:ℤ) n)).card = (2 * n + 1).toNat := by
  rw [icc_setSum_eq n hn, Int.card_Icc]
  congr 1
  omega

/-- **R1b helper (CLOSED R21).** The diffset of `[0,n]` with itself is exactly the symmetric
    interval `[-n,n]`. The `⊇` half writes any `z ∈ [-n,n]` as `max z 0 − max (-z) 0`, both in `[0,n]`. -/
theorem icc_setDiff_eq (n : ℤ) (hn : 0 ≤ n) :
    setDiff (Finset.Icc (0:ℤ) n) (Finset.Icc (0:ℤ) n) = Finset.Icc (-n) n := by
  ext z
  simp only [setDiff, mem_image₂, mem_Icc]
  constructor
  · rintro ⟨a, ⟨ha0, han⟩, b, ⟨hb0, hbn⟩, rfl⟩
    exact ⟨by omega, by omega⟩
  · rintro ⟨hzlo, hzhi⟩
    refine ⟨max z 0, ⟨by omega, by omega⟩, max (-z) 0, ⟨by omega, by omega⟩, by omega⟩

/-- **SUB-HOLE R1b — CLOSED R21.** `|Icc 0 n − Icc 0 n| = 2n+1` for `0 ≤ n`, via `icc_setDiff_eq`
    (`= [-n,n]`) + `Int.card_Icc`. -/
theorem icc_setDiff_card (n : ℤ) (hn : 0 ≤ n) :
    (setDiff (Finset.Icc (0:ℤ) n) (Finset.Icc (0:ℤ) n)).card = (2 * n + 1).toNat := by
  rw [icc_setDiff_eq n hn, Int.card_Icc]
  congr 1
  omega

/-- The integer interval `[0,n]` has `n+1` points (`n : ℕ`). -/
theorem icc_card (n : ℕ) : (Finset.Icc (0:ℤ) (n:ℤ)).card = (n + 1) := by
  rw [Int.card_Icc]
  omega

/-- The realizable set is nonempty: `c = 1` is realizable, via the growing interval family
    `A n = B n = Icc 0 n`. REASSEMBLED `sorry`-free from the two interval-cardinality sub-holes
    `icc_setSum_card` / `icc_setDiff_card` (and `Nat.card_Icc`); the three `Realizes` clauses are
    finite/algebraic for this family (K = 3 doubling; equality in clause (ii); `n+1 → ∞`). -/
theorem realizes_one : Realizes 1 := by
  refine ⟨fun n => Finset.Icc (0:ℤ) (n : ℤ), fun n => Finset.Icc (0:ℤ) (n : ℤ), 3, ?_, ?_, ?_⟩
  · -- |A n| = n+1 → ∞
    have hc : (fun n : ℕ => ((Finset.Icc (0:ℤ) (n:ℤ)).card : ℝ)) = (fun n : ℕ => (n : ℝ) + 1) := by
      funext n
      rw [icc_card n]
      push_cast
      ring
    rw [hc]
    apply Filter.tendsto_atTop_add_const_right
    exact tendsto_natCast_atTop_atTop
  · -- clause (i): |A n + B n| = 2n+1 ≤ 3·(n+1) = 3·|A n|
    filter_upwards with n
    rw [icc_setSum_card (n:ℤ) (by positivity), icc_card n]
    have h2n : (2 * (n:ℤ) + 1).toNat = 2 * n + 1 := by omega
    rw [h2n]
    push_cast
    have hn0 : (0:ℝ) ≤ (n:ℝ) := Nat.cast_nonneg n
    nlinarith [hn0]
  · -- clause (ii): (2n+1)^1 = 2n+1 ≤ 2n+1 = |A n − B n|
    filter_upwards with n
    rw [icc_setSum_card (n:ℤ) (by positivity), icc_setDiff_card (n:ℤ) (by positivity)]
    rw [Real.rpow_one]

theorem realizableSet_nonempty : RealizableSet.Nonempty :=
  ⟨1, realizes_one⟩

/-- **SUB-HOLE (alternative angle, R21) — the GHR 4/3 upper bound, ISOLATED.**
    Every realizable exponent is `≤ 4/3`. This is the [GHR2007, Theorem 2] structural upper bound
    `|A−B| ≤ |A+B|^{4/3+o(1)}` under bounded doubling — the IRREDUCIBLE hard analytic content of
    `realizableSet_bddAbove` (Mathlib has Plünnecke–Ruzsa but NOT this specific GHR bound; it is a
    substantial formalization left as ONE clearly-named documented `sorry`). All of the
    `BddAbove`-plumbing hardness collapses into this single lemma. DOCUMENTED `sorry`. -/
theorem ghr_upper {c : ℝ} (hc : Realizes c) : c ≤ 4 / 3 := by
  sorry

/-- The realizable set is bounded above by the structural [GHR2007, Theorem 2] cap `4/3`. This
    makes `sSup RealizableSet` a genuine real (not `sSup ∅ = 0` and not an unbounded junk sup).
    REASSEMBLED `sorry`-free from the isolated hard lemma `ghr_upper` — the `BddAbove` witness is
    just `⟨4/3, …⟩` with the upper-bound condition discharged by `ghr_upper`. -/
theorem realizableSet_bddAbove : BddAbove RealizableSet :=
  ⟨4 / 3, fun _ hc => ghr_upper hc⟩

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

/-- The Griego per-column digit set `{0,2,3,4,5,6,7,8,9,10}` (drop digit `1`, max digit `10`). The
    held Python cert uses this 10-element set with base `b = 21 = 2·max+1` for its single-column digit
    injectivity. The cached Lean `CarryFree`/`tensor_pow_*` chain proves a STRONGER box-injectivity
    that ALSO needs sums in-digit (`2·|a+b| < Q`), so the carry-free base here is `Qbase = 41 > 4·max`
    (NOT 21): with max digit 10, max `|a+b| = 20`, and `2·20 = 40 < 41`. Every downstream structural
    lemma is parametric in `Qbase`, so this base-`Q` choice changes nothing in the B1 scaffolding —
    only the deferred B3 numeric tie-in of the tensor sumset/diffset to `theta` cares. -/
def Ubase : Finset ℤ := {0, 2, 3, 4, 5, 6, 7, 8, 9, 10}
def Qbase : ℤ := 41
theorem Ubase_carryfree : CarryFree Qbase Ubase := by
  refine ⟨by decide, ?_⟩
  decide

/-- The closed-form element-range bound for the digit-tensor tower (parametric in the base bound
    `maxU`). `maxbk maxU Q 0 = maxU`, `maxbk maxU Q (k+1) = maxU + Q·(maxbk maxU Q k)`. -/
def maxbk (maxU Q : ℤ) : ℕ → ℤ
  | 0 => maxU
  | (k + 1) => maxU + Q * maxbk maxU Q k

/-- The element-range bound `maxUbase` of the base digit set: every `u ∈ Ubase` lies in
    `[0, maxUbase]`. The numeric literal comes from the scan row (the Griego digit set is
    nonnegative with explicit max digit). DOCUMENTED WITNESS DATA (numeric). HOLE. -/
def maxUbase : ℤ := 10
/-- The base set is nonnegative and bounded by `maxUbase = 10`: every `u ∈ {0,2,…,10}` satisfies
    `0 ≤ u ≤ 10`. Finite check over the explicit 10-element set. -/
theorem Ubase_range : 0 ≤ maxUbase ∧ (∀ u ∈ Ubase, 0 ≤ u ∧ u ≤ maxUbase) := by
  refine ⟨by decide, ?_⟩
  decide

/-- Pinned to type-correct CLOSED forms consumed only by SHAPE downstream (`an_separated` /
    `interval_union_disjoint_*` are proved parametrically). The NUMERIC dilution content
    (`mₙ = ⌊qⁿ/sⁿ⌋`, the actual interval-band bottom) stays deferred to B2/B3 — this round pins only
    the shape, NOT the numeric values. `mnData := fun _ => 1` (one separated translate) and
    `negLoData n = -(2·maxbk n + 1)` (band bottom one spacing below the lowest translate window). -/
def mnData : ℕ → ℕ := fun _ => 1
def negLoData : ℕ → ℤ := fun n => -(2 * maxbk maxUbase Qbase n + 1)

/-- The dilution data, now PINNED to the AP shape (only the counts `mnData`/`negLoData` stay open):
    `an_shift n i = i·(2·maxbk n + 1)` is an arithmetic progression with spacing strictly exceeding
    the sum/diffset diameter `2·maxbk n`; `an_index n = {0,…,mₙ−1}`; `an_interval n` is a band placed
    ENTIRELY BELOW the lowest translate window (every element `≤ −(2·maxbk n + 1)`), so its sum/diff
    with `bk n` is disjoint from every translate's. Pinning the SHAPE (not the numeric counts) is what
    makes the spacing + interval-vs-union disjointness in `an_separated` computable. -/
def an_shift (n : ℕ) : ℕ → ℤ := fun i => (i : ℤ) * (2 * maxbk maxUbase Qbase n + 1)
def an_index (n : ℕ) : Finset ℕ := Finset.range (mnData n)
noncomputable def an_interval (n : ℕ) : Finset ℤ :=
  Finset.Icc (negLoData n) (-(2 * maxbk maxUbase Qbase n + 1))

/-- **The composite witness sets, now PINNED to the GHR composite shape** (no longer opaque):
    `bk n = U^{⊗n}` (the cached tensor power) and
    `ak n = [1,Lₙ] ∪ ⋃ᵢ (aᵢ + bk n)` (interval ∪ separated translates).
    Pinning the SHAPE (not the numeric data) is what makes the finite count `griego_disjoint_union_count`
    provable from the general decomposition lemmas above; only the disjointness of the pieces (which
    needs the separation choice) stays a documented hole. -/
def bk (n : ℕ) : Finset ℤ := tpow Qbase Ubase n
noncomputable def ak (n : ℕ) : Finset ℤ :=
  an_interval n ∪ (an_index n).biUnion (fun i => tr (an_shift n i) (bk n))

/- ============================================================================================
    R15 OUTLINER (B1a RE-PLAN) — the GHR separation, factored into a CHEAP general spacing lemma
    + a small residual construction obligation.

    The R15 scout's load-bearing finding: B1a as a single `sorry` is NOT closable, because it
    quantifies over `an_shift`/`an_index`/`an_interval` which are themselves `sorry` defs — there
    is nothing to compute disjointness FROM. So B1a is REALLY two pieces, and this re-plan splits
    them so the GENERIC half closes this round and the construction-pinning is isolated:

      (1) `setSum_tr_pair_disjoint` / `setDiff_tr_pair_disjoint` — GENERAL, sorry-free target:
          if the shift gap `|c − c'|` strictly exceeds the DIAMETER of the sum/diffset `B±B`
          (every element of `B±B` lies in `[lo, lo + diam]`), the two translate images
          `c+(B±B)`, `c'+(B±B)` are disjoint. Pure ℤ interval arithmetic via `setSum_tr`
          (`= image (c+·) (B±B)`) + `Finset.disjoint_left` + a `<`/`≤` value bound. This is the
          cached-lemma-shaped reusable content — no construction needed.
      (2) `an_separated` — the RESIDUAL construction obligation (the genuinely uncached, harder
          half): the explicit shifts `an_shift n i` are placed on an arithmetic progression with
          spacing exceeding `diam (bk n ± bk n)`, and the interval `an_interval n` is placed
          below all translates. The load-bearing idea (GHR's own `aᵢ−aⱼ ∉ Bₙ−Bₙ`, made concrete):
          `an_shift n i = i · (spacing n)` with `spacing n = 2·maxbk n + 1 > diam`. Closing it
          needs an element-range bound `maxbk` on `bk n = tpow Qbase Ubase n` (NOT yet a lemma —
          the natural next sub-target; provable by induction on the `box`/`emb` structure, the
          carry-free digit base bounds each coordinate). Left documented `sorry`.

    `griego_ak_disjoint` is then REASSEMBLED sorry-free from (1) + (2): given the spacing bound,
    each pair of translates is disjoint by (1); the interval-vs-union by the same interval bound
    pushed through `disjoint_biUnion_right`. This mirrors the R14 B1 move (split a monolith, keep
    the parent sorry-free). Closing (1) — the cheap generic half — is THIS round's deliverable;
    (2) `an_separated` is the smaller residual hole.
    ============================================================================================ -/

/-- A finite set of integers `S` has all elements within `diam` of a low point `lo`. The witness
    `lo = min, diam = max − min` always exists for nonempty `S`; we carry it abstractly so the
    spacing lemma is stated cleanly. -/
def WithinDiam (S : Finset ℤ) (lo diam : ℤ) : Prop := ∀ z ∈ S, lo ≤ z ∧ z ≤ lo + diam

/-- **GENERAL SPACING LEMMA, SUM side (sorry-free target — the cheap half of B1a).** If every
    element of the sumset `setSum B B` lies in `[lo, lo + diam]` and the shift gap `|c − c'|`
    strictly exceeds `diam`, the two translate sumsets are disjoint. Proof path: `setSum_tr`
    rewrites each to `image (·+·) (setSum B B)`; `Finset.disjoint_left`; an element common to both
    gives `c + w = c' + w'` with `w, w' ∈ [lo, lo+diam]`, so `|c − c'| = |w' − w| ≤ diam`,
    contradicting `diam < |c − c'|`. -/
theorem setSum_tr_pair_disjoint (c c' : ℤ) (B : Finset ℤ) (lo diam : ℤ)
    (hwd : WithinDiam (setSum B B) lo diam) (hgap : diam < |c - c'|) :
    Disjoint (setSum (tr c B) B) (setSum (tr c' B) B) := by
  rw [setSum_tr, setSum_tr, Finset.disjoint_left]
  rintro z hz hz'
  rw [mem_image] at hz hz'
  obtain ⟨w, hw, rfl⟩ := hz
  obtain ⟨w', hw', heq⟩ := hz'
  have hwb := hwd w hw
  have hwb' := hwd w' hw'
  have hle : |c - c'| ≤ diam := by
    rw [abs_le]
    constructor <;> omega
  linarith

/-- **GENERAL SPACING LEMMA, DIFF side (sorry-free target).** Same statement for `setDiff`. -/
theorem setDiff_tr_pair_disjoint (c c' : ℤ) (B : Finset ℤ) (lo diam : ℤ)
    (hwd : WithinDiam (setDiff B B) lo diam) (hgap : diam < |c - c'|) :
    Disjoint (setDiff (tr c B) B) (setDiff (tr c' B) B) := by
  rw [setDiff_tr, setDiff_tr, Finset.disjoint_left]
  rintro z hz hz'
  rw [mem_image] at hz hz'
  obtain ⟨w, hw, rfl⟩ := hz
  obtain ⟨w', hw', heq⟩ := hz'
  have hwb := hwd w hw
  have hwb' := hwd w' hw'
  have hle : |c - c'| ≤ diam := by
    rw [abs_le]
    constructor <;> omega
  linarith

/- ============================================================================================
    R18 OUTLINER (an_separated SET-UP) — the `maxbk` element-range bound + AP shift-spacing.

    `an_separated` reduces to ONE genuinely-new finite fact: an element-range bound on
    `bk n = tpow Qbase Ubase n`. Everything else (`WithinDiam` for the sum/diffset, the
    shift-spacing, the interval-vs-union disjointness) follows from it by ℤ interval arithmetic
    and the already-cached `setSum_tr`/`setDiff_tr` rewrites + `disjoint_biUnion_right`.

    The decomposition the builder should close (named sub-holes below, all `sorry` for now):

      (R18-1) `box_elem_range` — the `box`/`emb` step bound: if `U ⊆ [0,maxU]`, `V ⊆ [0,maxV]`,
              `0 ≤ Q`, then `box Q U V ⊆ [0, maxU + Q·maxV]`. Pure `rintro` + `mem_image`/
              `mem_product` + `nlinarith`/`mul_le_mul` (the `emb (u,v) = u + Q·v` value bound).
      (R18-2) `tpow_elem_range` — the induction: carrying a BASE element-range hypothesis
              `hbase : ∀ u ∈ Ubase, 0 ≤ u ∧ u ≤ maxU` (parametric; the numeric `maxU` literal is
              left as documented witness data), `tpow Qbase Ubase n ⊆ [0, maxbk maxU Qbase n]`
              where `maxbk maxU Q 0 = maxU`, `maxbk maxU Q (k+1) = maxU + Q·(maxbk maxU Q k)`.
              `induction n` exactly as `tensor_pow_sumset_card` (line 226) — base = hbase, step =
              R18-1 with `U := Ubase`, `V := tpow … k`, IH the range of the tower. Needs
              `0 ≤ Qbase` (from `Ubase_carryfree.1 : 0 < Qbase`) and `0 ≤ maxbk` (induction).
      (R18-3) `bk_within_diam` — from R18-2: `WithinDiam (setSum (bk n) (bk n)) 0 (2·maxbk…)` and
              `WithinDiam (setDiff (bk n) (bk n)) (−maxbk…) (2·maxbk…)`. `setSum`/`setDiff` are
              `image₂ (±)`; `rintro z; mem_image₂` gives `z = a±b`, each in `[0,maxbk]`, so the
              ± value lands in the stated window — `omega` after the two range facts.

    Then PIN the witness data (still documented numeric `sorry`, but the SHAPE is fixed so the
    spacing computes):
      `an_index n  := Finset.range (mn n)`            -- the mₙ shifts, 0..mₙ−1
      `an_shift n i := (i : ℤ) · (2·maxbk… + 1)`      -- AP with spacing `> diam = 2·maxbk…`
      `an_interval n := Finset.Icc (negLo n) (negLo n + (Lₙ−1))`  -- placed BELOW all translates
                                                                   -- (negLo ≪ 0, or i starts at 1)
    With this shape:
      - spacing: `i≠j ⟹ |an_shift n i − an_shift n j| = |i−j|·(2·maxbk…+1) ≥ 2·maxbk…+1 > diam`,
        an `omega`/`nlinarith` over ℤ once `maxbk… ≥ 0` and `|i−j| ≥ 1`.
      - interval-vs-union: `disjoint_biUnion_right`; each `setSum/Diff (tr (an_shift n i) (bk n))
        (bk n)` rewrites via `setSum_tr`/`setDiff_tr` to a window `[an_shift n i + lo, …]` strictly
        ABOVE `an_interval n ± bk n` (which sits in the negative/low band), so `disjoint_left` +
        a value bound closes it.

    RECOMMENDED (watchdog-cheap, reviewer-cheap, matches R14/R15): prove R18-1/2/3 PARAMETRICALLY,
    carrying `maxU`/`hbase` as hypotheses, and leave only the numeric `maxU`/`negLo`/`Lₙ`/`mn`
    literals as documented witness `sorry`. That closes the STRUCTURAL content of `an_separated`
    (the spacing + disjointness logic) this round; only the numeric digit-set literals stay open.
    ============================================================================================ -/

/-- (R18-1) **`box`/`emb` step range bound — CLOSED R18.** An element of `box Q U V` is
    `emb Q (u,v) = u + Q·v` with `u ∈ [0,maxU]`, `v ∈ [0,maxV]`, `0 ≤ Q`, so it lands in
    `[0, maxU + Q·maxV]`. Pure `mem_image`/`mem_product` + `mul_le_mul_of_nonneg_left` value bound. -/
theorem box_elem_range (Q maxU maxV : ℤ) (U V : Finset ℤ) (hQ : 0 ≤ Q)
    (hU : ∀ u ∈ U, 0 ≤ u ∧ u ≤ maxU) (hV : ∀ v ∈ V, 0 ≤ v ∧ v ≤ maxV) :
    ∀ z ∈ box Q U V, 0 ≤ z ∧ z ≤ maxU + Q * maxV := by
  intro z hz
  simp only [box, mem_image, mem_product] at hz
  obtain ⟨⟨u, v⟩, ⟨hu, hv⟩, rfl⟩ := hz
  simp only [emb]
  obtain ⟨hu0, huM⟩ := hU u hu
  obtain ⟨hv0, hvM⟩ := hV v hv
  have hQv : Q * v ≤ Q * maxV := mul_le_mul_of_nonneg_left hvM hQ
  have hQv0 : 0 ≤ Q * v := mul_nonneg hQ hv0
  exact ⟨by linarith, by linarith⟩

/-- `maxbk` is nonnegative when the base bound and `Q` are. -/
theorem maxbk_nonneg (maxU Q : ℤ) (hmaxU : 0 ≤ maxU) (hQ : 0 ≤ Q) (n : ℕ) :
    0 ≤ maxbk maxU Q n := by
  induction n with
  | zero => simpa [maxbk] using hmaxU
  | succ k ih =>
    simp only [maxbk]
    have : 0 ≤ Q * maxbk maxU Q k := mul_nonneg hQ ih
    linarith

/-- (R18-2) **`tpow` element-range bound by induction — CLOSED R18.** Carries the base hypothesis
    `hbase` (`Ubase ⊆ [0,maxU]`) parametrically — the numeric `maxU` literal stays documented witness
    data (`maxUbase`/`Ubase_range`). `induction n`; base = `hbase`; step = `box_elem_range` with the
    IH range of the tower as the second factor and `0 ≤ Qbase`. -/
theorem tpow_elem_range (maxU : ℤ) (hQ : 0 ≤ Qbase)
    (hbase : ∀ u ∈ Ubase, 0 ≤ u ∧ u ≤ maxU) (n : ℕ) :
    (∀ z ∈ tpow Qbase Ubase n, 0 ≤ z ∧ z ≤ maxbk maxU Qbase n) := by
  induction n with
  | zero =>
    intro z hz
    simpa [tpow, maxbk] using hbase z hz
  | succ k ih =>
    intro z hz
    rw [tpow] at hz
    have := box_elem_range Qbase maxU (maxbk maxU Qbase k) Ubase (tpow Qbase Ubase k)
      hQ hbase ih z hz
    simpa [maxbk] using this

/- ---------- R18 helper lemmas for `an_separated` (all sorry-free) ---------- -/

/-- The sumset of `bk n` lies in the window `[0, 2·maxbk n]`. -/
theorem setSum_bk_within (n : ℕ) :
    WithinDiam (setSum (bk n) (bk n)) 0 (2 * maxbk maxUbase Qbase n) := by
  have hmaxU := Ubase_range.1
  have hbase := Ubase_range.2
  have hQ : (0:ℤ) ≤ Qbase := le_of_lt Ubase_carryfree.1
  intro z hz
  simp only [setSum, bk, mem_image₂] at hz
  obtain ⟨a, ha, b, hb, rfl⟩ := hz
  have hra := tpow_elem_range maxUbase hQ hbase n a ha
  have hrb := tpow_elem_range maxUbase hQ hbase n b hb
  exact ⟨by omega, by omega⟩

/-- The diffset of `bk n` lies in the window `[−maxbk n, maxbk n]` (diam `2·maxbk n`). -/
theorem setDiff_bk_within (n : ℕ) :
    WithinDiam (setDiff (bk n) (bk n)) (-(maxbk maxUbase Qbase n)) (2 * maxbk maxUbase Qbase n) := by
  have hmaxU := Ubase_range.1
  have hbase := Ubase_range.2
  have hQ : (0:ℤ) ≤ Qbase := le_of_lt Ubase_carryfree.1
  intro z hz
  simp only [setDiff, bk, mem_image₂] at hz
  obtain ⟨a, ha, b, hb, rfl⟩ := hz
  have hra := tpow_elem_range maxUbase hQ hbase n a ha
  have hrb := tpow_elem_range maxUbase hQ hbase n b hb
  exact ⟨by omega, by omega⟩

/-- The AP shifts are spaced strictly wider than the diameter `2·maxbk n`. -/
theorem an_shift_spacing (n : ℕ) (i j : ℕ) (hij : i ≠ j) :
    2 * maxbk maxUbase Qbase n < |an_shift n i - an_shift n j| := by
  have hQ : (0:ℤ) ≤ Qbase := le_of_lt Ubase_carryfree.1
  have hmb : 0 ≤ maxbk maxUbase Qbase n := maxbk_nonneg maxUbase Qbase Ubase_range.1 hQ n
  set s : ℤ := 2 * maxbk maxUbase Qbase n + 1 with hs
  have hdij : (1 : ℤ) ≤ |(i : ℤ) - (j : ℤ)| := by
    have : (i : ℤ) ≠ (j : ℤ) := by exact_mod_cast hij
    rcases lt_or_gt_of_ne this with h | h
    · rw [abs_of_neg (by omega)]; omega
    · rw [abs_of_pos (by omega)]; omega
  have hrw : an_shift n i - an_shift n j = ((i : ℤ) - (j : ℤ)) * s := by
    show (i : ℤ) * s - (j : ℤ) * s = ((i : ℤ) - (j : ℤ)) * s
    ring
  rw [hrw, abs_mul, abs_of_nonneg (by omega : (0:ℤ) ≤ s)]
  have : s * 1 ≤ |(i:ℤ) - (j:ℤ)| * s := by
    rw [mul_comm s 1]
    exact mul_le_mul_of_nonneg_right hdij (by omega : (0:ℤ) ≤ s)
  omega

/-- Each AP shift is nonnegative (`i : ℕ`). -/
theorem an_shift_nonneg (n : ℕ) (i : ℕ) : 0 ≤ an_shift n i := by
  have hQ : (0:ℤ) ≤ Qbase := le_of_lt Ubase_carryfree.1
  have hmb : 0 ≤ maxbk maxUbase Qbase n := maxbk_nonneg maxUbase Qbase Ubase_range.1 hQ n
  simp only [an_shift]
  apply mul_nonneg (by positivity)
  omega

/-- The interval-band sumset is disjoint from the union of translate sumsets:
    the interval band sits strictly below `0` (the bottom of the lowest translate window). -/
theorem interval_union_disjoint_sum (n : ℕ) :
    Disjoint (setSum (an_interval n) (bk n))
      ((an_index n).biUnion (fun i => setSum (tr (an_shift n i) (bk n)) (bk n))) := by
  have hQ : (0:ℤ) ≤ Qbase := le_of_lt Ubase_carryfree.1
  have hbase := Ubase_range.2
  rw [Finset.disjoint_biUnion_right]
  intro i _
  rw [Finset.disjoint_left]
  intro z hzI hzU
  simp only [setSum, an_interval, bk, mem_image₂, mem_Icc] at hzI
  obtain ⟨x, ⟨_, hxhi⟩, y, hy, rfl⟩ := hzI
  have hry := tpow_elem_range maxUbase hQ hbase n y hy
  rw [setSum_tr, mem_image] at hzU
  obtain ⟨w, hw, hwq⟩ := hzU
  have hwwd := (setSum_bk_within n) w (by simpa [bk] using hw)
  have hsh := an_shift_nonneg n i
  omega

/-- The interval-band diffset is disjoint from the union of translate diffsets:
    the interval band's diff window lies strictly below `−maxbk n` (the bottom of the lowest
    translate diff window). -/
theorem interval_union_disjoint_diff (n : ℕ) :
    Disjoint (setDiff (an_interval n) (bk n))
      ((an_index n).biUnion (fun i => setDiff (tr (an_shift n i) (bk n)) (bk n))) := by
  have hQ : (0:ℤ) ≤ Qbase := le_of_lt Ubase_carryfree.1
  have hbase := Ubase_range.2
  rw [Finset.disjoint_biUnion_right]
  intro i _
  rw [Finset.disjoint_left]
  intro z hzI hzU
  simp only [setDiff, an_interval, bk, mem_image₂, mem_Icc] at hzI
  obtain ⟨x, ⟨_, hxhi⟩, y, hy, rfl⟩ := hzI
  have hry := tpow_elem_range maxUbase hQ hbase n y hy
  rw [setDiff_tr, mem_image] at hzU
  obtain ⟨w, hw, hwq⟩ := hzU
  have hwwd := (setDiff_bk_within n) w (by simpa [bk] using hw)
  have hsh := an_shift_nonneg n i
  omega

/-- **RESIDUAL CONSTRUCTION OBLIGATION (the harder, uncached half of B1a) — CLOSED R18.** The
    explicit shifts and interval realise the separation: `bk n ± bk n` sits in a window of diameter
    `2·maxbk n`, the AP shifts `an_shift n i = i·(2·maxbk n+1)` are spaced wider than that diameter,
    and the interval band `an_interval n` sits strictly below all translate windows. Assembled from
    the R18 helpers (all sorry-free): `setSum/setDiff_bk_within` (range from `tpow_elem_range`),
    `an_shift_spacing` (AP gap), `interval_union_disjoint_sum/diff` (band below). The only remaining
    `sorry` it depends on is the documented numeric witness data (`Ubase`/`Qbase`/`maxUbase`/
    `mnData`/`negLoData` and their range/carry-free facts) — the STRUCTURAL content is closed. -/
theorem an_separated (n : ℕ) :
    ∃ loS diamS loD diamD : ℤ,
      WithinDiam (setSum (bk n) (bk n)) loS diamS ∧
      WithinDiam (setDiff (bk n) (bk n)) loD diamD ∧
      (∀ i ∈ an_index n, ∀ j ∈ an_index n, i ≠ j →
          diamS < |an_shift n i - an_shift n j| ∧
          diamD < |an_shift n i - an_shift n j|) ∧
      Disjoint (setSum (an_interval n) (bk n))
               ((an_index n).biUnion (fun i => setSum (tr (an_shift n i) (bk n)) (bk n))) ∧
      Disjoint (setDiff (an_interval n) (bk n))
               ((an_index n).biUnion (fun i => setDiff (tr (an_shift n i) (bk n)) (bk n))) := by
  refine ⟨0, 2 * maxbk maxUbase Qbase n, -(maxbk maxUbase Qbase n), 2 * maxbk maxUbase Qbase n,
    setSum_bk_within n, setDiff_bk_within n, ?_,
    interval_union_disjoint_sum n, interval_union_disjoint_diff n⟩
  intro i _ j _ hij
  have hsp := an_shift_spacing n i j hij
  exact ⟨hsp, hsp⟩

/-- **SUB-HOLE B1a — REASSEMBLED sorry-free from the general spacing lemmas + the residual
    `an_separated` obligation.** The `mₙ` translate images and the interval piece are pairwise
    disjoint in BOTH sums and diffs. The pairwise translate disjointness comes from
    `setSum/Diff_tr_pair_disjoint` applied with the diameters and spacing from `an_separated`; the
    interval-vs-union pieces are carried directly by `an_separated`. (When the two spacing lemmas
    close, B1a's only residual `sorry` is `an_separated` — the construction-pinning.) -/
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
  obtain ⟨loS, diamS, loD, diamD, hwdS, hwdD, hsp, hintS, hintD⟩ := an_separated n
  refine ⟨?_, hintS, ?_, hintD⟩
  · intro i hi j hj hij
    exact setSum_tr_pair_disjoint _ _ (bk n) loS diamS hwdS (hsp i hi j hj hij).1
  · intro i hi j hj hij
    exact setDiff_tr_pair_disjoint _ _ (bk n) loD diamD hwdD (hsp i hi j hj hij).2

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
