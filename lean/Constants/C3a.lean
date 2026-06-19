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

/-! ## R22 strict improvement: the `d = 130` beat cell, wedge `c = 2353/2000`.

PRIMARY R22 beat cell: `A = {0,2,3,4,5,6,7,8,9,10}`, base `B = 21`, `d = 130`, `T = 244`,
density `≈ 1.8769`. The carry-free digit-DP integers are copied verbatim from the
reviewer-re-derivable numerical certificate
(`constants/3a/certificate/sweep/climb_state.json`, cell `d130_T244`; also mirrored in
`constants/3a/certificate/beat_d130/beat_d130.json`). The cell's GHR value is
`value_new ≈ 1.1767830604497`, strictly above the wedge `c = 2353/2000 = 1.1765`.

The same monotone log-free chain as above gives:
`θ(U) ≥ 2353/2000  ⟺  |U−U|^Q ≥ |U+U|^Q · (2·max(U)+1)^P` with `c − 1 = 353/2000`,
so `P = 353`, `Q = 2000`. These exponents keep `decide` comfortably fast (~11.5 s total,
well under the R19 Q=5000 budget; the R21 attempt's Q=10000 was the kernel blowup).

Provenance/trust split: exactly as the R19 d=100 cell — the three big integers are TRUSTED
literals whose provenance is re-derived OUT of Lean by `verify_beat.py` / `digit_dp.py`
(the carry-free DP is an OOM hazard inside the kernel and is NOT recomputed here). All the
load-bearing arithmetic (the power inequalities) lives inside the formalization as
axiom-free `decide`. -/

/-- `|U+U|` for the R22 d=130 beat cell (126 digits). Source: `climb_state.json::d130_T244`. -/
def Nplus130 : ℕ := 483667226263608214580619446622793188413862899653492241091421848720825650329463032236822416528779054004297246251345644396500000

/-- `|U−U|` for the R22 d=130 beat cell (157 digits). Source: `climb_state.json::d130_T244`. -/
def Nminus130 : ℕ := 1179025549375377004051117585564873771635920143474533329894733356094404628784073452792728622460460724660990338165065516607315422503133169360888999628449913401

/-- `max(U)` for the R22 d=130 beat cell (172 digits). Source: `climb_state.json::d130_T244`. -/
def maxU130 : ℕ := 3867927452132688378438329512290875973553092936327081887292099987545400486065486724209575622746404207235296991785081947430956034473342270463738301696101336476626791946588644

/-- The R22 wedge numerator `P₂` (with `c = 1 + P₂/Q₂ = 2353/2000`, so `P₂ = 353`). -/
def P2 : ℕ := 353

/-- The R22 wedge denominator `Q₂` (`Q₂ = 2000`). -/
def Q2 : ℕ := 2000

/-- **Load-bearing kernel check (the d=130 beat cell passes the wedge).**
`|U+U|^Q₂ · (2·max(U)+1)^P₂ ≤ |U−U|^Q₂`, i.e. `θ(U) ≥ 1 + P₂/Q₂ = 2353/2000`. Log-free,
~1-million-bit `Nat` powers via GMP, no `native_decide`. Axiom-free (`[propext]`). -/
theorem newGE130 : Nplus130 ^ Q2 * (2 * maxU130 + 1) ^ P2 ≤ Nminus130 ^ Q2 := by decide

/-- **Strictness witness (the d=80 record cell FAILS the R22 wedge).**
`|U−U|^Q₂ < |U+U|^Q₂ · (2·max(U)+1)^P₂` for the d=80 record cell, i.e. the record value
`1.1740744476935212 < 2353/2000`. With `newGE130` this certifies a STRICT improvement over
the record (`value_record < 2353/2000 ≤ value_new`). Axiom-free `decide`. -/
theorem recLT130 : recNminus ^ Q2 < recNplus ^ Q2 * (2 * recMaxU + 1) ^ P2 := by decide

/-- `0 < |U+U|` for the R22 d=130 beat cell. -/
theorem Nplus130_pos : 0 < Nplus130 := by decide

/-- `|U+U| ≤ |U−U|` for the R22 d=130 beat cell. -/
theorem Nplus130_le_Nminus130 : Nplus130 ≤ Nminus130 := by decide

/-- `0 < Q₂`. -/
theorem Q2_pos : 0 < Q2 := by decide

/-- **R22 main theorem.** Under the named GHR bridge, the d=130 beat cell's verified counts
give `C_3a ≥ 1 + 353/2000 = 2353/2000`. Strictly beats the previously held & Lean-checked
`5877/5000 = 1.1754` (and the true record `1.1740744476935212`, via `recLT130`). The discrete
content (`newGE130`) is axiom-free; the only trust boundary is `GHR_lower`. -/
theorem c3a_ge_2353_2000 (c3a : ℝ) (hbridge : GHR_lower c3a) :
    c3a ≥ 1 + (353 : ℝ) / 2000 := by
  have h := hbridge Nplus130 Nminus130 maxU130 P2 Q2 Nplus130_pos Q2_pos
    Nplus130_le_Nminus130 newGE130
  simpa [P2, Q2] using h

/-- **R22 numeric form.** Under the bridge, `C_3a ≥ 2353/2000` (`= 1.1765`), strictly above
the held `5877/5000 = 1.1754`. -/
theorem c3a_ge_2353_2000' (c3a : ℝ) (hbridge : GHR_lower c3a) :
    c3a ≥ 2353 / 2000 := by
  have h := c3a_ge_2353_2000 c3a hbridge
  norm_num at h ⊢
  linarith

/-! ## R23 strict improvement: the `d = 140` beat cell, wedge `c = 1177/1000`.

PRIMARY R23 beat cell: `A = {0,2,3,4,5,6,7,8,9,10}`, base `B = 21`, `d = 140`, `T = 263`,
density `≈ 1.8786`. The carry-free digit-DP integers are copied verbatim from the
reviewer-re-derivable numerical certificate
(`constants/3a/certificate/beat_d140/beat_d140.json`, cell `d140_T263`). The cell's GHR
value is `value_new ≈ 1.1771186319558`, strictly above the wedge `c = 1177/1000 = 1.1770`.

The same monotone log-free chain as above gives:
`θ(U) ≥ 1177/1000  ⟺  |U−U|^Q ≥ |U+U|^Q · (2·max(U)+1)^P` with `c − 1 = 177/1000`,
so `P = 177`, `Q = 1000`. These exponents keep `decide` fast (`Q = 1000 < R22's Q = 2000`,
which decided in ~11.5 s; R21's Q=10000 was the kernel blowup).

Provenance/trust split: exactly as the R19/R22 cells — the three big integers are TRUSTED
literals whose provenance is re-derived OUT of Lean by `verify_beat.py` / `digit_dp.py`
(the carry-free DP is an OOM hazard inside the kernel and is NOT recomputed here). All the
load-bearing arithmetic (the power inequalities) lives inside the formalization as
axiom-free `decide`. -/

/-- `|U+U|` for the R23 d=140 beat cell (136 digits). Source: `beat_d140.json::d140_T263`. -/
def Nplus140 : ℕ := 3134964631416341157347896012445129330079198543361818679368635051359477236592630515798738179031612773450441996030492777384237480067723465

/-- `|U−U|` for the R23 d=140 beat cell (169 digits). Source: `beat_d140.json::d140_T263`. -/
def Nminus140 : ℕ := 1917727135747547616406943410757865790239803964286902231799394250495503136907988109943303932312311534932990938532498712842732855094364549316265313097912793764577082149931

/-- `max(U)` for the R23 d=140 beat cell (185 digits). Source: `beat_d140.json::d140_T263`. -/
def maxU140 : ℕ := 64516569533889487833393828142223439783902685347643508039836208175980509513559182519359802979879314759887696623968078168342677322038173530072092398992745205512807139631466507280163106443

/-- The R23 wedge numerator `P₃` (with `c = 1 + P₃/Q₃ = 1177/1000`, so `P₃ = 177`). -/
def P3 : ℕ := 177

/-- The R23 wedge denominator `Q₃` (`Q₃ = 1000`). -/
def Q3 : ℕ := 1000

/-- **Load-bearing kernel check (the d=140 beat cell passes the wedge).**
`|U+U|^Q₃ · (2·max(U)+1)^P₃ ≤ |U−U|^Q₃`, i.e. `θ(U) ≥ 1 + P₃/Q₃ = 1177/1000`. Log-free
`Nat` powers via GMP, no `native_decide`. Axiom-free (`[propext]`). -/
theorem newGE140 : Nplus140 ^ Q3 * (2 * maxU140 + 1) ^ P3 ≤ Nminus140 ^ Q3 := by decide

/-- **Strictness witness (the d=80 record cell FAILS the R23 wedge).**
`|U−U|^Q₃ < |U+U|^Q₃ · (2·max(U)+1)^P₃` for the d=80 record cell, i.e. the record value
`1.1740744476935212 < 1177/1000`. With `newGE140` this certifies a STRICT improvement over
the record (`value_record < 1177/1000 ≤ value_new`). Axiom-free `decide`. -/
theorem recLT140 : recNminus ^ Q3 < recNplus ^ Q3 * (2 * recMaxU + 1) ^ P3 := by decide

/-- `0 < |U+U|` for the R23 d=140 beat cell. -/
theorem Nplus140_pos : 0 < Nplus140 := by decide

/-- `|U+U| ≤ |U−U|` for the R23 d=140 beat cell. -/
theorem Nplus140_le_Nminus140 : Nplus140 ≤ Nminus140 := by decide

/-- `0 < Q₃`. -/
theorem Q3_pos : 0 < Q3 := by decide

/-- **R23 main theorem.** Under the named GHR bridge, the d=140 beat cell's verified counts
give `C_3a ≥ 1 + 177/1000 = 1177/1000`. Strictly beats the previously held & Lean-checked
`2353/2000 = 1.1765` (R22), `5877/5000 = 1.1754` (R18/R19), and the true record
`1.1740744476935212` (via `recLT140`). The discrete content (`newGE140`) is axiom-free; the
only trust boundary is `GHR_lower`. -/
theorem c3a_ge_1177_1000 (c3a : ℝ) (hbridge : GHR_lower c3a) :
    c3a ≥ 1 + (177 : ℝ) / 1000 := by
  have h := hbridge Nplus140 Nminus140 maxU140 P3 Q3 Nplus140_pos Q3_pos
    Nplus140_le_Nminus140 newGE140
  simpa [P3, Q3] using h

/-- **R23 numeric form.** Under the bridge, `C_3a ≥ 1177/1000` (`= 1.1770`), strictly above
the held `2353/2000 = 1.1765`. -/
theorem c3a_ge_1177_1000' (c3a : ℝ) (hbridge : GHR_lower c3a) :
    c3a ≥ 1177 / 1000 := by
  have h := c3a_ge_1177_1000 c3a hbridge
  norm_num at h ⊢
  linarith

/-! ## ROUND 24 — the d=150 beat cell (`C_3a ≥ 239/203 = 1.1773399…`).

Same proven carry-free drop-1 base-21 GHR digit lever as R18/R19/R22/R23, pushed one rung
further: `A = {0,2,3,4,5,6,7,8,9,10}`, `B = 21`, `d = 150`, `T = 282` (density `1.8800`;
carry-free since `B = 21 > 2·max(A) = 20`). Reviewer-re-derivable numerical certificate at
`constants/3a/certificate/beat_d150/beat_d150.json` (cell `d150_T282`,
`verify_beat.py --recompute`). The cell's GHR value is `value_new ≈ 1.1774136588225`,
strictly above the wedge `c = 239/203 = 1.1773399…`.

The same monotone log-free chain gives `θ(U) ≥ 239/203 ⟺
|U−U|^Q ≥ |U+U|^Q · (2·max(U)+1)^P` with `c − 1 = 36/203`, so `P = 36`, `Q = 203`. The
exponents keep `decide` fast (`Q = 203 ≪ R22's Q = 2000` which decided in ~11.5 s; R21's
Q=10000 was the kernel blowup — far below it).

Provenance/trust split: exactly as R19/R22/R23 — the three big integers are TRUSTED literals
whose provenance is re-derived OUT of Lean by `verify_beat.py` / `digit_dp.py` (the carry-free
DP is an OOM hazard inside the kernel and is NOT recomputed here). All the load-bearing
arithmetic (the power inequalities) lives inside the formalization as axiom-free `decide`. -/

-- The d=150 decide lemmas use exponent Q₄ = 203; the file-wide
-- `set_option exponentiation.threshold 6000` (set near the top) covers it.

/-- `|U+U|` for the R24 d=150 beat cell (146 digits). Source: `beat_d150.json::d150_T282`. -/
def Nplus150 : ℕ := 20368752287338608568410165192730428108438003847872159490727906616963038878748891077110031128908255285303824809431154129437865067062663903709920716

/-- `|U−U|` for the R24 d=150 beat cell (181 digits). Source: `beat_d150.json::d150_T282`. -/
def Nminus150 : ℕ := 3132772467004354042340402489674953793055251008972361502165693655041621037047022188474825311910251490919596584550287513072684960825866511067843014580729185435519747493315946311006851

/-- `max(U)` for the R24 d=150 beat cell (199 digits). Source: `beat_d150.json::d150_T282`. -/
def maxU150 : ℕ := 1076128700947105424942699934266586023464296341535009189412143770590930217897788662281829169147671181252698751322378624550846459909603822557256657869961255681970440375687415452172777430715188659691922

/-- The R24 wedge numerator `P₄` (with `c = 1 + P₄/Q₄ = 239/203`, so `P₄ = 36`). -/
def P4 : ℕ := 36

/-- The R24 wedge denominator `Q₄` (`Q₄ = 203`). -/
def Q4 : ℕ := 203

/-- **Load-bearing kernel check (the d=150 beat cell passes the wedge).**
`|U+U|^Q₄ · (2·max(U)+1)^P₄ ≤ |U−U|^Q₄`, i.e. `θ(U) ≥ 1 + P₄/Q₄ = 239/203`. Log-free
`Nat` powers via GMP, no `native_decide`. Axiom-free (`[propext]`). -/
theorem newGE150 : Nplus150 ^ Q4 * (2 * maxU150 + 1) ^ P4 ≤ Nminus150 ^ Q4 := by decide

/-- **Strictness witness (the d=80 record cell FAILS the R24 wedge).**
`|U−U|^Q₄ < |U+U|^Q₄ · (2·max(U)+1)^P₄` for the d=80 record cell, i.e. the record value
`1.1740744476935212 < 239/203`. With `newGE150` this certifies a STRICT improvement over the
record (`value_record < 239/203 ≤ value_new`). Axiom-free `decide`. -/
theorem recLT150 : recNminus ^ Q4 < recNplus ^ Q4 * (2 * recMaxU + 1) ^ P4 := by decide

/-- `0 < |U+U|` for the R24 d=150 beat cell. -/
theorem Nplus150_pos : 0 < Nplus150 := by decide

/-- `|U+U| ≤ |U−U|` for the R24 d=150 beat cell. -/
theorem Nplus150_le_Nminus150 : Nplus150 ≤ Nminus150 := by decide

/-- `0 < Q₄`. -/
theorem Q4_pos : 0 < Q4 := by decide

/-- **R24 main theorem.** Under the named GHR bridge, the d=150 beat cell's verified counts
give `C_3a ≥ 1 + 36/203 = 239/203`. Strictly beats the previously held & Lean-checked
`1177/1000 = 1.1770` (R23), `2353/2000 = 1.1765` (R22), `5877/5000 = 1.1754` (R18/R19), and
the true record `1.1740744476935212` (via `recLT150`). The discrete content (`newGE150`) is
axiom-free; the only trust boundary is `GHR_lower`. -/
theorem c3a_ge_239_203 (c3a : ℝ) (hbridge : GHR_lower c3a) :
    c3a ≥ 1 + (36 : ℝ) / 203 := by
  have h := hbridge Nplus150 Nminus150 maxU150 P4 Q4 Nplus150_pos Q4_pos
    Nplus150_le_Nminus150 newGE150
  simpa [P4, Q4] using h

/-- **R24 numeric form.** Under the bridge, `C_3a ≥ 239/203` (`≈ 1.1773399`), strictly above
the held `1177/1000 = 1.1770`. -/
theorem c3a_ge_239_203' (c3a : ℝ) (hbridge : GHR_lower c3a) :
    c3a ≥ 239 / 203 := by
  have h := c3a_ge_239_203 c3a hbridge
  norm_num at h ⊢
  linarith

end C3a
