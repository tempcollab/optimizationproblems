# Digest: Pesenti & Vladu, "Discrepancy Minimization via Regularization" (arXiv:2211.05509)

**Constant 10c (upper-bound side).** Least K with disc(A) ≤ K√n for all n, A∈[-1,1]^{n×n},
disc(A)=min_{x∈±1^n} ||Ax||_∞.

**What the paper ACTUALLY proves (caution — ledger overstates it).**
- Theorem 4.5: for every A∈[-1,1]^{n×n}, ∃ x∈{±1}^n with ||Ax||_∞ ≤ **4.1√n + O(1)**,
  via a poly-time randomized algorithm. The paper says it "improves Spencer's constant
  from 5.4 to 4.1" and only **"sketches how to obtain 3.7√n"** (§4.2 sketch, not a full
  rigorous theorem in the body).
- The README/ledger lists the verified upper bound as 3√(3/2) ≈ 3.674235 [PV2022] — this
  is the *sketched* 3.7 value, NOT the fully-proven 4.1. FLAG: the rigorously-proven
  constant in PV2022 is 4.1, with +O(1) (asymptotic, not "for all n"). The 3.674235 is at
  best a sketch and at worst not a clean finite-n bound. Reconcile before treating 3.674
  as the bar to beat.
- Method: ℓ_q-regularization of the max coordinate (potential Φ = ℓ_q reg.), partial
  coloring via a 2-dim subspace where the Hessian/operator norm is small (Lemma 4.2/4.6),
  Newton-step "walk on the edges" rounding. Constant comes from optimizing q∈(0,1) and a
  step parameter η. Belshaw [Bel13] earlier got 5.199; Schmidt's 3.65 is unpublished
  personal communication (the README "3.65*").

**Slack on upper side.** Improving the analytic constant means a tighter potential-function
analysis (better q, η, subspace-dimension argument) — a continuous-analysis proof, NOT a
reproducible numerical SDP certificate. Hard to make reviewer-checkable in one run, and the
"verified bar" itself (3.674 vs 4.1) is murky.

**LOWER-bound side (the tractable target).** C_10c ≥ disc(A)/√n for ANY single finite
matrix A∈[-1,1]^{n×n}. Current verified record (in-repo, G2026): a 6×6 ±1 matrix with
exact disc = 4 ⇒ 4/√6 ≈ **1.632993**. Bandeira's blog: best previously √2 ≈ 1.414
(2×2 [[1,1],[1,-1]]), "no known lower bound above 2" (i.e. above the ratio... above the
2×2); Spielman mentioned an unpublished numerical matrix slightly above √2. Finding a
sign matrix with disc(A)/√n > 1.632993 is an open, AlphaEvolve-style COMBINATORIAL SEARCH;
the certificate is one explicit ±1 matrix + a verified disc value (check via min over
sign vectors, or branch-and-bound / exact argument for small n).
