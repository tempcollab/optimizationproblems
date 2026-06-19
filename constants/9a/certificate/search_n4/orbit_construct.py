"""Z_7 diagonal-orbit construction for C_7^⊠4.

Orbits under t -> word + t*(1,1,1,1) mod 7 (size 7 each, 2401/7 = 343 orbits).
cdist is translation invariant, so confusability is translation invariant: if we add
the SAME diagonal shift to two words their confusability is unchanged. An orbit O_r is
"self-independent" iff the rep r and r+t*(1,1,1,1) are independent for all t=1..6 (since
the orbit is closed under the shift and shift preserves confusability, pairwise within
the orbit reduces to rep-vs-shifts). Two orbits O_r, O_s are mutually independent iff
EVERY cross pair is independent.

We:
 1. Find self-independent orbits.
 2. Build the orbit-conflict graph on those: O_r ~ O_s if some cross-pair confusable.
 3. MIS on that graph (CP-SAT) -> union of orbits, each contributing 7.
Then optionally local-repair.
"""
import json, os, itertools
import numpy as np
from ortools.sat.python import cp_model
from graph import build_adjacency, NV, id_to_word, word_to_id, CONF_LETTER

HERE = os.path.dirname(os.path.abspath(__file__))


def shift(w, t):
    return tuple((c + t) % 7 for c in w)


def conf_words(u, v):
    return all(CONF_LETTER[u[i], v[i]] for i in range(4))


def main():
    arr, adj = build_adjacency()
    # orbit reps: canonical = min id in orbit
    seen = np.zeros(NV, dtype=bool)
    orbits = []  # list of (rep_word, [member words])
    for i in range(NV):
        if seen[i]:
            continue
        w = id_to_word(i)
        members = [shift(w, t) for t in range(7)]
        for m in members:
            seen[word_to_id(m)] = True
        orbits.append(members)
    print("num orbits", len(orbits))
    # self-independent orbits: rep vs all shifts independent
    selfind = []
    for members in orbits:
        r = members[0]
        ok = all(not conf_words(r, members[t]) for t in range(1, 7))
        if ok:
            selfind.append(members)
    print("self-independent orbits", len(selfind))
    # orbit-conflict graph
    K = len(selfind)
    reps = [o[0] for o in selfind]
    # O_a ~ O_b iff exists cross pair confusable. By translation invariance, suffices to
    # check rep_a vs all shifts of rep_b (a+t' vs b == a vs b-t'), i.e. r_a vs members_b.
    confG = np.zeros((K, K), dtype=bool)
    for a in range(K):
        ra = reps[a]
        for b in range(a + 1, K):
            mb = selfind[b]
            c = any(conf_words(ra, mb[t]) for t in range(7))
            confG[a, b] = confG[b, a] = c
    print("orbit-conflict graph built, edges", confG.sum() // 2)
    # MIS on orbit graph, each orbit weight 7
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"o{i}") for i in range(K)]
    iu, ju = np.where(np.triu(confG, 1))
    for a, b in zip(iu.tolist(), ju.tolist()):
        m.Add(x[a] + x[b] <= 1)
    m.Maximize(sum(x))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 120
    s.parameters.num_search_workers = 8
    st = s.Solve(m)
    chosen = [i for i in range(K) if s.Value(x[i])]
    print("orbits chosen", len(chosen), "-> vertices", 7 * len(chosen),
          "status", s.StatusName(st), "bound", s.BestObjectiveBound())
    # assemble vertex set
    ids = []
    for i in chosen:
        for w in selfind[i]:
            ids.append(word_to_id(w))
    ids = sorted(set(ids))
    # verify
    bad = 0
    for i in range(len(ids)):
        row = adj[ids[i]]
        for j in range(i + 1, len(ids)):
            if row[ids[j]]:
                bad += 1
    print("orbit-union size", len(ids), "confusable pairs", bad)
    if bad == 0:
        json.dump({"ids": ids, "size": len(ids),
                   "words": [list(id_to_word(i)) for i in ids]},
                  open(os.path.join(HERE, "seed_orbit.json"), "w"))
        print("saved seed_orbit.json")

if __name__ == "__main__":
    main()
