"""
Strong feasible-only iterated local search (ILS) MIS on C_7^box4, the proper version.

Core loop (Andrade-Resende-Werneck style (1,2)-swap local search):
  - free(u): u not in S and tight[u]==0  -> can add for +1.
  - (1,2)-swap: a vertex v in S with exactly two "1-tight" neighbors u1,u2 (each whose only
    S-neighbor is v) that are mutually non-adjacent  -> drop v, add u1,u2  for +1.
  We scan ALL of S for a (1,2)-swap each round (not just one random v), making it a true
  local optimum before perturbing.  Perturbation: force-add g random vertices (removing their
  S-neighbors), then re-optimize.  Restart from best on stagnation.

Seeds optionally from a JSON. Persists best feasible each improvement.

Usage: python3 ils_mis.py [seed_json|-] [budget_s] [out_json] [pert_g]
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
            adj[i].append(VIDX[tuple((w[k] + d[k]) % 7 for k in range(N))])
    return adj


ADJ = build_adj()
ADJSET = [set(a) for a in ADJ]


class Sol:
    __slots__ = ("inS", "tight", "size")

    def __init__(self):
        self.inS = bytearray(NV)
        self.tight = [0] * NV
        self.size = 0

    def add(self, u):
        self.inS[u] = 1
        self.size += 1
        for w in ADJ[u]:
            self.tight[w] += 1

    def rem(self, u):
        self.inS[u] = 0
        self.size -= 1
        for w in ADJ[u]:
            self.tight[w] -= 1

    def copy_from(self, other):
        self.inS = bytearray(other.inS)
        self.tight = list(other.tight)
        self.size = other.size


def greedy_fill(sol, rng):
    order = list(range(NV)); rng.shuffle(order)
    for u in order:
        if not sol.inS[u] and sol.tight[u] == 0:
            sol.add(u)


def local_opt(sol, rng):
    """Run add-moves and (1,2)-swaps to a local optimum."""
    improved = True
    while improved:
        improved = False
        # add moves
        frees = [u for u in range(NV) if not sol.inS[u] and sol.tight[u] == 0]
        if frees:
            rng.shuffle(frees)
            for u in frees:
                if not sol.inS[u] and sol.tight[u] == 0:
                    sol.add(u)
            improved = True
            continue
        # (1,2)-swap scan over S
        Slist = [u for u in range(NV) if sol.inS[u]]
        rng.shuffle(Slist)
        did = False
        for v in Slist:
            # 1-tight neighbors of v whose unique S-neighbor is v
            ok = []
            for u in ADJ[v]:
                if not sol.inS[u] and sol.tight[u] == 1:
                    # confirm unique S-neighbor is v
                    cnt = 0; only = -1
                    for w in ADJ[u]:
                        if sol.inS[w]:
                            cnt += 1; only = w
                            if cnt > 1:
                                break
                    if cnt == 1 and only == v:
                        ok.append(u)
            if len(ok) >= 2:
                found = None
                for i in range(len(ok)):
                    for j in range(i + 1, len(ok)):
                        if ok[j] not in ADJSET[ok[i]]:
                            found = (ok[i], ok[j]); break
                    if found:
                        break
                if found:
                    sol.rem(v); sol.add(found[0]); sol.add(found[1])
                    did = True
                    break
        if did:
            improved = True


def plateau_swap(sol, rng, tries=8):
    """Do up to `tries` 0-gain (1,1)-swaps: drop v in S, add a 1-tight neighbor u (whose only
    S-neighbor is v). Moves along equal-size local optima to diversify."""
    for _ in range(tries):
        Slist = [u for u in range(NV) if sol.inS[u]]
        if not Slist:
            return
        v = rng.choice(Slist)
        cands = []
        for u in ADJ[v]:
            if not sol.inS[u] and sol.tight[u] == 1:
                cands.append(u)
        if cands:
            u = rng.choice(cands)
            # u may have another S-neighbor besides v? tight==1 means exactly one S-neighbor;
            # is it v? It is adjacent to v and tight 1, so its unique S-neighbor is v.
            sol.rem(v); sol.add(u)


def perturb(sol, rng, g):
    """Force-add g random vertices, removing their S-neighbors."""
    for _ in range(g):
        u = rng.randrange(NV)
        if sol.inS[u]:
            continue
        for w in list(ADJ[u]):
            if sol.inS[w]:
                sol.rem(w)
        sol.add(u)


def main():
    seed_json = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "-" else None
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 240.0
    out_json = sys.argv[3] if len(sys.argv) > 3 else "ils_best.json"
    pert_g = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    t0 = time.time()
    rng = random.Random(20240619)
    cur = Sol()
    if seed_json:
        with open(seed_json) as f:
            data = json.load(f)
        for w in data["words"]:
            u = VIDX[tuple(w)]
            if not cur.inS[u] and cur.tight[u] == 0:
                cur.add(u)
        print(f"seeded {cur.size} from {seed_json}", flush=True)
    greedy_fill(cur, rng)
    local_opt(cur, rng)
    best = Sol(); best.copy_from(cur)
    print(f"init local-opt size={cur.size} ({time.time()-t0:.1f}s)", flush=True)

    def save():
        words = [list(VERTS[u]) for u in range(NV) if best.inS[u]]
        with open(out_json, "w") as f:
            json.dump({"num_verts": len(words), "words": words}, f)

    save()
    last_print = t0
    stall = 0
    # accept the WORKING solution (random-walk style) to diversify; track best separately.
    while time.time() - t0 < budget:
        g = pert_g + (rng.randint(0, 6) if stall > 30 else 0)
        perturb(cur, rng, g)
        local_opt(cur, rng)
        # plateau wander: try a few 0-gain swaps to move along equal-size local optima
        plateau_swap(cur, rng, tries=8)
        if cur.size > best.size:
            best.copy_from(cur); save(); stall = 0
            print(f"  best={best.size} ({time.time()-t0:.1f}s)", flush=True)
        elif cur.size < best.size - 3:
            # too far below: restart from best occasionally
            if rng.random() < 0.5:
                cur.copy_from(best)
            stall += 1
        else:
            stall += 1
        if stall > 120:
            cur.copy_from(best)
            perturb(cur, rng, pert_g + rng.randint(2, 8))
            local_opt(cur, rng)
            if cur.size > best.size:
                best.copy_from(cur); save()
                print(f"  best={best.size} ({time.time()-t0:.1f}s)", flush=True)
            stall = 0
        if time.time() - last_print > 30:
            last_print = time.time()
            print(f"  ... cur={cur.size} best={best.size} ({time.time()-t0:.1f}s)", flush=True)
    save()
    print(f"DONE best={best.size} saved {out_json} ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
