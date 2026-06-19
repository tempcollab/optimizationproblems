"""
Shared infrastructure for constant 28a (Borsuk first-failing dimension).

Builds the strongly regular graph G_2(4) = srg(416, 100, 36, 20) from the
GF(16) Hermitian-form model used by Bondarenko / Jenrich-Brouwer / Gri2026,
and exposes:

  - build_g24()        -> (adjacency A (416x416 int), vertices list)
  - gram_standard(A)   -> G = 96 I + 24 A - 6 J   (PSD rank 65, Gri's Lemma 2)
  - gram_integer(A)    -> Y = A - sI with s = -4  (Jenrich's integer Gram, rank 65)
  - euclidean_rep(G)   -> X (n x f) with rows the point vectors, f = rank(G)
  - max_clique_le(A, k) -> bool: True iff omega(graph) <= k  (bitset search)

These are the load-bearing finite/algebraic objects. Everything here is exact
integer arithmetic except euclidean_rep (a closed-form PSD factorization).

NOTE: every consumer sketch leaves ITS hard step as a hole; this file is just
the trusted scaffold (the part that mirrors the already-verified Gri2026 facts).
"""

import numpy as np
import itertools


# ---------------------------------------------------------------------------
# GF(16) = F_2[a]/(a^4 + a + 1)
# ---------------------------------------------------------------------------

def _gf16_tables():
    # elements 0..15 as 4-bit polynomials over F_2; a = x is the primitive root
    # reduction poly x^4 + x + 1  ->  x^4 = x + 1  (bit 4 -> bits 1 and 0)
    exp = [0] * 32
    log = [0] * 16
    x = 1
    for i in range(15):
        exp[i] = x
        log[x] = i
        x <<= 1
        if x & 0x10:
            x ^= 0b10011  # x^4 + x + 1
    for i in range(15, 30):
        exp[i] = exp[i - 15]
    return exp, log


_EXP, _LOG = _gf16_tables()


def gf_mul(a, b):
    if a == 0 or b == 0:
        return 0
    return _EXP[_LOG[a] + _LOG[b]]


def gf_add(a, b):
    return a ^ b


def gf_pow(a, e):
    r = 1
    for _ in range(e):
        r = gf_mul(r, a)
    return r


def gf_frob4(a):
    # Frobenius x -> x^4 (the conjugation for the Hermitian form over GF(16)/GF(4))
    return gf_pow(a, 4)


# ---------------------------------------------------------------------------
# Projective points of PG(2,16) and the Hermitian form
#   h(u,w) = u0 w0^4 + u1 w1^4 + u2 w2^4
# ---------------------------------------------------------------------------

def projective_points():
    """273 projective points of PG(2,16) as canonical representatives."""
    pts = []
    for a in range(16):
        for b in range(16):
            for c in range(16):
                if a == 0 and b == 0 and c == 0:
                    continue
                # canonical form: leading nonzero coord scaled to 1
                v = (a, b, c)
                lead = next(x for x in v if x != 0)
                inv = _EXP[(15 - _LOG[lead]) % 15] if lead != 0 else 0
                cv = tuple(gf_mul(inv, x) for x in v)
                pts.append(cv)
    pts = sorted(set(pts))
    return pts


def herm(u, w):
    return gf_add(gf_add(gf_mul(u[0], gf_frob4(w[0])),
                         gf_mul(u[1], gf_frob4(w[1]))),
                  gf_mul(u[2], gf_frob4(w[2])))


def is_isotropic(u):
    return herm(u, u) == 0


# ---------------------------------------------------------------------------
# G_2(4) vertices = orthogonal bases (unordered triples of pairwise-orthogonal
# non-isotropic projective points). Two vertices adjacent iff ... (Gri Lemma).
# ---------------------------------------------------------------------------

def _canon(v):
    """Canonical projective representative (leading nonzero coord scaled to 1)."""
    if all(x == 0 for x in v):
        return None
    lead = next(x for x in v if x != 0)
    inv = _EXP[(15 - _LOG[lead]) % 15]
    return tuple(gf_mul(inv, x) for x in v)


