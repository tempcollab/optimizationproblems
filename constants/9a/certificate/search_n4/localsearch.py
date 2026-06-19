"""Stochastic local search for large independent set in C_7^⊠4.

Uses the (k,1)-swap / tabu "best-in / plateau" local search ("dynamic local search"
style, the family VZ2002 / MO2017 used). Maintains an independent set S; tries to
1-improve by adding a free vertex; if stuck, does a (1,2)/(2,3) swap (remove tight
vertices, add two that become free) to escape, with random restarts.

Bounded-compute: hard wall-clock cap from argv; prints best-so-far + elapsed each
report interval; persists best set to incumbent_ls.json.

Represents the graph by per-vertex neighbor lists (degree 80) for fast tightness updates.
"""
import sys, json, time, os, random
import numpy as np
from graph import build_adjacency, NV, id_to_word, word_to_id, DIM

HERE = os.path.dirname(os.path.abspath(__file__))
INC = os.path.join(HERE, "incumbent_ls.json")
INC_CPSAT = os.path.join(HERE, "incumbent.json")


def neighbor_lists(adj):
    return [np.where(adj[i])[0].tolist() for i in range(NV)]


class LS:
    def __init__(self, nbrs):
        self.nbrs = nbrs
        self.inS = np.zeros(NV, dtype=bool)
        # tight[v] = number of neighbors of v currently in S
        self.tight = np.zeros(NV, dtype=np.int32)
        self.S = set()

    def reset(self):
        self.inS[:] = False
        self.tight[:] = 0
        self.S = set()

    def add(self, v):
        self.inS[v] = True
        self.S.add(v)
        for u in self.nbrs[v]:
            self.tight[u] += 1

    def remove(self, v):
        self.inS[v] = False
        self.S.discard(v)
        for u in self.nbrs[v]:
            self.tight[u] -= 1

    def free_vertices(self):
        # vertices not in S with tight==0 (can be added)
        return [v for v in range(NV) if not self.inS[v] and self.tight[v] == 0]

    def greedy_extend(self, order=None):
        if order is None:
            order = list(range(NV))
            random.shuffle(order)
        for v in order:
            if not self.inS[v] and self.tight[v] == 0:
                self.add(v)

    def one_improvements(self):
        # add any free vertex
        added = True
        while added:
            added = False
            frees = [v for v in range(NV) if not self.inS[v] and self.tight[v] == 0]
            if frees:
                self.add(random.choice(frees))
                added = True
        return len(self.S)


def main():
    cap = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0
    seed_from = sys.argv[2] if len(sys.argv) > 2 else None
    t0 = time.time()
    arr, adj = build_adjacency()
    nbrs = neighbor_lists(adj)
    print(f"[{time.time()-t0:.1f}s] neighbor lists built", flush=True)

    ls = LS(nbrs)
    best_set = []
    best = 0
    # load prior best
    for f in (INC, INC_CPSAT):
        if os.path.exists(f):
            try:
                d = json.load(open(f))
                if d.get("size", 0) > best:
                    best = d["size"]; best_set = d["ids"]
            except Exception:
                pass
    print(f"[start] prior best {best}", flush=True)

    last_report = time.time()
    restarts = 0
    # force-fix 0000 each restart (symmetry rep) for consistency
    z = word_to_id((0, 0, 0, 0))

    while time.time() - t0 < cap:
        ls.reset()
        ls.add(z)
        # random greedy
        ls.one_improvements()
        # plateau / (2,3)-swap local search for a budget of iterations
        cur = len(ls.S)
        no_improve = 0
        while time.time() - t0 < cap and no_improve < 4000:
            cur = len(ls.S)
            if cur > best:
                best = cur
                best_set = sorted(ls.S)
                json.dump({"ids": best_set, "size": best,
                           "words": [list(id_to_word(i)) for i in best_set]},
                          open(INC, "w"))
                print(f"[{time.time()-t0:.1f}s] NEW best {best} (restart {restarts})", flush=True)
                no_improve = 0
            # perturbation: remove 1-2 random vertices from S, then greedily re-extend
            if len(ls.S) >= 2:
                victims = random.sample(list(ls.S - {z}), min(2, len(ls.S) - 1)) if len(ls.S) > 1 else []
                for v in victims:
                    ls.remove(v)
            ls.one_improvements()
            no_improve += 1
            if time.time() - last_report > 20:
                print(f"[{time.time()-t0:.1f}s] best={best} cur={len(ls.S)} restarts={restarts}", flush=True)
                last_report = time.time()
        restarts += 1

    print(f"[{time.time()-t0:.1f}s] DONE best={best} restarts={restarts}", flush=True)

if __name__ == "__main__":
    main()
