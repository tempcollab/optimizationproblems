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

## The remaining hole — H_BIG (the real difficulty; does NOT beat the record yet)

**This round does NOT beat 10.271.** The skew-sum truncation converges to `gr(Av(1324))≈11.6`
only **logarithmically slowly**: `L=8 → 3.773`, and even `L=16` (which would need
`|Av_16(1324)|`, an enormous enumeration) reaches only `≈5.10`. No feasible `L` clears 10.271
by *this* construction. The construction is rigorous and the certificate machinery is complete
and reusable — but the *machine* is too weak.

**H_BIG (reshaped from the original H1).** Build a *higher-growth* sound transfer matrix whose
certified Perron root exceeds 10.271. The reason skew-sum caps low: it forbids *interleaving*,
which is exactly where the growth lives. The record engine (BBEPP, Bevan 9.81, AERWZ 9.47) uses
a **staircase of `Av(213)`/`Av(132)` Catalan cells**, whose transfer matrix has *GF-weighted*
(not plain-integer) entries — that is where a continuum sneaks in and why no single integer
matrix in the literature beats 10.271. Concrete next-round candidates:
- the **AERWZ insertion-encoding automaton** (genuine finite automaton, provably sound, but
  caps ~9.47 — still below record, useful as a stronger foundation);
- a **staircase of Catalan cells** with the GF-weighted entries *rigorously rationally
  lower-bounded* (each cell's GF `≥` an explicit rational at the evaluation point), turning the
  weighted matrix into an integer/rational matrix to which the Collatz–Wielandt certificate
  below applies verbatim. This is the most promising route to actually clear 10.271 and is
  squarely Lean-fit (finite matrix + rational inequalities).

The Collatz–Wielandt + companion-matrix machinery in the script is exactly what certifies any
such matrix once built — H_BIG is "find the matrix", not "certify it".

## Spec concerns

None with the top-level statement (right constant, right direction, right threshold, the limit
exists by Marcus–Tardos). The outline's *mechanism* is sound and unchanged. One honest note for
the outliner: the dispatch's hope that "a single finite machine clears 10.271" is, per the
literature and these experiments, **multi-round** — clean integer transfer matrices (skew-sum,
AERWZ insertion encoding) all cap below the record; clearing 10.271 needs the Catalan-cell
staircase with rigorously bounded GF-weighted entries (angle reshaped into H_BIG above), not a
plain integer automaton. The sketch line is the right one; it just needs the stronger machine.

## Promotable lemmas

**`skew_sum_closure_Av1324`** — *For permutations `a, b`: the skew sum `a ⊖ b` avoids 1324 iff
both `a` and `b` avoid 1324.* (Equivalently: `Av(1324)` is closed under skew sum; a skew sum of
1324-avoiders is 1324-avoiding.) Proved green this round in
`certificate/transfer-matrix-lower.py` (`prove_skew_sum_closure()` — exact finite rank
argument; `brute_check_skew_closure()` — exhaustive re-check to total length 7). General and
reusable (any skew-sum / skew-component construction on `Av(1324)`, e.g. the tromino sketch).
Reviewer: certify into `lemmas/`.
