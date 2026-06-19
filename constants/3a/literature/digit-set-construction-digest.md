# C_3a digit-set lower-bound constructions — literature digest (R17)

C_3a = largest c with arbitrarily large A,B ⊆ ℤ, |A+B| ≪ |A|, |A−B| ≫ |A+B|^c.
Movable side = LOWER bound. Upper bound 4/3 [GHR2007]. All record lower bounds since 2007
come from the **GHR digit-set lemma**, NOT from the A,B sumset definition directly.

## The GHR lemma (the engine of every record)

[GHR2007] For any finite U ⊆ ℤ≥0 with 0 ∈ U,
  C_3a ≥ 1 + log(|U−U| / |U+U|) / log(2·max(U)+1).
The digit-set instantiation: fix base B and alphabet A ∋ 0; take
  U(A,B,d,T) = { Σ_{i<d} a_i B^i : a_i ∈ A, Σ a_i ≤ T }.
If **B > 2·max(A)** (carry-free regime) then u±v has digit vector (a_i ± b_i) over A±A with
no carries; the only cross-position coupling is the digit-sum cap T. So |U±U| is an EXACT
integer computable by a cap-coupled DP without enumerating |U| ≈ |A|^d elements.

**The 1.25 ceiling (recorded in constants/3a.md, attributed to a GHR2007 lemma):** lower bounds
obtained THIS way (digit-set U) cannot exceed 1.25. So the digit-set headroom above the current
record is 1.1740744 → ~1.25. (I could not re-derive the 1.25 from the predecessor papers — none
of Gerbicz/Zheng/AlphaEvolve restate it; treat it as the repo's recorded GHR fact, not
re-verified this round. It does NOT bound C_3a itself, only the digit-set CONSTRUCTION method.)

## Record chain (all digit-set, all 2025–26)

| value | who | structure |
|---|---|---|
| 1.14465 | GHR2007 | original digit set |
| 1.1479 (table) / 1.1584 (papers) | AlphaEvolve [GGSWT2025] | evolved digit set |
| 1.173050 | Gerbicz [G2025] | base-11 (B=5), alphabet {0..5}, m=81411, L=65536, FINITE |
| 1.173077 | Zheng [Z2025] | base-11 (B=5), ASYMPTOTIC limit (m,L→∞), variational/large-deviations |
| **1.1740744** | **Griego [G2026], PR #71** | **base-21, alphabet {0,2,3,…,10} (skips 1!), d=80, T=150, FINITE** |

## Gerbicz [G2025], arXiv:2505.16105 — 1.173050

- Map g(x₁,…,xₘ) = Σ_k x_k·(2B+1)^k, x_k ∈ {0,…,B}, with a cap via L (∈ W(m,L,B)).
  So base = 2B+1, alphabet = {0..B} (the full GHR carry-free choice: 2·max(A)=2B < 2B+1).
- **FINITE explicit construction**: m=81411, L=65536, **B=5** (base 11, alphabet {0,1,2,3,4,5}).
- Parametric search 1≤m≤128, L=64, 1≤B≤7; observed empirically: for fixed L the largest θ
  occurs at **B=5 and m≈(5/4)·L**. Then scaled up L. "Further improvements might be possible
  by increasing L." No optimality claim; the m≈(5/4)L density relation is the key heuristic.

## Zheng [Z2025], arXiv:2506.01896 — 1.173077

- SAME map family as Gerbicz (g, base 2B+1, alphabet {0..B}, cap), but takes m,L→∞ and computes
  the **asymptotic limit** via large-deviations rate functions I(c,B).
- The limit is a VARIATIONAL formula: θ₀ = sup over (B,r,a) of an explicit ratio of entropy/rate
  terms over log(2B+1). Numerically maximized over B∈{3..10}, r∈(0.5,2): the **sup is at B=5**,
  r≈0.55–0.60, a≈0.18–0.22, giving 1.173077.
- KEY: 1.173077 is the **asymptotic supremum of the {0..B} digit-set family** (over B, density,
  weight). It is NOT a hard ceiling for C_3a — it is the d→∞ ceiling of THAT specific alphabet
  family. No 1.25 discussion.

## Griego [G2026], PR #71 — 1.1740744 (the record)

- **FINITE** digit set, NOT asymptotic: A = {0,2,3,4,5,6,7,8,9,10} (note: **omits 1**),
  B = 21 = 2·10+1, d = 80, T = 150 (density ρ = T/d = 1.875). Carry-free (B=21 > 2·max(A)=20).
- Exact integers (reproduced bit-for-bit by the R16 engine):
  - |U+U| = 75448362167176243488362019935078206851619643198150854886920234689186981134888 (77 digits)
  - |U−U| = 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415 (96 digits)
  - max(U) = 2995805288150731620410662946668903948341032736664352641511848666717243994160370658179324073879212562136150 (106 digits)
  - value = 1.174074447693521163363531806… (directed-rounded > 1.1740744)
- **No reasoning given for the parameters; no optimality claim** (PR #71 itself; params
  "prepared with assistance from ChatGPT 5.5 Pro"). Pure found point with slack.

## The decisive structural observation (R17)

**Griego's FINITE d=80 value (1.1740744) already EXCEEDS Zheng's ASYMPTOTIC supremum of the
{0..B} family (1.173077).** This is only possible because Griego uses a **different alphabet
shape** — base 21 with alphabet {0,2,…,10} that DROPS the digit 1 — which is outside Zheng's
{0,1,…,B} family. Dropping 1 raises |U−U|/|U+U| (fewer small-difference collisions) at the cost
of a slightly larger max(U). So:
- The digit-set frontier is governed by the choice of (alphabet shape, base, density), and the
  TWO known good regions (Zheng's B=5 full-alphabet asymptotic vs Griego's B=21 drop-1 finite)
  give nearly equal values — the surface is flat near the top but NOT yet mapped for asymmetric
  ("drop-some-digit") alphabets at large d.
- The principled question is the **asymptotic supremum over alphabet SHAPE** (which digits to
  include), not just over (B, density) as Zheng did. Griego is one finite sample of a better
  shape; its d→∞ limit is unknown and is the natural target.
</content>
</invoke>