def _line_points(u, w):
    """All projective points on the line spanned by distinct points u, w."""
    s = set()
    for a in range(16):
        for b in range(16):
            if a == 0 and b == 0:
                continue
            v = tuple(gf_add(gf_mul(a, u[k]), gf_mul(b, w[k])) for k in range(3))
            cv = _canon(v)
            if cv is not None:
                s.add(cv)
    return s


def build_g24():
    """
    Returns (A, vertices) with A the 416x416 integer adjacency of G_2(4) and
    `vertices` the deterministic list of 416 orthogonal bases (each an unordered
    triple of pairwise-orthogonal non-isotropic projective points).

    Brouwer's projective model (Gri2026 Section 2): vertices are the unordered
    triples A = {a1,a2,a3} of pairwise-orthogonal non-isotropic projective points
    of PG(2,16) under the Hermitian form. T(A) = the isotropic 15-set on the three
    lines spanned by pairs of A. Two vertices A, A' are adjacent iff |T(A)∩T(A')|=3.

    Verified by this module's __main__ block: 416 vertices, srg(416,100,36,20),
    adjacency eigenvalues 100/20/-4 (mult 1/65/350), Gram rank 65, omega = 5.
    Deterministic (sorted projective points, sorted triples), exact GF(16)
    arithmetic + integer bitsets -- no floating point in the graph itself.
    """
    pts = projective_points()
    iso = [p for p in pts if is_isotropic(p)]
    noniso = [p for p in pts if not is_isotropic(p)]
    iso_set = set(iso)
    iso_index = {p: i for i, p in enumerate(iso)}

    # orthogonal triples of non-isotropic points, in deterministic order
    ni = noniso
    Nn = len(ni)
    orthadj = [[] for _ in range(Nn)]
    for i in range(Nn):
        for j in range(i + 1, Nn):
            if herm(ni[i], ni[j]) == 0:
                orthadj[i].append(j)
    triples = []
    for i in range(Nn):
        oi = set(orthadj[i])
        for j in orthadj[i]:
            oj = oi & set(orthadj[j])
            for k in oj:
                if k > j:
                    triples.append((ni[i], ni[j], ni[k]))
    triples.sort()  # deterministic vertex order

    # T(A) as a 65-bit isotropic-set mask
    def T_mask(A):
        m = 0
        for a, b in itertools.combinations(range(3), 2):
            for p in _line_points(A[a], A[b]) & iso_set:
                m |= (1 << iso_index[p])
        return m

    masks = [T_mask(A) for A in triples]
    n = len(triples)
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        mi = masks[i]
        for j in range(i + 1, n):
            if bin(mi & masks[j]).count("1") == 3:
                A[i, j] = 1
                A[j, i] = 1
    return A, triples


def standard_partition(verts):
    """
    Gri2026 Lemma 1 partition wrt the first isotropic point q0 (in the
    deterministic order of `projective_points()` filtered to isotropics):
      B = vertices containing a non-isotropic point orthogonal to q0,
      C = V \\ B.
    Returns (q0, B_idx, C_idx) with B_idx, C_idx lists of vertex indices into
    `verts`. (B further splits into 3 size-32 components B1,B2,B3 -- see
    b_components.)
    """
    pts = projective_points()
    iso = [p for p in pts if is_isotropic(p)]
    q0 = iso[0]
    B_idx, C_idx = [], []
    for vi, A in enumerate(verts):
        # A is a triple of non-isotropic points; in B iff some a_i is orthogonal
        # to q0 (h(a_i, q0) == 0)
        if any(herm(a, q0) == 0 for a in A):
            B_idx.append(vi)
        else:
            C_idx.append(vi)
    return q0, B_idx, C_idx


