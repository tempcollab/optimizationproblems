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

/-- ============================================================================================
    HOLE B — THE READ-OFF (the genuine remaining content): the Griego tensor family realizes the
    certified exponent `theta`, via the GHR COMPOSITE witness (NOT the bare tensor power — the
    bare power violates clause (i); see the header). Concretely the witness is

        B n := U^{⊗n}  (cached `tensor-multiplicativity`: |U^{⊗n} ± U^{⊗n}| = |U±U|^n),
        A n := [1, Lₙ] ∪ ⋃_{i=1}^{mₙ} (aᵢ + B n),  mₙ ≈ qⁿ/sⁿ,  Lₙ ≈ qⁿ/(K−1),

    for which clause (i) `|A n + B n| ≤ K·|A n|` holds with a FIXED K and clause (ii)
    `|A n + B n|^θ ≤ |A n − B n|` holds with θ = 1 + log(D/S)/log Q. Uses the cached
    `tensor_pow_*_card` lemmas (for the Bₙ-cardinalities) PLUS the dilution combinatorics (the m
    translates + interval bounding the doubling) PLUS reconciling θ = 1 + log(D/S)/log Q with the
    cleared predicate exponent. This is the multi-round real-analysis + combinatorics piece, left
    as a documented `sorry` so the reviewer can first rule the DEFINITION above in/out.

    `theta` is the certified real exponent from `NativeDecideSmallMT` (θ > 1.1771). -/
theorem griego_realizes : Realizes theta := by
  sorry

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
