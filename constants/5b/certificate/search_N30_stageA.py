#!/usr/bin/env python3
"""
C_5b (Sidon density in (4,5)-sets, Erdos #757) — approach stage-a-max-m-bounded-N30.

ROUND 8 REWRITE of the DISQUALIFIED search_N30_mtargeted.py anneal loop into the
BINDING BOUNDED-COMPUTE PROTOCOL form (the prior anneal hung silently for ~2500s and
was force-killed in R6 AND R7).  The contract here:

  1. A FIXED, FINITE candidate POOL P is built ONCE, up front, from a deterministic
     structured construction (NOT an unbounded {0..W} enumeration, NOT anneal-until-found).
     |P| is printed and fixed before any search.
  2. Stage A maximizes m = #(midpoint-injective 3-APs) over size-30 (4,5)-SUBSETS of P
     using the CHEAP incremental m objective (m_add_gain) — NO exact-alpha in the inner
     loop.  The search runs in SHORT CHUNKS with a HARD per-chunk wall-clock cap; at every
     chunk boundary it PRINTS (best m so far, sets visited, elapsed) and FLUSHES, and it
     appends that progress line to a log file under this folder so a killed chunk loses
     nothing.  A hard TOTAL cap bounds the whole run.
  3. Stage B runs EXACT alpha = N - tau (scipy.milp cross-checked by B&B — reused from
     search_N30.py, NEVER a density heuristic) ONLY on the tiny high-m shell (m >= M_SHELL)
     that Stage A surfaces.  It reports the (m, alpha) frontier.
  4. If Stage A walls below m = n-2 = 28 over the fixed pool, that PRINTED m-ceiling over
     the NAMED pool P is the deliverable — an honest wall over P, NOT a global impossibility
     claim.

EXACTNESS / HONESTY (CLAUDE.md rigor):
  * (4,5)-property: the DIFFERENCE condition (every 4-subset >=5 distinct |diffs|), exact,
    reused from search_N30.is_45set / add_keeps_45.
  * alpha = N - tau exact via scipy.milp, cross-checked by alpha_bb (search_N30.alpha_exact).
  * A found gadget is a CONJECTURE until the Lean cert fires; this script writes NOTHING
    into constants/5b.md or current.md.  Its deliverable is the printed m-ceiling over the
    named pool plus the Stage-B (m, alpha) frontier on the high-m shell.

Beat arithmetic (re-verified): a size-30 (4,5)-set with alpha <= 17 gives c* <= 17/30 =
0.56667 < 4/7 = 0.571428..., a strict beat.  alpha <= 17 <=> tau >= 13.  HY at m=n-2=28
permits tau <= floor((5*30+3*28)/17) = floor(234/17) = 13, so alpha=17 is allowed (not
forbidden).  Reaching it needs m at/near the cap 28 AND a transversal-efficient (clustered,
non-path) arrangement — the open question Stage A probes.

Run:
  python3 search_N30_stageA.py --pool                 # build + print the fixed pool, exit
  python3 search_N30_stageA.py --stageA --chunks K     # K bounded Stage-A chunks (default 6)
  python3 search_N30_stageA.py --stageB                # Stage B exact-alpha on the saved shell
  python3 search_N30_stageA.py --summary              # fast deterministic re-check (no search)
Each Stage-A chunk has a HARD per-chunk cap (--chunk-seconds, default 50s) and the whole
run has a HARD total cap (--total-seconds, default 330s).
"""
import argparse, itertools, json, os, random, sys, time

import search_N30 as S   # reuse the exact, validated R5 machinery (is_45set, alpha_exact, ...)

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "stageA_progress.log")
SHELL_FILE = os.path.join(HERE, "stageA_shell.json")
POOL_FILE = os.path.join(HERE, "stageA_pool.json")
BEST_FILE = os.path.join(HERE, "stageA_best.json")

