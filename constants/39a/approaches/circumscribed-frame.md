# Sketch B — circumscribed-frame

**Goal:** push the upper bound to $H_3 \le 13$ (beat the verified Prymak $\le 14$).

## Strategy

Prymak normalizes $K$ by its **minimal-volume circumscribed parallelotope** and maps it to the
cube. This forces the cube skeleton $E$ and admits the bad symmetric $p=(1/2,\dots,1/2)$
configuration that pins the count at 14. Change the normalization so that worst case is never
forced:

- **B1:** a different circumscribing **frame** — a parallelotope chosen to minimize the
  worst-case per-cell covering count (not volume), or a non-parallelotope frame adapted to $K$'s
  contact directions — for which the analogue of $\max_p C(E'\cup V',\operatorname{int}(O'))\le 13$.
- **B2:** alternatively a **two-frame case split**: cube-like bodies get frame $F_1$, others get
  Prymak's box; choose frames so each regime certifies $\le 13$.

The reduction lemmas (Prymak Lemma 2.1/2.2) must be re-derived for the new frame: it must contain
a contact configuration with $O'\subseteq K$, and covering $E'\cup V'$ with $\operatorname{int}(O')$-translates needs $\le 13$.

## Holes

- **B0 (bookkeeping):** the minimal-volume parallelotope baseline.
- **B1 (crux):** an alternative circumscribed frame existing for **every** convex body $K$, whose
  per-cell worst case is $\le 13$. The universality (frame exists for all $K$) is load-bearing and
  continuum.
- **B2:** the re-derived reduction lemma for the new frame (continuum/affine — likely Lean-hostile).
- **B3:** per-cell $\le 13$ over the new frame's parameter atlas (rational LP analogue).

## Risk
This is the highest-variance angle: replacing the normalization re-opens the whole reduction, and
the frame-existence (B1, B2) is a continuum optimization with no obvious rational core. If the new
frame still admits a symmetric worst case, no gain. Included for breadth and because the lossy step
is precisely the normalization — but it is Lean-hostile in its load-bearing part.

## Lean fit
Mixed, leaning Lean-hostile: B1/B2 are continuum (numerical certificate, adversarial
hand-rederivation); only B3 (per-cell LP) is rational/Lean-fit.
