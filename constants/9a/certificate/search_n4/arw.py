"""ARW-style iterated local search for MIS on C_7^⊠4.

Andrade-Resende-Werneck (2012) local search: the core move is the (1,2)-swap
(2-improvement): find a vertex v in S and two non-adjacent vertices a,b not in S
such that N(a)∩S = N(b)∩S = {v} and a not~ b — remove v, add a,b (net +1).
Combined with simple (0,1) additions of free vertices and plateau (1,1) swaps,
plus perturbation (force a random vertex in, kicking out its neighbors) for ILS.

Maintains:
  inS, tight[v] = |N(v)∩S|, and for tight==1 vertices, tight1nb[v] = the single S-nbr.

Bounded-compute: wall-clock cap argv[1]; persists best to incumbent_arw.json; prints
best + elapsed periodically.
"""
import sys, json, time, os, random
import numpy as np
from graph import build_adjacency, NV, id_to_word, word_to_id

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "incumbent_arw.json")
SEEDS = ["incumbent.json", "incumbent_ls.json", "incumbent_arw.json",
         "seed_product.json", "seed_orbit.json"]


def main():
    cap = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0
    t0 = time.time()
    arr, adj = build_adjacency()
    nbrs = [np.where(adj[i])[0].tolist() for i in range(NV)]
    nbrset = [set(n) for n in nbrs]
    print(f"[{time.time()-t0:.1f}s] graph built", flush=True)

    inS = np.zeros(NV, dtype=bool)
    tight = np.zeros(NV, dtype=np.int32)
    # tight1nb[v] valid only when tight[v]==1
    tight1nb = np.full(NV, -1, dtype=np.int32)
    S = set()

    def add(v):
        inS[v] = True; S.add(v)
        for u in nbrs[v]:
            tight[u] += 1
            if tight[u] == 1:
                tight1nb[u] = v
    def rem(v):
        inS[v] = False; S.discard(v)
        for u in nbrs[v]:
            tight[u] -= 1
            if tight[u] == 1:
                # recompute its single S-neighbor
                for w in nbrs[u]:
                    if inS[w]:
                        tight1nb[u] = w; break
    def reset():
        inS[:] = False; tight[:] = 0; tight1nb[:] = -1; S.clear()

    def add_free():
        # add all free (tight==0) vertices greedily in random order
        free = np.where((~inS) & (tight == 0))[0]
        np.random.shuffle(free)
        for v in free:
            if not inS[v] and tight[v] == 0:
                add(int(v))

    def two_improve_pass():
        """One sweep: for each v in S, see if it can be replaced by 2 vertices.
        Returns True if any improvement applied."""
        improved = False
        for v in list(S):
            if not inS[v]:
                continue
            # candidates: vertices x with tight==1 and tight1nb==v (x's only S-nbr is v)
            cand = [int(x) for x in nbrs[v] if not inS[x] and tight[x] == 1 and tight1nb[x] == v]
            if len(cand) < 2:
                continue
            # find two non-adjacent candidates
            found = None
            cs = cand
            random.shuffle(cs)
            for i in range(len(cs)):
                a = cs[i]
                na = nbrset[a]
                for j in range(i + 1, len(cs)):
                    b = cs[j]
                    if b not in na:
                        found = (a, b); break
                if found:
                    break
            if found:
                a, b = found
                rem(v); add(a); add(b)
                improved = True
        return improved

    best = 0; best_set = []
    for f in SEEDS:
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            try:
                d = json.load(open(p))
                if d.get("size", 0) > best:
                    best = d["size"]; best_set = d["ids"]
            except Exception:
                pass
    print(f"[start] prior best {best}", flush=True)

    def save():
        json.dump({"ids": sorted(best_set), "size": best,
                   "words": [list(id_to_word(i)) for i in best_set]}, open(OUT, "w"))

    z = word_to_id((0, 0, 0, 0))
    last = time.time()
    it = 0
    # ILS loop: keep a current solution, perturb, local-search, accept if >= best-1
    # start current from seed if available else greedy
    reset()
    if best_set:
        # rebuild from best_set (respecting independence; they are independent)
        for v in best_set:
            if tight[v] == 0 and not inS[v]:
                add(v)
    add_free()
    while time.time() - t0 < cap:
        it += 1
        # local search to a 2-opt local max
        while time.time() - t0 < cap:
            add_free()
            if not two_improve_pass():
                add_free()
                if not two_improve_pass():
                    break
        cur = len(S)
        if cur > best:
            best = cur; best_set = sorted(S); save()
            print(f"[{time.time()-t0:.1f}s] NEW best {best} (iter {it})", flush=True)
        # perturbation (ILS kick): force g random non-S vertices in, removing their S-nbrs
        g = random.choice([1, 1, 1, 2])
        for _ in range(g):
            v = random.randrange(NV)
            if inS[v]:
                continue
            for u in list(nbrs[v]):
                if inS[u]:
                    rem(u)
            if tight[v] == 0:
                add(v)
        if time.time() - last > 20:
            print(f"[{time.time()-t0:.1f}s] best={best} cur={len(S)} iters={it}", flush=True)
            last = time.time()
    print(f"[{time.time()-t0:.1f}s] DONE best={best} iters={it}", flush=True)

if __name__ == "__main__":
    main()
