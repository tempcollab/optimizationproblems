# Sketch — lassak-glue (NEW, R3)

**Goal:** push the upper bound to $H_3 \le 13$ (beat the verified Prymak $\le 14$), by stating the
final bound and exhibiting the **two-regime glue** nobody in the population had written yet.

## Why this sketch exists

The population had two halves of a 13-bound (generic LP in `GenericThirteenLP`, direct near-$1/2$
cover in `octahedral-direct`) but **no file that states $H_3\le13$ and assembles them**. Without the
assembly the two halves have no fixed interface and the reviewer has no single target. This sketch
is that assembly: it states `H3 ≤ 13` against the registry `H3` (from `CertifyFourteen`, no value
smuggled) and partitions Prymak's parameter space $[0,1]^6$ at an explicit rational margin $\delta$.

## The structural argument (why 13 is reachable)

Prymak: $H_3 \le \max_{p\in[0,1]^6} C(E\cup V_p, \operatorname{int}(O_p))$, with the 14-floor
attained **only at $p=(1/2,\dots,1/2)$** (Remark 2.3 / F0). R3 added the hard complementary fact:
**at $p=1/2$ the 14-floor cannot be beaten inside the $O_p$ frame at all** — $O_p-O_p$ is exactly
the unit cube, all 51 tight marked-pair differences are on its boundary (zero slack), and the cube
faces are min-vol-box contacts so no enlarged piece $W$ can widen past them (both the edge-midpoint
and corner-push enlargement screens returned zero mergeable pairs). So the only escape is to
**partition** $p$-space and bound the bottleneck point by a *different* mechanism:

- **Generic regime** ($p$ outside a rational $\delta$-ball $N(1/2)$): $C(E\cup V_p,\operatorname{int}(O_p))\le13$
  — finite rational LP / Farkas, supplied by `GenericThirteenLP` (hole `H_GEN`). Lean-fit.
- **Near-$1/2$ regime** ($p\in N(1/2)$): bound $H(K_p)\le13$ **directly** via Lassak-stability
  (the body is near-symmetric, $H_3^s=8$), supplied by `octahedral-direct` (holes E1/E2). Bounding
  $H(K)$ directly — not via the $O_p$ cover — is exactly what dodges the 14-floor. Lean-hostile.
- **Glue:** total partition ($\texttt{Near}:=\neg\,\texttt{Generic}$, tautological case split) +
  the cached covering primitives $\Rightarrow$ $\max$ over both regimes $\le13$ $\Rightarrow H_3\le13$.

## R3 builder — what was closed (sketch stays green)

The interface was tightened and the **final glue + case-split assembly is now CLOSED** (no sorry of
its own); the load-bearing content lives in three named holes pointing at the sibling sketches.

- **`H3_le_13 : H3 ≤ 13` — final step CLOSED.** Restructured so the top-level theorem is literally
  `Nat.sInf_le every_body_cover_13`. Because the registry def is
  `H3 = sInf {N | ∀ K, IsConvexBody3 K → IsCoveredBy N K (interior K)}`, the statement
  `every_body_cover_13 : ∀ K, IsConvexBody3 K → IsCoveredBy 13 K (interior K)` is *exactly* the
  membership of `13` in that set, so `Nat.sInf_le` discharges `H3 ≤ 13` with no sorry, correct
  strict direction (13 < 14), against the genuine R1 registry `H3` — no bound smuggled. (Verified:
  build green; `#print axioms H3_le_13` shows only `[propext, sorryAx, Classical.choice, Quot.sound]`,
  no custom axiom; `sorryAx` flows only through the three real holes + imported placeholders.)
- **`per_param_cover_13` — GLUE CLOSED.** The two-regime case split (`generic_or_near`, total by
  `Near := ¬ Generic`, `em`) routes each `p` to `generic_branch_cover` or `near_cover_le_13`. No
  anonymous sorry: each branch is a *named* interface hole. (Previously the generic branch was a
  bare `sorry` inside `H3_le_13`; now it is the named hole `generic_branch_cover`.)
