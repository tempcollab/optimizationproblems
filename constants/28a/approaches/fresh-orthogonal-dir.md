# fresh-orthogonal-dir — a 4th codimension direction inside G_2(4)

**Attack line A** (explorer §5). Closest to the proven 65→64→63 machinery.

## Target
A `>= 316`-point sub-configuration `S` of `G_2(4)` whose Euclidean rep lives in a
**62-dim** subspace, with `omega(S) <= 5` so `ceil(|S|/5) >= 64 > 63`.

## Mechanism
The 65→64→63 drops came from integer vectors orthogonal (in the Gram metric) to
large sub-configurations: Jenrich's `p` (B2−B3) drops `C ∪ B1` to 64; his `q`
(2·B1−B2−B3) drops `C` to exactly 63. We seek a vector `r` dropping a *different*
≥316-point subset one more dimension to 62.

## Round 1 — what was closed

**Holes 1 & 2 (build + partition) — CLOSED, exact.** `g24.build_g24` is now a real
construction: Brouwer's PG(2,16) Hermitian model (vertices = orthogonal triples of
non-isotropic projective points; adjacency iff the isotropic 15-sets `T(A)` meet in 3
points). `python3 g24.py` asserts, exactly: srg(416,100,36,20), eigenvalues 100/20/−4
(mult 1/65/350), Gram `96I+24A−6J` rank 65, **ω=5** (exhibits a K5, certifies no K6),
standard partition `|B|=96` (3 components of 32), `|C|=320`. All exact GF(16)/integer
arithmetic; deterministic. (This is the shared Lean-fit scaffold — see Promotable.)

**Hole 3 (load-bearing) — RESHAPED to its exact form, structured family REFUTED
exactly.** The skeleton's vague "find an integer vector `r`" is replaced by the
decidable statement it actually needs. Since `colspace(Gram) = E` (the 65-dim
eigenspace of `A` for eigenvalue 20), for any vertex subset `T`:

> `embedding-dim(T) = rank(Gram[T,T]) = 65 − dim(E ∩ span{e_q : q ∈ T^c})`,
> so `embedding-dim(T) <= 62 ⇔ dim(E ∩ span(e_{T^c})) >= 3`.

A valid `R^62` set needs `|T| >= 316` (so `|T^c| <= 100`), with `dim(E ∩ span(e_{T^c}))
>= 3` and `ω(T) <= 5`. For the standard partition (`T^c = B`, `|B|=96`) this dimension
is **exactly 2** — precisely Gri's codim-2 `span(S1,S2,S3)`, and exactly why `C` lands
at 63 not 62. The "fresh direction" is a 3rd independent vector of `E` supported on
`<= 100` coordinates.

The structured family — `Q = B(q0) ∪ (second B-set)`, the sketch's stated "second
isotropic point" evasion — is searched **exactly** and refuted:

- The intersection `C(q) ∩ C(q')` of any two isotropic C-sets is **exactly 245** points
  (all 2080 pairs identical by symmetry) — far below 316. The stated evasion provably
  cannot reach the count.
- Every union `B(q) ∪ B(q')` has size ≥ 111 (`|T| <= 305 < 316`). The **smallest** `Q`
  with `cap_dim(E,Q) >= 3` obtainable from a second B-structure has `|Q| = 146`, giving
  a dim-62 subset of **exactly 270** points (exact integer rank 62, ω≤5) — `ceil(270/5)
  = 54 << 64`. **Deficit: 46 points.**
- Adding up to 4 arbitrary coordinates to a single B-set never raises `cap_dim` above 2.
- 2000 random 100-coordinate sets `Q`: **none** reach `cap_dim >= 3`.

## Holes remaining
- **`search_codim4_vector_general` (OPEN, the one real hole left).** Does *any*
  `<=100`-coordinate set `Q` give `dim(E ∩ span(e_Q)) >= 3` (⇒ a `>=316`-vertex subset
  at embedding-dim `<= 62`)? Exhaustive search over `C(416,100)` is infeasible; only the
  symmetry-defined family is refuted this round. **Blocker:** need either an algebraic
  non-existence proof from the structure of `E ∩ span(e_Q)` (the eigenspace meets a
  100-coordinate window in dim 0 generically; ≥3 demands a very special `Q`), or a
  smarter exact search over a *complete* candidate family. The structured evidence
  (3rd direction costs ≥146 vertices; 270 is the structured ceiling) strongly suggests
  **no** such `Q` exists with the count — i.e. line A is most likely a genuine wall —
  but that is a conjecture, not yet certified.

## Claim
**NO improvement.** Best *certified* dim-62 subset = **270 points** (need ≥316;
`ceil(270/5)=54 < 64`). Upper bound stays **63** (Gri2026). The structured
fresh-direction family is refuted exactly; the general existence question is the open
hole. Per CLAUDE.md nothing is written into `constants/` as a bound.

## What would push it
Either (a) settle `search_codim4_vector_general` negatively with an algebraic argument
(turning line A into a clean "no fresh direction" obstruction theorem — high value even
as a negative), or (b) find a `Q` with `|Q|<=100`, `cap_dim>=3` and the surviving `T`
keeping `ω<=5` outside the symmetry-defined family. The exact evidence leans hard toward
(a). If (a) lands, it also informs the outliner that line A (and by inheritance the
gri-augment/mixed lines that fight the same no-spare-direction obstruction) needs a
structurally different point set, not a deeper search inside `G_2(4)`'s C-orbit.

## Promotable lemmas
- **`g24.build_g24` + `g24.standard_partition` + `g24.b_components`** — the exact
  G_2(4) construction and Gri's Lemma-1 partition, proved green this round (verified by
  `g24.py.__main__`: srg(416,100,36,20), ω=5, |B|=96/3×32, |C|=320). Reusable by every
  28a sketch (srg-sweep, gri-augment, mixed-construction all need the same graph). This
  is the shared Lean-fit certificate core the outliner flagged. Proposed for `lemmas/`.

## Self-assessment
The principled line held up: the exact reformulation (eigenspace ∩ coordinate-window)
is the right intermediate statement, and the structured search closes cleanly with an
exact 270-point ceiling (deficit 46). One honest open hole remains (general `Q`
existence), with strong-but-uncertified evidence it is a wall. Medium feasibility, high
informativeness — the round produced a verified scaffold and an exact negative, not a
bound.
