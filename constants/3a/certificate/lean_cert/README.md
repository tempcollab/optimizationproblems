# C_3a Lean certificate — `lake build`-checked lower bound `C_3a ≥ 5877/5000`

Round 19. Converts the R18 verified *numerical* beat (`C_3a ≥ 5877/5000 = 1.1754`, beating
the record `1.1740744476935212`) into a machine-checked Lean theorem. This does NOT change
the held bound number — it upgrades the existing verified beat to the gold-standard
`lake build`-checked form (CLAUDE.md "Prefer Lean-certifiable").

## Lean file

`lean/Constants/C3a.lean` (namespace `C3a`). Wired into `lake build` via the existing
`[[lean_lib]] name = "Constants"` glob `Constants.+` in `lean/lakefile.toml` — no lakefile
change needed.

## Build target + how to re-check

From `lean/` (Mathlib pinned at `v4.31.0`, `lean-toolchain` = `leanprover/lean4:v4.31.0`):

```
export PATH=$HOME/.elan/bin:$PATH
lake build Constants.C3a          # the module alone (~4s after Mathlib is cached)
lake build                        # whole tree: 8574 jobs, PASS
```

## `#print axioms` (re-run on a tiny importing file)

```
#print axioms C3a.newGE
#print axioms C3a.recLT
#print axioms C3a.c3a_ge_5877_5000
#print axioms C3a.c3a_ge_5877_5000'
```

Output (verified R19):

```
'C3a.newGE'              depends on axioms: [propext]
'C3a.recLT'              depends on axioms: [propext]
'C3a.c3a_ge_5877_5000'   depends on axioms: [propext, Classical.choice, Quot.sound]
'C3a.c3a_ge_5877_5000''  depends on axioms: [propext, Classical.choice, Quot.sound]
```

- The two load-bearing power inequalities (`newGE`, `recLT`) are **axiom-free** apart from
  `propext` (no `sorryAx`, no `Classical.choice`, no `Quot.sound`, no `native_decide` /
  `ofReduceBool`). Pure kernel `decide` over GMP `Nat` at ~2-million-bit scale.
- The assembled bound theorems carry only the standard Mathlib trio
  `[propext, Classical.choice, Quot.sound]` (from the `ℝ` machinery) — **no `sorryAx`, no
  new axiom, no `native_decide`**.
- The GHR analytic bridge `GHR_lower` is an explicit **hypothesis** on the bound theorems
  (visible in the signature), NOT a Lean `axiom`, so it does not appear in `#print axioms`.
  This is the honest trust boundary, structurally identical to 9a's `ThetaGeFromIndep` and
  5b's `MTThm15`.

## What is proved IN Lean vs the trust boundary

PROVED inside Lean (axiom-free `decide`):
- `newGE : Nplus ^ Q * (2*maxU+1) ^ P ≤ Nminus ^ Q` — the beat cell (d=100, T=187) passes
  the wedge `θ(U) ≥ 1 + P/Q = 5877/5000` (log-free integer-power form).
- `recLT : recNminus ^ Q < recNplus ^ Q * (2*recMaxU+1) ^ P` — the d=80 RECORD cell FAILS
  the same wedge (`value_record < c`), certifying the improvement is STRICT.
- The pure-ℝ assembly `c3a_ge_5877_5000` / `c3a_ge_5877_5000'` (feeding `newGE` through the
  bridge and simplifying `1 + 877/5000 = 5877/5000`).

NAMED TRUSTED BRIDGE (the only non-`decide` content):
- `GHR_lower (c3a : ℝ) : Prop := ∀ (s d m p q : ℕ), 0 < s → 0 < q → s ≤ d →
   s^q * (2*m+1)^p ≤ d^q → c3a ≥ 1 + (p:ℝ)/q` — packages ONLY the GHR2007 analytic
  existence step ("`θ(U) ≥ c` ⟹ `C_3a ≥ c`", the construction of arbitrarily large
  extremal `A,B`), which Mathlib cannot state (no `C_3a` object). It supplies NO arithmetic;
  the integer inequality is handed to it already `decide`-proven.

## Route (A): log-free integer powers (per the R19 outline-reviewer ruling)

The bound is stated as the big-int power inequality; NO `Real.log` / `Real.rpow` enters the
certified path. The equivalence
`θ(U) ≥ 1+P/Q  ⟺  d^Q ≥ s^Q·(2m+1)^P` (`d ≥ s`, `q > 1`, all logs monotone) is established
once on paper in `constants/3a/literature/GHR2007-lemma-digest.md`; only its conclusion is
carried into Lean (via `GHR_lower`).

## Integer provenance (trusted as literals, NOT recomputed in the kernel)

The three big integers per cell are copied verbatim from the already-reviewer-verified
numerical certificate:
- Beat cell (d=100, T=187): `constants/3a/certificate/beat_largerd/beat_d100.json` PRIMARY
  (`Nplus`, `Nminus`, `maxU`).
- Record cell (d=80, T=150): `constants/3a/certificate/engine/record_{plus,minus,max}.txt`.

Their provenance is re-derivable OUT of Lean by `constants/3a/certificate/beat_largerd/verify_beat.py`
and the carry-free digit-DP `constants/3a/certificate/engine/digit_dp.py::count_opset`
(R18-reviewer-verified bit-for-bit). A Lean-kernel digit-DP recompute is deliberately NOT
done (unprobed kernel-OOM hazard; not this round's increment). This is the 9a precedent
(R13 trusted the 367 codewords as literals, verified provenance out of Lean).

## `set_option`s required

- `set_option exponentiation.threshold 6000` — default 256 leaves `^` symbolic so `decide`
  silently fails; raise above the q=5000 exponent.
- `set_option maxRecDepth 10000` — for the kernel fold over the big literals.
- `decide`, NOT `norm_num`, for the power inequalities (`norm_num` expands one side to a
  ~600k-digit numeral and stalls).
