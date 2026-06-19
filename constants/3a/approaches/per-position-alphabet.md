# per-position-alphabet — inhomogeneous digit alphabets (untried, larger space)

**Direction:** lower bound on C_3a. **Record to beat:** 1.1740744 [G2026].
**Borrows:** the exact-DP engine from `alphabet-search-dp` (`ghr_dp.py`).

## Strategy
Every construction in the lineage (GHR, Gerbicz, Zheng, Griego) uses the **same alphabet at
every digit position**. Letting the alphabet vary by position `i` (e.g. denser low digits,
sparser high digits where `max(U)` — the denominator `log q` — is most sensitive) strictly
enlarges the carry-free family while preserving injectivity (base set by the global max digit).
Explorer lever #4: "Untried." The DP extends trivially — each step uses its own feature list.

To stay searchable, parameterize by a few **blocks** of positions, each with its own alphabet.

## Holes
- **H1 ENGINE:** position-dependent sumset/diffset/max DP taking `[A_0,…,A_{d-1}]`. Same
  `(sa,sap)` / `(la,ra)` state machinery; only per-step feature lists differ. Validate: all
  `A_i` equal → identical to `ghr_dp`; plus a small brute-force.
- **H2 SEARCH (hard):** find a blocked schedule `{A_i}, T` beating the record on float-θ. The
  space is much larger than homogeneous — need a principled schedule (taper max digit with
  position), not blind search.
- **H3 CONFIRM + CERTIFY:** exact counts + directed-rounded rational log bound (reuse
  `alphabet-search-dp` H2/H3).

## Hard step
The search (H2): the inhomogeneous space is large; a good schedule must be reasoned from where
the ratio is sensitive (high positions dominate `log q`, low positions add cheap sums/diffs),
not enumerated.

## Certify
Python integer DP + rational log bound. Lean-fittable on the winning counts.
