"""
Full-graph (2401-vertex) MIS local search on C_7^box4, seeded from an orbit-union incumbent.
Uses the standard (2,1)-swap plateau local search (drop 1 to admit 2) with perturbation and
restarts.  This is the orbit-union + LOCAL REPAIR OFF THE LATTICE step (MO2017-style):
start from the best orbit-union, then repair using individual-vertex moves.

Adjacency = C_7^box4 confusability (matches R13 Lean engine).  Persists best set each
improvement so a killed chunk loses nothing.

Usage: python3 full_local.py [seed_json] [budget_s] [out_json]
  if seed_json omitted, starts from empty / greedy.
"""

import sys
import time
import json
import random
from itertools import product

N = 4


def cdist(a, b):
    d = abs(a - b)
    return min(d, 7 - d)


CONF = [[1 if cdist(a, b) <= 1 else 0 for b in range(7)] for a in range(7)]

VERTS = [tuple(w) for w in product(range(7), repeat=N)]
VIDX = {w: i for i, w in enumerate(VERTS)}
NV = len(VERTS)


def confusable(ui, vi):
    u = VERTS[ui]; v = VERTS[vi]
    for i in range(N):
        if not CONF[u[i]][v[i]]:
            return False
    return True


# Build adjacency lists (conflict graph). 2401 verts; each has limited neighbors.
def build_adj():
    adj = [[] for _ in range(NV)]
    # neighbors of a vertex: all words confusable in every coord (cdist<=1 each coord),
    # excluding self. Per coord 3 choices (-1,0,+1 mod 7) -> 3^4=81 including self -> 80 nb.
    for i, w in enumerate(VERTS):
        nbrs = []
        for d in product((-1, 0, 1), repeat=N):
            if all(x == 0 for x in d):
                continue
            v = tuple((w[k] + d[k]) % 7 for k in range(N))
            nbrs.append(VIDX[v])
        adj[i] = nbrs
    return adj


def main():
    seed_json = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "-" else None
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 240.0
    out_json = sys.argv[3] if len(sys.argv) > 3 else "full_local_best.json"
    t0 = time.time()
    adj = build_adj()
    adjset = [set(a) for a in adj]
    print(f"adj built NV={NV} deg={len(adj[0])} ({time.time()-t0:.1f}s)", flush=True)

    rng = random.Random(99)

    sol = set()
    tight = [0] * NV  # number of solution-neighbors

    def add(u):
        sol.add(u)
        for w in adj[u]:
            tight[w] += 1

    def rem(u):
        sol.discard(u)
        for w in adj[u]:
            tight[w] -= 1

    # seed
    if seed_json:
        with open(seed_json) as f:
            data = json.load(f)
        for w in data["words"]:
            u = VIDX[tuple(w)]
            if tight[u] == 0 and u not in sol:
                add(u)
        print(f"seeded from {seed_json}: {len(sol)} verts ({time.time()-t0:.1f}s)", flush=True)
    # greedy fill
    order = list(range(NV)); rng.shuffle(order)
    for u in order:
        if u not in sol and tight[u] == 0:
            add(u)
    print(f"after greedy fill: {len(sol)} ({time.time()-t0:.1f}s)", flush=True)

    best = set(sol)
    best_len = len(best)

    def save():
        words = [list(VERTS[u]) for u in best]
        with open(out_json, "w") as f:
            json.dump({"num_verts": len(words), "words": words}, f)

    save()
    print(f"  best={best_len} ({time.time()-t0:.1f}s)", flush=True)

    stall = 0
    last_print = t0
    while time.time() - t0 < budget:
        free = [u for u in range(NV) if u not in sol and tight[u] == 0]
        if free:
            add(rng.choice(free))
            stall = 0
        else:
            improved = False
            sol_list = list(sol); rng.shuffle(sol_list)
            for v in sol_list:
                ok = [u for u in adj[v] if u not in sol and tight[u] == 1
                      and len(adjset[u] & sol) == 1]
                if len(ok) >= 2:
                    found = None
                    for a_i in range(len(ok)):
                        ua = ok[a_i]
                        for b_i in range(a_i + 1, len(ok)):
                            ub = ok[b_i]
                            if ub not in adjset[ua]:
                                found = (ua, ub); break
                        if found:
                            break
                    if found:
                        rem(v); add(found[0]); add(found[1])
                        improved = True; stall = 0
                        break
            if not improved:
                stall += 1
                if sol:
                    v = rng.choice(list(sol))
                    rem(v)
                    nb = [u for u in adj[v] if u not in sol and tight[u] == 0]
                    if nb:
                        add(rng.choice(nb))
                if stall > 1000:
                    # partial restart: drop ~10% random
                    drop = rng.sample(list(sol), max(1, len(sol) // 10))
                    for u in drop:
                        rem(u)
                    stall = 0
        if len(sol) > best_len:
            best = set(sol); best_len = len(best); save()
            print(f"  best={best_len} ({time.time()-t0:.1f}s)", flush=True)
        if time.time() - last_print > 30:
            last_print = time.time()
            print(f"  ... cur={len(sol)} best={best_len} ({time.time()-t0:.1f}s)", flush=True)

    save()
    print(f"DONE best={best_len} saved {out_json} ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
