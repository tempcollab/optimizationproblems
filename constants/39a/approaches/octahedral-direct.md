# Sketch E — octahedral-direct

**Goal:** push the upper bound to $H_3 \le 13$ (beat the verified Prymak $\le 14$).

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

## Holes

- **E0 (mechanical):** 8 explicit illumination directions for the octahedron (demonstrates the loss).
- **E1 (crux 1):** characterize $\mathcal F$ — show forcing $p\approx 1/2$ implies $K$ near-symmetric.
  Continuum, partly Lean-hostile.
- **E2 (crux 2):** the $\le 13$ direct cover for all $K\in\mathcal F$. If reduced to a finite rational
  cover of a parametrized family, partly Lean-fit; the asymmetry handling may be continuum.
- **E3:** the 13-piece generic cover (shared with sketch A's regime R1).

## Why this is conceptually the cleanest
It attacks the genuine extremal body on its own terms rather than fighting the reduction's
artifact. Risk: characterizing $\mathcal F$ and proving a uniform $\le 13$ cover over a continuum
family is analytically heavy; the "controlled asymmetry" must be quantified. Borrows the generic
regime from sketch A.

## Lean fit
Mixed/Lean-hostile in E1–E2 (continuum family). Certify numerically; a finite rational
sub-cover of $\mathcal F$ would be Lean-fit.