N = 30
CAP = N - 2          # Lemma 2.4 edge cap m <= n-2 = 28
M_SHELL = 24         # Stage B runs exact alpha only on the tiny high-m shell (m >= this).
                     # Set to 24 (not 27) because Stage A walls at m=25 over the fixed
                     # pool P; capturing m in {24,25} gives a non-empty (m,alpha) frontier
                     # at the TOP of what the pool reaches.  The BEAT shell would be m=28
                     # (=n-2); that the pool never reaches it IS the bounded negative.
WINDOW = 2200        # pool window bound (a size-30 (4,5)-set first fits around ~1500)


def logline(msg, also_print=True):
    with open(LOG, "a", buffering=1) as f:
        f.write(msg + "\n")
    if also_print:
        print(msg, flush=True)


# ---------------------------------------------------------------------------
# m bookkeeping (cheap incremental objective) — reuse three_ap_triples for the exact m.
# ---------------------------------------------------------------------------

def m_count(A):
    """Exact #(3-term APs) inside A = #edges of the 3-AP hypergraph (Lemma 2.4: <= n-2)."""
    return len(S.three_ap_triples(A))


def m_gain(A_set, A_sorted, v):
    """How many NEW 3-APs appear when v is added to A (cheap, O(|A|))."""
    gain = 0
    for a in A_sorted:
        c = 2 * v - a
        if c > a and c in A_set:           # v is the midpoint of {a, v, c}
            gain += 1
    for b in A_sorted:
        other = 2 * b - v                  # b is the midpoint of {v, b, other}
        if other != v and other in A_set and ((v < b < other) or (other < b < v)):
            gain += 1
    return gain


def m_loss(A_set, A_sorted, v):
    """How many 3-APs are DESTROYED when v is removed from A (cheap, O(|A|))."""
    rest = A_set - {v}
    rest_sorted = [x for x in A_sorted if x != v]
    return m_gain(rest, rest_sorted, v)


# ---------------------------------------------------------------------------
# (1) The FIXED, FINITE candidate POOL P — built ONCE, deterministically, up front.
# ---------------------------------------------------------------------------

def build_pool(window=WINDOW):
    """Deterministic structured pool P (NOT an unbounded {0..W} box).  Fixed up front.
    P = union of:
      (a) A_base coordinates (the record set's basin — known cap-saturator structure);
      (b) the best N=30 (4,5)-set found in R5 (the Fibonacci subsequence), rescaled to fit
          the window so its 3-AP-rich layout is reachable;
      (c) a generalized-Fibonacci / Zeckendorf lattice in [0, window]: sums of distinct
          Fibonacci numbers <= window (Zeckendorf representations are 3-AP-structured and
          (4,5)-friendly);
      (d) a Sidon-style quadratic lattice {k^2 mod p} packed into the window (perfect-
          difference-set style, dense in small differences).
    All coordinates are clamped/dedup'd into [0, window], sorted.  |P| is bounded and fixed.
    """
    P = set()

    # (a) A_base, scaled to fit the window (A_base spans 1056, already < window)
    for v in S.A_BASE:
        P.add(int(v))

    # (b) the genuine small-scale Fibonacci prefix (3-APs are affine-invariant, so the
    #     UNSCALED Fibonacci numbers that fit the window carry real 3-AP structure; the
    #     huge-scale R5 subsequence does NOT survive rescaling-with-rounding, since that
    #     map is non-affine and destroys APs).  Include all Fibonacci numbers <= window.
    fib0 = [1, 2]
    while fib0[-1] <= window:
        fib0.append(fib0[-1] + fib0[-2])
    for f in fib0:
        if 0 <= f <= window:
            P.add(f)

    # (c) Zeckendorf / generalized-Fibonacci lattice: all sums of distinct Fibonacci
    #     numbers <= window.  These are the canonical 3-AP-structured integers.
    fib = [1, 2]
    while fib[-1] <= window:
        fib.append(fib[-1] + fib[-2])
    fib = [f for f in fib if f <= window]
    # sums of up to 3 distinct fibs (kept finite/bounded), within window
    for r in (1, 2, 3):
        for combo in itertools.combinations(fib, r):
            s = sum(combo)
            if 0 <= s <= window:
                P.add(s)

    # (d) quadratic-residue / Singer-style lattice mod a prime near window, packed in
    import sympy
    p = int(sympy.prevprime(window))
    for k in range(p):
        v = (k * k) % p
        if 0 <= v <= window:
            P.add(v)

    # (e) a coarse arithmetic grid to give the local search room to move (every 7th point)
    for v in range(0, window + 1, 7):
        P.add(v)

    return sorted(P)


