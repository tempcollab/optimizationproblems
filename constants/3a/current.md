# C_3a — tracking file (lower bound)

The largest constant such that there exist arbitrarily large sets $A,B$ with $|A+B|\ll|A|$
and $|A-B|\gg|A+B|^{C_{3a}}$. We are pushing the **lower bound**.

## Status

improved

## Bounds            table: 1.1740744 · held: 1.1774273905511207

table: 1.1740744 [G2026] · held: 1.1774273905511207 (verified R3 — exact-counting certificate, d=150, T=285)

Verified R3: lower bound θ ≥ 1.1774273905511207333163761169274037138206151764288896… via
`constants/3a/certificate/certify_3a.py 150 285` (d=150, T=285; base 21, A={0,2,…,10}; same
unchanged drop-1 family and certify_3a.py as the R2 d=110 build, only (d,T) co-tuned). Reviewer
reproduced the run ALONE (305.7 s), confirmed S=|U+U| (146 digits), D=|U−U| (182 digits),
max(U) (199 digits), guard 21 ≥ 2·max(A)+1 printed OK (d-independent, load-bearing), D > S.
Independently re-derived the interval-ln lower endpoint at 2000/4000-bit precision: script θ_iv.a
= …414754546099212 ≤ true θ = …414754813954583 ≤ θ_iv.b = …414755320617595 (interval width
7.7e-121), so θ_iv.a ≤ true θ confirmed. DP code byte-identical to the R2-verified version
(git: no changes since R1 commit); re-confirmed count_sum/count_diff/max_U match brute force at
5 small (d,T) incl. the saturated T=20 base-20-trap case (S=400, D=441). Margin +0.0033530 over
the record, +0.0014218 over the prior held.

Verified R2: lower bound θ ≥ 1.1760055927978140029771014788… via
`constants/3a/certificate/certify_3a.py 110 210` (d=110, T=210; base 21, A={0,2,…,10}).
Reviewer reproduced the run (78.5 s), independently brute-forced both DP recurrences against
full enumeration of U at 7 small (d,T) cases (all match), confirmed the carry-free validity
guard 21 ≥ 2·max(A)+1 is load-bearing (base-20 trap overcounts 382/421 vs 400/441), checked the
GHR2007 lemma hypotheses incl. |U−U| < 2·max(U)+1, and re-derived the interval-ln lower endpoint
at 2000/4000-bit precision (θ_iv.a ≤ true θ). Margin +0.0019312 over the record.

R3 also banked a machine-checked Lean hardening of the *continuum endpoint* half:
`constants/3a/lean/C3a.lean` (toolchain leanprover/lean4:v4.31.0, Mathlib rev
fabf563a7c95a166b8d7b6efca11c8b4dc9d911f) proves `1 + log(D/S)/log q ≥ 1.175 > 1.1740744` from
the d=110 literals via the exact integer reduction `S^40·q^7 ≤ D^40` (norm_num). `lake build`
clean; `#print axioms` = [propext, Classical.choice, Quot.sound] only (no sorryAx). Value 1.175
< held, so it does NOT move held — gold-standard hardening of the easy half.

## Progress log

- R2: VERIFIED first held bound θ ≥ 1.1760055927978140 (>1.1740744 [G2026], margin +0.0019312).
  Exact-integer-counting certificate, d=110/T=210, base-21 gapped-digit family; both DPs
  brute-force-validated, interval-ln endpoint re-derived independently. Slug push-d-cotuned-T.
- R3: VERIFIED raised held to θ ≥ 1.1774273905511207 (d=150/T=285, +0.0014218 over prior held,
  +0.0033530 over record). Same unchanged certify_3a.py/family, only (d,T) co-tuned; reproduced
  ALONE (305.7 s), interval-ln endpoint re-derived at 2000/4000-bit (θ_iv.a ≤ true θ), DP
  byte-identical to R2-verified version + re-spot-checked vs brute force. Slug push-d-cotuned-T.
- R3: VERIFIED Lean hardening (does NOT raise held): sorry-free `constants/3a/lean/C3a.lean`
  machine-checks `1 + log(D/S)/log q ≥ 1.175 > 1.1740744` from the d=110 literals via integer
  reduction S^40·q^7 ≤ D^40 (norm_num); lake build clean, #print axioms shows only the 3 standard
  axioms. Slug lean-formalize-interval-ln.
