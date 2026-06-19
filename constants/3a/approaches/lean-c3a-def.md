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

## R14 — B1 CLOSED (the finite/combinatorial disjoint-union count)

This round's deliverable: **sub-hole B1 (`griego_disjoint_union_count`) is now proved sorry-FREE**,
together with a reusable, fully-axiom-clean finite combinatorics toolkit. `lake build C3a` EXIT 0
(2970 jobs); `#print axioms` confirms the split below.

### What I closed (sorry-free, `[propext, Classical.choice, Quot.sound]`, NO sorryAx)
The genuine load-bearing finite content of the GHR composite count, added to `C3aDef.lean`:
- `tr`, `setSum_tr`/`setDiff_tr` (sum/diff of a one-coordinate translate = translate of the
  sum/diff — pure ring algebra), `setSum_tr_card`/`setDiff_tr_card` (a translate's sum/diff has the
  SAME cardinality — translation injective);
- `setSum_union`/`setDiff_union`, `setSum_biUnion`/`setDiff_biUnion` (distributivity over `∪`/`biUnion`);
- **`setSum_card_decompose` / `setDiff_card_decompose`** — the GHR additive identity at the
  cardinality level: for pairwise-disjoint translate images + a disjoint interval piece,
  `|(I ∪ ⋃ᵢ(aᵢ+B)) ± B| = mₙ·|B±B| + |I±B|`, via `Finset.card_biUnion` + `card_union_of_disjoint` +
  `setSum/Diff_tr_card`. These two are the reusable heart and are **promotable** (see below).

`#print axioms setSum_card_decompose` / `setDiff_card_decompose` / the four `*_tr_card`/`*_biUnion`
helpers: all `[propext, Classical.choice, Quot.sound]` — sorryAx-free.

### B1 itself — `griego_disjoint_union_count`, proved sorry-free
`#print axioms griego_disjoint_union_count` → `[propext, sorryAx, Classical.choice, Quot.sound]`.
The proof TERM is sorry-free; the `sorryAx` enters ONLY via the explicitly-named hypotheses/data it
consumes (`griego_ak_disjoint` (B1a) + the witness data `Ubase`/`Qbase`/`Ubase_carryfree`/
`an_interval`/`an_index`/`an_shift`). No smuggled axiom; the count derivation is real.

### Two intermediate-statement fixes (my job, recorded)
1. **Exponent `^ n → ^ (n+1)`.** With `bk n = U^{⊗n} = tpow Qbase Ubase n`, the cached
   `tensor_pow_sumset_card` gives `|U±U|^(n+1)` (the `tpow … n` convention has `n+1` factors). The
   planned B1 exponent `^ n` was off by one; the true, provable statement is `^ (n+1)`.
2. **One shared `tₙ` → two witnesses `tsum`, `tdiff`.** GHR's single interval term `t` additionally
   relies on `|I+B| = |I−B|` for the long interval — a SEPARATE finite fact, not part of the
   disjoint-union count. Carrying `tsum = |[1,Lₙ]+Bₙ|` and `tdiff = |[1,Lₙ]−Bₙ|` separately makes B1
   exactly the count the decomposition lemmas prove, with no smuggled interval-symmetry; the
   `tsum = tdiff` reconciliation is deferred to B3.

Also: `bk`/`ak` are no longer opaque `sorry` defs — `bk n := tpow Qbase Ubase n` and
`ak n := an_interval n ∪ (an_index n).biUnion (fun i => tr (an_shift n i) (bk n))` are now PINNED to
the GHR composite shape. This pinning is what made B1 provable; only the disjointness of the pieces
(which needs the separation choice) stays a hole.

