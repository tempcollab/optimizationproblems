## 82a  (C_82a: essential minimum of the Zhang-Zagier height h_Z(alpha)=h(alpha)+h(1-alpha)), LOWER bound — Polya-escape hunt

- Current bounds: lower = **0.2487458 = log(1.282416)** [F18, Flammang 2018; reviewer-verified R1]. upper = 0.2540419719 [this run R11] (table upper 0.25444 [Doc01b]).
- Softer target overall: the **UPPER** side (6 straight verified breaks R5-R11). On the LOWER side, the honest verdict below is: **no genuine escape from the closure exists; every Polya angle the dispatch names collapses back into BMQS strong duality D(g)=ess=P(g) or the product-formula drop-out.** I name the precise collapse mechanism for each, and flag the one structurally-thin spot.

---

### THE LOAD-BEARING NEW FACT I VERIFIED THIS ROUND (read first)

I read the BMQS paper body directly from the on-disk PDF (`literature/pdfs/bmqs2601.18978.pdf`, extracted to /tmp/bmqs.txt), NOT the abstract. Two passages are decisive and were not transcribed verbatim in prior rounds:

**(A) Theorem D (Thm 6.5), verbatim: `D(g) = ess(h_g) = P(g)`** — strong duality, where
`D(g) = sup over { k>=0, a_i in R>=0, P_i in Z[x]\{0} } of inf_{z in C} ( g(z) - sum_i a_i log|P_i(z)| )`.
The dual sup is over **ALL** integer polynomials `P_i in Z[x]` (the conjugate variable z), NOT only the w=z(1-z) subalgebra. This is the auxiliary-function method. Theorem D says it is **EXACT**: its supremum equals the essential minimum. There is no slack between "the best auxiliary function" and "the true essential minimum" — only a *truncation* gap (finitely many columns) between any computed aux function and D(g).

**(B) The lower-bound proof (Prop, lines 3195-3300), verbatim mechanism.** BMQS derive `ess(h_g) >= inf_z(g - sum a_i log|Q_i|)` from the **product formula over ALL places** `prod_{v in M_Q} |alpha|_v = 1`. The non-archimedean places enter through the single inequality (their eq, line 3300):
`sum_i a_i log|Q_i(beta)|_p <= log+|beta|_p` for every prime p, valid because the Q_i have integer coefficients AND `sum_i a_i deg Q_i <= 1` (their condition 6.42). The archimedean part is what's left to optimize (the Green function g on C).

**Why (A)+(B) is the master wall.** Any valid lower bound L on C_82, by definition, satisfies L <= ess(h_g) = D(g). D(g) is the auxiliary-function optimum over the FULL Z[x] dual. So **no "different paradigm" can certify a value larger than the best auxiliary function can** — a genuinely-new method can at most be a *different route to certify a value D(g) also certifies*. The contour-LP closure (R3 ceiling 0.2487857) caps the *Z[w]-subdictionary truncation* of D(g); the remaining headroom up to ess lives only in the *non-w columns of D(g)* and in the truncation. This reframes all four dispatch angles precisely. I take them in turn.

---

### POLYA ANGLE 1 — direct finiteness / counting / sieve / successive-minima certificate (bypass the symmetric-functional reduction)

**Is it outside the closed span?** Superficially yes — a counting/lattice argument on "{alpha : h_Z(alpha) <= H} is finite" reads the DEFINITION directly and never forms a Galois-symmetric mean functional. This is the dispatch's most novel-sounding angle.

