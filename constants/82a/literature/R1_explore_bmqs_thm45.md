# R1 explore — BMQS Theorem 4.5 pushforward measure family μ_{P,Q} as an UPPER-bound route for C_82

Explorer: math-explorer, round 1. Assigned angle: investigate BMQS (arXiv:2601.18978)
Theorem 4.5 — the dense pushforward-measure family μ_{P,Q} — as a FRESH upper-side
construction to push below the R11 record **0.2540419719** (a different lineage from the
R5–R11 Doche perturbed-polynomial family). Read full §4 (Thm 4.1, Prop 4.4, Thm 4.5) and
§7.3 (Prop 7.8) of the PDF, and ran a numerical proof-of-concept of the objective.

**Verdict up front: the recipe is concrete, finite, and reproducible, and it IS a genuinely
different (single-irreducible-pair, lemniscate-supported) construction than Doche. BUT
every VALID low-degree pair gives a value FAR above the record (~0.34–0.69), the density
theorem only promises convergence in a high-degree limit with no efficient search
direction, and Doche is NOT a sub-case of the Thm-4.5 family — Doche optimizes over REAL
exponents on a product (an interior cone direction the single-integer-pair family lacks).
So Thm 4.5 by itself is unlikely to beat 0.254 cheaply; its real value is as a NEW
parametrization to feed a search, and the most promising variant is the weighted/product
generalization (μ′ / Remark 4.6 / weighted V=∏Pᵢ^{qᵢ}) which is exactly Doche — i.e. the
record family already lives in this picture. Detailed below.**

---

## 1. The exact UPPER-bound recipe (crux — what to compute given (P,Q))

**The primal objective (BMQS §1.6, §1.3).** The Zhang–Zagier Green function is
`g(z) = log⁺|z| + log⁺|1−z| = log max(1,|z|) + log max(1,|1−z|)`.
For ANY conjugation-invariant probability measure μ on C with `∫ log|Q| dμ ≥ 0` for all
`Q ∈ Z[x]\{0}` (the cone `P^Z_log(C)`), BMQS §1.3 gives
`ess(h_g) = C_82 ≤ ∫ g dμ`. The primal LP is `P(g) = inf_{μ ∈ P^Z_log} ∫ g dμ = C_82`
(strong duality, Thm 6.5). **So every valid μ yields an upper bound; mu_{P,Q} is a valid μ
(Thm 4.5), hence ∫ g dμ_{P,Q} is an upper bound on C_82.**

**The measure μ_{P,Q} (BMQS (4.25), Prop 4.4).** For coprime monic irreducible
`P,Q ∈ Z[X]`, set `d = deg P`, `e = deg Q`, and `φ_{P,Q} = P^{e+1}/Q^{d}` (a rational map
of degree `d(e+1)`). Then
`μ_{P,Q} = (φ_{P,Q})_* λ_{S¹} / (d(e+1))`  — the **pullback of unit-circle Haar measure**.
Its support is the lemniscate `{ |P(z)|^{e+1} = |Q(z)|^{d} }`, and its potential is
`U^{μ_{P,Q}}(z) = − max( log|P(z)|/d , log|Q(z)|/(e+1) )`  (Prop 4.4).

**The concrete computation (BMQS Prop 7.8 — THIS is the "given (P,Q), compute this number"
recipe).** Define, for θ ∈ [0,1], the C-polynomial
`S_θ(X) = P(X)^{e+1} − e^{2πiθ} · Q(X)^{d}`  (degree `d(e+1)`),
and let `w` range over its roots (`e_w` = ramification index; generically 1). Then
```
∫ g dμ_{P,Q}  =  ∫₀¹ ρ(θ) dθ ,
ρ(θ) = (1 / (d(e+1))) · Σ_{S_θ(w)=0} e_w · g(w)
      = (1 / (d(e+1))) · Σ_{S_θ(w)=0} [ log⁺|w| + log⁺|1−w| ].
```
So the recipe is: **for each θ on a grid of [0,1], form S_θ, find its d(e+1) roots, sum
log⁺|w|+log⁺|1−w|, divide by d(e+1), then average over θ (a single 1-D Riemann/contour
integral over the unit circle).** This is exactly the same KIND of finite, certifiable
quadrature as the existing `verify_upper_*.py` certificates (1-D outward-rounded sum of a
log⁺-of-a-rooted-polynomial integrand). VALIDITY of the bound rests on Thm 4.5's
admissibility proof: `∫ log|F| dμ_{P,Q} ≥ max( log|Res(F,P)|/d , log|Res(F,Q)|/(e+1) ) ≥ 0`
because Res(F,P), Res(F,Q) are integers not both zero (P,Q coprime, F irreducible) — the
SAME resultant-integrality clause Flammang/Doche already use.