### Holes remaining (12 documented `sorry`, all build GREEN)
- **B1a `griego_ak_disjoint` (line 330) — NEW named sub-hole exposed by closing B1.** The pairwise
  disjointness of the `mₙ` translate images + the interval piece, in both sums and diffs. This is the
  genuine *uncached* combinatorial content (GHR's separation `aᵢ−aⱼ ∉ Bₙ−Bₙ`), depending on the
  explicit shift choice. Finite once `an_shift` is pinned, but no cached lemma supplies it. BLOCKER:
  needs an explicit `an_shift`/`an_interval`/`an_index` construction + a range/pigeonhole disjointness
  proof — substantial but strictly finite; the natural next builder target.
- **Witness data (lines 302–311):** `Ubase`/`Qbase`/`Ubase_carryfree` (the Griego digit set + base +
  carry-free property), `an_interval`/`an_index`/`an_shift` (the dilution data). Documented holes —
  the explicit numeric/shift literals.
- **B2 `griego_bounded_doubling` (392), B3 `griego_diff_lower_bound` (401), B4 `griego_card_tendsto`
  (409)** — the three real-analysis sub-holes (floor-dilution doubling; θ-reconciliation via cached
  `log_bridge` + the `tsum=tdiff` interval-symmetry; atTop sup packaging). Left documented, NOT scoped
  this round (multi-round analysis infra, as planned).
- **Pre-existing:** `realizes_one` (139), `realizableSet_bddAbove` (150).

`griego_realizes` (assembled from B2/B3/B4), `c3a_ge_theta`, `c3a_lower_bound_def` are unchanged and
still assemble; B1's exponent/witness reshape did not touch them (the assembly routes through B2/B3/B4,
not B1 — B1 is the finite content B3 will consume).

## Claim
NO held raise — this is structural Lean progress only (B1 closed). `held` stays the verified Python
value C_3a > 1.1779 (R13). Even fully closed, the wired bridge certifies only θ>1.1771 (the B-side
reads `NativeDecideSmallMT`), not the held 1.1779. The claim of this round is solely that the
load-bearing finite combinatorial sub-hole B1 is now a real sorry-free Lean derivation (depending only
on the documented B1a + witness-data holes), and that two general axiom-clean counting lemmas are
available for reuse.

## R15 — B1a SPACING LEMMAS CLOSED (`setSum_tr_pair_disjoint` / `setDiff_tr_pair_disjoint`)

This round's deliverable: **the two general spacing lemmas the outliner factored out of B1a are now
proved sorry-free and axiom-clean**, and `griego_ak_disjoint` (B1a) is consequently reassembled with
its proof TERM sorry-free (the only `sorryAx` it now carries traces solely to the residual
`an_separated` hole it legitimately consumes). `lake build C3a` EXIT 0 (2969 jobs).

### What I closed (sorry-free, `#print axioms = [propext, Classical.choice, Quot.sound]`, NO sorryAx)
- **`setSum_tr_pair_disjoint`** (line ~365): if every element of `setSum B B` lies in `[lo, lo+diam]`
  and the shift gap `diam < |c − c'|`, then `setSum (tr c B) B` and `setSum (tr c' B) B` are disjoint.
  Proof: `setSum_tr` rewrites both to `image (c+·) (setSum B B)`; `Finset.disjoint_left` gives a common
  `c+w = c'+w'` with `w,w' ∈ [lo,lo+diam]`; `abs_le` + `omega` derive `|c−c'| ≤ diam`, contradicting
  `hgap` via `linarith`. Pure ℤ interval arithmetic — no construction needed.
- **`setDiff_tr_pair_disjoint`** (line ~380): the `setDiff` analogue, identical proof via `setDiff_tr`.

`#print axioms` (recorded via a throwaway `Sketches/AxCheck.lean`, since deleted):
```
'C3a.setSum_tr_pair_disjoint'  depends on axioms: [propext, Classical.choice, Quot.sound]
'C3a.setDiff_tr_pair_disjoint' depends on axioms: [propext, Classical.choice, Quot.sound]
'C3a.griego_ak_disjoint'       depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
```
The `griego_ak_disjoint` `sorryAx` is honest: the reassembly proof term is sorry-free; the `sorryAx`
enters ONLY through the named `an_separated` obligation it `obtain`s. (R14-style: a discharged proof
that consumes a documented sub-hole shows `sorryAx` tracing only to that hole.)

### Intermediate-statement note (NOT required this round)
The two spacing lemmas as planned (`WithinDiam (B±B) lo diam ∧ diam < |c−c'| ⟹ Disjoint …`) are
exactly true and provable as stated — no reshape needed. The one small Lean adjustment vs the plan's
suggested tactic path: `abs_lt` does NOT fire on `diam < |w'−w|` (it matches `|·| < ·`, abs on the
LHS), so I instead prove `|c−c'| ≤ diam` via `rw [abs_le]; constructor <;> omega` (omega uses the
membership equality `c+w = c'+w'` plus the two `WithinDiam` bounds) and close with `linarith`.

