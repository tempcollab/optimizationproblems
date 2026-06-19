import Mathlib

/-!
# A machine-checked lower bound on the continuum (interval-ln) endpoint of the
  Gyarmati–Hennecart–Ruzsa sum-difference constant `C_3a`.

This file formalises the *continuum endpoint* step of the numerical lower-bound
certificate for `C_3a` (see `constants/3a/certificate/certify_3a.py`).

## What the numerical certificate establishes (out of Lean)

The GHR2007 lemma (`constants/3a/literature/GHR2007_lemma.md`): for any finite set
`U ⊆ ℕ` with `0 ∈ U`,
  `C_3a ≥ θ(U) = 1 + ln(|U−U| / |U+U|) / ln(2·max(U)+1)`.
For the verified `d = 110, T = 210` instance of the base-21 drop-1 digit family, the
exact-integer dynamic-programming certificate computes (as exact big integers, no floats):
  `S = |U+U|`, `D = |U−U|`, `m = max(U)`, `q = 2m+1`.
These three integer literals — and only these — are carried into Lean below. The DP
*counting* of `S`, `D`, `m` stays the numerical certificate; it is **not** re-done here.

## What THIS Lean file proves (the endpoint, fully inside the formalisation)

Taking `S`, `D`, `q` as the literal integers from the verified certificate, we prove
  `1 + Real.log (D / S) / Real.log q ≥ 1 + 7/40 = 1.175`,
a value that strictly exceeds the published table record `1.1740744` [G2026].

The load-bearing step is reduced — with **no** `exp`/`log` numeric bounds, no `sorry`,
no extra axiom — to the *purely algebraic integer inequality*
  `S^40 * q^7 ≤ D^40`,
which `norm_num` decides on the exact big integers. The reduction uses only the strict
monotonicity of `Real.log` (`Real.log_le_log`) and positivity of `Real.log q` (since
`q > 1`). This is the discrete/algebraic shape that Lean certifies cleanly:
`7/40 ≤ log(D/S)/log q  ⟺  q^7 ≤ (D/S)^40  ⟺  S^40·q^7 ≤ D^40`.

This `1.175` bound is *below* our reviewer-verified held value `1.1760055927978140`
(also a `d=110` value); it does **not** raise `held`. It banks a machine-checked
proof of the easy (continuum) half of the certificate as a `lake build`-checkable
theorem — the gold-standard hardening track.
-/

open Real

namespace C3a

/-- Exact integer literals from the reviewer-verified `d = 110, T = 210` certificate
(`certify_3a.py 110 210`, base 21, `A = {0,2,…,10}`, drop-1 digit family).
`S = |U+U|`, `D = |U−U|`, `q = 2·max(U)+1`. -/
def S : ℕ := 92705280150149557241060040925257650294778564084075401198748837829236511291636097166290731809667005452395284
def D : ℕ := 3681997220096007623545821167575964274432148557703482564789415590948047764144361920922788745648782524799208324807660608218695537922441
def q : ℕ := 27804969353190843603887312343733914954255006183601562188635147416873153704400464342290533460390401248073717172969344053559018098633273404332320021

/-- **Reduction lemma.** For positive reals `S, D` and `q > 1`, the integer-power
inequality `q^7 ≤ (D/S)^40` already forces the rational lower bound `7/40` on the
endpoint ratio `log(D/S)/log q`. Proof: take logs (strict monotonicity of `Real.log`),
use `log (x^n) = n · log x`, and divide by the positive quantity `log q`. -/
theorem ratio_ge_of_pow
    {S D q : ℝ} (hS : 0 < S) (hD : 0 < D) (hq : 1 < q)
    (hpow : (q : ℝ) ^ (7 : ℕ) ≤ (D / S) ^ (40 : ℕ)) :
    (7 : ℝ) / 40 ≤ Real.log (D / S) / Real.log q := by
  have hlogq : 0 < Real.log q := Real.log_pos hq
  have hDSpos : 0 < D / S := div_pos hD hS
  have hmono : Real.log ((q : ℝ) ^ (7 : ℕ)) ≤ Real.log ((D / S) ^ (40 : ℕ)) :=
    Real.log_le_log (by positivity) hpow
  rw [Real.log_pow, Real.log_pow] at hmono
  have h7 : (7 : ℝ) * Real.log q ≤ (40 : ℝ) * Real.log (D / S) := by exact_mod_cast hmono
  rw [div_le_div_iff₀ (by norm_num) hlogq]
  linarith

/-- The exact-integer core: the algebraic inequality `S^40 · q^7 ≤ D^40` on the
verified literals, decided by `norm_num`. This is the only computational step. -/
theorem pow_ineq : S ^ 40 * q ^ 7 ≤ D ^ 40 := by
  unfold S D q
  norm_num

/-- **Main endpoint theorem.** The GHR2007 endpoint formula evaluated at the verified
`d = 110` integer literals satisfies
  `1 + log(D/S) / log q ≥ 1.175`,
strictly above the table record `1.1740744` [G2026]. Fully machine-checked: the DP
counts `S, D, q` enter as literals, and the inequality rests only on the algebraic
fact `pow_ineq` plus monotonicity of `log`. -/
theorem theta_endpoint_ge :
    (1 : ℝ) + Real.log ((D : ℝ) / (S : ℝ)) / Real.log (q : ℝ) ≥ 1 + 7 / 40 := by
  have hS : (0 : ℝ) < (S : ℝ) := by unfold S; norm_num
  have hD : (0 : ℝ) < (D : ℝ) := by unfold D; norm_num
  have hq : (1 : ℝ) < (q : ℝ) := by unfold q; norm_num
  -- lift the integer inequality `S^40 * q^7 ≤ D^40` to `q^7 ≤ (D/S)^40`
  have hpowℕ : S ^ 40 * q ^ 7 ≤ D ^ 40 := pow_ineq
  have hpowℝ : ((S : ℝ)) ^ 40 * (q : ℝ) ^ 7 ≤ (D : ℝ) ^ 40 := by exact_mod_cast hpowℕ
  have hSpow : (0 : ℝ) < (S : ℝ) ^ 40 := by positivity
  have hpow : (q : ℝ) ^ (7 : ℕ) ≤ ((D : ℝ) / (S : ℝ)) ^ (40 : ℕ) := by
    rw [div_pow]
    rw [le_div_iff₀ hSpow]
    linarith
  have := ratio_ge_of_pow hS hD hq hpow
  linarith

/-- Numerically, `1 + 7/40 = 1.175 > 1.1740744`, the published record [G2026]. -/
theorem theta_endpoint_beats_record :
    (1 : ℝ) + Real.log ((D : ℝ) / (S : ℝ)) / Real.log (q : ℝ) > 1.1740744 := by
  have h := theta_endpoint_ge
  norm_num at h ⊢
  linarith

end C3a
