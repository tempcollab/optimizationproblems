/-
Sketch: ghr-lemma-lean  (constant 3a, LOWER bound -- the Lean-certifiable line)

TARGET (top-level theorem): a machine-checked lower bound

    1 + Real.log (diff / s) / Real.log q  >  1.1740744

for the explicit exact counts (s, diff, q) of the winning finite digit set U
(d = 84, T = 162, A = {0,2,3,...,10}, base 21) produced by the verified Python exact DP
(alphabet-search-dp WINNERS[(84,162)]).  This is the quantity

    theta := 1 + log(|U-U| / |U+U|) / log(2*max(U) + 1)

of the GHR2007 single-set lemma, so the theorem certifies C_3a >= theta > 1.1740744 for
that construction.  (The R2 numerical certificate gives theta = 1.1744750903655619; the
machine-checked claim here is the strictly weaker, hole-free 1.1740744 -- still a strict
improvement on the published record 1.1740744 is NOT what this proves; see commentary: the
top-level theorem proves > 1.1740744, which equals the published record value, while the
*verified held* numerical bound is 1.17447509.  The Lean theorem is the gold-standard
*certificate of the construction*; the held numerical value is unchanged.)

DESIGN (keep the heavy DP OUT of the kernel): the three counts s, diff, q are produced and
checked by the trusted Python DP (certificate/ghr_dp.py).  In Lean we take them as given Nat
literals (the cheap path) and prove the final inequality.  The inequality

    1 + log(diff/s)/log q > 1.1740744

is reduced to a PURE INTEGER inequality with NO logs:

    log(diff/s)/log q >= 15/86            (since 15/86 = 0.174418... > 0.1740744)
  <=> 86 * log(diff/s) >= 15 * log q       (log q > 0)
  <=> log( (diff/s)^86 ) >= log( q^15 )
  <=> (diff/s)^86 >= q^15                  (log strictly monotone)
  <=> diff^86 >= s^86 * q^15               (clear denominators; s,q > 0)

The last line is a comparison of two ~8700-digit Nats, discharged by `decide` in the kernel
(no `sorry`, no axiom).  15/86 was chosen as the smallest-denominator rational strictly
between the record threshold 0.1740744 and the true ratio 0.17447509.
-/

import Mathlib

namespace C3a

/-- The three exact counts for the WINNING finite set U (d=84, T=162, A={0,2..10}, base 21),
    from the validated Python exact DP (alphabet-search-dp WINNERS[(84,162)]).
    s = |U+U|, diff = |U-U|, q = 2*max(U)+1. -/
def sUpU  : ℕ := 6097708534951589347439183607038270910158216193597072358058994024712092458076766270
def dUmU  : ℕ := 145710369635805984294872090934229656671521875518799257570738793680742528284363557961708618559623567675
def qMaxU : ℕ := 1165254416489684872554618217361872378435684345652187969599710464819025051454571621932090673372945921527696090485

/-- The load-bearing INTEGER inequality (the only "hard" computation, done by the kernel).
    `diff^86 >= s^86 * q^15`.  Equivalent to `(diff/s)^86 >= q^15`, the power form of the
    log inequality `log(diff/s)/log q >= 15/86`. -/
theorem power_ineq : sUpU ^ 86 * qMaxU ^ 15 ≤ dUmU ^ 86 := by
  unfold sUpU qMaxU dUmU
  decide

/-- Positivity facts about the counts. -/
theorem sUpU_pos  : 0 < sUpU  := by unfold sUpU;  decide
theorem dUmU_pos  : 0 < dUmU  := by unfold dUmU;  decide
theorem qMaxU_ge_two : 2 ≤ qMaxU := by unfold qMaxU; decide

/-- H3 / TOP-LEVEL THEOREM (machine-checked, hole-free).
    `1 + log(diff/s)/log q > 1.1740744` for the winning counts. -/
