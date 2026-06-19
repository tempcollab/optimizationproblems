"""General Z_7-orbit construction over all shift generators g=(g0,g1,g2,g3).

Orbit of w under t->w+t*g mod 7. Self-independent iff for all t in 1..6, some coord i has
(t*g_i mod 7) in {2,3,4,5} (cdist of t*g_i from 0 is >=2). Note this depends only on g,
not w (translation invariance), so EITHER every orbit under g is self-independent or none.
Pick the best generator(s), build orbit-conflict graph, MIS. Try all g (7^4=2401), filter
to self-independent generators, then for each run orbit MIS, keep best.
"""
import json, os, itertools
import numpy as np
from ortools.sat.python import cp_model
from graph import build_adjacency, NV, id_to_word, word_to_id, CONF_LETTER

HERE = os.path.dirname(os.path.abspath(__file__))


def far(x):  # cdist from 0 >= 2
    return min(x % 7, (7 - x) % 7) >= 2


def gen_self_indep(g):
    for t in range(1, 7):
        if not any(far((t * g[i]) % 7) for i in range(4)):
            return False
    return True


def conf_words(u, v):
    return all(CONF_LETTER[u[i], v[i]] for i in range(4))


def shiftw(w, t, g):
    return tuple((w[i] + t * g[i]) % 7 for i in range(4))


def orbit_mis(g, adj, cap=20):
    # orbits under g: partition Z_7^4. rep = canonical min id.
    seen = np.zeros(NV, dtype=bool)
    orbits = []
    for i in range(NV):
        if seen[i]:
            continue
        w = id_to_word(i)
        members = [shiftw(w, t, g) for t in range(7)]
        # orbit may be smaller if g has order <7 in some sense, but g!=0 over Z_7 prime =>
        # t*g cycles through 7 distinct multiples unless g=0 vector. Distinct members.
        mset = set(members)
        for mm in mset:
            seen[word_to_id(mm)] = True
        orbits.append(sorted(mset, key=word_to_id))
    K = len(orbits)
    reps = [o[0] for o in orbits]
    # conflict: O_a~O_b iff rep_a confusable with some member of O_b
    confG = np.zeros((K, K), dtype=bool)
    for a in range(K):
        ra = reps[a]
        for b in range(a + 1, K):
            c = any(conf_words(ra, mb) for mb in orbits[b])
            confG[a, b] = confG[b, a] = c
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"o{i}") for i in range(K)]
    iu, ju = np.where(np.triu(confG, 1))
    for a, b in zip(iu.tolist(), ju.tolist()):
        m.Add(x[a] + x[b] <= 1)
    # weight = orbit size
    m.Maximize(sum(len(orbits[i]) * x[i] for i in range(K)))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = cap
    s.parameters.num_search_workers = 8
    s.Solve(m)
    chosen = [i for i in range(K) if s.Value(x[i])]
    ids = sorted({word_to_id(w) for i in chosen for w in orbits[i]})
    return ids


def main():
    arr, adj = build_adjacency()
    # canonicalize generators up to scaling (t*g gives same orbit family) and coord perms;
    # just dedup by orbit of g under Z_7^* scaling
    gens = []
    seen = set()
    for g in itertools.product(range(7), repeat=4):
        if all(c == 0 for c in g):
            continue
        # canonical scaling rep
        canon = min(tuple((s * c) % 7 for c in g) for s in range(1, 7))
        if canon in seen:
            continue
        seen.add(canon)
        if gen_self_indep(g):
            gens.append(g)
    print("self-independent generators (up to scaling):", len(gens))
    best = 0; best_ids = []; best_g = None
    for k, g in enumerate(gens):
        ids = orbit_mis(g, adj, cap=15)
        if len(ids) > best:
            best = len(ids); best_ids = ids; best_g = g
            print(f"gen {g}: orbit-union {len(ids)}  (NEW best {best})", flush=True)
        else:
            print(f"gen {g}: orbit-union {len(ids)}", flush=True)
    print("BEST orbit-union", best, "gen", best_g)
    if best_ids:
        # verify
        bad = sum(1 for i in range(len(best_ids)) for j in range(i+1, len(best_ids))
                  if adj[best_ids[i], best_ids[j]])
        print("verify confusable pairs:", bad)
        json.dump({"ids": best_ids, "size": best, "gen": list(best_g),
                   "words": [list(id_to_word(i)) for i in best_ids]},
                  open(os.path.join(HERE, "seed_orbit.json"), "w"))
        print("saved")

if __name__ == "__main__":
    main()
