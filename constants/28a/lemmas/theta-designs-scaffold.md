# Cached certified scaffold — Steiner / Witt / Cameron design constructors

**Certified by proof-reviewer, round 4.** Reproduced independently (not on the builder's
say-so). Any 28a sketch may import `constants/28a/certificate/theta_designs.py` and rely on
these constructors without re-deriving them. Analogous to the cached `g24.py` scaffold.

## What is certified

Source: `constants/28a/certificate/theta_designs.py`. All exact integer / GF(2) arithmetic
(no floating point). Each constructor self-checks its defining incidence property at runtime.

### `bose_sts(t) -> (n, blocks)`
Bose construction of a Steiner triple system `S(2,3,n)`, `n = 6t+3`. Returns sorted 3-tuples;
runtime assertion verifies every pair lies in exactly one block (a genuine `S(2,3,n)`).
Reviewer reproduced the pair-cover property on `S(2,3,9)` and `S(2,3,15)`.

### `golay24() -> [24,12] extended binary Golay generator (GF(2))`
Bordered QR(11) circulant model. Certified via the weight enumerator
`1 + 759 x^8 + 2576 x^12 + 759 x^16 + x^24` (asserted at runtime over all 4096 codewords).

### `witt_S5_8_24()` / `witt_S3_6_22()`
759 octads = weight-8 Golay codewords = blocks of `S(5,8,24)`; deleting two points gives the
77 blocks of `S(3,6,22)` (runtime assertion: every 3-subset of the 22-set in exactly one
block, 1540 triples). Reviewer reproduced both.

### `cameron_graph() -> (A, pairs)`  — the load-bearing one
Cameron graph on 231 pairs of a 22-set; two pairs adjacent iff disjoint and their 4-union
lies in a block of `S(3,6,22)`. **Reviewer rebuilt it and independently verified the strongly
regular parameters `srg(231,30,9,3)`** (regular degree 30; adjacent pairs share exactly
`lambda = 9` common neighbours; non-adjacent share `mu = 3`) and the **clique number
`omega(A) = 7`** by an independent Bron–Kerbosch (matches Brouwer's table). M22.2-transitive
hence vertex-transitive.

## Scope / caveats
- These are CONSTRUCTORS of exact combinatorial objects, not bounds. They produce the
  vertex-transitive two-distance candidate graphs the sketches test; the Borsuk firing
  decision is made elsewhere.
- The greedy `alpha` lower bound used in `theta-cover-dual::resolve_cameron` (alpha >= 17) is a
  LOWER bound only (sufficient for non-firing: `17 > need_omega(231) = 3`); it is NOT the exact
  independence number and must not be cited as exact.

## Source
`constants/28a/certificate/theta_designs.py`. Sorry/axiom-clean exact integer construction;
reproduced independently by the reviewer (Cameron SRG parameters + `omega = 7`).
