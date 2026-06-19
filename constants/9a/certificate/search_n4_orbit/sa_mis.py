"""
Strong simulated-annealing MIS on C_7^box4 (2401 verts), penalty formulation.

State = subset S (membership array). Energy E = lambda * (#conflict edges inside S) - |S|.
Moves: flip a random vertex (add/remove). Accept by Metropolis. We track the best FEASIBLE
(conflict-free) set seen, recovered by greedily repairing the incumbent each time |S| is large.

This explores far more freely than feasible-only (2,1) swaps and is the standard effective
heuristic for Shannon-capacity independent-set search.

Seed optionally from a JSON word list. Persists best FEASIBLE set each improvement.

Usage: python3 sa_mis.py [seed_json|-] [budget_s] [out_json] [lambda]
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


def build_adj():
    adj = [[] for _ in range(NV)]
    for i, w in enumerate(VERTS):
        for d in product((-1, 0, 1), repeat=N):
            if all(x == 0 for x in d):
                continue
            v = tuple((w[k] + d[k]) % 7 for k in range(N))
            adj[i].append(VIDX[v])
    return adj


def feasible_repair(member, tight):
    """Greedily remove highest-conflict vertices until conflict-free, then greedily add.
    Returns a feasible independent set (list of node ids)."""
    # copy
    sol = set(i for i in range(NV) if member[i])
    t = list(tight)
    # remove until no conflict: repeatedly drop the vertex with max conflict
    # conflict count of u = number of solution-neighbors that are also in sol
    # tight[u] counts solution-neighbors; for u in sol, conflict = tight[u]
    import heapq
    while True:
        # find a conflicting vertex in sol
        worst = -1; worstc = 0
        for u in sol:
            if t[u] > worstc:
                worstc = t[u]; worst = u
        if worst < 0:
            break
        # remove worst
        sol.discard(worst)
        for w in ADJ[worst]:
            t[w] -= 1
    # greedily add free vertices
    order = list(range(NV))
    RNG.shuffle(order)
    for u in order:
        if u not in sol and t[u] == 0:
            sol.add(u)
            for w in ADJ[u]:
                t[w] += 1
    return sol


ADJ = None
RNG = random.Random(20240619)


def main():
    global ADJ
    seed_json = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "-" else None
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 240.0
    out_json = sys.argv[3] if len(sys.argv) > 3 else "sa_best.json"
    lam = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
    t0 = time.time()
    ADJ = build_adj()
    print(f"adj built NV={NV} ({time.time()-t0:.1f}s) lambda={lam}", flush=True)

    member = [False] * NV
    tight = [0] * NV  # solution-neighbor count for every vertex

    def add(u):
        member[u] = True
        for w in ADJ[u]:
            tight[w] += 1

    def rem(u):
        member[u] = False
        for w in ADJ[u]:
            tight[w] -= 1

    if seed_json:
        with open(seed_json) as f:
            data = json.load(f)
        for w in data["words"]:
            u = VIDX[tuple(w)]
            if not member[u]:
                add(u)
        print(f"seeded {sum(member)} verts from {seed_json}", flush=True)
    else:
        order = list(range(NV)); RNG.shuffle(order)
        for u in order:
            if tight[u] == 0 and not member[u]:
                add(u)
        print(f"greedy init {sum(member)} verts", flush=True)

    size = sum(member)
    # conflict edges inside S = sum over u in S of tight[u] / 2
    conf_edges = sum(tight[u] for u in range(NV) if member[u]) // 2

    best_feas = feasible_repair(member, tight)
    best_len = len(best_feas)

    def save(s):
        words = [list(VERTS[u]) for u in s]
        with open(out_json, "w") as f:
            json.dump({"num_verts": len(words), "words": words}, f)

    save(best_feas)
    print(f"  best_feasible={best_len} ({time.time()-t0:.1f}s)", flush=True)

    # SA schedule
    T = 1.5
    Tmin = 0.02
    step = 0
    last_print = t0
    last_repair = t0
    while time.time() - t0 < budget:
        # adaptive cooling over budget (reheat cycles for diversification)
        frac = ((time.time() - t0) / budget * 4.0) % 1.0
        T = max(Tmin, 1.5 * (1 - frac) + Tmin)
        for _ in range(5000):
            u = RNG.randrange(NV)
            if member[u]:
                # remove: delta E = lambda*(-tight[u]) - (-1) = -lambda*tight[u] + 1
                dE = -lam * tight[u] + 1
            else:
                # add: delta E = lambda*tight[u] - 1
                dE = lam * tight[u] - 1
            if dE <= 0 or RNG.random() < pow(2.718281828, -dE / T):
                if member[u]:
                    rem(u); size -= 1; conf_edges -= tight[u] if False else 0
                else:
                    add(u); size += 1
        step += 1
        # periodically extract a feasible solution from the current (possibly infeasible) state
        if time.time() - last_repair > 3:
            last_repair = time.time()
            feas = feasible_repair(member, tight)
            if len(feas) > best_len:
                best_len = len(feas); best_feas = feas; save(best_feas)
                print(f"  best_feasible={best_len} ({time.time()-t0:.1f}s)", flush=True)
        if time.time() - last_print > 30:
            last_print = time.time()
            cur_conf = sum(tight[u] for u in range(NV) if member[u]) // 2
            print(f"  ... |S|={sum(member)} conf_edges={cur_conf} T={T:.2f} "
                  f"best={best_len} ({time.time()-t0:.1f}s)", flush=True)
    feas = feasible_repair(member, tight)
    if len(feas) > best_len:
        best_len = len(feas); best_feas = feas; save(best_feas)
    save(best_feas)
    print(f"DONE best_feasible={best_len} saved {out_json} ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
