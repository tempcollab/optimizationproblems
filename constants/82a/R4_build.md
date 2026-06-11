# R4 build — C_82a LOWER bound (Zhang-Zagier essential minimum)

Target to beat: **Flammang [F18] 0.2487458 = log(1.282416)** (verified R1).
Outcome: **NO raise. A reproducible verified-NEGATIVE + a load-bearing memory CORRECTION.**
held lower stays Flammang 0.2487458; Status stays `none`. This is exactly the
reviewer-sanctioned deliverable (the R1-R3 milestone class), scoped per the outline
review's mandatory corrections.

## What I built

### (1) Root-location diagnostic correction — `certificate/gap_diagnostic.py` (+ `gap_diagnostic.json`)
Self-contained (numpy only), with a `selftest`. Across ALL 24 Flammang Table-1 polys it
computes per poly: roots z of Q_j(z(1-z))=0, their distance to the two circles |z|=1 and
|1-z|=1, mean sigma_ZZ over the roots, the circle-min of the FULL Flammang aux f, and the
per-poly MIN and MEAN gaps (root-f minus circle-min), using the principled "exclude the
self term" f (a genuine ZZ-minimal P is coprime to each Q_j). Emits `gap_diagnostic.json`.

Corrected, reproduced numbers:
- **circle-min f = 0.2487462** (reproduces Flammang record, +4.4e-7).
- **Roots HUG both circles**: deg_w>=12 mean dist 0.012-0.034, max usually <0.05
  (j=13 0.025, j=15 0.030, j=17 0.038, j=23 0.050). The |z| in [0.5,2.0] spread is the
  OTHER circle (|z|~1.97 => |1-z|~1), NOT an off-circle lemniscate.
- **mean sigma_ZZ ~0.24-0.27, NOT 0.44** (j=8 0.260, j=13 0.254, j=15 0.253, j=24 0.271).
- **The bogus "0.44" = the FULL-f-WITH-SELF +inf artifact on the tiny deg-8 poly j=5**
  (full-f mean 0.4320; honest mean sigma_ZZ 0.2406; its roots lie ON the circles).
  Explorer B over-generalized this single tiny-poly artifact. **This corrects the wrong
  R3 lemniscate Rule the loop has carried since R3.**

### (2) Equidistribution-route obstruction note — `approaches/R4-min-vs-mean-equidistribution.md`
- States the min-vs-mean lower-bound identity and that it is the ONLY non-barred live
  mechanism.
- Reports the **MEAN gap, prominently**, and shows it is positive and PERSISTENT
  (+0.003 to +0.02 at deg_w 16-22), while the MIN gap collapses toward/below 0 — and that
  the mechanism uses the MEAN gap, so the route is NOT killed by a shrinking gap.
- Transcribes **FR06 Theorem 3.1 verbatim** (arXiv:1606.04299 §3, PDF on disk) with its
  source, and certifies the two defects: (A) **circular** — the error term contains
  (4h)^{1/2}, the bounded height; made numeric: leverage mean_lambda f - circle-min =
  0.0508, but (4*0.249)^{1/2} = 0.998 (20x the leverage) => the bound is quantitatively
  vacuous, not just circular; (B) **capacity-1 / wrong target** — equidistributes to
  lambda_{S^1} on a single circle, the wrong limit measure for the two-circle ZZ support.

## Exact reproducible check commands
```
cd constants/82a/certificate
python3 gap_diagnostic.py selftest    # cores [A]-[E], prints "selftest: ALL PASS", exit 0
python3 gap_diagnostic.py             # full per-poly table + degree trend; writes .json
```
Selftest cores: [A] circle-min reproduces Flammang; [B] roots hug circles (deg_w>=12);
[C] mean sigma_ZZ in [0.23,0.28] not 0.44; [D] the 0.44 is the j=5 self-term artifact;
[E] MEAN gap persists >1.5e-3 at deg_w>=16. The mean_lambda f = 0.2995 and the
circularity numbers in the note are recomputable from the same f.

## Honest scope of the verified-NEGATIVE (per outline-review, obeyed exactly)
ESTABLISHED: the R3 lemniscate/0.44 diagnosis is wrong and corrected; the correct slack
is the persistent min-vs-mean MEAN gap; the FR06/Petsche tool is circular + capacity-1
inert. NOT CLAIMED: the route is NOT declared "DEAD"; recorded as **OPEN / "no cheap or
screenable lever found"** — the persistent mean gap is UNCAPTURED because a degree-uniform
floor needs a height-INDEPENDENT containment lemma that does not exist (log|disc|/energy
versions barred; h versions circular). The defective "delta->0 from the MIN gap" argument
is NOT used. The BMQS "strong duality forces delta->0" step is NOT used (non-sequitur:
duality pins the optimum to the unknown C_82, not to circle-min). The mean-gap data is on
Flammang's AUX polys, not ZZ-minimal polys, so it is suggestive, not a uniform-floor proof
— stated explicitly in the note (Defect 3 caveat).

## Barred/closed angles touched: NONE
Uses only numpy root-finding, the committed Z[w] aux f, and FR06 Thm 3.1 algebra. Does NOT
touch OSS energy / multivariate-integrality / power-sum / resultant LP, contour-LP / Z[w] /
SOS, asymmetric-z, k>32 LLL, integer-locus, or BMRL.

## Spec concerns
- The min-vs-mean f gaps are computed with the SELF term excluded (index j removed from the
  sum). This is principled (a ZZ-minimal P is coprime to each Q_j; the +inf at Q_j's own
  roots is a numerical artifact, NOT a property of genuine ZZ conjugates) and the script
  documents and exposes both versions. The outline-review's quoted mean-gap magnitudes
  (+0.005-0.02) came from the WITH-self artifact-inflated f; my principled excl-self gaps
  are slightly smaller (+0.003-0.02 at deg_w 16-22) but still robustly persistent and >>
  1.5e-4. The qualitative conclusion (MEAN gap persists, MIN gap collapses, route OPEN) is
  unchanged and, if anything, the excl-self version is the more defensible object. A reviewer
  re-deriving should be aware the two f-conventions differ at the 1e-3 level; neither changes
  the verdict. No other part of the constrained spec was unmet.