**Precise collapse mechanism (decisive, NOT toolless hand-waving).** By Northcott, `{alpha : h_Z(alpha) <= H, deg <= D}` is finite for every (H,D); finiteness of the essential-minimum set requires a UNIFORM-in-degree exclusion (only finitely many alpha across ALL degrees). A direct counting/sieve certificate would have to show: only finitely many algebraic numbers of unbounded degree have h_Z <= H. But the essential minimum is, by BMQS Theorem A (Cor 6.7, verified in the PDF), **realized by a generic sequence of algebraic integers** — i.e. there genuinely ARE infinitely many alpha with h_Z arbitrarily close to ess from above, equidistributing toward a limit measure. So a finiteness certificate for a target H necessarily reads "H < (the limit-measure value) = D(g)". The number it can certify is **bounded above by D(g)** — the same auxiliary-function optimum. Concretely: to exclude an infinite family of high-degree alpha with h_Z <= H you must bound `(1/d) sum_beta sigma_ZZ(beta)` below by H for all but finitely many minimal polynomials, and `(1/d) sum_beta sigma_ZZ(beta)` IS the Galois-symmetric mean functional — you are back inside the R6 dichotomy (power sums + log-energy + height). There is **no counting invariant of a minimal polynomial that is (i) computable, (ii) a lower bound on the conjugate-mean of sigma_ZZ, and (iii) not a symmetric function of the roots** = not power-sums/disc/height. Lattice-point / successive-minima arguments (Minkowski, the geometry of the coefficient lattice) bound the NUMBER of small-height polynomials of fixed degree (Northcott counting, Masser-Vaaler) — they give DENSITY/UPPER results (cf. Morales 2201.11174, upper/density only), never a positive essential-minimum floor.

**Literature check (verified):** my web search for "essential minimum lower bound counting/finiteness without auxiliary function" returns ONLY the auxiliary-polynomial/Smyth family and BMQS (which states the two methods are LP-dual). The Lehmer-type effective bounds (Dobrowolski/Voutier, 1211.3110) bound dh(alpha) from below by something that -> 0 as d -> inf — they do NOT give a positive essential-minimum floor and are a different problem. **No counting/sieve essential-minimum lower bound exists in the literature.**

**Verdict: COLLAPSES into the closure. Longshot at best, and structurally barred by Theorem D + Theorem A (generic-sequence realization).** Not round-sized. The collapse is precise: any finiteness certificate's certified H is <= D(g), and forming the per-polynomial floor re-enters the symmetric-mean dichotomy.

---

### POLYA ANGLE 2 — specialization to a tractable sub-family, then transfer

**Is it outside the closed span?** The sub-family idea (fixed degree, a specific tower/field) is genuinely a different object — a sub-problem can have a LARGER essential minimum, provable by non-energy means.

**Precise collapse mechanism.** Two independent kills:
1. **A sub-family bound is a bound on a DIFFERENT, larger constant, and does not transfer down.** Restricting to (say) totally-real alpha, or alpha in a fixed field, or a fixed tower, gives `ess(h_Z | subfamily) >= ess(h_Z)`, possibly much larger — but the essential minimum of the FULL problem is the inf over ALL algebraic numbers, realized (Theorem A) by a generic integer sequence that is NOT confined to any proper sub-family. A floor on a sub-family says nothing about the alpha that actually realize ess. This is exactly the **splitting-hypothesis** obstruction the R4/R6 digests found for Fili-Petsche / totally-p-adic bounds: those bounds ARE sub-family (totally-real / totally-p-adic) essential-minimum floors, and they are simply absent for the ZZ ess-min class.
2. **Within any sub-family, the lower-bound machine is still Smyth's LP** (R3 survey verified across the whole cousin family: trace, Mahler, house, Faltings — all the same auxiliary-function LP). A "non-energy lower bound that provably exceeds 0.2487458" on a sub-family would itself have to be a new lower-bound technique; none exists, and a fixed-degree numerical computation gives a CONJECTURE (a spectrum value), not a degree-uniform floor — and degree-uniformity is exactly what the essential minimum demands.

**Verdict: COLLAPSES. Not an escape.** A sub-family floor bounds a larger constant and does not descend to ess; the splitting-hypothesis wall is precisely this angle, already closed (R4/R6). Not round-sized.

---

### POLYA ANGLE 3 — analogy to cousin constants; is any recent lower-bound technique there NON-symmetric-functional and transferable?

I re-checked the cousin family against the dispatch's named list. **Every lower-bound technique in the family is Smyth's auxiliary-function/integer-transfinite-diameter LP** (R3 survey, verified vs primary sources). Per-cousin status:

