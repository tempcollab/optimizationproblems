# Check record — block-taper-probe (constant 3a, lower bound)

**Claimed bound:** NONE. This sketch is an honest **NEGATIVE result** — the principled
inhomogeneous (block-structured) lever does NOT improve the bound. HELD 1.1744750903655619
[R2, alphabet-search-dp] is unchanged. The sketch is GREEN (all three holes H1/H2/H3 closed)
but it proves no new lower bound; it establishes that no schedule in the principled block family
beats the homogeneous family.

**Reproduce (full, ~2–3 min):**
```
cd constants/3a/certificate && python3 block-taper-probe.py
```

**Expected tail:**
```
[H2] best d=40 schedule: homog  theta=1.1684468940
[H2] d=48 homog=1.1702291088  top1_thin=1.1702095693  order_survives=True
[FINDING] homogeneous d=40 theta=1.1684468940 ; best INHOMOGENEOUS d=40 theta=1.1684298170 ; gap=+1.708e-05
[FINDING] NEGATIVE: no principled block schedule beats the homogeneous family. ...
[FINDING] block-taper-probe does NOT beat HELD=1.1744750903655619 -- this sketch leaves the bound unimproved (honest negative result, not a forced bound).
[H3] certify_theta_lb = 1.168446894030  (<= true theta 1.168446894030: True)
```

**What is established (load-bearing):**
- **H1** — a position-dependent exact-integer DP for `|U+U|`, `|U-U|`, `max(U)` over a per-position
  alphabet list with global carry-free base `b = 2·max(∪ A_i)+1`. Validated three ways: reproduces
  `ghr_dp` exactly when all positions share `A_REC`; matches an **independent brute-force
  enumerator** on genuinely inhomogeneous tiny cases; fast bitmask/2D-grid paths match the slow DP.
- **H2** — a cheap d=40 sensitivity probe ranking 8 principled block schedules. Every inhomogeneous
  schedule scores strictly below the homogeneous baseline; the ranking order survives the lift to
  d=48 (the cross-d validation). Since θ is monotone in d for a fixed shape, no schedule overtakes
  homogeneous at full d, so none clears HELD.
- **H3** — the certify path (`certify_theta_lb` from `lemmas/log_bounds.py`) is wired and shown to
  produce a directed-rounded rational `θ_lb ≤ true θ` on the ranked-best schedule (path validity at
  probe scale only — no record-scale lift, because nothing beats HELD).

**Mechanism of the negative result:** the denominator `log q = d·log(2·max(U)+1)` is fixed by the
GLOBAL max digit. Low-block enrichment leaves max(U) unchanged but grows `|U+U|` at least as fast as
`|U−U|` (ratio shrinks); high-block thinning can't lower the base while any low block still carries
the top digit (only loses elements); raising a high digit costs more in the denominator than it
gains. The homogeneous `{0,2..10}` is locally optimal even under block perturbation — confirming the
round-2 "alphabet near-saturated" wall now against the full block family, not just homogeneous edits.

**Verdict signal for the reviewer:** dead-end the inhomogeneous lever (RETHINK / mark exhausted), do
not re-dispatch this builder — there is no schedule to fill. Productive levers stay alphabet-search-dp
(longer d / re-tuned T/d) and the zheng rate-function ceiling.
