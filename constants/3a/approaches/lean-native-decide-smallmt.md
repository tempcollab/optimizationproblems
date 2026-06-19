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

## Holes (R4 update)
1. **`griego_100_190_int_cert : D^40 > S^40·Q^7` — CLOSED (hole-free).** `native_decide`. Built
   green, no `sorry`. The load-bearing step. `#print axioms` →
   `[griego_100_190_int_cert._native.native_decide.ax_1_1]` (the native_decide trust axiom; NO
   sorryAx). Operands ~4800 digits, ~0.5s.
2. **Top theorem made FAITHFUL (R4) — `c3a_lower_bound`, hole-free.** The R3/early-R4 Nat
   placeholders (`(1175:Nat)>1174`, `(47:Nat)*40<48*40`) — green proofs of irrelevant statements
   smuggled by `sorry` — are REMOVED. Replaced by a single theorem
   `c3a_lower_bound (bridge : D^40 > S^40*Q^7 → 1175 ≤ Cnum) : 1175 ≤ Cnum := bridge
   griego_100_190_int_cert`, where `Cnum := ⌊1000·C_3a⌋`, so the conclusion `1175 ≤ Cnum` is
   exactly "C_3a ≥ 1.175 > 1.1740744". This is `sorry`-free and adds NO axiom (`#print axioms
   c3a_lower_bound` → the same single native_decide axiom only).
3. **The one cited step is now an EXPLICIT, VISIBLE HYPOTHESIS, not a hole.** `bridge` =
   [GHR2007] read-off `C_3a ≥ θ` (legit because 0∈A and b=21 > 2·max(A)=20 ⇒ g injective,
   carry-free) ∘ real-log algebra `(D^40 > S^40·Q^7) ⟹ θ > 47/40`. Making it a hypothesis (not an
   `axiom`, not a `sorry`) is the honest encoding: the reader sees precisely what is assumed, and
   the proof body itself is gap-free. The remaining Lean-internal work — formalizing GHR2007 and a
   `Real.log` monotonicity bridge to *discharge* `bridge` (needs Mathlib) — does NOT touch the
   load-bearing integer comparison and is the documented next step.

## Verification level (be precise)
- **Machine-checked, hole-free (no sorryAx):** the integer inequality `D^40 > S^40·Q^7` at
  (100,190) — equivalently θ > 47/40 = 1.175 — and the `c3a_lower_bound` derivation from it given
  `bridge`.
- **Assumed (visible hypothesis, cited [GHR2007] + log algebra):** `bridge`. Not yet formalized.
- So the Lean file establishes, hole-free, the exact integer fact that powers a 1.175 beat, and
  reduces "C_3a > 1.175" to a single named, cited bridge — with no `sorry` and no smuggled axiom.

## Literals re-derived from scratch (R4)
Recomputed (S,D,Q) at (100,190) independently with the certified `exact-sumdiff-dp` DP after the
small-case brute-force oracle sanity check (self_test: 8 cases incl. clamp-exercising (4,40),(5,20),
ALL match). The Lean literals were string-matched against this recomputation:
- S=|U+U| — 97 digits, head 86388581 / tail 26122695 — MATCH.
- D=|U−U| — 121 digits, head 13829645 / tail 69875299 — MATCH.
- Q=2·max(U)+1 — 133 digits, head 16669764 / tail 42124381 — MATCH.
θ = 1.175495508 > 1.1740744 (record). No literal mismatch.

## State
- New this round (R4). Lake project bootstrapped at `constants/3a/lean/` (Lean v4.31.0, core only,
  no Mathlib dep — builds in ~0.5s, EXIT 0). The load-bearing `native_decide` is green; the top
  theorem is now faithful and `sorry`-free.
- Borrows: `griego-family-larger-mT` (the (s,d,M) values and the integer-inequality certificate
  form), `exact-sumdiff-dp` lemma (the certified counts).
- The bound this Lean cert proves (1.175) is BELOW the held 1.176 — it does not raise `held`; its
  value is the machine-checked certification level (a `lake build` cert is the gold-standard
  certificate CLAUDE.md prefers). Matching 1.176 in Lean needs the den=10000 operands — out of
  `native_decide` reach for now.

## Promotable lemmas
None this round (the integer-inequality theorem is sketch-specific to (100,190); the reusable
DP-counts lemma `exact-sumdiff-dp` is already cached).