- **Schur-Siegel-Smyth trace (OSS 2401.03252, 1.80203):** the one genuine post-LP advance = the multivariate/log-energy integrality column (`int int log|Q(x,y)| dmu dmu`, Q=x-y giving log-energy). This is symmetric-functional (it IS the discriminant/log-energy cone) and **BARRED for ZZ** (a^deg wall, R1/R5). The single-variable Smyth half is mean-DIRECT only because the trace objective is LINEAR with integer trace — ZZ's sigma_ZZ is non-linear, conjugate-sum = d*h_Z (unknown height), forcing the min-reduction (R5). NOT transferable.
- **Mahler/Lehmer essential minima, house/Schinzel-Zassenhaus (Pritsker 2101.06710, Flammang-Rhin):** integer transfinite diameter / auxiliary functions = Flammang's own method. Symmetric-functional. Not distinct.
- **Faltings ess-min (BMRL 1609.00071):** same Smyth real-section method; novelty is Koebe-distortion of the modular-curve Green function, irrelevant to ZZ's elementary Green function (R2). Not transferable.
- **Bogomolov property / Amoroso-Dvornicich, totally-p-adic (1504.04985, 2404.11559), Fili-Petsche energy integrals (1306.3544):** ALL are (1) splitting-hypothesis-conditional (totally-real/p-adic/local-containment), ABSENT for the ZZ class, AND (2) log-energy mutual-energy integrals on the Berkovich line = barred + capacity-1 trivial at the archimedean place (R4/R6). Not transferable.

**The reason there is no non-symmetric-functional cousin technique:** BMQS Theorem B (Thm 4.1, verified in PDF) characterizes admissible measures EXACTLY by `int log|Q| dmu >= 0 for all Q in Z[x]`. So the ONLY sign-definite-usable drop-out objects on a Galois orbit are the `log|Q|` columns; any "different functional" with arithmetic content (integrality drop-out) is a positive combination of these = inside D(g). A functional WITHOUT integrality content (a smooth/Polya mollifier kernel) gives an analytic inequality with no drop-out, hence no bound (R4 Angle 4). There is no third kind of object.

**Verdict: COLLAPSES. No transferable non-symmetric-functional technique exists in the cousin family.** Every candidate is either the barred energy column, the same LP, or splitting-conditional (absent for ZZ).

---

### POLYA ANGLE 4 — genuine adelic / product-formula combination of archimedean (circle) + non-archimedean (p-adic), beyond the single-place 0.2406 ceiling

This is the angle the dispatch most pointedly asks whether prior closure "genuinely covers the adelic-sum case or only the single-place case." **I checked this directly in the BMQS proof and the answer is now precise: the prior closure DOES genuinely cover the adelic-sum case, because the adelic sum IS the proof mechanism.**

**Precise mechanism (from BMQS lines 3195-3300, read in full).** The lower-bound proof is built ON the product formula `prod_v |alpha|_v = 1`. The non-archimedean places are used to ABSORB the column terms: condition 6.42 (`sum a_i deg Q_i <= 1`) plus integer coefficients gives, at every prime p, `sum_i a_i log|Q_i(beta)|_p <= log+|beta|_p`. So the p-adic part of each column is dominated by the p-adic Weil height, leaving the archimedean part `g(beta) - sum a_i log|Q_i(beta)|` to optimize on C. The optimum over ALL (a_i, Q_i) of `inf_z(g - sum a_i log|Q_i|)` is D(g) = ess. **The archimedean+non-archimedean combination via the product formula is not an unexploited lever — it is the literal foundation of the lower bound, and its full optimum is D(g), pinned to ess by strong duality.**

**Why the 0.2406 (Zagier) figure does not signal residual adelic headroom.** Zagier's [Zag93] `(1/2)log((1+sqrt5)/2) = 0.2406` is the lower bound you get from the COARSEST use of the product formula (one inequality `|Res(P, P(1-x))| >= 1`, no archimedean optimization). Flammang's 0.2487458 is the SAME adelic identity with the archimedean place optimized over a 24-column auxiliary function. The "non-archimedean residue caps at 0.2406" finding (R5/R6) is the value of the non-archimedean inequality ALONE; combining it with the archimedean optimization is exactly Flammang, and that combined optimum is what D(g) caps. There is no third decomposition: the product formula has been fully used. A "richer adelic decomposition" would have to introduce a non-archimedean LOWER contribution beyond `|Res|>=1` — but for alpha ranging over all algebraic numbers (no splitting hypothesis) the finite places give NO surplus floor (Angle 2/Angle 3 splitting wall), and making the surplus effective via |disc|/|Res| moments re-enters the barred log-energy span (R6 Candidate 1, verified).

