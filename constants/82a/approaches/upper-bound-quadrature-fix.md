# Approach: fixing the rigorous quadrature enclosure for the UPPER bound h(q)

Status: IMPLEMENTED (round 4, Angle 1) — builder-claimed, pending reviewer verification.
The objective, family, calibration and admissibility are all VERIFIED (R2/R3). The
broken integral enclosure in `certificate/verify_upper.py::certify()` (vacuous ~2.2)
has been REPLACED by `certify_maxAB()`, the un-split `G = max(A,B)` enclosure of
Angle 1. Both stages land with the SAME harness (M0=200000, rem_cap=1e-10, ~145s):

  STAGE A (re-cert): rigorous  log h(Doche q) <= 0.2544362773 < 0.25444.   [LANDS]
  STAGE B (BREAK):   rigorous  log h(q*)      <= 0.2543326887 < 0.25443677. [BREAK]

Both runs RESOLVE COMPLETELY (frontier=0, unresolved cells=0; ~628k/652k leaves), and
the rigorous outward-rounded enclosures match the float values to ~1e-7 — i.e. the
max(A,B) enclosure is essentially TIGHT, not merely "good enough". The Stage-B margin
below the record is 1.041e-4 (the record corresponds to integral 89.544; the q*
enclosure is 89.489). Selftest (mode `selftest`) passes 0/300 violations for both the
flat and midpoint cell bounds vs high-precision mpmath sampled integrals.

Reproduce: `python3 verify_upper.py selftest` (soundness), then
`python3 verify_upper.py stageA` and `python3 verify_upper.py stageB`.