### Holes remaining after R15 (13 documented `sorry`, all build GREEN)
- **`an_separated` (line ~414) — the residual construction obligation** (the harder, uncached half of
  B1a). NOT closed this round, by plan. BLOCKER: it asserts the existence of the diameters AND the
  shift-spacing `diam < |aᵢ−aⱼ|` AND the interval-vs-union disjointness for the *concrete* witness data
  `an_shift`/`an_index`/`an_interval` — but those are themselves `sorry` defs (lines 309–311). There is
  nothing to compute the spacing from until the witness data is pinned. Closing it needs (a) pinning
  `an_shift n i = i·(2·maxbk n + 1)` (an AP) and `an_interval n` below all translates, and (b) a new
  `maxbk` element-range bound on `bk n = tpow Qbase Ubase n` (provable by induction on the box/emb
  carry-free digit structure). That `maxbk` lemma + the witness-data pinning is the natural next
  sub-target. NOT attempted this round (it is the larger, construction-bearing half, and depends on the
  Ubase/Qbase witness data which is also still a hole).
- **Witness data:** `Ubase`/`Qbase`/`Ubase_carryfree` (302–304), `an_interval`/`an_index`/`an_shift`
  (309–311) — the explicit Griego digit set + base + carry-free property + dilution data.
- **B2/B3/B4** (`griego_bounded_doubling`, `griego_diff_lower_bound`, `griego_card_tendsto`) — the
  three real-analysis sub-holes. Multi-round; not scoped.
- **Pre-existing:** `realizes_one` (140), `realizableSet_bddAbove` (151).

`griego_ak_disjoint` (B1a) and `griego_disjoint_union_count` (B1) are unchanged in statement and still
green; B1a is now a sorry-free reassembly modulo `an_separated`.

## Status
R15: B1a spacing lemmas `setSum_tr_pair_disjoint`/`setDiff_tr_pair_disjoint` CLOSED sorry-free
(`[propext, Classical.choice, Quot.sound]`); `griego_ak_disjoint` reassembled sorry-free modulo the
residual `an_separated` hole. `lake build C3a` EXIT 0 (2969 jobs). 13 documented `sorry`
(`an_separated` is now the load-bearing residual of B1a; witness data; B2/B3/B4; realizes_one;
bddAbove). No smuggled axiom. No `held` raise — structural only; even fully wired the bridge certifies
θ>1.1771, below the held 1.1779.
File: `lean/Sketches/C3aDef.lean`.

(Superseded: the R14 "12 documented sorry" status — B1a's spacing lemmas now closed, `an_separated`
named as the residual.)

## Promotable lemmas
**R15 — flag for certification** (proved sorry-free this round in `lean/Sketches/C3aDef.lean`,
`#print axioms = [propext, Classical.choice, Quot.sound]`, general — not sketch glue):
- `setSum_tr_pair_disjoint` (line ~365): `WithinDiam (setSum B B) lo diam → diam < |c − c'| →
  Disjoint (setSum (tr c B) B) (setSum (tr c' B) B)`.
- `setDiff_tr_pair_disjoint` (line ~380): the `setDiff` analogue.
  Both: a shift gap strictly exceeding the diameter of the sum/diffset ⟹ the two translate images are
  disjoint. Reusable for any composite/AP-dilution disjointness argument.

**R14 — flag for certification** (still pending, all `[propext, Classical.choice, Quot.sound]`):
- `setSum_card_decompose` / `setDiff_card_decompose` (lines ~271/285) — the disjoint-union GHR
  additive count `|(I ∪ ⋃ᵢ(aᵢ+B)) ± B| = |shifts|·|B±B| + |I±B|` under pairwise + interval
  disjointness. The reusable heart of any composite-dilution count.
- Supports: `setSum_tr_card` / `setDiff_tr_card` (translate cardinality-invariance),
  `setSum_union`/`setDiff_union`, `setSum_biUnion`/`setDiff_biUnion` (sum/diff distributivity),
  `setSum_tr`/`setDiff_tr` (translate-pushout). All sorry-free, axiom-clean.

(The earlier R12 "None this round" note is superseded.)
