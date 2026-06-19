"""C_7^⊠4 conflict graph — adjacency identical to the Lean engine (C9.lean).

A vertex is a word in Z_7^4. cdist(a,b) = min(|a-b|, 7-|a-b|).
Two letters are *confusable* iff cdist <= 1. Two words are *confusable* (= ADJACENT
in the strong power, i.e. they cannot both be in an independent set) iff EVERY
coordinate is confusable. Two words are *independent* iff SOME coordinate has cdist >= 2.

An independent set = a set of words pairwise independent (a "code").
"""
import itertools
import numpy as np

N = 7
DIM = 4
NV = N ** DIM  # 2401

# cyclic distance table on Z_7
CD = np.zeros((N, N), dtype=np.int8)
for a in range(N):
    for b in range(N):
        d = abs(a - b)
        CD[a, b] = min(d, N - d)

# confusable letters: cdist <= 1
CONF_LETTER = (CD <= 1)  # 7x7 bool


def words():
    return list(itertools.product(range(N), repeat=DIM))


def word_to_id(w):
    i = 0
    for c in w:
        i = i * N + c
    return i


def id_to_word(i):
    w = []
    for _ in range(DIM):
        w.append(i % N)
        i //= N
    return tuple(reversed(w))


def confusable(u, v):
    """True iff u,v adjacent in strong power (every coord confusable)."""
    for i in range(DIM):
        if not CONF_LETTER[u[i], v[i]]:
            return False
    return True


def build_adjacency():
    """Return adjacency as a list of frozensets/bitsets is heavy (2401 verts).
    Instead build a boolean NV x NV would be 2401^2 = 5.76M bytes ok."""
    W = words()
    arr = np.array(W, dtype=np.int8)  # NV x 4
    # adjacency: for each pair, all coords confusable
    # Build via per-coordinate confusable matrices then AND across coords.
    adj = np.ones((NV, NV), dtype=bool)
    for c in range(DIM):
        col = arr[:, c]  # NV
        # confusable per coordinate: CONF_LETTER[col[i], col[j]]
        cm = CONF_LETTER[np.ix_(col, col)]  # NV x NV bool
        adj &= cm
    np.fill_diagonal(adj, False)  # no self-loops
    return arr, adj


if __name__ == "__main__":
    arr, adj = build_adjacency()
    deg = adj.sum(axis=1)
    print("NV", NV, "edges", adj.sum() // 2)
    print("degree min/mean/max", deg.min(), deg.mean(), deg.max())
    # sanity: word 0000 neighbors should be words where every coord in {0,1,6} (cdist<=1)
    z = word_to_id((0, 0, 0, 0))
    nbr = np.where(adj[z])[0]
    # each coord can be 0,1,6 -> 3 choices -> 3^4 = 81, minus self = 80
    print("deg(0000) =", len(nbr), "expected", 3 ** DIM - 1)
