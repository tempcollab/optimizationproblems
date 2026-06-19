# Lean certificate record — `lean-native-decide-smallmt`

- **Lake project:** `constants/3a/lean/` (Lean v4.31.0). **As of R5 the project DEPENDS ON
  Mathlib** (pinned to the `v4.31.0` tag, rev `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, recorded
  in `lake-manifest.json`). Mathlib is used only for the real-arithmetic log bridge; the
  load-bearing integer step is still pure Lean-core `Nat` via `native_decide`.
- **Build target:** `lake build C3a` (default target `C3a`, which imports
  `Sketches.NativeDecideSmallMT`). Build is EXIT 0 (~10s incremental; Mathlib oleans come from the
  Azure cache via `lake exe cache get`/`lake update`, ~2968 jobs). **Re-confirmed R6:**
  `Build completed successfully (2968 jobs).` EXIT 0.
- **Load-bearing theorem (HOLE-FREE, machine-checked):**
  `C3a.griego_100_190_int_cert : D ^ 40 > S ^ 40 * Q ^ 7`, discharged by `native_decide`.
  Operands ~4800 digits. This is the cleared-denominator form of θ > 47/40 = 1.175.
- **Log-algebra HALF of the bridge (FORMALIZED R5, GENERALISED R6, HOLE-FREE):**
  `C3a.log_bridge (s d q A B : ℕ) (hs : 0 < s) (hq : 1 < q) (hB : 0 < B) (hint : s^B * q^A < d^B) :`
  `1 + (A:ℝ)/(B:ℝ) < 1 + Real.log ((d:ℝ)/(s:ℝ)) / Real.log (q:ℝ)`.
  Proved with Mathlib (`Real.log_lt_log`, `Real.log_pow`, `lt_div_iff₀`, `div_lt_div_iff₀`,
  `div_pow`, `positivity`, `nlinarith`). This is step (A) of the GHR bridge — `(int ineq) ⟹
  θ > 1 + A/B` — now a Lean theorem, no longer an assumption, and **fully general in the exponents**
  (R6): the integer cert `d^B > s^B·q^A` is exactly the cleared-denominator form of `θ > 1 + A/B`
  for any `A,B` with `0 < B`. The 7/40 numerals live only in the `theta_gt` specialisation, which
  instantiates `(A,B)=(7,40)`: `C3a.theta_gt : (47:ℝ)/40 < theta` (since `1 + 7/40 = 47/40`).
  PROMOTABLE to `constants/3a/lemmas/` (axiom-clean, general, no sketch-specific numerals).
- **Faithful top theorem (HOLE-FREE given ONE explicit, visible hypothesis):**
  `C3a.c3a_lower_bound (ghr : theta ≤ C3aReal) : (47:ℝ)/40 < C3aReal`
  — proved `:= lt_of_lt_of_le theta_gt ghr` (no `sorry`, no added custom axiom).
  `theta := 1 + log(D/S)/log Q`, `C3aReal` is the opaque real C_3a. So `(47:ℝ)/40 < C3aReal` is
  "C_3a > 1.175 > 1.1740744". The ONE remaining cited step is the named hypothesis `ghr`: the
  [GHR2007] tensor-power LIMIT read-off `θ ≤ C_3a` — NOT a `sorry`, NOT an `axiom`.
- **`#print axioms` lines (re-confirmed R6 — verbatim tool output):**
  - `#print axioms C3a.griego_100_190_int_cert`
    → `[propext, griego_100_190_int_cert._native.native_decide.ax_1_1]` (native_decide trust axiom; NO sorryAx).
  - `#print axioms C3a.log_bridge`
    → `[propext, Classical.choice, Quot.sound]` (Mathlib's standard axioms only; NO sorryAx, NO
      native_decide axiom — the generalised log bridge is pure real arithmetic).
  - `#print axioms C3a.theta_gt`
    → `[propext, Classical.choice, Quot.sound, Q_gt_one._native.native_decide.ax_1_1,`
      `S_pos._native.native_decide.ax_1_1, griego_100_190_int_cert._native.native_decide.ax_1_1]`
      (standard + native_decide; NO sorryAx).
  - `#print axioms C3a.c3a_lower_bound`
    → same set as `theta_gt` (standard Mathlib axioms + the three native_decide trust axioms; NO
      sorryAx, NO smuggled custom axiom). The only assumption is the explicit `ghr` parameter.
- **Holes remaining (`sorry`):** NONE. The file is `sorry`-free. The only non-machine-checked
  content is the explicit hypothesis `ghr : theta ≤ C3aReal` (the cited [GHR2007] tensor-power limit
  read-off `C_3a ≥ θ`), a visible parameter of `c3a_lower_bound`, not a hidden gap. Discharging it
  requires (i) a Lean DEFINITION of C_3a (the sup-over-constructions exponent) and (ii) formalizing
  the GHR2007 digit-tensor-power LIMIT lemma — multi-round real-analysis. It does NOT touch the
  load-bearing integer comparison nor the now-formalized log-algebra step.
- **R5 vs R4 narrowing:** in R4 the WHOLE bridge `(D^40>S^40·Q^7) → 1175 ≤ Cnum` was one assumed
  hypothesis bundling the log algebra + the GHR read-off. R5 PROVES the log-algebra half
  (`log_bridge`/`theta_gt`) in Lean, so the remaining assumption is exactly the GHR2007 limit
  read-off `θ ≤ C_3a` — a strictly smaller, sharply-named hole.
- **Numbers (independently re-derived from scratch, R4; unchanged R5):** (m,T)=(100,190),
  A={0,2,…,10}, b=21. S=|U+U| (97 digits, head 86388581 / tail 26122695), D=|U-U| (121 digits,
  head 13829645 / tail 69875299), Q=2·max(U)+1 (133 digits, head 16669764 / tail 42124381).
  θ = 1.175495508 > 1.1740744. The Lean literals were string-matched against the from-scratch
  recomputation (S/D/Q all exact match).
- **Honest scope:** this Lean cert proves C_3a > 1.175 (below our held 1.176 Python cert), and it is
  NOT self-contained — the GHR limit read-off `ghr` is still an explicit hypothesis. Do NOT claim
  θ>1.175 is self-contained in Lean while `ghr` is assumed.
