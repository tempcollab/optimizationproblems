# maxdigit-base-sweep — sweep the max digit / carry-free base (NEW, round 4)

**Direction:** lower bound on C_3a. **Value to beat (verified held, R3):** 1.1752717416788478
(alphabet-search-dp, d=96, T=184, A={0,2..10}, max digit M=10, base 21).
**Borrows:** the exact-DP engine (`ghr_dp.py`) and the certified rational log bound
(`lemmas/log_bounds.py`) — same certification shape as `alphabet-search-dp`.

## Why this is genuinely new
Every prior 3a search FIXED the max digit at M=10 (base 21). The R2 alphabet study varied only
the SMALL-digit shape of {0..10} (omissions), all at M=10. The max digit M is the one free
parameter nobody swept exactly, and it controls a real trade-off:
- raising M widens the carry-free base b = 2M+1, which RAISES the log-q denominator
  log(2M+1) (hurts theta), but also widens the per-digit alphabet and the |U-U|/|U+U| count
  spread (helps the numerator);
- lowering M shrinks the denominator but also the spread.
Whether the trade-off favours M=10, or a nearby M, has never been measured. The explorer flagged
this as the one finite question the d=40 brute proxy could not answer (it fixed M=10), and named
the rate-function line (`zheng-nonuniform-ratefn`) as the *principled* predictor of optimal M.
This sketch is the *direct, cheap, exact-DP* way to ask the same question NOW.

## Strategy
Family A_M = {0, 2, 3, ..., M} (drop digit 1 = proven-good shape, keep 0 for the GHR lemma).
Sweep M in a small window around 10 (e.g. {8,9,10,11,12}) at a moderate comparison d0 (~48–64)
where each exact-DP point is cheap, over a T-grid at the re-tuned ratio c~1.90–1.95 per M. The
decisive output is the RANKING of M at d0. If some M* != 10 strictly out-ranks M=10, lift M* to
full d (the alphabet-search-dp d>=96 machinery, same engine) and certify theta > HELD. If M=10
wins, this closes as a VERIFIED NEGATIVE (base 21 optimal among nearby bases) — a real reusable
result that retires the "different base" question and concentrates compute on Lever A.

## Holes
- **H1 MAX-DIGIT SWEEP (open):** `sweep_maxdigit(d0, M_window, c_grid)` — exact-DP at moderate
  d0 per M over a T-grid; return per-M best theta + ranking. Cheap. Decides M=10 vs M!=10.
- **H2 LIFT WINNER (open, only if M* != 10 wins):** re-run M* at full d (>=96, re-tuned c);
  cache exact counts; re-check GHR constraint |U-U| <= 2max(U)+1 and 0 in A.
- **H3 CERTIFY (open):** certified rational theta_lb > HELD via `lemmas/log_bounds.py`. If H1
  confirms M=10 optimal, close NEGATIVE (no certification, documented dead lever).

## Hard step
H1's d0-ranking must be MONOTONE-PREDICTIVE of the full-d ranking — the M that wins at d0 must
still win at d>=96. The base/denominator term log(2M+1) is d-independent and the count-spread
ratio converges with d, so the ranking SHOULD lift (same logic block-taper-probe validated: its
d=40 ranking survived to d=48). The builder must spot-check the top-2 M at a second d0' before
paying for the full-d lift.

## Relation to other sketches
- Complements `zheng-nonuniform-ratefn` (Lever B): that derives the asymptotic optimal M
  *principled-ly*; this measures it *directly* at finite d. Either confirms the other.
- If a new base wins, it lifts the whole `alphabet-search-dp` lever onto a better base and feeds
  a new `(A,d,T)` to the `ghr-lemma-lean` Lean line.
- Risk: M=10 may simply be optimal (the published record + all repo work chose it). Then the
  payoff is a clean negative, not a lift. Worth one moderate-d sweep to settle it.

## Certify
Numerical: exact-integer DP (`ghr_dp.py`) + directed-rounded rational log bound
(`lemmas/log_bounds.py`). Lean-fittable (feeds `ghr-lemma-lean` if a new base wins).
Sketch file: `constants/3a/certificate/maxdigit-base-sweep.py` (builds green; H1/H2/H3 are
NotImplementedError holes; engine validated against Griego's record via `validate_engine_record()`).
