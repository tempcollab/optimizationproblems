#!/usr/bin/env python3
"""
Sketch: transfer-matrix-lower
Target (LOWER bound): gr(Av(1324)) > 10.271   [beats BBEPP2017 record 10.271]

Strategy (explorer angle C, cleanest Lean-fit certificate):
  Build a FINITE automaton / transfer matrix whose accepted language is a VERIFIED
  subclass S subset Av(1324). Then gr(S) = spectral radius rho(M) of the nonnegative
  integer transfer matrix M, and gr(Av(1324)) >= gr(S) = rho(M) since S subset Av(1324).
  A Collatz-Wielandt rational witness v > 0 with  M v >= lam v (entrywise) certifies
  rho(M) >= lam exactly, in rational linear algebra. If lam > 10.271 the record is beaten.

================================================================================
WHAT THIS ROUND (R1) DELIVERS -- a fully rigorous, end-to-end certified lower bound
via the cleanest provably-sound subclass found, the SKEW-SUM closure.
================================================================================

Sound subclass S_L (the transfer-matrix's accepted language)
------------------------------------------------------------
Every permutation skew-decomposes uniquely as a skew sum

        sigma = c_1 (-) c_2 (-) ... (-) c_t

of skew-INDECOMPOSABLE components c_i (the skew sum a(-)b places a in the top-left and
b in the bottom-right: every point of a is above-and-left of every point of b).

  S_L  :=  { sigma in Av(1324) : every skew-component c_i has length <= L }.

This is literally a SUBSET of Av(1324) (counted without repetition -- the skew
decomposition is unique), so |S_L,n| <= |Av_n(1324)| and gr(S_L) <= gr(Av(1324)).

SOUNDNESS  (obligation 1 -- proved, see prove_skew_sum_closure() below):
  LEMMA (skew-sum closure of Av(1324)).  a (-) b avoids 1324  <=>  a and b both avoid 1324.
  Proof of "<=" (the only direction we need): suppose a, b avoid 1324 and a(-)b contains
  a 1324 at positions q1<q2<q3<q4 with value-ranks (1,3,2,4).  In a(-)b the a-points occupy
  the LEFT positions and the HIGH values, the b-points the RIGHT positions and LOW values.
  Positions increase, so the chosen points lie in a as a position-prefix: the first t are in
  a, the last 4-t in b, for some t in {0,1,2,3,4}.  If t in {1,2,3} the occurrence "crosses".
  But then the t a-points -- having the HIGHEST values -- must carry the t LARGEST value-ranks
  among {1,2,3,4}.  Checking each t (done exactly in prove_skew_sum_closure):
      t=1: a-ranks must be {4}      but prefix-positions give ranks {1}        -- impossible
      t=2: a-ranks must be {3,4}    but prefix-positions give ranks {1,3}      -- impossible
      t=3: a-ranks must be {2,3,4}  but prefix-positions give ranks {1,2,3}    -- impossible
  (rank of position q1,q2,q3,q4 in pattern 1324 is 1,3,2,4 resp.)  So no crossing 1324
  exists; the occurrence is entirely in a or entirely in b, contradicting avoidance.   QED
  By induction over the number of components, every skew sum of avoiders avoids 1324, so
  S_L subset Av(1324) for every L.  (We also re-verify the lemma by brute force below.)

COUNT  (obligation: the matrix counts the subclass, no over/under-count):
  Let b_k = #{skew-indecomposable 1324-avoiders of length k}  (1 <= k <= L), computed
  EXACTLY by brute force here.  Because the skew decomposition is unique, the counting
  sequence f_n = |S_L,n| satisfies the LINEAR RECURRENCE
        f_n = sum_{k=1}^{L} b_k f_{n-k},   f_0 = 1,
  verified against brute-force enumeration of S_L (verify_recurrence()).  Hence
        gr(S_L) = lim f_n^{1/n} = (largest root of  x^L - sum_k b_k x^{L-k})
                = rho(M),  M = companion matrix of the recurrence (nonnegative integer).

CERTIFICATE  (obligation 2 -- exact rational Collatz-Wielandt):
  M's Perron eigenvector is geometric: v_i = q^{L-1-i}.  For the shift rows
  (M v)_i = v_{i-1} = q * v_i, so taking lam = q gives equality there.  For row 0,
  (M v)_0 / v_0 = sum_{k=1}^{L} b_k q^{1-k}, which EXCEEDS q for any rational q strictly
  below rho(M).  We pick such a rational q, set lam = q and v_i = q^{L-1-i} (exact Fractions),
  and re-check  M v >= lam v  componentwise in exact rational arithmetic.  This certifies
  rho(M) >= lam, hence gr(Av(1324)) >= lam.

HONEST STATUS -- THE RECORD IS *NOT* BEATEN THIS ROUND.
  The skew-sum truncation converges to gr(Av(1324)) ~ 11.6 only logarithmically slowly:
  L=8 gives ~3.773, and even L=16 (needing |Av_16(1324)|, an enormous enumeration) reaches
  only ~5.10.  No feasible L clears 10.271 by THIS construction.  We therefore CERTIFY the
  honest sub-record value and leave the record-beating step as an explicit hole H_BIG: find
  a *sound* automaton/transfer matrix (e.g. a staircase of Av(132)/Av(213) Catalan cells with
  rigorously bounded GF-weighted entries, BBEPP's actual engine) whose certified Perron root
  exceeds 10.271.  The Collatz-Wielandt machinery below is exactly what certifies it once the
  matrix exists -- so this round discharges H2 (soundness) + H3 (CW certificate) on a real
  machine and reshapes H1 to "a HIGHER-growth sound machine" (see approach doc).

Both load-bearing obligations are met for the value we CLAIM (a lower bound, just below the
record): (1) S_L subset Av(1324), proved + brute-checked; (2) exact rational CW inequality.
"""
from fractions import Fraction
from itertools import permutations, combinations

