# Sketch `lean-c3a-def` — scoped Lean DEFINITION of C_3a (de-risk the bridge)

## Strategy
The self-contained machine-checked Lean theorem `C_3a > 1.1771` has, per the R12 explorer, exactly
ONE uncached blocker: `C3aReal` is currently `opaque` in `lean-native-decide-smallmt`, so the
read-off `θ ≤ C3aReal` can only be an ASSUMED hypothesis (`ghr`). Everything else is already a
Lean theorem: the integer core (`native_decide`, θ>1.1771, hole-free), the log-algebra half
(`log-bridge`, cached), and the finite/counting half of the limit (`tensor-multiplicativity`,
cached).

This sketch is **definition-only and deliberately proves NO new bound**. It replaces the opaque
constant with a CONCRETE `sSup`-over-a-predicate definition `C3aRealDef`, and exposes the read-off
as named holes so the **reviewer can rule the definitional approach in/out cheaply** before the run
commits multiple rounds to the real-analysis read-off.

Borrows: `lean-native-decide-smallmt` (`theta`, `theta_gt` — the certified θ>1.1771), the cached
`tensor-multiplicativity` lemmas (`sumset`/`diffset`, `tensor_pow_*_card`), `log-bridge`.

## R12 — FAITHFULNESS FIX (this round's deliverable)

The R12 outline-reviewer's load-bearing finding: the R11 draft predicate **dropped the doubling
clause `|A+B| ≪ |A|`** and used `A = B` single-family witnesses. Dropping a constraint enlarges the
realizable set, so the sup could EXCEED C_3a — making `c3a_lower_bound_def` a statement about an
inflated, non-faithful constant. This round restores the doubling clause in the right asymptotic
sense and switches to the faithful two-set form, verified against the [GHR2007] source.

### The exact [GHR2007] definition (verified against the PDF, R12)
Extracted `https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf` with `pdfminer` (saved nowhere
binary — text only). The constant is **inequality (5) / Theorem 1** (PDF text lines 520–600,
640–720):

> Theorem 1. Let K > 1 be a real number. There exist a real number θ₀ > 1.14465 and two sets of
> integers A and B **arbitrarily large** such that `|A+B| ≤ K|A|` (7) and `|A−B| ≥ (2(K−1)/3K)^{5/4} |A+B|^{θ₀}`.
>
> (5):  `|A| = n`, `|A+B| ≤ K|A|`  and  `|A−B| ≥ c(K)|A+B|^θ`,  where `c(K) > 0`.

So, exactly:

    C_3a = sup { θ : ∃ K > 1, ∃ c(K) > 0, arbitrarily large finite (A,B) with
                 (i)  |A+B| ≤ K·|A|              (the doubling |A+B| ≪ |A|, FIXED K)
                 (ii) |A−B| ≥ c(K)·|A+B|^θ       (cleared |A−B| ≫ |A+B|^θ) }.

BOTH clauses are genuine. K is a **fixed** constant for the witnessing family (independent of the
family index n) — that is the precise sense of `≪`. This is what the R11 draft dropped.

### Why the witness is a TWO-SET composite, NOT the bare tensor power `A=B=U^{⊗k}`
This is the crux the reviewer asked to pin down. The R11 draft's `A = B = U^{⊗k}` **violates clause
(i)**: with `A = B = U^{⊗k}`, `|A+B| = |U+U|^k`, `|A| = |U|^k`, so the doubling ratio is
`(|U+U|/|U|)^k → ∞` — UNBOUNDED, no fixed K works. (Generally `|A+A| ≥ |A|`, so `|A+A| ≤ K|A|` with
fixed K fails for any growing set.) So the bare tensor family is correctly **excluded** by the
restored clause — confirming the clause is load-bearing, not cosmetic.

The actual [GHR2007, Lemma p.4–5] witness realizing `θ = 1 + log(d/s)/log q` (PDF lines 1405–1700)
is the **composite**:

    Bₖ := U^{⊗k}   (the digit-tensor power; |Bₖ| = |U|^k, |Bₖ ± Bₖ| = |U±U|^k = s^k / d^k),
    Aₖ := [1, Lₖ] ∪ ⋃_{i=1}^{mₖ} (aᵢ + Bₖ),   mₖ = ⌊qᵏ/sᵏ⌋,   Lₖ = ⌊3qᵏ/(2(K−1))⌋,