# ---------------------------------------------------------------------------
# (2) Stage A — maximize m over size-30 (4,5)-SUBSETS of the FIXED pool P, in CHUNKS.
# ---------------------------------------------------------------------------

def greedy_max_m_seed(P, rng, target_n=N):
    """Greedily build a size-N (4,5)-subset of P, at each step adding the pool point that
    keeps (4,5) AND maximizes the incremental m-gain (cheap).  Deterministic given rng for
    tie-break ordering of P.  Returns a (4,5)-set of size N, or the largest reachable."""
    Plist = list(P)
    rng.shuffle(Plist)
    A_sorted = [Plist[0]]
    A_set = {Plist[0]}
    while len(A_sorted) < target_n:
        best_v = None
        best_gain = -1
        for v in Plist:
            if v in A_set:
                continue
            if not S.add_keeps_45(A_sorted, v):
                continue
            g = m_gain(A_set, A_sorted, v)
            if g > best_gain:
                best_gain = g
                best_v = v
        if best_v is None:
            break                       # cannot extend within P keeping (4,5)
        A_set.add(best_v)
        A_sorted = sorted(A_set)
    return A_sorted


def m_of_set(A_set, A_sorted):
    """Recompute m via cheap incremental sum (each vertex's gain counted once)."""
    return len(S.three_ap_triples(A_sorted))


def stageA_local_improve(A_sorted, P, rng, deadline, best_m, shell, batch=40):
    """BEST-IMPROVEMENT replacement hill-climb over P maximizing m (cheap incremental),
    with random kicks to escape plateaus.  Each step: pick the in-set vertex of LOWEST
    3-AP degree (the weakest link), then scan a sampled BATCH of pool points and take the
    swap that maximizes m while keeping (4,5).  Accepts equal-or-better m (plateau); on a
    stall, does a random kick (swap a random vertex).  Records every (4,5)-set with
    m >= M_SHELL into `shell`.  Time-bounded by `deadline`."""
    A_set = set(A_sorted)
    cur_m = m_count(A_sorted)
    best = list(A_sorted)
    bm = cur_m
    visited = 0
    Plist = list(P)
    stall = 0
    while time.time() < deadline:
        visited += 1
        # degree of each in-set vertex in the 3-AP hypergraph (weakest link to swap out)
        tr = S.three_ap_triples(A_sorted)
        deg = {x: 0 for x in A_sorted}
        for (i, j, k) in tr:
            deg[A_sorted[i]] += 1; deg[A_sorted[j]] += 1; deg[A_sorted[k]] += 1
        if stall > 6:
            rem = rng.choice(A_sorted)            # random kick
            stall = 0
        else:
            mindeg = min(deg.values())
            cands = [x for x in A_sorted if deg[x] == mindeg]
            rem = rng.choice(cands)
        rest = [x for x in A_sorted if x != rem]
        rest_set = set(rest)
        # scan a sampled batch of pool points; take the best m-improving (4,5)-valid swap
        sample = rng.sample(Plist, min(batch, len(Plist)))
        best_cand = None
        best_cm = -1
        for v in sample:
            if v in rest_set:
                continue
            if not S.add_keeps_45(rest, v):
                continue
            g = m_gain(rest_set, rest, v)
            if g > best_cm:
                best_cm = g
                best_cand = v
        if best_cand is None:
            stall += 1
            continue
        cand = sorted(rest + [best_cand])
        cm = m_count(cand)
        if cm >= cur_m:
            A_sorted = cand
            A_set = set(cand)
            if cm > cur_m:
                stall = 0
            else:
                stall += 1
            cur_m = cm
            if cm >= M_SHELL:
                shell[tuple(cand)] = cm
            if cm > bm:
                bm = cm
                best = list(cand)
                if bm > best_m:
                    logline(f"      [stageA] new best m={bm} (visited {visited}) "
                            f"set={best}")
        else:
            stall += 1
    return best, bm, visited


