## 82a — generative-theory outline (R1, this run, 2026-06-15)
Spec review: **required** (the load-bearing analytic lemma is non-obvious and the
"is it generative enough to be a contribution" question is the whole point — the
outline-reviewer should sanity-check the magnitude lemma and the scope claim before
the builder spends a round).

Task to beat: NOT a numeric bound. The "record to beat" is the paper's own DIAGNOSTIC-ONLY
status: Prop. `thm:record-fires` + the remark on l.647 explicitly concede the criterion
"does not produce $R_0,R_2$" — it scores them after the fact. The deliverable is a
reviewer-verifiable theorem/construction with GENERATIVE content (tells you which firing
block to BUILD, from a seed), strictly past that diagnostic status, with a re-runnable check.

Held verified bounds (must stay intact, not the target): upper 0.2538893183, lower 0.2524001332.

---

### Inputs verified this round (use as the outline's data — re-derived, not re-litigated)

- **bridge $=P_1^5P_2^5P_4$, $R_0=\mathrm{pp}(Q_1-P_1^5P_2^5P_4\,P_8)$, $R_2=\mathrm{pp}(Q_2+P_1^5P_2^5P_4\,P_7)$.**
- **Degree arithmetic (probe-confirmed, this run):** $\deg(\mathrm{bridge}\cdot P_8)=2a+16$
  ($a$ = bridge exponent). At $a=5$: $\deg=26<28=\deg Q_1$, so $R_0=Q_1-\mathrm{bridge}\,P_8$
  KEEPS $Q_1$'s top two coefficients and $\deg R_0=\deg Q_1=28$ exactly. At $a=6$: $\deg=28=\deg Q_1$
  with leading coeff $+1$, which CANCELS $Q_1$'s leading $+1$ → $\deg R_0$ drops to 27 and $r_Q$
  jumps (0.476→0.523, probe 4). **So $a=5$ is exactly the largest exponent with
  $\deg(\mathrm{bridge}\cdot P_8)<\deg Q_1$, i.e. the maximal LEADING-COEFFICIENT-preserving
  displacement.** This is a clean combinatorial fact, NOT a heuristic — it is the spine of the
  optimality statement and it CORRECTS the explorer's looser "$2a+17$" / "$a$ max preserving deg 28".
- **$R_0$ is a coprime sibling, not small on $\Omega$:** mean $\log|R_0|=7.11\approx\log|Q_1|=7.09$;
  $r_Q(R_0)=-0.0688\approx r_Q(Q_1)=-0.0702$ (Table `tab:recordfire`); $\gcd(R_0,Q_1)=1$, irreducible,
  squarefree, $R_0(0)=R_0(1)=1$ (probe 3). $R_0$ fires by INHERITING $Q_1$'s reduced cost.
- **Magnitude split (the mechanism, probe 3):** on the active bulk of $\Omega$,
  $|Q_1|/|\mathrm{bridge}\cdot P_8|\sim e^{3.16}\sim 23\times$; in $Q_1$'s deepest 2% wells the ratio
  flips to $\sim 3.65$ ($>1$). The bridge is exponentially small on the bulk, comparable in the wells.

---

## Angle 1 (TOP PICK): the degree-preserving coprime-sibling generator theorem

