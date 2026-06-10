# Digest: Jones & Malavolta, "The Grothendieck Constant is Strictly Larger than Davie–Reeds' Bound" (arXiv:2603.30039)

**Result.** K_G^R ≥ K_DR + 10^{-12} (K_DR ≈ 1.67696, Davie–Reeds). Best current lower bound.
Concurrent Hei26 (arXiv:2603.22616) gets the weaker K_DR + 10^{-26}.

**Method.** Perturbative analysis of the Davie–Reeds operator. Davie–Reeds optimizer is a
"square wave" f=g on the line; they add a small cubic perturbation ε to a "Hermite
projection game" / 2-player XOR (Gaussian) game and show every optimizer is unstable, so
the integrality gap strictly increases. Mostly a continuous functional-analytic proof;
discretizes to a finite matrix only at the very end. The +10^{-12} is the provable margin
of the perturbation, NOT a numerical SDP value.

**Tractability for a computational run: POOR.** Both sides of 10a are analytic:
- Lower bound: continuous perturbation of an operator — improving the margin means a
  sharper perturbation analysis, not an SDP. Hard to make reviewer-reproducible quickly.
- Upper bound: BMMN2011 (arXiv:1103.6161) proved < Krivine's π/(2 ln(1+√2)) ≈ 1.782214 but
  with NO explicit numerical gap stated. So the *verified explicit numerical* upper bound is
  still essentially Krivine's 1.782214; beating it numerically would need a new rounding
  scheme analysis — possible but heavy, not a one-run SDP.

Avoid 10a as a computational target this run.
