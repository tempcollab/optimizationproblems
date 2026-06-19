# C_9 (Θ(C_7)) — orbit-restricted search on C_7^⊠4 (slug c7-4-orbit-restricted-search-113)

Round 14. Target: an independent set of size ≥ 113 in C_7^⊠4 (→ 113^(1/4) ≈ 3.26039 >
record 3.2578). **Result: NO BEAT.** Best found = **105** (single Z_7 orbit-union), which is
below the 108 record [VZ2002], let alone 113.

## Adjacency (matches the R13 Lean engine `lean/Constants/C9.lean`)

cdist(a,b)=min(|a−b|,7−|a−b|) on letters 0..6; confusable iff cdist ≤ 1; two length-4 words
confusable iff every coordinate confusable; independent iff some coordinate has cdist ≥ 2.
Self-test: `python3 c7graph.py` (verifies the rule on the known cdist facts).

## Files

- `c7graph.py` — core graph utils + adjacency self-test + `check_independent_set` validator.
- `orbits.py` — diagonal Z_7 orbit machinery (shows the naive (1,1,1,1) generator gives 0
  internally-independent orbits).
- `find_generators.py` — enumerates the 360 "good" generator scale-classes (every nonzero
  multiple has a cdist≥2 coordinate ⇒ every orbit internally independent).
- `scan_generators.py` — greedy MIS estimate of the orbit-union ceiling over all 360
  generators (top = 105 = 15 orbits).
- `orbit_mis.py`, `strong_orbit_mis.py` — greedy / strong-local-search MIS on the 343-node
  orbit-conflict graph for a chosen generator (best = 15 orbits = 105).
- `exact_orbit.py` — B&B on the orbit-conflict graph (timed out; LB 14, did not beat the LS 15).
- `full_local.py`, `ils_mis.py`, `sa_mis.py` — full-graph (2401-vertex) local repair off the
  orbit lattice, seeded from the 105 orbit-union and from scratch.

## Reproduce the key results

```
cd constants/9a/certificate/search_n4_orbit
python3 c7graph.py                              # adjacency self-test
python3 find_generators.py                      # 360 good generator classes
timeout 200 python3 strong_orbit_mis.py 1 3 4 3 180   # orbit-union -> 105 (15 orbits)
python3 -c "import json; from c7graph import check_independent_set as C; \
  d=json.load(open('strong_gen1_3_4_3.json')); print(C(d['words']))"   # (True, 0, 105)
timeout 320 python3 ils_mis.py strong_gen1_3_4_3.json 300 ils_seeded_v2.json 4  # stays 105
timeout 320 python3 ils_mis.py - 300 ils_scratch_v2.json 4                       # ~101 scratch
```

## Best set (valid, but below record — NOT certified to Lean)

`strong_gen1_3_4_3.json` — 105 distinct length-4 words in [0,6], pairwise independent
(0 confusable pairs, verified by `check_independent_set`). Generator (1,3,4,3), a union of
15 internally-independent size-7 Z_7-orbits. Since 105 < 108 < 113, this certifies nothing
new; no Lean cert produced this round.

## Conclusion (honest)

Single Z_7 orbit-unions cap at ≈ 15 orbits = 105 vertices (orbit-conflict graph is
vertex-transitive, α_orbit ≈ 15 across all 360 good generators). Local repair off the lattice
(ILS, SA) could not escape the 105 basin and did not reach 108. A beat (113) — or even
matching the 108 record — requires a stronger MIS engine (KaMIS/ReduMIS or symmetry-broken
ILP) and/or a richer seed (multi-generator cosets, or a lift of the C_7^⊠2/C_7^⊠3 optimum),
not single-orbit local search.