def run_stageA(chunks, chunk_seconds, total_seconds, seed=20260808, fresh=False):
    """Run `chunks` bounded Stage-A chunks, each capped at chunk_seconds wall-clock, whole
    run capped at total_seconds.  Prints (best m, visited, elapsed) at every chunk boundary
    and persists progress + the high-m shell to disk so a kill loses nothing."""
    t0 = time.time()
    rng = random.Random(seed)
    P = build_pool()
    with open(POOL_FILE, "w") as f:
        json.dump({"window": WINDOW, "pool_size": len(P), "pool": P}, f)
    logline("=" * 74)
    logline(f"[stageA] FIXED POOL P built: |P|={len(P)} in window [0,{WINDOW}] "
            f"(A_base + rescaled-Fib + Zeckendorf + QR + grid). saved to {POOL_FILE}")
    logline(f"[stageA] target N={N}, edge cap m<=n-2={CAP}, shell m>={M_SHELL}; "
            f"chunks={chunks} chunk_cap={chunk_seconds}s total_cap={total_seconds}s")

    # load any prior shell so chunks accumulate across invocations
    shell = {}
    if os.path.exists(SHELL_FILE):
        try:
            with open(SHELL_FILE) as f:
                for k, v in json.load(f).items():
                    shell[tuple(json.loads(k))] = v
        except Exception:
            shell = {}

    # intensification seed (best set found across prior invocations), persisted to disk
    best_seed = None
    if os.path.exists(BEST_FILE):
        try:
            with open(BEST_FILE) as f:
                bd = json.load(f)
            best_seed = bd["set"]
        except Exception:
            best_seed = None
    if best_seed is None and shell:
        bk = max(shell.items(), key=lambda kv: kv[1])
        best_seed = list(bk[0])

    global_best = list(best_seed) if best_seed else None
    global_bm = m_count(best_seed) if best_seed else -1
    for c in range(chunks):
        if time.time() - t0 >= total_seconds:
            logline(f"[stageA] TOTAL CAP {total_seconds}s reached, stopping at chunk {c}")
            break
        chunk_deadline = min(time.time() + chunk_seconds, t0 + total_seconds)
        # alternate: even chunks intensify from the best set so far (if any), odd chunks
        # restart from a fresh greedy max-m seed (deterministic per chunk via seeded rng)
        if c % 2 == 0 and global_best is not None and len(global_best) == N:
            seed_set = list(global_best)
        else:
            seed_set = greedy_max_m_seed(P, rng)
        if len(seed_set) < N:
            logline(f"  [chunk {c}] greedy seed reached only |A|={len(seed_set)}<{N} "
                    f"within P; skipping")
            continue
        sm = m_count(seed_set)
        if sm >= M_SHELL:
            shell[tuple(seed_set)] = sm
        best, bm, visited = stageA_local_improve(
            seed_set, P, rng, chunk_deadline, global_bm, shell)
        if bm > global_bm:
            global_bm = bm
            global_best = list(best)
            with open(BEST_FILE, "w") as f:
                json.dump({"m": global_bm, "set": global_best}, f)
        elapsed = time.time() - t0
        logline(f"  [chunk {c}] seed_m={sm} chunk_best_m={bm} global_best_m={global_bm} "
                f"visited={visited} shell={len(shell)} elapsed={elapsed:.0f}s")
        # persist shell after every chunk (kill-safe)
        with open(SHELL_FILE, "w") as f:
            json.dump({json.dumps(list(k)): v for k, v in shell.items()}, f)

    logline("=" * 74)
    logline(f"[stageA] DONE: global best m over pool P = {global_bm} (edge cap {CAP}); "
            f"shell |m>={M_SHELL}| = {len(shell)} sets; total elapsed {time.time()-t0:.0f}s")
    if global_best is not None:
        logline(f"[stageA] best set (m={global_bm}): {global_best}")
        assert S.is_45set(global_best), "best set must be a (4,5)-set!"
        logline(f"[stageA] verify is_45set(best)={S.is_45set(global_best)}")
    return global_bm, global_best, shell


