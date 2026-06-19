# Sketch `lean-native-decide-smallmt` — machine-checked (Lean) C_3a lower bound

## Strategy
Port the verified C_3a lower bound to a `lake build`-passing Lean theorem — the gold-standard
certificate (CLAUDE.md prefers Lean-fit; the held 1.176 bound is currently only a Python big-int
cert). The load-bearing step is a SINGLE pure big-integer inequality, exactly `native_decide`-shaped.

**The operand-size choice is the whole game.** The held 1.176 cert at (110,210) uses denominator
10000 → operands `D^10000`, `S^10000·Q^1760` are ~1.3M digits, too big for the kernel-trusted
compiled `native_decide` term. So this Lean sketch deliberately takes a SMALLER-θ point with a
SMALL denominator:
- point (m,T)=(100,190), A={0,2,…,10}, b=21 (Griego family);
- rational 47/40 = 1.175, which still strictly beats the record 1.1740744 (Griego 2026);
- cleared-denominator form `D^40 > S^40·Q^7`, operands only ~4800 digits — `native_decide` finishes
  in ~0.5s (verified, R4).

This certifies a Lean-machine-checked *beat* (1.175 > 1.1740744), not the largest θ. The held 1.176
stays the Python certificate; this is the complementary Lean-fit certificate of a record beat.

## Why the integers are trustworthy
S=|U+U|, D=|U-U|, Q=2·max(U)+1 at (100,190) are the output of the certified `exact-sumdiff-dp`
lemma (constants/3a/lemmas/exact-sumdiff-dp.md), cross-checked vs brute force on 12 cases in R3.
They are embedded as explicit literals in the Lean file; the DP need NOT be formalized — only the
final integers + the inequality are in Lean.

## Holes (R5 update)
The R4 `bridge` hypothesis bundled TWO independent steps: (A) the log algebra
`(D^40>S^40·Q^7) ⟹ θ>47/40`, and (B) the GHR2007 read-off `C_3a ≥ θ`. **R5 splits them and
FORMALIZES (A) in Lean**; only (B) remains assumed.

1. **`griego_100_190_int_cert : D^40 > S^40·Q^7` — CLOSED (hole-free).** `native_decide`. The
   load-bearing integer step. `#print axioms` → `[propext,
   griego_100_190_int_cert._native.native_decide.ax_1_1]` (native_decide trust axiom; NO sorryAx).
   Operands ~4800 digits.
2. **LOG-ALGEBRA HALF (A) — CLOSED THIS ROUND (R5), hole-free.** New lemma
   `log_bridge (s d q : ℕ) (hs : 0<s) (hq : 1<q) (hint : s^40*q^7 < d^40) :`
   `(47:ℝ)/40 < 1 + Real.log((d:ℝ)/s)/Real.log q`. Pure real arithmetic via Mathlib
   (`Real.log_lt_log`, `Real.log_pow`, `lt_div_iff₀`, `div_pow`, `positivity`, `nlinarith`).
   `#print axioms log_bridge` → `[propext, Classical.choice, Quot.sound]` (Mathlib standard axioms
   only; NO sorryAx). Specialised to the certified literals as `theta_gt : (47:ℝ)/40 < theta`,
   where `theta := 1 + log(D/S)/log Q`. **To enable this the project now requires Mathlib**, pinned
   to the v4.31.0 tag (rev `fabf563a…`) in `lake-manifest.json` — `lake build C3a` EXIT 0 (~2968
   jobs, oleans from the Azure cache).
3. **Top theorem `c3a_lower_bound` — CLOSED (hole-free given the ONE remaining cited step).**
   `c3a_lower_bound (ghr : theta ≤ C3aReal) : (47:ℝ)/40 < C3aReal := lt_of_lt_of_le theta_gt ghr`.
   `C3aReal` is the opaque real C_3a; `(47:ℝ)/40 < C3aReal` is "C_3a > 1.175 > 1.1740744".
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
- **Machine-checked, hole-free (no sorryAx):** (i) the integer inequality `D^40 > S^40·Q^7` at
  (100,190) via `native_decide`; (ii) **NEW R5** — the log-algebra step
  `(D^40>S^40·Q^7) ⟹ θ>47/40` via `log_bridge`/`theta_gt`, proved over ℝ with Mathlib; and
  (iii) the `c3a_lower_bound` derivation `(47:ℝ)/40 < C3aReal` from `theta_gt` and `ghr`.
