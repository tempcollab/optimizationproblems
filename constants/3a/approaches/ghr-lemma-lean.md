# ghr-lemma-lean — machine-checked certificate via the GHR single-set construction (LEAN line)

**Direction:** lower bound on C_3a. **Top-level theorem proves:** `1 + log(diff/s)/log q > 1.1740744`
for the winning d=84,T=162 counts. **Held numerical bound (unchanged by this sketch):**
1.1744750903655619 [R2, alphabet-search-dp].
**Borrows:** the winning `(A,d,T)` and exact counts from `alphabet-search-dp`.

## Status (round 3): BUILT GREEN, AXIOM-CLEAN, ALL CODE HOLES CLOSED

`lake build Sketches.Ghr` is green and `#print axioms C3a.beats_record` shows
`[propext, Classical.choice, Quot.sound]` only — **no `sorryAx`, no smuggled axiom**. The
proof file is `lean/Sketches/Ghr.lean` (hyphen-free module name so Lean's grammar accepts it);
the convention-required slug file `lean/Sketches/ghr-lemma-lean.lean` re-exports it (module
`Sketches.«ghr-lemma-lean»` also builds).

## Strategy (the actual proof, not the original 4-hole plan)
3a is **strongly Lean-fit**: the load-bearing step is exact integer counting of
`|U+U|, |U-U|, max(U)` plus one rational log inequality. The original skeleton listed four
holes (H0 bootstrap, H1 GHR lemma, H2 counts, H3 log inequality). This round collapses the
*provable-in-Lean* part (H0+H2+H3) into one hole-free theorem and is explicit about the one
piece that stays a literature fact (H1).

**Intermediate-statement reshape (builder's job, recorded here):** the skeleton planned H3 as
the load-bearing step `log(diff/s) - 0.1740744·log q > 0` via "atanh series / norm_num
extended" — i.e. porting `lemmas/log_bounds.py`'s rational-series machinery into Lean. That is
heavy and unnecessary. The TRUE provable statement that makes the strategy work is the **pure
integer inequality**
```
sUpU^86 * qMaxU^15  ≤  dUmU^86            -- C3a.power_ineq, ~8700-digit Nats, by `decide`
```
because `1 + log(diff/s)/log q > 1.1740744` ⟸ `log(diff/s)/log q ≥ 15/86`
⟺ `86·log(diff/s) ≥ 15·log q` ⟺ `(diff/s)^86 ≥ q^15` ⟺ `diff^86 ≥ s^86·q^15`
(`Real.log` strictly monotone; `s,q > 0`). `15/86 = 0.1744186…` is the **smallest-denominator**
rational strictly between the threshold 0.1740744 and the true ratio 0.17447509 (found by a
1-line search). This routes around the atanh port entirely: the kernel discharges one 8700-digit
`Nat` comparison via `decide`, and the analytic bridge is four off-the-shelf Mathlib lemmas
(`Real.log_le_log`, `Real.log_pow`, `Real.log_mul`, `Real.log_div`, `Real.log_pos`,
`div_le_div_iff₀`).

## Holes — all CODE holes closed; one literature-fact hole remains by design
- **H0 BOOTSTRAP — CLOSED.** Lake project at `constants/3a/lean/` created, `lean-toolchain`
  pinned to `leanprover/lean4:v4.31.0`, Mathlib pinned to rev `fabf563a…` (tag `v4.31.0`) in
  `lake-manifest.json`, `lake exe cache get` ran (8512 cached oleans), `lake build` green.
- **H2 EXACT COUNTS — CLOSED (cheap path).** The winner's `|U+U|, |U-U|, 2 max U+1` are `Nat`
  literals (`sUpU`/`dUmU`/`qMaxU`) from the validated Python DP. (The "full path" of re-deriving
  the DP inside Lean is NOT done and is not needed for the certificate; the counts are trusted
  from `ghr_dp.py`, exactly as the design intended.)
- **H3 LOG INEQUALITY — CLOSED, hole-free, axiom-clean.** `C3a.beats_record` proves
  `1 + log(diff/s)/log q > 1.1740744` with no `sorry`/axiom (see the reshape above).
- **H1 GHR SINGLE-SET LEMMA — NOT formalized in Lean (literature fact, honest gap).** The Lean
  theorem certifies the *arithmetic exponent inequality* `1 + log(diff/s)/log q > 1.1740744`.
  The link `C_3a ≥ 1 + log(|U-U|/|U+U|)/log(2 max U + 1)` (carry-free base-21 injectivity on
  U±U ⇒ the GHR2007 single-set bound) is taken from GHR2007 and is NOT proved inside this file.
  Formalizing it (Finset sumset/diffset cardinalities, base-21 injectivity, the projection
  construction) is the next round's high-value `lemmas/` candidate — substantial but self-
  contained. Until then, the certificate is "the construction's exponent inequality is
  machine-checked; its standing as a C_3a lower bound rests on the cited GHR2007 lemma".

## Value CLAIMED this round (clearly a claim until reviewer verifies)
- Lean machine-checked: `1 + log(diff/s)/log q > 1.1740744` for the d=84,T=162 counts —
  axiom-clean. This is a **gold-standard certificate of the construction**, NOT a new numerical
  value: the verified held bound stays **1.1744750903655619** (this sketch does not raise it;
  CLAUDE.md prefers a machine-checked theorem even at equal value). Target hole-free for the
  documented top-level theorem `> 1.1740744`: **yes** (axiom-clean). Does it beat the table
  value 1.1744750903655619? **No** — equal-or-below in numerical value by design; its worth is
  the certificate strength, not the magnitude.

## What would push it further
1. **Formalize H1 (GHR single-set lemma) in Lean** → promotes the whole chain to a true
   machine-checked `C_3a ≥ …` statement and yields a reusable `lemmas/` Lean lemma.
2. **Sharpen the threshold** toward the held 1.17447509: replace `15/86` with a finer rational
   (e.g. via the convergents of 0.17447509) — only matters once H1 is formalized and we want the
   Lean theorem to assert the *held* value rather than the conservative 1.1740744. The power
   inequality `diff^a ≥ s^a q^b` scales with the denominator `a` (digits ≈ 105·a), still well
   within `decide`'s reach for a up to a few thousand.
3. **Full path on H2** (re-derive the counts via an in-kernel DP) would remove the trust in the
   Python DP, but is large and low-priority vs. H1.

## Promotable lemmas
None this round that are *general*. `C3a.power_ineq` and `C3a.beats_record` are sketch-specific
(they hard-code this winner's literals), so they are not cache candidates. The genuinely reusable
Lean lemma is the **un-formalized H1 GHR single-set lemma**; once proved green next round it is
the prime `lemmas/` admission (every future `(A,d,T)` Lean sketch would import it).

## Certify
Lean `lake build Sketches.Ghr` green + `#print axioms C3a.beats_record` → no `sorryAx`.
Certificate record: `constants/3a/certificate/ghr-lemma-lean.CHECK.md`.