RECORD_LOWER = Fraction(10271, 1000)  # BBEPP2017 verified lower bound to strictly beat


# ----------------------------------------------------------------------------- #
#  Pattern machinery (1324 = value pattern (1,3,2,4) at increasing positions)    #
# ----------------------------------------------------------------------------- #
def contains_1324(p):
    """True iff permutation p (0-indexed tuple) contains the pattern 1324."""
    n = len(p)
    for a, b, c, d in combinations(range(n), 4):
        # positions a<b<c<d, need values p[a] < p[c] < p[b] < p[d]
        if p[a] < p[c] < p[b] < p[d]:
            return True
    return False


def is_skew_indecomposable(p):
    """True iff p cannot be written a (-) b with a,b nonempty.
    p is skew-DECOMPOSABLE iff some proper position-prefix 0..i holds exactly the TOP
    values {n-i-1, ..., n-1}.  (That prefix would be the top-left block a.)"""
    n = len(p)
    mn = n
    for i in range(n - 1):
        mn = min(mn, p[i])
        if mn == n - (i + 1):
            return False
    return True


def skew_components(p):
    """Return the list of skew-component lengths of p (unique skew decomposition)."""
    n = len(p)
    comps = []
    start = 0
    mn = n
    for i in range(n):
        mn = min(mn, p[i])
        if mn == n - (i + 1):
            comps.append(i - start + 1)
            start = i + 1
            mn = n
    return comps


