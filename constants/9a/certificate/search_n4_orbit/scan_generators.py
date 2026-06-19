"""
Quick scan over good generator scale-classes: for each, build the orbit-conflict graph and
estimate its independence number via fast greedy random restarts (short budget per gen).
Report generators whose orbit-union reaches the most vertices.  This finds the best cyclic
structures to feed into a strong MIS solver.

Usage: python3 scan_generators.py [per_gen_iters] [total_budget_s]
"""

import sys
import time
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


def good_generator_classes():
    classes = {}
    for v in product(range(7), repeat=N):
        if all(c == 0 for c in v):
            continue
        ok = True
        for t in range(1, 7):
            s = tuple((t * v[i]) % 7 for i in range(N))
            if not any(c in FAR for c in s):
                ok = False
                break
        if not ok:
            continue
        cls = min(tuple((t * v[i]) % 7 for i in range(N)) for t in range(1, 7))
        classes[cls] = True
    return sorted(classes.keys())


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


def build_adj(GW):
    M = len(GW)
    adj = [set() for _ in range(M)]
    for i in range(M):
        for j in range(i + 1, M):
            if not orbits_compatible(GW[i], GW[j]):
                adj[i].add(j)
                adj[j].add(i)
    return adj


def greedy(adj, order):
    chosen = []
    banned = set()
    for u in order:
        if u in banned:
            continue
        chosen.append(u)
        banned.add(u)
        banned |= adj[u]
    return chosen


def main():
    per_iters = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    total_budget = float(sys.argv[2]) if len(sys.argv) > 2 else 270.0
    t0 = time.time()
    classes = good_generator_classes()
    print(f"good gen classes: {len(classes)} ({time.time()-t0:.1f}s)", flush=True)
    rng = random.Random(7)
    results = []
    for gi, gen in enumerate(classes):
        if time.time() - t0 > total_budget:
            print(f"budget reached at gen {gi}/{len(classes)}", flush=True)
            break
        ow = orbit_data(gen)
        GW = [w for w in ow if len(w) == 7 and internally_independent(w)]
        M = len(GW)
        if M == 0:
            continue
        adj = build_adj(GW)
        deg = [len(a) for a in adj]
        best = 0
        order = list(range(M))
        order.sort(key=lambda u: deg[u])
        best = max(best, len(greedy(adj, order)))
        for _ in range(per_iters):
            rng.shuffle(order)
            best = max(best, len(greedy(adj, order)))
        results.append((best * 7, best, gen, M, sum(deg) / M))
    results.sort(reverse=True)
    print(f"\nTop generators by orbit-union greedy verts ({time.time()-t0:.1f}s):", flush=True)
    for verts, k, gen, M, avgdeg in results[:25]:
        print(f"  verts~{verts} ({k} orbits) gen={gen} M={M} avgdeg={avgdeg:.1f}", flush=True)


if __name__ == "__main__":
    main()
