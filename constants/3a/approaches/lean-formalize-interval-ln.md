# lean-formalize-interval-ln — Lean hardening of the continuum endpoint

**Type:** gold-standard hardening (Lean certificate). Does NOT raise `held`; banks a
machine-checked proof of the easy (continuum) half of the `C_3a` lower-bound certificate.

## Idea

The numerical certificate `certify_3a.py` produces three exact integers from the
verified `d=110, T=210` DP run: `S = |U+U|`, `D = |U−U|`, `q = 2·max(U)+1`, and then
forms the GHR2007 endpoint `θ(U) = 1 + ln(D/S)/ln(q)` via interval arithmetic. This
angle converts that final continuum step into a `lake build`-checkable Lean theorem,
taking `S, D, q` as literals (the DP counting stays numerical/out-of-Lean).

## Key trick (the load-bearing reduction)

Targeting the clean rational `θ ≥ 1 + 7/40 = 1.175` (chosen for an exact integer-power
reduction, with `7/40 = 0.175`) avoids ALL `exp`/`log` Taylor bounds:

```
7/40 ≤ log(D/S)/log q
  ⟺  7·log q ≤ 40·log(D/S)            (log q > 0 since q > 1)
  ⟺  log(q^7) ≤ log((D/S)^40)         (Real.log_pow)
  ⟺  q^7 ≤ (D/S)^40                   (Real.log strict monotone)
  ⟺  S^40 · q^7 ≤ D^40                (clear the positive denominator)
```

The last line is a PURE integer inequality on the literals, decided by `norm_num`
(operands ~7000 digits; ratio `D^40/(S^40·q^7) ≈ 7.08·10^5`, large slack). So the only
real-analysis content is `Real.log_le_log` (monotonicity) and `Real.log_pos` — no
numeric log enclosure at all.

## Status — R3: COMPILES, sorry-free, gold-standard

- Bootstrapped `elan` (→ ~/.elan) and a Lake project at `constants/3a/lean/`.
- **Pinned** (committed): `lean-toolchain = leanprover/lean4:v4.31.0`; Mathlib
  `rev = fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` (inputRev `v4.31.0`) in
  `lake-manifest.json`. `lake exe cache get` works (Mathlib oleans from Azure cache).
- `constants/3a/lean/C3a.lean` proves, with NO `sorry` / NO added axiom:
  - `C3a.ratio_ge_of_pow` — the reduction lemma (abstract `S,D,q`).
  - `C3a.pow_ineq` — `S^40 · q^7 ≤ D^40` on the verified literals (`norm_num`).
  - `C3a.theta_endpoint_ge` — `1 + log(D/S)/log q ≥ 1 + 7/40` (= 1.175).
  - `C3a.theta_endpoint_beats_record` — `… > 1.1740744` (the [G2026] table record).
- `lake build C3a` → "Build completed successfully (8559 jobs)" (~10 s incremental).
- `#print axioms` on all four theorems: `[propext, Classical.choice, Quot.sound]` only —
  NO `sorryAx`, NO smuggled hypothesis. (Recorded in
  `constants/3a/certificate/LEAN_CERTIFICATE.md`.)
- The `S, D, q` literals in `C3a.lean` match `certify_3a.py 110 210` exactly
  (re-derived and checked: S 107 digits, D 133, q 146; `q = 2·max(U)+1`).

## Claim (UNVERIFIED until the reviewer reproduces)

Machine-checked: `θ(U) = 1 + ln(|U−U|/|U+U|) / ln(2·max(U)+1) ≥ 1.175` for the verified
`d=110` instance, hence `C_3a ≥ 1.175 > 1.1740744` (record). This is a Lean re-derivation
of the continuum endpoint, NOT a new numerical bound: `1.175 < held = 1.1760055927978140`,
so it does not move `held`. The value here is deliberately the clean `7/40` (large-slack)
exponent, not the tightest endpoint.

## What would push it further

1. **Tighten the Lean value toward `held`.** Use a finer rational exponent
   `p/r ≈ 0.17600559` (e.g. `1000·log(D/S) ≥ 176·log q ⟺ S^1000·q^176 ≤ D^1000`). The
   reduction is identical; only `norm_num` on a larger integer inequality is needed.
   Check feasibility first in Python: pick `p/r` with `p/r ≤ true_ratio` and
   `1 + p/r > held`-target, confirm `S^r·q^p ≤ D^r`. (Note: matching `held` to all 16
   digits needs `r ~ 10^16`; pick the coarsest `p/r` that clears the target you want to
   formalise — there is a real ceiling at the true ratio `0.176005592797814003`.)
2. **Formalise the GHR2007 lemma itself** (`θ(U) ≤ C_3a`) in Lean — currently the
   bridge from the endpoint to `C_3a` is cited (literature), not formalised. This is the
   larger multi-round target that would make the whole bound machine-checked.
3. **Formalise (a slice of) the DP counting** so `S, D, max(U)` are themselves Lean-proved
   for a small `(d,T)` rather than transcribed literals — the genuinely hard, multi-round
   half. Start with brute-force enumeration agreement at `d ≤ 4` (the explorer/role-memory
   already validate the DP there numerically).

## Reproduce

```
cd constants/3a/lean
lake exe cache get
lake build C3a
# axioms:
echo 'import C3a
#print axioms C3a.theta_endpoint_ge' > /tmp/Ax.lean && lake env lean /tmp/Ax.lean
```
