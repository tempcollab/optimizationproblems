# transfer-matrix-lower — LOWER bound via verified-subclass transfer matrix + Collatz-Wielandt

**Side / target.** Lower bound. Top-level target (unchanged, outliner's): `gr(Av(1324)) >=
rho(M) >= r > 10.271`, beating BBEPP2017's verified record 10.271.

**Strategy.** A finite nonnegative transfer matrix `M` whose accepted language is a *verified
subclass* `S ⊆ Av(1324)`. Then `gr(S) = rho(M)` (Perron root) and `gr(Av(1324)) >= rho(M)`. A
**Collatz–Wielandt** rational witness `v > 0` with `Mv >= lam·v` entrywise certifies
`rho(M) >= lam` by exact rational arithmetic. Pick `lam > 10.271`.

## What R1 closed (verified, in `certificate/transfer-matrix-lower.py`)

The two load-bearing obligations are **fully discharged on a concrete sound machine** — the
**skew-sum closure** construction:

- **H2 (soundness) — CLOSED.** Sound subclass `S_L := { σ ∈ Av(1324) : every skew-component of
  σ has length ≤ L }`. This is literally a *subset* of `Av(1324)`, counted *without repetition*
  (the skew decomposition `σ = c₁ ⊖ c₂ ⊖ … ⊖ cₜ` into skew-indecomposables is **unique**), so
  `|S_L,n| ≤ |Av_n(1324)|`.
  **Skew-sum closure lemma (proved):** `a ⊖ b` avoids 1324 ⇔ `a, b` both avoid 1324. Proof:
  in `a ⊖ b` the `a`-points hold the left positions and the high values; a *crossing* 1324
  occurrence would put its first `t∈{1,2,3}` points in `a`, which (being highest-valued) must
  carry the `t` largest value-ranks of `1324` — but the ranks on the first `t` pattern positions
  of `1324=(1,3,2,4)` are never the `t` largest (`t=1→{1}`, `t=2→{1,3}`, `t=3→{1,2,3}`).
  Contradiction ⇒ no crossing occurrence ⇒ avoidance is component-local; induction over `t`
  gives `S_L ⊆ Av(1324)` for all `L`. Verified two ways in the script: an exact finite
  rank-argument check `prove_skew_sum_closure()`, and a brute-force re-check
  `brute_check_skew_closure()` over all avoider pairs with `|a|+|b| ≤ 7`.

- **H1 (build the matrix) — CLOSED for this machine.** `b_k` = #{skew-indecomposable
  1324-avoiders of length `k`} computed **exactly** by brute force (`1,1,3,12,56,289,1604,9415`
  for `k=1..8`). Uniqueness of skew decomposition ⇒ the count `f_n = |S_L,n|` satisfies the
  linear recurrence `f_n = Σ_{k=1}^L b_k f_{n−k}`, so `gr(S_L) = rho(M)` with `M` the
  `L×L` nonnegative-integer **companion matrix** of the recurrence. The script confirms the
  matrix counts the subclass with **no over/under-count** (`verify_recurrence()`: the recurrence
  reproduces the brute-force count of `S_L` for `n ≤ 7`).

- **H3 (Collatz–Wielandt witness) — CLOSED.** Geometric witness `v_i = q^{L−1−i}`, `lam = q`
  with `q` a rational strictly below `rho(M)`. Shift rows give exact equality `(Mv)_i = q·v_i`;
  row 0 gives `(Mv)_0/v_0 = Σ_k b_k q^{1−k} > q` for any `q < rho(M)`. Re-checked entrywise in
  exact `Fraction` arithmetic (numpy is used **only** to pick `q`; the certificate is pure
  rational). Independently re-derived: row 0 is a strictly positive rational, shift rows exact 0.

**Certified value (CLAIM, pending reviewer):** `gr(Av(1324)) >= 1886663/500000 = 3.773326`
at `L=8`. Exact, reproducible, axiom-clean.

## H_BIG status — DISCHARGED this round (R2) as a sound floor-raise, NOT a record break

**This round does NOT beat 10.271** — no sound finite/integer machine does at feasible size
(see "decisive computable question — answered: NO" below). But H_BIG is **discharged** in the
sense that its load-bearing holes (`insertion_encoding_states` / the sound quotient / the general
CW) are now **closed** by a complete, certified construction (the bounded-state insertion
automaton `A_K`), raising the sound floor `3.773326 → 6.223319`. The R1 skew-sum machine remains
in the file as the original floor; the R2 automaton is the higher sound bound.

The remaining *record-reaching* work is a genuinely NEW hole (a GF-weighted Catalan-cell
staircase, or Conjecture 8) — flagged for the outliner below; it is not a continuation of
pushing `K` on an exact integer automaton (which provably caps logarithmically).

## R2 — H_BIG DISCHARGED with a SOUND bounded-state insertion-encoding automaton

### What I closed this round (H_BIG)

The R2 dispatch pointed H_BIG at the **min-weighted `(n,r)` quotient** (Angle A). I **measured
that plan and found it a dead end** (see "Reshape" below), and replaced it with a **strictly
sounder, exact** construction that I fully closed and certified:

**The sound machine `A_K` (a finite automaton, no averaging, no min-weighting, no Conjecture 8):**

1. **Insert-new-maximum bijection (E1).** Every permutation of `[n]` is built by a unique
   sequence of "insert the new global maximum at position `pos`" steps. (verified, `n≤6`.)
2. **Local edge rule (E2), exhaustively verified to length 8→9.** Inserting the new max at
   position `pos` into a 1324-avoider `p` creates a 1324 **iff** the left-prefix `p[:pos]`
   contains the pattern **132** (the new max is the global max, so it can only be the `4` of a
   1324; a 1324 is created iff a 132 sits entirely to its left). Hence the allowed insertion
   positions are exactly `0..t`, `t` = length of the longest 132-avoiding prefix of `p`.
3. **Finite state (E3).** `state(p) := standardize(p[:t+1])`. Restricting to `|state| ≤ K` gives
   a finite automaton `A_K` (states + integer edge multiplicities), built by BFS.
4. **Sound EXACT subclass (E4), verified.** Walks of length `n` in `A_K` are in **bijection**
   with `B_K := { p ∈ Av(1324) : every value-prefix of p has state-length ≤ K }`, a genuine
   subset of `Av(1324)` counted without repetition (verified `|B_K,n| = #walks` for `n≤8`, and
   `#walks ≤ |Av_n|` for `n≤12`). Therefore **`gr(B_K) = ρ(A_K) ≤ gr(Av(1324))` unconditionally**.

