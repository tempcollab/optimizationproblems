# R7 outline review — rigorous proof of the first-variation lemma (82a UPPER)

Reviewed: `/tmp/round-7/proof-outliner.md` Angle 1 (the build target is to be written
to `constants/82a/approaches/R7-firstvar-rigorous.md`, which does not yet exist).
Supporting numerics re-run: `constants/82a/certificate/verify_firstvar_lemma.py` and a
fresh contour/kink-set audit (below).

**Verdict: CHANGES REQUESTED.**

The TECHNIQUE is right and the lemma is TRUE and certifiable. The DCT-on-the-difference-
quotient route is the correct, self-contained way to handle the moving boundary, and the
load-bearing claim (Φ'(0)=r̃_Q) holds on the held family. But the outline states one
hypothesis (H1) that is **literally false for the held dictionary**, and states the
active-set geometry (H2) in a way that is **numerically wrong**. Both are fixable while
building, and neither voids the lemma — but if the builder copies them verbatim into the
written proof, the reviewer re-deriving (b) will hit a contradiction at the first
dictionary block and the milestone fails. Fix them in the statement, then the proof
closes. Specifics below.

---

## What is correct (verified, can be built)

1. **(H3) D-constancy / no-cross-term — TRUE and the easy half.** Recomputed on the R2
   anchor: arg_A = 61.546 < arg_B = 71.986, gap 10.44. arg_A is affine in q_Q with slope
   deg Q, so D ≡ arg_B is locally constant and dD/dq_Q = 0; the quotient cross-term
   vanishes. δ = (arg_B − arg_A)/deg Q is explicit (≈1.3 for deg 8). Step (a) discharges
   cleanly. The honest out-of-scope caveat (A-attains-D gives a −Φ·degQ/D² cross-term) is
   correctly flagged. Keep it.

2. **The DCT route is the right mechanism.** The difference quotient
   (G(s,q_Q)−G(s,0))/q_Q is 1-Lipschitz (max of functions is 1-Lipschitz in any added
   term), dominated by |log|Q∘χ||, with a.e. pointwise limit log|Q∘χ|·1_{A_0>B}. DCT then
   needs nothing about the boundary except measure-zero, which the kink-set finiteness
   supplies. This genuinely sidesteps the moving boundary — it is the correct, citation-
   free body, with Danskin/Bertsekas as a clean corroborating citation (not a dependency).
   No hidden obstruction in this route.

3. **The candidate block log|Q∘χ| IS L¹ (in fact bounded).** Audited min|Q∘χ| over the
   contour for all four test blocks: j3 4.07e-2, j9 1.06e-2, j6 8.21e-3, j7 1.56e-2 — none
   has a contour root, so log|Q∘χ| is bounded (|log|j9∘χ|| ≤ 6.88), hence trivially L¹.
   The domination hypothesis for the CANDIDATE is solid. This is the part (H1) needs to
   assert, and only this part.

4. **The kink set is finite.** Sign changes of A_0−B are STABLE at 64 across N = 5e5,
   2e6, 8e6 (active fraction 0.06854 stable to 5 digits). So K is finite (the active set
   is a union of ~32 intervals) and A_0−B is not identically zero (max +2.52, min −194).
   The measure-zero claim DCT needs holds.

5. **Numerics reproduce.** r̃(j9) = −0.00677 on the R2 anchor matches the R6 build
   exactly; sign predictions (fire/dry) and the finite-difference match are intact.

---

## Issue A (MUST FIX — the stated hypothesis is false): (H1) is wrong for A_0/B.

The outline's (H1) reads: *"Q is a fixed integer poly with NO root on the contour χ([0,1]);
together with every R in A_0, B having no root on χ([0,1])."* The second clause is **false
for the held dictionary**:

- The contour χ(s)=z(1−z) **passes through 0** at s=0 (z=1).
- **P1 = [1,0] = the monomial X**, with P1(0)=0. So P1∘χ has a genuine zero ON the contour
  at s=0, and A_0 contains a term q1·log|χ(s)| → −∞ as s→0.
- Audited min|R∘χ| confirms it: P1 0.0 (exact), and P2, P3, Q1, Q2 are 1e-6…1e-7 (their
  roots sit on/microscopically near the contour too). These are NOT contour-root-free.

So A_0 and B are **NOT bounded / not real-analytic on all of [0,1]** — they have integrable
log-singularities at the contour roots of the A/B blocks. The outline's clean "log|R∘χ| are
real-analytic and BOUNDED on [0,1]" is wrong as written.

**Why the lemma still holds (and how to restate H1 correctly):** the singularities are in
A_0 and B, *not in the candidate Q* (item 3). At every such singularity A_0 → −∞ (verified:
the cell of min A_0 = −213 is NOT in the active set), so those points sit deep in the
INACTIVE set {A_0<B} and never touch the kink K nor the active integrand. The correct
hypotheses are:

- **(H1′)** The CANDIDATE Q has no root on χ([0,1]) ⇒ log|Q∘χ| is bounded, hence L¹. (This
  is the only block that must be contour-root-free, because it is the one whose log enters
  the difference-quotient dominator.) — TRUE for j3/j6/j7/j9.
- **(H1″)** A_0 and B are real-analytic on [0,1] **off the finite set of contour roots of
  their constituent blocks**, where they have integrable −∞ log-singularities; A_0, B ∈
  L¹([0,1]) and A_0 → −∞ at each of its singularities, so a neighborhood of each lies in
  {A_0<B}. (This is what makes A_0−B real-analytic where it can vanish, so K stays finite.)

The builder must NOT write "no block has a contour root." Write (H1′)+(H1″). The reviewer
WILL check P1 and reject a proof that asserts A_0 is bounded.

## Issue B (MUST FIX — geometry misstated): the active arc is NOT [0, 0.8221].

The outline (H2) and the corollary repeatedly call the active set "{A_0>B} = [0, 0.8221]
⊊ [0,1]" — a single interval. In the harness s∈[0,1] convention this is **numerically
wrong**: the active set is a UNION OF ~32 INTERVALS (64 kink crossings), with total measure
0.0685, and it does NOT start at s=0 (s=0 is the deepest INACTIVE point, A_0=−∞ there). The
"[0, 0.8221]" figure is a stale R6 number in a different (s∈[0,π], normalized) convention and
must not be transplanted into the s∈[0,1] statement.

This does not affect the DCT proof (which never uses the interval structure — only that K is
finite). But:
- (H2) should say: "A_0−B is real-analytic off the singularities and ≢0; its zero set K is
  finite (64 points on the held R2 anchor at N up to 8e6), so {A_0>B} is a finite union of
  intervals of total measure ≈0.0685." Do NOT write "[0,0.8221]".
- The pushforward measure ν in the corollary is supported on this finite-union arc, not a
  single interval — restate accordingly.

## Issue C (CHECK while building — the "a.e. pointwise limit on the kink" line).

Step (b1) is correct but the builder must state the kink case precisely: ON K (A_0=B) the
difference quotient need not converge to log|Q∘χ|·1_{A_0>B}, but K has measure zero (Issue
A/B), so the a.e. limit is unaffected. The outline has this right; just ensure the written
proof says "for s ∉ K" and cites K finite (from H2′), not "for all s." Also: the one-sided
derivatives at a kink point differ (log|Q∘χ| vs 0) — this is exactly why the claim is a.e.,
not everywhere, and why DCT (not classical Leibniz) is the right tool. Make that explicit so
the reviewer sees the kink is handled, not ignored.

## Issue D (minor — D-constancy is at the q_Q=0 point, but state the window).

Step (a) is fine, but the proof should state δ explicitly and note D-constancy holds on the
whole window |q_Q|<δ (needed because the central finite-difference in the supporting check
uses ±eps; eps=1e-4 ≪ δ≈1.3, verified arg_A(±eps) stays below arg_B). The outline's
"dD/dq_Q=0 in a neighbourhood" is correct; just pin δ.

## Honest-scoping check — PASS (do not relax it)

The corollary's WITD framing is scoped correctly: it claims only that the SIGN of r̃_Q is a
weighted integer-Chebyshev condition on the active arc, and explicitly does NOT claim the
full inf_Q r̃_Q ≍ −log t_{Z,φ} equivalence (flagged future work), and does NOT claim "lower
locus = complement of upper arc." The upper-internal dual-loci framing is the defensible one.
Keep this guardrail verbatim; the reviewer will reject any drift toward the complement claim.

---

## Summary of required changes (all in the STATEMENT, the proof body is sound)

1. **Replace (H1)** with (H1′) candidate-Q-only contour-root-free + (H1″) A_0,B real-analytic
   off integrable log-singularities (P1=X vanishes at χ=0, contradicting the original H1).
2. **Replace the "[0,0.8221]" active arc** with "finite union of ~32 intervals, measure
   ≈0.0685, K = 64 points" in the s∈[0,1] convention; restate ν's support accordingly.
3. **State the kink case as a.e. (s∉K)** and pin K finite from real-analyticity, so the
   reviewer sees the measure-zero handling, not a hand-wave.
4. **Pin δ** in step (a) and note D-constancy holds on |q_Q|<δ (covers the ±eps check).
5. Keep the DCT body, the Danskin/Bertsekas citation-not-dependency framing, and the honest
   WITD scoping exactly as outlined.

None of these blocks the round — they are statement corrections that make the proof actually
re-derivable. With them, Angle 1 is a clean, certifiable milestone. Proceed to build after
fixing the hypotheses. Do NOT fall back to Angle 2 (no live A-dominant family) or Angle 4
(saturated). Stay on Angle 1.
