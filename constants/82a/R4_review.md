# R4 review — C_82a LOWER bound (Zhang-Zagier essential minimum)

## Verdict: APPROVE (verified-NEGATIVE + standing-memory CORRECTION, NOT a raise)
## Verification level: verified
## Milestone logged: YES (`- R4:` appended to constants/82a/current.md Progress log)

The R4 deliverable is explicitly NOT a bound raise. It is the R1-R3 milestone class:
a reproducible verified-NEGATIVE that *advances the frontier* by (i) overturning a
WRONG diagnosis the loop has carried in run_state since R3, and (ii) certifying the
only non-barred live tool inert. I verified it on exactly those terms. held stays
Flammang **0.2487458**; the table value remains **0.2487458** (no number moved, and
none was claimed to).

## What I independently reproduced (with numbers)

### Certificate runs (reproduced from scratch)
- `python3 gap_diagnostic.py selftest` -> cores [A]-[E] **ALL PASS**, exit 0.
- `python3 gap_diagnostic.py` -> full per-poly table + degree trend, writes JSON.
- circle-min of FULL Flammang aux f over |z|=1 = **0.2487462** (reproduces Flammang
  record 0.2487458, +4.4e-7).

### 1. Diagnosis correction — INDEPENDENTLY CONFIRMED
I recomputed the conjugate roots with a *fully independent* implementation
(`numpy.polynomial` composition of Q_j with w = z - z^2, distinct from the script's
manual `np.convolve` accumulation):
- **j=13 (deg_w 12):** 24 roots, mean dist to {|z|=1, |1-z|=1} = **0.0187**, max
  **0.0251**, mean sigma_ZZ = **0.2537**, |z| in **[0.527, 1.872]** — bit-matches the
  script row. Roots HUG the two circles; no far-lemniscate mass.
- **Large-|z| = the OTHER circle, confirmed:** j=24 largest-modulus root has |z|=**2.009**
  and |1-z|=**1.027** (dist to |1-z|=1 is 0.027). The [0.5,2] modulus spread is the
  second circle, not an off-circle lemniscate.
- **The 0.44 is the WITH-SELF artifact, confirmed:** at Q_5's own roots the self-term
  -c_5 log|Q_5(w)| diverges to +inf (numerically log|Q_5| -> large negative), inflating
  the with-self mean f to ~**0.43** (I reproduced 0.4336). j=5's roots lie ON the
  circles (mean dist 0.0) and its honest mean sigma_ZZ is **0.2406**. The "mean_nu f ~0.44
  off-circle lemniscate" memory Rule is a genuine over-generalization of one tiny deg-8
  poly's self-term artifact, and is WRONG. This correctly overturns the standing R3 memory.
- **mean sigma_ZZ ~0.24-0.27, NOT 0.44** across the substantive sequence (j=8 0.260,
  j=13 0.254, j=15 0.253, j=17 0.256, j=24 0.271) — reproduced.

### 2. FR06 obstruction certificate — INDEPENDENTLY CONFIRMED
- **Source check (WebFetch-equivalent: extracted the PDF on disk):** FR06/D'Andrea-
  Narvaez-Clauss-Sombra **Theorem 3.1** (arXiv:1606.04299, `frl_equidist_jtnb.pdf`,
  offset 21369) reads, verbatim modulo OCR artifacts: "There is a positive constant
  C0 <= 15 such that for every C^1 function f: P^1(C) -> R and every xi in Qbar^x,
  |int f dmu_S - int f dlambda_{S^1}| <= Lip_sph(f) (pi/deg(xi) + (4 h(xi) + C0
  log(deg(xi)+1)/deg(xi))^{1/2})", and "In particular if h(xi) <= 1 ... C <= 64." The
  build's transcription in the approach note is **character-for-character correct**.
