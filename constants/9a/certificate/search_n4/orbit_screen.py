"""Fast screen of all self-independent generators g via GREEDY weighted MIS on the
orbit-conflict graph (343 nodes), to find promising orbit-union sizes quickly. Then
report top generators; exact MIS is run only on the best handful afterwards.
"""
import json, os, itertools, time
import numpy as np
from graph import id_to_word, word_to_id, CONF_LETTER, NV

HERE = os.path.dirname(os.path.abspath(__file__))


def far(x):
    return min(x % 7, (7 - x) % 7) >= 2

def gsi(g):
    return all(any(far((t*g[i]) % 7) for i in range(4)) for t in range(1, 7))

def conf_words(u, v):
    return CONF_LETTER[u[0],v[0]] and CONF_LETTER[u[1],v[1]] and CONF_LETTER[u[2],v[2]] and CONF_LETTER[u[3],v[3]]

def shiftw(w, t, g):
    return ((w[0]+t*g[0])%7,(w[1]+t*g[1])%7,(w[2]+t*g[2])%7,(w[3]+t*g[3])%7)


def orbit_graph(g):
    seen = np.zeros(NV, dtype=bool)
    orbits = []
    for i in range(NV):
        if seen[i]:
            continue
        w = id_to_word(i)
        members = list({shiftw(w, t, g) for t in range(7)})
        for mm in members:
            seen[word_to_id(mm)] = True
        orbits.append(members)
    K = len(orbits)
    reps = [o[0] for o in orbits]
    adjlist = [[] for _ in range(K)]
    for a in range(K):
        ra = reps[a]
        for b in range(a+1, K):
            if any(conf_words(ra, mb) for mb in orbits[b]):
                adjlist[a].append(b); adjlist[b].append(a)
    return orbits, adjlist

def greedy_mis(orbits, adjlist):
    K = len(orbits)
    deg = np.array([len(a) for a in adjlist])
    alive = np.ones(K, dtype=bool)
    chosen = []
    # min-degree greedy
    order = list(np.argsort(deg))
    for v in order:
        if alive[v]:
            chosen.append(v)
            alive[v] = False
            for u in adjlist[v]:
                alive[u] = False
    return chosen

def main():
    seen = set(); gens = []
    for g in itertools.product(range(7), repeat=4):
        if all(c == 0 for c in g):
            continue
        canon = min(tuple((s*c)%7 for c in g) for s in range(1, 7))
        if canon in seen:
            continue
        seen.add(canon)
        if gsi(g):
            gens.append(g)
    print("generators:", len(gens), flush=True)
    t0 = time.time()
    results = []
    for k, g in enumerate(gens):
        orbits, adjlist = orbit_graph(g)
        chosen = greedy_mis(orbits, adjlist)
        sz = sum(len(orbits[i]) for i in chosen)
        results.append((sz, g))
        if k % 30 == 0:
            print(f"[{time.time()-t0:.1f}s] screened {k}/{len(gens)} best so far {max(r[0] for r in results)}", flush=True)
    results.sort(reverse=True)
    print("TOP 15 generators by greedy orbit-union:")
    for sz, g in results[:15]:
        print("  ", sz, g, flush=True)
    json.dump([[sz, list(g)] for sz, g in results], open(os.path.join(HERE, "gen_screen.json"), "w"))

if __name__ == "__main__":
    main()
