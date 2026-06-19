"""
Exact / near-exact MIS on the 343-node orbit-conflict graph for a given generator, to PIN
the orbit-union ceiling 7*alpha_orbit.  Uses a branch-and-bound with greedy coloring bound
(Tomita-style), wall-clock capped.  If it completes, alpha_orbit is exact (single-orbit-union
ceiling = 7*alpha_orbit).  If it times out, reports the best found + the remaining UB.

Usage: python3 exact_orbit.py V0 V1 V2 V3 [budget_s]
"""

import sys
import time
from itertools import product

N = 4


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
    seen = set(); ow = []
    for w in product(range(7), repeat=N):
        if w in seen:
            continue
        ob = set(); cur = w
        for _ in range(7):
            ob.add(cur); cur = tuple((cur[i] + gen[i]) % 7 for i in range(N))
        for x in ob:
            seen.add(x)
        ow.append(sorted(ob))
    return ow


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


def main():
    gen = tuple(int(x) for x in sys.argv[1:5])
    budget = float(sys.argv[5]) if len(sys.argv) > 5 else 200.0
    t0 = time.time()
    ow = orbit_data(gen)
    GW = [w for w in ow if len(w) == 7 and internally_independent(w)]
    M = len(GW)
    # complement adjacency as bitsets for fast B&B on the conflict graph
    adj = [0] * M
    for i in range(M):
        for j in range(i + 1, M):
            if not orbits_compatible(GW[i], GW[j]):
                adj[i] |= (1 << j); adj[j] |= (1 << i)
    full = (1 << M) - 1
    print(f"gen={gen} M={M} built ({time.time()-t0:.1f}s)", flush=True)

    best = [0]
    deadline = t0 + budget
    timed_out = [False]

    # greedy coloring bound on a candidate bitset P -> number of color classes (UB on indep)
    def color_bound(P):
        # returns list of (vertex, colorindex) processed in order giving an UB
        order = []
        uncolored = P
        color = 0
        while uncolored:
            color += 1
            avail = uncolored
            # one color class: pick an independent (in conflict graph) subset greedily
            cls = 0
            tmp = avail
            while tmp:
                v = (tmp & -tmp).bit_length() - 1
                tmp &= ~(1 << v)
                if not (adj[v] & cls):
                    cls |= (1 << v)
                    order.append((v, color))
                    uncolored &= ~(1 << v)
        return order

    import sys as _sys
    _sys.setrecursionlimit(10000)

    def expand(P, size):
        if time.time() > deadline:
            timed_out[0] = True
            return
        if P == 0:
            if size > best[0]:
                best[0] = size
            return
        order = color_bound(P)
        # process in reverse (highest color first) for pruning
        for v, c in reversed(order):
            if timed_out[0]:
                return
            if size + c <= best[0]:
                return
            # choose v: independent set so neighbors excluded
            newP = P & ~adj[v] & ~(1 << v)
            # restrict P to vertices not yet "removed": standard Tomita removes v from P too
            expand(newP, size + 1)
            P &= ~(1 << v)

    expand(full, 0)
    status = "TIMEOUT(lower bound)" if timed_out[0] else "EXACT"
    print(f"gen={gen} alpha_orbit {status} = {best[0]}  ceiling=7*{best[0]}={7*best[0]} "
          f"({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