# ----------------------------------------------------------------------------- #
#  Obligation 1: SOUNDNESS  --  skew-sum closure of Av(1324)                      #
# ----------------------------------------------------------------------------- #
def prove_skew_sum_closure():
    """Exact finite proof that a crossing 1324 is impossible in a skew sum a(-)b.

    Pattern 1324 has value-rank pattern (1,3,2,4) at positions (q1,q2,q3,q4) with
    q1<q2<q3<q4.  In a(-)b, a-points take the left positions and the high values.
    A crossing occurrence has the first t points (t in {1,2,3}) in a; those t points,
    carrying the highest values, must have the t LARGEST ranks of {1,2,3,4}.  We show the
    ranks actually sitting on the first t positions are never the t largest -> impossible.
    """
    # rank of pattern position q_i (1-indexed pos i -> rank), pattern 1324:
    posrank = {1: 1, 2: 3, 3: 2, 4: 4}
    for t in (1, 2, 3):
        a_ranks = sorted(posrank[i] for i in range(1, t + 1))        # ranks on prefix positions
        b_ranks = sorted(posrank[i] for i in range(t + 1, 5))        # ranks on suffix positions
        a_must_be_top = (min(a_ranks) > max(b_ranks))                # a needs the highest ranks
        assert not a_must_be_top, f"crossing 1324 NOT excluded for t={t}"
    return True


def brute_check_skew_closure(max_total=7):
    """Re-verify the lemma by brute force: for all a,b avoiders with |a|+|b|<=max_total,
    a(-)b avoids 1324.  (Direction we use: both avoid => sum avoids.)"""
    def skew_sum(a, b):
        n = len(a) + len(b)
        # a in top-left: values offset by len(b); b in bottom-right.
        return tuple([x + len(b) for x in a] + list(b))
    allp = {n: list(permutations(range(n))) for n in range(1, max_total)}
    for la in range(1, max_total):
        for lb in range(1, max_total - la + 1):
            for a in allp[la]:
                if contains_1324(a):
                    continue
                for b in allp[lb]:
                    if contains_1324(b):
                        continue
                    if contains_1324(skew_sum(a, b)):
                        raise AssertionError(f"skew closure FAILS: {a} (-) {b}")
    return True


# ----------------------------------------------------------------------------- #
#  Build the transfer (companion) matrix M of the sound subclass S_L            #
# ----------------------------------------------------------------------------- #
def skew_indec_counts(L):
    """b_k = #{skew-indecomposable 1324-avoiders of length k}, exact, 1<=k<=L."""
    b = [0] * (L + 1)
    for k in range(1, L + 1):
        b[k] = sum(
            1 for p in permutations(range(k))
            if (not contains_1324(p)) and is_skew_indecomposable(p)
        )
    return b


def build_subclass_automaton(L):
    """H1 (this round: the skew-sum machine) + H2 (soundness, discharged above).

    Returns (M, b) where M is the L x L nonnegative integer companion matrix of the
    recurrence  f_n = sum_{k=1}^L b_k f_{n-k}  counting S_L = { avoiders whose every
    skew-component has length <= L }.  rho(M) = gr(S_L) <= gr(Av(1324))."""
    b = skew_indec_counts(L)
    M = [[0] * L for _ in range(L)]
    for j in range(L):
        M[0][j] = b[j + 1]            # row 0 = [b_1, ..., b_L]
    for i in range(1, L):
        M[i][i - 1] = 1               # shift rows
    return M, b


def verify_recurrence(b, L, upto=7):
    """Confirm the matrix counts the subclass exactly: the recurrence f_n = sum b_k f_{n-k}
    reproduces the BRUTE-FORCE count of S_L (no over/under-counting)."""
    # recurrence values
    f = [1] + [0] * upto
    for n in range(1, upto + 1):
        f[n] = sum(b[k] * f[n - k] for k in range(1, min(L, n) + 1))
    # brute counts of S_L
    for n in range(1, upto + 1):
        brute = sum(
            1 for p in permutations(range(n))
            if (not contains_1324(p)) and max(skew_components(p)) <= L
        )
        assert f[n] == brute, f"recurrence != subclass count at n={n}: {f[n]} vs {brute}"
    return True


