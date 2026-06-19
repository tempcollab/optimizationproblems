# Sketch E — octahedral-direct

**Goal:** push the upper bound to $H_3 \le 13$ (beat the verified Prymak $\le 14$).

## R3 revision — the rival enlargement line is GEOMETRICALLY DEAD, so this is the only $p\approx1/2$ route

This round established (exact, reproducible in `certificate/octahedral-direct.py`'s
`enlargement_is_dead_screen`) that the competing "enlarge the covering piece $W$" mechanism for the
$p=1/2$ neighborhood (sketch A's A1′, the `minvol-corner-slack` certificate) is not merely
Lean-hostile but **impossible**: $O_p-O_p$ is *exactly* the unit cube, every one of the 51 tight
marked-pair differences lies **on its boundary** (zero slack along every tight direction), and the
cube faces are min-vol-box contacts so $W\subseteq\operatorname{int}(K)\subseteq$ cube cannot widen
past them. Both the R2 edge-midpoint screen and the R3 corner-push screen returned **zero**
mergeable tight pairs at every margin up to $s=0.4$. So no admissible $W$ with the marked points
fixed drops $14\to13$ at $p=1/2$. **The $p\approx1/2$ half must abandon the cube-skeleton/marked-point
frame and cover the body $K$ directly via its near-symmetry (this sketch).** The enlargement line
(A1′ / `minvol-corner-slack`) should be retired.

## Strategy

Bypass the skeleton reduction at the bottleneck. The 14-ceiling at $p=1/2$ is an **artifact of
the reduction** — it demands the full cube skeleton $E$ be covered by translates of the small
octahedron $\operatorname{int}(O_p)$. But the body actually being bounded at $p=1/2$ is (an affine
image of) a **near-symmetric** body, and a centrally symmetric 3-D body has $H\le 8$ (Lassak
$H_3^s=8$). The stub confirms numerically that the octahedron itself is symmetric, hence $\le 8$,
far below 14 — direct evidence the reduction is lossy here.

- **E1:** characterize the family $\mathcal F$ of bodies whose Prymak normalization forces
  $p\approx(1/2,\dots,1/2)$ — octahedron-like, symmetric core plus controlled asymmetry.
- **E2:** for every $K\in\mathcal F$, an explicit cover by $\le 13$ translates of $\operatorname{int}(K)$:
  $\sim 6$–$8$ symmetric-core (Lassak-type) directions $+$ a bounded number of corrective translates
  for the asymmetry.
- **E3:** glue with the generic regime ($p$ away from $1/2$), where a 13-piece $\tau$ is feasible.

## R3 build outcome — E0 + E2-core CLOSED, E1 OPEN (reshaped, honest)

Reproduce: `python3 constants/39a/certificate/octahedral-direct.py` (runs clean, exit 0).

**Closed this round (exact / directed-rounded):**
- **E0** — explicit illuminating set $D=-V$ (6 directions) for the octahedron, by Boltyanski's
  active-facet criterion (vertex check suffices). **Exact** illumination margin $=1$ (unnormalized,
  $=1/\sqrt3$ unit). So $I(\text{octahedron})\le 6\le 13$, far below 14 — direct evidence the
  reduction is lossy at $p=1/2$.
- **E2-core / Lemma S' (reshaped from the original E2)** — an **exact, certifiable sufficient
  condition** for $D=-V$ to illuminate an arbitrary polytope $K$: *orthant-coherence* (at every
  vertex the active facet outer normals share a coordinate-sign). Then $d=-\varepsilon e_i$
  illuminates that vertex, so $I(K)\le 6\le 13$ with a verified margin. Sufficiency independently
  corroborated (1932 coherent bodies, 0 illumination failures on a full-boundary direct test).
  Explicit perturbation threshold located at $t\approx 0.30$ (all sampled bodies within stay
  6-covered).

**Reshaping note (intermediate-statement search):** the original E1/E2 planned statement
"$p\approx1/2 \Rightarrow K$ near-symmetric $\Rightarrow H(K)\le 13$" is **false as written** —
a body can touch all 6 cube face centers ($p=1/2$ contacts) and still be highly asymmetric,
bulging a facet normal into a cube-corner cone that breaks the cover (verified:
`counterexample_face_center_not_symmetric`). So I replaced the false symmetry intermediate with
the **true, provable** orthant-coherence criterion (E2-core) plus the honest open question
(E1) of whether the forced family meets it.

## Holes

- **E0 (mechanical):** CLOSED — explicit 6-direction illumination of the octahedron, exact margin.
- **E2-core (Lemma S'):** CLOSED — orthant-coherence $\Rightarrow I(K)\le 6\le 13$, exact + sweep.
- **E1 (LOAD-BEARING, OPEN):** the Prymak-forced family at $p\approx1/2$ satisfies
  orthant-coherence. The naive symmetry reading is **false** (counterexample); E1 needs the full
  min-volume-box geometry to bound the normal-fan deviation away from the corner cones.
  Continuum / Lean-hostile. **NOT established** — this is the genuine wall.
- **E3:** the 13-piece generic cover (shared with sketch A / generic-thirteen-lp) — out of scope
  for E; lives in the generic regime.

## Claimed bound (clearly a CLAIM until hole-free)
**No unconditional near-$1/2$ bound yet.** Verified sub-results: $I(\text{octahedron})\le 6$ and
orthant-coherence $\Rightarrow \le 6$. The conditional statement "orthant-coherent $K$ near
$p\approx1/2$ are 6-covered $\le 13$" holds; the unconditional $H_3\le 13$ for this regime does
**not** — E1 is open. Target hole-free: **no**. Table value to beat: $H_3\le 14$.

## What would push it further
Close E1: derive from the min-volume-box optimality conditions (six face-center contacts +
volume-balancing) a quantitative bound on how far $K$'s facet normals can tilt from the
octahedron normal fan, and show that bound keeps $K$ orthant-coherent (or, more weakly,
illuminable by $\le 13$ directions). If that reduces to a finite rational parametrized
sub-cover it becomes Lean-fit; otherwise it is a directed-rounded continuum certificate.

## Spec concerns
- **E1 is not merely Lean-hostile — it is genuinely unproved and the naive statement is false.**
  Face-center contacts do NOT force symmetry/orthant-coherence. The near-$1/2$ half is therefore
  NOT closed; the bounded-asymmetry correction does not yet yield $\le 13$ for the whole forced
  family. Stated honestly here rather than asserted.
- The whole sketch only ever produces $\le 6$ (well under 13) for the bodies it CAN handle — the
  slack to 13 is large, so once E1 closes the bound is comfortable. The risk is entirely in E1.

## Why this is conceptually the cleanest
It attacks the genuine extremal body on its own terms rather than fighting the reduction's
artifact. Risk: characterizing $\mathcal F$ and proving a uniform $\le 13$ cover over a continuum
family is analytically heavy; the "controlled asymmetry" must be quantified. Borrows the generic
regime from sketch A.

## Lean fit
Mixed/Lean-hostile in E1–E2 (continuum family). Certify numerically; a finite rational
sub-cover of $\mathcal F$ would be Lean-fit.
