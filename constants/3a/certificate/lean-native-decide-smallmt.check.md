# Lean certificate record — `lean-native-decide-smallmt`

- **Lake project:** `constants/3a/lean/` (Lean v4.31.0). **As of R5 the project DEPENDS ON
  Mathlib** (pinned to the `v4.31.0` tag, rev `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, recorded
  in `lake-manifest.json`). Mathlib is used only for the real-arithmetic log bridge; the
  load-bearing integer step is still pure Lean-core `Nat` via `native_decide`.
- **Build target:** `lake build C3a` (default target `C3a`, which imports
  `Sketches.NativeDecideSmallMT`). Build is EXIT 0 (~6s incremental; Mathlib oleans come from the
  Azure cache via `lake exe cache get`/`lake update`, ~2968 jobs).
- **Load-bearing theorem (HOLE-FREE, machine-checked):**
  `C3a.griego_100_190_int_cert : D ^ 40 > S ^ 40 * Q ^ 7`, discharged by `native_decide`.
  Operands ~4800 digits. This is the cleared-denominator form of θ > 47/40 = 1.175.
- **Log-algebra HALF of the bridge (FORMALIZED R5, HOLE-FREE):**
  `C3a.log_bridge (s d q : ℕ) (hs : 0 < s) (hq : 1 < q) (hint : s^40 * q^7 < d^40) :`
  `(47:ℝ)/40 < 1 + Real.log ((d:ℝ)/(s:ℝ)) / Real.log (q:ℝ)`.
  Proved with Mathlib (`Real.log_lt_log`, `Real.log_pow`, `lt_div_iff₀`, `div_pow`, `positivity`,
  `nlinarith`). This is step (A) of the GHR bridge — `(int ineq) ⟹ θ > 1.175` — now a Lean theorem,
  no longer an assumption. Specialised to the certified literals as `C3a.theta_gt : (47:ℝ)/40 < theta`.
- **Faithful top theorem (HOLE-FREE given ONE explicit, visible hypothesis):**
  `C3a.c3a_lower_bound (ghr : theta ≤ C3aReal) : (47:ℝ)/40 < C3aReal`
  — proved `:= lt_of_lt_of_le theta_gt ghr` (no `sorry`, no added custom axiom).
  `theta := 1 + log(D/S)/log Q`, `C3aReal` is the opaque real C_3a. So `(47:ℝ)/40 < C3aReal` is
  "C_3a > 1.175 > 1.1740744". The ONE remaining cited step is the named hypothesis `ghr`: the
  [GHR2007] tensor-power LIMIT read-off `θ ≤ C_3a` — NOT a `sorry`, NOT an `axiom`.
- **`#print axioms` lines (recorded R5):**
  - `#print axioms C3a.griego_100_190_int_cert`
    → `[propext, griego_100_190_int_cert._native.native_decide.ax_1_1]` (native_decide trust axiom; NO sorryAx).
  - `#print axioms C3a.log_bridge`
    → `[propext, Classical.choice, Quot.sound]` (Mathlib's standard axioms only; NO sorryAx).
  - `#print axioms C3a.theta_gt`
    → `[propext, Classical.choice, Quot.sound, Q_gt_one._native…, S_pos._native…,`
      `griego_100_190_int_cert._native…]` (standard + native_decide; NO sorryAx).
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