- **`every_body_cover_13` — reduced to `per_param_cover_13` via `prymak_param`.** The
  arbitrary-body cover follows from the per-parameter cover through the Prymak parameterization;
  the only sorry on this path is `prymak_param` (H_RED).
- **Statement tightening (intermediate-statement search).** The old `reduction_to_per_p` was stated
  against `Body` covering and was effectively vacuous (it consumed a per-`p` Body cover and produced
  `H3 ≤ 13` with a single opaque sorry). It is replaced by the *true, provable* decomposition:
  `prymak_param` (body→param, the real Prymak Lemma 2.2 content) + the `Nat.sInf_le` step (closed).
  This makes H_RED an honest existence statement instead of a black-box reduction.

## Remaining holes (explicit `sorry` — nothing rests silently on them)

- **`Body p` (placeholder def)** — opaque normalized-body family; instantiated with H_RED.
- **H_RED — `prymak_param`** — Prymak Lemma 2.2 affine-normalization: every 3-D convex body is
  covering-equivalent to some `Body p`, `p ∈ [0,1]^6`. Shared infra (= CertifyFourteen D1/D2/D5).
  *Blocker:* the affine normalization + open→closed discretization are the heavy Prymak
  formalization; parked, shared with `certify-fourteen`'s D-holes.
- **H_GENERIC — `generic_branch_cover`** — transports the `E∪V_p`-by-`int(O_p)` LP cover
  (`generic_cover_le_13'`, imported verbatim from `GenericThirteenLP`) to a `Body p`-by-`int(Body p)`
  cover. *Blocker:* needs the affine identification `CoverTarget/Piece ↔ Body/int Body` (part of the
  same normalization as H_RED) **and** GenericThirteenLP's own open holes `H_GEN_*`.
- **H_NEAR — `near_cover_le_13`** — direct Lassak-stability cover of `Body p` for `p ∈ N(1/2)`.
  *Blocker:* this is `octahedral-direct`'s continuum hole (E1/E2); Lean-hostile, awaits a numerical
  certificate / a finite rational perturbed-direction sub-cover.

## Borrows

- `GenericThirteenLP` (its generic-regime 13-cover, imported as `H_GENERIC`).
- `octahedral-direct` (its direct Lassak-stability near-$1/2$ cover, as `H_NEAR`).
- `CertifyFourteen` lemmas (`IsCoveredBy.union`, `.mono_left`, `coveringNumber_mono_left`) + the
  registry `H3` def — the glue is assembled from these.

## Lean fit

The **assembly / partition / glue is Lean-fit** (finite case split + cached primitives, against the
genuine `H3` registry def). The two regime-bounds are holes: generic Lean-fit, near-$1/2$ Lean-hostile.
The value of this sketch is making the interface between the halves explicit and giving the run one
stated target `H3_le_13`.

## What would push it

- Close `H_NEAR` via `octahedral-direct`'s Lassak-stability bound (the genuine continuum hole).
- Close `H_GENERIC` via `GenericThirteenLP`'s `H_GEN_τ` (the rational LP at an off-center box) plus
  the affine transport.
- `H_RED` is the heavy Prymak formalization (shared with `certify-fourteen`'s D-holes); the glue can
  stand on a numerical reduction certificate while the Lean H_RED is parked.

## Value claimed (this is a CLAIM until hole-free — not a verified fact)

- Table value to beat: **H_3 ≤ 14** (Prymak 2023, verified).
- Claimed (unverified) target of this sketch: **H_3 ≤ 13**, upper bound. **Hole-free: NO** — three
  load-bearing holes remain (`prymak_param`/H_RED, `generic_branch_cover`/H_GENERIC,
  `near_cover_le_13`/H_NEAR). The sketch builds green and states the genuine target with the
  correct direction, but it does NOT yet establish the bound. Beats table only once hole-free.

## Promotable lemmas

None this round. The two closed glue theorems (`per_param_cover_13`, `H3_le_13`) are sketch glue
specific to `Body`/`Generic`/`Near` placeholders (and inherit `sorryAx` through those imported
placeholder defs), so they are NOT axiom-clean and NOT reusable as cached lemmas — they are not
promotable. (`generic_or_near`, `H3_le_13` carry `sorryAx` from imports, so none clears the cache
bar.)
