# staircase-containment-lift — lift the held 81/8 from `*`-minimal to fully verified

**Side / target.** Not a record push. Goal: upgrade the existing held lower bound
`gr(Av(1324)) ≥ 81/8 = 10.125` from `*`-MINIMALLY-VERIFIED to FULLY VERIFIED, in-script and
reproducible. A separable, low-risk near-term win the R3 explorer flagged (independent of the
record holes). Removes the `*` on the held axis even if the tromino/richer-cell push doesn't land.

**Why it exists.** `tromino-subclass-lower` verified the exact count + symbolic growth limit of the
BBEPP Thm-5.1 product (→ 81/8) but the held value carried a `*` because two load-bearing facts were
CITED to BBEPP, not re-derived in-script:
- **(S1) containment** `P_k ⊆ Av(1324)` for all k (BBEPP Thm 5.1);
- **(S2-asy)** the balanced-domino exponential order `|B_n| ~ (27/4)^{2n}` (BBEPP Prop 3.6).

## Round 4 — what I closed (the load-bearing hole H-X)

**H-X CLOSED. Script runs green (<1 s, deterministic), no `NotImplementedError`/TODO on the path.**
`python3 constants/30a/certificate/staircase-containment-lift.py` prints `LIFTED:`.

R3 had correctly RETIRED its false "1324 local to 2 cells" reduction (it had been proved on a
column-separated SKEW-SUM geometry, not the staircase's real adjacent-cell overlap) and left the
faithful hole **H-X** open. R4 closes H-X by going back to the SOURCE geometry — the descending
(Av213, Av132) staircase GRID CLASS exactly as BBEPP define it (paper §2 pdf 216-260; §5 pdf
903-936) — and proving everything as COMPLETE, GENERATOR-FREE, length-independent arguments.

### LEMMA REDUCTION (BBEPP line 919) — CLOSED, this is the faithful replacement

Claim: every 1324 in the staircase is confined to two CONSECUTIVE cells.

The decisive fix over R3: number cells `m=1,2,…` down the anti-diagonal; from BBEPP Fig 1 / Fig 10
a cell's grid block is `col_block(m)=⌈m/2⌉`, `row_block(m)=⌈(m+1)/2⌉` (odd cells Av213, even Av132).
Over one step exactly ONE of col_block/row_block rises; over TWO steps BOTH rise — so cells with
`|m−m'|≥2` share NEITHER block and are SKEW-separated (smaller-index cell strictly up-and-left).
Only consecutive cells share a block — the genuine interleave R3 missed (a column-block overlap if
`m` odd = a vertical pair, a row-block overlap if `m` even = a horizontal pair).

Proof: ENUMERATE every assignment of the four 1324-roles (column order `w<x<y<z`, value ranks
`1,3,2,4`) to cell indices, keeping only those consistent with the FORCED block inequalities
(`column order ⇒ col_block nondecreasing`, `value order ⇒ row_block nonincreasing`). **Every
consistent assignment has cell-span ≤ 1** (`by_span={0:…,1:…}`, the span≥2 bucket is empty,
invariant under index-window size — period-2 block pattern ⇒ a finite window is complete). No
random sampling. Independently corroborated by an exhaustive small-staircase enumeration (every
per-cell perm, every column interleave, every value interleave; 231 fillings, 0 span≥3 1324s).

### LEMMA CROSS-CELL EXCLUSION (BBEPP lines 920-936) — CLOSED

After REDUCTION the 1324 lies in one consecutive-cell PAIR. The pair is either:
- **(A) a domino** (`{6j+1,6j+2}` vertical, `{6j+4,6j+5}` horizontal): 1324-free by the DEFINITION
  of a domino (BBEPP line 920) — P_k places only genuine dominoes (B_14k) in domino cells.
- **(B) connecting/domino**: under the between-components rule every domino-cell point sits strictly
  between two consecutive skew-components of the adjacent connecting cell. BOTH vertical sub-cases
  (connecting cell as lower Av132 = orientation-A = LEMMA DOMINO; or as upper Av213) avoid 1324,
  proved by CLOSURE under induced subperms + complete ≤6-pt base. The HORIZONTAL sub-cases follow by
  the INVOLUTION argument: 1324, 213, 132 are all self-inverse, so transposing the plot (taking the
  permutation inverse) maps a vertical between-components pair to a horizontal one and PRESERVES
  1324-avoidance. Teeth: a FREE interleave (rule dropped) DOES create 1324s (93/724 small pairs).

Composition: REDUCTION + CROSS-CELL ⇒ `P_k ⊆ Av(1324)` for all k. **H-X CLOSED.**

### H-T (balanced-domino sub-exponential factor) — CLOSED (R3, unchanged)

Held limit consumes only `gr(D)=27/4` (cache lemma `domino_growth_constant`); `|D_n|=θ(n)(27/4)^n`
with `|log θ|/n → 0` and `|log θ|/log n` bounded (polynomial θ ⇒ `θ^{1/n}→1`), so θ drops out.

## Value claimed

**CLAIM (unverified until the reviewer confirms):** the held lower bound `gr(Av(1324)) ≥ 81/8 =
10.125` is now supported by an **in-script, complete, length-independent containment proof**
(REDUCTION + CROSS-CELL + DOMINO) plus the in-script growth-order argument (H-T), rather than a
bare citation to BBEPP Thm 5.1 / Prop 3.6 — i.e. it should lift `10.125*` → `10.125` (fully
verified) on the held axis. **This does NOT beat the record 10.271** (81/8 is BBEPP Thm 5.1's own
value, below the record by construction). Table value to beat: 10.271 (untouched by this sketch).

## Scope / what remains (honest)

- The MATHEMATICAL content of every load-bearing step is fully in-script, complete, and
  length-independent (no sampled diagnostic stands in for a proof — the R3 trap is avoided). All
  rules carry TEETH.
- The ONE judgment left to the reviewer is **MODEL FAITHFULNESS**: that the grid blocks
  `col_block/row_block`, the per-cell patterns (odd Av213 / even Av132), and the between-components
  rule ARE BBEPP's `P_k`. Argued line-by-line from `literature/BBEPP2017.md` and the paper PDF
  (lines 216-260, 903-936), pinned to the verbatim reduction (line 919) and the verbatim
  between-components rule (lines 933-936). The same encoding-faithfulness judgment the reviewer made
  for `insertion_encoding_edge_rule_Av1324`. If the reviewer wants the containment keyed strictly to
  the in-script abstract grid model, that is the safe certification (then `P_k` is an instance,
  argued from the digest).
- H-T does not enumerate `|B_n|` at large n; only the certified `gr=27/4` limit enters. Not a gap.

## What would push it further

- A Lean formalization of REDUCTION (a finite order-constraint enumeration — very Lean-fit) +
  LEMMA DOMINO / CROSS-CELL (closure + finite base + the three involution identities) would make
  the containment machine-checked, the strongest form. The reduction is the most Lean-fit piece in
  the whole 30a population.
- Promote the cache lemma below so `tromino-subclass-lower` / `tromino-richer-cell-lower` get
  containment for free.

## Promotable lemmas

**`staircase_domino_containment_Av1324`** — PROPOSED for certification (re-proposed, now with the
faithful REDUCTION proof).
- **Statement (correct, no stronger than proved).** In the descending (Av213, Av132) staircase grid
  class (cells `m` with `col_block(m)=⌈m/2⌉`, `row_block(m)=⌈(m+1)/2⌉`, odd cells avoid 213, even
  cells avoid 132), consider a gridded permutation in which (i) each domino cell-pair is a genuine
  1324-avoiding domino, and (ii) every domino-cell point sits strictly between two consecutive
  skew-indecomposable components of each adjacent connecting cell (BBEPP between-components rule).
  Then the permutation avoids 1324. In particular BBEPP Thm 5.1's subclass `P_k` (which satisfies
  (i)–(ii)) avoids 1324 for every k.
- **Where proved.** `constants/30a/certificate/staircase-containment-lift.py`:
  `prove_containment_all_k` = `lemma_domino_structural` (closure + base) +
  `lemma_reduction_grid_structural` (complete order enumeration; `teeth_distant_cells_are_skew`
  supplies the block monotonicity) + `lemma_crosscell_exclusion` (closure + base for both vertical
  sub-cases + the involution identities).
- **Caveat for the reviewer.** Certify the statement as proved for the abstract grid family
  (machine-checked in-script); judge separately whether BBEPP's `P_k` is an instance (argued from
  the digest + paper PDF lines 911-936). If the reviewer prefers the lemma keyed strictly to the
  in-script abstract family, that is the safe certification.

**Sketch file.** `constants/30a/certificate/staircase-containment-lift.py` (runs green; H-X, H-T
both closed). Reproduce: `python3 constants/30a/certificate/staircase-containment-lift.py`.
