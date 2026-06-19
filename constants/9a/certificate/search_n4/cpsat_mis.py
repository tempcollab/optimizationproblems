"""Exact MIS on C_7^⊠4 via CP-SAT, bounded-compute chunk.

Symmetry-breaking: Z_7^4 translation acts simply transitively on the 2401 vertices, so
WLOG some independent set containing the all-zero word 0000 is optimal up to translation.
We FIX x[0000] = 1 (the orbit representative). This is sound: if alpha = k, some max
indep set S exists; translate S by -s for any s in S to get a max indep set containing
0000 (translation is a graph automorphism since cdist is translation invariant on Z_7).

Also break the per-coordinate dihedral flip + coordinate-permutation symmetry lightly by
a lex constraint is hard to add cleanly; we rely on the 0000-fix + solver.

Persists incumbent set to incumbent.json each improvement (solution callback).
Prints best-so-far + bound + elapsed. Hard wall-clock cap from argv.
"""
import sys, json, time, os
import numpy as np
from ortools.sat.python import cp_model
from graph import build_adjacency, NV, word_to_id, id_to_word, DIM

HERE = os.path.dirname(os.path.abspath(__file__))
INCUMBENT = os.path.join(HERE, "incumbent.json")

def main():
    cap = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0
    t0 = time.time()
    arr, adj = build_adjacency()
    # edges as upper-triangular pairs
    iu, ju = np.where(np.triu(adj, 1))
    print(f"[{time.time()-t0:.1f}s] graph: {NV} verts, {len(iu)} edges", flush=True)

    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{i}") for i in range(NV)]
    for a, b in zip(iu.tolist(), ju.tolist()):
        m.Add(x[a] + x[b] <= 1)
    # symmetry-break: fix 0000 in the set
    z = word_to_id((0, 0, 0, 0))
    m.Add(x[z] == 1)
    m.Maximize(sum(x))

    # warm start from existing incumbent if present
    best_known = 0
    if os.path.exists(INCUMBENT):
        try:
            data = json.load(open(INCUMBENT))
            ids = data.get("ids", [])
            if ids:
                best_known = len(ids)
                hint_ids = set(ids)
                for i in range(NV):
                    m.AddHint(x[i], 1 if i in hint_ids else 0)
                print(f"[hint] warm-started from incumbent size {best_known}", flush=True)
        except Exception as e:
            print("hint load failed", e, flush=True)

    class CB(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
            self.best = best_known
        def on_solution_callback(self):
            cur = sum(int(self.Value(x[i])) for i in range(NV))
            if cur > self.best:
                self.best = cur
                ids = [i for i in range(NV) if self.Value(x[i])]
                json.dump({"ids": ids, "size": cur,
                           "words": [list(id_to_word(i)) for i in ids]},
                          open(INCUMBENT, "w"))
                print(f"[{time.time()-t0:.1f}s] incumbent {cur}", flush=True)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = cap
    solver.parameters.num_search_workers = 8
    solver.parameters.log_search_progress = False
    cb = CB()
    status = solver.Solve(m, cb)
    print(f"[{time.time()-t0:.1f}s] status={solver.StatusName(status)} "
          f"best={cb.best} bound={solver.BestObjectiveBound()}", flush=True)

if __name__ == "__main__":
    main()
