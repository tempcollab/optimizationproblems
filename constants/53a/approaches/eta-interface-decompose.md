# eta-interface-decompose

## Idea

Expose the eta-invariant additive term as a **syntactic free parameter** of the recursion step,
so a future sub-`3p^2` generic `eta(C_p^3)` result plugs straight in and the whole downstream
scaffold re-derives a strictly-better bound mechanically.

The existing `recursion_step` hard-wires the local-estimate additive term `+ p^2` (from
Grinsztajn Lemma 2.3 `D_k(C_p^3) ≤ p*k + p^2`, itself the eta bound `eta(C_p^3) ≤ 3*p^2`,
Bhowmik–Schlage-Puchta 2017 — the current `c = 3` wall). But the entire `C_53 ≤ 4` derivation
only ever uses `+ p^2` through the single comparison inequality `p^2 - 2p + 2 ≤ (p-1)Q`
(`comparison_ineq`). Replacing the literal `p^2` by a free `c : ℤ` constrained only by
`heta : c ≤ p^2` *relaxes* the left side of the chain, so the same `comparison_ineq` still
closes it — no new number theory.

## Status — BUILT (this round, R6), conditional infrastructure. `held` stays 4.

Added to `lean/Constants/C53a.lean` (appended after `recursion_step`, lines ~104–171):

- **`recursion_step_c`** — the eta-coefficient-parameterised recursion step. Same statement as
  `recursion_step` but the additive term is a free integer `c` with `heta : c ≤ p^2` and the
  step hypothesis `hstepc : D(p*m) ≤ p*D(m) + c`. The chain closes with
  `nlinarith [hcmp, heta]`, where `hcmp := comparison_ineq p Q hp hpQ` is reused **verbatim**
  (it is stated for a generic integer `p`, no primality assumption).
- **`recursion_step_of_c`** — recovers the original hard-wired-`p^2` `recursion_step` as the
  `c := p^2` instance of `recursion_step_c`, with `heta : p^2 ≤ p^2` discharged by `le_refl`.
  Witnesses that `recursion_step_c` is a strict generalisation: the existing scaffold sits
  inside it as the trivial `c = p^2` case, nothing downstream is lost.

### Build / certificate

- `lake build Constants` — GREEN, genuine recompile (deleted `Constants.C53a.olean` first;
  "Built Constants.C53a (8.0s)", 2968 jobs).
- `#print axioms recursion_step_c` → `[propext, Classical.choice, Quot.sound]` — no `sorryAx`,
  no smuggled axiom.
- `#print axioms recursion_step_of_c` → `[propext, Classical.choice, Quot.sound]` — clean.
- All 12 pre-existing theorems still build with clean axioms (no upstream regression). No
  `sorry`/`admit` tactic anywhere in the file.
- Certificate record: `constants/53a/certificate/` (build target `lake build Constants`,
  axiom audit `#print axioms` block at the foot of `C53a.lean`).

### Honest scope — NO sub-4 claim

This does **not** beat 4. It is conditional on `heta : c ≤ p^2` exactly as the scaffold is
conditional on `+ p^2` today: with `c = p^2` it *is* the present bound. The value is purely the
forward-leverage interface — it turns the eta dependence into a syntactic hypothesis. `held`
stays 4 (record-break is barriered on the open sub-`3p^2` eta-coefficient problem, BSP-2017
wall, re-confirmed five rounds).

## How to push it further

The interface is now in place; the leverage is realised only by a genuine eta input. Concretely:

1. **(small infra)** Thread `recursion_step_c` through `global_induction`: generalise the
   `hstep` hypothesis to `hstepc : ∀ p m, D(p*m) ≤ p*D(m) + c p` with `heta : ∀ p, c p ≤ p^2`
   for a per-prime coefficient function `c : ℕ → ℤ`, and replace the `recursion_step` call in
   the cons branch by `recursion_step_c` with `heta p`. This propagates the syntactic knob all
   the way up to the iSup capstone, so the entire pipeline becomes parameterised in `c`.
   (One-round Lean-fit; still conditional, still `held = 4`.)

2. **(record lever, HARD / open)** Supply a generic input lemma `c p ≤ (3 - δ)*p^2` (the eta
   improvement) and re-run the parameterised pipeline. A `δ > 0` valid for ALL large primes `p`
   would, after recomputing the comparison constant, push the conditional bound strictly below
   4 — the only path that moves `held`. This is the open frontier (`eta-coefficient-barrier`),
   Lean-hostile, multi-round. The interface here is what makes that plug-in mechanical once the
   eta result exists.

## Sources

- M. Grinsztajn, *An upper bound for the Davenport constant of `C_n^3`* (2026),
  https://github.com/maaxgrin/davenport-cn3-bound — Lemma 2.1 (inductive method), Lemma 2.3
  (local estimate `D_k(C_p^3) ≤ p*k + p^2`).
- Bhowmik, Schlage-Puchta, *Davenport constant of `Z_p^3`* (2017) — `eta(C_p^3) ≤ 3p^2 - 4p - 3`
  (the `c = 3` wall the `heta` parameter abstracts).
- Reused verbatim: `comparison_ineq` (this file), `mul_le_mul_of_nonneg_left`, `nlinarith`.
