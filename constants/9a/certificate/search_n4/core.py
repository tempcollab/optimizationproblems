"""Shared core for the C_7^box4 strong unstructured MIS attack (R15).

Reuses the EXACT adjacency convention of the Lean engine (C9.lean):
  cdist(a,b) = min(|a-b|, 7-|a-b|); two letters confusable iff cdist <= 1;
  two words confusable (ADJACENT, cannot coexist in an independent set) iff
  EVERY coordinate is confusable; independent iff SOME coord has cdist >= 2.

Provides:
  - vertex <-> word maps (id = base-7),
  - bitset adjacency (NV rows, each a Python int bitmask of length NV) for fast LS,
  - the full automorphism group Aut(C_7^box4) = D_7 wr S_4 (order 921984) as
    permutations of the 2401 vertices: per-coordinate dihedral (7 rotations x 2
    reflections) + S_4 coordinate permutations.

All checks here are re-derived from scratch (independent of R14 code) so this
module doubles as the verifier.
"""
import itertools

N = 7
DIM = 4
NV = N ** DIM  # 2401


def cdist(a, b):
    d = abs(a - b) % N
    return min(d, N - d)


CONF_LETTER = [[1 if cdist(a, b) <= 1 else 0 for b in range(N)] for a in range(N)]


def id_to_word(i):
    w = []
    for _ in range(DIM):
        w.append(i % N)
        i //= N
    return tuple(reversed(w))


def word_to_id(w):
    i = 0
    for c in w:
        i = i * N + c
    return i


WORDS = [id_to_word(i) for i in range(NV)]


def confusable(u, v):
    """True iff words u,v are ADJACENT in the strong power."""
    for i in range(DIM):
        if not CONF_LETTER[u[i]][v[i]]:
            return False
    return True


def build_bitset_adj():
    """adj[i] = Python int bitmask: bit j set iff word i confusable with word j (i != j)."""
    adj = [0] * NV
    for i in range(NV):
        u = WORDS[i]
        m = 0
        for j in range(NV):
            if i != j and confusable(u, WORDS[j]):
                m |= (1 << j)
        adj[i] = m
    return adj


# ----- automorphism group -----------------------------------------------------
# A dihedral element of D_7 on Z_7: x -> s*x + r mod 7, s in {+1,-1}, r in 0..6.
# cdist is invariant under these (rotation + reflection of the 7-cycle).
def dihedral_perms():
    perms = []
    for s in (1, -1):
        for r in range(N):
            perms.append(tuple((s * x + r) % N for x in range(N)))
    return perms  # 14 permutations of Z_7


DIHEDRAL = dihedral_perms()


def apply_aut(perm_coords, coord_perm, word):
    """Apply an automorphism to a word.
      perm_coords: list of DIM dihedral permutations (one per ORIGINAL coordinate)
      coord_perm:  a permutation of range(DIM) (where each coord goes)
    New word w' : w'[coord_perm[c]] = perm_coords[c](word[c]).
    """
    out = [0] * DIM
    for c in range(DIM):
        out[coord_perm[c]] = perm_coords[c][word[c]]
    return tuple(out)


def random_aut_vertex_perm(rng):
    """Return a permutation 'p' of range(NV): p[i] = id of image of word i under a
    uniformly random automorphism."""
    pc = [DIHEDRAL[rng.randrange(len(DIHEDRAL))] for _ in range(DIM)]
    cp = list(range(DIM))
    rng.shuffle(cp)
    p = [0] * NV
    for i in range(NV):
        p[i] = word_to_id(apply_aut(pc, cp, WORDS[i]))
    return p


# ----- independent-set verification (from-scratch) ----------------------------
def is_independent(id_list):
    """Re-derive the rule and check: returns (ok, num_conf_pairs, distinct)."""
    ids = list(id_list)
    distinct = (len(set(ids)) == len(ids))
    conf = 0
    ws = [WORDS[i] for i in ids]
    n = len(ws)
    for a in range(n):
        for b in range(a + 1, n):
            if confusable(ws[a], ws[b]):
                conf += 1
    return (conf == 0 and distinct), conf, distinct


if __name__ == "__main__":
    adj = build_bitset_adj()
    # sanity: degree of 0000 is 80
    z = word_to_id((0, 0, 0, 0))
    print("NV", NV, "deg(0000)", bin(adj[z]).count("1"), "expected 80")
    degs = [bin(adj[i]).count("1") for i in range(NV)]
    print("deg min/max", min(degs), max(degs))
    edges = sum(degs) // 2
    print("edges", edges, "expected 96040")
    # sanity: automorphisms preserve adjacency on a sample
    import random
    rng = random.Random(1)
    p = random_aut_vertex_perm(rng)
    bad = 0
    for _ in range(2000):
        i = rng.randrange(NV); j = rng.randrange(NV)
        if i == j:
            continue
        a_ij = (adj[i] >> j) & 1
        a_pij = (adj[p[i]] >> p[j]) & 1
        if a_ij != a_pij:
            bad += 1
    print("aut adjacency violations (sample 2000):", bad, "(should be 0)")
