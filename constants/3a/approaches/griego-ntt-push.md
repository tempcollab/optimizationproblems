# Sketch `griego-ntt-push` — fast convolution DP to push m=130-200 (higher θ)

## Strategy
Continue the verified Griego-family climb past the m=110 compute wall. The held bound C_3a > 1.176
sits at (110,210); θ is monotone increasing in m toward a conjectural family supremum Λ ≈ 1.185
(scout R4 power-law fit, comfortably below the 1.25 GHR cap). The only cheap lever past 1.176 is
MORE m on the SAME family (base-21 / A={0,2,…,10} is the unique optimal alphabet — L1 proved this).

**Why a new algorithm (not just more of L2):** the R3 dynamic-low-clamp sum-set bitmask DP closes
m≤110 in seconds but hits a wall at m=130+ (mask width grows with T; a single m=130 point did not
finish in ~5 min of scouting, R4). To reach m=130-200 the sum-set count needs a fast-convolution
path — NTT/exact-integer-FFT per layer and/or repeated squaring in m (m enters logarithmically).
The diff-set DP (2-D) and max_U (greedy) already scale cheaply; only the sum-set count is the wall.

This is the m-push compute hole of `griego-family-larger-mT`, given its own slug + file so a builder
can own it in parallel without colliding with L2's verified file. It does NOT disturb L2's held
1.176 — it tries to RAISE it (toward ~1.1764 at m=130, ~1.177 at m=150, ~1.1779 at m=200, per the
fit; verify by exact DP before trusting).

## Holes (file: certificate/griego-ntt-push.py)
1. **`fast_sumset_count` — OPEN (NotImplementedError).** Exact |U+U| via NTT (prime modulus) or
   exact-integer FFT on the reachable-Σx bitmask, repeated squaring in m. MUST be exact — float FFT
   only if rounding error is rigorously bounded < 0.5 (an integer count corrupted by 1 fabricates
   the bound). This is the load-bearing engineering hole.
2. **`validate_fast_dp` — OPEN.** Validate the fast count EXACTLY against the R3 clamped-DP oracle
   (imported from L2) on 12+ cases incl. clamp-exercising / non-contiguous ones, BEFORE any large-m
   number is trusted. Rule (R3): a fast-but-wrong DP fabricates a bound. This gate is mandatory.
3. **`scan_large_m` — OPEN.** Scan m=120..200 along T≈1.9m, PRINTING EACH POINT INCREMENTALLY
   (Rule R2: no single silent Bash > ~5 min — checkpoint per point, run in background with an
   until-loop watcher). Find the highest-θ point.
4. **`certify_best` — OPEN.** At the best (m,T) emit the largest k/10000 with
   d^10000 > s^10000·(2M+1)^(k-10000) — same certificate FORM as the held 1.176, at a higher θ.
   That k/10000 is the new held candidate (> 1.176).

## State
- New this round (R4). Imports the certified `exact-sumdiff-dp` oracle (L2) as validation ground
  truth; reuses count_diffset / max_U directly (they already scale).
- Borrows: `griego-family-larger-mT` (the oracle, the family, the certificate form),
  `exact-sumdiff-dp` lemma.
- Risk: diminishing returns — doubling m from 110 buys only ≈ +0.002 θ (1/√m tail), so the
  realistic ceiling of this lever is ~1.18, not 1.25. Still a strictly-higher held than 1.176 if
  any m∈[130,200] point clears it (the fit says yes; exact DP must confirm).
- Validation gate (hole 2) is the make-or-break correctness step; the speedup is worthless if it
  miscounts.
