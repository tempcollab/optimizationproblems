"""
Core C_7^box4 graph utilities for the orbit-restricted independent-set search.

Adjacency rule (matches the R13 Lean engine in lean/Constants/C9.lean):
  cdist(a,b) = min(d, 7-d) where d = |a-b|  (a,b in 0..6)
  confusable(a,b) = (cdist(a,b) <= 1)
  Two words u,v (length 4) are CONFUSABLE iff EVERY coordinate is confusable.
  Independent (non-adjacent) iff SOME coordinate has cdist >= 2.

n = 4, so vertices = Z_7^4 = 2401 codewords.
"""

from itertools import product

N = 4          # power
Q = 7          # alphabet C_7


def cdist(a, b):
    d = abs(a - b)
    return min(d, 7 - d)


# precompute confusable table on letters 0..6
CONF = [[1 if cdist(a, b) <= 1 else 0 for b in range(7)] for a in range(7)]


def confusable_word(u, v):
    """True iff u,v confusable (adjacent or equal) in C_7^box4."""
    for i in range(N):
        if not CONF[u[i]][v[i]]:
            return False
    return True


def independent_word(u, v):
    """True iff u,v non-confusable (some coord cdist>=2)."""
    return not confusable_word(u, v)


# all 2401 vertices as tuples, with a stable index
VERTS = [tuple(w) for w in product(range(7), repeat=N)]
VIDX = {w: i for i, w in enumerate(VERTS)}
NV = len(VERTS)
assert NV == 7 ** N == 2401


def encode(w):
    """Pack a word into an int base 7."""
    x = 0
    for c in w:
        x = x * 7 + c
    return x


def check_independent_set(words):
    """Brute-check a list of words is pairwise independent and distinct.
    Returns (ok, num_confusable_pairs, num_distinct)."""
    ws = [tuple(w) for w in words]
    distinct = len(set(ws))
    bad = 0
    M = len(ws)
    for i in range(M):
        ui = ws[i]
        for j in range(i + 1, M):
            if confusable_word(ui, ws[j]):
                bad += 1
    return (bad == 0 and distinct == M, bad, distinct)


if __name__ == "__main__":
    # sanity: independence rule self-test against a couple of known facts
    # 0 and 1 confusable (cdist 1); 0 and 2 not (cdist 2)
    assert CONF[0][1] == 1 and CONF[0][6] == 1
    assert CONF[0][2] == 0 and CONF[0][3] == 0
    # word-level
    assert confusable_word((0, 0, 0, 0), (1, 1, 1, 1))      # all coords cdist1
    assert not confusable_word((0, 0, 0, 0), (2, 1, 1, 1))  # first coord cdist2
    print("c7graph self-test OK; NV =", NV)