Moves: UPPER bound. Two deliverables, ranked by softness:
- **STAGE A (banked milestone):** rigorously certify `log h(Doche's q) <= 0.25444`
  (Doche's q = (13.1,10.6,3.2,1.15,0.24); float value 0.25443616). No sub-record margin
  to clear — robust to a still-somewhat-loose enclosure.
- **STAGE B (record-break):** rigorously certify `log h(q*) < 0.25443677` at
  q* = (11.74,8.77,2.45,1.55,0.53) (float value 0.25433258). Needs the enclosure tight
  to ~1e-4, ~8x better than the (broken) current harness — but with the Angle-1 fix the
  *true* loss is only outward-rounding slack, well under 1e-4.

---

## Root-cause diagnosis (ran this round — confirms the fix)

The certify() integrand is the Jensen log-max `G(t) = max(A(t), B(t))` with
`A = Σ q_i log|P_i(w)|`, `B = log|Q1(w)| + log|Q2(w)|`, `w(t)=e^{it}-e^{2it}`. True
`∫_0^{2π} G dt = 89.489`, giving log h = 89.489/(2π·56) = 0.25433.

certify() instead writes `G = (1/2)log|Q1|^2 + (1/2)log|Q2|^2 + max(0, A - B)` and bounds
the two pieces SEPARATELY. Measured contributions at M0=3e5:
- `Σ width·(fQ1+fQ2)` (the `+log|Q|` midpoint part) = **89.178** — accurate.
- `Σ (h^3/24)·curvQ` (curvature remainder of `(1/2)log|Q1|^2`) = **+44.1** — spurious.
  `curvQ = |((1/2)log|Q|^2)''|` blows up like `1/|Q|^2 ~ 4e16` at the near-zero of Q1
  (min|Q1|~1.8e-7 at s=0.1045); the midpoint-rule remainder `h^3·curv` is O(1) per cell
  and accumulates to 44 over the cells flanking the near-zero. The midpoint rule simply
  fails on a `log|0|` singularity.
- The conservative log+ branch `int_cons = width·max(0, rr_hi)` then over-counts the
  `-log|Q|` spike (corner bound rr_hi ~ +log(1/1.8e-7) ≈ +15 per the spike cells), and
  refinement re-adds split children on top of the already-counted loose parent
  (108 -> 614 -> 777 across rounds). These are the remaining ~700 of slack.

**The integrand has NO singularity to handle.** Where Q1 is near zero the log+ is active
(ratio A-B = +2.65 > 0 there, confirmed), so the `-log|Q1|` inside max(0,·) CANCELS the
`+log|Q1|` in int_S: G = A = Σ q log|P|, smooth. The brokenness is entirely an artifact
of splitting `+log|Q|` from `-log|Q|`. The fix is to NOT split them.

---

## Angle 1 (TOP PICK — IMPLEMENTED): enclose `G = max(A, B)` directly, no `±log|Q|` split

Moves: upper bound. Stage A -> 0.25444; Stage B -> ~0.25434 (true value + slack).

IMPLEMENTED as `certify_maxAB()` / `cell_AB()` / `cell_int_maxAB()` in verify_upper.py.
Result above. The implementation uses THREE valid per-cell upper bounds and takes the
min: (FLAT) `width*max(A_hi,B_hi)`; (STRADDLE, O(h^2)) the midpoint value plus the
integrated Taylor deviation `max(A_slope,B_slope)*r^2 + (1/3)max(A_curv,B_curv)*r^3`,
valid via `max(a+x,b+y)<=max(a,b)+max(x,y)` for x,y>=0; (MIDPOINT, O(h^3)) the
midpoint rule on the single dominant smooth branch where one branch dominates the
whole cell and its curvature is tame. Cells whose straddle deviation exceeds rem_cap
are bisected; only leaf cells are summed (no parent double-count). The STRADDLE O(h^2)
bound was the load-bearing addition — the pure flat sup of the original skeleton was
~0.0020 too loose at M0=6e5 (would have needed M0~1e8 for Stage A); the O(h^2) bound
+ adaptive refinement converges to ~1e-7 slack in 6 refine rounds. What would push it
further: a tighter q from continuous optimization (the float optimum 0.25433258 is the
current floor on this Doc01b family); or a richer base-poly dictionary for a lower
limit point (a genuinely new construction, not just re-optimizing q).

Skeleton:
  1. Per cell [a,b], form verified enclosures `[A_lo, A_hi]` of `A(t)=Σ q_i log|P_i(w)|`
     and `[B_lo, B_hi]` of `B(t)=log|Q1(w)|+log|Q2(w)|`, using the EXISTING `rho_full`
     Taylor-model machinery (it already returns tight midpoint rho and a 2nd-order cell
     enclosure of `(1/2)log rho`'s value AND its `f''` curvature bound `fpp_hi`). For a
     factor: `(1/2)log|P|^2` value over the cell is enclosed by the midpoint-rule
     interval `[ f(m) - (h^2/8)fpp_hi - ... , f(m) + ... ]`; simpler and sufficient,
     use the monotone-Taylor cell enclosure `f(m) + f'(m)[-r,r] + (1/2)fpp_hi[−r²,r²]`
     (already the pattern in `U2_enclosure`/`rho_full`). — by reused Taylor model.
  2. Cell upper bound of G: `G_hi = max(A_hi, B_hi)`. Then
     `∫_cell G dt <= width · G_hi` (a flat per-cell sup; outward-rounded). — by sup bound.
     OPTIONAL tightening for Stage B: where the cell is entirely in one branch
     (`A_lo > B_hi` ⇒ G=A, or `B_lo > A_hi` ⇒ G=B), use the midpoint rule
     `width·f_up(m) + (h^3/24)·curv` on that single SMOOTH branch — but ONLY on cells
     where the active factor is bounded away from its zeros (so curv is finite/small).
     On cells straddling a P_i or Q_i zero, the active branch's curv blows up, so DON'T
     use the midpoint rule there — use the flat `width·G_hi` (which is finite because
     `max` caps the downward dip: at a Q1 zero, B_hi→−∞ but A_hi is finite, so
     `G_hi = A_hi` is finite). — by branch test.
  3. Sum over cells, divide by `2π·D`, D = max(Σ q_i deg P_i, 56). Adaptively refine any
     cell where `G_hi - (width-normalized lower est) ` is too wide (Stage B only;
     Stage A's flat sum already lands < 0.25444 — verify). — by outward-rounded sum.
  4. Cite Doc01a Lemmas 2-5 + the verified admissibility (deg Q=56>0, X,(1-X)∤Q,
     gcd(P_i,Q)=1): h(q) is a genuine limit point, so C_82 <= log h(q) for this
     admissible q. — by citation + existing `admiss` check.

Hard step: **showing `∫_cell G dt <= width·max(A_hi, B_hi)` is both VALID and TIGHT
enough.** Validity is immediate: `G(t) = max(A,B) <= max(sup A, sup B) <= max(A_hi,B_hi)`
pointwise. Tightness is the real question — a flat sup-per-cell bound is O(h) accurate
(error ~ width·(slope·width)/2 summed = O(1)·max|G'|·total-width). With M0=3e5 cells
(width 2e-5) and |G'| bounded (G is Lipschitz except at the integrable log-dips which
`max` removes from the UPPER side), the flat-sum overshoot is ~ (1/2)·mean|G'|·width per
cell. Mechanism it should hold: |G'| = |A'| or |B'| = |Σ q_i Re(P_i'/P_i · w')| which is
O(10²) on most of the contour but spikes to O(10⁶) only in O(width) neighborhoods of the
zeros (where `(log|P|)' ~ 1/(t−t0)`). The flat-sum error there is
`Σ width·width·|G'| ~ width·∫|G'| ~ width·O(log)` near each zero = O(1e-4) total — right
at the Stage-B margin. So Stage B likely needs the midpoint-rule tightening (step 2
optional branch) on the smooth bulk (98% of cells where one branch dominates and is far
from its zeros), keeping the flat bound only on the O(1e3) zero/kink cells. Stage A does
not — the flat sum at M0=3e5 should already give <= 0.25444 with margin.

Check the builder runs / reviewer reproduces:
- Stage A: `python3 verify_upper.py certify_dochesq` prints
  `Σ width·max(A_hi,B_hi)/(2π·56) <= L` with `L <= 0.254437 < 0.25444`, nbad=0.
- Stage B: same at q*, `L < 0.25443677`, plus the cross-check that the float harness
  (`float`) gives ~0.25433 at q* and ~0.254436 at Doche's q (sanity that the rigorous L
  is not far above the true value — if L lands near 2.2 the fix is incomplete).
- Reviewer re-derives the pointwise inequality `G <= max(A_hi,B_hi)` and re-runs the sum.

Why this is the top pick: it DELETES the two broken pieces (the divergent `+log|Q|`
curvature and the conservative `-log|Q|` corner branch) rather than patching them, by
returning to the un-split Jensen `max(A,B)` form. The `max` provably caps every downward
log-singularity, so no cell is ever vacuous. It reuses `rho_full` verbatim — minimal new
code, low risk. Stage A is near-certain; Stage B rides the same harness with the
optional midpoint tightening on smooth cells.

---

## Angle 2: keep the split, but fix int_S with an analytic log-singularity bound

Moves: upper bound, same targets. Keep certify()'s `int_S + int_logplus` structure but
repair the two leaks:
  - int_S leak (curvQ=+44): on cells where `|Q_i|^2` cell-enclosure `rho_lo <= τ`
    (τ ~ 1e-6), DO NOT use the midpoint+curvature rule. Instead bound
    `∫_cell (1/2)log|Q_i|^2 dt` analytically: `(1/2)log|Q_i|^2 <= (1/2)log(rho_hi)`
    (the cell-UP value), so `∫_cell <= width·(1/2)log(rho_hi)` — a flat sup, finite,
    no curvature. (Same flat-sup idea as Angle 1, applied only to int_S.)
  - int_logplus leak: replace `int_cons = width·max(0, rr_hi)` corner bound by refining
    until `rr_lo > 0` (force the smooth-positive branch) OR `rr_hi <= 0` (zero branch);
    and FIX the refinement double-count (add children's estimate, subtract the parent's
    — or only sum LEAF cells at the end, never accumulate parents).

Hard step: the refinement double-count fix and ensuring the flat int_S bound + the log+
flat bound don't EACH count the `±log|Q|` spike (they would: int_S adds `+log|Q|_hi`,
int_logplus's rr subtracts `-log|Q|_lo`; on a spike cell `+log|Q|_hi` is a large negative
(good) but `-log|Q|_lo` is a large positive (bad) — the cancellation only happens
pointwise, not bound-wise). This is exactly why the split is fragile — Angle 1 avoids it.
Mechanism: works, but the bound is looser than Angle 1 by the `log|Q|_hi - log|Q|_lo`
cell gap on spike cells. Adequate for Stage A, marginal for Stage B.

Check: same as Angle 1; additionally assert `partial_integral_hi` is monotone-bounded
across refine rounds (no double-count) by summing leaves only.

Why second: it patches the broken structure instead of removing it, carries the
split-cancellation fragility, and needs the refinement-bookkeeping fix on top. More
moving parts, looser. Use only if Angle 1's `rho_full`-based A/B enclosures surprise.

---

## Angle 3: smooth provable majorant of log+ + change of variables (heavier, fallback)

Moves: upper bound. Replace `max(0,x)` by a smooth majorant `μ_β(x) = (1/β)log(1+e^{βx})`
(softplus) with `μ_β >= max(0,x)` everywhere and `μ_β - max(0,x) <= (log 2)/β`, so
`∫ μ_β <= ∫ max(0,·) + 2π(log2)/β`. Pick β so `2π(log2)/(β·2π·56) < 1e-5`, i.e.
β > ~2500. Then enclose the SMOOTH `μ_β(A−B)` by a Taylor model (no kink). For the log
dips, change variable near each zero t0: with `A ~ q_i log|t−t0| + smooth`, split off
`∫ q_i log|t−t0| dt = q_i[(t−t0)(log|t−t0|−1)]` analytically on a small subinterval and
Taylor-enclose the smooth remainder.

Hard step: large β makes `μ_β` STIFF (its derivatives scale like β^k), so the Taylor-model
curvature `μ_β'' ~ β` forces tiny cells (`h ~ 1/β ~ 4e-4`) exactly at the kink — a lot of
cells, and the analytic-singularity splitting needs the local Puiseux/Laurent expansion of
A at each P_i zero, which is real work. Mechanism: valid (softplus majorant inequality is
elementary; analytic log-integral is exact), but the most engineering. Strictly dominated
by Angle 1 here because Angle 1's `max(A,B)` form has NO kink to smooth and NO singularity
to change variables for (max caps both). Keep only if both Angles 1 and 2 stall.

---

## Ranking

1. **Angle 1** first — by a wide margin. It removes both bugs at the source by reverting
   to the un-split `G = max(A,B)` Jensen form, where `max` provably caps every downward
   log-singularity (so no vacuous cell) and there is no separate divergent `+log|Q|`
   curvature term. It reuses `rho_full`/`verify_vec` machinery verbatim. Stage A
   (re-cert <= 0.25444) is near-certain at M0=3e5 with the flat per-cell sup; Stage B
   (<0.25443677) rides the same harness with the optional midpoint-rule tightening on the
   ~98% smooth bulk cells, since the true value 0.25433 sits 1e-4 under the record.
2. **Angle 2** if Angle 1's A/B enclosures need the existing split scaffolding — patches
   int_S (flat log-up bound on spike cells) and int_logplus (refinement bookkeeping +
   force smooth branch). Looser, more fragile (split cancellation), but reuses more of the
   current file.
3. **Angle 3** only as a last resort — a softplus majorant + analytic singularity
   splitting; valid but the stiffest and most engineering, and Angle 1 makes both of its
   devices unnecessary.

Bank Stage A regardless of whether Stage B's margin survives outward rounding.

## Spec review: SKIP recommended (low-risk, decisive diagnosis)
The root cause is pinpointed and reproduced (the +44 curvature term and the conservative
log+ branch), the fix is a well-understood reformulation (`max(A,B)`, no split) reusing
verified machinery, the pointwise inequality is elementary, and Stage A has no sub-record
margin to clear. This is a routine quadrature-rigor repair, not a novel/risky relaxation
claim. If the builder finds the flat-sum slack overshoots even Stage A at feasible M0
(unexpected), escalate to outline review before chasing Stage B.
