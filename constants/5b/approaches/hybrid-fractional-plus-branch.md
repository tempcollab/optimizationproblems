# hybrid-fractional-plus-branch — C_5b (Erdős #757, UPPER bound)

**Goal:** improve the upper bound `c* ≤ 4/7 ≈ 0.5714286` (verified [MT26]). A beat = one
indecomposable (4,5)-set `A` with `h(A)/|A| < 4/7`.

**Status (R4): MACHINERY built + Lean-verified (clean axioms). Does NOT beat `4/7`.**
The `max`-composition first version is done; the genuinely-scaling interleaved version is
the next step.

## Idea

The minimum AP-transversal `τ` of the 3-AP hypergraph `H(A)` controls the bound via
`h(A) ≤ N − τ`. Two independent, already-verified lower bounds on `τ` exist:

- `C5bTransversal.hLe_of_fracMatching` — fractional / LP-duality, cheap `O(|F|·N)`, but with
  an integrality gap (`τ ≥ ⌈ν*⌉`; on `A_base` `ν*=4.5 → ⌈·⌉=5`, i.e. only `h ≤ 9`);
- `C5bBranch.hLe_of_branchCert` — branch-and-bound, exact (reaches integral `τ`), cost
  `O(3^budget)` (on `A_base` `τ = 6 → h ≤ 8`).

The hybrid combines them by **`τ ≥ max(τ_frac, τ_branch)`** — equivalently the bound on the
Sidon subset is `|S| ≤ min(m_frac, N − k_branch − 1)`. A single call certifies
`h(A) ≤ N − max(τ_frac, τ_branch)`, picking up whichever certificate is tighter.

## Exactly what is proven (R4)

`C5bHybrid.hLe_of_hybrid` (in `lean/Constants/C5bHybrid.lean`): given a fractional certificate
(params `D, m_frac, FW_frac` with `D·(N−m_frac−1) < totalW`) AND a branching certificate
(`noTransLe FW_branch k_branch = true`), every `Nodup S ⊆ A` avoiding BOTH listed families has
`S.length ≤ min m_frac (N − k_branch − 1)`. Proof: `le_min` over the two soundness lemmas —
a one-liner, trivially valid.

`C5bHybrid.Validation.Abase_avoiders_le_8_hybrid`: on `A_base`, feeding the fractional cert
(`τ ≥ 5`, `h ≤ 9`) and the branching cert (`τ ≥ 6`, `h ≤ 8`), the hybrid resolves
`min 9 8 = 8` — the `max` correctly prefers the branch `τ = 6`. Tight `h(A_base) ≤ 8` via the
combined route.

- `lake build Constants.C5bHybrid` PASS; full `lake build` PASS (8565 jobs).
- Zero `sorry`; **plain `decide`** where decidable facts are checked (no `native_decide`).
- `#print axioms hLe_of_hybrid` and `…Abase_avoiders_le_8_hybrid` →
  `[propext, Classical.choice, Quot.sound]` (no `sorryAx`, no `Lean.ofReduceBool`).
- Independent numerical re-check: `constants/5b/certificate/hybrid/check_hybrid_cert.py`
  (PASS) recomputes the 12 APs, `ν*=4.5→h≤9`, exact `τ=6→h≤8`, `max(5,6)=6→h≤8`.

## Exactly what is NOT proven (the deferred interleaving — DO NOT overclaim)

The `max` composition is a **sound, simple first version**. It does **NOT** make the branch
budget small at large `N`:

- It does **not** knock the fractional residual down before branching. The branching
  certificate still has to certify the **full** `τ` on its own — its budget is unchanged
  (on `A_base` the certified budget is the full `k = τ − 1 = 5`, not a small residual).
- Therefore the N≈30 **scaling** property — the thing this slug is named for — is **not yet
  achieved**. At `N = 30` the standalone branch budget is ≈ 12–13, so `3^13 ≈ 1.6M` worst-case
  leaves still threaten plain `decide`. The `max` composition does not reduce that.

In short: `h(A) ≤ N − max(τ_frac, τ_branch)` is proven and is genuinely useful (one call,
tighter of the two), but it is **not** the budget-shrinking interleaved certificate.

## How to push further (toward the actual N≈30-scaling cert)

1. **The genuinely-interleaved lemma (the real scaling step).** Build
   `hLe_of_branchOnResidual`: given a fractional dual certificate of value `a` (with explicit
   dual support / a list of edges it "pays for") AND a branching certificate
   `noTransLe FW_residual (g) = true` over the **contracted residual** family `FW_residual`
   (the APs not yet covered by the fractional support, with the paid vertices identified),
   conclude `τ ≥ a + g` — and crucially the branch budget is `g = τ − a` (1–2 units), so
   `3^g` stays tiny at `N = 30`. The hard step is the **soundness of contraction**: prove that
   any transversal `H` of the full family `FW` splits as (vertices charged to the fractional
   support, contributing `≥ a` by LP duality on the support) + (vertices hitting the residual,
   contributing `≥ g` by the residual branching cert), with no double counting. This needs the
   fractional lemma to expose its dual support (currently `hLe_of_fracMatching` only exposes
   the *value* via `totalW`/`loadOK`); refactor it to also yield a *partition* of `H` by which
   vertices carry the LP charge. This is the genuinely new content and likely a full round.

2. **An N≈30 gadget to certify.** The interleaved lemma needs a real indecomposable N≈30
   (4,5)-set with `h = ⌈9N/17⌉+1` (e.g. `N=30, h=17, 17/30≈0.5667`). Block assembly is proven
   useless (Lemma 3.6 → mediant). Frame via the modular / GL95-Fibonacci layout. The gadget
   search is the `cpsat-exact-existence-N28-N30` slug; once it produces a candidate, certify
   its (4,5)-property via `is45setB` (in `C5b.lean`) and its `h ≤ N−τ` via the interleaved
   cert. Then `held` can move below `4/7` for the first time.

3. **Validate the interleaved version on `A_base`** as the budget-1 milestone: fractional
   `a = 5` (residual gap 1), so the residual branch budget is `g = 1` (`3^1 = 3` leaves)
   reaching `τ = 6` — same tight `h ≤ 8` but with the *small* budget that scales, proving the
   interleaving mechanism end-to-end before deploying it at `N = 30`.

## Importable interface

```
import Constants.C5bHybrid
open C5bHybrid
-- hLe_of_hybrid : Nodup A → edgesOK A FW_frac → loadOK A FW_frac D →
--                 D*(|A|-m_frac-1) < totalW FW_frac →
--                 edgesOK A FW_branch → noTransLe FW_branch k_branch = true →
--                 Nodup S → S ⊆ A → avoidsAll S FW_frac → avoidsAll S FW_branch →
--                 S.length ≤ min m_frac (|A| - k_branch - 1)
```
Depends on `C5bTransversal` (`hLe_of_fracMatching`) and `C5bBranch` (`hLe_of_branchCert`,
`noTransLe`).

## Sources

- [MT26] Ma & Tang, arXiv:2602.23282 (Lemma 2.3: in a weak Sidon set, Sidon ⟺ no 3-term AP;
  Thm 1.5: `c* = inf f(n)/n`; Lemma 3.6: well-separated union ⇒ additive `h`).
- LP duality for hitting sets / fractional matching (standard); branch-and-bound hitting-set
  lower bound (standard). Both formalized in this repo's `C5bTransversal` / `C5bBranch`.
