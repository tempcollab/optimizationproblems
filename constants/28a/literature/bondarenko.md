# Bondarenko 2014 — On Borsuk's conjecture for two-distance sets (arXiv:1305.2584, DCG 51)

PDF/txt saved under `pdfs/1305.2584.{pdf,txt}`. The origin of the whole SRG-counterexample line; answers Larman's two-distance question.

## Results
- **Thm 1 (G_2(4)).** Two-distance set `{x_1,...,x_416} ⊂ S^64 ⊂ R^65`, inner products `1/5` or `−1/15`, cannot be partitioned into 83 parts ⇒ `b(65) >= b_2(65) >= 84`. This is the `srg(416,100,36,20)` construction Jenrich–Brouwer and Gri2026 build on. `ω = 5`, `ceil(416/5)=84`.
- **Thm 2 (Fi_23).** Two-distance set of **31671** points on `S^781 ⊂ R^782`, inner products `1/10` or `−1/80`, cannot be split into 1376 parts ⇒ `b_2(782) >= 1376` (much higher dimension, much larger margin).
- **Corollaries.** Product/tensor tricks: `b_2(66n+k) >= 84n+k+1`, `b_2(783n+k) >= 1377n+k+1`. Also `b_2(781)>=1225` etc.

## Mechanism — SRG → two-distance set → Borsuk
A strongly regular graph `srg(v,k,λ,µ)` has adjacency eigenvalues `k, r>0, s<0`. The matrix `A − sI` (or a PSD affine combination) is a Gram matrix; its columns give a **two-distance representation** on a sphere in `R^f` where `f` = multiplicity of the positive eigenvalue `r`. For `G_2(4)`: `f = 65`. A subset has strictly smaller diameter **iff its vertices are pairwise adjacent (a clique)** [for the normalization where non-adjacent = max distance]. So:
> minimum #parts of smaller diameter `>= |V| / ω(Γ)` (clique cover bound), and the Borsuk number `>= ceil(v/ω)`.
The counterexample works because `ceil(v/ω) > f + 1`. For `G_2(4)`: `ceil(416/5)=84 > 66`.

## Obstruction / what's left open (the levers)
The bound is `ceil(v/ω(Γ))` vs `f+1`. To improve the *dimension* you want, for a target dim `m`, an SRG (or sub-configuration) with positive-eigenvalue multiplicity `f <= m` yet `ceil(v/ω) > m+1`. Two slack sources:
1. **Bigger ratio `v/ω`** (more points per clique). `G_2(4)` already has the extremal `ω=5`.
2. **Smaller `f`** (lower embedding dimension) via sub-configurations in coordinate subspaces (this is exactly Jenrich/Gri codim reductions) — but each dropped dimension costs points.
No SRG between `G_2(4)` (dim 65) and `Fi_23` (dim 782) is known to give a counterexample in dim <65 directly; all motion 65→64→63 is by **sub-configuration + added point** inside `G_2(4)`, not a new graph.

## Lean-fit
Same shape as Gri2026: the load-bearing fact is `ω(G_2(4))=5` (finite clique bound) plus integer-eigenvalue Gram/PSD reasoning. Continuum-free. The `Fi_23` example is far higher-dimensional and less relevant to the 63→62 frontier.