- **Assumed (single visible hypothesis, cited [GHR2007]):** `ghr : theta ≤ C3aReal` — the
  tensor-power limit read-off `C_3a ≥ θ`. NOT yet formalized.
- So the Lean file now establishes, hole-free, BOTH the integer fact AND the log algebra that turn
  it into "θ > 1.175", reducing "C_3a > 1.175" to the single named GHR2007 limit read-off — a
  strictly smaller assumed hole than R4's bundled `bridge`. Still NOT self-contained: do not claim
  θ>1.175 is a complete Lean proof while `ghr` is assumed.

## Literals re-derived from scratch (R4)
Recomputed (S,D,Q) at (100,190) independently with the certified `exact-sumdiff-dp` DP after the
small-case brute-force oracle sanity check (self_test: 8 cases incl. clamp-exercising (4,40),(5,20),
ALL match). The Lean literals were string-matched against this recomputation:
- S=|U+U| — 97 digits, head 86388581 / tail 26122695 — MATCH.
- D=|U−U| — 121 digits, head 13829645 / tail 69875299 — MATCH.
- Q=2·max(U)+1 — 133 digits, head 16669764 / tail 42124381 — MATCH.
θ = 1.175495508 > 1.1740744 (record). No literal mismatch.

## State
- R4: Lake project bootstrapped at `constants/3a/lean/` (Lean v4.31.0, core only). Integer core
  hole-free; whole bridge bundled as one assumed hypothesis.
- **R5: added a pinned Mathlib dependency** (v4.31.0 tag, rev `fabf563a…`, in
  `lake-manifest.json`) and FORMALIZED the log-algebra half of the bridge (`log_bridge`,
  `theta_gt`). `lake build C3a` EXIT 0 (~2968 jobs; Mathlib oleans from the Azure cache). The
  remaining assumed step is narrowed to exactly the GHR2007 limit read-off `ghr : theta ≤ C3aReal`.
  This is the ONLY Lean sketch, so the Mathlib dep affects no sibling.
- Borrows: `griego-family-larger-mT` (the (s,d,M) values and the integer-inequality certificate
  form), `exact-sumdiff-dp` lemma (the certified counts).
- The bound this Lean cert proves (1.175) is BELOW the held 1.176 — it does not raise `held`; its
  value is the machine-checked certification level (a `lake build` cert is the gold-standard
  certificate CLAUDE.md prefers). Matching 1.176 in Lean needs the den=10000 operands — out of
  `native_decide` reach for now.

## Promotable lemmas
- **`log_bridge`** (proved green R5, hole-free, axioms `[propext, Classical.choice, Quot.sound]`).
  Statement:
  `theorem log_bridge (s d q : ℕ) (hs : 0 < s) (hq : 1 < q) (hint : s^40 * q^7 < d^40) :`
  `(47:ℝ)/40 < 1 + Real.log ((d:ℝ)/(s:ℝ)) / Real.log (q:ℝ)`.
  Proved in `lean/Sketches/NativeDecideSmallMT.lean` (`namespace C3a`). REUSABLE: this is the
  cleared-denominator-integer-inequality ⟹ real-θ-bound step for the SPECIFIC rational 47/40 at
  this point. A fully general cache lemma would parametrise the exponents/target
  (`d^B > s^B · q^A ⟹ θ > 1 + A/B`); the reviewer may prefer to promote that generalised form
  rather than the 47/40-specialised one. Flagging the green proof so the reviewer can certify
  whichever shape it wants into `lemmas/`. (The 47/40 numerals are the only sketch-specific part;
  the proof skeleton — `Real.log_lt_log` ∘ `Real.log_pow` ∘ `lt_div_iff₀` ∘ `div_pow` ∘ `nlinarith`
  — generalises verbatim.)
- (`exact-sumdiff-dp`, the DP-counts lemma, is already cached.)
