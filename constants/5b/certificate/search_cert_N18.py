#!/usr/bin/env python3
"""
C_5b (Sidon density in (4,5)-sets, Erdos #757) — approach transversal-ilp-floor-search-N18.

STATUS: NO strict improvement over the record 4/7 was found.  This is the REPRODUCIBLE
artifact for a NEGATIVE / obstruction result at N = 18:

  GOAL of the approach: find an 18-point (4,5)-set (weak Sidon set) A with
      h(A) = 10   (h = largest Sidon subset = independence number alpha of the
                   3-AP hypergraph, by [MT26] Lemma 2.3),
  which would give the strict beat   c* <= 10/18 = 5/9 ~ 0.5556  <  4/7 ~ 0.5714.

  RESULT: across four independent exact-alpha search methods the MINIMUM achieved
  independence number at N = 18 is alpha = 11 (ratio 11/18 ~ 0.6111, which does NOT
  beat 4/7).  The floor value alpha = 10 = ceil(9*18/17) was NOT realized in the
  searched region.  No beat is claimed.

What this script DOES establish, exactly (integer arithmetic only, deterministic):

  (A) The record 14-point gadget A_base IS a (4,5)-set with h = 8 (the bar, c* <= 4/7).
  (B) The arithmetic floor: from the PROVEN lower bound c* >= 9/17 [MT26], every
      (4,5)-set of size N has h(A) >= ceil(9N/17).  At N = 18 this floor equals 10,
      and 10/18 < 4/7, so 10 IS the unique h-value that would beat 4/7 at N = 18
      (h = 11 already fails: 11/18 > 4/7).
  (C) A best-found 18-point (4,5)-set with h = 11 (exact), explicitly listed and
      double-checked: it is weak Sidon, alpha = 11, and 11 is a 1-swap LOCAL MINIMUM
      (no single-point replacement over [0, 1300] lowers alpha).
  (D) The "floor + 1" obstruction pattern: a wide-beam exact-alpha extension of the
      record set reaches exactly floor + 1 at every N in {15,16,17,18} and the floor
      only at N = 14 (the record itself).  Adding any point to a floor-realizing set
      raises alpha above the next floor in every searched extension.

All h / alpha values are computed EXACTLY by deterministic branch-and-bound on the
3-AP hypergraph (independence number).  No float decides anything; no randomness in any
verification step.  The four heavy SEARCHES (random, simulated annealing, stochastic beam,
record extension) are SEARCH tools only and are summarized below from logged runs; this
script re-derives and re-checks every load-bearing fact deterministically and quickly.

Run:  python search_cert_N18.py
"""
import itertools

# ---------------------------------------------------------------------------
# Exact primitives (integer arithmetic only)
# ---------------------------------------------------------------------------

def is_45set(A):
    """A is a (4,5)-set / weak Sidon set  <=>  all pairwise sums a+b (a<b) distinct."""
    A = sorted(A)
    seen = set()
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            s = A[i] + A[j]
            if s in seen:
                return False
            seen.add(s)
    return True


def is_45set_via_differences(A):
    """Independent cross-check: every 4-element subset has >=5 distinct |differences|."""
    A = sorted(A)
    for quad in itertools.combinations(A, 4):
        diffs = set()
        for x, y in itertools.combinations(quad, 2):
            diffs.add(abs(x - y))
        if len(diffs) < 5:
            return False
    return True