# ----------------------------------------------------------------------------- #
#  Obligation 2: Collatz-Wielandt rational witness  M v >= lam v                 #
# ----------------------------------------------------------------------------- #
def collatz_wielandt_witness(M, b, L):
    """H3 (discharged).  Geometric witness v_i = q^{L-1-i}, lam = q, with q a rational
    strictly below rho(M).  Returns (lam, v) with all entries exact Fractions, satisfying
    (M v)_i >= lam * v_i for every i.  Certifies rho(M) >= lam."""
    # Find rho(M) numerically only to pick a good rational q below it (the CHECK is exact).
    import numpy as np
    rho = max(np.linalg.eigvals(np.array(M, dtype=float)).real)
    # pick q = a rational just below rho such that  sum_k b_k q^{1-k} >= q  (verified exactly).
    # Walk q down from rho until the exact row-0 inequality holds.
    q = Fraction(int(rho * 10**6) - 1, 10**6)  # rational just below rho
    def row0_ge(q):
        # (M v)_0 / v_0 = sum_{k=1}^L b_k q^{1-k} >= q  <=>  sum_k b_k q^{L-k} >= q^L
        lhs = sum(b[k] * q ** (L - k) for k in range(1, L + 1))
        return lhs >= q ** L
    steps = 0
    while not row0_ge(q):
        q -= Fraction(1, 10**6)
        steps += 1
        if steps > 10**6:
            raise RuntimeError("could not find rational CW witness below rho")
    lam = q
    v = [q ** (L - 1 - i) for i in range(L)]   # exact Fractions, all > 0
    return lam, v


# ============================================================================= #
#  H_BIG re-pointed (R2): SOUND BOUNDED-STATE INSERTION-ENCODING AUTOMATON       #
#  (exact quotient + dominant-SCC exact-rational Collatz-Wielandt)               #
# ============================================================================= #
#
#  This round REPLACES the originally-planned "min-weighted (n,r) quotient" with a
#  STRICTLY SOUND, EXACT (lossless) bounded-state automaton.  Reason recorded in the
#  approach doc and below: the planned min-weighted (n,r) quotient was MEASURED to
#  collapse to a near-triangular matrix whose rho is a cutoff-boundary artifact (~8,
#  the boundary self-loop), NOT a genuine sound growth bound -- the per-group minimum
#  out-degree on the coarse (n,r) grouping is dominated by worst-case vertices of
#  out-degree 1.  That plan is a dead end (documented honestly).  The construction
#  below is sounder: an EXACT subclass count via a finite automaton, certified by
#  exact-rational CW on its dominant strongly-connected component.
#
#  THE SOUND MACHINE (all four facts verified in this file / by exhaustive check):
#
#  (E1) INSERT-NEW-MAXIMUM BIJECTION.  Every permutation of [n] is built by a UNIQUE
#       sequence of "insert the new maximum at position pos" steps (pos in 0..len),
#       inserting values 1,2,...,n in increasing order.  (verify_insert_max_bijection)
#
#  (E2) LOCAL EDGE RULE (exhaustively verified to length 8->9, prove_edge_rule):
#       inserting the new maximum at position pos into a 1324-avoider p creates a 1324
#       occurrence  <=>  the left-prefix p[:pos] CONTAINS the pattern 132.
#       (The new max is the global max, so it can only be the '4' of a 1324; a 1324 is
#       created iff a 132 sits entirely to its left.)  Hence the ALLOWED insertion
#       positions of p are exactly pos in 0..t, where t = length of the longest prefix
#       of p that avoids 132.
#
#  (E3) FINITE STATE.  The only data of p that governs future insertions is the
#       standardisation of its longest 132-avoiding prefix:
#             state(p) := standardize( p[: t+1] ),   t = max_avoid_prefix(p).
#       Inserting a new max maps state(p) -> state(p') deterministically with integer
#       edge multiplicity.  Restricting to states of length <= K gives a FINITE
#       automaton A_K (states + integer edges).
#
#  (E4) SOUND EXACT SUBCLASS.  Walks of length n in A_K from the empty state are in
#       BIJECTION with the subclass
#             B_K := { p in Av(1324) : every value-prefix of p has state-length <= K },
#       a genuine SUBSET of Av(1324) counted without repetition (verified
#       |B_K,n| == #walks for n<=8, verify_subclass_count).  Therefore
#             gr(B_K) = rho(A_K)  <=  gr(Av(1324))    -- UNCONDITIONALLY.
#       This is an EXACT quotient (no averaging, no min-weighting, no Conjecture 8):
#       distinct walks give distinct permutations, so A_K never OVER-counts avoiders
#       (#walks <= |Av_n| verified to n=12).
#
#  CERTIFICATE.  rho(A_K) = max over strongly-connected components of rho(component).
#  We isolate the DOMINANT SCC (its walks are a subset of A_K's, so a CW bound on it is
#  still a valid lower bound on gr(Av(1324))), power-iterate in FLOAT only to obtain an
#  approximate Perron vector, RATIONALISE it to a positive integer vector w, and emit
#  the exact Collatz-Wielandt bound
#             lam := min_i (M w)_i / w_i        (exact Fractions)
#  which satisfies  M w >= lam * w  entrywise BY CONSTRUCTION, certifying
#  rho(dominant SCC) >= lam, hence gr(Av(1324)) >= lam.  Pure rational arithmetic in the
#  load-bearing check; float is used only to choose w.
#
#  MEASURED OUTCOME (the decisive computable question of the dispatch -- does a sound
#  bounded machine clear 10.271?).  NO.  This sound automaton converges to the true
#  gr(Av(1324)) ~ 11.6 only logarithmically in K:
#       K = 6  ->  rho = 3.962871   (#states 352)
#       K = 7  ->  rho = 4.683514   (#states 1276)
#       K = 8  ->  rho = 5.286072   (#states 4708)
#       K = 9  ->  rho = 5.792960   (#states 17578)
#       K = 10 ->  rho ~ 6.223      (#states 66198)
#  The increments shrink (0.72, 0.60, 0.51, 0.43, ...) -- clearing 10.271 needs K well
#  beyond 20 (billions of states), INFEASIBLE.  So this round does NOT beat the record
#  10.271.  But it STRICTLY IMPROVES the held sound floor 3.773326 -> 6.223319 (K=10,
#  the largest cutoff certified with an exact-rational CW witness here; K=11 ~250k states
#  is the next step, beyond a single-call budget), an unconditional sound lower bound with
#  a fully reproducible rational certificate.  This confirms the
#  R1+R2 finding (memory + explorer + Walks2025): no clean sound finite/integer machine
#  reaches 10.271 at feasible size; the record needs the Catalan-cell staircase with
#  GF-weighted entries (Angle C/D, the tromino sketch) or a proof of Conjecture 8
#  (Angle B, conjecture8-diagonal-lower).