def b_components(A, B_idx):
    """Connected components of the induced graph on B (Gri: 3 components of 32)."""
    Bset = set(B_idx)
    seen = set()
    comps = []
    for start in B_idx:
        if start in seen:
            continue
        stack = [start]
        comp = []
        seen.add(start)
        while stack:
            u = stack.pop()
            comp.append(u)
            for w in np.nonzero(A[u])[0].tolist():
                if w in Bset and w not in seen:
                    seen.add(w)
                    stack.append(w)
        comps.append(sorted(comp))
    return comps


# ---------------------------------------------------------------------------
# Gram matrices and Euclidean representation
# ---------------------------------------------------------------------------

def gram_standard(A):
    n = A.shape[0]
    J = np.ones((n, n), dtype=np.int64)
    I = np.eye(n, dtype=np.int64)
    return 96 * I + 24 * A - 6 * J


def gram_integer(A):
    s = -4
    return A.astype(np.int64) - s * np.eye(A.shape[0], dtype=np.int64)


def euclidean_rep(G, tol=1e-7):
    """Factor PSD Gram G = X X^T, return X (n x f), f = numerical rank."""
    w, V = np.linalg.eigh(G.astype(float))
    keep = w > tol
    f = int(keep.sum())
    X = V[:, keep] * np.sqrt(w[keep])
    return X, f


def subspace_dim(X, tol=1e-6):
    """Affine/linear dimension of the row-span of X."""
    s = np.linalg.svd(X, compute_uv=False)
    return int((s > tol).sum())


# ---------------------------------------------------------------------------
# Clique number bound (bitset branch-and-bound) -- the Lean-fit certificate core
# ---------------------------------------------------------------------------

def max_clique_le(A, k):
    """
    True iff the maximum clique of graph A has size <= k.
    Pure combinatorial search; this is exactly the step a Lean proof would
    discharge by enumeration. Reused by every sketch's diameter-cap check.
    """
    n = A.shape[0]
    nbrs = [frozenset(np.nonzero(A[i])[0].tolist()) for i in range(n)]

    best = [0]

    def expand(R_size, P, X):
        if not P and not X:
            best[0] = max(best[0], R_size)
            return
        if R_size + len(P) <= best[0]:
            return
        if best[0] > k:
            return
        # pivot
        PuX = P | X
        if PuX:
            u = max(PuX, key=lambda v: len(P & nbrs[v]))
            cand = list(P - nbrs[u])
        else:
            cand = list(P)
        for v in cand:
            expand(R_size + 1, P & nbrs[v], X & nbrs[v])
            P = P - {v}
            X = X | {v}
            if best[0] > k:
                return

    expand(0, frozenset(range(n)), frozenset())
    return best[0] <= k


if __name__ == "__main__":
    A, verts = build_g24()
    n = A.shape[0]
    assert n == 416, n
    deg = A.sum(axis=1)
    assert deg.min() == 100 and deg.max() == 100
    J = np.ones((n, n), dtype=np.int64)
    I = np.eye(n, dtype=np.int64)
    # strongly regular identity A^2 = kI + lam A + mu(J-I-A)
    assert np.array_equal(A @ A, 100 * I + 36 * A + 20 * (J - I - A))
    w = np.linalg.eigvalsh(A.astype(float))
    import collections
    mult = collections.Counter(np.round(w).astype(int).tolist())
    assert mult == {100: 1, 20: 65, -4: 350}, dict(mult)
    G = gram_standard(A)
    assert int((np.linalg.eigvalsh(G.astype(float)) > 1e-6).sum()) == 65
    assert max_clique_le(A, 5) and not max_clique_le(A, 4)
    q0, B_idx, C_idx = standard_partition(verts)
    assert len(B_idx) == 96 and len(C_idx) == 320, (len(B_idx), len(C_idx))
    comps = b_components(A, B_idx)
    assert sorted(len(c) for c in comps) == [32, 32, 32], [len(c) for c in comps]
    print("g24 verified: srg(416,100,36,20), eig 100/20/-4 mult 1/65/350,")
    print("Gram rank 65, omega=5, partition |B|=96 (3x32) |C|=320. PASS")
