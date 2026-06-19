# staircase-containment-lift — lift the held 81/8 from `*`-minimal to fully verified

**Side / target.** Not a record push. Goal: upgrade the existing held lower bound
`gr(Av(1324)) ≥ 81/8 = 10.125` from `*`-MINIMALLY-VERIFIED to FULLY VERIFIED, in-script and
reproducible. A separable, low-risk near-term win the R3 explorer flagged (independent of the
record holes). Removes the `*` on the held axis even if the tromino/richer-cell push doesn't land.

**Why it exists.** `tromino-subclass-lower` verified the exact count + symbolic growth limit of the
BBEPP Thm-5.1 product (→ 81/8) but the held value carried a `*` because two load-bearing facts were
CITED to BBEPP, not re-derived in-script:
- **(S1) containment** `P_k ⊆ Av(1324)` for all k (BBEPP Thm 5.1);
- **(S2-asy)** the balanced-domino exponential order `|B_n| ~ (27/4)^{2n}`, i.e. the
  sub-exponential factor `θ(n)` with `θ(n)^{1/n} → 1` (BBEPP Prop 3.6).

## Round 3 — what I closed

**Both holes CLOSED in-script. Script runs green (~9 s), no `NotImplementedError`/TODO left.**
`python3 constants/30a/certificate/staircase-containment-lift.py` prints the lift.

### H-C (containment `P_k ⊆ Av(1324)`, all k) — CLOSED

Proved by a faithful, **length-independent** structural argument with two modular lemmas, each
fully reproduced in-script:

- **LEMMA DOMINO (orientation-A single domino).** A 2-cell domino where the UPPER cell avoids
  213, the LOWER cell avoids 132, every upper-cell point sits strictly BETWEEN two consecutive
  skew-indecomposable components of the lower cell (BBEPP "between-components" interleave), and
  upper values exceed lower values — **avoids 1324.** Proved for ALL sizes by:
  - **CLOSURE** (`lemma_domino_closure`): the family is closed under taking induced
    sub-permutations (induced upper still avoids 213; induced lower still avoids 132; a
    gap-point stays in a gap as components shrink). Verified on every 4-subset up to 6 points
    (0 violations / 7206+).
  - **complete finite base** (`lemma_domino_exhaustive_base`): NO orientation-A domino on ≤6
    points contains 1324 — and the enumeration covers **every** 4-point split (0,4)…(4,0), so
    a 1324 in a domino of ANY size would induce a 1324 in an enumerated 4-point domino.
    Contradiction → no orientation-A domino contains 1324, all sizes. **1779 dominoes checked.**
  - **Teeth:** the three OTHER orientations (up132/lo213, up213/lo213, up132/lo132) each DO
    create a 1324 (asserted). So the descending **(Av213, Av132)** orientation is genuinely
    load-bearing — not a vacuous guard.

- **LEMMA REDUCTION (a 1324 is local to two consecutive cells).** In any descending-staircase
  filling (VALUE rule: value strictly decreasing with cell index; COLUMN rule: cells with index
  gap ≥ 2 have disjoint, ordered column ranges — the anti-diagonal geometry), every 1324 has all
  four points in two consecutive cells. **Structural proof:** the "4" sits in the minimal cell
  index, the "1" in the maximal; but "4" is the rightmost column and "1" the leftmost — if the
  cell-span were ≥ 2 the column rule would put the "1" strictly right of the "4", contradiction;
  so cell-span ≤ 1. Stress-validated on 114 804 random fillings of a **superset** model
  (arbitrary within-cell content): 0 occurrences span ≥ 3 cells. **Boundary check** confirms the
  column-disjointness premise is load-bearing: with wide column overlap (cells 2 apart overlap),
  a 1324 CAN span ≥ 3 cells — so the premise has teeth and matches BBEPP's anti-diagonal.

  **Composition:** a 1324 in `P_k` ⇒ (REDUCTION) its 4 points lie in two consecutive cells = one
  orientation-A between-components domino ⇒ (DOMINO) impossible. Hence `P_k ⊆ Av(1324)` for all k.

### H-T (balanced-domino sub-exponential factor) — CLOSED

