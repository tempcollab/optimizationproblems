# R2 — Restricted firing-optimality of the bridge exponent a

Status: BUILT (round 2). Certificate PASSES; awaiting proof-reviewer verification.

## BUILD STATUS (round 2, this build)
Angle 1 (certified consecutive-difference enclosures D_a < 0) implemented in
`constants/82a/certificate/firstvar_09_restricted_optimality.py`. PASSES at N=40000
(~248s total). All three outline-reviewer must-implements done:
- M1 (asymmetric signed-integral upper accumulation): certainly-IN cell banks w*int_hi
  (negative help allowed); STRADDLE cell banks w*max(0,int_hi) (positive only). The
  symmetric |.| bound is NOT reused.
- M2 (per-cell enclosure = directed-rounded difference of half-logs): via vv.rsub on
  [lRb_lo - lRa_hi, lRb_hi - lRa_lo], outward on the subtraction.
- M3 (m_R > 0 for a=1..4, plus a=5): inf_{Omega_F}|R_a| certified > 0 for every a in
  the chain (a=1..5), 0 unresolved well cells.

Certified outward-rounded UPPER bounds (N=40000):
  D_1^hi = -2.06e-3, D_2^hi = -1.52e-3, D_3^hi = -8.54e-4, D_4^hi = -3.12e-4 (all < 0).
  (True float D_a = -6.85, -5.28, -3.68, -1.82 in 1e-3; D_hi over-estimates, safe.)
The tight pair D_4 clears 0 with margin +3.12e-4. WELL_TOL=2e-5, MAX_DEPTH=44, well
refinement reached depth 6 with frontier=0. m_R_a >= 7.4e-9..4.7e-6 for a=1..5.
Chain: D_a<0 (a=1..4) => r_R_1 > ... > r_R_5 => |r| maximised at a=5 = R0.

Paper: new Prop prop:restricted-opt + Rem rem:a6 (a=6 caveat, deg-27) + eq:diff-id
under sec:generator; r_{R_a} margin column added to tab:degfloor; firstvar_09 row added
to the verification table tab:verify. a=6 caveat is a prose Remark ONLY, never a
certified D_5 pair.

Reproduce: cd constants/82a/certificate; python3 firstvar_09_restricted_optimality.py 40000

## Outline (original, round 2)

## Goal (theory deepening, no numeric bound)
Add PREDICTIVE content past `rem:gen-scope`: prove that among the **degree-preserving**
(deg R_a = 28) admissible siblings R_a = pp(Q1 - g_a), g_a = P1^a P2^a P4 . P8,
a ∈ {1,...,5}, the firing margin r_{R_a}(Ω_F) is STRICTLY DECREASING in a, so firing
strength is MAXIMISED at the degree boundary a = 5 = Grinsztajn's R0. State the caveat
that the unconstrained optimum is a = 6 but it has deg R_6 = 27 (breaks degree
preservation / the shared-normalizer transfer identity).

Held bounds stay frozen (upper 0.2538893183, lower 0.2524001332), Status none.

## LANDMINE
"a=5 firing-optimal" UNQUALIFIED is FALSE: a=6 fires harder
(r_{R_6} = -0.03591 < r_{R_5} = -0.03560). The theorem MUST carry the
degree-preservation restriction explicitly.

## Numerics established this round (float probe, /tmp/probe_margin_vs_a.py + ad-hoc)
- r_{R_a} (pp, anchor Ω_F = record\{Q1}, N=2e6) decreasing on a=1..5:
  -0.01796, -0.02481, -0.03010, -0.03378, -0.03560.
- Smallest gap r_{R_4} - r_{R_5} = +0.00182 (load-bearing).
- Difference D_a := r_{R_{a+1}} - r_{R_a} = (1/28)∫_{Ω_F} log|R_{a+1}/R_a| ds is
  -0.00685, -0.00528, -0.00368, -0.00182 for a=1..4 — all strictly < 0.
- Active-set boundary uncertainty CANCELS in the difference (~5e-7 in the
  |B_F-A_F|<0.01 band vs 1.8e-3 gap) — this is why the difference line is safe.
- Naive analytic subordination is FALSE: g_{a+1}/g_a = P1·P2 = X(1-X) = χ, and
  |χ| > 1 on ~10.7% of Ω_F. No pointwise inequality; monotonicity is integrated.

## Recommended line (Angle 1): certified consecutive-DIFFERENCE enclosures D_a < 0
Reuse prop:degfloor (degree/admissibility a=1..5, exact) + lem:transfer (the difference
identity is eq:transfer-id with Q*:=R_a). NEW: a `certify_diff(a)` in firstvar_08 that
returns a rigorous outward-rounded UPPER bound on the SIGNED integral
(1/28)∫_{Ω_F} log|R_{a+1}/R_a| ds for a=1..4 and asserts it is < 0. Per-cell integrand
bound [lR1_lo - LR_a_hi, LR1_hi - lR_a_lo]; adaptive well bisection on the ~84k shared
near-root cells (the same harness firstvar_08 runs). Chain the 4 sign certs to the
ordering; add the r_{R_a} margin column to Table tab:degfloor + a monotonicity
Proposition under sec:generator with the a=6 caveat.

Hard step: certify D_4 = (1/28)∫_{Ω_F} log|R_5/R_4| < 0 (true value -1.8e-3; integrand
sign-changing). Mechanism: adaptive bisection kills the per-cell well looseness; the
ratio R_5/R_4 has milder wells than R/Q1 (already cleared in R1).

## Alternatives (see /tmp/round-2/proof-outliner.md for full skeletons)
- Angle 2: per-a two-sided margin enclosures [lo_a,hi_a], ordered by non-overlap. More
  fragile (half-width budget 9.1e-4; boundary straddle does NOT cancel). Fallback only.
- Angle 3: hybrid — difference for tight pairs (a=3→4, 4→5) + cheap margins for wide
  pairs + the certified table column as a standalone artifact. Use if D_4 is borderline.
- Pure analytic subordination: REJECTED — load-bearing |χ|<1 on Ω_F is numerically false.

## Pointers
Full ranked outline: /tmp/round-2/proof-outliner.md
Cert to extend: constants/82a/certificate/firstvar_08_sibling_generator.py
Paper anchor: sec:generator, prop:degfloor, tab:degfloor, lem:transfer, eq:transfer-id.