**Certificate.** `ρ(A_K) = max over SCCs of ρ(SCC)`. I isolate the **dominant strongly-connected
component** (its walks ⊆ `A_K`'s, so a CW bound on it is still a valid lower bound), power-iterate
in **float only** to get an approximate Perron vector, rationalise to a positive integer vector
`w`, and emit the exact Collatz–Wielandt bound `λ := min_i (Mw)_i/w_i`, which satisfies
`Mw ≥ λw` entrywise **by construction** in exact `Fraction` arithmetic. Pure rational in the
load-bearing check; float only chooses `w`. This reuses the R1 CW machinery, generalised off the
companion shape to a general sparse nonnegative matrix.

**Certified values (exact rational CW, reproduced):**

| K | #states | dominant SCC | certified `λ` (exact) | float |
|---|---|---|---|---|
| 6 | 352 | 155 | `21667027/5467507` | 3.962871 |
| 8 | 4708 | 2652 | `19992608/3782129` | 5.286072 |
| 9 | 17578 | 10660 | `1804171/311442` | 5.792960 |
| **10** | **66198** | **42484** | **`8887516/1428099`** | **6.223319** |

### Claimed value (CLAIM, pending reviewer)

**`gr(Av(1324)) ≥ 8887516/1428099 = 6.223319`** (K=10), a **sound, unconditional** lower bound
with a fully reproducible exact-rational CW certificate. This **strictly improves the held floor
3.773326 → 6.223319** (nearly doubles it). It does **NOT** beat the record 10.271.

### The decisive computable question — answered: NO

The dispatch's central question — *does a sound bounded machine clear 10.271?* — is **answered
negatively**. `A_K` converges to the true `gr ≈ 11.6` only **logarithmically** in `K`
(increments 0.72, 0.60, 0.51, 0.43, … for K=6→10), and state count grows ≈×3.6 per `K`. Clearing
10.271 needs `K` well beyond 20 (billions of states) — infeasible. This confirms R1 + explorer +
Walks2025: no clean sound finite/integer machine reaches 10.271 at feasible size.

### Reshape of the H_BIG hole (intermediate-statement search) — why the min-weighted (n,r) plan was dropped

The dispatched Angle-A plan (min out-degree on the `(size n, r short values)` quotient) is
**sound but useless**, and I measured it before discarding: collapsing all sizes into a single
`r`-state gives a **near-triangular** transition matrix (only `r→r` and `r→r+1` entries, each ≈1
because the per-group minimum is dominated by the worst vertex, out-degree 1). Its `ρ` is a
**cutoff-boundary artifact** (≈8, the boundary self-loop from un-expanded top states), not a
genuine growth bound; `rho(Q_min) = rho(A_avg) = 8.0` at N=9 both reduce to the same triangular
artifact. So the min-weighted `(n,r)` quotient cannot even certify a meaningful sound bound. I
therefore **reshaped H_BIG** to the *exact* bounded-state quotient above (lossless, no
min-weighting), which is both sounder and quantitatively far better (6.22 vs an artifact). This
is intermediate-statement search: the planned hole's mechanism was wrong; the true provable one
is the exact `A_K` automaton.

## Spec concerns

None with the top-level statement (right constant, direction, threshold; limit exists by
Marcus–Tardos). **For the outliner:** the dispatch's hope that a *single finite/integer machine
clears 10.271* is now firmly refuted across three independent machines (skew-sum, min-weighted
`(n,r)` quotient, bounded-state insertion automaton) — all cap well below the record by the same
logarithmic wall. The lower-bound record needs either (i) the **Catalan-cell staircase with
rigorously rational-bounded GF-weighted entries** (the tromino sketch / Angle C-D), or (ii) a
proof of **Conjecture 8** (the `conjecture8-diagonal-lower` hedge / Angle B). This sketch's
remaining open work is exactly that GF-weighted-cell machine — a genuinely new hole, best opened
by the outliner as a fresh line rather than continuing to push `K` on an exact integer automaton.

## Promotable lemmas

**`skew_sum_closure_Av1324`** — *For permutations `a, b`: the skew sum `a ⊖ b` avoids 1324 iff
both `a` and `b` avoid 1324.* (Equivalently: `Av(1324)` is closed under skew sum; a skew sum of
1324-avoiders is 1324-avoiding.) Proved green this round in
`certificate/transfer-matrix-lower.py` (`prove_skew_sum_closure()` — exact finite rank
argument; `brute_check_skew_closure()` — exhaustive re-check to total length 7). General and
reusable (any skew-sum / skew-component construction on `Av(1324)`, e.g. the tromino sketch).
Reviewer: certify into `lemmas/`.
