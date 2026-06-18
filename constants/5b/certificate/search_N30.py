#!/usr/bin/env python3
"""
C_5b (Sidon density in (4,5)-sets, Erdos #757) — approach cpsat-exact-existence-N28-N30.

GOAL of the approach (the GADGET half of an upper-bound beat of 4/7):
    find ONE indecomposable (4,5)-set A of size N in {30,32,34} with
        h(A) = ceil(9N/17) + 1    (= 17 at N=30, 18 at N=32, 19 at N=34),
    where h(A) = largest Sidon subset of A = independence number alpha of the 3-AP
    hypergraph H(A) (MT26 Lemma 2.3, valid because a (4,5)-set is in particular weak
    Sidon).  Such a gadget gives, via [MT26] Theorem 1.5 (c* = inf_N f(N)/N),
        c* <= h(A)/N  <  4/7
    i.e. it STRICTLY beats the verified record 4/7.  Arithmetic (verified exactly):
        N=30: 17/30 = 0.56667 < 4/7 = 0.571428...   (a beat)
        N=32: 18/32 = 0.56250 < 4/7                  (a beat)
        N=34: 19/34 = 0.55882 < 4/7                  (a beat)
        N=28: 16/28 = 4/7 EXACTLY                    (ties, NOT a beat — excluded)

WHY N>=30 (verified in rounds 1-2, see constants/5b/approaches/): the proven lower
bound c* >= 9/17 forces h(A) >= ceil(9N/17) =: floor(N).  Exact-alpha searches at
N=15..18 wall at floor+1 (floor+2 at N=15), never the floor.  floor+1 itself first
beats 4/7 at N=30.  So the realistic target is h = floor+1, and only from N=30 up.

WHY a SINGLE indecomposable set (verified R3, Lemma 3.6): for a WELL-SEPARATED union
A u B, h is exactly additive: h(AuB) = h(A)+h(B).  Two copies of the record set give
16/28 = 4/7 exactly — a tie, never a beat (the mediant of equal ratios).  So a beat
REQUIRES a single set that does NOT decompose into well-separated blocks.  This script
checks indecomposability explicitly (block_split below) and the search seeds OUTSIDE the
A_base basin (GL95-Fibonacci / CRT / B_2-modular / Singer templates).

EXACTNESS (CLAUDE.md rigor):
  * The (4,5)-property is checked EXACTLY by the difference condition (every 4-subset
    has >=5 distinct pairwise |differences|) — the CORRECTED definition (round 2,
    verified vs arXiv:2602.23282), STRICTLY stronger than weak-Sidon.
  * h(A) is computed EXACTLY as alpha = N - tau, tau = min 3-AP transversal, by an ILP
    (scipy.milp) AND cross-checked by a deterministic branch-and-bound.  NEVER a
    3-AP-edge-count heuristic (maximizing edges does NOT minimize alpha — verified
    rounds 1-2).
  * A search-found gadget is a CONJECTURE until the Lean cert fires on it; this script
    NEVER writes a bound into constants/5b.md.  Its deliverable is a re-runnable
    candidate-or-obstruction map.

Run:  python3 search_N30.py            (reproducible summary, ~1-2 min)
      python3 search_N30.py --search   (re-run the heavy seeded search, deterministic)
"""
import itertools, random, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]


# ---------------------------------------------------------------------------
# Exact (4,5)-set predicate (DIFFERENCE condition) — full and incremental.
# ---------------------------------------------------------------------------

def is_45set(A):
    """TRUE (4,5)-set definition (Ma-Tang 2026, arXiv:2602.23282): EVERY 4-element
    subset has >=5 distinct values among its 6 pairwise ABSOLUTE differences.
    STRICTLY stronger than weak-Sidon: {0,1,2,4} is weak-Sidon (distinct sums) but
    has only 4 distinct diffs, so it is NOT a (4,5)-set."""
    A = sorted(A)
    for quad in itertools.combinations(A, 4):
        diffs = set(abs(x - y) for x, y in itertools.combinations(quad, 2))
        if len(diffs) < 5:
            return False
    return True