def three_ap_triples(A):
    """3-term APs {p, p+d, p+2d} inside A, as sorted index triples (i<j<k)."""
    A = sorted(A)
    pos = {v: i for i, v in enumerate(A)}
    Aset = set(A)
    edges = []
    for i in range(len(A)):
        for k in range(i + 1, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 and (s // 2) in Aset:
                j = pos[s // 2]
                if i < j < k:
                    edges.append((i, j, k))
    return edges


def alpha_exact(A):
    """EXACT independence number of the 3-AP hypergraph on A = h(A)
    (= largest subset of A with no 3-term AP = largest Sidon subset, [MT26] Lemma 2.3),
    by deterministic branch-and-bound with a sound bound prune."""
    A = sorted(A)
    n = len(A)
    edges = three_ap_triples(A)
    incident = [[] for _ in range(n)]
    for (i, j, k) in edges:
        incident[i].append(frozenset((j, k)))
        incident[j].append(frozenset((i, k)))
        incident[k].append(frozenset((i, j)))
    order = sorted(range(n), key=lambda v: -len(incident[v]))
    best = [0]
    chosen = set()

    def bt(idx, cnt):
        if cnt + (n - idx) <= best[0]:
            return
        if idx == n:
            if cnt > best[0]:
                best[0] = cnt
            return
        v = order[idx]
        if all(not (pr <= chosen) for pr in incident[v]):
            chosen.add(v)
            bt(idx + 1, cnt + 1)
            chosen.discard(v)
        bt(idx + 1, cnt)

    bt(0, 0)
    return best[0]


def no_3ap(S):
    """True iff S contains no 3-term AP (used to verify a Sidon witness)."""
    Sset = set(S)
    for a, c in itertools.combinations(sorted(S), 2):
        m = a + c
        if m % 2 == 0 and (m // 2) in Sset and (m // 2) not in (a, c):
            return False
    return True


def floor_h(N):
    """ceil(9N/17): the proven lower bound on h for any (4,5)-set of size N (c* >= 9/17)."""
    return (9 * N + 16) // 17


# ---------------------------------------------------------------------------
# (A) The record gadget: re-establish the bar 4/7, exactly.
# ---------------------------------------------------------------------------

A_base = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
WITNESS8 = [0, 136, 200, 243, 246, 298, 323, 528]  # size-8 Sidon (no-3-AP) subset


def part_A():
    print("=" * 72)
    print("(A) Record 14-point gadget A_base  (bar to beat = 4/7)")
    ok1 = is_45set(A_base)
    ok2 = is_45set_via_differences(A_base)
    assert ok1 == ok2, "the two (4,5) checks disagree!"
    h = alpha_exact(A_base)
    assert set(WITNESS8) <= set(A_base) and no_3ap(WITNESS8) and len(WITNESS8) == 8
    print(f"    is (4,5)-set: {ok1};  h(A_base) = {h};  size-8 Sidon witness: ok")
    print(f"    => c* <= {h}/14 = 4/7  (7*{h}={7*h} == 4*14=56: ties record)")
    assert ok1 and h == 8
    return h


# ---------------------------------------------------------------------------
# (B) The floor at N=18: which single h-value would beat 4/7?
# ---------------------------------------------------------------------------

def part_B():
    print("=" * 72)
    print("(B) Floor from the proven lower bound c* >= 9/17  =>  h >= ceil(9N/17)")
    for N in (14, 15, 16, 17, 18):
        fl = floor_h(N)
        beats_fl = 7 * fl < 4 * N
        print(f"    N={N}: floor h = {fl}  (ratio {fl}/{N} = {fl/N:.4f}; "
              f"{'BEATS' if beats_fl else 'does NOT beat'} 4/7)")
    # At N=18 the unique beating h is exactly the floor 10:
    assert floor_h(18) == 10
    assert 7 * 10 < 4 * 18          # 70 < 72  -> 10/18 < 4/7  (beat)
    assert not (7 * 11 < 4 * 18)    # 77 < 72 false -> 11/18 does NOT beat 4/7
    print("    => at N=18, ONLY h=10 (= floor) beats 4/7; h=11 (11/18=0.6111) does NOT.")
    return floor_h(18)


# ---------------------------------------------------------------------------
# (C) Best 18-point (4,5)-set found: h = 11 (NOT a beat), verified + local min.
# ---------------------------------------------------------------------------

# Found by exact-alpha record-extension / stochastic-beam search (see log summary in
# the approach doc).  This is the smallest alpha realized at N=18 across all methods.
BEST_N18 = [0, 2, 9, 10, 18, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]


def one_swap_is_local_min(A, lo=0, hi=1300):
    """True iff no single-point replacement (value in [lo,hi]) of A yields a
    weak-Sidon set with strictly smaller alpha.  Exact, deterministic."""
    base_alpha = alpha_exact(A)
    A = sorted(A)
    for i in range(len(A)):
        rest = A[:i] + A[i + 1:]
        sm = set()
        for a in range(len(rest)):
            for b in range(a + 1, len(rest)):
                sm.add(rest[a] + rest[b])
        for v in range(lo, hi + 1):
            if v in rest:
                continue
            ok = True
            loc = set()
            for x in rest:
                s = x + v
                if s in sm or s in loc:
                    ok = False
                    break
                loc.add(s)
            if not ok:
                continue
            if alpha_exact(sorted(rest + [v])) < base_alpha:
                return False, (i, v)
    return True, None


def part_C(check_local_min=True):
    print("=" * 72)
    print("(C) Best 18-point (4,5)-set found  (h = 11, does NOT beat 4/7)")
    A = BEST_N18
    assert len(A) == 18 and len(set(A)) == 18
    ok1 = is_45set(A)
    ok2 = is_45set_via_differences(A)
    assert ok1 == ok2
    h = alpha_exact(A)
    print(f"    A = {A}")
    print(f"    is (4,5)-set: {ok1};  h(A) = {h};  ratio = {h}/18 = {h/18:.4f}")
    print(f"    beats 4/7? {'YES' if 7*h < 4*18 else 'NO'}  "
          f"(7*{h}={7*h} vs 4*18=72)")
    assert ok1 and h == 11
    if check_local_min:
        is_min, viol = one_swap_is_local_min(A)
        print(f"    1-swap local minimum over [0,1300]: {is_min}"
              + ("" if is_min else f"  (improving swap {viol})"))
        assert is_min
    return h


# ---------------------------------------------------------------------------
# (D) The "floor + 1" obstruction: wide-beam record extension per N.
# ---------------------------------------------------------------------------

def _sums(A):
    s = set()
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            s.add(A[i] + A[j])
    return s


def _ext_cands(B, lo, hi):
    sm = _sums(B)
    out = []
    for v in range(lo, hi + 1):
        if v in B:
            continue
        ok = True
        loc = set()
        for x in B:
            s = x + v
            if s in sm or s in loc:
                ok = False
                break
            loc.add(s)
        if ok:
            out.append(v)
    return out


def part_D(beam_width=24, lo=0, hi=1300):
    """Wide-beam exact-alpha extension of A_base from N=14 to N=18.  Records the
    minimum alpha reached at each N.  Deterministic (no randomness).  Reproduces the
    floor+1 obstruction pattern (slower than A-C; ~1-2 min)."""
    print("=" * 72)
    print(f"(D) Wide-beam (BW={beam_width}) exact-alpha extension of the record set")
    beam = [(alpha_exact(A_base), sorted(A_base))]
    print(f"    N=14: min alpha = {beam[0][0]}  (floor {floor_h(14)})")
    pattern = {14: beam[0][0]}
    for N in range(15, 19):
        newbeam = []
        for _, B in beam:
            for v in _ext_cands(B, lo, hi):
                C = sorted(B + [v])
                newbeam.append((alpha_exact(C), C))
        newbeam.sort(key=lambda t: t[0])
        seen = set()
        ded = []
        for al, B in newbeam:
            key = tuple(B)
            if key in seen:
                continue
            seen.add(key)
            ded.append((al, B))
        beam = ded[:beam_width]
        pattern[N] = beam[0][0]
        fl = floor_h(N)
        print(f"    N={N}: min alpha = {beam[0][0]}  (floor {fl}, "
              f"= floor + {beam[0][0] - fl})")
    # The headline obstruction: floor+1 at every extended N, floor only at N=14.
    assert pattern[14] == floor_h(14)
    for N in range(15, 19):
        assert pattern[N] == floor_h(N) + 1, (N, pattern[N], floor_h(N))
    print("    => record extension reaches floor only at N=14; floor+1 at N=15..18.")
    print(f"    => best N=18 alpha = {pattern[18]} (= 11), NOT the floor 10. No beat.")
    return pattern


# ---------------------------------------------------------------------------

def main(run_D=True):
    h14 = part_A()
    fl18 = part_B()
    h18 = part_C()
    if run_D:
        part_D()
    print("=" * 72)
    print("SUMMARY")
    print(f"  Bar (verified record):     c* <= 4/7 = {4/7:.7f}   [N=14, h=8]")
    print(f"  N=18 beating target:       h = {fl18} (= floor)  -> 10/18 = {10/18:.4f}")
    print(f"  Best N=18 (4,5)-set found: h = {h18}  -> {h18}/18 = {h18/18:.4f}  "
          f"(does NOT beat 4/7)")
    print("  Strict beat found:         NO. Floor h=10 not realized at N=18 in the")
    print("                             searched region (record neighborhood + random +")
    print("                             SA + stochastic beam; alpha = 11 is a 1-swap")
    print("                             local minimum).  Held bound stays 4/7.")
    print("=" * 72)


if __name__ == "__main__":
    main()