**What it generates, from what seed.** Input: a distinguished firing block $Q^*$ (here $Q_1,Q_2$,
the deg-28 factors of Doche's block) and the active set $\Omega$ of the anchor family. Output: an
EXPLICIT one-parameter family of admissible firing blocks $R(a,\text{tail}) = \mathrm{pp}(Q^*\mp g_a)$,
$g_a=P_1^aP_2^a P_4\cdot P_{\text{tail}}$, of which $R_0,R_2$ are the instances. The theorem proves
(not diagnoses) that every member fires and is an independently-adjoinable denominator block,
and pins the maximal admissible $a$.

**Precise statement to aim for.**
> *Theorem (sibling generator).* Let $Q^*\in\Z[X]$ be a firing perturbing block on family $F$
> ($r_{Q^*}<\log h$), with $\min_s|Q^*(\chi(s))|>0$ (contour-root-free). Let $g\in\Z[X]$ ("bridge")
> satisfy (i) $\deg g<\deg Q^*$; (ii) $|g(\chi(s))|\le|Q^*(\chi(s))|$ for $s$ in a subset
> $\Omega_0\subseteq\Omega$ of measure $\ge1-\delta$; (iii) $R:=\mathrm{pp}(Q^*\mp g)$ is squarefree,
> $R(0)=R(1)=1$, and $\gcd(R,Q^*)=1$. Then (a) $\deg R=\deg Q^*$ and $R$ shares $Q^*$'s top
> $(\deg Q^*-\deg g)$ coefficients; (b) $|r_R-r_{Q^*}|\le \tfrac{1}{\deg Q^*}\!\big(\,\log 2\cdot\delta
> +\!\int_{\Omega\setminus\Omega_0}\!\big|\log\tfrac{|R|}{|Q^*|}\big|\,ds\big)$; and (c) if this bound
> keeps $r_R<\log h$, then $R$ is an admissible firing block coprime to $Q^*$, adjoinable as an
> independent denominator factor. The Grinsztajn $R_0,R_2$ are the instances $Q^*\in\{Q_1,Q_2\}$,
> $g=P_1^5P_2^5P_4\cdot P_{\{8,7\}}$, with $\delta\approx0.02$.

Plus the COMBINATORIAL optimality rider (fully rigorous, no analysis):
> *Proposition (maximal displacement).* For $g_a=P_1^aP_2^a P_4 P_{\text{tail}}$ with $\deg P_{\text{tail}}=12$,
> $\deg g_a=2a+16$. $\deg(Q^*\mp g_a)=\deg Q^*=28$ iff $2a+16\le 27$ iff $a\le5$; at $a=5$ the top two
> coefficients of $Q^*$ are preserved, and $a=5$ is the unique largest exponent preserving the leading
> coefficient. (At $a=6$, $\deg g_a=28=\deg Q^*$ and the leading terms cancel, dropping the degree.)

**Skeleton.**
1. *Setup & admissibility.* State $Q^*$ firing, $\Omega$, the bridge ansatz; verify (iii) by sympy
   (gcd / irreducibility / squarefree / value-at-0,1) — already done in probe 3.
2. *Degree preservation (a).* Pure polynomial algebra: $\deg g<\deg Q^*\Rightarrow$ top coefficients
   of $Q^*$ survive the subtraction; primitive part doesn't change degree. The optimality rider is the
   $2a+16$ count above. — by elementary algebra + one sympy degree print.
3. *The marginal-transfer bound (b) — THE HARD STEP.* $r_R-r_{Q^*}=\frac{1}{\deg Q^*}\int_\Omega
   \log\frac{|R(\chi)|}{|Q^*(\chi)|}\,ds$ (same degree, so the normalizer is shared). Write
   $\frac{|R|}{|Q^*|}=|1\mp g/Q^*|$ up to the primitive-part content factor (a single rational constant,
   handled separately and exactly). Split $\Omega=\Omega_0\cup(\Omega\setminus\Omega_0)$:
   - On $\Omega_0$ ($|g/Q^*|\le1$): $\big|\log|1\mp g/Q^*|\big|\le -\log(1-|g/Q^*|)\le \frac{|g/Q^*|}{1-|g/Q^*|}$,
     and on the bulk $|g/Q^*|\le e^{-c}$ with $c\approx3.16$ measured, so this is uniformly small.
   - On $\Omega\setminus\Omega_0$ (the deep wells, measure $\le\delta$): bound $\big|\log\frac{|R|}{|Q^*|}\big|
     \le \log\frac{1}{\min|R(\chi)|}+\log\max|Q^*(\chi)|$ — FINITE because $R$ is contour-root-free
     ($\min_s|R(\chi)|>0$, audited $\ge10^{-2}$ class) — times $\delta$.
   — by the $\log|1\mp g/Q^*|$ expansion (bulk) + the contour-root-free $L^1$ bound (wells).
4. *Firing transfer (c).* Combine: $r_R\le r_{Q^*}+(\text{bound (b)})<\log h$, given the measured
   numbers. So $R$ fires. — by Cor. `cor:criterion` applied to $R$.
5. *Independence.* $\gcd(R,Q^*)=1$ ⇒ $R$ is a fresh admissible block, $\deg Q$ grows by $\deg R$.
   — by Lemma `lem:doche` admissibility for the enlarged dictionary.

**Hard step — made precise (this is what the outline-reviewer must vet):**
The load-bearing inequality is the **deep-well correction bound** in step 3. State it as:
$$\Big|\int_\Omega \log\tfrac{|R(\chi(s))|}{|Q^*(\chi(s))|}\,ds\Big|\;\le\;
\underbrace{\int_{\Omega_0}\frac{|g/Q^*|}{1-|g/Q^*|}\,ds}_{\text{bulk, }\le\,\frac{e^{-c}}{1-e^{-c}}}\;+\;
\underbrace{\delta\cdot\big(\log\tfrac{1}{m_R}+M_{Q^*}\big)}_{\text{wells}},$$
where $c=\mathrm{ess\,inf}_{\Omega_0}\log|Q^*/g|$ ($\approx3.16$), $m_R=\min_s|R(\chi(s))|>0$,
$M_{Q^*}=\max_s\log|Q^*(\chi(s))|$, $\delta=|\Omega\setminus\Omega_0|$ ($\approx0.02$).
**Why it holds:** the bulk term is the standard $|\log|1+u||\le -\log(1-|u|)\le |u|/(1-|u|)$ for
$|u|\le e^{-c}<1$; the well term is just "$\log$ of a quantity bounded away from $0$ and $\infty$,
times the well measure" — finite precisely because $R$ has no roots on the contour $\chi(|z|=1)$.
**Where rigor could fail (flag to reviewer):**
(α) the constant $c$ must be a CERTIFIED lower bound of $\log|Q^*/g|$ on $\Omega_0$, not the mean —
the builder must take $\Omega_0=\{|g|\le|Q^*|\}$ and bound $|g/Q^*|\le1$ there, making the bulk term
$\le\int_{\Omega_0}\frac{1}{0}$... NO — on the boundary $|g/Q^*|\to1$ the bound $\frac{|u|}{1-|u|}$
blows up. **FIX:** define $\Omega_0=\{|g/Q^*|\le\theta\}$ for a fixed $\theta<1$ (e.g. $\theta=1/2$),
absorb $\{\theta<|g/Q^*|\le1\}$ into the "wells" term where the finite contour-root-free bound applies.
Then $\delta=|\{|g/Q^*|>\theta\}|$ and the bulk term is $\le\frac{\theta}{1-\theta}|\Omega_0|$.
(β) the content factor (primitive part of $Q^*\mp g$) contributes $\deg Q^*\cdot\log|\mathrm{cont}|$ to
the integral — must be computed exactly (sympy `.primitive()` gives it as a rational) and added, not
dropped. For $R_0,R_2$ the content is $1$ (probe 3 takes pp with no scaling) — verify and state.
(γ) the bound must come out NUMERICALLY $<\log h - r_{Q^*}$ with the certified $\theta,\delta,m_R,M_{Q^*}$;
if the rigorous constants are too loose to clear it, the theorem proves "$R$ fires" only conditionally
on the measured (not certified) margin — that weakens (c) to a diagnostic again. **The reviewer should
check the rigorous constants actually close the gap for $R_0$**: $r_{Q^*}\approx-0.069$, $\log h=0.2536$,
so the slack is $\approx0.32\cdot28\approx 9$ in the un-normalized integral — generous, the bound
should clear it comfortably, but this must be DEMONSTRATED, not asserted.

**Check the builder produces / reviewer re-runs.**
- `sibling_generator.py` (new): given $Q^*\in\{Q_1,Q_2\}$ and bridge ansatz, construct $R$, assert
  (a) $\deg R=28$ + shared top coeffs, (iii) admissibility (sympy), and EVALUATE the four rigorous
  constants $\theta$-split bound: $|\Omega_0|,\delta,\,\sup_{\Omega_0}|g/Q^*|\le\theta$, $m_R$, $M_{Q^*}$,
  by outward-rounded grid evaluation (the same harness style as `verify_upper.py`). Print the RHS of the
  hard-step inequality and confirm $r_{Q^*}+\text{RHS}<\log h$. Cross-check $r_R$ measured directly
  ($-0.0688$) lies within $[r_{Q^*}-\text{RHS},\,r_{Q^*}+\text{RHS}]$.
- finite-difference confirmation that $r_R<\log h \Leftrightarrow \partial_+\log h/\partial q_R<0$,
  reusing `firstvar_04_perturbing_marginal` on the $R$-adjoined family.
- the optimality rider: one print of $\deg(\mathrm{bridge}_a\cdot P_8)=2a+16$ for $a=3..6$ and the
  resulting $\deg R$ (probe 4 already shows it).

**Honest scope line (mandatory in the paper).** PROVES: $R_0,R_2$ are degree-preserving coprime
admissible siblings of $Q_1,Q_2$ whose marginal is transferred from the seed by a certified
magnitude-subordination bound, and $a=5$ is the maximal leading-coefficient-preserving exponent — a
stated CONSTRUCTION RECIPE, given the distinguished block as seed. DOES NOT prove: that the criterion
ALONE (no seed) predicts $R_0,R_2$; that the bridge $P_1^5P_2^5P_4$ or the tails $P_7,P_8$ are OPTIMAL
among generators (that is the open WITD residual — keep heuristic); that the recipe produces the BEST
siblings. This clears the referee bar as a contribution: it converts "we diagnose $R_0,R_2$ fire"
(current l.647) into "here is the explicit generator, the magnitude condition that makes it fire, and
the degree count that forces $a=5$ — $R_0,R_2$ are its instances."

---

## Angle 2 (alternative framing): the bridge-exponent family + optimality of $a=5$ as the headline

Rather than a general subordination theorem, make the COMBINATORIAL optimality the centerpiece (it is
the most fully-rigorous piece and needs no analytic lemma):
> *Theorem (the firing-sibling family and its boundary).* For the distinguished block $Q_1$ (deg 28)
> and tail $P_8$ (deg 12), the bridge family $g_a=P_1^aP_2^aP_4$ yields siblings $R_a=\mathrm{pp}(Q_1-g_aP_8)$
> with: $\deg R_a=28$ and $R_a$ coprime/admissible for $a\in\{1,\dots,5\}$; $\deg R_a<28$ for $a\ge6$
> (leading-term cancellation); and $r_{R_a}\to r_{Q_1}$ monotonically as $a$ grows within the
> degree-preserving range, with $a=5$ the boundary case ("deepest" displacement still copying the leading
> behaviour). Grinsztajn's $R_0$ is $R_5$.
**Skeleton:** (1) degree count $2a+16$ (rigorous); (2) admissibility per $a$ by sympy (rigorous, finite
check $a=1..5$); (3) the $r_{R_a}\approx r_{Q_1}$ transfer — reuses Angle-1's hard step but only NEEDS it
qualitatively (monotone approach), so the analytic constants can be looser. **Hard step:** the same
$\log|1-g_a/Q_1|$ bound, but here used only to show $r_{R_a}$ stays firing across $a=1..5$ — a weaker ask.
**Check:** `sibling_family.py` printing $(\deg R_a, \text{admissible}?, r_{R_a})$ for $a=1..6$; the
table IS the theorem. **Scope:** proves the family + its degree boundary; the *choice* of tail ($P_7$ vs
$P_8$, for $R_0\perp R_2$ coprimality) is stated as a coprimality requirement, not optimized.
**Why a viable fallback:** if Angle-1's certified magnitude constants turn out too loose to rigorously
force $r_R<\log h$ (risk γ above), this version still delivers a real generative theorem — the explicit
family + the rigorous degree-boundary optimality + admissibility-per-$a$ — without leaning on the
analytic constant clearing the gap. Lower ceiling, higher floor.

---

## Angle 3 (alternative framing): constructive existence theorem via the deep-well displacement

> *Theorem (firing siblings exist for any deep-well block).* Let $Q^*$ be a firing perturbing block whose
> contour-distance min$_s|Q^*(\chi(s))|=m>0$ and whose $|Q^*|$ has wells of relative depth $\ge\rho$ on a
> subset of $\Omega$ of measure $\ge\eta$. Then there exists an integer bridge $g$, $\deg g<\deg Q^*$,
> producing an admissible firing sibling $R=\mathrm{pp}(Q^*-g)$ coprime to $Q^*$ — explicitly, any $g$
> integer-supported on (a power of the smallest base factors)$\times$(a tail with a root in the wells)
> with $|g|\le|Q^*|$ off the wells and $|g|\gtrsim|Q^*|$ on them.
**Hard step:** an EXISTENCE/genericity claim — that such a $g$ exists in $\Z[X]$ with the dual magnitude
property (small on bulk, large in wells) AND keeping $R$ contour-root-free. This is the hardest to make
rigorous in one round: it needs a constructive lattice argument (the R7 LLL/closest-vector machinery,
which R7 found SPARSE — naive rounding dry, firing blocks isolated). **Verdict: rank last.** The existence
is plausible but the constructive guarantee is exactly the open hard problem R7 hit; do NOT promise it as
a theorem. Could appear as a *conjecture* + the worked $R_0,R_2$ instance.

---

## Refuted lines — do NOT propose (from R7 + paper Remark l.709)

- **Equilibrium / transfinite-diameter generative rule** (paper `rem:noteq`, R7): REFUTED. $\Omega$'s
  equilibrium potential $\approx0.524\ne\log h=0.254$; integer firing roots sit strictly inside the unit
  disk ($|\zeta|\in[0.43,0.79]$) and cannot reach the continuous potential wells. "Roots track the deep
  wells of $U^\nu$" is FALSE for the integer problem. Any angle resting on roots reaching equilibrium
  wells is dead.
- **"$R_0$ is small on $\Omega$"**: WRONG — $R_0$ is the same size as $Q_1$; it fires by inheriting $Q_1$'s
  cost. The generator is a sibling construction, not an approximation-to-zero.
- **Global $r_Q$-minimization over all $\Z[X]$ as the principle**: R7 proved sparse knife-edge integer
  lattice; no closed-form minimizer. The generator is a SUBROUTINE from a seed, never claim it solves
  unconstrained $r_Q$-min.

---

## Ranking & recommendation

**Recommend Angle 1, with Angle 2 as the explicit fallback in the SAME builder round.** Angle 1 is the
genuine generative contribution (a stated construction + the magnitude condition that makes it fire +
why $a=5$), and its hard step is a clean two-piece bound on a single integrable function — the kind of
lemma a builder can write and a reviewer can re-derive in one pass. The only real risk (γ) is whether the
RIGOROUS constants in the deep-well term clear the firing gap; the seed slack ($r_{Q^*}\approx-0.069$ vs
$\log h=0.254$, un-normalized $\approx9$) is large, so this should clear comfortably — but it is exactly
why Spec review is required. If it does NOT clear rigorously, Angle 2 (the bridge-exponent family +
rigorous degree-boundary optimality) is already 80% of the same artifact and delivers a referee-acceptable
generative theorem WITHOUT depending on the analytic constant — so the builder should compute the
degree-count + per-$a$ admissibility table (Angle 2, rigorous, cheap) FIRST, then attempt the Angle-1
magnitude bound on top. Angle 3 is a conjecture, not a one-round theorem; mention only as future work.

The combined Angle 1+2 artifact converts the paper's `rem` l.647 from "explanatory, not generative" to
"the criterion + the explicit sibling generator account for $R_0,R_2$ block-for-block: they are the
maximal degree-preserving coprime siblings of the distinguished block, firing by magnitude-subordination
of the bridge on $\Omega$." That is the milestone.
