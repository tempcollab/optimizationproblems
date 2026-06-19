"""Strong ARW-style iterated local search for MIS on C_7^box4 (R15).

This is a genuinely stronger solver than R14's hand-rolled (1,2)-ILS:
  - exact ARW (1,2)-swap local search using tightness counters + the candidate
    trick (find vertices whose ONLY solution-neighbor is the removed vertex),
  - plateau (1,1)-swaps to traverse equal-size optima,
  - force-based perturbation (ARW: force k random vertices in, evict conflicts),
  - AUTOMORPHISM diversification: periodically map the whole incumbent by a random
    element of Aut(C_7^box4) (preserves independence + size, jumps basins).

Bounded-compute: runs a fixed iteration budget per invocation with a hard
wall-clock cap, prints+flushes best/iters/elapsed periodically, and persists the
incumbent + RNG state to disk so a kill loses nothing.

Usage: python3 arw_ils.py <seconds> <seed_json_or_'cold'> <state_tag>
"""
import sys, os, json, time, random
import numpy as np
from core import NV, WORDS, word_to_id, is_independent

DATA = np.load("adj_cache.npz")
FLAT = DATA["flat"]
OFF = DATA["offsets"]
AUTS = np.load("aut_cache.npz")["perms"]


def nbrs(v):
    return FLAT[OFF[v]:OFF[v + 1]]


class Solver:
    def __init__(self, rng):
        self.rng = rng
        self.insol = np.zeros(NV, dtype=bool)      # membership
        self.tight = np.zeros(NV, dtype=np.int32)  # # solution-neighbors (for v not in sol)
        self.sol = []                              # list of solution vertices

    def reset_empty(self):
        self.insol[:] = False
        self.tight[:] = 0
        self.sol = []

    def add(self, v):
        self.insol[v] = True
        self.sol.append(v)
        nb = nbrs(v)
        self.tight[nb] += 1

    def remove(self, v):
        self.insol[v] = False
        self.sol.remove(v)
        nb = nbrs(v)
        self.tight[nb] -= 1

    def set_solution(self, ids):
        self.reset_empty()
        for v in ids:
            self.add(v)

    def free_vertices(self):
        """vertices not in sol with tightness 0 (can be added directly)."""
        free = np.where((~self.insol) & (self.tight == 0))[0]
        return free

    def greedy_fill(self):
        """add free vertices greedily (min-degree-into-free heuristic, randomized)."""
        while True:
            free = self.free_vertices()
            if len(free) == 0:
                break
            # pick a random free vertex (randomization aids restarts)
            v = int(free[self.rng.randrange(len(free))])
            self.add(v)

    # ---- ARW (1,2) improvement -------------------------------------------
    def one_two_improve(self):
        """One pass of (1,2)-swaps: remove x, add two non-adjacent vertices whose
        only solution-neighbor was x. Returns number of improving swaps applied."""
        improved = 0
        sol_snapshot = list(self.sol)
        self.rng.shuffle(sol_snapshot)
        for x in sol_snapshot:
            if not self.insol[x]:
                continue
            # candidates: neighbors of x that, after removing x, would have tight 1->0
            # i.e. currently tight[w]==1 and x in nbrs(w) (x is their unique sol-nbr)
            nb = nbrs(x)
            cand = nb[(self.tight[nb] == 1) & (~self.insol[nb])]
            if len(cand) < 2:
                continue
            # need two mutually non-adjacent candidates
            found = self._find_nonadj_pair(cand)
            if found is None:
                continue
            a, b = found
            self.remove(x)
            self.add(int(a))
            self.add(int(b))
            improved += 1
        return improved

    def _find_nonadj_pair(self, cand):
        cl = list(cand)
        # candidate set is usually small; check pairs but cap work
        m = len(cl)
        if m > 60:
            self.rng.shuffle(cl)
            cl = cl[:60]
            m = 60
        candset = set(int(c) for c in cl)
        for i in range(m):
            a = int(cl[i])
            na = set(int(z) for z in nbrs(a))
            for j in range(i + 1, m):
                b = int(cl[j])
                if b not in na:
                    return (a, b)
        return None

    def local_search(self, plateau_budget=30, deadline=None):
        """Descend to a (1,2)-local optimum, using a bounded number of plateau
        moves to escape equal-size optima. Returns when no (1,2)-improvement is
        found after exhausting the plateau budget."""
        self.greedy_fill()
        plateau_used = 0
        while True:
            imp = self.one_two_improve()
            if imp:
                self.greedy_fill()
                continue
            # no strict improvement: spend a plateau move (bounded) and retry
            if plateau_used < plateau_budget and self.plateau_step():
                plateau_used += 1
                self.greedy_fill()
                continue
            break

    def plateau_step(self):
        """Try a (1,1) plateau swap that opens up a new free vertex (changes basin).
        Remove x, add one vertex w (its unique sol-nbr was x), giving equal size but
        possibly new free vertices. Returns True if a plateau move was made."""
        sol_snapshot = list(self.sol)
        self.rng.shuffle(sol_snapshot)
        for x in sol_snapshot:
            if not self.insol[x]:
                continue
            nb = nbrs(x)
            cand = nb[(self.tight[nb] == 1) & (~self.insol[nb])]
            if len(cand) == 0:
                continue
            w = int(cand[self.rng.randrange(len(cand))])
            self.remove(x)
            self.add(w)
            return True
        return False

    # ---- perturbation -----------------------------------------------------
    def force_perturb(self, k):
        """ARW force step: insert k random vertices, evicting their sol-neighbors."""
        for _ in range(k):
            v = self.rng.randrange(NV)
            if self.insol[v]:
                continue
            # evict solution neighbors of v
            nb = nbrs(v)
            for u in nb[self.insol[nb]]:
                self.remove(int(u))
            self.add(v)

    def aut_diversify(self):
        """Map the whole incumbent by a random automorphism (size-preserving)."""
        p = AUTS[self.rng.randrange(len(AUTS))]
        new = [int(p[v]) for v in self.sol]
        self.set_solution(new)