CUTOFF_K_CERTIFIED = 10         # largest K certified with an exact-rational CW witness here
#  K=10  ->  lam = 8887516/1428099 = 6.223319  (66198 states, dominant SCC 42484; ~9 min)
#  K=9   ->  lam = 1804171/311442  = 5.792960  (17578 states, dominant SCC 10660; ~1 min)
#  K=8   ->  lam = 19992608/3782129 = 5.286072 (4708 states; seconds) -- fast self-check


def contains_132(p):
    """True iff permutation p (0-indexed tuple) contains the pattern 132."""
    n = len(p)
    for a, b, c in combinations(range(n), 3):
        if p[a] < p[c] < p[b]:
            return True
    return False


def insert_max(p, pos):
    """Insert the new global maximum (= len(p)) at position pos into p."""
    return p[:pos] + (len(p),) + p[pos:]


def max_avoid_prefix(p):
    """t = length of the longest prefix p[:t] that AVOIDS 132 (so p[:t+1] is the first
    prefix that contains a 132, or t = len(p) if no prefix contains 132)."""
    for m in range(len(p) + 1):
        if contains_132(p[:m]):
            return m - 1
    return len(p)


def standardize(pre):
    """Standardise a sequence to a permutation of {0,..,len-1} preserving relative order."""
    order = sorted(range(len(pre)), key=lambda i: pre[i])
    rank = [0] * len(pre)
    for r, i in enumerate(order):
        rank[i] = r
    return tuple(rank)


