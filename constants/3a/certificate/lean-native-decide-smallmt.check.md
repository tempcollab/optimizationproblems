# Lean certificate record — `lean-native-decide-smallmt`

- **Lake project:** `constants/3a/lean/` (Lean v4.31.0, no Mathlib — core only).
- **Build target:** `lake build C3a` (default target `C3a`, which imports `Sketches.NativeDecideSmallMT`).
  Build is EXIT 0, ~0.5s (R4).
- **Load-bearing theorem (HOLE-FREE, machine-checked):**
  `C3a.griego_100_190_int_cert : D ^ 40 > S ^ 40 * Q ^ 7`, discharged by `native_decide`.
  Operands ~4800 digits. This is the cleared-denominator form of θ > 47/40 = 1.175.
- **Faithful top theorem (HOLE-FREE given an explicit, visible hypothesis):**
  `C3a.c3a_lower_bound (bridge : D^40 > S^40*Q^7 → 1175 ≤ Cnum) : 1175 ≤ Cnum`
  — proved `:= bridge griego_100_190_int_cert` (modus ponens, no `sorry`, no added axiom).
  `Cnum := ⌊1000·C_3a⌋`, so `1175 ≤ Cnum` is "C_3a ≥ 1.175 > 1.1740744". The one cited step
  ([GHR2007] read-off C_3a ≥ θ + real-log algebra θ > 47/40) is the named HYPOTHESIS `bridge`,
  NOT a `sorry` and NOT an `axiom`.
- **`#print axioms` lines (recorded R4):**
  - `#print axioms C3a.griego_100_190_int_cert`
    → `[griego_100_190_int_cert._native.native_decide.ax_1_1]` (the native_decide trust axiom; NO sorryAx).
  - `#print axioms C3a.c3a_lower_bound`
    → `[griego_100_190_int_cert._native.native_decide.ax_1_1]` (same single native_decide axiom; NO sorryAx).
    (In Lean 4.31 native_decide emits `_native.native_decide.ax_…` rather than `Lean.ofReduceBool`;
    either way it is the standard native-decision trust kernel, not a sorry.)
- **Holes remaining (`sorry`):** NONE. The file is `sorry`-free. The only non-machine-checked
  content is the explicit hypothesis `bridge` (the cited [GHR2007] read-off + log algebra),
  which is a visible parameter of `c3a_lower_bound`, not a hidden gap. The full Lean-internal
  proof of `bridge` (formalizing GHR2007 + a `Real.log` monotonicity bridge, which needs Mathlib)
  is the documented remaining work; it does not touch the load-bearing integer comparison.
- **Numbers (independently re-derived from scratch, R4):** (m,T)=(100,190), A={0,2,…,10}, b=21.
  S=|U+U| (97 digits, head 86388581 / tail 26122695), D=|U-U| (121 digits, head 13829645 / tail
  69875299), Q=2·max(U)+1 (133 digits, head 16669764 / tail 42124381). θ = 1.175495508 > 1.1740744.
  The Lean literals were string-matched against the from-scratch recomputation (S/D/Q all exact
  match). The recomputation reused the certified `exact-sumdiff-dp` DP after passing the small-case
  brute-force oracle sanity check (8 self-test cases incl. clamp-exercising (4,40),(5,20)).