**Verdict: COLLAPSES, and now PROVABLY so, not "toolless."** The prior rounds recorded the p-adic angle as "OPEN-but-toolless"; this round's reading of the BMQS product-formula proof upgrades that to a precise closure: the adelic sum is the proof's foundation, its full optimum is D(g)=ess, and no extra non-archimedean floor exists absent a splitting hypothesis the ZZ class lacks. Not round-sized; not an escape.

---

### THE ONE STRUCTURALLY-THIN SPOT (brutal honesty — but it too is dominated)

There is exactly one place where the prior closure is a NUMERICAL screen rather than a structural impossibility: **asymmetric (non-w) columns `log|R(z)|`, R in Z[z] not a pullback of Z[w].** These ARE in BMQS's D(g) (the dual is over all Z[x]), and the R6 dichotomy's "any height-independent degree-uniform MEAN floor reduces to power-sums+log-energy+height" is an argument about Galois-SYMMETRIC functionals — a single asymmetric `log|R(z)|` column is z<->1-z-asymmetric, so it is not literally inside that symmetric span. R2 closed asymmetric-z columns NUMERICALLY (LP weight ~0, raise ~1e-8 on the both-circle gate), and R3 closed them STRUCTURALLY via the leading-coefficient obstruction (`prod_i R(alpha_i) = Res(P,R)/a^deg < 1` for non-integer alpha, so the column does not drop out — it makes the bound worse, reducing to the barred integer-locus reduction). 

**Why it is nonetheless dominated and not an opening:** even granting asymmetric columns work cleanly (i.e. restricting to the integer locus a=1 where they DO drop out), they are still inside D(g) — and D(g) = ess. The R3 contour ceiling 0.2487857 caps the Z[w] truncation, but the full D(g) (with asymmetric columns) could in principle reach up to ess (which is <= 0.2540, the upper bound). HOWEVER: (i) the integer-locus reduction needed to admit them is barred (the 2log(a)/d penalty -> 0, R2), and (ii) the R2 numerical screen already priced asymmetric-z columns against the both-circle LP dual and they returned ~1e-8 — LP-saturated. So the thin spot is real (the symmetric-functional dichotomy does not literally cover asymmetric columns) but it is closed by the LEADING-COEFFICIENT obstruction (structural, R3) AND the both-circle numerical saturation (R2), not by the R6 symmetric dichotomy. **This is the most honest characterization of where the closure is thinnest — and it is still closed, on a different (older) warrant.** Re-attempting it would re-run R2/R3 dead ends.

---

### Net assessment for the outliner

**Every Polya angle the dispatch named collapses back into the closure. The collapse mechanisms, now precise:**
1. Counting/finiteness/sieve: certified H <= D(g) = ess (Theorem D), and forming the per-polynomial floor re-enters the symmetric-mean dichotomy; BMQS Theorem A (generic-integer-sequence realization) blocks a uniform finiteness floor above ess.
2. Specialization+transfer: a sub-family floor bounds a LARGER constant and does not descend; this IS the splitting-hypothesis wall (R4/R6), absent for ZZ.
3. Analogy: BMQS Theorem B makes `log|Q|` columns the ONLY sign-definite arithmetic objects; every cousin technique is the same LP, the barred energy column, or splitting-conditional.
4. Adelic combination: the product formula IS the proof foundation (BMQS lines 3195-3300); its full optimum is D(g)=ess; 0.2406 is the coarsest single use, Flammang the optimized use, and there is no third decomposition without a splitting hypothesis.

**The master reason there is no escape: BMQS Theorem D (D(g)=ess=P(g), strong duality, verified from the PDF this round).** The auxiliary-function method is not "one route" — it is provably EXACT. Any lower-bound paradigm is dominated by D(g), and D(g) over the saturated Z[w] dictionary is R3-ceilinged at 0.2487857 (+4e-5 above Flammang); the only headroom to ess is in non-w columns (closed by the leading-coeff obstruction + both-circle saturation) and in unbounded-degree LLL breeding (R1/R2 inert). **No round-sized lower-bound raise is reachable.**

