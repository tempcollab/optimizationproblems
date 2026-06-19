"""Sweep a family of non-order-7 generators: build conflict graph, greedy orbit-MIS,
report best total + internal-indep orbit stats. Bounded-compute: persists best to JSON."""
import itertools, json, sys, time, random
from engine import *
from solve_mis import greedy_weighted_mis, cpsat_weighted_mis

PERMS = {
  'id': (0,1,2,3,4),
  '5cyc': (1,2,3,4,0),
  '2cyc': (1,0,2,3,4),
  '3cyc': (1,2,0,3,4),
  '2+2': (1,0,3,2,4),
  '2+3': (1,0,3,4,2),
  '4cyc': (1,2,3,0,4),
}

STATE = 'sweep_state.json'

def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {'best_total': 0, 'best_gen': None, 'best_words': None, 'tried': []}

def save_state(s):
    json.dump(s, open(STATE, 'w'))

def eval_gen(pname, perm, b, cpsat_time=0):
    orbits = all_orbits(perm, b)
    good, weights, adj = build_conflict_graph(orbits)
    if not good:
        return 0, [], good, weights, adj
    g = greedy_weighted_mis(weights, adj)
    gt = sum(weights[i] for i in g)
    best_sel, best_tot = g, gt
    if cpsat_time > 0:
        chosen, total, st, bnd = cpsat_weighted_mis(weights, adj, time_limit=cpsat_time, warmstart=g)
        if total > best_tot:
            best_sel, best_tot = chosen, total
    words = []
    for i in best_sel:
        words.extend(good[i])
    return best_tot, words, good, weights, adj

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'greedy'
    cpsat_time = float(sys.argv[2]) if len(sys.argv) > 2 else 0
    seed_start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    n_b = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    only_perm = sys.argv[5] if len(sys.argv) > 5 else None
    t0 = time.time()
    s = load_state()
    perms = {only_perm: PERMS[only_perm]} if only_perm else PERMS
    for pname, perm in perms.items():
        for k in range(seed_start, seed_start + n_b):
            random.seed(1000*hash(pname) % 99991 + k)
            b = tuple(random.randrange(Q) for _ in range(N))
            key = f"{pname}:{b}"
            if key in s['tried']:
                continue
            tot, words, good, weights, adj = eval_gen(pname, perm, b, cpsat_time)
            n_good = len(good)
            s['tried'].append(key)
            if tot > s['best_total']:
                s['best_total'] = tot
                s['best_gen'] = {'perm': list(perm), 'b': list(b), 'pname': pname}
                s['best_words'] = [list(w) for w in words]
                save_state(s)
            print(f"[{round(time.time()-t0,1)}s] {pname} b={b} good_orbits={n_good} total={tot} BEST={s['best_total']}", flush=True)
            save_state(s)
    print(f"DONE best={s['best_total']} gen={s['best_gen']} elapsed={round(time.time()-t0,1)}", flush=True)