**Numerical proof-of-concept (this round, N_θ=900–2000, np.roots).** Verified the recipe
runs and gives valid numbers. Simplest valid coprime irreducible pairs:
| (P, Q) | d, e | deg φ | ∫ g dμ_{P,Q} |
|---|---|---|---|
| x²−x+1, x−1 | 2,1 | 4 | 0.38303 |
| x²−x+1, x | 2,1 | 4 | 0.38303 |
| cyclo₅ (x⁴−x³+x²−x+1), x | 4,1 | 8 | 0.34566 |
| cyclo₅, x−1 | 4,1 | 8 | 0.37876 |
| cyclo₇, x | 6,1 | 12 | 0.33993 |
| x²−x+1, x²+1 | 2,2 | 6 | 0.46000 |
| x⁴+1, x−1 | 4,1 | 8 | 0.47751 |

Best valid single-pair value found ≈ **0.340**, vs record **0.25404**. (Caution logged: a
non-coprime / reducible pair like P=x⁴−3x³+4x²−3x+1=(x−1)²(x²−x+1), Q=x−1 spuriously gave
0.194 — BELOW the lower bound 0.2524 — i.e. an INVALID measure where the density formula
degenerates. **Always check P,Q monic irreducible coprime before trusting the value.**)

## 2. Relationship to the Doche R5–R11 family (is Doche a sub-case?)

**No — Doche is not a special case of the Thm-4.5 μ_{P,Q} family, and the Thm-4.5 family is
not a superset of Doche.** They are different points of the SAME cone `P^Z_log(C)`:
- **μ_{P,Q} (Thm 4.5):** a SINGLE coprime pair of monic IRREDUCIBLE integer polynomials,
  integer (unit) exponents `e+1` and `d`; the support is one lemniscate. Dense as a SET
  over all such pairs, but each member is rigid (no free real exponents).
- **Doche (R5–R11):** the limit/equidistribution measure of a perturbed PRODUCT family
  `h(q) = exp ∫ g dμ_q`, where μ_q is the equidistribution measure on the lemniscate-type
  set `{ |∏_m P_m(χ)^{q_m}| = |Q₁(χ)| }` in the variable `χ = z(1−z)`, with **FREE REAL
  exponents q_m** (R5–R11 added more free-exponent blocks Q₅,Q₆). This is the weighted
  generalization — BMQS's own Remark 4.6 (μ′ via `P^{deg Q}/Q^{deg P}`) and §1.4's
  `V=∏P^q` direction — i.e. an INTERIOR cone direction reached by tuning real exponents,
  which the single-integer-pair Thm-4.5 family cannot directly express.
