# decorated-domino-upper — UPPER bound by refining BBEPP's "factor 2"

**Side / target.** Upper bound. Top-level target (unchanged, faithful):
`gr(Av(1324)) <= beta * 27/4 < 13.5` for a certified per-point interleave multiplicity
`beta < 2`, beating BBEPP2017's record 13.5.

**Strategy (explorer angle A1 — Lean-fit, highest-slack target).**
BBEPP's injection `Av_n(1324) -> {o,x}^n x D_n` (Thm 4.1) records the vertical interleave as an
*arbitrary* binary word (read top-to-bottom by value: `o` = upper/Av(213) cell, `x` =
lower/Av(132) cell), collapsing all upper-cell points into a domino's top cell and all
lower-cell points into the bottom cell. Counting gives `2^n * (27/4)^n => 13.5`. The factor
`2^n` is the "very rudimentary" overcount BBEPP flag (p.14): the achievable-word set `W_n` is a
*strict* subset of `{o,x}^n`. If `|W_n| <= C*beta^n` with `beta < 2`, then since the image lies
in `W_n x D_n`, `gr <= beta * 27/4 < 13.5`.

## What I closed this round

- **H1 — CLOSED.** `gr(D) = 27/4` exact (BBEPP Thm 3.1 / OEIS A000139,
  `|D_n| = 2(3n+3)!/((n+2)!(2n+3)!)`). Returned as an exact `Fraction`; cross-checked
  `A000139(1..6) = 2,6,22,91,408,1938`. **Promotable** (see below).
- **H4 — CLOSED (validity, n<=8).** I *reimplemented* BBEPP's whole upper-bound machinery and
  verified it by exhaustion:
  - the greedy gridding (Prop 2.1 even/odd pivot rules) yields strips that genuinely avoid 213
    (upper) and 132 (lower) — `0` invalid strips for all n<=8;
  - `sigma -> (interleave_word, domino)` is a genuine **injection** — `#distinct (word,domino)
    pairs == |Av_n(1324)|` for every n<=9 (zero collisions). My `avoids_1324` reproduces OEIS
    A061552: `1,2,6,23,103,513,2762,15793,94776`. So the injection setup is sound and faithful.

## The load-bearing finding (it RESHAPES H2 — flagged to the outliner)

The sketch's planned H2 was "a **forbidden local factor** in the interleave word forced by
1324-avoidance" → transfer matrix on admissible words → Perron root `< 2`. **Exhaustive
computation up to n=8 REFUTES that mechanism:**

- **Every** binary factor of length 2, 3, 4 occurs in some achievable word
  (`forbidden_local_factors()` returns the empty set). So there is **no bounded-length
  forbidden factor**, hence **no transfer matrix on the `{o,x}` word alphabet with Perron root
  `< 2`**. This is *why* BBEPP could not refine the factor 2 as a word constraint — the
  constraint is **not local in the word**; it is **joint (word × domino)**.
- The only provable *pure-word* constraint is the O(1) prefix rule **"every achievable word
  begins with `oo`"** (the two largest values always sit in upper cells). Removes a constant,
  not a factor — `beta` stays `= 2`.
- `|W_n|`, n=1..10 `= 1,1,2,3,5,10,22,49,107,228`; successive ratios
  `1.5,1.67,2.0,2.2,2.23,2.18,2.13` — consistent with a growth rate **near, possibly just below,
  2**, but **not certifiably `< 2`** from accessible `n` and not separated from 2 by any provable
  margin. (Not a known OEIS sequence.)

**Honest claim this round: only `beta = 2` is certifiable ⇒ bound `= 2*27/4 = 13.5`. This does
NOT beat the record.** I refuse to fabricate a sub-2 `beta`. The script's top-level
`upper_bound()` deliberately *raises* on the open hole rather than print a number it cannot
prove; `status_report()` (the `__main__` path) prints the verified parts + the refutation.

## Holes remaining and the blocker on each

- **H2 (OPEN, the hard step).** Certified `beta < 2` with image ⊆ `W_n x D_n`, `|W_n| <=
  C*beta^n`. **Blocker:** the pure-word forbidden-factor formulation is *dead* (refuted above).
  The constraint that actually shrinks the count is **joint**: for a *fixed* domino, only some
  words are consistent (and vice versa). A valid H2 must bound the number of (word, domino)
  pairs *jointly*, e.g. via a transfer matrix whose states carry partial domino/arch state, not
  just the last word symbols. This is genuinely the refinement BBEPP could not find; I did not
  find it either this round.
- **H3 (OPEN, mechanical).** Converts a certified `beta` to `beta * 27/4`. Trivial once H2 lands;
  currently raises through H2.

## Value claimed

**Claim (unverified, and NOT an improvement): `gr(Av(1324)) <= 13.5`** — i.e. this round only
reproduces the existing record `13.5`, it does **not** beat it. `target hole-free: no`.
Nothing to write to `current.md`.

## What would push it further / reshaped plan (for the outliner)

The pure-word H2 is refuted, so the *line* needs re-planning (outliner's call):

1. **Joint transfer matrix.** States = (small window of recent word symbols) × (a bounded
   summary of the domino arch state needed to decide 1324-consistency). Count admissible
   (word, domino-step) transitions; Perron root might beat `2*27/4`. Risk: the necessary domino
   state may be unbounded (then not a finite matrix) — needs theory on which arch state is
   load-bearing.
2. **Per-domino word bound.** I measured max words/domino = `1,1,1,1,2,4,8,17,32` (n=1..9) —
   roughly doubling, so words-per-domino is itself ~`2^{n/2}`-ish and NOT O(1); a naive
   "few words per domino" bound fails. But the *distinct dominoes that actually arise*
   (`1,2,6,23,102,494,2530,13455,73515`) are far fewer than `|D_n|`
   (`2,6,22,91,408,1938,9614,49335,260130`): the real overcount is **unachievable dominoes**,
   not the word. A refinement bounding "achievable dominoes" could be the better road and is
   a different sketch than "decorate the word."
3. **Consider RETHINK.** If the orchestrator wants to keep this slug, it should be re-pointed at
   the joint (word, domino) count (1) — the current "forbidden word factor" framing is a proven
   dead end. Sibling `bona-forbidden-factor-upper` faces the analogous (documented) local-factor
   saturation wall; both upper-side local-factor attacks share this barrier.

## Promotable lemmas

- **`domino_growth_constant`** — statement: the number of `n`-point 1324-avoiding dominoes is
  `|D_n| = 2(3n+3)!/((n+2)!(2n+3)!)` (OEIS A000139), with `gr(D) = 27/4` (exact). Source: BBEPP
  Thm 3.1. Proved/realized green in the sketch as the exact closed form `A000139(n)` plus the
  exact `Fraction(27,4)`; cross-checked against A000139's first terms. Reusable by every 30a
  upper/lower sketch built on the domino skeleton (this sketch, tromino, bona). Reviewer:
  certify into `constants/30a/lemmas/` as the cited exact constant (it is a literature theorem,
  not a re-derivation — bar is "the cited formula is transcribed correctly", which the
  small-`n` cross-check confirms).
