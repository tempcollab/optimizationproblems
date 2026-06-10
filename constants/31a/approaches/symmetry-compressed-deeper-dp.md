# Approach: Symmetry-compressed deeper DP (the genuine record-break shot)

Spec review: required
Status: proposed (round 1)
Moves: LOWER bound. Aiming strictly past **0.792665992** [H2024], target ~0.793–0.795.

## Idea

Same Lueker–Heineman recurrence and feasibility certificate as
`exact-dp-certificate.md` (read that for the inequality-direction argument and
Lemma 2.1). The record-break requires a window depth deeper than what naive
storage allows in this container. H2024 hit the wall at ℓ=20 (≈4.4 TB). We do
NOT need ℓ=20 — we need any ℓ whose certified rate `2(r-eps)` exceeds 0.792665992.
The published progression (ℓ→bound) suggests the record sits around ℓ=18–20; so
the target is to certify at ℓ≈17–18 *in RAM* via aggressive state compression,
or to show a single extra effective depth beyond what fits naively.

## State-compression levers (each multiplies feasible depth)

1. **Complementation symmetry** `(s,t) ~ (~s,~t)`: factor 2 (H2024 note this).
2. **Pair-swap symmetry** `(s,t) ~ (t,s)`: factor ~2 (diagonal fixed points aside).
3. **Reversal / frontier-equivalence**: many suffix-window pairs induce identical
   DP-frontier transition behavior; collapsing transition-equivalent classes can
   give a further constant factor. Determine the equivalence by orbit/refinement.
4. **Low-precision storage + interval certification**: store iterates in fp32 or
   fixed-point to fit depth, then certify the *final* feasible triplet in interval
   arithmetic — the certificate check is one pass, so its precision is decoupled
   from the iteration precision.

Memory table (this container): ℓ=16 ≈ 34 GB fp64 (17 GB w/ 2× sym, ~9 GB w/ 4×
sym, ~4 GB at fp32 + 4× sym); ℓ=17 ≈ 137 GB fp64 → ~17 GB at fp32+4×sym; ℓ=18 ≈
550 GB → ~34 GB at fp32+4×sym. So fp32 + 4× symmetry brings ℓ=17 into a large-RAM
regime and ℓ=18 near the edge.

## Skeleton

1. Build the recurrence with a canonical-orbit indexing (symmetries 1+2, ideally
   3) — by tool: orbit enumeration + transition table on canonical reps.
2. Value-iterate at the largest ℓ that fits (target ℓ=17–18) in fp32/fixed point
   — by tool: numpy, in-place updates, blocked memory access.
3. Read off `(u, r)`; certify `(u, r, eps)` in **interval/exact arithmetic** in a
   single pass — by tool: `fractions` or interval lib on the canonical reps,
   expanding orbits only logically.
4. Report exact `gamma_2 >= 2(r-eps)`; require it `> 0.792665992`.

## Hard step

**Whether symmetry + low-precision storage actually reaches an ℓ whose certified
rate beats 0.792665992 within this container's RAM and one-round runtime.**
Mechanism: the certified rate is monotone in ℓ; the question is purely whether
the compression factor (≤ ~8×: 2×compl · 2×swap · ≤2×frontier) times the fp64→
fp32 factor (2×) — total ~16× — is enough to fit a *record-beating* depth. 16×
buys roughly 2 extra ℓ over naive fp64-in-RAM (ℓ=14 fits naively → ℓ=16 with
compression). If the record truly requires ℓ≈19–20, this still falls short and
degrades to the verified-reproduction milestone. The orbit-3 "frontier
equivalence" collapse is the uncertain lever that could buy more; its size is
unknown until enumerated.

## Check

Same as `exact-dp-certificate.md`: a one-pass componentwise feasibility re-check
of `(u,r,eps)` on canonical orbit representatives, printing exact `2(r-eps)`.
Reviewer re-runs; the value must strictly exceed 0.792665992.
