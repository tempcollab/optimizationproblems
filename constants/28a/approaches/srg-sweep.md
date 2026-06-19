# srg-sweep — a different SRG / two-distance set with embedding dim <= 62

**Attack line C** (explorer §5). Cheapest to *state*; biggest potential jump; highest
existence risk. This round it was turned from a stub into a **complete, reproducible finite
database search**. Result this round: a precisely-scoped **NEGATIVE** — no qualifying SRG
parameter set is found, and the open boundary is pinned to 207 explicit parameter rows.

## Target
Beat the verified upper bound **63**. Need a two-distance set (or SRG-derived point set)
in `R^f`, `f <= 62`, whose smaller-diameter subsets are cliques of a graph `G` with
`ceil(v / omega(G)) >= 64`.

## Mechanism (Bondarenko 2014; graph form Musin 2025; SRG sweep precedent arXiv:2005.12025)
For `srg(v,k,lambda,mu)` with adjacency eigenvalues `k, r>0, s<0` (multiplicities `1,f,g`):
- `Y = A - sI` is PSD of rank `1+f`; its columns realise the vertices as a two-distance set
  whose **affine** span has dimension `f = mult(r)` (verified: G_2(4) gives `f=65`,
  the published dimension).
- A smaller-diameter subset is exactly a **clique**, so `b >= theta(G) >= ceil(v/omega(G))`.
- Counterexample in `R^f` iff `ceil(v/omega) > f+1`. To beat 63: **`f <= 62` AND
  `ceil(v/omega) >= 64`**.

## What was FILLED this round (holes closed)
1. **`load_brouwer_srg_table()`** — now ingests Brouwer's full feasible-parameter table
   `v <= 1300` (26 sub-pages, **4538 rows**, cached in `certificate/srgtab_html/`), plus
   17 large named SRGs from `srgbig.html` (`LARGE_SRGS`). No silent cap.
2. **Exact arithmetic** — `positive_eig_multiplicity` cross-checked against the table's
   own `r^f`/`s^g` columns on **all 4231 integer-eigenvalue rows: 0 mismatches**.
   Conference (irrational-eigenvalue) rows handled via `f=g=(v-1)/2`.
3. **Per-row certifiable test** — `certifies_counterexample`: `f<=62` AND
   `ceil(v/omega_DH) >= 64`, where `omega_DH = 1 + floor(k/(-s))` is the
   Delsarte–Hoffman (ratio) clique **upper** bound. Because `omega <= omega_DH`, the
   forced parts `>= ceil(v/omega_DH)` — so this is a **sufficient, parameter-only,
   reproducible** counterexample certificate. **Result: 0 rows certify.**
4. **Residual reduction** — of the **564** rows with `f <= 62`, **357 are ruled out
   completely** by sound parameter-only arguments (see below); **207 remain open**.
5. **Infinite families** — closed-form proofs that Triangular `T(n)`, Lattice `L2(n)`, and
   Latin-square/`OA(m,t)` graphs **never** qualify (their clique number scales with `f`,
   so small `f` forces `v/omega` small). Covers all `n`, not just tabulated rows.

Run: `python3 constants/28a/certificate/srg-sweep.py` (self-contained from the cached
HTML; exit 0).

## The negative result, precisely scoped
- **Certifiable sweep is empty.** No feasible parameter set (v<=1300 + 17 big named SRGs +
  3 infinite families) satisfies `f<=62 AND ceil(v/omega_DH)>=64`.
- **357 / 564 `f<=62` rows fully ruled out:** 77 with `v<64` (cannot reach 64 parts);
  57 marked non-existent (`-`, absolute/Krein bound violations); 100 by the **exact**
  clique number of a recognised named family (`T(n)`→`n-1`, `n^2`→`n`, `OA(m,t)`→`m`)
  exceeding `need_omega`; 123 by a **provable** clique lower bound (`omega>=2` always,
  `omega>=3` when `lambda>=1`, since an edge + a common neighbour is a triangle) exceeding
  `need_omega`. All kills are conservative: verified that a genuine G_2(4)-style winner
  (true `omega=5`) at `f<=62` would survive as OPEN, never be wrongly eliminated.

## Holes that REMAIN (the open boundary — exact scope)
- **207 parameter rows** with `f<=62` where a counterexample is not arithmetically
  excluded: each would need an **explicit graph** whose true clique number is `<= need_omega`
  (ranging 3..20). They survive because the only parameter-only ω **upper** bound
  (Delsarte–Hoffman) is loose (e.g. for G_2(4) it gives `omega_DH=26` vs true `omega=5`),
  so it neither certifies nor refutes them. Settling each requires the actual graph's exact
  `omega` (via `g24.max_clique_le` once the graph is built) — a per-graph computation, many
  of these of unsettled existence (`?`). **No qualifying graph is currently known**
  (Musin 2025 confirms dims 4..63 still open; arXiv:2005.12025's SRG sweep finds nothing
  below G_2(4)'s dim 65 except sub-configurations).
- **Honest caveat on the certifiable test:** because `omega_DH` badly overestimates `omega`,
  the empty *certifiable* sweep alone does **not** close the problem — a real winner with
  small true `omega` would be missed by it. The load-bearing part of the negative is the
  **residual reduction**: the open region is exactly those 207 rows, no more.

## What would push it further
- For each of the 207 open rows that corresponds to a **known** graph, build it and run
  `g24.max_clique_le` to get exact `omega`, converting OPEN → ruled-out (or → candidate).
  The small-`f` Krein1 rows (`f=8, 22, 23, 24`) with large `v` are the most attractive:
  smallest embedding dimension. Most are sub-constituents / of `?` or `-` existence — worth
  a targeted pass next round.
- The genuinely promising structural target remains G_2(4) **sub-configurations** (lines A/B),
  not a new whole SRG: this sweep's negative is the evidence that no *new* SRG shortcuts the
  63→62 step, so effort should concentrate on `fresh-orthogonal-dir`.

## Claimed value
**No improvement claimed.** Table value to beat: upper bound **63**. This sketch's verified
output is a (reproducible) **negative search result**, not a bound — per CLAUDE.md a search
result is not written into `held`. It informs the population: rules out the "new SRG" shortcut
over a large, explicitly-scoped region and concentrates remaining risk on 207 named rows.

## Promotable lemmas
None this round. (The eigenvalue-multiplicity + Delsarte–Hoffman arithmetic is reusable but
lives as plain Python here, not yet a Lean lemma; `g24.max_clique_le` is the future Lean-fit
clique core, still a hole in the shared scaffold.)

## Self-assessment
Hole fully discharged on the *certifiable* side; the residual 207 are an honest open boundary,
not a hidden gap. The line is near-dead as a *record-breaker* (matches 30 years + the 2025
literature finding nothing), but it is now a clean, scoped negative that redirects the
population toward the sub-configuration lines.