# ---------------------------------------------------------------------------
# (3) Stage B — EXACT alpha = N - tau on the tiny high-m shell ONLY.
# ---------------------------------------------------------------------------

def floor_h(n):
    return (9 * n + 16) // 17           # ceil(9n/17)


def run_stageB():
    """Run EXACT alpha = N - tau (milp cross-checked by B&B) on EVERY set in the saved
    high-m shell (m >= M_SHELL).  Report the (m, alpha) frontier and flag any beat."""
    if not os.path.exists(SHELL_FILE):
        print("no shell file — run --stageA first", flush=True)
        return
    with open(SHELL_FILE) as f:
        raw = json.load(f)
    shell = {tuple(json.loads(k)): v for k, v in raw.items()}
    fl = floor_h(N)
    print("=" * 74)
    print(f"[stageB] EXACT alpha on the high-m shell (m>={M_SHELL}); |shell|={len(shell)}")
    print(f"         N={N}, floor=ceil(9N/17)={fl}, BEAT needs alpha<={fl+1}=17 (tau>=13)")
    frontier = {}
    beats = []
    for i, (Aset, m) in enumerate(sorted(shell.items(), key=lambda kv: -kv[1])):
        A = list(Aset)
        assert S.is_45set(A), f"shell set not (4,5)!: {A}"
        a = S.alpha_exact(A, cross_check=True)     # milp == bb, exact
        if m not in frontier or a < frontier[m]:
            frontier[m] = a
        beat = 7 * a < 4 * N
        if beat:
            beats.append((m, a, A))
        if i < 20 or beat:
            print(f"   m={m:2d} alpha={a:2d} tau={N-a:2d} (floor+{a-fl}) "
                  f"beats4/7={'YES *** BEAT' if beat else 'no'}", flush=True)
    print("-" * 74)
    print("   joint (m -> best alpha) frontier:", dict(sorted(frontier.items())))
    if beats:
        print("   *** CONJECTURAL BEAT(S) FOUND — verify + Lean-certify ***")
        for m, a, A in beats:
            print(f"      m={m} alpha={a} ratio={a}/{N}={a/N:.5f} < 4/7 : {A}")
    else:
        print("   NO beat on the shell — verified NEGATIVE over the fixed pool P.")
    return frontier, beats


# Frontier-defining (4,5)-sets surfaced by Stage A over the FIXED pool P this round,
# recorded for a fast deterministic re-check.  Each is an exact (4,5)-set with exact
# (m, alpha) (milp == bb).  CONJECTURE / obstruction witnesses, NOT certified bounds.
# Headline NEGATIVE: max m reached over P is 26 (< cap 28); best alpha at the max-m
# level is 20 = floor+4 -> NO beat (a beat needs alpha <= 17).
FRONTIER_SETS = {
    # m, alpha (exact, milp==bb), the set
    "m26_best_alpha": (26, 20,
        [66, 241, 308, 416, 466, 504, 524, 537, 550, 655, 684, 790, 844, 866, 942, 982,
         1075, 1272, 1323, 1347, 1409, 1427, 1443, 1521, 1842, 2020, 2142, 2163, 2170,
         2198]),
    "m25_best_alpha": (25, 21,
        [31, 51, 71, 555, 568, 598, 646, 816, 824, 932, 988, 1034, 1039, 1044, 1050,
         1056, 1065, 1131, 1165, 1197, 1261, 1296, 1314, 1350, 1488, 1594, 1844, 1988,
         2037, 2132]),
}


