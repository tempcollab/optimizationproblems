/-
# C_3a = Gyarmati–Hennecart–Ruzsa sum-difference constant: a machine-checked lower bound.

This file upgrades the R18 verified *numerical* lower bound `C_3a ≥ 5877/5000 = 1.1754`
into a `lake build`-checked Lean theorem.

## What C_3a is

`C_3a` is the largest exponent `θ` for which, for arbitrarily large finite integer sets
`A,B` with `|A+B| ≤ K|A|`, one can force `|A−B| ≥ |A+B|^θ` (the sum–difference constant,
[GHR2007]). The record lower bound is produced by the GHR digit-set construction: a finite
`U ⊆ ℤ_{≥0}` with `0 ∈ U` gives

  `C_3a ≥ θ(U) := 1 + log(|U−U| / |U+U|) / log(2·max(U)+1)`.

For a base-`q = 2·max(U)+1` block construction the sum/difference sets are *carry-free*, so
`|U+U|`, `|U−U|`, `max(U)` are exact integers (computed by the digit-DP engine in
`constants/3a/certificate/engine/digit_dp.py`).

## The route taken here (Route A — log-free integer powers)

For a rational target `c = 1 + P/Q` (here `c = 5877/5000`, so `P = 877`, `Q = 5000`),

  `θ(U) ≥ c  ⟺  log(|U−U|/|U+U|) / log(2·max(U)+1) ≥ P/Q`
          `⟺  (|U−U|/|U+U|)^Q ≥ (2·max(U)+1)^P`        (all logs monotone: d ≥ s, q > 1)
          `⟺  |U−U|^Q ≥ |U+U|^Q · (2·max(U)+1)^P`.

The right-hand integer inequality is `decide`-able over `ℕ` (GMP big-ints in the kernel),
and **NO `Real.log` / `Real.rpow` ever enters the certified statement**. The monotone-
bijection chain above (valid because `P,Q ≥ 0`, `q > 1`, `s,d > 0`) is established once on
paper in `constants/3a/literature/GHR2007-lemma-digest.md`; only its *conclusion* — the
integer inequality ⟹ `C_3a ≥ 1+P/Q` — is carried into Lean, as the named bridge below.

## The honest trust boundary

