# Bevan 2015 lower bound + recent (2025) walk method + transferable techniques

## Bevan 2015 — arXiv:1406.2890 (gr ≥ 9.81), PDF `pdfs/bevan2015.pdf`
- Predecessor of the BBEPP lower bound; same "explicit subclass + concentration" philosophy.
- Builds a subclass of Av(1324) with a "particularly regular structure" (a staircase-like
  construction whose cross-sections relate to **Łukasiewicz paths** / plane trees).
- **Theorem 1.2 (the engine):** the number of occurrences of a fixed pattern in a Łukasiewicz
  path of length n is **asymptotically normal** (and hence concentrated). Proof: cluster method
  (Goulden–Jackson / Guibas–Odlyzko correlation polynomial) + kernel method.
- Concentration ⟹ the subclass count is dominated by its typical member ⟹ growth rate
  g(λ,δ); optimise over (λ,δ) ⟹ 9.81. A crude version of the same construction (no
  concentration) already gives 9.40399 "It is rather a surprise that such a simple construction
  exhibits a growth rate as large as this." — i.e. **simple explicit constructions get
  surprisingly close**; concentration squeezes the last bit.
- Take-away for attacks: concentration of substructure statistics is what turns an explicit
  construction into a sharp lower bound; it is the reusable lemma type for any new construction.

## AERWZ 2006 — the insertion-encoding / automaton lower bound (gr ≥ 9.47)
arXiv:math/0502504 (primarily on 4231, applied to 1324). Method: the **insertion encoding**
of 1324-avoiders gives a sequence of **finite automata** accepting subclasses of Av(1324); the
growth rate of each subclass = **spectral radius (Perron root) of the automaton's transition
matrix**. A larger automaton ⟹ a larger certified subclass ⟹ a better lower bound. This is a
purely finite, reproducible computation (eigenvalue of an explicit nonnegative integer matrix).

## Recent: arXiv:2512.19462 (2025) "Pattern avoiding permutations as walks"
- Encodes pattern-avoiders as **walks in a directed graph**: building a permutation by
  successive insertion of a new maximum = traversing an edge; vertices = equivalence classes of
  intermediate states. Growth = **spectral radius of the adjacency/transfer matrix**
  (Perron–Frobenius); lower bounds on the spectral radius via the **Collatz–Wielandt formula**
  (exhibit a vector v ≥ 0 with Av ≥ r·v ⟹ spectral radius ≥ r — a finite, checkable certificate).
- Theorem 5: #{132-avoiders of length n with k short values} = (n−k+1)/(n+1)·C(n+k,n)
  (a closed form). Theorem 7: recurrence for edge counts between partition classes.
- **Conjecture 8:** the growth rate of walks in the *grouped* (quotient by #short values)
  1324-graph is a lower bound for L(1324). Computationally verified to path length 50.
- Conditional on Conj 8: **lower bound 10.418** (would beat 10.271). **NO unconditional
  improvement over 10.271** — confirms BBEPP is still the rigorous record (as of June 2026).
- KEY: the *ungrouped* walk graph (an exact subclass) gives an **unconditional** lower bound =
  its spectral radius; the conjecture is only needed for the *grouped* speed-up. So a finite
  truncation of the exact insertion-encoding graph, with a Collatz–Wielandt certificate, is a
  rigorous lower bound whose only question is whether the truncation's Perron root exceeds 10.271.

## Transferable Stanley–Wilf techniques from neighbouring constants
- **4231 (AERWZ):** a subclass of Av(4231) is in bijection with a regular language; transfer
  matrix ⟹ growth rate. Direct template for a 1324 lower bound: find a large regular/automaton
  subclass of Av(1324), compute the dominant eigenvalue.
- **1234 / monotone & layered (Regev, Bóna):** L(1234) = 9 exactly (Regev), L(monotone
  length-k) = (k−1)^2. These are SOLVED via the merge/√-superadditivity and RSK; the merge
  inequality √γ ≤ √α+√β (CJS Lemma 4) is the shared upper-bound primitive.
- **General insertion encoding (Albert–Atkinson–Vatter):** any "geometrically griddable" or
  "regular" subclass has a rational GF / finite automaton — the systematic way to manufacture
  certifiable lower bounds.

## Lean-fit assessment
The **insertion-encoding / transfer-matrix lower bound is the most Lean-fit attack on either
side**: a fixed nonnegative integer matrix M (transition matrix of a finite automaton
accepting a verified subclass of Av(1324)) plus a Collatz–Wielandt witness vector v with
Mv ≥ r·v entrywise certifies spectral radius ≥ r — a finite, exact, rational linear-algebra
check (no continuum estimate). The hard/creative step is producing an automaton subclass whose
Perron root provably exceeds 10.271 (state count may need to be large), and proving the
language is genuinely ⊆ Av(1324). Both are discrete.
