# Certificate — ghr-lemma-lean (Lean machine-checked, constant 3a)

Gold-standard Lean certificate of the d=84, T=162 GHR single-set construction's
sum-difference exponent inequality.

## Build target

```
cd constants/3a/lean
lake build Sketches.Ghr        # the proof module (hyphen-free name)
lake build                     # full default target (also builds Sketches.«ghr-lemma-lean»)
```

Lean toolchain: `leanprover/lean4:v4.31.0` (pinned in `lean/lean-toolchain`).
Mathlib pinned: rev `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` (tag `v4.31.0`) in
`lean/lake-manifest.json`.

## Axiom check (the load-bearing rigor check)

```
import Sketches.Ghr      -- or:  import Sketches.«ghr-lemma-lean»
open C3a
#print axioms beats_record
```

Output:

```
'C3a.beats_record' depends on axioms: [propext, Classical.choice, Quot.sound]
'C3a.power_ineq'   depends on axioms: [propext]
```

NO `sorryAx`, NO smuggled custom axiom. The three printed axioms are the standard
Mathlib foundation (propositional extensionality, choice, quotient soundness); they
do not smuggle the hard step.

## What the theorem certifies

`C3a.beats_record`:

```
1 + Real.log (dUmU / sUpU) / Real.log qMaxU  >  1.1740744
```

with the exact `Nat` literals (from the validated Python exact DP,
alphabet-search-dp `WINNERS[(84,162)]`):
- `sUpU  = |U+U| = 6097708534951589347439183607038270910158216193597072358058994024712092458076766270`
- `dUmU  = |U-U| = 145710369635805984294872090934229656671521875518799257570738793680742528284363557961708618559623567675`
- `qMaxU = 2*max(U)+1 = 1165254416489684872554618217361872378435684345652187969599710464819025051454571621932090673372945921527696090485`

Method (no logs in the kernel-load-bearing step): the inequality is reduced to the
pure integer comparison

```
sUpU^86 * qMaxU^15  ≤  dUmU^86       (C3a.power_ineq, ~8700-digit Nats, by `decide`)
```

which is equivalent to `(diff/s)^86 ≥ q^15`, i.e. `log(diff/s)/log q ≥ 15/86`, and
`15/86 = 0.1744186... > 0.1740744`. `15/86` is the smallest-denominator rational strictly
between the threshold 0.1740744 and the true ratio 0.17447509. The analytic bridge
(monotonicity of `Real.log`, `Real.log_pow`, `Real.log_mul`, `Real.log_div`,
`Real.log_pos`) is fully formal.

## Scope / what is NOT formalized in Lean (honest)

The Lean theorem certifies the *arithmetic exponent inequality*
`1 + log(diff/s)/log q > 1.1740744`. The link from this quantity to `C_3a ≥ (that quantity)`
is the GHR2007 single-set lemma (carry-free base-21 injectivity ⇒
`C_3a ≥ 1 + log(|U-U|/|U+U|)/log(2 max U + 1)`), which is taken from the literature and is
NOT itself proved inside this Lean file (former hole H1). The `Nat` literals for the counts
are taken as given from the trusted Python DP (former hole H2, cheap path).