with shifts aᵢ separated (`aᵢ − aⱼ ∉ Bₖ − Bₖ`) so translates + interval are sum/diff-disjoint.
GHR compute `|Aₖ + Bₖ| = mₖ·sᵏ + t`, `|Aₖ − Bₖ| = mₖ·dᵏ + t`, `t = |[1,Lₖ]+Bₖ|`, and with
`mₖ ≈ qᵏ/sᵏ`, `Lₖ ≈ qᵏ/(K−1)` the doubling is DILUTED to the FIXED bound `|Aₖ+Bₖ| ≤ K|Aₖ|`
(clause (i) HOLDS) while `|Aₖ−Bₖ| ≥ (qd/s)^k ≥ c(K)·|Aₖ+Bₖ|^θ` (clause (ii)). The cached
`tensor_pow_*_card` lemmas supply exactly the Bₖ-cardinalities the computation rests on; the
dilution wrapper (m translates + interval) is the additional combinatorics — the genuine remaining
content of HOLE B `griego_realizes`.

**Conclusion:** with the doubling clause restored and the witness understood as the GHR composite,
(a) `RealizableSet ⊆ {registry-realizable}` ⟹ `C3aRealDef ≤ C_3a` (the SAFE direction for a lower
bound), (b) the 4/3 structural cap applies honestly, and (c) the Griego family IS a member (via the
composite, not the bare tensor), so the definition is non-vacuous and the held bound flows through
it. Both R12-reviewer objections (dropped doubling; A=B collapse) are dissolved.

