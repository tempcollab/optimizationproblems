# Sketch `lean-native-decide-smallmt` — machine-checked (Lean) C_3a lower bound

## Strategy
Port the verified C_3a lower bound to a `lake build`-passing Lean theorem — the gold-standard
certificate (CLAUDE.md prefers Lean-fit; the held 1.176 bound is currently only a Python big-int
cert). The load-bearing step is a SINGLE pure big-integer inequality, exactly `native_decide`-shaped.

**R8 — the operand-size assumption was WRONG; tested it, native_decide handles ~1.69M-digit
operands.** Earlier rounds ASSUMED the den=10000 operands (~1.3-1.7M digits) were "too big for
the kernel" and deliberately fell back to a smaller-θ, small-denominator point (47/40 = 1.175 at
(100,190), ~4800-digit operands). R8 actually ran the build: Lean 4.31's `native_decide` discharges
the den=10000 comparison at (140,265) (~1.69M-digit operands) in **~6.7s**. The GMP-backed compiled
`Nat` arithmetic is far more capable than the digit-count guess. Measured R8 build times (all EXIT 0,
axioms clean): den=250 (θ>1.176) ~16s, den=500 (θ>1.176) ~9s, den=1000 (θ>1.177) ~6s,
**den=10000 (θ>1.1771) ~6.7s ← chosen**.

So the integer core now certifies the FULL held value, not a coarse stand-in:
- point (m,T)=(140,265), A={0,2,…,10}, b=21 (Griego family — the verified held-source point);
- rational 11771/10000 = 1.1771, exactly the verified Python held bound (R7);
- cleared-denominator form `D^10000 > S^10000·Q^1771`, operands ~1.69M digits — `native_decide`
  ~6.7s; TIGHT, with negative control `¬(D^10000 > S^10000·Q^1772)` also `native_decide` (^1772
  fails), matching the Python cert's k=11771 PASS / k=11772 FAIL.

This is the Lean-fit companion of the held bound: the integer core is now at PARITY with the
verified `held` (1.1771), a strict record beat over 1.1740744 (Griego 2026). The `held` itself
stays the Python certificate while the bridge hole `ghr` is open — see Holes below.

## Why the integers are trustworthy
S=|U+U|, D=|U-U|, Q=2·max(U)+1 at (100,190) are the output of the certified `exact-sumdiff-dp`
lemma (constants/3a/lemmas/exact-sumdiff-dp.md), cross-checked vs brute force on 12 cases in R3.
They are embedded as explicit literals in the Lean file; the DP need NOT be formalized — only the
final integers + the inequality are in Lean.