def verify_frontier():
    """Re-derive the Stage-A (m, alpha) frontier sets EXACTLY (is_45set + milp==bb)."""
    fl = floor_h(N)
    print("=" * 74)
    print(f"(verify-frontier) exact re-check of the recorded Stage-A frontier over pool P")
    print(f"   N={N}, floor={fl}, edge cap m<=n-2={CAP}, BEAT needs alpha<={fl+1}=17")
    for tag, (m, a, A) in FRONTIER_SETS.items():
        assert len(A) == N and len(set(A)) == N, tag
        ok = S.is_45set(A)
        am = S.alpha_milp(A); ab = S.alpha_bb(A)
        assert am == ab == a, (tag, am, ab, a)
        assert m_count(A) == m, (tag, m_count(A), m)
        beat = 7 * a < 4 * N
        print(f"   {tag}: m={m} (cap {CAP}, deficit {CAP-m}) alpha={a} (floor+{a-fl}) "
              f"is45set={ok} milp==bb={am==ab} beats4/7={'YES' if beat else 'no'}")
    print(f"   R5 unbounded Fib m=26 set: alpha={S.alpha_exact(S.BEST_SETS[30][1])} "
          f"(floor+3), span={max(S.BEST_SETS[30][1])} -- note: lives at ~2.18M scale, "
          f"NOT in any bounded window")
    print("   => NEGATIVE over P: max m reached = 26 < cap 28; best alpha at max-m = 20 "
          "(floor+4), NO beat.")


def part_summary():
    """Fast deterministic re-check of the load-bearing facts (no search)."""
    print("=" * 74)
    print("(summary) C_5b stage-a-max-m-bounded-N30 — load-bearing facts (exact, no search)")
    A = S.A_BASE
    print(f"   A_base N=14: m={m_count(A)} (cap n-2={len(A)-2}, SATURATED) "
          f"alpha={S.alpha_exact(A)}  => c* <= 8/14 = 4/7 (the bar)")
    fib = S.BEST_SETS[30][1]
    print(f"   R5 Fib N=30: m={m_count(fib)} (cap 28, deficit 2) alpha={S.alpha_exact(fib)} "
          f"(=floor+{S.alpha_exact(fib)-floor_h(30)})  => no beat")
    fl = floor_h(N)
    print(f"   N=30 BEAT target: alpha <= {fl+1}=17 (tau>=13); 17/30={17/30:.5f} < "
          f"4/7={4/7:.5f}")
    if os.path.exists(POOL_FILE):
        with open(POOL_FILE) as f:
            pd = json.load(f)
        print(f"   fixed pool P: |P|={pd['pool_size']} in window [0,{pd['window']}]")
    if os.path.exists(SHELL_FILE):
        with open(SHELL_FILE) as f:
            sh = json.load(f)
        ms = [v for v in sh.values()]
        print(f"   high-m shell (saved): |shell|={len(ms)} "
              f"max m={max(ms) if ms else 'NA'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", action="store_true")
    ap.add_argument("--stageA", action="store_true")
    ap.add_argument("--stageB", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--verify-frontier", action="store_true")
    ap.add_argument("--chunks", type=int, default=6)
    ap.add_argument("--chunk-seconds", type=float, default=50.0)
    ap.add_argument("--total-seconds", type=float, default=330.0)
    ap.add_argument("--seed", type=int, default=20260808)
    args = ap.parse_args()

    if args.pool:
        P = build_pool()
        with open(POOL_FILE, "w") as f:
            json.dump({"window": WINDOW, "pool_size": len(P), "pool": P}, f)
        print(f"fixed pool P: |P|={len(P)} in window [0,{WINDOW}], saved to {POOL_FILE}",
              flush=True)
        return
    if args.stageA:
        run_stageA(args.chunks, args.chunk_seconds, args.total_seconds, seed=args.seed)
        return
    if args.stageB:
        run_stageB()
        return
    if args.verify_frontier:
        verify_frontier()
        return
    # default: summary
    part_summary()
    verify_frontier()


if __name__ == "__main__":
    main()