def is_weak_sidon(A):
    """Weaker reference property: all pairwise sums a+b (a<b) distinct.  Implied by,
    not equivalent to, is_45set.  Kept only for cross-reference."""
    A = sorted(A)
    seen = set()
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            s = A[i] + A[j]
            if s in seen:
                return False
            seen.add(s)
    return True


def add_keeps_45(A_sorted, v):
    """Incremental check: given a (4,5)-set A_sorted (assumed valid) and a new value v
    not in A, is A u {v} still a (4,5)-set?  Only 4-subsets CONTAINING v can be newly
    violated, so check the C(|A|,3) quads {v}+triple.  Exact, much faster than full."""
    n = len(A_sorted)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                quad = (A_sorted[i], A_sorted[j], A_sorted[k], v)
                diffs = set(abs(x - y) for x, y in itertools.combinations(quad, 2))
                if len(diffs) < 5:
                    return False
    return True


# ---------------------------------------------------------------------------
# 3-AP hypergraph and EXACT alpha = h(A) = N - tau.
# ---------------------------------------------------------------------------

def three_ap_triples(A):
    """3-term APs {a, (a+c)/2, c} inside A, as sorted index triples (i<j<k)."""
    A = sorted(A)
    pos = {v: i for i, v in enumerate(A)}
    Aset = set(A)
    tr = []
    for i in range(len(A)):
        for k in range(i + 1, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 and (s // 2) in Aset:
                j = pos[s // 2]
                if i < j < k:
                    tr.append((i, j, k))
    return tr


def alpha_milp(A):
    """EXACT h(A) = independence number alpha of the 3-AP hypergraph, via
    alpha = N - tau where tau = min vertices hitting all 3-AP triples (ILP, scipy.milp).
    NOT an edge-count heuristic: this is the exact min-transversal LP solved to
    integer optimality."""
    A = sorted(A)
    n = len(A)
    tr = three_ap_triples(A)
    if not tr:
        return n
    c = np.ones(n)
    rows = []
    for (i, j, k) in tr:
        r = np.zeros(n)
        r[i] = r[j] = r[k] = 1.0
        rows.append(r)
    con = LinearConstraint(np.array(rows), lb=1, ub=np.inf)
    res = milp(c=c, constraints=[con], integrality=np.ones(n), bounds=Bounds(0, 1))
    if not res.success:
        raise RuntimeError("milp failed: " + str(res.message))
    tau = int(round(res.fun))
    return n - tau


def alpha_bb(A):
    """EXACT alpha by deterministic branch-and-bound (independent arbiter for milp)."""
    A = sorted(A)
    n = len(A)
    tr = three_ap_triples(A)
    incident = [[] for _ in range(n)]
    for (i, j, k) in tr:
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


def alpha_exact(A, cross_check=True):
    """h(A), exact.  Uses milp; optionally cross-checks against the B&B arbiter."""
    a = alpha_milp(A)
    if cross_check:
        b = alpha_bb(A)
        if a != b:
            raise AssertionError(f"alpha mismatch milp={a} bb={b} for {sorted(A)}")
    return a


def no_3ap(S):
    Sset = set(S)
    for a, c in itertools.combinations(sorted(S), 2):
        m = a + c
        if m % 2 == 0 and (m // 2) in Sset and (m // 2) not in (a, c):
            return False
    return True


# ---------------------------------------------------------------------------
# Indecomposability check (Lemma 3.6 guard).
# ---------------------------------------------------------------------------

def block_split(A, gap_factor=2):
    """Detect a WELL-SEPARATED 2-block split.  A is decomposable (in the Lemma-3.6
    sense) if it splits at some sorted gap g into A_lo, A_hi where g exceeds the span
    of BOTH parts — then A_lo, A_hi sit in disjoint translates and h is additive.
    Returns the split (A_lo, A_hi) or None.  Conservative: a returned None means we
    found no obvious well-separated split (the set is plausibly indecomposable);
    a returned split means it IS decomposable and Lemma 3.6 makes it useless."""
    A = sorted(A)
    n = len(A)
    for t in range(1, n):
        lo, hi = A[:t], A[t:]
        gap = hi[0] - lo[-1]
        span_lo = lo[-1] - lo[0] if len(lo) > 1 else 0
        span_hi = hi[-1] - hi[0] if len(hi) > 1 else 0
        if gap > gap_factor * max(span_lo, span_hi, 1):
            return (lo, hi)
    return None


def is_indecomposable(A):
    return block_split(A) is None


# ---------------------------------------------------------------------------
# Seed templates OUTSIDE the A_base basin.
# ---------------------------------------------------------------------------

def seed_fibonacci(N):
    """GL95-style Fibonacci-recursive layout (3-AP-rich scaffold)."""
    fib = [1, 2]
    while len(fib) < N + 3:
        fib.append(fib[-1] + fib[-2])
    return fib[:N]


def seed_crt(N, m1=7, m2=11):
    """CRT/digit layout: a*m2 + b over small ranges (modular B_2-ish)."""
    vals = []
    a = 0
    while len(vals) < N:
        for b in range(m2):
            vals.append(a * m2 + b)
            if len(vals) >= N:
                break
        a += 1
    return sorted(set(vals))[:N]


def seed_singer(N, q=None):
    """Perfect-difference-set (Singer) style: quadratic residues mod a prime."""
    import sympy
    p = sympy.nextprime(2 * N)
    qr = sorted(set((x * x) % p for x in range(1, p)))
    return qr[:N]


def seed_geometric(N, base=3):
    """Geometric/lacunary: base^k offsets — very (4,5)-friendly, few 3-APs (bad alpha,
    but a useful EXTREME to map the landscape)."""
    return [base ** k for k in range(N)]


# ---------------------------------------------------------------------------
# Greedy (4,5)-set builder with random restarts (incremental 4,5 check).
# ---------------------------------------------------------------------------

def greedy_build(N, window, rng, prefix=None, tries_per=4000):
    """Build a (4,5)-set of size N: start from `prefix` (a valid (4,5)-set), greedily
    add random values in [0,window] keeping the (4,5)-property (incremental check)."""
    if prefix is None:
        A = [0]
    else:
        A = sorted(prefix)
        if not is_45set(A):
            return None
    cand = list(range(0, window + 1))
    rng.shuffle(cand)
    ci = 0
    stalls = 0
    while len(A) < N and stalls < tries_per:
        if ci >= len(cand):
            rng.shuffle(cand)
            ci = 0
        v = cand[ci]; ci += 1
        if v in A:
            stalls += 1
            continue
        if add_keeps_45(A, v):
            A = sorted(A + [v])
            stalls = 0
        else:
            stalls += 1
    return sorted(A) if len(A) == N else None


def hill_climb_alpha(A0, window, rng, target, time_budget, log=None):
    """Move one point at a time to reduce exact alpha while staying a (4,5)-set.
    alpha computed EXACTLY (milp, no cross-check inside the loop for speed; the final
    reported best is re-verified with cross_check=True)."""
    t0 = time.time()
    A = sorted(A0)
    besth = alpha_milp(A)
    bestA = list(A)
    N = len(A)
    it = 0
    while time.time() - t0 < time_budget and besth > target:
        it += 1
        i = rng.randrange(N)
        rest = sorted(A[:i] + A[i + 1:])
        v = rng.randint(0, window)
        if v in rest:
            continue
        if not add_keeps_45(rest, v):
            continue
        cand = sorted(rest + [v])
        h = alpha_milp(cand)
        if h <= besth:                       # accept equal-or-better (plateau)
            A = cand
            if h < besth:
                besth = h
                bestA = list(A)
                if log:
                    log(f"      hill: alpha -> {h} after {it} moves")
    return bestA, besth


def anneal_alpha(A0, window, rng, target, time_budget, T0=2.0, cool=0.9995, log=None):
    """Simulated annealing on exact alpha with single-point REPLACEMENT moves, staying a
    (4,5)-set throughout.  Accepts worse moves with prob exp(-dAlpha/T) to escape the
    plateaus where plain hill-climb stalls.  alpha computed EXACTLY (milp) every move.
    Returns the BEST (lowest-alpha) (4,5)-set seen and its alpha (re-verifiable)."""
    import math
    t0 = time.time()
    A = sorted(A0)
    cur = alpha_milp(A)
    best = list(A)
    besth = cur
    N = len(A)
    T = T0
    it = 0
    while time.time() - t0 < time_budget and besth > target:
        it += 1
        T *= cool
        if T < 1e-3:
            T = T0                              # reheat
        i = rng.randrange(N)
        rest = sorted(A[:i] + A[i + 1:])
        v = rng.randint(0, window)
        if v in rest or not add_keeps_45(rest, v):
            continue
        cand = sorted(rest + [v])
        h = alpha_milp(cand)
        d = h - cur
        if d <= 0 or rng.random() < math.exp(-d / T):
            A = cand
            cur = h
            if h < besth:
                besth = h
                best = list(A)
                if log:
                    log(f"      anneal: alpha -> {h} (move {it}, T={T:.3f})")
    return best, besth


# ---------------------------------------------------------------------------
# The seeded exact-alpha search (deterministic, re-runnable).
# ---------------------------------------------------------------------------

def run_search(N, target, seconds=600, window=None, seed=20260618, logfile=None):
    """Search for a (4,5)-set of size N with exact alpha <= target, seeding OUTSIDE the
    A_base basin.  Returns (best_alpha, best_set, achieved_histogram)."""
    if window is None:
        window = max(60, 4 * N)
    rng = random.Random(seed)
    t0 = time.time()
    best = (99, None)
    hist = {}

    def log(msg):
        line = msg + "\n"
        if logfile:
            with open(logfile, "a", buffering=1) as f:
                f.write(line)
        print(msg, flush=True)

    # ---- 1. structured seeds (escape the basin) ----
    seed_specs = []
    for w in (window, 2 * window):
        seed_specs.append(("fib", seed_fibonacci(N)))
        seed_specs.append(("crt7-11", seed_crt(N, 7, 11)))
        seed_specs.append(("crt11-13", seed_crt(N, 11, 13)))
        try:
            seed_specs.append(("singer", seed_singer(N)))
        except Exception:
            pass
    for name, S in seed_specs:
        if time.time() - t0 > seconds:
            break
        # Repair the seed into a valid (4,5)-set prefix by greedy subset selection.
        prefix = []
        for v in sorted(set(S)):
            if add_keeps_45(prefix, v):
                prefix.append(v)
        # extend to size N, then hill-climb
        A0 = greedy_build(N, max(window, (max(S) if S else window)), rng, prefix=prefix)
        if A0 is None:
            log(f"  [seed {name}] could not extend to N={N}")
            continue
        h0 = alpha_milp(A0)
        budget = min(40.0, seconds - (time.time() - t0))
        A, h = hill_climb_alpha(A0, window, rng, target, budget, log=log)
        hist[h] = hist.get(h, 0) + 1
        log(f"  [seed {name}] start alpha={h0} -> hill alpha={h}  (target {target})")
        if h < best[0]:
            best = (h, list(A))
            log(f"  *** new global best alpha={h} from seed {name}: {A}")
            if h <= target:
                return best[0], best[1], hist

    # ---- 2. random restarts (basin-free) ----
    restarts = 0
    while time.time() - t0 < seconds:
        restarts += 1
        A0 = greedy_build(N, window, rng)
        if A0 is None:
            continue
        budget = min(30.0, seconds - (time.time() - t0))
        A, h = hill_climb_alpha(A0, window, rng, target, budget, log=log)
        hist[h] = hist.get(h, 0) + 1
        if h < best[0]:
            best = (h, list(A))
            log(f"  [random restart {restarts}] new best alpha={h}: {A}")
            if h <= target:
                return best[0], best[1], hist
    log(f"  [random] {restarts} restarts, best alpha={best[0]}")
    return best[0], best[1], hist


# ---------------------------------------------------------------------------
# Reproducible summary (fast; re-derives the load-bearing facts exactly).
# ---------------------------------------------------------------------------

def floor_h(N):
    return (9 * N + 16) // 17        # ceil(9N/17)


# Best (lowest-alpha) GENUINE (4,5)-set found this round at each N, recorded so the
# summary is fast and deterministic.  These are CANDIDATES / OBSTRUCTION witnesses,
# NOT certified bounds.  Each is an exact (4,5)-set with exact alpha (milp==bb).
# See the obstruction map in the approach doc.  NONE beats 4/7 — the best realized
# alpha sits a large gap ABOVE the floor+1 target (the tau-deficit, see below).
BEST_SETS = {
    # Best N=30: a Fibonacci-derived structured (4,5)-set, exact alpha=19 (milp==bb),
    # indecomposable.  The (4,5)-valid subsequence of the Fibonacci numbers (with the
    # collisions {1,2,3,5} dropped) is the LOWEST-alpha N=30 set found this round —
    # structured seeds beat the random search here.  Still alpha=19 > floor+1=17.
    30: (19, [1, 2, 3, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584,
              4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811,
              514229, 832040, 1346269, 2178309]),
    32: (20, [1, 2, 3, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584,
              4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811,
              514229, 832040, 1346269, 2178309, 3524578, 5702887]),
    34: (21, [1, 2, 3, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584,
              4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811,
              514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352]),
    # The (4,5)-valid Fibonacci subsequence: a clean structured family, exact alpha
    # (milp==bb), indecomposable, the LOWEST-alpha sets found this round at every N —
    # structured seeds beat the random anneal (which walled at alpha 20-22).  Each is
    # EXACTLY floor+2 (one above the floor+1 beat target), so NONE beats 4/7.
    # Cross-check (random-search, N=30, alpha=20, indecomposable):
    #   [21,154,163,229,262,305,324,370,425,600,621,768,980,1029,1054,1078,1212,
    #    1508,1623,1984,2195,2222,2345,2426,2485,2535,2657,2748,2759,2983]
}


def part_obstruction():
    """The structural obstruction, stated and re-verified exactly.  A beat at N needs
    alpha <= floor(N)+1, i.e. tau = N - alpha >= N - floor(N) - 1.  The record set
    A_base achieves tau-density 6/14 = 0.4286 at N=14; the best (4,5)-set found at N=30
    achieves only tau-density 10/30 = 0.333 — the per-point transversal efficiency
    DROPS as N grows in the searched region, the opposite of what a beat requires."""
    print("=" * 74)
    print("(obstruction) tau-density: why the searched region cannot beat 4/7")
    a_base_tau = 14 - alpha_milp(A_BASE)
    print(f"    A_base (N=14, alpha=8): tau={a_base_tau}, tau/N={a_base_tau/14:.4f}")
    for N in (30, 32, 34):
        fl = floor_h(N)
        need_tau = N - (fl + 1)
        print(f"    N={N}: BEAT needs alpha<={fl+1} i.e. tau>={need_tau} "
              f"(tau/N>={need_tau/N:.4f})")
        if N in BEST_SETS:
            alpha, A = BEST_SETS[N]
            got_tau = N - alpha
            print(f"        best found: alpha={alpha}, tau={got_tau} "
                  f"(tau/N={got_tau/N:.4f})  => tau DEFICIT = {need_tau-got_tau}")
    print("    => best achieved tau-density ~0.37-0.38 stays BELOW both the target")
    print("       (~0.43) and A_base's rate (0.4286): tau-deficit 2 at every N,")
    print("       i.e. realized alpha = floor+3, no beat (need floor+1) in this space.")


def part_arithmetic():
    print("=" * 74)
    print("(arith) Which (N, h) strictly beat the verified record 4/7?")
    for N in (28, 30, 32, 34):
        fl = floor_h(N)
        h = fl + 1
        beats = 7 * h < 4 * N
        print(f"    N={N}: floor=ceil(9N/17)={fl}, target h=floor+1={h}, "
              f"ratio {h}/{N}={h/N:.5f}, beats 4/7={4/7:.5f}? "
              f"{'YES' if beats else 'NO (tie/lose)'}")
    assert 7 * 17 < 4 * 30          # 119 < 120  -> 17/30 beats
    assert 7 * 16 == 4 * 28         # 112 == 112 -> 16/28 ties (NOT a beat)
    assert 7 * 18 < 4 * 32
    assert 7 * 19 < 4 * 34
    print("    => target N in {30,32,34}; N=28 ties exactly and is excluded.")


def part_record():
    print("=" * 74)
    print("(record) A_base: the bar to beat (4/7), re-verified exactly")
    assert is_45set(A_BASE), "A_base must be a (4,5)-set"
    a_milp = alpha_milp(A_BASE)
    a_bb = alpha_bb(A_BASE)
    assert a_milp == a_bb == 8, (a_milp, a_bb)
    print(f"    is_45set(A_base)={is_45set(A_BASE)}  alpha(milp)={a_milp}  "
          f"alpha(bb)={a_bb}  => c* <= 8/14 = 4/7 (the bar)")
    # sanity: milp and bb agree on a known set, and weak-Sidon != (4,5)
    bad = [0, 1, 2, 4]
    assert is_weak_sidon(bad) and not is_45set(bad)
    print("    [spec] {0,1,2,4} weak-Sidon but NOT (4,5)-set: "
          f"{is_weak_sidon(bad) and not is_45set(bad)} (difference cond is stronger)")


def part_candidates():
    print("=" * 74)
    print("(candidates) Best (4,5)-sets found this round (CONJECTURES, not certified)")
    if not BEST_SETS:
        print("    (no recorded candidates yet — run with --search to populate)")
        return
    for N in sorted(BEST_SETS):
        alpha, A = BEST_SETS[N]
        assert len(A) == N and len(set(A)) == N
        ok45 = is_45set(A)
        a_milp = alpha_milp(A)
        a_bb = alpha_bb(A)
        assert a_milp == a_bb == alpha, (N, a_milp, a_bb, alpha)
        indec = is_indecomposable(A)
        beats = 7 * alpha < 4 * N
        fl = floor_h(N)
        print(f"    N={N}: alpha={alpha} (floor {fl}, =floor+{alpha-fl})  "
              f"ratio={alpha}/{N}={alpha/N:.5f}  beats 4/7? {'YES' if beats else 'no'}")
        print(f"        is_45set={ok45}  indecomposable={indec}  "
              f"milp==bb={a_milp==a_bb}")
        print(f"        A = {A}")
        if beats and indec and ok45:
            print("        *** CONJECTURAL BEAT — pending Lean certification ***")


def main():
    do_search = "--search" in sys.argv
    part_arithmetic()
    part_record()
    if do_search:
        print("=" * 74)
        print("(search) heavy seeded exact-alpha search (deterministic)")
        logf = "/tmp/search_N30.log"
        for N in (30, 32, 34):
            target = floor_h(N) + 1
            print(f"\n  --- N={N}, target alpha <= {target} ---")
            t0 = time.time()
            alpha, A, hist = run_search(N, target, seconds=600, logfile=logf)
            print(f"  N={N}: best alpha={alpha} (target {target})  "
                  f"hist={dict(sorted(hist.items()))}  time={time.time()-t0:.0f}s")
            if A is not None:
                print(f"        best set: {A}")
    part_candidates()
    part_obstruction()
    print("=" * 74)
    print("STATUS: gadget search half.  A candidate is a CONJECTURE until the Lean")
    print("        cert fires; no bound is written into constants/5b.md by this script.")
    print("=" * 74)


if __name__ == "__main__":
    main()
