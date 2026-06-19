# θ(d) scaling for the record family (drop-1, A={0,2..10}, base 21) — measured round 2

Engine: GHR lemma θ = 1 + ln(|U−U|/|U+U|)/ln(2max(U)+1). Counts via the validated exact
integer DP (`explore_harness.py`); independently brute-force-cross-checked at d≤4 (S,D,max all
match). Each (d, best-T) below is a single isolated run timed on this container.

| d   | best T | T/d   | θ (float)     | Δθ vs prev | runtime |
|-----|--------|-------|---------------|------------|---------|
| 80  | 152    | 1.900 | 1.174153642   | —          | ~46 s   |
| 90  | 172    | 1.911 | 1.174899247   | +0.000746  | ~39 s   |
| 100 | 192    | 1.920 | 1.175495347   | +0.000596  | ~62 s   |
| 110 | 210    | 1.909 | 1.176005593   | +0.000510  | ~93 s   |
| 120 | 228    | 1.900 | 1.176437439   | +0.000432  | ~132 s  |

(Record [G2026] is d=80, T=150 → 1.1740744. T=152 at d=80 already nudges to 1.174154 —
the record's own T is slightly sub-optimal.)

Key facts:
- **Monotone increasing, NOT converged.** Every +10 in d clears the record by a wider margin.
- **Δθ decays geometrically**, ratio ≈ 0.856 per +10 d. Geometric extrapolation:
  d=130 ≈ 1.17681, d=150 ≈ 1.17740, d→∞ family asymptote ≈ **1.1777–1.1780**.
  (d=120 measured at 1.176437 — matches the predicted 1.17644 to 5 decimals, validating the model.)
  So the drop-1/base-21 family's *limit* sits ~0.0037 above the record — a real but bounded
  ceiling; pure d-push cannot exceed it.
- **Optimal-T window scales ≈ 1.90–1.92·d** (T center ≈ 1.91·d; sweep ±2–3 to find the per-d
  optimum). The ratio drifts up very slightly with d.
- **Runtime grows ~quadratically** (state count ∝ T ∝ d, and the ty-range ∝ 2T): d=90 ~40 s,
  d=110 ~95 s. Extrapolating, d=130 ≈ 3–4 min, d=150 ≈ 6–10 min — all within one tool call.
  The naive Python bignum-bitset DP is the bottleneck; pruning/symmetry could push much further.

Decision: pure d-push is the dominant, near-certain near-term lever. d=100 (1.17550) or d=110
(1.17600) is a clean single-run win, +0.0014 / +0.0019 over the record — far above the round-1
d=90 (+0.0008). Co-tune T ≈ 1.91·d.
