"""Weighted orbit-MIS solver (CP-SAT, time-limited) + greedy fallback."""
from ortools.sat.python import cp_model

def greedy_weighted_mis(weights, adj, order=None):
    m = len(weights)
    if order is None:
        # by weight desc then degree asc
        order = sorted(range(m), key=lambda i: (-weights[i], len(adj[i])))
    chosen = []
    banned = set()
    for i in order:
        if i in banned:
            continue
        chosen.append(i)
        for j in adj[i]:
            banned.add(j)
    return chosen

def cpsat_weighted_mis(weights, adj, time_limit, warmstart=None, workers=8):
    m = len(weights)
    model = cp_model.CpModel()
    x = [model.NewBoolVar(f"x{i}") for i in range(m)]
    added = set()
    for i in range(m):
        for j in adj[i]:
            if i < j:
                model.Add(x[i] + x[j] <= 1)
                added.add((i, j))
    model.Maximize(sum(weights[i] * x[i] for i in range(m)))
    if warmstart is not None:
        ws = set(warmstart)
        for i in range(m):
            model.AddHint(x[i], 1 if i in ws else 0)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    status = solver.Solve(model)
    chosen = [i for i in range(m) if solver.Value(x[i]) == 1]
    total = sum(weights[i] for i in chosen)
    return chosen, total, solver.StatusName(status), solver.BestObjectiveBound()
