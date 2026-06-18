# bridge-combos-completeness-half

**Angle.** The harder half of the decidable bridge `is45setB l = true → C5bCap.Is45 l.toFinset`
(which wires the R8 cap lemma `C5bCap.m_le_n_sub_2` into the concrete engine): prove that the
repo's CUSTOM `combos` enumerator (`C5b.combos`, `lean/Constants/C5b.lean:122`) is **complete** —
every 4 pairwise-distinct elements of `l` arise (in some order) as a member of `combos l 4`. This
is the prerequisite the perm-half (`bridge-perm-invariance-half`) names as its `combos_complete`
hypothesis. No bound move (search-immune Lean machinery).

## Status — R9: BUILT, `lake build` PASS on `Constants.C5bCombos`, axiom-clean (CLAIM, pending review)

New file `lean/Constants/C5bCombos.lean` (wired into the build via the existing
`globs = ["Constants.+"]`). Three lemmas, no `sorry`, no `native_decide`:

- `length_of_mem_combos (l k t) : t ∈ combos l k → t.length = k`
  — every enumerated combo has the right length (induction on `l`/`k` over the recurrence).
- `mem_combos_of_sublist {t l} : t <+ l → t ∈ combos l t.length`
  — **the hard step**: every length-`k` subsequence (`List.Sublist`) of `l` is enumerated. Proved
  by induction on the `List.Sublist` derivation, matching `combos`'s include/exclude recurrence
  `combos (x::xs)(k+1) = (combos xs k).map (x::·) ++ combos xs (k+1)`:
    - `slnil` → `combos [] 0 = [[]]`;
    - `cons` (drop `x`) → the exclude (right `++`) branch via the IH;
    - `cons_cons` (keep `x`) → the include (`map (x::·)`, left `++`) branch via the IH.
  No Mathlib `sublistsLen` membership lemma applies (custom `combos`), so it is from the recurrence.
- `four_distinct_perm_sublist {l} (hl : l.Nodup) … : ∃ t, t <+ l ∧ t ~ [a,b,c,d]`
  — realizes 4 distinct members of a `Nodup` list as the `l`-ordered subsequence
  `l.filter (· ∈ [a,b,c,d])`, shown to be a `List.Perm` of `[a,b,c,d]` by
  `perm_ext_iff_of_nodup` (both `Nodup`, same element set).
- **`combos_complete {l} (hl : l.Nodup) (ha hb hc hd : ∈ l) (6 ne's) : ∃ t, t ∈ combos l 4 ∧ t ~ [a,b,c,d]`**
  — the bridge-ready completeness lemma: assembles the subsequence (`four_distinct_perm_sublist`),
  upgrades it to a `combos l 4` member (`mem_combos_of_sublist` + `length_of_mem_combos`, length 4
  from `Perm.length_eq`).

### Certificate
- Build target: `lake build Constants.C5bCombos` — PASS (Mathlib v4.31.0 pinned).
- `#print axioms combos_complete` → `[propext, Quot.sound]` (also for the three supporting lemmas).
  NO `sorryAx`, NO `Classical.choice`, NO `native_decide`/`ofReduceBool`. Cleaner than the
  CLAUDE.md ceiling (propext/Classical.choice/Quot.sound).
- Independent cross-checks (both confirm `combos l 4` covers every 4-subset exactly once):
  - in-kernel `#eval`: `(combos L 4).length = C(|L|,4)` on `L` of size 6,7 (15, 35); every member
    length-4 and distinct; the underlying SETS (`map mergeSort |> eraseDups`) number C(|L|,4).
  - external Python re-enumeration of the same recurrence vs `itertools.combinations` on
    `n ∈ {6,7,8}`: `cover_all_subsets = True`, `count = C(n,4)`, all members length 4.
- Certificate folder: `constants/5b/certificate/combos/` (build target + axioms line + the two
  cross-check scripts).

## Why this is the right form for the bridge
`Is45 l.toFinset` quantifies over 4 pairwise-distinct points in ANY order. `is45setB l` checks
`diffs4Bof` on each `combos l 4` member (ONE index order per 4-subset). `combos_complete` delivers
SOME member `t` with `t ~ [a,b,c,d]`; the perm-half reads `diffs4Bof t = diffs4B w x y z = true`
(`t` length 4) and lifts along the `List.Perm` to `diffs4B a b c d = true`. Stating the bridge via
`List.Perm` (not Finset-set-equality) is exactly the notion `diffs4B`-perm-invariance is phrased
over, so the perm-half discharges it directly.

## How to push further (next round — the assembly slug `decidable-bridge-is45-full`)
With BOTH halves landed, a later round assembles `is45setB l = true → Is45 l.toFinset` in ~10 lines:
given distinct `a,b,c,d ∈ l.toFinset` (use `List.mem_toFinset` to get `∈ l`), `combos_complete`
gives `t ∈ combos l 4` with `t ~ [a,b,c,d]`; `List.all_eq_true` on `is45setB` gives
`diffs4Bof t = true`; `length_of_mem_combos` gives `t.length = 4` so `t = [w,x,y,z]` and
`diffs4Bof t = diffs4B w x y z`; the perm-half's `diffs4B_perm` lifts it to `diffs4B a b c d = true`.
Then fire the `Abase` corollary (`m_le_n_sub_2` on `Abase.toFinset`, m ≤ 14−2 = 12).

## Notes / non-overlap
- File `C5bCombos.lean` imports only `Mathlib` + `Constants.C5b`; it does NOT depend on the
  perm-half's `C5bBridgePerm.lean`, so it compiles independently of that sibling build.
