# zheng-nonuniform-ratefn — generalize Zheng's rate function to non-uniform digits (THEORY/GUIDE)

**Direction:** lower bound on C_3a. **Record to beat:** 1.1740744 [G2026].
**Borrows:** the finite exact-DP engine (`ghr_dp.py`) for the realization step.

## Strategy
Zheng's Cramér large-deviation asymptotic assumes the **uniform** alphabet `{0..B}` (mean
`B/2`, uniform mgf), so his closed-form θ does **not** cover Griego's non-uniform set
(`{0..10}\{1}`). Nobody has written the limiting θ for a **general digit distribution** `p` on a
finite alphabet `A`. Deriving it (a) predicts which alphabet shape maximizes the exponent —
guiding/replacing the brute search of `alphabet-search-dp`, and (b) upper-bounds what any finite
construction in this single-set family can reach (a principled ceiling below 1.25). Explorer
levers #2 and #3.

## Engine to derive
With digits iid from `p` on `A`, cap `T = c·d`:
`lim (1/d) log|U| = H(p) − I_p(c)`, `I_p(c) = sup_t (tc − log E_p[e^{ta}])` the Legendre
transform of `p`; analogous joint-cap exponents for `|U+U|` (a+a′ convolution) and `|U−U|`
(a−a′); `log q → d·log(2 max A + 1)`. Assemble θ_inf as the ratio. **Validation target:**
uniform `p` must reproduce Zheng's table (`B=5 → θ−1 = 0.1730773`).

## Holes
- **H1 RATE FUNCTION:** implement `I_p(c)` and joint-cap sumset/diffset exponents for general
  `p`; validate against Zheng's uniform table.
- **H2 OPTIMIZE (hard):** maximize θ_inf over `(A, p, c)` — variational problem over alphabet
  support and weights. Expected to point near/beyond Griego's shape.
- **H3 REALIZE + CERTIFY (hard):** convert the optimal `(A,p,c)` into a finite `(A,d,T)` (via
  digit multiplicity / per-position frequency) and exact-DP-certify θ > 1.1740744. Tying the
  asymptotic optimum to a *valid finite* construction is the second hard step.

## Hard step
Two: the variational optimization (H2) and tying its asymptotic limit to a finite, exactly
certifiable construction (H3). The asymptotic alone is not a bound — it must be realized
finitely and certified.

## Certify
The asymptotic guides; the **bound** is certified by the finite Python integer DP (H3).
Not directly Lean-fit (continuous optimization), but its output `(A,d,T)` feeds the Lean line.
