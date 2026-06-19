# Lean certificate record — `lean-native-decide-smallmt`

- **Lake project:** `constants/3a/lean/` (Lean v4.31.0). The project DEPENDS ON Mathlib (pinned
  to the `v4.31.0` tag, rev `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, recorded in
  `lake-manifest.json`). Mathlib is used only for the real-arithmetic log bridge; the
  load-bearing integer step is pure Lean-core `Nat` via `native_decide`.
- **Build target:** `lake build C3a` (default target `C3a`, which imports
  `Sketches.NativeDecideSmallMT`). Build is EXIT 0 (~18s incremental; Mathlib oleans from the
  Azure cache via `lake exe cache get`/`lake update`, 2968 jobs). **Re-confirmed R8:**
  `Build completed successfully (2968 jobs).` EXIT 0.

## R8 update — integer core bumped to the FULL held value θ > 1.1771 at (140,265)

- **Point changed (100,190)→(140,265).** R8 actually TESTED native_decide on the den=10000
  operands (~1.69M digits) instead of assuming they were too big (the R4/R5 assumption was
  untested and WRONG): the kernel discharges the comparison in ~6.7s. So the integer core now
  certifies the SAME tight rational as the verified Python held bound, 11771/10000 = 1.1771, at
  (m,T)=(140,265), A={0,2,…,10}, base 21 — up from the old coarse 47/40 = 1.175 at (100,190).
  Measured native_decide build times at this point (all EXIT 0, axioms clean):
  den=250 (θ>1.176, ~42k digits) ~16s; den=500 (θ>1.176, ~84k digits) ~9s;
  den=1000 (θ>1.177, ~169k digits) ~6s; **den=10000 (θ>1.1771, ~1.69M digits) ~6.7s ← chosen.**

- **Load-bearing theorem (HOLE-FREE, machine-checked):**
  `C3a.griego_140_265_int_cert : D ^ 10000 > S ^ 10000 * Q ^ 1771`, discharged by `native_decide`.
  Operands ~1.69M digits. Cleared-denominator form of θ > 11771/10000 = 1.1771.
- **Tightness / negative control (HOLE-FREE, machine-checked):**
  `C3a.griego_140_265_int_cert_tight : ¬ (D ^ 10000 > S ^ 10000 * Q ^ 1772)`, by `native_decide`.
  The ^1772 inequality FAILS, so 11771/10000 is the EXACT integer-certifiable θ at this point
  (matches the Python certificate's k+1 negative control: k=11771 PASS / k=11772 FAIL).
- **Log-algebra HALF of the bridge (FORMALIZED, GENERALISED, HOLE-FREE):**
  `C3a.log_bridge (s d q A B : ℕ) (hs : 0 < s) (hq : 1 < q) (hB : 0 < B) (hint : s^B * q^A < d^B) :`
  `1 + (A:ℝ)/(B:ℝ) < 1 + Real.log ((d:ℝ)/(s:ℝ)) / Real.log (q:ℝ)`.
  Proved with Mathlib (`Real.log_lt_log`, `Real.log_pow`, `lt_div_iff₀`, `div_lt_div_iff₀`,
  `div_pow`, `positivity`, `nlinarith`). Step (A) of the GHR bridge — `(int ineq) ⟹ θ > 1 + A/B`
  — a Lean theorem, fully general in the exponents. The 1771/10000 numerals live only in the
  `theta_gt` specialisation, which instantiates `(A,B)=(1771,10000)`:
  `C3a.theta_gt : (11771:ℝ)/10000 < theta` (since `1 + 1771/10000 = 11771/10000`).
  Already PROMOTED to `constants/3a/lemmas/log-bridge.md` (R7), axiom-clean, general.
- **Faithful top theorem (HOLE-FREE given ONE explicit, visible hypothesis):**
  `C3a.c3a_lower_bound (ghr : theta ≤ C3aReal) : (11771:ℝ)/10000 < C3aReal`
  — proved `:= lt_of_lt_of_le theta_gt ghr` (no `sorry`, no added custom axiom).
  `theta := 1 + log(D/S)/log Q`, `C3aReal` is the opaque real C_3a. So `(11771:ℝ)/10000 < C3aReal`
  is "C_3a > 1.1771 > 1.1740744". The ONE remaining cited step is the named hypothesis `ghr`: the
  [GHR2007] tensor-power LIMIT read-off `θ ≤ C_3a` — NOT a `sorry`, NOT an `axiom`.
- **`#print axioms` lines (re-confirmed R8 — verbatim tool output):**
  - `#print axioms C3a.griego_140_265_int_cert`
    → `[propext, C3a.griego_140_265_int_cert._native.native_decide.ax_1_1]` (native_decide trust
      axiom; NO sorryAx).
  - `#print axioms C3a.griego_140_265_int_cert_tight`
    → `[propext, C3a.griego_140_265_int_cert_tight._native.native_decide.ax_1_1]` (NO sorryAx).
  - `#print axioms C3a.log_bridge`
    → `[propext, Classical.choice, Quot.sound]` (Mathlib's standard axioms only; NO sorryAx, NO
      native_decide axiom).
  - `#print axioms C3a.theta_gt`
    → `[propext, Classical.choice, Quot.sound, Q_gt_one._native…, S_pos._native…,`
      `griego_140_265_int_cert._native…]` (standard + native_decide; NO sorryAx).
  - `#print axioms C3a.c3a_lower_bound`
    → same set as `theta_gt` (standard Mathlib axioms + the native_decide trust axioms; NO
      sorryAx, NO smuggled custom axiom). The only assumption is the explicit `ghr` parameter.
- **Holes remaining (`sorry`):** NONE. The file is `sorry`-free. The only non-machine-checked
  content is the explicit hypothesis `ghr : theta ≤ C3aReal` (the cited [GHR2007] tensor-power
  limit read-off `C_3a ≥ θ`), a visible parameter of `c3a_lower_bound`, not a hidden gap.
  Discharging it requires (i) a Lean DEFINITION of C_3a (the sup-over-constructions exponent) and
  (ii) formalizing the GHR2007 digit-tensor-power LIMIT lemma — multi-round real-analysis. It does
  NOT touch the load-bearing integer comparison nor the formalized log-algebra step.
- **Numbers (committed at (140,265) in scan-mT-results.txt; independently re-derived from scratch
  in R7's griego-ntt-push verification — 3-way oracle gate, byte-for-byte count match):**
  (m,T)=(140,265), A={0,2,…,10}, b=21.
  S=|U+U| (136 digits, head 88785247 / tail 58197858),
  D=|U−U| (169 digits, head 54747299 / tail 84610391),
  M=max(U) (185 digits, head 64516569 / tail 03949365),
  Q=2·max(U)+1 (186 digits, head 12903313 / tail 07898731).
  θ ≈ 1.1771373652 > 1.1740744. The Lean S/D/Q literals were string-matched against the committed
  scan row; tight: D^10000 > S^10000·Q^1771 holds, ^1772 fails.
- **Honest scope:** this Lean cert now machine-checks the integer core for C_3a > 1.1771 — the
  SAME value as the verified held — but it is STILL NOT self-contained: the GHR limit read-off
  `ghr` remains an explicit hypothesis. Do NOT claim θ>1.1771 is a complete self-contained Lean
  proof while `ghr` is assumed; it raises the machine-checked CERTIFICATION LEVEL of the integer
  core to the held value, not the verified `held` itself (the held is the Python certificate;
  this is its gold-standard-track Lean companion, integer core now at parity).
