# Approach: eta-coefficient-barrier  (REGISTER-AND-PARK — do not re-spend)

**Constant:** 53a — Davenport constant of `C_n^3`.
**Status:** parked frontier marker. No bound built; documents WHY `C_53 < 4` is unreachable
this run so future rounds don't re-spend on small-prime / bookkeeping fixes.

These are established facts from the round-2 math-explorer report
(`/tmp/round-2/math-explorer.md`) and the saved literature digests — recorded here, NOT
recomputed.

## The verified lever: `C_53-ratio ~ 3 + c/3`

With `eta(C_p^3) <= c*p^2`, the extraction lemma gives the additive recursion term
`a(p) ~ M/3 ~ (c/3) p^2`, and the worst case `n = p*q` with `p ~ q` yields
`C_53-ratio ~ 3 + a(p)/p^2 ~ 3 + c/3`. Hence:

- `c = 3` (current proven bound)  =>  `C_53 -> 4`.
- `c = 3 - delta`                 =>  `C_53 <= 4 - delta/3`.

Numerically confirmed by the explorer with the EXACT `a(p) = M - p*j0`: two-prime sup
**3.9987 at (p,q) = (3929, 3931)**, with `a(p)/p^2 -> 1` (0.99899 at p=997, 0.99975 at
p=3989). The sup is genuinely 4, carried entirely by the leading coefficient `c = 3`.

## The published wall (c = 3)

- **Best unconditional general bound:** `eta(C_p^3) <= 3p^2 - 4p - 3`
  [Bhowmik-Schlage-Puchta 2017, "Davenport's constant for groups with large exponent",
  arXiv:1702.03403, Thm 1.2(3); density-increment method]. Leading coefficient is genuinely
  `3` — this is exactly Grinsztajn's Lemma 2.3 input and exactly what pins the sup at 4.
- **The open problem:** `eta(C_p^3) <= p^2` (i.e. `c = 1`) would follow from Alon-Dubiner +
  Roth-type estimates "for all but finitely many pairs," but BSP flag the exceptional small
  pairs as "way beyond current computational means." No published unconditional sub-`3p^2`.
- **Alon-Dubiner** `eta(C_n^r) <= c_r(n-1)+1` is LINEAR in n but with `c_3` astronomically
  large (best explicit `c_3 < ~20233`); useless against `3p^2` in the controlling regime
  (this is the origin of Zakarczemny's old `C_53 <= 20369`).
- **Exact small-prime / special-form values** (`eta(C_3^3)=17`, `eta(C_5^3)=33`,
  `eta(C_n^3)=8n-7` for `n=3^a 5^b`, etc.) cover only `n` built from {2,3,5} — they do NOT
  feed the general large-prime lever and cannot move the sup.

## Refuted theses (do NOT re-try)

- "Improve the small-prime local estimates p=2,3,5,7 to move the record" — REFUTED (round 1
  and re-confirmed round 2). `C_53` is a sup/limit over all n carried by two large primes;
  only the leading coefficient of `a(p)` as `p -> inf` survives. Finite-prime fixes are inert.
- "Tighten the comparison inequality / closed-form bookkeeping" — the bound ratio is exactly
  `4 - (P(n)-1)/(n-1) -> 4` at primorials; bookkeeping alone cannot beat 4.

## The single knob that beats 4

An unconditional `eta(C_p^3) <= (3-delta)p^2` for all `p >= p_0` (sub-`3p^2` leading
coefficient). This is the `sub-3p2-eta-longshot` (NOT registered — research-hard, multi-round,
Lean-hostile continuum/combinatorial core: re-running BSP's density increment tracking a
leading constant below 3, or a new slice-rank/polynomial-method count of zero-sum-free sets in
`C_p^3`). Recorded here so the frontier is captured once.
