"""Sketch: maxdigit-base-sweep  (constant 3a, LOWER bound)

TARGET (top-level claim):
    There exist a finite digit alphabet A = {0, 2, 3, ..., M} (0 in A, 1 omitted, max digit
    M), digit count d, global sum cap T, with carry-free base b = 2*M+1, such that the
    exactly-counted set
        U = { sum_i a_i b^i : a_i in A, sum a_i <= T }
    satisfies
        1 + log(|U-U| / |U+U|) / log(2*max(U)+1)  >  1.1752717416788478.
    By the GHR2007 single-set lemma this is a valid lower bound on C_3a, strictly beating the
    R3 verified held bound 1.1752717416788478 (alphabet-search-dp, d=96, T=184, M=10, base 21).

WHY THIS EXISTS (a finite question NOBODY has swept):
    Every prior search on this constant FIXED the max digit at M=10 (base 21) and only varied
    the SMALL-digit shape of {0..10} (the explorer's R2 finding: {0,2..10} won all 8 omission
    variants at d=40, but ALL of those variants kept M=10 / base 21).  The max digit M sets
    BOTH the carry-free base b=2M+1 (the log-q denominator) AND the achievable diff/sum count
    spread (the numerator).  Raising M widens the per-digit alphabet (more |U-U| relative to
    |U+U| spread, helping the numerator) but ALSO raises the log-q denominator log(2M+1) --
    a genuine trade-off that has never been measured.  Lowering M (e.g. M=9, base 19; M=8,
    base 17) shrinks the denominator but also the spread.  The asymptotic rate-function line
    (zheng-nonuniform-ratefn) is the PRINCIPLED way to predict the optimal M; THIS sketch is
    the direct, cheap, exact-DP way to ASK THE FINITE QUESTION NOW: does any M != 10 beat
    M=10 at a re-tuned (d, T)?  If a different base wins even at a moderate d, it lifts the
    whole alphabet-search-dp lever onto a better base.

STRATEGY:
    The alphabet family is A_M = {0, 2, 3, ..., M} (drop digit 1, the proven-good shape; keep
    0 for the GHR lemma).  Sweep M over a small window around 10 (e.g. M in {8, 9, 10, 11, 12})
    at a MODERATE comparison d (d0 ~ 48-64) where each exact-DP point is cheap, scanning a
    T-grid at the re-tuned ratio c ~ 1.90-1.95 for each M.  Compute the EXACT theta via the
    same validated engine (ghr_dp.py: sumset_bitmask + diffset_fast + max_U).  This is a
    RELATIVE comparison at fixed d0 -- it does NOT itself certify a record (d0 is too small).
    The decisive output is the RANKING of M at d0: if some M* != 10 strictly out-ranks M=10 at
    d0, lift M* to the full d (the alphabet-search-dp d>=96 machinery, same engine) and
    exact-DP-certify theta > HELD with the directed-rounded rational log bound
    (lemmas/log_bounds.py).  If M=10 wins the d0 sweep, this sketch closes as a verified
    NEGATIVE (the base-21 choice is optimal among nearby bases) -- a real, reusable result
    that retires the "maybe a different base helps" question and concentrates compute on
    Lever A's d-pushing.

NOTE on the carry-free constraint (must hold for the GHR lemma to apply):
    b = 2*max(A)+1 = 2M+1 guarantees digit-wise sums in [0, 2M] and diffs in [-M, M] stay in
    (-b, b), so the base-b encoding is injective on U+U and U-U (no carries).  This is BUILT
    IN by construction for every M (the engine's carry_free_base(A) returns exactly 2M+1).
    The GHR technical constraint |U-U| <= 2*max(U)+1 must be re-checked per winner (it held
    with huge slack for M=10; expected to hold for nearby M, but the builder MUST verify).

HOLES:
  (H1) MAX-DIGIT SWEEP -- OPEN.  sweep_maxdigit(d0, M_window, c_grid) runs the exact-DP at a
       moderate d0 for each M in the window across a T-grid, returns the per-M best theta and
       the ranking.  Cheap (d0 small).  Decides whether any M != 10 out-ranks M=10.
  (H2) LIFT WINNER -- OPEN (only if H1 finds M* != 10 winning).  Re-run the winning M* at the
       full d (>=96, re-tuned c) via the alphabet-search-dp engine; cache exact counts; re-check
       the GHR constraint |U-U| <= 2max(U)+1 and 0 in U.
  (H3) CERTIFY -- OPEN (reuses lemmas/log_bounds.py, the certified directed-rounded rational
       log bound).  Certify theta_lb > HELD = 1.1752717416788478 for the lifted winner.
       If H1 instead confirms M=10 optimal, this sketch closes NEGATIVE (no certification, a
       documented dead lever) -- still a valid round outcome.

HARD STEP:
  H1's ranking at d0 must be MONOTONE-PREDICTIVE of the ranking at full d -- i.e. the M that
  wins at d0 must still win at d>=96 (the same assumption block-taper-probe validated for its
  schedules: ranking order at d=40 survived to d=48).  The base/denominator trade-off is
  d-independent (log(2M+1) does not depend on d) and the count spread ratio converges with d,
  so the d0 ranking SHOULD lift -- but this is the load-bearing assumption the builder must
  spot-check (re-run the top-2 M at a second, larger d0' and confirm the order is stable)
  before paying for the full-d lift.

CERTIFY:
  Numerical: exact-integer DP (ghr_dp.py) + directed-rounded rational log bound
  (lemmas/log_bounds.py).  Same certification shape as alphabet-search-dp -- Lean-fittable
  (feeds the ghr-lemma-lean line if a new base wins).

Running this file now: validates the engine against Griego's record, then STOPS at the H1
max-digit-sweep hole with a clear [hole] message (the sweep itself is the builder's job; even
a moderate d0 sweep over 5 values of M is minutes, not seconds, so it is NOT run in __main__).
"""

