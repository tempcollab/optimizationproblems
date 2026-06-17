# Digest: Bhowmik & Schlage-Puchta 2017, "Davenport's constant for groups with large exponent"

Source: arXiv:1702.03403 (PDF + text saved under constants/53a/literature/pdfs/arxiv_1702.03403.{pdf,txt}).
This is Grinsztajn's reference [2] — the SOURCE of the load-bearing local input `eta(C_p^3) <= 3p^2-4p-3`.

## The eta(C_p^3) bound (the load-bearing input for p>=7)
Theorem 1.2(3): for prime p>=7 and d>=3,
   eta(Z_p^d) <= (p^d - p)/(p^2 - p) * (3p - 7) + 4.
For d=3 this collapses (since (p^3-p)/(p^2-p) = p+1) to
   eta(C_p^3) <= (p+1)(3p-7) + 4 = 3p^2 - 4p - 3.   <-- EXACTLY Grinsztajn's input.
Proved in Section 4 by the **density-increment method**. The leading term is genuinely
quadratic (d*p^2 in d dimensions, i.e. 3p^2 for d=3); there is NO sub-3p^2 leading
coefficient hiding in the derivation.

## The conditional p^2 they could NOT prove
Theorem 1.4 / remark (lines ~296-303): "the statement is trivial if eta(Z_p^d) <= p^{d-1}";
for d=3 that is eta(C_p^3) <= p^2. They note this STRONGER linear/quadratic-with-coeff-1 form
follows from the Alon-Dubiner theorem + Roth-type estimates "for all but finitely many pairs",
BUT the exceptional small pairs {p=2 all d; (3,3),(3,4),(3,5),(5,3)} are "way beyond current
computational means." So they prove only the QUADRATIC 3p^2 unconditionally. A genuine
unconditional eta(C_p^3) <= (3-delta)p^2 for all large p is NOT in this paper.

## Other contents (not directly used)
- Theorem 1.1: D(G) <= exp(G) + |G|/exp(G) - 1 when exp(G) >= sqrt|G|; D(G) <= 2 sqrt|G| - 1
  otherwise. (Large-exponent regime — not the C_p^3 elementary case.)
- Theorem 1.2(1),(2): exact s(Z_3^d), s(Z_5^d) values for small d (Bose/Pellegrino/Edel et al./Potechin).
- Theorem 1.3: existence of zero-sums of length ~ p or 3p (adapts Reiher's proof of Kemnitz).

## Bottom line for 53a
The best PUBLISHED unconditional upper bound on eta(C_p^3) for general large prime p is the
QUADRATIC 3p^2-4p-3. No sub-3p^2 leading coefficient exists in print. Beating C_53 < 4
requires eta(C_p^3) <= (3-delta)p^2 for ALL large p (see math-explorer R2 arithmetic), which
would be a new unconditional rank-3 eta result — a research-level open problem, not a bookkeeping fix.
