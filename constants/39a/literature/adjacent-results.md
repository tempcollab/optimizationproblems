# Digest: Adjacent results & special classes for $H_3$

## Special-class illumination numbers in $\mathbb{R}^3$ (lower-bound landscape)
- **Cap bodies (all, 3-D): illumination number = 6** (arXiv 2507.08712, 2025; extends
  Ivanov-Strachan's centrally-symmetric cap-body result). Illuminating directions = vertices
  of a regular tetrahedron + 2 body-dependent directions. => cap bodies are NOT worst-case.
- **Spiky balls / cap bodies, Gallai-type problem** (arXiv 2408.01341, 2024) — illumination
  of cap bodies, related techniques. Not worst-case either.
- **Constant width bodies:** covering conjecture confirmed for $6\le n\le 15$ by spherical
  coverings / X-raying (Bondarenko-Prymak-Radchenko). Not the $n=3$ worst case.

**Takeaway:** every studied special 3-D class needs $\le 8$ (often $\le 6$). The only known
body forcing $8$ is the **parallelepiped** (and affine images). No published 3-D body is known
to require $>8$. Hadwiger conjectures none exists. So **the lower bound 8 is conjecturally
tight** — raising it would refute the Hadwiger conjecture in $\mathbb{R}^3$ (a major open
problem, not a target).

## Symmetric case (sharp anchor)
$H_3^s=8$ (Lassak 1984), sharp (cube). The symmetric problem in $\mathbb{R}^3$ is *solved*;
only the general (not-necessarily-symmetric) $H_3$ is open. The hard general bodies are
the **non-symmetric** ones (simplex-like / the $p=1/2$ configuration in Prymak).

## Asymptotic / high-dim (not directly usable for n=3, context only)
- Rogers-Shephard + Rogers covering density: $H_n\le \binom{2n}{n}n(\ln n+\ln\ln n+5)$.
- Huang-Slomka-Tkocz-Vritsiou: $H_n\le \exp(-c\sqrt n)4^n$ (thin-shell).
- Campos-van Hintum-Morris-Tiba: $H_n\le \exp(-cn/\ln^8 n)4^n$ (Bourgain slicing).
All are $(4+o(1))^n$-scale — useless near $n=3$.

## Lassak (n=3 lineage, the parallelepiped comparison)
Lassak 1988/1998 "covering a 3-D convex body by smaller homothetic copies": the original
"compare body to a suitable parallelepiped" idea Papadoperakis and Prymak refined. The
minimal-volume parallelotope normalization in Prymak descends from here.