def state_of(q):
    """state(q) = standardize(q[: t+1]) with t = max_avoid_prefix(q).  (E3)"""
    return standardize(q[: max_avoid_prefix(q) + 1])


# --- (E1) insert-new-maximum is a bijection with all permutations --------------- #
def verify_insert_max_bijection(n=6):
    """Every permutation of [n] is reachable by a unique insert-new-maximum sequence."""
    got = set()

    def build(p):
        if len(p) == n:
            got.add(p)
            return
        for pos in range(len(p) + 1):
            build(insert_max(p, pos))
    build(())
    return got == set(permutations(range(n)))


# --- (E2) local edge rule: creates 1324 <=> left-prefix contains 132 ------------ #
def prove_edge_rule(max_len=8):
    """Exhaustively verify, for every 1324-avoider p of length <= max_len and every
    insertion position pos: contains_1324(insert_max(p,pos)) == contains_132(p[:pos])."""
    for k in range(0, max_len + 1):
        for p in permutations(range(k)):
            if contains_1324(p):
                continue
            for pos in range(k + 1):
                if contains_1324(insert_max(p, pos)) != contains_132(p[:pos]):
                    return False
    return True


# --- (E3) build the finite bounded-state automaton A_K -------------------------- #
def build_insertion_automaton(K):
    """Return (states, edges) of the finite automaton A_K: states = reachable state_of()
    values of length <= K, edges[(s,s')] = #{allowed insertions s -> s'} (integer).

    By (E2) the allowed insertions of a state s (itself a 132-avoiding-prefix form, so
    max_avoid_prefix(s) = len(s)-1) are pos in 0..len(s)-1; we drop transitions whose
    target state exceeds length K (the sound cutoff -- it only removes walks)."""
    from collections import defaultdict
    seen = {()}
    frontier = [()]
    edges = defaultdict(int)
    while frontier:
        s = frontier.pop()
        t = max_avoid_prefix(s)
        for pos in range(t + 1):
            sp = state_of(insert_max(s, pos))
            if len(sp) <= K:
                edges[(s, sp)] += 1
                if sp not in seen:
                    seen.add(sp)
                    frontier.append(sp)
    return sorted(seen, key=lambda x: (len(x), x)), dict(edges)


# --- (E4) the automaton counts the sound subclass B_K exactly ------------------- #
def value_prefix(p, i):
    """Subsequence of p on values {0,..,i-1}, standardised (already a permutation of [i])."""
    return tuple(x for x in p if x < i)


def in_BK(p, K):
    """p in B_K iff every value-prefix of p has state-length <= K."""
    for i in range(1, len(p) + 1):
        if len(state_of(value_prefix(p, i))) > K:
            return False
    return True


def verify_subclass_count(K, upto=8):
    """Confirm #walks of length n in A_K == |B_K,n| (a subset of Av(1324)) for n<=upto,
    so rho(A_K) = gr(B_K) <= gr(Av(1324)) with no over-counting."""
    from collections import defaultdict
    states, edges = build_insertion_automaton(K)
    trans = defaultdict(lambda: defaultdict(int))
    for (s, sp), m in edges.items():
        trans[s][sp] += m
    cur = {(): 1}
    walk = [1]
    for _ in range(upto):
        nxt = defaultdict(int)
        for s, c in cur.items():
            for sp, m in trans[s].items():
                nxt[sp] += c * m
        walk.append(sum(nxt.values()))
        cur = nxt
    for n in range(0, upto + 1):
        bk = sum(1 for p in permutations(range(n))
                 if (not contains_1324(p)) and in_BK(p, K))
        if walk[n] != bk:
            raise AssertionError(f"A_K walk count != |B_K,{n}|: {walk[n]} vs {bk}")
    return True


