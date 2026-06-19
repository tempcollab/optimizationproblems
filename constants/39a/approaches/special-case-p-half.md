# Sketch A — special-case-p-half

**Goal:** push the upper bound to $H_3 \le 13$ (beat the verified Prymak $\le 14$).
**Claimed bound this round:** still **14** (NOT improved). The 13-cover holes remain open.

## Strategy

Prymak's reduction: $H_3 \le \max_{p\in[0,1]^6} C(E\cup V_p,\operatorname{int}(O_p))$, with the
max attained only at $p=(1/2,\dots)$ (Remark 2.3), where $O_p$ is the regular octahedron
(face midpoints) and the 14 marked points (8 cube vertices + 6 midpoints) are mutually
$\ell_1$-uncoverable. Split $p$-space: generic $p$ → a 13-piece LP; a neighborhood of $1/2$ →
a larger admissible piece $W\supsetneq O_p$ drawing on the slack between $O_p$ and $K$.

## Closed this round (exact rational, reproducible)

Check: `python3 constants/39a/certificate/special-case-p-half.py` (prints PASS lines).

- **F0 — Remark 2.3, exact.** 0 of 14 marked points pairwise coverable at $p=1/2$; minimum
  pairwise $\ell_1$-distance is **exactly 1** = radius of $O_p-O_p$. The obstruction is tight,
  zero slack (confirms the reviewer's flag in exact arithmetic).
- **F1 — fragility.** The obstruction is supported on the *single point* $p=1/2$. Nudging one
  coordinate to $p_1=1/2+1/10$ already makes 14 pairs strictly coverable, 12 of them
  vertex/face-point pairs (e.g. $(0,0,0)+q_{30}$), with an exact interior certificate against
  the exact facets of $O_p-O_p$. So the count-reducing **merge** (one translate covers a
  vertex AND a face point) is available for every $p\neq 1/2$.
- **F2 — the worst-case framing corrected (key finding).** $K=O_p$ (the regular octahedron
  itself) does **not** normalize to $p=1/2$: it admits an enclosing parallelotope of volume
  **2** (explicit: a $\pm1$ matrix $R$ of $\det 4$, $\mathrm{vol}=8/|\det R|$), strictly below
  the cube's 8. So the cube is not its minimal-volume box. Hence a body *forced* to $p=1/2$ by
  the minimal-volume normalization is strictly larger than $O_p$ near the cube corners — there
  **is** slack between $O_p$ and any genuine $p=1/2$ body. (Also $K=O_p$ is centrally symmetric
  ⇒ $H\le 8$, so it never needs the special case anyway.) This means the reviewer's "$K$ can be
  exactly $O_p$ with zero slack" worst case is **not a body the reduction actually produces at
  $p=1/2$** — the enlargement leverage is not dead on arrival.
- **(doc) edge obstacle.** The naive single-merge 13-structure (8 vertex-translates + 5
  face-translates, one face merged onto a vertex) is **infeasible once the 12 edges must be
  covered** — the merged translate loses its edge-covering duty. So A2 needs a genuine $\tau'$
  redesign, not a free merge. (Float screen, documentary only, not load-bearing.)

## Holes that remain

- **A1′ (crux, OPEN).** F2 shows slack *exists*, but it is qualitative. A uniform, **rational**,
  finite enlargement $W$ with $O_p\subseteq W\subseteq\operatorname{int}(K)$ valid across *all*
  $p=1/2$-forced bodies needs a **quantitative lower bound on corner slack** derived from the
  minimal-volume-box condition. **Blocker:** the six contacts + "$C$ is the min-vol box" do not,
  by themselves, force quantifiable room near the cube corners (the corners carry no contact;
  $K$ can be thin there subject only to the min-vol balancing). This is a continuum/affine fact,
  Lean-hostile, and is exactly the leverage approach E (octahedral-direct) and approach B
  (circumscribed-frame) are set up to supply. **A1′ cannot close inside approach A's
  contact-only frame this round.**
- **A2 (OPEN).** A 13-piece structure $\tau'$ whose Prop-2.6 LP — vertices + 6 face rectangles
  **+ all 12 edges**, over $Q_P=\bigcap_{v}O_v$ — is feasible on a generic box. The naive merge
  is edge-infeasible (above); a correct $\tau'$ needs a combinatorial redesign plus a rational
  LP search, then an exact Farkas re-check. The merge mechanism itself is sound (F1).
- **A3 (OPEN).** Symmetry-reduced 13-feasible box atlas of $[0,1]^6$ minus a neighborhood of
  $1/2$; depends on A2.

## Spec concerns (strategy-level — for the outliner)

The sketch's R1/R2 split is sound in spirit, **but the R2 mechanism as written ("enlarge $O_p$
toward cube vertices using $O_p$-to-$K$ slack, uniformly over a neighborhood") is not closable
within approach A's contact-only frame.** Two-part reason, both established exactly this round:
1. The slack F2 guarantees is *qualitative*; making it a finite rational $W$ needs a quantitative
   corner-slack bound from the min-vol-box condition — a continuum fact A's machinery doesn't carry.
2. If one insists on a contact-only (uniform) $W$, the reviewer's zero-slack body $K=O_p$ would
   kill it — except F2 shows $K=O_p$ is *not* a $p=1/2$ body, so the obstruction isn't where the
   reviewer placed it; the real obstruction is the missing *quantitative* corner bound.

**Recommendation:** R2 should be handed to the outliner to either (a) fold A's R2 into approach E
(direct cover of the near-octahedral family, where the symmetry/min-vol slack is the natural
lever), or (b) re-plan R2 as a min-vol-box corner-slack lemma (approach B's territory). A's R1
(generic 13-piece LP, A2/A3) is genuinely Lean-fit and worth keeping as the generic-regime engine
once R2 is sourced elsewhere.

## What would push it

- A2: redesign $\tau'$ so the 6 face-translates retain enough edge-covering reach while one
  vertex/face merge drops the count to 13; verify the **edge-inclusive** rational LP at a
  concrete off-center $p$ (exact Farkas), then build the atlas A3. This is mechanical-but-real.
- A1′/R2: needs the quantitative corner-slack bound — most naturally pursued in E/B.

## Lean fit

R1 core (A2/A3) is finite rational LP / Farkas — Lean-fit, and shares the LP-in-Mathlib core
that sketch D (certify-fourteen) is building. R2/A1′ is continuum (corner-slack) — Lean-hostile.

## Promotable lemmas

None this round. (F0/F1/F2 are exact computational facts specific to this configuration, useful
as commentary but not yet packaged as reusable certified lemmas; F2's "octahedron min box < cube"
could become a small lemma if a sibling needs it, but no sketch imports it yet.)
