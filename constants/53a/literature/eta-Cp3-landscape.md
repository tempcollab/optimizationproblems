# eta(C_p^3) landscape — what is known (math-explorer R2)

The decisive lever for C_53 < 4 is a smaller eta(C_p^3) for ALL large p. Survey of known bounds:

## Lower bound (construction)
- eta(C_n^r) >= (2^r - 1)(n-1) + 1  [standard construction]. For r=3: eta(C_p^3) >= 7p - 6.
  So eta(C_p^3) is at LEAST linear with leading coeff 7. The conjectural truth is linear ~7p.

## Upper bounds
- **General large prime p (UNCONDITIONAL): eta(C_p^3) <= 3p^2 - 4p - 3** [Bhowmik-Schlage-Puchta
  2017, Thm 1.2(3), density-increment]. QUADRATIC. This is the only general unconditional bound
  with a usable leading coefficient — and it is what Grinsztajn plugs in.
- **Alon-Dubiner** [Combinatorica]: eta(C_n^r) <= c_r (n-1) + 1, LINEAR in n for fixed r,
  with c_r >= 2^r - 1 and c_r <= (c r ln r)^r (absolute). For r=3 the best EXPLICIT general
  bound is c_3 < ~20233 (this is the origin of Zakarczemny's C_53 <= 20369). Linear, but the
  constant is astronomically larger than 3p^2 for every p of interest, so it does NOT beat the
  quadratic in the regime that controls the sup (two near-equal large primes).
- **Exact small-prime values:** eta(C_3^3)=17, eta(C_5^3)=33 [Bhowmik-Schlage-Puchta].
  These lift (inductive method) to EXACT linear formulas for special COMPOSITE forms:
  eta(C_n^3)=8n-7 for n=3^a 5^b, eta(C_n^3)=7n-6 for n=2^a 3. These are NOT bounds for general
  prime p — they only cover n built from {2,3,5} (or 3,5), the small-prime-power chains.

## The gap that kills the angle
- Conjectured truth: eta(C_p^3) ~ 7p (linear).
- Best unconditional general bound: 3p^2 (quadratic).
- A SUB-3p^2 unconditional bound (any eta(C_p^3) <= (3-delta)p^2 for all large p) is the
  missing ingredient. It does not exist in print. BSP explicitly flag that proving even
  eta(C_p^3) <= p^2 unconditionally is "way beyond current computational means" for the
  exceptional small pairs, and open in general for large p.

## Arithmetic linking eta to C_53 (math-explorer R2, verified numerically)
Grinsztajn's extraction (Lemma 2.2): a(p) = M - p*j0 where M = eta-bound, j0 ~ x ~ 2M/(3p).
=> a(p) ~ M - p*(2M/(3p)) = M/3.  With M = c*p^2:  a(p) ~ (c/3) p^2.
Single-step at n=p*q, p~q:  C_53-ratio ~ 3 + a(p)/p^2 ~ 3 + c/3.
=> eta(C_p^3) <= c p^2  ==>  C_53 <= 3 + c/3.
   c=3 (current 3p^2)  -> C_53 -> 4 (confirmed: a(p)/p^2 -> 1, two-prime sup = 3.9987 at p=3929,q=3931).
   c=3-delta           -> C_53 <= 4 - delta/3.
So ANY eps reduction in the LEADING coeff of eta(C_p^3) (for all large p) strictly beats 4.
But a sub-leading / lower-order improvement, or a fix at finitely many primes, does NOTHING:
the sup is a limit p,q->infinity and only the leading coefficient survives.
