# interleaved-residual-cert — C_5b (Erdős #757, UPPER bound)

**Goal:** improve the upper bound `c* ≤ 4/7 ≈ 0.5714286` (verified [MT26]). A beat = one
indecomposable (4,5)-set `A` with `h(A)/|A| < 4/7`.

**Status (R5): MACHINERY built + Lean-verified (clean axioms, no sorry/native_decide). Does
NOT beat `4/7`.** The genuinely-interleaved (fix-then-branch) soundness lemma is built and the
budget-shrink mechanism is validated. A SHARP honest finding: the milestone "budget g=1 on
A_base" is mathematically NOT achievable — A_base is a worst-case half-integral instance.

## Idea

The minimum AP-transversal `τ` of the 3-AP hypergraph `H(A)` controls the bound via
`h(A) ≤ N − τ`. The R4 `hLe_of_hybrid` took the plain `min` of the fractional and branch
`|S|`-bounds — sound, but the branch still had to certify the **full** `τ` on its own (budget
unchanged → `3^13` intractable at `N ≈ 30`). The **interleaved** version splits the work:

- pick a support set `P` of vertices; a **fractional** certificate `FW_frac` (support ⊆ P)
  forces any transversal to use `≥ a` vertices from `P`;
- the **residual** family `FW_res` = listed APs that **avoid** `P` is branched with budget `g`;
- the two parts are vertex-disjoint, so they add with **no double counting**:
  `τ ≥ a + (g + 1)`, hence `h(A) ≤ N − a − g − 1`, branching only `g` (the residual gap),
  not the full `τ`.

This is the LP-fix-then-branch rule for 3-Hitting-Set (Nemhauser–Trotter half-integrality;
refs arXiv:2308.05974, 2506.24114, 1811.09429).

## Exactly what is proven (R5) — `lean/Constants/C5bInterleaved.lean`

`C5bInterleaved.hLe_of_interleaved` : given `A` Nodup, support `P`, a fractional cert
(`edgesOK A FW_frac`, `suppInP P FW_frac`, `loadOK A FW_frac D`, `0 < D`, `D·a ≤ totalW
FW_frac`) AND a residual cert (`edgesOK A FW_res`, `resAvoidsP P FW_res`, `noTransLe FW_res g
= true`), every `Nodup S ⊆ A` avoiding both families has `S.length ≤ N − a − g − 1`.

**The load-bearing new content (the disjoint residual attribution) is INSIDE the
formalization:** an arbitrary hitting set `H` is partitioned `(H ∩ P) ⊎ (H \ P)`; the
fractional load lemma forces `|H ∩ P| ≥ a` (off-`P` vertices carry zero listed charge —
`vertexLoad_zero_of_notInP`, `loadSum_filterP`, `frac_lb_on_P`), and `H \ P` hits the residual
(`res_hitsAll_filter`) so `noTransLe_sound` gives `|H \ P| ≥ g + 1`. Disjoint partition of the
`Nodup` list ⇒ `|H| ≥ a + (g + 1)`. Reuses `C5bTransversal.totalW_le_loadSum`,
`C5bBranch.noTransLe_sound`, `C5bBranch.hitsAll_removeVertex_erase`.

Validations (zero added axioms, plain `decide`, no `native_decide`):

- `SynValidation.Asyn_avoiders_le_8` — **the mechanism FIRES**: synthetic 4-AP instance, two
  disjoint APs charged fractionally (`a = 2`, `D = 1`, `nu* = 2`), two disjoint APs in the
  residual (branch `g = 1`, `3^1 = 3` leaves), reaching `τ = 4` ⇒ `h ≤ 8`. The fractional cert
  carries 2 of the 4; the branch budget is `1`, not the full `3`.
- `BaseValidation.Abase_avoiders_le_8_interleaved` — `A_base` in the **degenerate** `P = ∅`
  form (`a = 0`, `g = 5`), soundly re-deriving the tight `h(A_base) ≤ 8`.

`lake build Constants.C5bInterleaved` PASS (no warnings); `#print axioms` →
`[propext, Classical.choice, Quot.sound]` for all three theorems. Independent re-check:
`constants/5b/certificate/interleaved/check_interleaved_cert.py` (PASS).

## SHARP honest finding — `A_base` is half-integral, the g=1 milestone is impossible there