# --- dominant SCC + exact-rational Collatz-Wielandt ----------------------------- #
def tarjan_sccs(n, adjset):
    """Iterative Tarjan: return list of SCCs (each a list of vertex indices)."""
    index = [None] * n
    low = [0] * n
    onstk = [False] * n
    stk = []
    cnt = [0]
    comps = []
    for root in range(n):
        if index[root] is not None:
            continue
        work = [(root, 0)]
        while work:
            node, pi = work[-1]
            if pi == 0:
                index[node] = low[node] = cnt[0]
                cnt[0] += 1
                stk.append(node)
                onstk[node] = True
            recurse = False
            nbrs = adjset[node]
            for i in range(pi, len(nbrs)):
                w = nbrs[i]
                if index[w] is None:
                    work[-1] = (node, i + 1)
                    work.append((w, 0))
                    recurse = True
                    break
                elif onstk[w]:
                    low[node] = min(low[node], index[w])
            if recurse:
                continue
            if low[node] == index[node]:
                comp = []
                while True:
                    w = stk.pop()
                    onstk[w] = False
                    comp.append(w)
                    if w == node:
                        break
                comps.append(comp)
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
    return comps


def dominant_scc_cw_bound(K, D=10**7):
    """HOLE H_BIG -- DISCHARGED.  Build A_K, find its dominant SCC, and return an exact
    rational Collatz-Wielandt lower bound  lam  on rho(A_K) = gr(B_K) <= gr(Av(1324)).

    The CW check  M w >= lam * w  (entrywise, exact Fractions) is the load-bearing,
    reproducible step; numpy float power-iteration is used ONLY to choose the positive
    integer witness vector w.  Returns (lam, n_states, scc_size)."""
    import numpy as np
    states, edges = build_insertion_automaton(K)
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    adj = [[] for _ in range(n)]          # adj[i] = list of (j, multiplicity)
    adjset = [[] for _ in range(n)]
    for (s, sp), m in edges.items():
        adj[idx[s]].append((idx[sp], m))
        adjset[idx[s]].append(idx[sp])

    comps = tarjan_sccs(n, adjset)

    def rho_of(comp):
        cs = set(comp)
        cidx = {v: i for i, v in enumerate(comp)}
        m = len(comp)
        if m == 1:
            v = comp[0]
            sl = sum(mm for (j, mm) in adj[v] if j == v)
            return sl, {v: 1.0}
        sub = [[] for _ in range(m)]
        for v in comp:
            for (j, mm) in adj[v]:
                if j in cs:
                    sub[cidx[v]].append((cidx[j], mm))
        w = np.ones(m)
        nrm = 0.0
        for _ in range(6000):
            nw = np.zeros(m)
            for i in range(m):
                acc = 0.0
                for j, mm in sub[i]:
                    acc += mm * w[j]
                nw[i] = acc
            nrm = nw.max()
            if nrm == 0:
                return 0.0, {}
            nw /= nrm
            if np.max(np.abs(nw - w)) < 1e-13:
                w = nw
                break
            w = nw
        return nrm, {comp[i]: w[i] for i in range(m)}

    best_rho, best_comp, best_w = 0.0, None, None
    for comp in comps:
        r, wv = rho_of(comp)
        if r > best_rho:
            best_rho, best_comp, best_w = r, comp, wv

    # exact-rational CW on the dominant SCC submatrix
    comp = best_comp
    cs = set(comp)
    cidx = {v: i for i, v in enumerate(comp)}
    m = len(comp)
    sub = [[] for _ in range(m)]
    for v in comp:
        for (j, mm) in adj[v]:
            if j in cs:
                sub[cidx[v]].append((cidx[j], mm))
    wi = [max(1, int(best_w[comp[i]] * D)) for i in range(m)]     # positive integer witness
    Mw = [0] * m
    for i in range(m):
        acc = 0
        for j, mm in sub[i]:
            acc += mm * wi[j]
        Mw[i] = acc
    lam = min(Fraction(Mw[i], wi[i]) for i in range(m))           # CW lower bound, exact
    # verify the entrywise inequality in exact rational arithmetic (load-bearing check)
    assert all(Fraction(Mw[i]) >= lam * wi[i] for i in range(m)), "exact CW inequality fails"
    assert all(x > 0 for x in wi), "witness must be strictly positive"
    return lam, n, m


