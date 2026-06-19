# Lean certificate — continuum (interval-ln) endpoint of C_3a

Machine-checked proof that the GHR2007 endpoint formula, evaluated at the
reviewer-verified `d = 110, T = 210` integer counts, exceeds the table record.

## What is formalised

The Lean project `constants/3a/lean/` proves (file `C3a.lean`):

```
theorem C3a.theta_endpoint_ge :
    (1 : ℝ) + Real.log ((D : ℝ) / (S : ℝ)) / Real.log (q : ℝ) ≥ 1 + 7 / 40

theorem C3a.theta_endpoint_beats_record :
    (1 : ℝ) + Real.log ((D : ℝ) / (S : ℝ)) / Real.log (q : ℝ) > 1.1740744
```

i.e. `θ(U) = 1 + ln(D/S)/ln(q) ≥ 1.175 > 1.1740744` (the published record [G2026]),
where `S = |U+U|`, `D = |U−U|`, `q = 2·max(U)+1` are the EXACT integer literals from
the reviewer-verified `certify_3a.py 110 210` run (base 21, A = {0,2,…,10}, drop-1).

The literals in `C3a.lean` match the verified certificate exactly:
- `S` (107 digits) = `|U+U|`
- `D` (133 digits) = `|U−U|`
- `q` (146 digits) = `2·max(U)+1`

### Scope (what is and is NOT in Lean)

- **In Lean (this file):** the continuum endpoint inequality, reduced to the purely
  algebraic integer fact `S^40 · q^7 ≤ D^40` (decided by `norm_num`) lifted through
  the strict monotonicity of `Real.log` and positivity of `log q` (`q > 1`). No
  `exp`/`log` numeric Taylor bounds are needed — the reduction
  `7/40 ≤ log(D/S)/log q  ⟺  q^7 ≤ (D/S)^40  ⟺  S^40·q^7 ≤ D^40` is exact.
- **Still numerical (out of Lean):** the dynamic-programming COUNTING of `S`, `D`,
  `max(U)` — that remains the `certify_3a.py` certificate. Only the final endpoint
  inequality is formalised here.

### Relation to `held`

This Lean bound is `1.175`, which is **below** the reviewer-verified `held` value
`1.1760055927978140` (also a `d=110` value). It does NOT raise `held`. The clean
rational exponent `7/40` is chosen for an exact integer-power reduction with large
slack (`D^40 / (S^40·q^7) ≈ 7.08·10^5`); it banks a machine-checked proof of the
easy (continuum) half of the certificate as the gold-standard hardening track.

## Build target

```
cd constants/3a/lean
lake exe cache get      # fetch pinned Mathlib oleans (first time only)
lake build C3a          # type-checks the proof; "Build completed successfully"
```

Pins (committed; do not float):
- `lean-toolchain`     : `leanprover/lean4:v4.31.0`
- `lake-manifest.json` : mathlib `rev = fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` (inputRev `v4.31.0`)

## `#print axioms` (the certificate of no hidden gap)

Run inside the project (`lake env lean` on a file that `import C3a` then
`#print axioms ...`):

```
'C3a.theta_endpoint_ge'            depends on axioms: [propext, Classical.choice, Quot.sound]
'C3a.theta_endpoint_beats_record' depends on axioms: [propext, Classical.choice, Quot.sound]
'C3a.ratio_ge_of_pow'             depends on axioms: [propext, Classical.choice, Quot.sound]
'C3a.pow_ineq'                    depends on axioms: [propext, Classical.choice, Quot.sound]
```

Only the three standard Mathlib axioms — NO `sorryAx`, NO added axiom, NO unproved
hypothesis. Type-checking IS the reproduction.
