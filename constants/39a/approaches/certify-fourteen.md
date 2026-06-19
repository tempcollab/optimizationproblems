# Sketch D — certify-fourteen

**Goal (NOT a record-break):** a machine-checked Lean proof of the *existing* bound
$H_3 \le 14$ (Prymak 2023). This does **not** beat the verified record — it is the Lean-infrastructure
de-risk for the record-break sketches A (`special-case-p-half`) and C (`larger-covering-piece`):
it gives $H_3$ a genuine Lean definition and proves the finite covering primitives A and C reuse.

## Round 1 — what was built (Lake bootstrapped; sorry-free core landed)

The Lake project `constants/39a/lean/` is bootstrapped (first Lean sketch of the run):
- toolchain pinned `leanprover/lean4:v4.31.0`; Mathlib pinned to the `v4.31.0` rev in
  `lake-manifest.json`; `lake exe cache get` hits the cache; `lake build` is green (exit 0).
- `.lake/` (7.3 GB) is gitignored; only the pinned `lean-toolchain`, `lakefile.toml`,
  `lake-manifest.json`, `H3.lean`, and `Sketches/CertifyFourteen.lean` are tracked.

**Closed this round (sorry-free, axiom-clean — `#print axioms` = `[propext, Classical.choice, Quot.sound]`):**
- **`H3` (the registry definition) — replaces the bound-smuggling `axiom H3`.** Now a genuine
  `noncomputable def`: `H3 = sInf { N | ∀ K, IsConvexBody3 K → IsCoveredBy N K (interior K) }`,
  with `IsConvexBody3 K := Convex ℝ K ∧ IsCompact K ∧ (interior K).Nonempty` over
  `ℝ³ = (Fin 3 → ℝ)`, and `IsCoveredBy N K L := ∃ t : Fin N → V, K ⊆ ⋃ i, (t i +ᵥ L)`. The
  definition contains **no** reference to the value 14. (Resolves the reviewer's critical caveat.)
- **`IsCoveredBy.mono_left`** — a cover of `K` restricts to any subset `K' ⊆ K`.
- **`IsCoveredBy.union`** — `m` translates covering `A` and `n` covering `B` give `m+n` covering
  `A ∪ B` (via `Fin.append`). This is the 8-vertex + 6-face = 14 assembly bookkeeping A/C need.
- **`coveringNumber_mono_left`** — monotonicity of `coveringNumber` in the covered set
  (`Nat.sInf_mem` + `Nat.sInf_le`).
- **`icc_covered_by_two`** — the 1-D interval primitive: `Icc a b` with `b ≤ a + 2L` is covered by
  two translates of `Icc 0 L` placed at `a` and `b-L` (explicit witness, no LP solver). This is
  exactly Prymak's edge-coverage LP in dimension one (the cube 1-skeleton edges are 1-D); the
  endpoint placement is the rational feasibility witness A and C reuse.

## Holes that remain (explicit `sorry` — honest, not smuggled)

The only `sorryAx` in the whole file is on `H3_le_14` itself, so no completed result depends on it.
- **D1** affine-normalization reduction to the cube-skeleton problem (Prymak Lemma 2.2).
- **D2** open→closed discretization $Q_P$ (Prymak Lemma 2.4 / Cor 2.5).
- **D3 (Lean-fit core)** per-box rational LP feasibility ⇒ local count ≤ 14 via multi-D Farkas
  (Prymak Prop 2.6). `icc_covered_by_two` is the 1-D seed; the full step needs the d-D polytope
  membership / Farkas certificate checker.
- **D4 (real obstacle)** a Lean-checkable box atlas compressing Prymak's 4.66M boxes.
- **D5** assemble ⇒ `H3 ≤ 14` (`theorem H3_le_14`, the lone open hole).

**Blocker on each:** D1/D2 require formalizing the minimal-volume-parallelotope normalization and
the 64-vertex intersection $Q_P$ over `ConvexBody`/affine maps — substantial Mathlib convex-geometry
work. D3 needs a general rational-Farkas membership primitive (the natural next builder step, generalizing
`icc_covered_by_two` to $\mathbb{R}^d$). D4 is the genuine scale obstacle (4.66M boxes is not
Lean-replayable as-is) — a record-break in A/C would sidestep it with a much smaller certificate.

## Claimed value
**No bound claimed.** D by construction cannot beat the verified $H_3 \le 14$ (table = 14, our
verified `held` unchanged). What is *verified* this round is Lean infrastructure, not a bound:
the genuine $H_3$ definition + four axiom-clean covering primitives.

## Spec concerns
- The registry definition uses `interior K` (Mathlib `interior`) for "translates of the interior",
  matching `[ABP2024-def-Hn]`. `IsConvexBody3` requires nonempty interior (= genuinely 3-D body),
  the standard meaning of "3-dimensional convex body". Reviewer should sanity-check this is the
  intended registry def (it is the faithful reading of the ABP2024 quote).
- `coveringNumber`/`H3` use `sInf` on ℕ, so they are `0` if no finite cover exists; for `H3` this is
  vacuous-safe because Prymak guarantees a finite (≤14) cover for every body, but the `def` does not
  itself assert finiteness — that is exactly what `H3_le_14` (the hole) will establish.

## Promotable lemmas
The four sorry-free, axiom-clean lemmas in `Sketches/CertifyFourteen.lean` are reusable across
sketches A and C and are candidates for `constants/39a/lemmas/`:
- `IsCoveredBy` (def), `coveringNumber` (def), `IsConvexBody3` (def), `H3` (def) — the shared vocabulary.
- `IsCoveredBy.mono_left` : `IsCoveredBy N K L → K' ⊆ K → IsCoveredBy N K' L`.
- `IsCoveredBy.union` : `IsCoveredBy m A L → IsCoveredBy n B L → IsCoveredBy (m+n) (A ∪ B) L`.
- `coveringNumber_mono_left` : `IsCoveredBy N K L → K' ⊆ K → coveringNumber K' L ≤ coveringNumber K L`.
- `icc_covered_by_two` : `0 ≤ L → a ≤ b → b ≤ a + 2*L → IsCoveredBy 2 (Icc a b) (Icc 0 L)`.
All proved in `Sketches/CertifyFourteen.lean`; reviewer to certify before admitting to `lemmas/`.
(They currently live in the `H3.CertifyFourteen` namespace; the reviewer may want them in a shared
namespace when promoting.)
