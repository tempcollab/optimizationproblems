# c7-4-orbit-restricted-search-113

**Angle:** find an independent set of size ≥ 113 in C_7^⊠4 (2401 vertices = Z_7^4) by
exploiting orbit structure — unions of small Z_7 orbits (cyclic coset structure) + local
repair off the orbit lattice — rather than a plain full-graph MIS (that is the sibling
`c7-4-improvement-113` angle). A ≥113 set gives 113^(1/4) ≈ 3.26039 > 3.2578 (record beat).
Record for n=4 is α(C_7^⊠4) = 108 [VZ2002]; Lovász window [108, 115].

**Adjacency (matches R13 Lean engine `lean/Constants/C9.lean`):** cdist(a,b)=min(|a−b|,7−|a−b|);
two letters confusable iff cdist ≤ 1; two words confusable iff every coordinate confusable;
independent iff some coordinate has cdist ≥ 2. Verified my Python `confusable_word` against
the engine's `confusable`/`cdist` (self-test in `certificate/search_n4_orbit/c7graph.py`).

## What I did (R14)

All compute ran as bounded, progress-emitting chunks (≤5 min/call, best-so-far + elapsed
flushed, incumbent persisted to JSON). Scripts under
`constants/9a/certificate/search_n4_orbit/`.

1. **Orbit infrastructure (`orbits.py`, `find_generators.py`).** The strong-power
   confusability relation on Z_7^4 is invariant under coordinate-wise translation, hence
   under any diagonal Z_7 action w → w + t·v (mod 7). The naive diagonal generator
   v=(1,1,1,1) makes every orbit a CLIQUE (step (1,1,1,1) is confusable), so 0 orbits are
   internally independent. I enumerated the **"good" generators** v: those where every
   nonzero multiple t·v (t=1..6) has a coordinate in {2,3,4,5} (cdist ≥ 2). There are
   **360 good generator scale-classes**; each gives 343 orbits of size 7, ALL internally
   independent (a size-7 independent set per orbit).

2. **Orbit-conflict graph + MIS (`orbit_mis.py`, `strong_orbit_mis.py`, `scan_generators.py`,
   `exact_orbit.py`).** For a good generator, two orbits are compatible iff every cross pair
   is independent; an orbit-union is independent iff its orbits are pairwise compatible. The
   reduced conflict graph has 343 nodes and is REGULAR (vertex-transitive), degree ~72–80
   depending on generator. k compatible orbits → 7k vertices.
   - Greedy + strong (2,1)-swap local search + random restarts on the 343-node graph:
     **best = 15 orbits = 105 vertices** for the best generators (1,3,4,3) and (1,3,3,3).
   - Scanned all 360 good generator classes (greedy estimate): **top is 105** (15 orbits);
     the bulk give 98 (14 orbits).
   - So a single-Z_7-orbit-union caps at ~105, since 16 orbits (112) was never reached and
     17 orbits (119, the multiple-of-7 ≥ 113) is far out of reach. **Pure single-orbit-unions
     do not even reach the 108 record, let alone 113.**

3. **Orbit-union + local repair off the lattice (`full_local.py`, `ils_mis.py`, `sa_mis.py`).**
   Seeded the strong feasible ILS ((1,2)-swap plateau local search + perturbation +
   plateau-wander) and a penalty-energy simulated annealer from the 105-vertex orbit-union
   and from scratch:
   - ILS from scratch: plateaus at **101–102**.
   - ILS seeded from 105: stays at **105** (the orbit-union is a deep local optimum;
     perturbation could not escape upward).
   - SA (penalty energy, low λ): only **85** feasible.
   - (high-λ reheat SA run: see report / certificate logs for the final number.)

## Best found this round: 105 (valid, verified)

`certificate/search_n4_orbit/strong_gen1_3_4_3.json` — a genuine 105-vertex independent set
in C_7^⊠4 (re-checked: 105 distinct length-4 words in [0,6], 0 confusable pairs, by
`c7graph.check_independent_set`). **105 < 108 (record) < 113 (beat threshold)** — NO beat,
NOT even matching the record. No Lean certificate is warranted (a 105-set certifies nothing
new; the n=4 engine is identical to the already-verified n=5 engine).

## Honest assessment / why it stalled

- The orbit restriction to a single Z_7 generator has a clean ceiling: the 343-node
  orbit-conflict graph (vertex-transitive, degree ~72–80) has independence number ≈ 15 across
  all 360 good generators, so single-orbit-unions cap at ~105 < 108. The +8 to reach 113 (and
  even the +3 to reach 108) must come from breaking orbit structure substantially.
- Local repair off the lattice did NOT escape the 105 basin: the orbit-union is a deep
  symmetric local optimum, and my (1,2)-swap ILS / penalty-SA could not climb out. Notably
  the unstructured ILS-from-scratch (101–102) is WORSE than the orbit-union (105), so the
  orbit structure helps as a seed but pins a basin the repair can't leave.
- This is consistent with the literature: α(C_7^⊠4)=108 was found by tailored computation
  (VZ2002), and a +5 jump to 113 (if it exists in [108,115]) is a genuine open search that
  did not fall to orbit-restricted local search in a round's compute.

## How to push further

1. **Stronger MIS engine.** Use a state-of-the-art MIS heuristic (e.g. KaMIS / ReduMIS, or
   the Andrade–Resende–Werneck iterated local search with proper (ω, ω+1) swaps and tabu),
   or a real ILP/MaxSAT solver with automorphism symmetry-breaking (the sibling ILP angle).
   My hand-rolled (1,2)-swap ILS is too weak to even reach 108.
2. **Two-generator / larger-group cosets.** A union of orbits under a Z_7×Z_7 or a non-cyclic
   abelian subgroup (cosets of a rank-2 subgroup) gives a richer lattice than a single Z_7;
   the 108-record set is not a single-orbit-union (108 is not a multiple of 7).
3. **Lift the C_7^⊠2 (α=10) or C_7^⊠3 (α=33) optimum** via a lexicographic / cross product
   plus repair, seeding a strong solver from 100 (= 10²) rather than from the orbit-union.
4. **Certify on success only.** Any ≥109 (new best toward beat) or ≥113 (beat) set is a
   conjecture until its list cert type-checks via the R13 engine
   (`isNIndepSet_of_cert` n:=4 + plain `decide` over C(size,2) pairs, ≤ ~6,328 pairs at 113,
   fast/axiom-free). Make a NEW file `lean/Constants/C9Cert<size>n4orbit.lean` (distinct from
   the sibling) wired through `isNIndepSet_of_cert`.

## Status

NO BEAT (best 105 < 108 record < 113 target). Clean negative + structural ceiling on the
single-orbit-union restriction. Search bottleneck confirmed: hand-rolled local search does not
reach the n=4 record; a stronger MIS engine or richer (multi-generator / product-lift) seed is
required.