## The definition now on the table (corrected)
```lean
def setSum (A B : Finset ℤ) : Finset ℤ := Finset.image₂ (· + ·) A B
def setDiff (A B : Finset ℤ) : Finset ℤ := Finset.image₂ (· - ·) A B

def Realizes (c : ℝ) : Prop :=
  ∃ A B : ℕ → Finset ℤ, ∃ K : ℝ,
    Filter.Tendsto (fun n => ((A n).card : ℝ)) Filter.atTop Filter.atTop ∧
    (∀ᶠ n in Filter.atTop, ((setSum (A n) (B n)).card : ℝ) ≤ K * ((A n).card : ℝ)) ∧   -- clause (i)
    (∀ᶠ n in Filter.atTop,
      ((setSum (A n) (B n)).card : ℝ) ^ c ≤ ((setDiff (A n) (B n)).card : ℝ))            -- clause (ii)

noncomputable def C3aRealDef : ℝ := sSup { c | Realizes c }
```
- Two sets `A n, B n` (matches the registry's two-set form, removes the A=B-collapse worry).
- Clause (i): a SINGLE fixed `K` (`∃ K`, outside the `∀ᶠ n`) bounds `|A n + B n| ≤ K|A n|` eventually
  — the bounded-doubling `≪` in the right asymptotic sense.
- Clause (ii): the cleared `≫` (constant c(K) absorbed into "eventually").

## Holes (all documented `sorry`, build GREEN — `lake build C3a` EXIT 0, 2970 jobs)
Exactly 3 `sorry` (warnings at `C3aDef.lean:139,150,169`):
- `realizes_one : Realizes 1` — nonemptiness witness. Needs a concrete bounded-doubling family with
  `|A−B| ≥ |A+B|^1` (the GHR composite at the trivial exponent, or any explicit such family).
  Feeds `realizableSet_nonempty`.
- `realizableSet_bddAbove : BddAbove RealizableSet` — bounded by the [GHR2007, Theorem 2] structural
  cap `4/3` (the proven upper bound), now applicable HONESTLY because the doubling clause is restored
  (the 4/3 bound is proved for the constrained constant). Makes `sSup` a genuine real. Needs the
  GHR2007 upper-bound theorem.
- `griego_realizes : Realizes theta` — **HOLE B, the load-bearing read-off**: the Griego family
  realizes θ via the GHR COMPOSITE witness (Bₖ = U^{⊗k} + the m-translate/interval dilution).
  Uses cached `tensor_pow_*_card` (for the Bₖ cardinalities) + the dilution combinatorics + the
  θ = 1+log(D/S)/log Q reconciliation.

Then (one line each, modulo the holes, no new `sorry`):
- `c3a_ge_theta : theta ≤ C3aRealDef` — `le_csSup realizableSet_bddAbove griego_realizes`.
- `c3a_lower_bound_def : 11771/10000 < C3aRealDef` — `lt_of_lt_of_le theta_gt c3a_ge_theta`.

## `#print axioms` (R12, recorded)
- `c3a_lower_bound_def` → `[propext, sorryAx, Classical.choice, Quot.sound,
  Q_gt_one._native…, S_pos._native…, griego_140_265_int_cert._native…]`. The `sorryAx` is honest —
  it traces ONLY to the 3 declared read-off holes; the `native_decide` axioms are the legitimate
  integer-core ones from `lean-native-decide-smallmt`. **No custom `axiom`, no smuggled hard step.**
- `c3a_ge_theta`, `realizableSet_nonempty` → `[propext, sorryAx, Classical.choice, Quot.sound]`
  (sorryAx via the holes only).

## What this round closed / what remains
- **CLOSED this round (the reviewer's requested fix):** the faithfulness defect. The doubling clause
  `|A+B| ≤ K·|A|` is restored with a fixed K, the predicate is two-set (no A=B collapse), and the
  definition is now provably a faithful UNDER-estimate of C_3a (`C3aRealDef ≤ C_3a`). The Griego
  family's membership route is pinned down concretely (the GHR composite, with the doubling-dilution
  computation spelled out and tied to the cached tensor-power cardinalities). The definition is
  non-vacuous. This was a *definitional* fix — no Lean lemma newly proved beyond keeping the
  assembly green; the deliverable is the corrected, reviewer-rulable definition + faithfulness
  argument.
- **REMAINS (3 holes):** `realizes_one`, `realizableSet_bddAbove`, `griego_realizes` (HOLE B). HOLE
  B is multi-round (the dilution combinatorics + the limit packaging); the other two need the GHR
  upper bound and a baseline witness. None attempted to close this round — this is the scoped
  definition-only de-risking step, as dispatched.

## Claim
NO held raise — this is a definitional de-risking step (explicitly NOT a bound claim). `held` stays
the verified Python value C_3a > 1.1776 (R11). The CLAIM of this sketch is only that the *definition*
is now faithful (a lower-bound under-estimate of the registry C_3a), pending the reviewer's in/out
ruling. When the 3 holes close in later rounds, `c3a_lower_bound_def` becomes a self-contained
machine-checked `C_3a > 1.1771` over the concrete registry definition.

## What would push it further
1. Close `griego_realizes` (HOLE B): formalize the GHR composite Aₖ = [1,Lₖ] ∪ ⋃(aᵢ+Bₖ), prove the
   doubling and the diff-set bounds from the cached `tensor_pow_*_card` + interval/translate counting,
   and package the `k→∞` realization (`Filter.atTop`). Biggest lever; multi-round.
2. Close `realizableSet_bddAbove`: formalize (or assume as a clearly-named hypothesis) the
   [GHR2007, Theorem 2] 4/3 upper bound under bounded doubling.
3. Close `realizes_one`: any explicit bounded-doubling family with `|A−B| ≥ |A+B|` (e.g. an
   arithmetic progression pair) suffices.

## Status
R12: faithfulness fix landed; `lake build C3a` EXIT 0 (2970 jobs); 3 documented `sorry`
(`realizes_one`, `realizableSet_bddAbove`, `griego_realizes`); axioms clean apart from the honest
hole `sorryAx`. No `held` raise — definitional scoping only.
File: `lean/Sketches/C3aDef.lean`.

## Promotable lemmas
None this round. No reusable sorry-free lemma was proved (the round's work was a definitional
reshape; `setSum`/`setDiff` are trivial glue, the substantive lemmas remain holes). The cached
`tensor-multiplicativity` and `log-bridge` lemmas are already promoted and are imported as-is.
