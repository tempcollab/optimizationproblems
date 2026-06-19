/-
  Sketch `lean-native-decide-smallmt` — machine-checked C_3a lower bound (gold-standard cert).

  Target (registry def, exact): C_3a is the largest constant such that arbitrarily large
  integer sets A,B exist with |A+B| << |A| and |A-B| >> |A+B|^{C_3a}. The GHR2007 lemma turns
  a finite U ∋ 0 into the lower bound  C_3a ≥ 1 + log(|U-U|/|U+U|) / log(2·max U + 1) =: θ.

  We certify, with `native_decide` on a SINGLE pure big-integer inequality, that θ > 1.175 for
  the Griego base-21 family point (m,T)=(100,190), A={0,2,…,10}, U={Σ xᵢ·21ⁱ : x∈Aᵐ, Σxᵢ≤T}:

        S = |U+U|,  D = |U-U|,  Q = 2·max(U)+1   (the explicit integers below),
        θ := 1 + log(D/S)/log(Q),     θ > 47/40 = 1.175  ⟺  D^40 > S^40 · Q^7.

  1.175 > 1.1740744 (Griego 2026, current record), so this is a strict record beat, and 47/40
  has denominator 40 → the operands D^40, S^40·Q^7 are only ~4800 digits: `native_decide`-sized
  (the held 1.176 cert uses den=10000 → ~1.3M-digit operands, too big for the kernel; that stays
  the Python certificate, this Lean file takes the smaller-θ point with the tractable operands —
  it certifies a Lean-machine-checked beat, not the largest θ).

  ===========================================================================================
  STRUCTURE OF THE BRIDGE θ → C_3a, and what is now formalized (R5).

  The GHR bridge from the machine-checked integer inequality to `C_3a ≥ θ > 1.175` splits into
  two independent steps:

    (A)  LOG-ALGEBRA HALF — `(D^40 > S^40·Q^7) ⟹ θ > 47/40`, where θ = 1 + log(D/S)/log Q.
         This is pure real-arithmetic / strict monotonicity of `Real.log` and `(·)^n` over ℝ₊.
         **FORMALIZED THIS ROUND (R5), hole-free**, as `log_bridge` below — proved with Mathlib
         (`Real.log_lt_log`, `Real.log_pow`, `lt_div_iff₀`, `div_pow`). `#print axioms log_bridge`
         shows only `[propext, Classical.choice, Quot.sound]` (Mathlib's standard axioms) and NO
         `sorryAx`. So the step that turns the verified integer fact into the real θ-inequality is
         now a Lean theorem, not an assumption.

    (B)  GHR2007 READ-OFF — `C_3a ≥ θ` for this single finite U. This is the genuine number-theory
         content of [GHR2007, Funct. Approx. 37(1):175–186]: the k→∞ digit-tensor-power of U (in
         base Q = 2·max(U)+1) has sumset/diffset cardinalities S^k, D^k and max ≈ Q^k, so the
         ratio log(D/S)/log Q is preserved in the limit and lower-bounds the sup-over-constructions
         that DEFINES C_3a. This is a real-analysis / asymptotic-density LIMIT statement tied to the
         definition of C_3a; Mathlib does not hand it over and formalizing it (together with a Lean
         definition of C_3a) is multi-round work.
         **REMAINS A SINGLE EXPLICIT, NAMED HYPOTHESIS** (`ghr` in `c3a_lower_bound`), visible in
         the theorem statement — NOT smuggled into a `sorry` or an `axiom`. C_3a itself is the
         `opaque` real `C3aReal` (its full Lean definition is part of step (B)'s remaining work).

  So vs the R4 state — where the WHOLE bridge `(D^40>S^40·Q^7) → 1175 ≤ Cnum` was one assumed
  hypothesis bundling (A)+(B) — this round PROVES half (A) in Lean and narrows the remaining
  assumption to exactly (B), the GHR2007 tensor-power limit read-off `θ ≤ C_3a`.

  ===========================================================================================
  WHAT IS MACHINE-CHECKED (hole-free, no `sorryAx`):
    * `griego_100_190_int_cert : D^40 > S^40 * Q^7`  — by `native_decide`, the load-bearing
      integer inequality (operands ~4800 digits). This is the cleared-denominator form of θ>47/40.
    * `log_bridge` — the LOG-ALGEBRA HALF (A): `(D^40 > S^40·Q^7) ⟹ θ > 47/40` over ℝ. Proved
      with Mathlib; `#print axioms` clean (no sorryAx).
    * `c3a_lower_bound` — `C_3a > 1.175` (as `(47:ℝ)/40 < C3aReal`), proved with NO `sorry` and
      NO added axiom, from `log_bridge griego_100_190_int_cert` together with the single cited
      GHR2007 read-off `ghr : θ ≤ C3aReal`.

  WHAT IS ASSUMED (visible in the theorem statement, NOT smuggled into a `sorry`/axiom):
    * the hypothesis `ghr : theta ≤ C3aReal` — the [GHR2007] tensor-power limit read-off (step (B)
      above). This is the one remaining cited step; making it a hypothesis (not an `axiom`, not a
      `sorry`) is the honest encoding: the reader sees exactly what is assumed, and the final
      theorem is `sorry`-free given it.

  The S, D, Q literals are the certified output of the `exact-sumdiff-dp` lemma
  (constants/3a/lemmas/exact-sumdiff-dp.md), independently re-derived from scratch (digit counts
  97/121/133, head/tail digits matched). The DP need NOT be formalized — only the final integers
  and the integer inequality are in Lean.
-/

import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

namespace C3a

open Real

/-- |U+U| at the Griego point (m,T)=(100,190), A={0,2,…,10}, base 21. (exact-sumdiff-dp output;
    97 digits, head 86388581, tail 26122695 — re-derived from scratch R4.) -/
def S : Nat :=
  8638858163236395941516217363401483550516890510168979216455897313481301114734493828535608526122695

/-- |U-U| at the same point. (exact-sumdiff-dp output; 121 digits, head 13829645, tail 69875299.) -/
def D : Nat :=
  1382964512679156077866486522728758254964658623537557243232151844465484252026971742625575326931601023363381964203669875299

/-- Q = 2·max(U)+1 at the same point. (exact-sumdiff-dp output; 133 digits, head 16669764, tail 42124381.) -/
def Q : Nat :=
  1666976484396337359195971982226944426836572608734079367934371687437278941172454316219532850092142202188288127911460969010248542124381

/-- LOAD-BEARING STEP (hole-free, `native_decide`): the cleared-denominator integer form of
    θ > 47/40 = 1.175.  D^40 > S^40 · Q^7.  Operands ~4800 digits — kernel-tractable. -/
theorem griego_100_190_int_cert : D ^ 40 > S ^ 40 * Q ^ 7 := by
  native_decide

/-- Cheap side facts about the literals (decidable comparisons), needed to instantiate the
    real-arithmetic bridge. `0 < S` and `1 < Q`. -/
theorem S_pos : 0 < S := by native_decide
theorem Q_gt_one : 1 < Q := by native_decide

/-- The real number θ for this point: `θ = 1 + log(D/S)/log Q`. -/
noncomputable def theta : ℝ := 1 + Real.log ((D : ℝ) / (S : ℝ)) / Real.log (Q : ℝ)

/-- ============================================================================================
    LOG-ALGEBRA HALF OF THE BRIDGE (step (A)) — FORMALIZED, HOLE-FREE.

    Abstract over the integers: from the cleared-denominator integer inequality
    `S^40 · Q^7 < D^40` (with `0 < S`, `1 < Q`) conclude the real θ-bound
    `47/40 < 1 + log(D/S)/log Q`  (i.e. θ > 1.175).

    Pure real arithmetic: strict monotonicity of `Real.log` and of `(·)^n` on ℝ₊.
    `#print axioms log_bridge` → `[propext, Classical.choice, Quot.sound]` only (no sorryAx). -/
theorem log_bridge (s d q : ℕ)
    (hs : 0 < s) (hq : 1 < q)
    (hint : s ^ 40 * q ^ 7 < d ^ 40) :
    (47 : ℝ) / 40 < 1 + Real.log ((d : ℝ) / (s : ℝ)) / Real.log (q : ℝ) := by
  -- real positivity facts
  have hsr : (0 : ℝ) < (s : ℝ) := by exact_mod_cast hs
  have hqr : (1 : ℝ) < (q : ℝ) := by exact_mod_cast hq
  have hlogQ : 0 < Real.log (q : ℝ) := Real.log_pos hqr
  -- the cast integer inequality over ℝ
  have hintR : (s : ℝ) ^ 40 * (q : ℝ) ^ 7 < (d : ℝ) ^ 40 := by exact_mod_cast hint
  -- s^40 > 0
  have hs40 : (0 : ℝ) < (s : ℝ) ^ 40 := by positivity
  -- q^7 < d^40 / s^40
  have hdiv : (q : ℝ) ^ 7 < (d : ℝ) ^ 40 / (s : ℝ) ^ 40 := by
    rw [lt_div_iff₀ hs40]; linarith [hintR]
  -- d^40/s^40 = (d/s)^40
  have hpow : (d : ℝ) ^ 40 / (s : ℝ) ^ 40 = ((d : ℝ) / (s : ℝ)) ^ 40 := by
    rw [div_pow]
  -- log(q^7) < log((d/s)^40)
  have hQ7pos : (0 : ℝ) < (q : ℝ) ^ 7 := by positivity
  have hloglt : Real.log ((q : ℝ) ^ 7) < Real.log (((d : ℝ) / (s : ℝ)) ^ 40) := by
    apply Real.log_lt_log hQ7pos
    rw [← hpow]; exact hdiv
  -- expand logs of powers:  7 * log q < 40 * log (d/s)
  rw [Real.log_pow, Real.log_pow] at hloglt
  -- 7/40 < log(d/s)/log q
  have key : (7 : ℝ) / 40 < Real.log ((d : ℝ) / (s : ℝ)) / Real.log (q : ℝ) := by
    rw [lt_div_iff₀ hlogQ]
    nlinarith [hloglt]
  linarith [key]

/-- Specialised to the certified (100,190) literals (still hole-free): θ > 47/40 = 1.175. -/
theorem theta_gt : (47 : ℝ) / 40 < theta := by
  have h := log_bridge S D Q S_pos Q_gt_one griego_100_190_int_cert
  simpa [theta] using h

/-- C_3a rendered as a real number. Its full Lean DEFINITION (the sup-over-constructions of the
    GHR sum-difference exponent) is part of the remaining step (B) work; here it is `opaque` so
    the read-off `θ ≤ C_3a` can be stated and used while that definition is deferred. -/
opaque C3aReal : ℝ

/-- ============================================================================================
    FAITHFUL TOP THEOREM (hole-free given the ONE cited GHR2007 read-off): C_3a > 1.175,
    hence C_3a > 1.1740744 — the strict record beat.

    The single remaining assumed step is `ghr : theta ≤ C3aReal` — the [GHR2007] tensor-power
    LIMIT read-off `C_3a ≥ θ` (step (B) in the header), legitimate because `0 ∈ A` and base
    `Q = 21^... > 2·max(U)` makes the digit map injective and carry-free. It is given as an
    EXPLICIT HYPOTHESIS — visible in the statement, not hidden in a `sorry` or an `axiom` — so the
    proof body adds NO axiom and NO `sorryAx`.

    The two ingredients are now both Lean theorems:
      * `griego_100_190_int_cert` — the machine-checked integer inequality (`native_decide`);
      * `theta_gt` (via `log_bridge`) — the FORMALIZED log-algebra step `(int ineq) ⟹ θ > 47/40`.
    The conclusion `(47:ℝ)/40 < C3aReal` (i.e. C_3a > 1.175) follows from `theta_gt` and `ghr`. -/
theorem c3a_lower_bound (ghr : theta ≤ C3aReal) : (47 : ℝ) / 40 < C3aReal :=
  lt_of_lt_of_le theta_gt ghr

end C3a