The R5 dispatch named a crisp milestone: re-derive `h(A_base) ≤ 8` with a tiny residual budget
`g = 1`. This is **mathematically not achievable** for the sound support-disjoint interleaving,
and `check_interleaved_cert.py` proves why (exact LP + exact τ, no heuristics):

- `A_base`'s 3-AP **cover LP is fully half-integral** (`ν* = 4.5`, every vertex `0` or `1/2`),
  with **no integral (`x=1`) vertex** — so Nemhauser–Trotter fixing is vacuous — and **no
  forced vertex** (143 distinct minimum covers, empty intersection).
- `max_{P ⊆ A} ( ⌈ν*(edges in P)⌉ + τ(edges avoiding P) ) = 6`, attained **only** at `P = ∅`
  (`a = 0`, full branch budget `g = 5`). Any nonempty support with `a ≥ 1` gives a strict total
  `≤ 5`.

So on A_base the interleaving cannot shrink the branch budget below the pure branch (`g = 5`).
The premise "interleaved branches only over `τ − ⌈ν*⌉ ≈ 1`" is FALSE for half-integral
instances: closing the `1.5` LP gap by branching half-integral vertices recovers only `1/2` of
LP value per branch, so the effective budget is not `τ − ⌈ν*⌉`. This is a genuine, recorded
characterization, not a build failure: the lemma is correct and reusable; A_base is simply a
pathological worst case for it.

## How to push further

1. **Deploy on an N≈30 gadget with an INTEGRAL LP component.** The interleaved cert's
   budget-shrink fires exactly when the cover LP has integral vertices (NT-fixable) or a large
   integral matching `a`. The `cpsat-exact-existence-N28-N30` search should therefore PREFER
   candidates whose 3-AP cover LP is **not** fully half-integral (report the LP solution per
   candidate; seek `a = ⌊integral matching⌋` large so `g = τ − a` is small). A candidate that
   is half-integral like A_base will NOT be `decide`-certifiable even with this cert — add the
   LP-integrality check as a search filter.
2. **Odd-set / blossom strengthening of the fractional half (the registered
   `odd-set-fractional-strengthening` hedge).** For a half-integral cluster `O`, an odd-set term
   lifts the fractional value toward the integral `τ`, raising `a` and shrinking `g`. This is
   the only route to making a half-integral N≈30 instance certifiable at small budget; if the
   N≈30 search finds only half-integral candidates, this becomes the priority. Build it as a
   sound add-on to `frac_lb_on_P` (extra `⌊|O|/2⌋`-type charge), validate it lifts A_base's
   `⌈ν*⌉` from 5 toward 6.
3. **Iterated fix-then-branch (true Nemhauser–Trotter recursion).** Rather than one `(P, g)`
   split, recurse: branch one half-integral vertex, re-solve the LP on each child (value drops
   `≥ 1/2`), fix the now-integral vertices, recurse. The total `decide` tree is then governed by
   the **number of half-integral branch levels** (`2·(τ − ν*)`), not the full `τ`. This is a
   larger lemma (a recursive predicate like `noTransLe` but interleaving an LP bound at each
   node); it is the genuinely-general scaling cert and likely a multi-round build. The current
   single-split lemma is its base case.

## Importable interface

```
import Constants.C5bInterleaved
open C5bInterleaved
-- hLe_of_interleaved : Nodup A → 0 < D →
--   edgesOK A FW_frac → suppInP P FW_frac → loadOK A FW_frac D → D*a ≤ totalW FW_frac →
--   edgesOK A FW_res → resAvoidsP P FW_res → noTransLe FW_res g = true →
--   Nodup S → S ⊆ A → avoidsAll S FW_frac → avoidsAll S FW_res →
--   S.length ≤ |A| - a - g - 1
```
Depends on `C5bTransversal` (`totalW_le_loadSum`, `loadSum_le`) and `C5bBranch`
(`noTransLe`, `noTransLe_sound`).

## Sources

- [MT26] Ma & Tang, arXiv:2602.23282 (Lemma 2.3; Thm 1.5: `c* = inf f(n)/n`; Lemma 3.6).
- LP-fix-then-branch / Nemhauser–Trotter half-integrality for `d`-Hitting-Set:
  arXiv:2308.05974, arXiv:2506.24114, arXiv:1811.09429.
