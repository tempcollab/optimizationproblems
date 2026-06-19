# [GHR2007] Gyarmati–Hennecart–Ruzsa — the lemma + 4/3 upper bound

PDF: constants/3a/literature/pdfs/ghr2007_sumdiff.pdf (text extraction garbled by math symbols;
key statements read from the paper + corroborated by Gerbicz/Zheng intros).

## The lower-bound lemma (the engine for ALL lower bounds here)

Lemma (GHR §2). Let K>1 and let U be a finite non-empty set of non-negative integers containing 0.
Set s=|U+U|, d=|U−U|, q=2·max(U)+1, θ=1+log(d/s)/log q. If d<q, then there exist pairs (A,B) of
finite non-empty integer sets, arbitrarily large, with |A+B| ≤ K|A| and |A−B| ≥ c(K)·|A+B|^θ.

Mechanism: TENSOR / DIRECT-POWER. From U one builds A,B as projections of the k-fold structure
(k→∞), so a single finite U with a good ratio d/s and small max(U) certifies the exponent θ for
arbitrarily large A,B. This is why a finite digit construction (Griego, Gerbicz) yields a genuine
bound on the asymptotic constant — no separate A,B search needed.

## The 1.25 cap (for the V(m,L) simplex family ONLY)

Ledger remark: the family U = projection of V(m,L) (unbounded coordinates, base L_k≈(2L)^k) gives
bounds of the lemma's form but CANNOT EXCEED 1.25. This cap is specific to the unbounded simplex.
Gerbicz's bounded-coordinate W(m,L,B) family and Griego's gapped-digit construction are NOT this
family and already pass 1.25-irrelevance (they sit at ~1.17, well below 1.25, but the cap argument
doesn't apply to them — the real ceiling for them is Zheng's 1.173077 / unknown for gapped digits).

## 4/3 upper bound

θ ≤ 4/3 (GHR2007), the structural side. Stands since 2007, OUT OF SCOPE for this run unless a soft
road appears (none seen). The whole live frontier is the lower-bound construction side, gap 4/3 −
1.1740744 ≈ 0.159.

## Original construction

GHR's own construction (m=8, L=9 example, q(U)=11668193551) yields θ=1.144655 — the 1.14465 in the
ledger. Superseded by AlphaEvolve (1.1584), Gerbicz, Zheng, Griego.

## Asymmetric A≠B?

The constant is defined with A,B possibly DIFFERENT. But the lemma packages everything into a
single set U via the tensor argument, so all known records use one U (symmetric A−A vs A+A under
the hood). Whether genuinely asymmetric digit sets A≠B in the digit construction can beat the
single-U bound is an UNTESTED lever (see explorer report).
