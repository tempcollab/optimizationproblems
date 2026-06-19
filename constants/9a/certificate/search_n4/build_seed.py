"""Construct a strong seed for C_7^⊠4 from known sub-structure.

1. Find alpha(C_7^⊠2)=10 optimal set via CP-SAT (tiny, 49 verts).
2. Product 10x10 = 100 set in C_7^⊠4 (independent: if (a,b) indep-pair in C_7^⊠2 means
   some coord differs by >=2; product of two such on coords (0,1) and (2,3) is indep iff
   the first half OR second half is indep -> actually product of independent sets: words
   (u1,u2) with u1 in A2, u2 in A2; two such are confusable iff both halves confusable;
   since A2 independent, two distinct words differ in some half by an independent pair...
   NOT automatically: if u1=v1 but u2,v2 are a confusable pair? u2,v2 in A2 distinct =>
   independent. So (u,v) confusable needs u1~v1 AND u2~v2; if u1=v1 then need u2~v2 but
   distinct A2 words are independent => not confusable. If u1!=v1 (distinct A2) independent
   => not confusable. So the product IS independent. Good: 100.)
3. Save product as a seed, then a Z_7 diagonal-orbit augmented version.
"""
import json, os
import numpy as np
from ortools.sat.python import cp_model
from graph import CONF_LETTER, id_to_word, word_to_id, NV

HERE = os.path.dirname(os.path.abspath(__file__))


def alpha_n2():
    # vertices Z_7^2, confusable iff both coords confusable
    import itertools
    V = list(itertools.product(range(7), repeat=2))
    idx = {v: i for i, v in enumerate(V)}
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{i}") for i in range(len(V))]
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            a, b = V[i], V[j]
            if CONF_LETTER[a[0], b[0]] and CONF_LETTER[a[1], b[1]]:
                m.Add(x[i] + x[j] <= 1)
    m.Maximize(sum(x))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 30
    s.Solve(m)
    A = [V[i] for i in range(len(V)) if s.Value(x[i])]
    return A


def main():
    A2 = alpha_n2()
    print("alpha(C_7^2) found:", len(A2), A2)
    # product set in Z_7^4
    prod = []
    for u in A2:
        for w in A2:
            prod.append((u[0], u[1], w[0], w[1]))
    ids = sorted(word_to_id(p) for p in prod)
    print("product size", len(ids))
    # verify independence
    from graph import build_adjacency
    arr, adj = build_adjacency()
    bad = 0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if adj[ids[i], ids[j]]:
                bad += 1
    print("product confusable pairs:", bad)
    json.dump({"ids": ids, "size": len(ids),
               "words": [list(id_to_word(i)) for i in ids]},
              open(os.path.join(HERE, "seed_product.json"), "w"))

if __name__ == "__main__":
    main()