- **Defect A (circular) re-derived:** as a lower bound, equidistribution gives
  mean_nu f >= mean_lambda f - Lip(f)(error). The error contains the bounded height
  h(xi) under a sqrt with a + sign. Numerically (reproduced from scratch): mean_lambda f
  over |z|=1 = **0.2995**, leverage mean_lambda f - circle-min = **0.0508**, while
  (4*0.249)^{1/2} = **0.998** (20x the leverage). The bound yields a NEGATIVE/vacuous
  lower bound — it cannot manufacture a height floor from the height it is trying to
  bound. Sound.
- **Defect B (capacity-1/wrong target):** the reference measure is lambda_{S^1}, the
  Haar measure on the SINGLE circle |z|=1 (the PDF statement confirms this), whereas ZZ
  conjugate mass sits on BOTH circles. Sound.

### 3. Rigor / scope — CONFIRMED CLEAN
- `## Status` = **none**, `held` lower = **0.2487458** — unchanged. No raise.
- No barred/closed angle touched: only numpy root-finding, the committed Z[w] aux f, and
  FR06 algebra. git status confirms only gap_diagnostic.{py,json}, the approach note, the
  FR06 PDF, R4 reports, and the current.md edit were added — no OSS-energy /
  multivariate-integrality / power-sum / resultant-LP / contour-LP / Z[w] / SOS /
  asymmetric-z / k>32 LLL / integer-locus / BMRL certificate.
- **No smuggled non-sequitur:** the approach note Section 4 explicitly disclaims the
  defective delta->0 (MIN-gap) argument and the BMQS strong-duality "forces delta->0"
  step; neither appears in the load-bearing reasoning. The MEAN gap (persistent) and MIN
  gap (collapsing) are correctly kept distinct.
- **Spec concern (excl-self vs with-self mean gap):** immaterial. The excl-self f is the
  principled object (a genuine ZZ-minimal P is coprime to each Q_j, so log|Q_j(alpha(1-alpha))|
  is finite — the +inf is purely a proxy artifact of using Q_j's own roots). The two
  conventions differ at the 1e-3 level; the qualitative verdict (MEAN gap persists, MIN
  gap collapses, FR06 inert, route OPEN) is unchanged either way.

## Defects found
None material. The build's "max usually < 0.05" hedge is correctly hedged: j=24's max
dist to nearest circle is 0.204 (mean 0.031, within the stated mean range) — the MEAN
claim is robust and the build says "max usually," not "max always." The selftest's
hug-check is mean-based on j=13/15/17/23, which is the right (un-cherry-picked) cut.

## New value vs table value
- New value: **no raise** — verified-NEGATIVE + memory correction. held lower stays
  **0.2487458**.
- Table value (record to beat): **0.2487458** [F18]. Unchanged.

## Goal Progress
- Eval: `grep -hE '^- R[0-9]+:' constants/*/current.md | wc -l`
- Previous: 16
- Current: 17
- Direction: **IMPROVED** (one reviewer-verified progress milestone: corrected the
  standing diagnosis + certified the FR06 route inert, both independently reproduced).

## Milestone line logged (in constants/82a/current.md)
`- R4: VERIFIED-NEGATIVE + standing-memory CORRECTION on the LOWER side (NO raise; held stays Flammang 0.2487458, Status none). ...` (full line in the Progress log).

## Memory note for the run_state
The standing R3 Rule "ZZ-minimal roots sit OFF both circles on the lemniscate
|z(1-z)|=const where mean_nu f ~0.44" is now REVIEWER-VERIFIED WRONG and should be
retracted from run_state Rules. Replacement: ZZ conjugate roots HUG the two circles
(mean dist 0.012-0.034 at deg_w>=12); the slack that remains is the min-vs-mean MEAN gap
(+0.003 to +0.02 on Flammang's family), which the only known tool (FR06 equidistribution)
cannot cash (circular + capacity-1). The min-vs-mean route is OPEN, not dead, but has no
cheap/screenable lever; a raise needs a height-independent containment lemma that does
not exist.