- **What the larger picture buys (and doesn't):** the extra freedom that drove R5–R11 was
  the REAL-exponent / multi-block product direction, NOT going to a richer single
  irreducible pair. Thm 4.5 trades that exponent freedom for "any irreducible pair," which
  the numerics show is far worse at low degree. So Thm 4.5 does NOT obviously hand us a
  knob Doche lacks; if anything Doche already sits in the more-favorable (weighted-product)
  part of the same cone. The honest read: **the record family is already the better-chosen
  point; Thm 4.5 is a re-coordinatization, not new slack** — consistent with R7_explore_polya
  §4 (lines 146–158), which flagged this exact angle and the same caution a round earlier.

## 3. Tractability — honest assessment

- **Evaluating ∫ g dμ_{P,Q} for a given (P,Q): YES, finite & reproducible.** It is one 1-D
  integral over θ∈[0,1] of a sum of log⁺ over the d(e+1) roots of S_θ; outward-rounded
  quadrature + interval root-enclosure certifies it exactly like the existing
  `verify_upper_q*.py` harnesses. No 2-D lemniscate integration is needed — the pushforward
  collapses it to the unit circle (this is the elegance of the construction).
- **Hard steps:** (i) the integrand log⁺|w|+log⁺|1−w| has a kink where roots cross |w|=1 or
  |1−w|=1 (mild, integrable, same care as existing certs); (ii) ramification points where
  S_θ has a multiple root (measure-zero in θ, but the enclosure must guard them); (iii) the
  normalization 1/(d(e+1)) and the requirement P,Q monic IRREDUCIBLE coprime must be
  machine-checked (sympy `factor_list` + `gcd`) — skipping this gives bogus sub-lower-bound
  "values" (the 0.194 trap above).
- **Smallest pairs that even have a chance:** none of the low-degree ones; best found ~0.34.
  To approach 0.254 the density proof (Thm 4.5) uses `μ_{Pn,Pn+1}` where Pn, Pn+1 are
  consecutive minimal polynomials of a sequence of algebraic integers equidistributing to
  the OPTIMAL measure — i.e. HIGH degree (tens), and you must already know which sequence.
  **There is no efficient way to pick the optimizing (P,Q) — exactly the "enormous search
  space, no efficient direction" wall BMQS state in §1.7.** Realistic path to a number
  < 0.2540419719 from the single-pair family alone: **unlikely cheaply**; would need a
  high-degree directed search with no known compass.

## 4. Softer target & where the slack is

- **Softer side: UPPER** (the user's directive, and structurally right — the upper side is
  a construction/search with a cheap reproducible certificate; lower side is OSS B&B, already
  pushed hard R14–R17 to 0.25240). Current upper held **0.2540419719**, gap to held lower
  0.25240 is only ~**0.00164** — a thin gap, so an upper-side gain must be precise.
- **Where the exploitable slack actually is:** NOT in switching to bare single-pair
  μ_{P,Q} (worse), but in the **weighted/product generalization the Thm-4.5 picture
  legitimizes** — i.e. confirming that the R5–R11 Doche family is the `V=∏P^q` member of
  this cone and then enlarging the DICTIONARY of irreducible factors P_m (new small-ZZ,
  in-lens integer polynomials in χ=z(1−z)) and/or the perturber Q, with free real exponents.
  The slack is the choice of integer factors and exponents, exactly as R7/R10/R11 found.

---

## Ranked, exploitable openings for the outliner

1. **(Most promising, low-risk) Enlarge the Doche dictionary further, justified by the
   Thm-4.5 cone picture.** Treat R5–R11 as the `V=∏P_m^{q_m}` member of `P^Z_log` and add
   one or two MORE free-exponent irreducible blocks in χ=z(1−z) chosen for small ZZ-measure
   / roots in the g=0 lens (beyond F18 Table-1 j=13,15 already used as Q₅,Q₆). Reuse the
   existing `verify_upper_q6.py` harness pattern. This is the proven R5–R11 lever and the
   one with a real chance to beat 0.2540419719 by another ~1e-5–1e-4. Hard step: finding a
   block that lowers, not raises, the optimized integral (diminishing returns — R11 gained
   only 2.2e-5).
2. **(Fresh, medium-risk) Pushforward objective as a NEW certifiable family with FREE REAL
   exponents — the μ′/Remark-4.6 weighted version.** Generalize the Prop-7.8 recipe to
   `S_θ = ∏_m P_m(X)^{n_m·e?} − e^{2πiθ} Q(X)^{?}` with real exponents (the continuous
   `V=∏P^q` limit), minimize `∫ g dμ` over exponents by the existing optimizer. This is the
   single-circle pushforward objective (cheaper integrand than Doche's χ-coordinate double
   integral) — possibly a cleaner/faster certificate for the SAME bound, and a fresh
   parametrization to search. Hard step: making the weighted pushforward a genuinely
   admissible measure (verify `U^μ ≤ 0` or the resultant clause for the product).
3. **(Exploratory, higher-risk) Directed high-degree single-pair search.** Use the density
   theorem literally: take a known small-ZZ algebraic integer sequence (Doche's near-optimal
   conjugates) as Pn, pair consecutive minimal polynomials, compute `∫ g dμ_{Pn,Pn+1}` via
   Prop 7.8. Only worth it if pairs of degree ~20–40 from the actual near-optimal family
   drop below ~0.255 in a quick scan. Hard step: no efficient compass for which pair; likely
   only matches/approaches, not beats.
4. **(Do not pursue as a standalone "new method")** Bare low-degree single irreducible pairs
   — numerically confirmed to sit at 0.34–0.69, hopeless against 0.254.

## Dead ends / cautions (do not retry)
- **Bare single-pair μ_{P,Q} at low degree** — ~0.34 best, far above record (this round).
- **Non-coprime / reducible (P,Q)** — gives spurious values BELOW the lower bound (0.194
  trap); the measure is invalid. Always sympy-check irreducible+coprime+monic first.
- **"Potential-theory reformulation as a new lever"** — R7_explore_polya §2,§4 verified
  strong duality leaves NO gap; the reframing is the existing method in new clothes.
- **Same-family q-only tuning** — R6 well is dry (gained 1.8e-6); gains since came only from
  new dictionary blocks.

## Sources read / digests
- BMQS arXiv:2601.18978 PDF — re-read §1.3/§1.6 (primal P(g)=inf ∫g dμ, the upper-bound LP),
  §4.1 (φ_{P,Q}, (4.25), Prop 4.4 potential, **Thm 4.5 density**, Remark 4.6 μ′), §7.3
  (**Prop 7.8** — the computable ρ(θ) recipe). Extracted via pdfminer
  (`/tmp/bmqs_full.txt`, 99231 chars). This file is the deeper §4/§7.3 digest the
  bmqs_2026_digest.md lacked.
- Cross-checked against existing `literature/doche_doc01b_digest.md` (Doche = weighted χ
  product limit measure) and `literature/R7_explore_polya.md` §4 (which pre-flagged this
  exact μ_{P,Q} angle).
- Numerical PoC of the Prop-7.8 objective: ad-hoc script (np.roots of S_θ over θ-grid +
  sympy irreducibility/coprimality gate); results tabulated above. Not committed (scratch).
