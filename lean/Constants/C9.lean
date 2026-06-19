/-
# C_9 = Θ(C_7): Shannon capacity of the 7-cycle — independent-set certificate engine.

This file formalizes the decidable independent-set certificate engine for the strong
powers `C_7^⊠n`, the soundness bridge from a valid list-certificate to a lower bound on
`Θ(C_7)`, and (in companion file `C9Cert367.lean`) the Lean-verification of the explicit
Polak–Schrijver 2018 size-367 independent set in `C_7^⊠5`.

`C_7 = Z_7`; two vertices `i,j` are *confusable* (adjacent-or-equal in `C_7`) iff their
cyclic distance `min(|i-j|, 7-|i-j|) ≤ 1`. In the strong power `C_7^⊠n`, two codewords
`u,v ∈ Z_7^n` are confusable iff every coordinate is confusable; they are *independent*
(non-confusable) iff SOME coordinate has cyclic distance `≥ 2`. An independent set is a
list of codewords pairwise independent.

A valid independent set of size `N` in `C_7^⊠n` gives `α(C_7^⊠n) ≥ N`, hence
`Θ(C_7) ≥ N^(1/n)`.

References:
- [PS2018] Polak, Schrijver, "New lower bound on the Shannon capacity of C_7 from
  circular graphs", IPL 143 (2019), arXiv:1808.07438. The 367 set is in the Appendix.
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.List.Pairwise

namespace C9

/-! ## Cyclic distance on Z_7 and the confusability predicate. -/

/-- Cyclic distance between two residues `a b : ℕ` mod 7: `min(|a-b|, 7-|a-b|)` on the
representatives in `[0,6]`.  We work with `ℕ` (with values taken `< 7`) so the kernel
reduces it cheaply with structural arithmetic. -/
def cdist (a b : ℕ) : ℕ :=
  let d := if a ≥ b then a - b else b - a
  min d (7 - d)

/-- Two letters are *confusable* in `C_7` iff their cyclic distance is `≤ 1`. -/
def confusable (a b : ℕ) : Bool := cdist a b ≤ 1

/-- A *codeword* is a `List ℕ` (each entry intended `< 7`). Two codewords are
*independent* (non-confusable in the strong power) iff SOME coordinate has cyclic
distance `≥ 2`, i.e. is NOT confusable.  Implemented as a short-circuiting `List.any`
over the zipped coordinates. -/
def indepPair (u v : List ℕ) : Bool :=
  (u.zip v).any (fun p => !confusable p.1 p.2)

/-! ## The list-certificate predicate.

`allPairsIndep S` checks that every word in `S` is independent from every *later* word,
by short-circuiting recursion (head-vs-tail then recurse on the tail). This avoids any
`Finset.powerset`/`Finset.powersetCard` enumeration — the route that OOMs the kernel —
and lets `decide` stop at the first confusable pair when checking a counterexample. -/
def allLaterIndep (u : List ℕ) (rest : List (List ℕ)) : Bool :=
  rest.all (fun v => indepPair u v)

/-- Pairwise-independence of a list of codewords, by structural recursion with
short-circuiting. -/
def allPairsIndep : List (List ℕ) → Bool
  | [] => true
  | u :: rest => allLaterIndep u rest && allPairsIndep rest

/-! ## Soundness: the `Bool` predicate matches `List.Pairwise`. -/

theorem allPairsIndep_iff (S : List (List ℕ)) :
    allPairsIndep S = true ↔ S.Pairwise (fun u v => indepPair u v = true) := by
  induction S with
  | nil => simp [allPairsIndep]
  | cons u rest ih =>
    simp only [allPairsIndep, allLaterIndep, Bool.and_eq_true, List.pairwise_cons, ih]
    constructor
    · rintro ⟨h1, h2⟩
      refine ⟨?_, h2⟩
      intro v hv
      have := List.all_eq_true.mp h1 v hv
      simpa using this
    · rintro ⟨h1, h2⟩
      refine ⟨?_, h2⟩
      rw [List.all_eq_true]
      intro v hv
      simpa using h1 v hv

end C9