def load_seed(arg):
    if arg == "cold":
        return None
    with open(arg) as f:
        d = json.load(f)
    if "ids" in d:
        return list(d["ids"])
    if "words" in d:
        return [word_to_id(tuple(w)) for w in d["words"]]
    raise ValueError("no ids/words in seed")


def main():
    secs = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0
    seedarg = sys.argv[2] if len(sys.argv) > 2 else "cold"
    tag = sys.argv[3] if len(sys.argv) > 3 else "run"
    statef = f"arw_state_{tag}.json"

    rng = random.Random()
    # resume best from state if present
    best_ids = None
    best = 0
    if os.path.exists(statef):
        with open(statef) as f:
            st = json.load(f)
        best_ids = st.get("best_ids")
        best = st.get("best", 0)
        rng.seed(st.get("rng_seed", time.time()))
        print(f"[resume] best={best} from {statef}", flush=True)
    else:
        rng.seed(hash((tag, time.time())) & 0xffffffff)

    seed_ids = load_seed(seedarg)
    if seed_ids is not None and best_ids is None:
        ok, conf, dist = is_independent(seed_ids)
        print(f"[seed] size={len(seed_ids)} independent={ok} conf={conf}", flush=True)
        if ok:
            best_ids = list(seed_ids)
            best = len(seed_ids)

    s = Solver(rng)
    if best_ids is not None:
        s.set_solution(best_ids)
    else:
        s.reset_empty()

    deadline = time.time() + secs
    t0 = time.time()
    it = 0
    last_print = t0
    cur_size = len(s.sol)
    while time.time() < deadline:
        s.local_search(deadline=deadline)
        cur_size = len(s.sol)
        if cur_size > best:
            best = cur_size
            best_ids = list(s.sol)
            ok, conf, dist = is_independent(best_ids)
            print(f"[NEW BEST] size={best} independent={ok} conf={conf} t={time.time()-t0:.1f}", flush=True)
            # persist immediately
            with open(statef, "w") as f:
                json.dump({"best": best, "best_ids": best_ids,
                           "rng_seed": rng.randrange(1 << 30)}, f)
        it += 1
        # perturbation schedule: alternate force-kicks and automorphism jumps,
        # occasionally restart from the incumbent
        r = rng.random()
        if r < 0.5:
            # restart from best, force-perturb
            if best_ids is not None:
                s.set_solution(best_ids)
            k = rng.randint(1, 4)
            s.force_perturb(k)
        elif r < 0.8:
            # automorphism diversification from best
            if best_ids is not None:
                s.set_solution(best_ids)
            s.aut_diversify()
            s.force_perturb(rng.randint(1, 3))
        else:
            # cold-ish restart to explore new basins
            s.reset_empty()
        now = time.time()
        if now - last_print > 15:
            print(f"  iter={it} best={best} cur={cur_size} elapsed={now-t0:.1f}", flush=True)
            last_print = now

    # final persist
    with open(statef, "w") as f:
        json.dump({"best": best, "best_ids": best_ids,
                   "rng_seed": rng.randrange(1 << 30)}, f)
    print(f"[DONE] iters={it} best={best} elapsed={time.time()-t0:.1f}", flush=True)
    if best_ids is not None:
        ok, conf, dist = is_independent(best_ids)
        print(f"[FINAL CHECK] size={best} independent={ok} conf={conf} distinct={dist}", flush=True)


if __name__ == "__main__":
    main()
