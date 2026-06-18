import Mathlib

/-!
# C_5b : upper-bound certification machinery (warm-up: the record 4/7 gadget)

Constant `C_5b` = `c*` = the largest `c` such that `h(A) ≥ c·|A|` for every
**(4,5)-set** (weak Sidon set) `A ⊂ ℝ`, where `h(A)` is the size of the largest
**Sidon** subset of `A`.  (Erdős problem #757.)

Source of the record bound and the gadget below:
Ma & Tang, *"Largest Sidon subsets in weak Sidon sets"* (arXiv:2602.23282, Feb 2026),
abbreviated **[MT26]**.  Current verified record:  `9/17 ≤ c* ≤ 4/7`.

## What this file does (warm-up — it does NOT beat the record)

It builds reusable, machine-checked **decidable** certification machinery for an
upper-bound gadget, and runs it on the *known record* set `A_base` (14 points) to
reproduce `c* ≤ 8/14 = 4/7` as a `lake build`-passing theorem.  Beating `4/7` later is
then a one-line swap of `A_base` for a denser gadget plus a re-`decide`.

## Encoding choice (so plain `decide` is kernel-tractable)

The naive route — predicates over `Finset ℤ` with `Finset.powersetCard` and
`Finset.decidableBAll` — is mathematically clean but the kernel `decide` on it OOMs
(the `h ≤ 8` check enumerates `C(14,9)=2002` subsets through heavy `Multiset`/quotient
machinery).  Instead we phrase the two finite facts as **`Bool`-valued computations over
explicit `List ℤ`** (`weakSidonB`, `noSidonSubsetB`).  Their `= true` statements `decide`
by ordinary kernel reduction of structurally-recursive list code — fast and with no extra
axioms.  Each `Bool` procedure is documented to compute exactly the intended combinatorial
predicate; the meaning is given in the docstrings and is directly auditable.

## What is FORMALIZED here (fully proved, no `sorry`, no smuggled hypothesis)

Two finite, decidable combinatorial facts about the 14-point list `Abase`:

1. `Abase_weakSidon : weakSidonB Abase = true`
   — `A_base` is a weak Sidon set: all pairwise sums `a+b` over *unordered* pairs of
   distinct elements are distinct.  This is the "(4,5)-set" property
   ([MT26], §Definitions; the ≥5-distinct-differences form is equivalent to
   all-pairwise-sums-distinct).

2. `Abase_hLe8 : noSidonSubsetB Abase 9 = true`
   — every 9-element sub-list of `A_base` (drawn from the 14 distinct points) contains a
   3-term arithmetic progression.  By **[MT26], Lemma 2.3** (inside a weak Sidon set, a
   subset is Sidon ⟺ it contains no 3-term AP), this says no 9-element subset of
   `A_base` is Sidon, i.e. `h(A_base) ≤ 8`.

A size-8 no-3-AP (hence Sidon) witness shows `h(A_base) ≥ 8`, so in fact `h(A_base) = 8`.

## What is CITED, not proved here (the gadget → bound bridge)

The implication `(A is weak Sidon) ∧ (h(A) ≤ m) ∧ (|A| = N)  ⟹  c* ≤ m/N` is
**[MT26], Theorem 1.5** (`c* = inf_{n} f(n)/n`).  We do not formalize the real constant
`c*` or Theorem 1.5; it is taken on trust from [MT26].  This file formalizes only the
*finite, decidable load-bearing content* — that `A_base` really is a weak Sidon set with
no Sidon 9-subset — the part a finite certificate can carry.  The cited bridge is packaged
as the explicit hypothesis `MTThm15` of `c5b_le_four_sevenths`, so the one
trusted-not-proved link is visible.
-/

namespace C5b

/-! ### The record gadget and the size-8 Sidon witness (explicit lists). -/

/-- The record 14-point (4,5)-set from [MT26] (AI-assisted search). -/
def Abase : List ℤ :=
  [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]

/-- A size-8 Sidon (= no-3-AP) subset of `A_base` from [MT26], witnessing
`h(A_base) ≥ 8`. -/
def AbaseWitness8 : List ℤ := [0, 136, 200, 243, 246, 298, 323, 528]

/-! ### Bool-valued combinatorial procedures (the decidable certificate engine).

These are reusable for ANY future gadget: swap `Abase` for a new list and re-`decide`. -/

/-- All *unordered* pairs `{x,y}` with `x ≠ y` drawn from list `l`, as ordered pairs
`(x,y)` with the index of `x` strictly less than the index of `y` (so each unordered pair
appears once).  Used for the pairwise-sum check. -/
def orderedPairs (l : List ℤ) : List (ℤ × ℤ) :=
  (l.zipIdx).flatMap (fun (xi : ℤ × ℕ) =>
    (l.zipIdx).filterMap (fun (yj : ℤ × ℕ) =>
      if xi.2 < yj.2 then some (xi.1, yj.1) else none))

/-- Pure-`Bool` "all entries distinct" over a `List ℤ` (structural recursion, no
`Decidable`-instance unfolding — kernel-cheap). -/
def nodupB : List ℤ → Bool
  | [] => true
  | x :: xs => (!xs.contains x) && nodupB xs

/-- `weakSidonB l = true` iff all pairwise sums `x+y` over the unordered pairs of `l`
(`orderedPairs`) are pairwise distinct — i.e. `l` is a weak Sidon set / (4,5)-set.
(Assumes the points of `l` are themselves distinct, which is checked separately.) -/
def weakSidonB (l : List ℤ) : Bool :=
  nodupB ((orderedPairs l).map (fun p => p.1 + p.2))

/-- `has3APB s = true` iff the list `s` contains a 3-term arithmetic progression:
three entries `a, b, c` (at distinct positions) with `a + c = 2*b`. -/
def has3APB (s : List ℤ) : Bool :=
  s.zipIdx.any (fun ai =>
    s.zipIdx.any (fun bj =>
      s.zipIdx.any (fun ck =>
        ai.2 ≠ bj.2 && bj.2 ≠ ck.2 && ai.2 ≠ ck.2 &&
          (ai.1 + ck.1 == 2 * bj.1))))

/-- All `k`-element sub-lists (combinations) of `l`, by index — each chosen as a
subsequence so elements stay distinct (when `l` has distinct entries). -/
def combos : List ℤ → ℕ → List (List ℤ)
  | _, 0 => [[]]
  | [], _ + 1 => []
  | x :: xs, k + 1 =>
      (combos xs k).map (x :: ·) ++ combos xs (k + 1)

/-- `noSidonSubsetB l k = true` iff every `k`-element sub-list of `l` contains a 3-term
AP — i.e. (by [MT26] Lemma 2.3, for a weak Sidon `l`) `l` has no Sidon subset of size
`k`, so `h(l) ≤ k - 1`. -/
def noSidonSubsetB (l : List ℤ) (k : ℕ) : Bool :=
  (combos l k).all has3APB

/-! ### Sanity (`#eval`) — printed at build, not load-bearing. -/

/-- `A_base` really lists 14 *distinct* integers. -/
theorem Abase_nodup : Abase.Nodup := by decide

/-- `A_base` has 14 elements. -/
theorem Abase_length : Abase.length = 14 := by decide

/-! ### The certified facts about the record gadget.

`Abase_hLe8` evaluates `combos Abase 9` (the 2002 nine-subsets) and scans each for a
3-AP; the structural recursion is deep, so we raise `maxRecDepth`.  This is a kernel
*evaluation depth* knob only — it does not weaken the proof or add axioms. -/

set_option maxRecDepth 100000

/-- **Fact 1.**  `A_base` is a weak Sidon set (a (4,5)-set): all pairwise sums distinct. -/
theorem Abase_weakSidon : weakSidonB Abase = true := by decide

/-- The size-8 witness is a genuine sub(list)set of `A_base`. -/
theorem AbaseWitness8_subset : AbaseWitness8 ⊆ Abase := by decide

/-- The size-8 witness has 8 distinct elements. -/
theorem AbaseWitness8_card : AbaseWitness8.length = 8 ∧ AbaseWitness8.Nodup := by
  exact ⟨by decide, by decide⟩

/-- The size-8 witness contains **no** 3-term AP, hence (Lemma 2.3) is Sidon:
`h(A_base) ≥ 8`. -/
theorem AbaseWitness8_no3AP : has3APB AbaseWitness8 = false := by decide

/-- **Fact 2.**  Every 9-element subset of `A_base` contains a 3-term AP, i.e.
`h(A_base) ≤ 8`.  With `AbaseWitness8_no3AP` this pins `h(A_base) = 8`. -/
theorem Abase_hLe8 : noSidonSubsetB Abase 9 = true := by
  decide

/-! ### The bound that [MT26] Theorem 1.5 draws from the two certified facts.

We record the gadget → bound bridge as an explicit hypothesis so the dependence on the
cited Theorem 1.5 is visible.  We do not formalize the real constant `c*`; `MTThm15`
packages exactly the cited content of [MT26] Theorem 1.5 for the form of certificate this
engine produces (a weak-Sidon list of length `N` with no Sidon `(m+1)`-subset). -/

/-- The cited bridge ([MT26] Thm 1.5), as an abstract relation on a real upper bound
`c5b`:  any weak-Sidon list of `N` distinct points with no Sidon `(m+1)`-subset forces
`c5b ≤ m / N`.  This is the ONLY mathematical input taken on trust; the hypotheses it is
fed (`weakSidonB`, `noSidonSubsetB`, `length`, `Nodup`) are all `decide`-checked above. -/
def MTThm15 (c5b : ℝ) : Prop :=
  ∀ (l : List ℤ) (N m : ℕ),
    l.Nodup → l.length = N → weakSidonB l = true → noSidonSubsetB l (m + 1) = true →
      0 < N → c5b ≤ (m : ℝ) / N

/-- **Warm-up upper bound.**  Granting the cited [MT26] Theorem 1.5 (`MTThm15`), the
`decide`-checked facts about `A_base` give `c* ≤ 8/14 = 4/7`.  No `sorry`; the only
mathematical input on trust is the explicit hypothesis `hThm15` = [MT26] Theorem 1.5. -/
theorem c5b_le_four_sevenths (c5b : ℝ) (hThm15 : MTThm15 c5b) :
    c5b ≤ 4 / 7 := by
  have h := hThm15 Abase 14 8 Abase_nodup Abase_length Abase_weakSidon Abase_hLe8
    (by norm_num)
  -- `h : c5b ≤ (8 : ℝ) / (14 : ℝ)`; and `8/14 = 4/7`.
  norm_num at h
  linarith [h]

end C5b