## Holes (R8 update)
The R4 `bridge` hypothesis bundled TWO independent steps: (A) the log algebra
`(int cert) ⟹ θ>k/den`, and (B) the GHR2007 read-off `C_3a ≥ θ`. R5 split them and FORMALIZED
(A) in Lean; only (B) remains assumed. **R8 bumped the integer cert (A's input) from the coarse
47/40=1.175 at (100,190) to the tight 11771/10000=1.1771 at (140,265)** — the integer core now
machine-checks the full held value.

1. **`griego_140_265_int_cert : D^10000 > S^10000·Q^1771` — CLOSED (hole-free), R8.**
   `native_decide`. The load-bearing integer step at (140,265); operands ~1.69M digits, ~6.7s.
   `#print axioms` → `[propext, griego_140_265_int_cert._native.native_decide.ax_1_1]` (native_decide
   trust axiom; NO sorryAx). Plus `griego_140_265_int_cert_tight : ¬(D^10000 > S^10000·Q^1772)`
   (also `native_decide`, NO sorryAx) — the tightness/negative control proving 1.1771 is the exact
   integer-certifiable θ at this point.
2. **LOG-ALGEBRA HALF (A) — CLOSED in R5, GENERALISED in R6, hole-free.** Lemma (R6 general form)
   `log_bridge (s d q A B : ℕ) (hs : 0<s) (hq : 1<q) (hB : 0<B) (hint : s^B*q^A < d^B) :`
   `1 + (A:ℝ)/(B:ℝ) < 1 + Real.log((d:ℝ)/s)/Real.log q`. Pure real arithmetic via Mathlib
   (`Real.log_lt_log`, `Real.log_pow`, `lt_div_iff₀`, `div_lt_div_iff₀`, `div_pow`, `positivity`,
   `nlinarith`). `#print axioms log_bridge` → `[propext, Classical.choice, Quot.sound]` (Mathlib
   standard axioms only; NO sorryAx, NO native_decide). **R6 change:** the exponents 40/7 are no
   longer baked into the lemma — it is now general in `(A,B)`, so the integer cert `d^B > s^B·q^A`
   certifies `θ > 1 + A/B` for ANY rational target. **R8:** the specialisation is now
   `theta_gt : (11771:ℝ)/10000 < theta` (instantiates `(A,B)=(1771,10000)`, uses
   `1 + 1771/10000 = 11771/10000`), where `theta := 1 + log(D/S)/log Q`. **The project requires Mathlib**, pinned
   to the v4.31.0 tag (rev `fabf563a…`) in `lake-manifest.json` — `lake build C3a` EXIT 0 (~2968
   jobs, oleans from the Azure cache). Re-confirmed R6: EXIT 0, axioms clean.
3. **Top theorem `c3a_lower_bound` — CLOSED (hole-free given the ONE remaining cited step).**
   `c3a_lower_bound (ghr : theta ≤ C3aReal) : (11771:ℝ)/10000 < C3aReal := lt_of_lt_of_le theta_gt ghr`.
   `C3aReal` is the opaque real C_3a; `(11771:ℝ)/10000 < C3aReal` is "C_3a > 1.1771 > 1.1740744".
   `#print axioms c3a_lower_bound` → `[propext, Classical.choice, Quot.sound]` + the three
   native_decide axioms; NO sorryAx, NO smuggled custom axiom.
4. **REMAINING HOLE — GHR2007 read-off (B), a single EXPLICIT NAMED HYPOTHESIS.**
   `ghr : theta ≤ C3aReal` = the [GHR2007] tensor-power LIMIT lemma `C_3a ≥ θ` (legit because 0∈A
   and base Q > 2·max(U) ⇒ the digit map is injective and carry-free, so the k→∞ digit-product of U
   has sumset/diffset S^k/D^k and max ≈ Q^k, preserving log(D/S)/log Q). Discharging it needs
   (i) a Lean DEFINITION of C_3a (the sup-over-constructions exponent) and (ii) formalizing the
   tensor-power limit argument — multi-round real-analysis Mathlib does not hand over. It is a
   visible parameter, NOT a `sorry`/`axiom`. NOT attempted this round (per the R5 scope).

## Verification level (be precise)
- **Machine-checked, hole-free (no sorryAx):** (i) the integer inequality `D^10000 > S^10000·Q^1771`
  at (140,265) via `native_decide` (operands ~1.69M digits, ~6.7s) PLUS its tightness negative
  control `¬(D^10000 > S^10000·Q^1772)` (also `native_decide`); (ii) the log-algebra step
  `(int cert) ⟹ θ>11771/10000` via `log_bridge`/`theta_gt`, proved over ℝ with Mathlib; and
  (iii) the `c3a_lower_bound` derivation `(11771:ℝ)/10000 < C3aReal` from `theta_gt` and `ghr`.
- **Assumed (single visible hypothesis, cited [GHR2007]):** `ghr : theta ≤ C3aReal` — the
  tensor-power limit read-off `C_3a ≥ θ`. NOT yet formalized.
- So the Lean file now establishes, hole-free, BOTH the integer fact AND the log algebra that turn
  it into "θ > 1.1771", reducing "C_3a > 1.1771" to the single named GHR2007 limit read-off. The
  integer core is now at PARITY with the verified `held` (1.1771). Still NOT self-contained: do not
  claim θ>1.1771 is a complete Lean proof while `ghr` is assumed — `ghr` keeps this a
  minimally-verified (*) Lean cert, not a `held`-raiser.

## Literals (committed scan-mT-results.txt @ (140,265); re-derived from scratch R7)
The (S,D,M) at (140,265) are the committed scan row, independently re-derived from scratch in R7's
griego-ntt-push verification (3-way oracle gate brute==indep==oracle on ≥15 cases incl. clamp +
non-contiguous + contiguous control, then byte-for-byte match of the committed counts). The Lean
literals were string-matched against that committed row:
- S=|U+U| — 136 digits, head 88785247 / tail 58197858 — MATCH.
- D=|U−U| — 169 digits, head 54747299 / tail 84610391 — MATCH.
- M=max(U) — 185 digits, head 64516569 / tail 03949365; Q=2M+1 — 186 digits, head 12903313 / tail 07898731 — MATCH.
θ ≈ 1.1771373652 > 1.1740744 (record). Tight: D^10000 > S^10000·Q^1771 holds, ^1772 fails.

### Prior (R4) point retired
Before R8 the integer core sat at the coarse (100,190)/47-40/1.175 point because the den=10000
operands were ASSUMED too big for native_decide. R8 tested and disproved that assumption (den=10000
~6.7s), so the core was moved to the tight (140,265) point. The old (100,190) literals (S 97d, D
121d, Q 133d) are no longer in the file.

## State
- R4: Lake project bootstrapped at `constants/3a/lean/` (Lean v4.31.0, core only). Integer core
  hole-free; whole bridge bundled as one assumed hypothesis.
- **R5: added a pinned Mathlib dependency** (v4.31.0 tag, rev `fabf563a…`, in
  `lake-manifest.json`) and FORMALIZED the log-algebra half of the bridge (`log_bridge`,
  `theta_gt`). `lake build C3a` EXIT 0 (~2968 jobs; Mathlib oleans from the Azure cache). The
  remaining assumed step is narrowed to exactly the GHR2007 limit read-off `ghr : theta ≤ C3aReal`.
  This is the ONLY Lean sketch, so the Mathlib dep affects no sibling.
- **R6: re-confirmed R5 build is sound (EXIT 0, `#print axioms` shows NO sorryAx) and GENERALISED
  `log_bridge` over the exponents** (`s^B·q^A < d^B ⟹ θ > 1+A/B`, params `(s,d,q,A,B)`), making it
  a clean promotable cache lemma with no sketch-specific numerals. `theta_gt` re-derived as the
  `(A,B)=(7,40)` specialisation. `lake build C3a` EXIT 0, axioms re-checked clean. The `ghr` hole is
  UNTOUCHED (open-ended GHR2007 tensor-power limit + Lean definition of C_3a — deliberately deferred
  per scope). Does NOT raise held (still targets 1.175 < held 1.176).
- **R8: BUMPED the integer core to the FULL held value θ > 1.1771 at (140,265), den=10000.**
  Disproved the long-standing "den=10000 too big for native_decide" assumption by simply running
  the build: the ~1.69M-digit comparison `D^10000 > S^10000·Q^1771` discharges in ~6.7s. Moved the
  point (100,190)→(140,265) — the verified held-source point — and added the tightness negative
  control `griego_140_265_int_cert_tight : ¬(D^10000 > S^10000·Q^1772)` (also native_decide). The
  general `log_bridge` lemma is UNCHANGED (re-used at (A,B)=(1771,10000)); `theta_gt` and
  `c3a_lower_bound` re-specialised to 11771/10000. `lake build C3a` EXIT 0 (2968 jobs, ~18s),
  `#print axioms` clean on all five theorems (NO sorryAx; only propext + Mathlib std + native_decide
  trust axioms). The `ghr` hole is UNTOUCHED (multi-round; per the R8 scope — finite max-operand
  sub-goal only, NOT the bridge). The integer core is now at PARITY with the verified held 1.1771;
  it still does NOT raise `held` while `ghr` is an assumed hypothesis (minimally-verified (*)).
- Borrows: `griego-ntt-push`/`griego-family-larger-mT` (the (s,d,M) values at (140,265), committed
  in scan-mT-results.txt + the integer-inequality certificate form), `exact-sumdiff-dp` lemma (the
  certified counts), `log-bridge` lemma (cached, the log-algebra half).
- The bound this Lean cert's integer core machine-checks is now 1.1771 (== held), but the cert is
  NOT self-contained: `ghr` (the GHR2007 limit read-off) is an assumed hypothesis, so it stays a
  minimally-verified (*) Lean cert — it does NOT raise `held`. Its value is the gold-standard
  machine-checked CERTIFICATION LEVEL of the integer core, now matched to the Python held.
- Next push for THIS sketch: either (a) close `ghr` (multi-round: Lean def of C_3a + tensor-power
  limit), making held a machine-checked theorem; or (b) when griego-ntt-push registers a higher
  held at m>140, bump the integer core to that point/rational (native_decide has ample headroom —
  ~1.7M-digit operands took 6.7s, so even larger den/points are tractable).

## Promotable lemmas
- **`log_bridge` — ALREADY PROMOTED (R7) to `constants/3a/lemmas/log-bridge.md`.** Nothing new to
  promote this round; `log_bridge` is unchanged (R8 re-uses it at (A,B)=(1771,10000)).
  `theorem log_bridge (s d q A B : ℕ) (hs : 0 < s) (hq : 1 < q) (hB : 0 < B)`
  `    (hint : s ^ B * q ^ A < d ^ B) :`
  `    1 + (A : ℝ) / (B : ℝ) < 1 + Real.log ((d : ℝ) / (s : ℝ)) / Real.log (q : ℝ)`.
  Proved in `lean/Sketches/NativeDecideSmallMT.lean` (`namespace C3a`). Fully general; axioms
  `[propext, Classical.choice, Quot.sound]`, no sorryAx.
- (`exact-sumdiff-dp`, the DP-counts lemma, is already cached.)
- **R8: no NEW promotable lemma.** `griego_140_265_int_cert` / `_tight` are sketch-specific
  big-int facts (not general), so not cache candidates.