import os
import sys
from math import log

sys.path.insert(0, os.path.dirname(__file__))
from ghr_dp import sumset_bitmask, diffset_fast, max_U, carry_free_base

RECORD = 1.1740744
HELD = 1.1752717416788478          # R3 verified value to beat (alphabet-search-dp d=96,T=184,M=10)

# Griego record literals (engine validation anchor)
_GRIEGO_A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
_GRIEGO_THETA = 1.17407444769352116


def alphabet_for_max(M):
    """The family A_M = {0, 2, 3, ..., M}: drop digit 1 (proven-good shape), keep 0, max = M.
    Carry-free base is b = 2M+1 (= carry_free_base(A_M))."""
    if M < 2:
        raise ValueError("M must be >= 2 to have a non-trivial alphabet")
    A = [0] + list(range(2, M + 1))
    assert carry_free_base(A) == 2 * M + 1
    return A


def theta_float(A, d, T):
    """Exact-integer counts -> float theta (RELATIVE comparison only; not a certified bound).
    Uses the validated fast engine.  The certified rational bound is applied later (H3) only
    to the lifted full-d winner, via lemmas/log_bounds.py."""
    s = sumset_bitmask(A, d, T)
    diff = diffset_fast(A, d, T)
    q = 2 * max_U(A, d, T) + 1
    return 1.0 + (log(diff) - log(s)) / log(q), s, diff, q


def validate_engine_record():
    """FULL engine sanity (SLOW ~155 s, NOT run in __main__): reproduce Griego's record theta
    to <1e-9 (the proof-outliner ALWAYS rule).  The builder runs this once before trusting H1."""
    th, _, _, _ = theta_float(_GRIEGO_A, 80, 150)
    ok = abs(th - _GRIEGO_THETA) < 1e-9
    print(f"[engine] Griego d=80,T=150 theta={th:.15f} vs {_GRIEGO_THETA} -> {'OK' if ok else 'MISMATCH'}",
          flush=True)
    return ok


def validate_engine_small():
    """FAST engine sanity (seconds): the small-d M=10 vs M=9 family difference is well-defined and
    the carry-free base is correct for each M.  Confirms the alphabet/base wiring builds green
    without the slow d=80 reproduction (per-role rule: __main__ must finish in seconds)."""
    for M in (8, 9, 10, 11):
        A = alphabet_for_max(M)
        assert A[0] == 0 and 1 not in A and max(A) == M
        assert carry_free_base(A) == 2 * M + 1
        th, s, diff, q = theta_float(A, 6, 9)  # tiny d -> instant
        assert diff >= s >= 1 and q >= 1
        print(f"[engine] M={M} base={2*M+1} d=6,T=9 theta={th:.6f} (s={s},diff={diff})", flush=True)
    return True


# ---------------------------------------------------------------------------
# H1 (OPEN): the max-digit / base sweep
# ---------------------------------------------------------------------------

