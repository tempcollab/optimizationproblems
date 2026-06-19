/-
Sketch: ghr-lemma-lean  (constant 3a, LOWER bound -- the Lean-certifiable line)

TARGET (top-level theorem): a machine-checked
    C_3a >= 1 + log(|U-U| / |U+U|) / log(2 * maxU + 1)  >  1.1740744
for an explicit finite digit set U (the winning (A,d,T) from alphabet-search-dp).

WHY LEAN-FIT (explorer's headline reason to pick 3a): the load-bearing step is EXACT
integer counting of |U+U|, |U-U|, maxU plus ONE rational log inequality -- no continuum
estimate, no SDP, no quadrature.  Lean's arbitrary-precision `Nat` handles the (astronomical
but exact) counts; the inequality goes through `Mathlib`'s `Real.log` lemmas.

DESIGN (keep the heavy DP OUT of the kernel): the three counts are produced and checked by
the trusted Python DP (certificate/ghr_dp.py, validated against the record). In Lean we
either (cheap path) take them as given Nat literals and prove only the final inequality, or
(full path) re-derive them via a Lean `Decide`/computed DP. The cheap path already yields a
real machine-checked theorem about the inequality `theta(s, diff, q) > 1.1740744`; the full
path additionally certifies the counts inside Lean.

HOLES:
  (H0) BOOTSTRAP: create the Lake project at constants/3a/lean/ (math template), pin
       lean-toolchain + Mathlib rev, `lake exe cache get`, `lake build` green. (Builder.)
  (H1) GHR LEMMA: `theorem ghr_single_set (U : Finset Nat) (h0 : 0 in U) ... :
       C_3a >= 1 + Real.log (|U-U|/|U+U|) / Real.log (2*maxU+1)`. Either prove the
       projection construction or take it as the imported cached lemma (lemmas/). This is the
       reusable core every Lean sketch wants in lemmas/.
  (H2) EXACT COUNTS: the winning U's |U+U|, |U-U|, maxU as `Nat` (literals from ghr_dp, or a
       Lean-internal computation). For the cheap path these are `def`s; sorry = the claim
       that they equal the DP output.
  (H3) LOG INEQUALITY: `Real.log (diff / s) - 0.1740744 * Real.log q > 0` via a rational
       lower bound (atanh series / `norm_num` extended), the load-bearing rigor step.

This file currently uses `sorry` for every hole. It is the SKELETON; it compiles green only
after H0 (the Lake/Mathlib bootstrap) -- until then it documents the target and holes.
Builder: do H0 first, then this file `lake build`s with the sorries.
-/

-- import Mathlib    -- (uncomment after H0 bootstrap)

namespace C3a

/-- The three exact counts for the winning finite set U (from the Python exact DP).
    Placeholders = Griego's record values; replace with the >1.1740744 winner. -/
def sUpU  : Nat := 75448362167176243488362019935078206851619643198150854886920234689186981134888
def dUmU  : Nat := 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415
def qMaxU : Nat := 1  -- HOLE H2: 2*max(U)+1 for the winner (literal too long to inline here)

/-
HOLE H1 (cached GHR single-set lemma -- target shape):

theorem ghr_single_set
    (U : Finset Nat) (h0 : (0 : Nat) ∈ U)
    (hq : (U - U).card ≤ 2 * U.max' _ + 1) :
    C3aConst ≥ 1 + Real.log ((U - U).card / (U + U).card) / Real.log (2 * U.max' _ + 1) :=
  sorry

HOLE H3 (the load-bearing inequality):

theorem beats_record :
    1 + Real.log ((dUmU : ℝ) / sUpU) / Real.log (qMaxU : ℝ) > 1.1740744 :=
  sorry
-/

end C3a