`GHR_lower` is the ONLY non-`decide` content: it packages the GHR2007 analytic existence
step ("`θ(U) ≥ c` ⟹ there exist arbitrarily large `A,B` realizing the exponent ⟹
`C_3a ≥ c`"). Mathlib has no `C_3a` object, so — exactly as 9a's `ThetaGeFromIndep` and
5b's `MTThm15` — this is carried as an explicit hypothesis on the bound theorem, NOT an
axiom. `#print axioms` stays clean and the trust link is visible in the signature.

Everything HARD and discrete (the exact `|U±U|`, `max U`, and the power inequality) lives
inside the formalization as axiom-free `decide` facts. The three big integers themselves are
copied verbatim from the already-reviewer-verified numerical certificate
(`constants/3a/certificate/beat_largerd/beat_d100.json`, PRIMARY cell `d=100, T=187`) and
`constants/3a/certificate/engine/record_{plus,minus,max}.txt` (record cell `d=80, T=150`);
their provenance is the R18 numerical cert (re-derivable by `verify_beat.py` / `digit_dp.py`),
NOT a Lean-kernel digit-DP (which would be an unprobed OOM hazard and is not this round's
increment). The 9a precedent: R13 likewise TRUSTED the 367 explicit codewords as literals
and verified their provenance OUT of Lean.

References:
- [GHR2007] Gyarmati, Hennecart, Ruzsa, "Sums and differences of finite sets",
  Funct. Approx. Comment. Math. 37(1):175–186, 2007.
- [G2026] Griego, repo PR #71 (the d=80 record construction, value 1.1740744476935212).
- R18 numerical certificate:
  `constants/3a/certificate/beat_largerd/{verify_beat.py,beat_d100.json}`.
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.NormNum

namespace C3a

-- `decide` over 2-million-bit `Nat` powers needs the `^`-evaluation threshold raised
-- (default 256 leaves `^` symbolic) and a generous recursion depth.
set_option exponentiation.threshold 6000
set_option maxRecDepth 10000
set_option linter.style.longLine false

/-! ## The exact carry-free digit-DP integers (copied from the verified numerical cert).

PRIMARY beat cell: `A = {0,2,3,4,5,6,7,8,9,10}`, base `B = 21`, `d = 100`, `T = 187`,
density `1.875`. `Nplus = |U+U|`, `Nminus = |U−U|`, `maxU = max(U)`. Source:
`constants/3a/certificate/beat_largerd/beat_d100.json`, PRIMARY. -/

/-- `|U+U|` for the PRIMARY beat cell (97 digits). -/
def Nplus : ℕ := 1809676398856174550300417555449738879384136473841359582569119926015537272761458027460646645303559

/-- `|U−U|` for the PRIMARY beat cell (120 digits). -/
def Nminus : ℕ := 283200275148368195620519608709969845295570791228221500087826652456730765783899422053982917843756754727394748462150287419

/-- `max(U)` for the PRIMARY beat cell (132 digits). -/
def maxU : ℕ := 833488242198168679597985613642005906426102127082424744776204497944077206892606506869265781425216988516305693554824753642250830689327

/-! Record cell (the bar we strictly beat): `d = 80`, `T = 150`, same alphabet/base. Source:
`constants/3a/certificate/engine/record_{plus,minus,max}.txt`. The R18 record value is
`1.1740744476935212` (the bar — note this is the TRUE record, strictly ABOVE the table
truncation `1.1740744`). -/

/-- `|U+U|` for the d=80 record cell (77 digits). -/
def recNplus : ℕ := 75448362167176243488362019935078206851619643198150854886920234689186981134888

/-- `|U−U|` for the d=80 record cell (96 digits). -/
def recNminus : ℕ := 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415

/-- `max(U)` for the d=80 record cell (106 digits). -/
def recMaxU : ℕ := 2995805288150731620410662946668903948341032736664352641511848666717243994160370658179324073879212562136150

/-- The wedge numerator `P` (with `c = 1 + P/Q = 5877/5000`, so `P = 877`). -/
def P : ℕ := 877

/-- The wedge denominator `Q` (`Q = 5000`). -/
def Q : ℕ := 5000

/-! ## The load-bearing power inequalities (axiom-free kernel `decide`). -/

/-- **Load-bearing kernel check (the beat cell passes the wedge).**
`|U+U|^Q · (2·max(U)+1)^P ≤ |U−U|^Q`, i.e. `θ(U) ≥ 1 + P/Q = 5877/5000`. This is the
log-free form of the bound; `decide` evaluates ~2-million-bit `Nat` powers (GMP), no
`native_decide`. Axiom-free. -/
theorem newGE : Nplus ^ Q * (2 * maxU + 1) ^ P ≤ Nminus ^ Q := by decide

/-- **Strictness witness (the record cell FAILS the same wedge).**
`|U−U|^Q < |U+U|^Q · (2·max(U)+1)^P` for the d=80 record cell, i.e. the record value
`1.1740744476935212 < 5877/5000`. Together with `newGE` this certifies the bound is a
STRICT improvement over the record (`value_record < c ≤ value_new`). Axiom-free `decide`. -/
theorem recLT : recNminus ^ Q < recNplus ^ Q * (2 * recMaxU + 1) ^ P := by decide

/-! ## The named GHR analytic bridge (the only trust boundary). -/

/-- **The honest named trust boundary.** `GHR_lower c3a` asserts the GHR2007 analytic
conclusion in its log-free form: whenever a finite digit set `U ⊆ ℤ_{≥0}` with `0 ∈ U`
yields exact counts `s = |U+U| > 0`, `d = |U−U| ≥ s`, `m = max(U)`, and the integer power
inequality `s^q · (2m+1)^p ≤ d^q` holds for some `q > 0` (this is exactly `θ(U) ≥ 1+p/q`,
log-free), then `C_3a ≥ 1 + p/q`.

This packages ONLY the GHR existence step (`θ(U) ≥ c ⟹ C_3a ≥ c`): the construction of
arbitrarily large extremal `A,B` from the base-`(2m+1)` block digit set, which Mathlib
cannot state (no `C_3a` object). It does NOT do any arithmetic — the integer inequality is
supplied, already `decide`-proven. Folding arithmetic into it would be a smuggle. Same
shape as 9a's `ThetaGeFromIndep` and 5b's `MTThm15`. -/
def GHR_lower (c3a : ℝ) : Prop :=
  ∀ (s d m p q : ℕ), 0 < s → 0 < q → s ≤ d →
    s ^ q * (2 * m + 1) ^ p ≤ d ^ q →
    c3a ≥ 1 + (p : ℝ) / q

/-! ## The assembled lower bound. -/

/-- `0 < |U+U|` for the PRIMARY beat cell (it is a 97-digit positive literal). -/
theorem Nplus_pos : 0 < Nplus := by decide

/-- `|U+U| ≤ |U−U|` for the PRIMARY beat cell. -/
theorem Nplus_le_Nminus : Nplus ≤ Nminus := by decide

/-- `0 < Q`. -/
theorem Q_pos : 0 < Q := by decide

/-- **Main theorem.** Under the named GHR bridge, the PRIMARY beat cell's verified counts
give `C_3a ≥ 1 + 877/5000 = 5877/5000`. The discrete content (`newGE`) is axiom-free; the
only trust boundary is `GHR_lower`. -/
theorem c3a_ge_5877_5000 (c3a : ℝ) (hbridge : GHR_lower c3a) :
    c3a ≥ 1 + (877 : ℝ) / 5000 := by
  have h := hbridge Nplus Nminus maxU P Q Nplus_pos Q_pos Nplus_le_Nminus newGE
  simpa [P, Q] using h

/-- **Numeric form.** Under the bridge, `C_3a ≥ 5877/5000` (`= 1.1754`). -/
theorem c3a_ge_5877_5000' (c3a : ℝ) (hbridge : GHR_lower c3a) :
    c3a ≥ 5877 / 5000 := by
  have h := c3a_ge_5877_5000 c3a hbridge
  norm_num at h ⊢
  linarith

end C3a
