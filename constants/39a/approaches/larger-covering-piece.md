# Sketch C — larger-covering-piece

**Goal:** push the upper bound to $H_3 \le 13$ (beat the verified Prymak $\le 14$).

**Round-1 builder status: the uniform line is REFUTED.** The crux hole C1 — a uniform
enlargement $W_p$ with $O_p \subseteq W_p \subseteq \operatorname{int}(K)$ for *every* admissible
$K$ — is **provably impossible**. C0 is closed; C1 is reshaped into the rigorous impossibility
theorem it actually proves (exact-rational, verified); the bound hole stays open with the exact
blocker. This sketch does **not** establish $H_3 \le 13$. The uniform approach C dead-ends and
needs the outliner to re-plan (the live escape is approach A's neighborhood special-case).

## Strategy (as originally planned)

Attack Remark 2.3 *uniformly in $p$*: find $O_p \subseteq W_p \subseteq \operatorname{int}(K)$
whose difference body $W_p - W_p$ contains some marked-pair difference for every admissible
$p$/$K$, so one translate covers two of the 14 marked points and the per-cell count drops to
$\le 13$ with the same Prymak LP machinery, one piece fewer.

## What closed this round

- **C0 (bookkeeping) — CLOSED.** Exact-rational $V_p(p)$ from $A_p$ (Prymak Sec. 2) and the 14
  marked points are implemented (`Vp_columns`, `marked_points`); at $p=(1/2,\dots,1/2)$ they are
  the 6 cube-face centres + 8 vertices, verified.

- **C1 (crux) — RESHAPED and CLOSED as an impossibility theorem.** The planned statement ("a
  uniform $W_p \supsetneq O_p$ inside every $K$") is **wrong/unprovable**; the *true* statement
  is its negation, which I prove with an exact-rational certificate
  (`uniform_enlargement_impossibility_certificate`):
  - **(F1)** At $p=(1/2,\dots,1/2)$, $O_p$ is the regular octahedron and $O_p-O_p$ is the
    $\ell_1$-ball of radius 1. All **91** marked pairs have $\ell_1$-distance **exactly 1**
    (min $=1$, 51 pairs realize it) — every marked-pair difference is on the **boundary** of
    $O_p-O_p$, never in its interior. So no translate of $\operatorname{int}(O_p)$ covers two
    marked points (Remark 2.3, reproduced exactly).
  - **(F2)** $K=O_p$ (the regular octahedron) is itself an **admissible body**: it touches each
    cube face at its centre (the prescribed contact) and the cube is a minimal-volume
    circumscribing parallelotope of the octahedron. Since $O_p\subseteq K$ for every admissible
    $K$ *and* $K=O_p$ is admissible, the guaranteed-inscribed set $\bigcap_{K\text{ adm}}K$ is
    **exactly $O_p$**.
  - **Theorem.** No $W$ with $O_p\subsetneq W\subseteq K$ for all admissible $K$ exists (it would
    lie in $\bigcap K = O_p$). Even allowing the open/closed subtlety: any $W\subseteq K=O_p$ has
    $W-W\subseteq O_p-O_p$, so $\operatorname{int}(W-W)\subseteq\operatorname{int}(O_p-O_p)$,
    which by (F1) contains none of the marked-pair differences. **No uniform larger piece exists.
    QED.**

- **C2 (mechanical)** is now a settled utility: the $\operatorname{int}(O_p-O_p)$ membership test
  is $\|d\|_1<1$, and it returns False on all 91 marked pairs at $p=1/2$ — confirming why 13 is
  unreachable on this line.

## Open hole (the blocker)

- **C-bound (was C3) — OPEN, BLOCKED.** The 13-piece uniform cover requires a piece strictly
  larger than $O_p$ guaranteed inside every $K$. C1 proves no such piece exists. So $H_3\le 13$
  is **not** established here. `per_cell_cover_le_13` stays `NotImplementedError`; the sketch
  still builds/runs (green).

## Spec concerns / verdict for the outliner

- The outliner's planned C1 statement ("uniform $W_p\subseteq\operatorname{int}(K)$ for all $K$")
  is **refuted** — it cannot be filled as written; this is a **RETHINK** for the *uniform* line,
  not a fillable hole. The mechanism the outline-reviewer flagged ("escape via a
  cube-vertex/face-point pair where $K$ has slack even as the octahedron") does **not** survive:
  at $K=O_p$ there is zero slack at the face midpoints **and** zero guaranteed slack anywhere
  beyond $O_p$, because $K$ can be exactly $O_p$.
- **The only escape that survives is non-uniform:** treat the neighborhood of $p=1/2$ as a
  special case. There $K=O_p$ (and nearby bodies) is centrally symmetric / near-symmetric, hence
  coverable by 8 translates of its interior ($H^s_3=8$) — far below 13 — so the *worst body* is
  not actually hard; only the *reduction's sub-problem* $C(E\cup V_p,\operatorname{int}(O_p))$ is.
  That is precisely **approach A** (special-case-p-half) and **approach E** (octahedral-direct).
  Recommend the outliner retire the uniform framing of C and fold its certified impossibility
  result into A/E as the rigorous justification for *why* the neighborhood must be handled
  separately.

## Reproducible check

`python3 constants/39a/certificate/larger-covering-piece.py` — exact rational (`fractions`),
no floats; prints the impossibility certificate and asserts (F1), the boundary count (91 pairs,
min $\ell_1=1$), $K=O_p$ admissibility (contacts = face centres), and that no marked pair is
coverable. Lean-portable (finite, rational, discrete).

## Lean fit
The impossibility theorem is finite/rational/discrete — fully Lean-fit if anyone wants to certify
the *negative* result. It does not yield a bound improvement.

## Promotable lemmas
None this round. The impossibility certificate is sketch-specific (it refutes this line, it is
not a reusable positive lemma other sketches import). The exact $V_p(p)$ parametrization (C0)
could be promoted later if A/E reuse it, but it is bookkeeping, not yet a certified cache lemma.
