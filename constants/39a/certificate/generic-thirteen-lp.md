# Certificate record — sketch `generic-thirteen-lp` (Lean + Python LP witness)

The Lean-fit generic-regime half of the $14\to13$ attack. Two artifacts:

1. **Lean sketch** `constants/39a/lean/Sketches/GenericThirteenLP.lean` — formalises the
   marked-point core of the load-bearing hole at a concrete off-center box.
2. **Python LP/Farkas witness** `constants/39a/certificate/generic-thirteen-lp.py` — finds and
   EXACTLY re-verifies the 13-piece cover (rational, no float in the load-bearing check).

## Reproduce

### Python (the LP search + exact witness re-verification)
```
cd constants/39a/certificate
python3 generic-thirteen-lp.py
```
Expected: `14-piece generic structure exact-feasible` (machinery check), then
`13-piece cover EXACT-feasible (pure Fraction, no LP solver): True`, then the
`STRUCTURAL FINDING` (40/64 corner boxes 13-feasible; single-coordinate offsets infeasible).
The load-bearing assertion is `verify_witness()` — pure `Fraction` arithmetic, NO LP solver
in the check (`scipy.linprog` is used ONLY to PROPOSE candidate centers; every reported
feasibility is re-derived exactly). The witness box is
`p* = (9/10, 1/10, 9/10, 9/10, 1/10, 1/10)`, strict-interior margin 0.0218.

### Lean (the formalised marked-point core)
```
cd constants/39a/lean
lake build Sketches.GenericThirteenLP
```
Result: `Build completed successfully (2413 jobs).` (exit 0). Warnings only — the `sorry`s on
the remaining honest holes (`CoverTarget`, `Piece`, `Generic`, `generic_cover_le_13`) plus
benign linters. `lake build Sketches.GenericThirteenLP Sketches.LassakGlue` also exit 0
(the dependent assembly sketch still builds against this file).

## `#print axioms` (run via `lake env lean` on an importing file)
```
markedStar_mem                       : [propext, Classical.choice, Quot.sound]
marked_points_covered_by_thirteen    : [propext, Classical.choice, Quot.sound]
segment_covered_by_two               : [propext, Classical.choice, Quot.sound]   -- R4
segment_subset_two                   : [propext, Classical.choice, Quot.sound]   -- R4
cubeEdge_subset                      : [propext, Classical.choice, Quot.sound]   -- R4
edges_covered_by_thirteen            : [propext, Classical.choice, Quot.sound]   -- R4 (H_GEN_EDGES)
target_star_covered_by_thirteen      : [propext, Classical.choice, Quot.sound]   -- R4
```
All **sorry-free and axiom-clean** (standard Mathlib trio only — NO `sorryAx`). These are the
genuinely-discharged sub-steps of H_GEN_τ at the witness box. **R4 closed H_GEN_EDGES**: the 12
cube edges are now covered in Lean by the SAME 13 translates (`edges_covered_by_thirteen`), and
the capstone `target_star_covered_by_thirteen` merges edges + marked points into the full target
`E ∪ V_{p*}` covered by 13 translates of `int(O_{p*})` — all at the single witness box `p*`. The
remaining theorems (`generic_cover_le_13`, `generic_regime_thirteen`) still carry `sorryAx` —
honest open holes (H_GEN_ATLAS / glue; the per-box content is now fully closed at `p*`).

## What this certifies (and what it does NOT)

CERTIFIED (this round): at the off-center box `p*`, the 14 marked points
$\{8\text{ cube vertices}\}\cup V_{p^*}$ are covered by **13** explicit rational translates of
$\operatorname{int}(O_{p^*})$ — one merge (contact point $q_{20}$ shares vertex-translate $t_5$).
So $C(\{\text{marked}\},\operatorname{int}O_{p^*})\le 13$ at $p^*$. Lean formalises the
marked-point membership; the Python certificate additionally verifies the 12 edges exactly
(`edge_covered_exact`).

NEWLY CERTIFIED (R4): **H_GEN_EDGES** — the 12 cube edges are covered IN LEAN by the same 13
translates, via the reusable primitive `segment_covered_by_two` / `segment_subset_two` (the
multi-D generalization of cached `icc_covered_by_two`: a parametrized segment vs an open polytope,
split at one rational `σ` per edge). The per-box content of H_GEN_τ is now fully Lean-certified at
`p*`: `target_star_covered_by_thirteen` gives `C(E ∪ V_{p*}, int(O_{p*})) ≤ 13` machine-checked.

NOT certified (open holes, the bound is still 14 globally):
- **H_GEN_ATLAS** — tiling the (THIN, revised) 13-feasible region by boxes via
  $Q_P=\bigcap_{v\in P}O_v$, and handing its complement to the near-1/2 sibling.
- **H_GEN_GLUE / Prymak reduction** — assembling $\max_p\le13$ and gluing to $H_3$.

## Spec concern recorded (reshapes the plan)
The planned H_GEN_ATLAS assumed the 13-region is all of $[0,1]^6\setminus N(1/2)$ (a coarse
atlas). FALSE: point-mergeability $\ne$ edge-feasible 13-cover. The merge frees a piece ONLY
where the 8 vertex-translates alone still cover all 12 edges, forcing ALL six $p_i$ off 1/2
together; single-/two-coordinate offsets have NO 13-cover; only 40/64 corner boxes do. The
generic/near-1/2 partition is NOT a simple ball around 1/2 — flagged for the outliner.
