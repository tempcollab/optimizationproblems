# Digest: Ma & Tang, "Largest Sidon subsets in weak Sidon sets" (arXiv:2602.23282, Feb 2026)

Source of the current C_5b record: lower 9/17 ≈ 0.5294, upper 4/7 ≈ 0.5714.
Erdős problem #757.

## Definitions
- **(4,5)-set** A ⊂ ℝ: every 4-element subset determines ≥ 5 distinct pairwise (absolute)
  differences (out of 6). Equivalently a "weak Sidon set": all pairwise sums x+y with x<y
  are distinct.
- **Sidon set** S: all pairwise sums x+y with x ≤ y distinct (stronger — includes x=y).
- h(A) := size of largest Sidon subset of A.
- f(n) := min{ h(A) : A a (4,5)-set, |A| = n }.
- **C_5b = c\*** is the largest c with h(A) ≥ c·|A| for every (4,5)-set A.

## Key characterization (Theorem 1.5) — load-bearing for the upper bound
c\* = lim_{n→∞} f(n)/n = **inf_{n≥1} f(n)/n**.
CONSEQUENCE: a SINGLE finite (4,5)-set A with h(A)/|A| = r gives the rigorous bound
c\* ≤ r. No blow-up / tensor / asymptotic argument needed. (This is what makes the
upper-bound side a clean finite gadget problem.)

## Hypergraph reformulation (Lemmas 2.3–2.4)
- **A.P.-hypergraph H(A):** 3-uniform, vertex set A, edges = 3-term APs {x−d, x, x+d} ⊆ A.
- **Lemma 2.3:** for a weak Sidon set A and S ⊆ A: S is Sidon ⟺ S contains no 3-term AP.
  Hence h(A) = α(H(A)) (independence number). [Verified concretely: {0,2,4} non-Sidon
  via 0+4=2+2; {0,1,3} Sidon.]
- H(A) for a (4,5)-set is **linear** (two edges meet in ≤1 vertex) and **F_7-free**
  (no specific 7-vertex config).
- **Lemma 2.4:** m_H ≤ n_H − 2 (edge count ≤ vertices − 2). Proof: midpoint map
  edge ↦ x is injective (weak Sidon) and misses min A, max A.

## Lower bound 9/17 (the harder side to improve)
Uses Henning–Yeo transversal bound for 3-uniform linear F_7-free hypergraphs:
  17·τ(H) ≤ 5·n_H + 3·m_H.
With m_H ≤ n_H − 2: 17τ ≤ 8 n_H, so τ ≤ (8/17)n, giving α = n − τ ≥ (9/17)n.
So h(A) ≥ (9/17)|A|. NOT a finite case analysis — it invokes a general extremal theorem.
To push: sharpen Henning–Yeo for this restricted class, or improve m ≤ n−2.

## Upper bound 4/7 (the softer side — Lean-fit gadget search)
Explicit 14-element (4,5)-set found by AI-assisted search:
  A_base = {0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056} ⊂ ℤ.
Verified (exhaustive): it IS a (4,5)-set and its largest Sidon subset has size exactly 8
(witness {0,136,200,243,246,298,323,528}). Hence f(14) ≤ 8 and c\* ≤ 8/14 = 4/7.
[Independently reproduced in Python: (4,5)-set ✓, max Sidon subset = 8 ✓.]
No optimality claim — authors note only that the search was AI-assisted.

## Prior bounds (context)
- [GL95] Gyárfás–Lehel: 1/2 + 1/(141·76) ≤ c\* ≤ 3/5. Reduced to a 3-uniform hypergraph
  extremal problem (the origin of the H(A) viewpoint).
- [MT26] improved both ends to 9/17 ≤ c\* ≤ 4/7.

## Where the slack is
- UPPER (soft, Lean-fit): the 4/7 gadget is a 14-point set, AI-found, no optimality claim.
  A better finite (4,5)-set with smaller h/|A| (e.g. 21 pts with h ≤ 11 → 11/21 ≈ 0.5238,
  or 28 → 15 → 0.5357) STRICTLY beats 4/7. The whole improvement is a finite search +
  a finite certificate (decidable (4,5)-check + decidable "no Sidon (m+1)-subset").
- LOWER (hard): improving 9/17 means a better extremal-hypergraph inequality.

## Verification recipe for an upper-bound gadget A (size N, claimed h(A) ≤ m, m/N < 4/7)
1. (4,5)-set: for every 4-subset, |{|x−y|}| ≥ 5. Finite enumeration over C(N,4).
2. h(A) ≤ m: every (m+1)-subset of A contains a 3-term AP — equivalently the 3-AP
   hypergraph H(A) has independence number ≤ m. Provide both an explicit max
   independent set (lower witness) and a transversal/covering certificate or full
   enumeration (upper). Both decidable; Lean via `decide` on `Finset ℤ` or an
   explicit certificate.