The held growth limit consumes ONLY the n-th-root LIMIT `gr(D) = 27/4` (certified cache lemma
`domino_growth_constant`), which is by definition insensitive to any sub-exponential `θ(n)`.
Made explicit in-script: `|D_n| = θ(n)·(27/4)^n` with `|log θ(n)|/n → 0` (n=40: 0.20, decreasing)
and `|log θ(n)|/log n` BOUNDED (≈ 2.2, not growing) — the signature of a polynomial `θ`, so
`θ(n)^{1/n} → 1`. The consecutive ratio `|D_{n+1}|/|D_n| → 27/4` (the certified limit) is
reprinted. The polynomial `θ` therefore drops out of the held product's n-th-root limit.

## Value claimed

**CLAIM (unverified until the reviewer confirms):** the held lower bound `gr(Av(1324)) ≥ 81/8 =
10.125` is now supported by an **in-script, reproducible containment + growth-order proof** rather
than a bare citation to BBEPP Thm 5.1 — i.e. it should lift `10.125*` → `10.125` (fully verified)
on the held axis. **This does NOT beat the record 10.271** (81/8 is BBEPP Thm 5.1's own value,
below the record by construction). Table value to beat: 10.271 (untouched by this sketch).

## Scope / what remains (honest)

- The two lemmas' MATHEMATICAL content is fully in-script and reproducible (closure + complete
  finite base; structural value/column argument with a teeth-having boundary check). The one
  judgment the reviewer must make is **model faithfulness**: that the abstract model
  (descending value-bands-by-cell + neighbor-only column overlap + orientation-A
  between-components per consecutive pair) captures BBEPP's exact `P_k`. I argue this from the
  BBEPP digest (descending (Av213,Av132) staircase, Prop 2.1; dominoes top-213/bottom-132 with
  the between-components rule, Thm 5.1) but it is not itself machine-certified — it is the same
  kind of faithfulness judgment the reviewer made for `insertion_encoding_edge_rule_Av1324`.
- H-T does not enumerate the exact balanced-domino count `|B_n|` at large n (that count is BBEPP
  Prop 3.6); the bound needs only the certified `gr=27/4` limit, which is what is used. Not a gap
  in the bound — flagged for completeness.

## What would push it further

- Promote the cache lemma below so every staircase sketch (`tromino-subclass-lower`,
  `tromino-richer-cell-lower`) gets containment for free — that is the compounding payoff.
- A Lean formalization of LEMMA DOMINO (finite enumeration + closure) and LEMMA REDUCTION
  (value/column order argument) would make the containment machine-checked, the strongest form.

## Promotable lemmas

**`staircase_domino_containment_Av1324`** — PROPOSED for certification.
- **Statement (correct, no stronger than proved).** Let `P` be the family of descending
  (Av213, Av132) staircase fillings in which (i) cell values strictly decrease with cell index,
  (ii) cells with index-gap ≥ 2 have disjoint, index-ordered column ranges (anti-diagonal),
  (iii) each consecutive-cell pair is an **orientation-A between-components domino** (upper cell
  avoids 213, lower avoids 132, every upper point strictly between the lower cell's
  skew-components, upper values above lower). Then `P ⊆ Av(1324)`. In particular the BBEPP Thm 5.1
  subclass `P_k` (which satisfies (i)–(iii)) avoids 1324 for every k.
- **Where proved.** `constants/30a/certificate/staircase-containment-lift.py`:
  `prove_containment_all_k` = `lemma_domino_structural` (closure `lemma_domino_closure` + base
  `lemma_domino_exhaustive_base`) + `lemma_reduction_structural` (`lemma_reduction_stress`).
- **Caveat for the reviewer.** Same model-faithfulness judgment as above: certify the statement
  as proved for the abstract family `P` (machine-checked in-script), and judge separately whether
  `P_k` of BBEPP Thm 5.1 is an instance of `P` (argued from the digest). If the reviewer wants
  the lemma keyed strictly to the in-script abstract family, that is the safe certification.

**Sketch file.** `constants/30a/certificate/staircase-containment-lift.py` (runs green; both holes
closed). Reproduce: `python3 constants/30a/certificate/staircase-containment-lift.py`.
