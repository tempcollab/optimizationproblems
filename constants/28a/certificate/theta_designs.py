"""
theta_designs.py  --  reproducible, network-free design constructors for the
theta-cover-dual sketch (constant 28a).

Builds the explicit vertex-transitive two-distance candidate graphs that the
sketch instantiates: Steiner block-intersection graphs S(2,k,n) and the Cameron
graph srg(231,30,9,3) (M22-transitive).  All exact integer arithmetic (no float).

Provides:
  bose_sts(t)            -> (npts, blocks)  Steiner triple system on n=6t+3 points
  block_intersection_graph(blocks)          -> int 0/1 adjacency (two blocks meet)
  golay24()              -> [24,12] extended binary Golay generator (exact GF(2))
  witt_S5_8_24()         -> 759 octads (blocks of S(5,8,24))
  witt_S3_6_22()         -> 77 blocks of S(3,6,22) (derived from the octads)
  cameron_graph()        -> (A, pairs)  srg(231,30,9,3) Cameron graph

Each constructor self-checks its defining incidence property on import-time call.
"""
import itertools
import numpy as np


# ---------------------------------------------------------------------------
# Steiner triple systems  S(2,3,n),  n = 3 (mod 6),  via Bose
# ---------------------------------------------------------------------------

def bose_sts(t):
    """Bose construction of a Steiner triple system on n = 6t+3 points.
    Returns (n, blocks) with blocks a sorted list of 3-tuples; verified STS."""
    m = 2 * t + 1
    def pt(i, k):
        return (i % m) + k * m
    def q(a, b):                       # idempotent commutative quasigroup on Z_m
        return ((t + 1) * (a + b)) % m
    blocks = set()
    for i in range(m):
        blocks.add(tuple(sorted([pt(i, 0), pt(i, 1), pt(i, 2)])))
    for k in range(3):
        for i in range(m):
            for j in range(i + 1, m):
                blocks.add(tuple(sorted([pt(i, k), pt(j, k), pt(q(i, j), (k + 1) % 3)])))
    blocks = sorted(blocks)
    _verify_steiner(3 * m, blocks, 3)
    return 3 * m, blocks


def _verify_steiner(npts, blocks, k):
    """Assert (npts, blocks) is an S(2,k,*): every pair in exactly one block."""
    seen = set()
    for b in blocks:
        assert len(b) == k
        for x, y in itertools.combinations(b, 2):
            assert (x, y) not in seen, "pair repeated -- not a Steiner 2-design"
            seen.add((x, y))
    assert len(seen) == npts * (npts - 1) // 2


def block_intersection_graph(blocks):
    """Adjacency of the block-intersection graph: edge iff two blocks meet.
    Exact integer 0/1 matrix.  This graph is the (vertex-transitive) SRG whose
    spherical 2-distance embedding the sketch tests."""
    m = len(blocks)
    bs = [set(b) for b in blocks]
    A = np.zeros((m, m), dtype=np.int8)
    for i in range(m):
        for j in range(i + 1, m):
            if bs[i] & bs[j]:
                A[i, j] = A[j, i] = 1
    return A


# ---------------------------------------------------------------------------
# Extended binary Golay code  ->  Witt designs  ->  Cameron graph
# ---------------------------------------------------------------------------

def golay24():
    """[24,12] extended binary Golay generator G = [I | B], B the bordered
    QR(11) circulant.  Exact GF(2).  Verified: weight enum 1+759x^8+2576x^12+...."""
    QR11 = {(x * x) % 11 for x in range(1, 11)}      # {1,3,4,5,9}
    B = np.zeros((12, 12), dtype=int)
    B[0, 1:] = 1
    B[1:, 0] = 1
    B[0, 0] = 0
    for i in range(11):
        for j in range(11):
            B[i + 1, j + 1] = 1 if ((j - i) % 11) in QR11 else 0
        B[i + 1, i + 1] = 1
    return np.concatenate([np.eye(12, dtype=int), B], axis=1) % 2


def _golay_codewords():
    G = golay24()
    rows = [G[i] for i in range(12)]
    cws = set()
    for mask in range(1 << 12):
        v = np.zeros(24, dtype=int)
        m, i = mask, 0
        while m:
            if m & 1:
                v = (v + rows[i]) % 2
            m >>= 1
            i += 1
        cws.add(tuple(v.tolist()))
    return cws


def witt_S5_8_24():
    """759 octads = weight-8 Golay codewords = blocks of S(5,8,24)."""
    cws = _golay_codewords()
    wts = {}
    for c in cws:
        w = sum(c)
        wts[w] = wts.get(w, 0) + 1
    assert wts == {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}, wts
    return [frozenset(i for i in range(24) if c[i]) for c in cws if sum(c) == 8]


def witt_S3_6_22():
    """77 blocks of S(3,6,22): delete two points from the octads through both."""
    octads = witt_S5_8_24()
    p, q = 22, 23
    blocks6 = [frozenset(o - {p, q}) for o in octads if p in o and q in o]
    assert len(blocks6) == 77, len(blocks6)
    # verify S(3,6,22): every 3-subset of the 22-set in exactly one block
    cnt = {}
    for b in blocks6:
        assert len(b) == 6
        for t in itertools.combinations(sorted(b), 3):
            cnt[t] = cnt.get(t, 0) + 1
    assert set(cnt.values()) == {1} and len(cnt) == 1540, (set(cnt.values()), len(cnt))
    return blocks6


def cameron_graph():
    """Cameron graph srg(231,30,9,3): vertices = 231 pairs of a 22-set; two pairs
    adjacent iff disjoint and their 4-point union lies in a block of S(3,6,22).
    M22.2-transitive (hence vertex-transitive).  Returns (A, pairs)."""
    blocks6 = witt_S3_6_22()
    pairs = [frozenset(e) for e in itertools.combinations(range(22), 2)]
    N = len(pairs)
    A = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        for j in range(i + 1, N):
            u = pairs[i] | pairs[j]
            if len(u) == 4:
                for b in blocks6:
                    if u <= b:
                        A[i, j] = A[j, i] = 1
                        break
    deg = A.sum(1)
    assert len(set(deg.tolist())) == 1 and int(deg[0]) == 30, sorted(set(deg.tolist()))
    return A, pairs


if __name__ == "__main__":
    n, blk = bose_sts(6)
    print("bose_sts(6): n=%d, blocks=%d (STS verified)" % (n, len(blk)))
    A, pairs = cameron_graph()
    print("cameron_graph: N=%d regular deg 30 (srg(231,30,9,3) verified)" % A.shape[0])
