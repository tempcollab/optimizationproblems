# block-taper-probe — principled inhomogeneous (block-structured) construction

**Direction:** lower bound on C_3a. **Value to beat:** HELD 1.1744750903655619 [R2, alphabet-search-dp].
**Borrows:** ghr_dp.py exact engine (homogeneous equivalence is the H1 gate); lemmas/log_bounds.py
(H3 certify); the leader's d=84,T=162 homogeneous winner as the baseline to beat.

## Strategy
Letting the alphabet vary by digit position is a strict superset of the homogeneous family, so a
block construction cannot do worse than the leader — but round-2 found NAIVE per-position tapers
backfire (space explodes, blind search loses). The fix: make the schedule **probe-driven**, not
blind. A cheap d=40 sensitivity probe (each point ~7–8 s) measures how float-θ responds to
enriching vs thinning the alphabet at LOW positions (cheap sums/diffs) vs HIGH positions (which
dominate max(U) = denominator log q). Only the top 1–2 ranked block schedules are scaled to full d
and exact-DP-certified. This opens the inhomogeneous lever (explorer Lever D) early but
principled — the round-2 caution was against *blind* tapers; the probe supplies the schedule that
caution said was missing (it does not strictly require Lever B's asymptotic to first land).

## Holes
- **H1 BLOCK ENGINE:** position-dependent sumset/diffset/max DP over a per-position alphabet list.
  Gate: all positions equal → reproduces ghr_dp exactly (+ tiny brute-force).
- **H2 PROBE + SEARCH (hard):** the d=40 sensitivity probe ranking a small candidate set; lift the
  top 1–2 to full d at the leader's T/d, one point at a time (flush=True; never a silent >600s
  call). Must clear HELD float-θ.
- **H3 CONFIRM + CERTIFY:** exact counts + `certify_theta_lb` from lemmas/log_bounds.py (NEVER the
  old per-position atanh primitive).

## Hard step
H2: the probe must correctly PREDICT the full-d winner from the cheap d=40 ranking. θ rises
monotonically with d for a FIXED shape (round-2 fact), so d=40 ranks fixed shapes correctly; the
open risk is whether that ranking survives ACROSS block schedules — validate by lifting the top-2
AND next-2 and confirming the order holds.

## Certify
Python exact integer DP + directed-rounded rational log bound (lemmas/log_bounds.py). Lean-fittable
on the winning counts (feeds ghr-lemma-lean if it wins).

## Risk / relation to round-2 rules
Round-2 NEVER flags *blind* per-position tapers; this is explicitly probe-ranked, so it is the
sanctioned way to attempt the lever. If the probe shows no block schedule clears HELD at d=40, this
sketch dead-ends cleanly (negative result: confirms the homogeneous family is locally optimal even
inhomogeneously) — that itself is useful information for Lever B's ceiling.

## Round 3 — built; all holes closed; NEGATIVE finding (does NOT beat HELD)

**Status: all three holes (H1, H2, H3) closed and green; `python block-taper-probe.py` exits 0.**
Claim: this sketch does **NOT** beat HELD 1.1744750903655619. It is an honest, principled negative
result — the inhomogeneous block lever does not help — not a forced bound. The held bound is
unchanged by this sketch.

### H1 — block exact-counting engine (CLOSED, validated)
Implemented `sumset_size_blocked` / `diffset_size_blocked` / `max_U_blocked` (per-position alphabet
list `Ai`, global carry-free base `b = 2·max(∪ A_i)+1`), plus fast `sumset_blocked_bitmask` /
`diffset_blocked_fast`. Validated three ways: (H1a) all-positions-`A_REC` reproduces `ghr_dp`
exactly at (8,15),(10,18); (H1b) an **independent brute-force enumerator** `_brute_counts` matches
the DP on genuinely inhomogeneous tiny cases (mixed per-position alphabets); (H1c) the fast paths
reproduce the slow validated DP at moderate d. The `max_U` greedy-from-top is optimal because the
global base `b` strictly exceeds every digit, so positional weight `b^i` dominates any combination
below it regardless of per-position alphabets.

### H2 — d=40 sensitivity probe (CLOSED) — the decisive negative signal
`probe_schedules(d=40, c=1.95)` ranks 8 principled schedules (homog; enrich-low +1 / full {0..10};
thin-high / top1-thin; raise-high +11; enrich-low+thin-high taper; shift 2→1 low). Each point ~7–9 s
on the fast engine. Result (best-first float-θ, T=78):

| schedule | θ (d=40) | base |
|---|---|---|
| **homog** (baseline) | **1.1684468940** | 21 |
| top1_thin | 1.1684298170 | 21 |
| high_thin | 1.1670118595 | 21 |
| high_raise11 | 1.1646901469 | 23 |
| low_enrich+1 / low_enrich_full | 1.1641373306 | 21 |
| low_enrich_high_thin | 1.1624293710 | 21 |
| low_shift21 | 1.1589577516 | 21 |

**Every inhomogeneous schedule is strictly below the homogeneous baseline** (closest is top1_thin,
gap +1.71e-5). Cross-d validation (the H2 hard step): lifted homog and the closest inhomog shape
(top1_thin) to d=48, T=94 — homog 1.1702291088 vs top1_thin 1.1702095693, **order survives**. Since
θ is monotone-increasing in d for a fixed shape (round-2 fact) and the ranked best shape is the
homogeneous one, no schedule in this principled family can overtake homogeneous at full d. So none
clears HELD.

### H3 — certify path (CLOSED, conditional)
`lift_and_certify` wires the exact blocked counts into `certify_theta_lb` (lemmas/log_bounds.py).
Demonstrated end-to-end on the ranked-best schedule at d=40: `certify_theta_lb = 1.168446894030`
(≤ true θ, confirmed). This is a path-validity check at probe scale, NOT a record-scale bound — and
since the probe's ranked best is homogeneous, the certify path would just re-derive the existing
homogeneous bound, not a new one. No inhomogeneous schedule is lifted to record-scale d because none
beats HELD even at the probe scale.

### Interpretation (why inhomogeneous backfires — mechanism, not just data)
The denominator is `log q = d·log(2·max(U)+1)`, set by the **global** max digit. Any low-block
enrichment leaves max(U) (hence the base) unchanged but adds correlated low-order digits that grow
|U+U| at least as fast as |U−U|, shrinking the ratio. Thinning a high block to lower max(U) requires
dropping the top digit *everywhere it appears as the global max* — but the low blocks still carry
digit 10, so the base stays 21 and thinning only loses elements (net θ drop). Raising a high digit
(→base 23) costs more in the denominator than it gains in the ratio. This is the same
"homogeneous {0,2..10} is near-saturated" wall round-2 found, now confirmed against the **full block
family**, not just homogeneous alphabet edits. Feeds Lever B's ceiling: the single-set family's slack
is in length+T/d (alphabet-search-dp), not in spatial inhomogeneity.

### What would push it further (for the outliner)
Nothing in *this* construction family — the negative result is robust (8 schedules, two d-scales,
mechanism understood). This is a `RETHINK`/dead-end signal for the inhomogeneous lever, NOT a
`CHANGES REQUESTED`: there is no schedule to fill in. The productive levers remain
alphabet-search-dp (longer d at re-tuned T/d) and the zheng rate-function ceiling. Recommend the
reviewer mark this sketch dead-ended (lever exhausted) rather than re-dispatch its builder.

## Promotable lemmas
None this round. (The blocked engine is sketch-specific glue validated for this sketch; it is not a
reusable certified lemma. No green bound was produced to cache.)