def certify_insertion_automaton(K=CUTOFF_K_CERTIFIED):
    """Assemble the SOUND bounded-state route and return the certified rational lower
    bound  gr(Av(1324)) >= lam = rho(A_K dominant SCC).  Beats 3.773326, below 10.271."""
    assert verify_insert_max_bijection(n=6), "(E1) insert-max bijection failed"
    assert prove_edge_rule(max_len=8), "(E2) local edge rule failed"
    assert verify_subclass_count(min(K, 6), upto=8), "(E4) A_K mis-counts subclass B_K"
    lam, nstates, sccsz = dominant_scc_cw_bound(K)
    print(f"SOUND bounded-state insertion automaton A_K (K={K}): {nstates} states, "
          f"dominant SCC {sccsz} states")
    print(f"CERTIFIED (exact rational Collatz-Wielandt on dominant SCC):")
    print(f"   gr(Av(1324)) >= gr(B_{K}) = rho(A_{K}) >= {lam} = {float(lam):.6f}")
    beats_floor = lam > Fraction(1886663, 500000)   # R1 held 3.773326
    beats_record = lam > RECORD_LOWER
    print(f"   beats R1 floor 3.773326: {beats_floor}   beats record 10.271: {beats_record}")
    if not beats_record:
        print("   HONEST: no feasible K clears 10.271 (logarithmic convergence to ~11.6);")
        print("   this is a strict SOUND improvement of the floor, not a record break.")
    return lam


def certify(L=8):
    # Obligation 1 -- soundness (analytic finite proof + brute re-check).
    assert prove_skew_sum_closure(), "skew-sum closure proof failed"
    assert brute_check_skew_closure(max_total=7), "brute skew-closure check failed"

    # Build the sound transfer matrix and confirm it counts the subclass exactly.
    M, b = build_subclass_automaton(L)
    assert verify_recurrence(b, L, upto=7), "transfer matrix mis-counts the subclass"

    # Obligation 2 -- exact rational Collatz-Wielandt certificate.
    lam, v = collatz_wielandt_witness(M, b, L)
    assert all(x > 0 for x in v), "witness must be strictly positive"
    Mv = [sum(Fraction(int(M[i][j])) * v[j] for j in range(L)) for i in range(L)]
    assert all(Mv[i] >= lam * v[i] for i in range(L)), "CW inequality M v >= lam v fails"

    print(f"skew-indecomposable 1324-avoider counts b_1..b_{L} = {b[1:]}")
    print(f"transfer matrix M is {L}x{L}, nonnegative integer (companion of the recurrence)")
    print(f"CERTIFIED (exact rational Collatz-Wielandt):  gr(Av(1324)) >= rho(M) >= {lam}")
    print(f"            = {float(lam):.6f}")
    beats = lam > RECORD_LOWER
    print(f"record to beat (BBEPP2017): {float(RECORD_LOWER)}   --  beats record: {beats}")
    if not beats:
        print("HOLE H_BIG REMAINS: this sound skew-sum machine certifies a TRUE but "
              "SUB-RECORD lower bound; converges to ~11.6 only logarithmically. A "
              "higher-growth sound machine (staircase of Catalan cells) is needed to clear "
              "10.271 -- the CW machinery above certifies it the moment that matrix exists.")
    return lam


if __name__ == "__main__":
    import sys
    # R1 floor (skew-sum subclass) -- fast, always runs.
    print("=" * 72)
    print("R1 skew-sum floor (verified):")
    certify(L=8)
    print("=" * 72)
    # R2 SOUND bounded-state insertion automaton -- the new, higher sound bound.
    # Default K=10 (the certified headline value 6.223319; ~9 min).  Pass an integer
    # argument to choose K (e.g. `python transfer-matrix-lower.py 8` for a fast check).
    K = int(sys.argv[1]) if len(sys.argv) > 1 else CUTOFF_K_CERTIFIED
    print(f"R2 SOUND bounded-state insertion-encoding automaton (K={K}):")
    certify_insertion_automaton(K)
