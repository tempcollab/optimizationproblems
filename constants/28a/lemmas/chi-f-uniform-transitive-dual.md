# Cached certified lemma — uniform fractional-clique-cover dual (chi_f for vertex-transitive G)

**Certified by proof-reviewer, round 4.** Re-derived independently (not on the builder's
say-so). Proposed by sketches `musin-edge-edit` and `theta-cover-dual`; both fire on it.

## What is certified

Let `G` be a finite graph on `n` vertices with clique number `omega(G)`, used as the
**smaller-distance graph** of a two-distance set (so a Borsuk part of smaller diameter is a
**clique** of `G`, and the Borsuk part count is the clique-cover number `theta(G) = chi(Gbar)`,
`Gbar` = complement).

### Lower bound (fully elementary — Lean-fit, the load-bearing half)
The uniform weighting `w_v = 1/omega(G)` is a feasible fractional-clique-cover dual: for every
**clique** `S` of `G` (= independent set of `Gbar`), `sum_{v in S} w_v = |S|/omega(G) <= 1`
since `|S| <= omega(G)`. Hence

    theta(G)  >=  chi_f(G)  >=  sum_v w_v  =  n / omega(G).

This is a rigorous LOWER bound on the Borsuk part count, with a finite rational certificate
(one weight `1/omega` plus the exact clique number). No LP solver, no floating point.

### Exactness for vertex-transitive G (cited)
When `G` is **vertex-transitive**, `chi_f(G) = n / omega(G)` exactly (the uniform dual is
optimal by symmetry-averaging; equivalently `chi_f(H) = |V|/alpha(H)` for vertex-transitive
`H` applied to `H = Gbar`, with `alpha(Gbar) = omega(G)`). Source: Scheinerman & Ullman,
*Fractional Graph Theory* (2011), Prop. 3.1.1 (`chi_f(H) = |V(H)|/alpha(H)` for
vertex-transitive `H`). The reviewer confirmed the citation states exactly this and that the
alpha/omega convention is handled correctly (the bound is on `theta(G) = chi(Gbar)`, and
`alpha(Gbar) = omega(G)`).

## Reviewer's independent re-derivation
- Re-derived the convention chain `theta(G) = chi(Gbar) >= chi_f(Gbar) = n/alpha(Gbar) =
  n/omega(G)` from scratch; the builder's statement is correct and **no stronger than proved**
  (it is a lower bound; exactness is only claimed under vertex-transitivity).
- Independent max-clique (Bron–Kerbosch) on `T(6) = J(6,2)`: `omega = 5`, so
  `chi_f = 15/5 = 3` — matches.
- Dual feasibility `|S|/omega <= 1` is immediate and checked.

## Scope / caveats
- The LOWER bound `theta(G) >= n/omega(G)` holds for ANY graph (no transitivity needed); only
  the *equality* `chi_f(G) = n/omega(G)` needs vertex-transitivity.
- For **non-vertex-transitive** `G` the uniform dual is generally NOT optimal and `chi_f` can
  strictly exceed `n/omega`; this lemma certifies only `theta >= n/omega`, not equality, there.

## Source
`constants/28a/certificate/musin-edge-edit.py::fractional_part_lower_bound_dual` (+
`exact_omega`), self-tested on `T(6)`. Sorry/axiom-clean (no Lean yet; the Python certificate
is the elementary feasibility argument above).