def _T_grid(d0, c_grid):
    """T-grid for d0: round(c*d0) for each c, plus +-1 neighbours, deduped & sorted."""
    Ts = set()
    for c in c_grid:
        T0 = round(c * d0)
        Ts.update((T0 - 1, T0, T0 + 1))
    return sorted(t for t in Ts if t >= 1)


def sweep_maxdigit(d0=40, M_window=(8, 9, 10, 11, 12),
                   c_grid=(1.86, 1.88, 1.90, 1.92, 1.94, 1.96), verbose=True):
    """HOLE H1 (CLOSED, round 4): for each max digit M in M_window, run the exact-DP at moderate
    d0 over a T-grid (T = round(c*d0)+-1 for c in c_grid), record the best theta per M, and
    return the ranking best-first.  Decides whether any M != 10 out-ranks M=10 at d0.

    Exact-integer counts; the theta here is a FLOAT ratio used ONLY for the relative ranking
    (d0 is too small to certify a record).  The certified rational bound (H3) is applied later
    only to a lifted full-d winner.  Each (d0, T) point is one sumset_bitmask call (the cost);
    at d0=40 each is ~5-9 s, so the whole sweep is a few minutes -- run as ONE background job
    with flush=True progress, never a silent >600 s foreground call.

    Returns (ranking, per_M) where
        ranking = sorted [(best_theta, M, best_T)] best-first,
        per_M   = {M: [(T, theta, s, diff, q), ...]} full per-point data.
    """
    per_M = {}
    best_per_M = []
    Ts = _T_grid(d0, c_grid)
    for M in M_window:
        A = alphabet_for_max(M)
        rows = []
        for T in Ts:
            th, s, diff, q = theta_float(A, d0, T)
            rows.append((T, th, s, diff, q))
            if verbose:
                print(f"  [H1] M={M:2d} base={2*M+1:2d} d0={d0} T={T} (c={T/d0:.3f}) "
                      f"theta={th:.8f}", flush=True)
        per_M[M] = rows
        bT, bth, *_ = max(rows, key=lambda r: r[1])
        best_per_M.append((bth, M, bT))
        if verbose:
            print(f"  [H1] M={M:2d} base={2*M+1:2d} BEST theta={bth:.8f} at T={bT} "
                  f"(c={bT/d0:.3f})", flush=True)
    ranking = sorted(best_per_M, key=lambda t: -t[0])
    if verbose:
        print("  [H1] ranking best-first:", flush=True)
        for th, M, T in ranking:
            print(f"        M={M:2d} base={2*M+1:2d} theta={th:.8f} (T={T})", flush=True)
    return ranking, per_M


def lift_winner(M_star, d, c):
    """HOLE H2 (open, only if H1 finds M* != 10 winning): re-run the winning max digit M* at the
    full d (>=96) and re-tuned c, via the same engine; return exact counts and re-check the GHR
    constraint |U-U| <= 2*max(U)+1 and 0 in A.  If M_star == 10 this is exactly the existing
    alphabet-search-dp winner (no new lift needed)."""
    raise NotImplementedError("H2: full-d lift of the winning max digit not implemented")


def certify_lifted(s, diff, q):
    """HOLE H3 (open): certify theta_lb > HELD via the reviewer-certified directed-rounded
    rational log bound in lemmas/log_bounds.py (import logN_lb/logN_ub; theta_lb = 1 +
    (logN_lb(diff) - logN_ub(s)) / logN_ub(q), all exact Fractions).  Do NOT use the naive
    atanh series at z~1 (per-role NEVER rule).  Returns a Fraction <= true theta."""
    raise NotImplementedError("H3: certified rational log bound on the lifted winner not implemented")


if __name__ == "__main__":
    import sys as _sys
    # Default (no args): cheap wiring check only -- finishes in seconds (per-role rule).
    # `python maxdigit-base-sweep.py sweep [d0]`  runs the H1 max-digit sweep (minutes; run as
    #     a background job, flush=True progress).
    if len(_sys.argv) >= 2 and _sys.argv[1] == "sweep":
        d0 = int(_sys.argv[2]) if len(_sys.argv) >= 3 else 40
        print(f"=== H1 max-digit sweep at d0={d0} ===", flush=True)
        ranking, _ = sweep_maxdigit(d0=d0)
    else:
        validate_engine_small()
        print("[stub] run `python maxdigit-base-sweep.py sweep [d0]` for the H1 sweep "
              "(background job).", flush=True)
