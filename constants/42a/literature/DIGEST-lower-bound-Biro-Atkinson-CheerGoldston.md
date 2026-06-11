# Lower-bound side of C_42 (Atkinson, Biró 1/2 and >1/2, Cheer-Goldston numerics)

## Chain of verified lower bounds
- Atkinson [Atk61]: liminf-type 1/6; [Atk69]: 1/3 (unpublished tech report), then π/8.
- **Biró [Bir94]** ("On a problem of Turán concerning sums of powers of complex numbers",
  Acta Math. Hungar. 65 (1994) 209-216): **C_42 >= 1/2** — the VERIFIED record lower bound
  (README & 42a.md both say 0.5). i.e. for n>=2, 1/2 < R_n < 1.
- **Biró [Bir00b]** ("An improved estimate in a power sum problem of Turán", Indag. Math.
  11(3) (2000) 343-358): proves limsup R_n > 1/2 strictly, with "some computable constant
  1/2 < c < 1/√2 ≈ 0.7071", but **does not compute c explicitly**. THIS is the named
  opening in 42a.md.

## IMPORTANT caveat I could NOT fully resolve (papers paywalled / not on arXiv)
The Biró papers are in Acta Math. Hungar. and Indag. Math.; NOT on arXiv, and ScienceDirect
returns 403. I could only read abstracts/secondary summaries. A secondary source
(web summary of the Indag. paper) suggests [Bir00b] may actually concern the UPPER-side
refinement R_n < 1 - (1-ε)·loglog n/log n, and that the extremal/variational problem
giving c "occurred naturally" in the EARLIER 1994 proof of R_n>1/2. The exact attribution
of "the constant c with 1/2<c<1/√2" to [Bir94] vs [Bir00b] needs the actual paper PDFs.
**The proof-builder MUST obtain Biró [Bir94] and [Bir00b] (library / interlibrary) before
relying on the structure of the variational problem.** This is the single biggest unknown.

## What is known about the method (from secondary sources)
- Lower bounds in this area use **Fejér-kernel / positive-definite trigonometric** machinery:
  to bound max_k |sum z_i^k| from below, one tests against a nonnegative kernel
  (Fejér-type) and uses positivity to force at least one power sum to be large. Biró's
  >1/2 proof reduces to an EXTREMAL PROBLEM over kernel coefficients whose optimal value
  is the constant c. Making c explicit = solving (or rigorously lower-bounding) that
  extremal problem.
- **Cheer-Goldston [CG96]** (Math. Comp. 65 (1996) 1349-1358, paywalled): purely
  COMPUTATIONAL. Computed R_n for n<=55, found the minimizing configurations, observed
  R_n decreasing toward a limit they estimate ≈ 0.7 (i.e. close to but below 0.7). This is
  a CONJECTURE, not a bound. It tells us: (a) the true value is near 0.7, so the lower
  bound 0.5 is loose by ~0.2 (huge slack), and the upper 0.69 is nearly tight; (b) the
  extremal configurations have structure (roots near the unit circle in a specific
  pattern) that could seed a rigorous lower-bound argument.

## Where the slack is on the lower side (the soft target)
- Gap on the lower bound: true value ≈0.7 vs verified 0.5 → ~0.2 of slack, vs essentially
  zero remaining slack on the upper bound (Griego already at 0.69065, ~1.5e-7 from the bar).
- Two routes to raise the lower bound past 0.5:
  (A) **Make Biró's c explicit.** If [Bir00b]/[Bir94]'s argument yields R_n > c for an
      identifiable extremal problem, evaluate/lower-bound that extremal value rigorously
      (it lies in (0.5, 0.7071)). Any rigorous c>0.5 beats the record. REQUIRES the paper.
  (B) **Fejér-kernel test functions from scratch.** Pick an explicit nonnegative kernel
      sum_k a_k cos(kθ) with a_k>=0 (or a finite positive-definite sequence) and derive
      a clean inequality of the form: for any unimodular-max config, max_k|sum z_i^k| >=
      f(coeffs). Optimize the kernel coefficients (a small LP/SDP: maximize the guaranteed
      lower bound subject to nonnegativity). This is SELF-CONTAINED and reviewer-checkable
      (the optimized kernel + the inequality is the certificate), and does NOT require the
      paywalled papers. Even a modest improvement (e.g. 0.5 → 0.52) is a verified milestone.

## Why the lower bound is the right target this run
- The upper bound is essentially exhausted by the two-block ansatz (Harcos≈Griego≈0.69).
- The lower bound has 0.2 of slack and TWO independent attack routes, one of which
  (Fejér/SDP kernel optimization) is fully reproducible and needs no inaccessible paper.
- Caveat: any lower bound is capped at the true value ≈0.7, and pushing past ~0.6 likely
  reproduces hard parts of Biró's argument. A first-round goal of c>0.5 (e.g. 0.51-0.55)
  via an explicit kernel is the realistic verified milestone.