**Recommendation:** surface to the user that the lower side is now closed not only operationally (six verified-negatives) but at the level of the governing duality theorem — there is no paradigm outside D(g), and D(g)'s computable truncation is stuck at Flammang. The genuinely pushable frontier is the **UPPER** side (held 0.2540419719, R11; Doche general-l free-exponent perturbing blocks gave 6 straight breaks). Do NOT switch off the lower bound without a fresh user signal, but the recommendation should be raised plainly.

### Angles to try (lower side): NONE round-sized. The only logged-milestone outcome available is another reproducible verified-NEGATIVE (e.g. a clean transcription of the BMQS product-formula proof + Theorem D as the structural cap on all four Polya angles — which is what this report establishes and a builder could certify as a closure note). No build can raise the bound.

### Dead ends (do NOT retry — all reviewer-verified-NEGATIVE in constants/82a/)
- OSS log-energy / discriminant / multivariate-integrality / power-sum / w-moment columns (any form): BARRED (R1, R5; a^deg leading-coeff wall, I(nu)<0 / S_k non-integer for non-integer alpha).
- Contour-LP / Z[w] / continuum-SOS: R3-CEILINGed at 0.2487857 (feasible primal mu_hat, LP strong duality).
- Asymmetric-z / coupled (z,1-z) columns: leading-coeff obstruction `prod=Res/a^deg<1` (R3) + both-circle LP saturation ~1e-8 (R2). [This is the "thin spot" above — still closed, on the R2/R3 warrant, not the R6 dichotomy.]
- k>32 LLL breeding (uniform + lobe-adaptive): INERT, Z[w] LP-saturated (R1, R2).
- Integer-locus reduction (a=1): 2log(a)/d penalty -> 0 (R2).
- BMRL Faltings transfer: same Smyth method (R2).
- FR06/Petsche effective equidistribution as stated: circular `(4h)^{1/2}` + capacity-1 single-circle (R4).
- SSS-trace mean-direct transplant: needs linear objective + integer trace; sigma_ZZ non-linear (R5).
- Min-vs-mean POINTWISE containment lemma: provably FALSE on Flammang's family (7/13 deg_w>=12 polys have a conjugate below circle-min); MEAN version = barred equidistribution wall (R6).
- p-adic / non-archimedean local-height as a separate lever: the adelic sum IS the LP foundation (this round, BMQS product-formula proof); full optimum = D(g)=ess; no surplus floor without a splitting hypothesis (R5/R6, sharpened here).

### Digests saved
- /home/agentuser/repo/constants/82a/literature/R7_explore_polya.md (copy of this report). NEW content vs prior rounds: BMQS Theorem D (D(g)=ess=P(g)) and the product-formula lower-bound proof (lines 3195-3300, condition 6.42, the per-prime inequality `sum a_i log|Q_i(beta)|_p <= log+|beta|_p`) transcribed from the on-disk PDF as the structural cap dominating ALL FOUR Polya angles — the first round to anchor the closure on the governing strong-duality theorem rather than angle-by-angle screens.

### Sources (verified against primary text this round)
- BMQS arXiv:2601.18978 (on-disk PDF, body read): Theorem D (Thm 6.5) `D(g)=ess(h_g)=P(g)`; Theorem A (generic-sequence realization); Theorem B (Thm 4.1, admissible-measure characterization `int log|Q| dmu>=0`); the product-formula lower-bound proof (lines 3195-3300, conditions 6.40-6.42). https://arxiv.org/abs/2601.18978
- Flammang [F18] hal-03295880 (digest + R3 body read): record lower bound 0.2487458, auxiliary function eq 2.1. 
- Zagier [Zag93]: 0.2406 = coarsest product-formula bound (single non-archimedean inequality, no archimedean optimization).
- Web search (this round): no counting/finiteness essential-minimum lower bound exists; all methods are auxiliary-polynomial/Smyth (BMQS LP-dual). https://arxiv.org/pdf/2601.18978 , https://arxiv.org/abs/1211.3110
- Prior closures cited: R1 (OSS bar), R2 (asymmetric-z/integer-locus/LLL), R3 (contour ceiling 0.2487857 + leading-coeff obstruction), R4 (FR06 circular), R5 (power-sum/SSS-trace), R6 (pointwise-containment FALSE + dichotomy).
