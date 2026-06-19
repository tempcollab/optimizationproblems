# Digest: Arman, Bondarenko, Prymak 2024 — "On Hadwiger's covering problem in small dimensions" (arXiv 2404.00547, Canad. Math. Bull. 68(4):1239-1250, 2025)

PDF: `constants/39a/literature/pdfs/abp2024.pdf`; text `abp2024.txt`.

## Role for 39a
Survey + new bounds, but **does NOT improve $H_3$**. Best $H_3\le 14$ stays Prymak [25];
$H_4\le 96$ stays Prymak-Shepelska [26]. Their John-ellipsoid method only wins for $n\ge 5$.
So for $H_3$ this paper is context/equivalence/history, not a competing technique.

## Definitions / equivalence (the ledger cites this paper)
- $C(A,B)=\min\{N:\exists t_1,\dots,t_N,\ A\subset\bigcup(t_j+B)\}$.
- $H_n=\min\{C(K,\mathrm{int}(K)):K\in\mathcal K_n\}$ over all convex bodies; $H_n^s$ over
  centrally symmetric bodies.
- **Boltyanski equivalence:** $H_n$ = minimal # external light sources to illuminate the
  boundary of every convex body. Covering by smaller homothets (Gohberg-Markus) is the same.
- Cube forces $H_n\ge 2^n$; **Hadwiger conjecture $H_n=H_n^s=2^n$**, equality only for
  parallelepipeds. Known only for $n=2$ ($H_2=4$, Levi).

## History in dimension 3
$H_3\le 34$ (Lassak 1988) $\to 20$ (Lassak 1998) $\to 16$ (Papadoperakis 1999) $\to 14$
(Prymak 2023). **Symmetric: $H_3^s=8$ exact and sharp (Lassak 1984).** All the low-dim
general-body results "were based on comparing the body with a suitable parallelepiped."

## Their general machinery (the high-dim toolkit; n>=5 only)
- **Rogers-Zong covering inequality (6):** $C(K,L)\le \frac{|K|}{|L|}\,\theta(L)$ for
  $|K-L|=|K|$ (more precisely involves $|K-L|/|L|$), $\theta(L)$ = lattice covering density.
- **John position:** take $L$ = max-volume inscribed ellipsoid = unit ball $B_2^n$ after
  affine map; then $C(K,\mathrm{int}K)\le \frac{|K+B_2^n|}{|B_2^n|}\theta(B_2^n)$.
- Bound $|K+B_2^n|$ via **quermassintegrals** (Steiner formula) + Bonnesen-type inequality
  (Bokowski-Heil), and the extremal fact that mean width/volume in John position is maximal
  for the **regular simplex** (general) or **cube** (symmetric) — Ball, Barthe,
  Schechtman-Schmuckenschlager. Plug in best known lattice covering densities $\theta(B_2^n)$.
- New: $H_5\le 72$, $H_6\le 305$, $H_7\le 41377$? (table values: $H_5\le933,H_6\le6137,...$ —
  see Table 1; symmetric $H_4^s\le 23$ etc.). Mean-width-of-simplex estimates for $5\le n\le8$.

**Why it fails for n=3:** the John-ellipsoid bound $\frac{|K+B|}{|B|}\theta(B_2^3)$ with
$\theta(B_2^3)\approx 1.46$ and the regular-simplex extremal is larger than 14. The
parallelepiped/skeleton-LP route (Prymak) is strictly better in $n=3,4$.
