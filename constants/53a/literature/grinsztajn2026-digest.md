# Digest: Grinsztajn 2026, "An upper bound for the Davenport constant of C_n^3"

Source: https://github.com/maaxgrin/davenport-cn3-bound (PDF saved at constants/53a/literature/pdfs/davenport.pdf, text at davenport.txt).
Discovered with GPT-5.5 Pro; deduction checked in a *conditional* Lean 4 formalization with Aristotle (DavenportCn3/Main.lean) that AXIOMATIZES the cited zero-sum inputs.

## Main result
Theorem 1.1: for every n >= 2, D(C_n^3) <= 4n - P(n) - 2, where P(n) = max_{p^a || n} p^a (largest primary component).
Since P(n) >= 2, D(C_n^3) <= 4(n-1), hence S := sup_{n>=2} (D(C_n^3)-1)/(n-1) <= 4.
Improves Zakarczemny's S <= 20369 to 3 <= S <= 4. Conjectural value S = 3 (equiv. pointwise D(C_n^3)=3(n-1)+1).

## Notation
- D_k(G): least N s.t. every length->=N sequence has k pairwise-disjoint nonempty zero-sum subsequences. D_1 = D.
- eta(G): least N s.t. every length->=N sequence has a nonempty zero-sum subsequence of length <= exp(G).

## Inputs used (these are what the conditional Lean treats as axioms)
1. p-group / lower bound: D(G) >= D*(G) = 1 + sum(n_i - 1), equality for p-groups [Gao-Geroldinger].
   => D(C_{p^a}^3) = 3p^a - 2, and D(C_m^3) >= 3m - 2.
2. Lemma 2.1 (Inductive method, proved in-paper): for H <= G, D(G) <= D_{D(H)}(G/H).
3. Lemma 2.2 (Extraction, proved in-paper): if eta(G) <= M and D_j(G) <= M then D_k(G) <= M + e(k-j) for k>=j, e=exp(G).
4. Lemma 2.3 (LOCAL ESTIMATE -- the load-bearing finite input): for every prime p and k >= 3p-2,
   D_k(C_p^3) <= p*k + p^2.
   - p=2: D_k(C_2^3) = 2k+3 (k>=2) [Freeze-Schmid]; 2k+3 <= 2k+4 = 2k + 2^2. (slack 1 already)
   - p=3: eta(C_3^3)=17, D_3(C_3^3)<=17 [Bhowmik-Schlage-Puchta]; Lemma 2.2 => D_k <= 3k+8 <= 3k+9 = 3k+3^2. (slack 1)
   - p=5: eta(C_5^3)=33, D_3(C_5^3)<=33 [B-SP]; => D_k <= 5k+18 <= 5k+25 = 5k+5^2. (slack 7!)
   - p>=7: M=(p+1)(3p-7)+4 = 3p^2-4p-3, eta(C_p^3)<=M, D_j bound, choose j0=floor(x); gives D_k <= pk+p^2.

## Proof of main theorem (Section 3) -- the global induction
Q = P(n). Factor n = Q*p_1*...*p_s, each p_i <= Q (since Q is the largest primary component).
m_0 = Q (prime power, base case D(C_Q^3)=3Q-2 = 4Q-Q-2). m_i = Q*p_1*...*p_i.
Inductive step C_{pm}^3 has subgroup H ~ C_m^3, quotient ~ C_p^3:
  D(C_{pm}^3) <= D_{D(C_m^3)}(C_p^3)   [Lemma 2.1]
             <= p*D(C_m^3) + p^2       [Lemma 2.3 with k = D(C_m^3) >= 3m-2 >= 3p-2]
             <= p*(4m - Q - 2) + p^2   [induction hyp]
The clean closed form 4pm-Q-2 follows from the COMPARISON INEQUALITY
   p^2 - 2p + 2 <= (p-1)Q,  true since Q>=p gives (p-1)Q >= p^2-p >= p^2-2p+2.
This comparison is LOOSE when Q >> p.

## Where the slack lives (explorer's numerical analysis)
The recursion actually produced is D_i = p_i*D_{i-1} + p_i^2 (additive p^2 term), D_0 = 3Q-2.
Tracking D/m: D_i/m_i = D_{i-1}/m_{i-1} + p_i/m_{i-1}. The whole excess over 3 is the sum of p_i/m_{i-1},
which is driven entirely by the +p^2 additive term.
- Replacing +p^2 by a LINEAR-in-p term collapses S to 3 exactly:
  with additive term 2p-2 (the conjecturally-correct value of D_k(C_p^3) - p*k for large k), numerical sup = 3.000.
  with +p^2: numerical sup ~ 3.99 (approaches 4).
  with +3p: sup ~ 4.98.
=> THE ENTIRE 3-to-4 GAP IS CARRIED BY THE p^2 IN LEMMA 2.3. Any sub-quadratic local estimate beats 4.

The worst-case ratios under the p^2 recursion are reached at SMALL n (worst found ~3.99 at n=128, i.e. p=2
chain), so improving the SMALL-PRIME local estimates (p=2,3,5,7) -- each a finite zero-sum verification --
directly pulls the sup below 4. The comparison inequality p^2-2p+2<=(p-1)Q is a second, independent source
of slack for the closed-form (loose when Q large), but it does not by itself lower the sup.
