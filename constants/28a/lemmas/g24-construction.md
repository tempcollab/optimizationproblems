# Cached certified lemma — exact G_2(4) construction + Gri Lemma-1 partition

**Certified by proof-reviewer, round 1.** Reproduced independently (not on the builder's
say-so). Any 28a sketch may import `constants/28a/certificate/g24.py` and rely on these
without re-deriving them.

## What is certified

Source: `constants/28a/certificate/g24.py`. The construction is exact (GF(16) integer
arithmetic via log/exp tables + integer bitsets; deterministic vertex order via sorted
projective points and sorted triples). No floating point enters the graph itself. The
reviewer rebuilt the graph twice (bit-identical adjacency and vertex order) and reproduced
every property below from scratch.

### `build_g24() -> (A, vertices)`
Brouwer's PG(2,16) Hermitian model: vertices = unordered triples of pairwise-orthogonal
non-isotropic projective points; adjacency iff the isotropic 15-sets `T(A)` meet in exactly
3 points. Certified properties of the returned `A` (416×416 int 0/1 adjacency):
- `|V| = 416`, `A` symmetric, zero diagonal, every degree `= 100`.
- **Strongly regular** `srg(416,100,36,20)`: the integer identity
  `A^2 = 100 I + 36 A + 20 (J − I − A)` holds exactly (verified over the integers).
- Adjacency spectrum `100^1, 20^65, (−4)^350` (eigenvalue multiplicities).
- Standard Gram `G = 96 I + 24 A − 6 J` is PSD with **exact rank 65 over Q** (verified by
  fraction-free Gaussian elimination, not float SVD).
- **Clique number ω = 5**: `max_clique_le(A,5)` true and `max_clique_le(A,4)` false
  (exhibits a 5-clique, certifies no 6-clique, by exact bitset branch-and-bound).

### `standard_partition(verts) -> (q0, B_idx, C_idx)`
Partition w.r.t. the first isotropic point `q0` (deterministic order): `B` = vertices
containing a non-isotropic point orthogonal to `q0`, `C = V \ B`. Certified:
`|B| = 96`, `|C| = 320`.

### `b_components(A, B_idx) -> [comp, ...]`
Connected components of the induced graph on `B`. Certified: **exactly 3 components of
size 32** each.

## Scope / how to use (no stronger than proved)
- These functions certify *exactly* the bulleted facts above and nothing more. In
  particular `max_clique_le` certifies ω(whole graph)=5; it does **not** by itself bound
  the clique number of an arbitrary induced subgraph (call it on the subgraph for that).
- `euclidean_rep` and `subspace_dim` in the same module use **float** SVD and are NOT
  certified here — use `exact_rank` (fraction-free, in `fresh-orthogonal-dir.py`) for any
  load-bearing rank claim. `gram_standard` / `gram_integer` are exact integer matrices.

## Reproduce
```
python3 constants/28a/certificate/g24.py     # asserts all of the above, prints "... PASS"
```
