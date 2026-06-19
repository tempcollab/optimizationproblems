# c7-4-improvement-113 — exact/near-exact MIS on C_7^⊠4 targeting α ≥ 113

**Angle.** Find an explicit independent set of size ≥ 113 in the strong power C_7^⊠4
(2401 vertices = Z_7^4). Two distinct words u,v are *confusable* (adjacent) iff in EVERY
coordinate the cyclic distance d_7(u_i,v_i) = min(|u_i−v_i|, 7−|u_i−v_i|) ≤ 1; *independent*
iff some coordinate has d_7 ≥ 2. An independent set of size N gives α(C_7^⊠4) ≥ N hence
Θ(C_7) ≥ N^(1/4).

- Record (verified, the value to beat): held = 3.2578 = 367^(1/5) [PS2018, n=5].
- n=4 known record: **108** [VZ2002] → 108^(1/4) ≈ 3.2237 (below the held value).
- Beat threshold via n=4: **113** → 113^(1/4) ≈ 3.26039 > 3.2578 (112 → 3.25315 < held, so
  113 is the exact n=4 threshold; a +5 jump over the n=4 record).
- Proven Lovász window: α(C_7^⊠4) ∈ [108, 115] (ϑ⁴ ≈ 115.0). 113 is INSIDE the window.

## Round 14 — what was built and run (bounded-compute chunks)

Conflict graph built exactly in `certificate/search_n4/graph.py` and verified against the
Lean engine's adjacency rule: 2401 vertices, **96040 edges, 80-regular** (each word has
exactly 3⁴−1 = 80 confusable neighbours — the 3 per-coordinate choices {0,±1}). deg(0000)=80
confirmed. So any set found here transfers to the R13 Lean engine cleanly.

Attacks run, all as capped progress-emitting chunks with on-disk incumbent persistence:

1. **CP-SAT exact MIS** (`cpsat_mis.py`), 0000-fixed by translation symmetry (Z_7^4 acts
   simply transitively; cdist is translation-invariant, so WLOG 0000 ∈ S). 250 s →
   incumbent **102**, dual bound 155. 560 s seeded from 102 → still **102**, dual bound 146
   (loose; worse than the known Lovász 115 ceiling, so NO new certified ceiling).
2. **Stochastic local search** (`localsearch.py`, random-restart greedy + (≤2)-swaps),
   270 s, 85 restarts → walls at **102** (from-scratch basins land 88–96).
3. **ARW (1,2)-swap iterated local search** (`arw.py`, 2-improvement + ILS kicks), two runs
   (270 s anchored, 330 s un-anchored gentle kicks), ~124k iterations → **102**, never
   improved the CP-SAT incumbent and from random starts could not even reach the record 108.
4. **Product construction** (`build_seed.py`): α(C_7^⊠2) = 10 found exactly; the 10×10
   product is a clean **100**-set in C_7^⊠4 (0 confusable pairs, verified).
5. **Z_7-orbit construction** (`orbit_screen.py` / `orbit_gen.py`): the diagonal (1,1,1,1)
   orbit is NEVER independent (a word and its t-shift differ by t in every coord ⇒ confusable
   at t=1). Generalised to all 360 self-independent shift generators g; greedy weighted MIS on
   the 343-node orbit-conflict graph tops out at **91**. Pure orbit-unions are WEAKER than the
   unstructured 102 — orbit structure alone does not reach the record region.

**Best found: 102** (valid, 0 confusable pairs, verified `incumbent.json`).

## Result — NEGATIVE this round (honest)

Best = **102 < record 108 < target 113**. This is NOT a bound move: 102^(1/4) ≈ 3.1830 is
below even the n=4 record, far below the held 3.2578. **No Lean certificate was produced**
(per the rule: cert only for a set ≥ 113, or a new best ≥ 109; 102 is neither). The canonical
`constants/9a.md` and `current.md` are untouched.

The consolation "certified dual ceiling" also did NOT materialise: CP-SAT's LP/dual bound
(146–155) is far looser than the already-known Lovász ϑ⁴ ≈ 115, so no improved ceiling on
α(C_7^⊠4) was obtained either.

**Key diagnostic finding:** generic exact (CP-SAT) and generic local search (2-improvement
ILS, ~124k iterations, 85+ restarts) BOTH stall at 102 and from random starts cannot even
reach the known record 108. The 108-set (and any 113-set, if it exists) appears to live in a
region of the configuration space inaccessible to generic MIS heuristics from cold starts —
it requires the *specific* VZ2002 simulated-annealing / circular-graph construction, not a
from-scratch generic solver. The 80-regularity makes the graph very dense and locally
symmetric, which is exactly the regime where 2-improvement plateaus.

## How to push this further (next round)

The bottleneck is reaching the record-108 region at all, before any +5 push to 113. Concrete
levers, roughly in order of promise:

1. **Seed from the actual VZ2002 108-set, then local-repair toward 113.** The 102-from-scratch
   wall is the real obstacle. Obtain the explicit 108-set (Vesel–Žerovnik 2002 / the
   cycle-powers paper [Jurkiewicz–Kubale]; web search confirms an explicit 108-vertex set
   exists in the literature) and seed CP-SAT / ARW from it. A remove-k/add-(k+1) repair off a
   *real* 108-set is far more likely to find +5 than a from-scratch search that can't even
   reach 108. This is the single highest-value next step.
2. **Stronger exact solver / heavier symmetry-breaking.** The 0000-fix alone is weak. Add
   per-coordinate dihedral-flip + S_4 coordinate-permutation lex constraints (|Aut| ≥
   14⁴·24 = 921,984) to prune the CP-SAT/B&B tree; consider a dedicated MaxIndependentSet
   solver (e.g. KaMIS / a clique solver on the complement) which beats CP-SAT on dense graphs.
3. **Better local search: penalty/tabu DLS (PLS / phased local search, the MO2017 family),
   not plain 2-improvement.** The ARW (1,2)-swap stalled; a dynamic-penalty or k>2 plateau
   search exploiting the Z_7^4 symmetry (the MO2017 template that found the 350 n=5 set) is the
   proven heuristic for odd-cycle powers and should climb past 102.
4. **Honest possibility: α(C_7^⊠4) may simply be < 113** (108–112). The Lovász window only
   says ≤ 115; it does not guarantee 113 exists. If repeated structured search from the real
   108-set cannot exceed 112, the angle should be marked exhausted and effort redirected to n=5
   (`symmetry-guided-search-c7-5-368`) with a genuinely new circular-graph (a,b,g).

## Reproduce

```
cd constants/9a/certificate/search_n4
python3 graph.py            # build + sanity-check the 2401-vertex conflict graph
python3 cpsat_mis.py 250    # exact MIS chunk (CP-SAT), 0000-fixed, ~250s -> incumbent.json
python3 localsearch.py 270  # stochastic local search chunk
python3 arw.py 270          # ARW (1,2)-swap ILS chunk
python3 build_seed.py       # alpha(C_7^2)=10 + product 100-set
python3 orbit_screen.py     # screen all 360 self-indep generators (greedy orbit MIS)
```

Incumbents persist to `incumbent.json` / `incumbent_ls.json` / `incumbent_arw.json`
(`{ids, size, words}`); best this round = 102 (`incumbent_backup102.json`).
