# R3 explorer follow-up notes on MT26 (arXiv:2602.23282)

Read deeper into the HTML body for round-3 scouting. New/confirmed facts beyond the R1 digest:

## Set hierarchy (confirms R2 correction, now with paper props)
- **Prop 2.1:** every Sidon set is a (4,5)-set.
- **Prop 2.2:** every (4,5)-set is a weak-Sidon set.
- Figure 2: STRICT inclusions Sidon ⊊ (4,5)-set ⊊ weak-Sidon.
- So (4,5)-set (difference condition) is strictly between Sidon and weak-Sidon. The R1
  digest's "(4,5)-set ≡ weak-Sidon" was wrong; R2 corrected it. CONFIRMED against paper props.

## The 14-pt record gadget A_base
- Paper gives A_base with NO explanation of how it was found, NO modular/arithmetic structure,
  NO optimality claim, NO conjecture about whether 4/7 is tight. It is used ALONE (not scaled).
- Paper proves ONLY f(14) ≤ 8. No table of f(n) for other n. => every N ≠ 14, 21 is genuinely
  unexplored slack (21 ruled out by the 9/17 floor, see Rules).

## Lemma 3.6 — the concatenation/blow-up lemma (KEY for the N≈30 angle)
- "Let A,B ⊂ ℝ be two finite (4,5)-sets. Then there exist q>0 and t∈ℝ such that
  C := A ∪ (qB+t) is a (4,5)-set, |C|=|A|+|B|, and h(C) ≤ h(A)+h(B)."
- Used for the existence/inf direction of Thm 1.5, NOT to build a record gadget.
- CRITICAL CONSEQUENCE for our search: with well-separated scales there are no cross-scale
  3-APs, so h(C) = h(A)+h(B) EXACTLY (the ≤ is tight here). Ratio(C) = mediant of the two
  component ratios => lies BETWEEN them => concatenation CANNOT beat the best component.
  - Two A_base copies: N=28, h=16, 16/28 = 4/7 exactly (ties, no beat).
  - A beat therefore needs a SINGLE IRREDUCIBLE gadget whose 3-AP structure spans the whole
    set and pushes h strictly below the additive value — not an assembly of well-separated
    blocks. This is why an N≈30 search must target an indecomposable set.

## GL95 prior upper bound 3/5 — Fibonacci construction
- MT26 says GL95's 3/5 upper bound "is constructed using an infinite sequence based on
  Fibonacci numbers." (Their lower bound reduces to a 3-uniform-linear-hypergraph transversal
  problem — same H(A) viewpoint as MT26.)
- This is a concrete recursive/structural TEMPLATE for the `modular-construction` angle, but it
  only achieves 3/5 > 4/7, so it is weaker than the current record — a lead for STRUCTURE
  (how to lay out points so 3-APs proliferate while keeping the difference condition), not a
  competitive ratio. Original GL95 paper: J. Combin. Theory Ser. B 64 (1995) 108–118
  (ScienceDirect S0095895685710283).

## Literature scan (June 2026)
- No paper after MT26 (Feb 26 / rev Mar 6 2026) has improved 9/17 ≤ c* ≤ 4/7. The Sárközy–Sós
  weak-Sidon companion result (g(n)=⌈(n+1)/2⌉, limit 1/2) is a DIFFERENT constant (weak-Sidon,
  not (4,5)-set) and does not bear on C_5b's 4/7.
