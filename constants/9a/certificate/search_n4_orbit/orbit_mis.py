"""
For a chosen GOOD generator v, build the 343-orbit reduced conflict graph and search for a
large set of pairwise-COMPATIBLE internally-independent orbits (an orbit-union independent
set).  k compatible orbits -> 7k vertices.  Target: >=17 orbits (119) so 7k>=113, or 16
(112) + later local repair.

Usage: python3 orbit_mis.py V0 V1 V2 V3 [time_budget_s]
"""

import sys
import time
import json
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


def make_orbit_data(gen):
    """Return (reps, orbit_words, internally_independent_mask)."""
    # canonical rep: shift so that coord0 == 0?  generator may have gen[0]==0, then coord0
    # is invariant -> canonicalize by another coordinate.  Use full orbit-set canon.
    seen = set()
    reps = []
    orbit_words = []
    for w in product(range(7), repeat=N):
        if w in seen:
            continue
        ob = []
        cur = w
        for t in range(7):
            ob.append(cur)
            cur = tuple((cur[i] + gen[i]) % 7 for i in range(N))
        obset = frozenset(ob)
        if obset in seen:
            continue
        for x in ob:
            seen.add(x)
        seen.add(obset)
        # dedup orbit (in case order<7) -> keep distinct
        ob_distinct = sorted(set(ob))
        reps.append(min(ob_distinct))
        orbit_words.append(ob_distinct)
    return reps, orbit_words


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


def greedy_mis(adj, order):
    """adj: list of sets (conflict). order: iteration order of nodes. Greedy independent."""
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
    gen = tuple(int(x) for x in sys.argv[1:5])
    budget = float(sys.argv[5]) if len(sys.argv) > 5 else 60.0
    t0 = time.time()
    reps, orbit_words = make_orbit_data(gen)
    # keep only full size-7 internally-independent orbits
    good_idx = []
    for i, w in enumerate(orbit_words):
        if len(w) == 7 and internally_independent(w):
            good_idx.append(i)
    GW = [orbit_words[i] for i in good_idx]
    M = len(GW)
    print(f"gen={gen} orbits={len(orbit_words)} good-size7-indep-orbits={M} "
          f"({time.time()-t0:.1f}s)", flush=True)
    if M == 0:
        return
    # build conflict graph among good orbits
    adj = [set() for _ in range(M)]
    for i in range(M):
        for j in range(i + 1, M):
            if not orbits_compatible(GW[i], GW[j]):
                adj[i].add(j)
                adj[j].add(i)
    deg = [len(a) for a in adj]
    print(f"orbit-conflict graph built: avg deg {sum(deg)/M:.1f} "
          f"min {min(deg)} max {max(deg)} ({time.time()-t0:.1f}s)", flush=True)

    best = []
    import random
    rng = random.Random(12345)
    iters = 0
    while time.time() - t0 < budget:
        iters += 1
        order = list(range(M))
        if iters == 1:
            order.sort(key=lambda u: deg[u])  # min-degree first
        else:
            rng.shuffle(order)
        sol = greedy_mis(adj, order)
        if len(sol) > len(best):
            best = sol
            print(f"  iter {iters}: orbits={len(best)} -> verts={7*len(best)} "
                  f"({time.time()-t0:.1f}s)", flush=True)
    words = []
    for idx in best:
        words.extend(GW[idx])
    out = {
        "gen": list(gen), "num_orbits": len(best), "num_verts": len(words),
        "iters": iters, "words": [list(w) for w in words],
    }
    fname = f"orbitmis_gen{'_'.join(map(str,gen))}.json"
    with open(fname, "w") as f:
        json.dump(out, f)
    print(f"DONE gen={gen} best_orbits={len(best)} verts={len(words)} "
          f"saved {fname} iters={iters} ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
