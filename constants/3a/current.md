# C_3a — tracking file (lower bound)

The largest constant such that there exist arbitrarily large sets $A,B$ with $|A+B|\ll|A|$
and $|A-B|\gg|A+B|^{C_{3a}}$. We are pushing the **lower bound**.

## Status

improved

## Bounds            table: 1.1740744 · held: 1.1760055927978140

table: 1.1740744 [G2026] · held: 1.1760055927978140 (verified R2 — exact-counting certificate, d=110, T=210)

Verified R2: lower bound θ ≥ 1.1760055927978140029771014788… via
`constants/3a/certificate/certify_3a.py 110 210` (d=110, T=210; base 21, A={0,2,…,10}).
Reviewer reproduced the run (78.5 s), independently brute-forced both DP recurrences against
full enumeration of U at 7 small (d,T) cases (all match), confirmed the carry-free validity
guard 21 ≥ 2·max(A)+1 is load-bearing (base-20 trap overcounts 382/421 vs 400/441), checked the
GHR2007 lemma hypotheses incl. |U−U| < 2·max(U)+1, and re-derived the interval-ln lower endpoint
at 2000/4000-bit precision (θ_iv.a ≤ true θ). Margin +0.0019312 over the record.

## Progress log

- R2: VERIFIED first held bound θ ≥ 1.1760055927978140 (>1.1740744 [G2026], margin +0.0019312).
  Exact-integer-counting certificate, d=110/T=210, base-21 gapped-digit family; both DPs
  brute-force-validated, interval-ln endpoint re-derived independently. Slug push-d-cotuned-T.
