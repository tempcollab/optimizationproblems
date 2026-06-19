"""
Strong MIS on the 343-node orbit-conflict graph for a chosen good generator, via
(2,1)-swap plateau local search with random restarts and perturbation (a standard strong
MIS heuristic: repeatedly try to add a free vertex; if none, do a (2,1) swap = drop 1 to
admit 2; periodically perturb to escape plateaus).  Reports best orbit count k; 7k vertices.

Persists best orbit set to JSON each improvement so a killed chunk loses nothing.

Usage: python3 strong_orbit_mis.py V0 V1 V2 V3 [budget_s]
"""

import sys
import time
import json
import random
from itertools import product

N = 4
FAR = {2, 3, 4, 5}


def cdist(a, b):
    d = abs(a - b)
    return min(d, 7 - d)


CONF = [[1 if cdist(a, b) <= 1 else 0 for b in range(7)] for a in range(7)]


def confusable_word(u, v):
    for i in range(N):
        if not CONF[u[i]][v[i]]:
            return False
    return True


def orbit_data(gen):
    seen = set()
    orbit_words = []
    for w in product(range(7), repeat=N):
        if w in seen:
            continue
        ob = set()
        cur = w
        for t in range(7):
            ob.add(cur)
            cur = tuple((cur[i] + gen[i]) % 7 for i in range(N))
        for x in ob:
            seen.add(x)
        orbit_words.append(sorted(ob))
    return orbit_words


def internally_independent(words):
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if confusable_word(words[i], words[j]):
                return False
    return True


def orbits_compatible(wa, wb):
    for a in wa:
        for b in wb:
            if confusable_word(a, b):
                return False
    return True


def build(gen):
    ow = orbit_data(gen)
    GW = [w for w in ow if len(w) == 7 and internally_independent(w)]
    M = len(GW)
    adj = [set() for _ in range(M)]
    for i in range(M):
        for j in range(i + 1, M):
            if not orbits_compatible(GW[i], GW[j]):
                adj[i].add(j)
                adj[j].add(i)
    return GW, adj


def local_search(adj, M, budget, t0, rng, save_cb):
    """(2,1)-swap plateau search with perturbation. Returns best (set of node ids)."""
    # current solution as a set; tight[v] = number of solution-neighbors of v (0 => free)
    def greedy_init():
        order = list(range(M)); rng.shuffle(order)
        sol = set(); banned = set()
        for u in order:
            if u in banned: continue
            sol.add(u); banned.add(u); banned |= adj[u]
        return sol

    best = set()
    sol = greedy_init()
    # tightness count
    tight = [0] * M
    for u in sol:
        for w in adj[u]:
            tight[w] += 1
    def add(u):
        sol.add(u)
        for w in adj[u]: tight[w] += 1
    def rem(u):
        sol.discard(u)
        for w in adj[u]: tight[w] -= 1

    stall = 0
    while time.time() - t0 < budget:
        # try to add any free vertex (tight==0, not in sol)
        free = [u for u in range(M) if u not in sol and tight[u] == 0]
        if free:
            add(rng.choice(free))
            stall = 0
        else:
            # try a (2,1) swap: find v in sol s.t. removing v creates >=2 free verts
            improved = False
            order = list(sol); rng.shuffle(order)
            for v in order:
                # candidates that would become free if v removed: tight==1 and their only
                # solution-neighbor is v
                cands = [u for u in adj[v] if u not in sol and tight[u] == 1]
                # filter: u's solution-neighbor is exactly v
                ok = []
                for u in cands:
                    if len(adj[u] & sol) == 1:  # only v
                        ok.append(u)
                if len(ok) >= 2:
                    # check we can add 2 mutually-nonadjacent ones
                    found = None
                    for a_i in range(len(ok)):
                        for b_i in range(a_i + 1, len(ok)):
                            if ok[b_i] not in adj[ok[a_i]]:
                                found = (ok[a_i], ok[b_i]); break
                        if found: break
                    if found:
                        rem(v); add(found[0]); add(found[1])
                        improved = True; stall = 0; break
            if not improved:
                stall += 1
                # perturbation: drop a random vertex (and force-add one of its neighbors)
                if sol:
                    v = rng.choice(list(sol))
                    rem(v)
                    nb = [u for u in adj[v] if u not in sol and tight[u] == 0]
                    if nb: add(rng.choice(nb))
                if stall > 200:
                    # restart
                    for u in list(sol): rem(u)
                    sol2 = greedy_init()
                    for u in sol2: add(u)
                    stall = 0
        if len(sol) > len(best):
            best = set(sol)
            save_cb(best)
    return best


def main():
    gen = tuple(int(x) for x in sys.argv[1:5])
    budget = float(sys.argv[5]) if len(sys.argv) > 5 else 120.0
    t0 = time.time()
    GW, adj = build(gen)
    M = len(GW)
    deg = [len(a) for a in adj]
    print(f"gen={gen} M={M} avgdeg={sum(deg)/M:.1f} built ({time.time()-t0:.1f}s)", flush=True)
    rng = random.Random(2024)
    state = {"best": 0}
    fname = f"strong_gen{'_'.join(map(str,gen))}.json"
    def save_cb(bestset):
        words = []
        for idx in bestset:
            words.extend(GW[idx])
        out = {"gen": list(gen), "num_orbits": len(bestset),
               "num_verts": len(words), "words": [list(w) for w in words]}
        with open(fname, "w") as f:
            json.dump(out, f)
        if len(bestset) > state["best"]:
            state["best"] = len(bestset)
            print(f"  best orbits={len(bestset)} verts={7*len(bestset)} "
                  f"({time.time()-t0:.1f}s)", flush=True)
    best = local_search(adj, M, budget, t0, rng, save_cb)
    print(f"DONE gen={gen} best_orbits={len(best)} verts={7*len(best)} "
          f"saved {fname} ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