theorem beats_record :
    (1 : ℝ) + Real.log ((dUmU : ℝ) / (sUpU : ℝ)) / Real.log (qMaxU : ℝ) > 1.1740744 := by
  -- positivity of the reals
  have hs : (0 : ℝ) < (sUpU : ℝ) := by exact_mod_cast sUpU_pos
  have hd : (0 : ℝ) < (dUmU : ℝ) := by exact_mod_cast dUmU_pos
  have hq2 : (2 : ℝ) ≤ (qMaxU : ℝ) := by exact_mod_cast qMaxU_ge_two
  have hq1 : (1 : ℝ) < (qMaxU : ℝ) := lt_of_lt_of_le (by norm_num) hq2
  have hq0 : (0 : ℝ) < (qMaxU : ℝ) := lt_trans (by norm_num) hq1
  -- log q > 0
  have hlogq : 0 < Real.log (qMaxU : ℝ) := Real.log_pos hq1
  -- the power inequality in ℝ: (diff)^86 >= (s)^86 * (q)^15
  have hpow : (sUpU : ℝ) ^ 86 * (qMaxU : ℝ) ^ 15 ≤ (dUmU : ℝ) ^ 86 := by
    have := power_ineq
    have hcast : ((sUpU ^ 86 * qMaxU ^ 15 : ℕ) : ℝ) ≤ ((dUmU ^ 86 : ℕ) : ℝ) := by
      exact_mod_cast this
    push_cast at hcast
    linarith [hcast]
  -- take logs:  log( s^86 * q^15 ) <= log( diff^86 )
  have hlhs_pos : (0 : ℝ) < (sUpU : ℝ) ^ 86 * (qMaxU : ℝ) ^ 15 :=
    mul_pos (pow_pos hs 86) (pow_pos hq0 15)
  have hlog_le : Real.log ((sUpU : ℝ) ^ 86 * (qMaxU : ℝ) ^ 15)
                  ≤ Real.log ((dUmU : ℝ) ^ 86) :=
    Real.log_le_log hlhs_pos hpow
  -- expand the logs:  86*log s + 15*log q <= 86*log diff
  rw [Real.log_mul (by positivity) (by positivity),
      Real.log_pow, Real.log_pow, Real.log_pow] at hlog_le
  -- hlog_le : 86 * log s + 15 * log q <= 86 * log diff
  -- rearrange to: 86*(log diff - log s) >= 15*log q
  have hsub : (15 : ℝ) * Real.log (qMaxU : ℝ)
                ≤ 86 * (Real.log (dUmU : ℝ) - Real.log (sUpU : ℝ)) := by
    push_cast at hlog_le ⊢
    linarith [hlog_le]
  -- log(diff/s) = log diff - log s
  have hlogdiv : Real.log ((dUmU : ℝ) / (sUpU : ℝ))
                  = Real.log (dUmU : ℝ) - Real.log (sUpU : ℝ) :=
    Real.log_div (ne_of_gt hd) (ne_of_gt hs)
  -- so 86 * log(diff/s) >= 15 * log q, hence log(diff/s)/log q >= 15/86
  have hratio : (15 : ℝ) / 86 ≤ Real.log ((dUmU : ℝ) / (sUpU : ℝ)) / Real.log (qMaxU : ℝ) := by
    rw [hlogdiv]
    rw [div_le_div_iff₀ (by norm_num) hlogq]
    -- 15 * log q <= (log diff - log s) * 86
    nlinarith [hsub]
  -- 1 + 15/86 = 1.17441... > 1.1740744
  have : (1 : ℝ) + 15 / 86 ≤ 1 + Real.log ((dUmU : ℝ) / (sUpU : ℝ)) / Real.log (qMaxU : ℝ) := by
    linarith [hratio]
  have hnum : (1.1740744 : ℝ) < 1 + 15 / 86 := by norm_num
  linarith [this, hnum]

end C3a
