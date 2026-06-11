# R5 outline — ranked attack angles, C_82a LOWER bound

Spec review: required
(Angle 1 carries a structural closure claim — the power-sum / moment column — that
must be checked for circularity and for any secret re-entry into the barred
energy / contour-LP span before the builder spends a build on it. Angles 2-3 are
diagnostic/closure too. Top pick is a verified-NEGATIVE, not a raise; the reviewer
should confirm it is a genuinely NEW lever-closure, not a re-digest of R3/R4.)

Target to beat: 0.2487458 = log(1.282416)  [Flammang F18, reviewer-verified R1]
  (moving the LOWER bound). NOTE: this round the HONEST realistic deliverable is a
  reproducible verified-NEGATIVE that CLOSES a previously-unexamined lever (a logged
  milestone under the run's verified-progress metric), NOT a raise. Both explorers
  converged that no cheap/screenable raise exists; the lower side is intrinsically
  stuck near Flammang inside closed spans. Say so plainly.

---

## Angle 1 (top pick): Power-sum / moment column ∫w^k dμ_w — verified-NEGATIVE lever-closure

Type: verified-NEGATIVE (closes lever (a) from the dispatch; the single most concrete,
fully screenable previously-unexamined lever). Does NOT move the bound.

What it closes: explorer A floated the power-sum column ∫w^k dμ_w (with w_i = z_i(1-z_i))
as the most plausible "non-energy mean handle" — Σw_i^k are claimed exact integers
(-2,2,-2,... on the Zagier extremal) and it is NOT the barred energy column (no x_1-x_2,
no log kernel). The lever must be CLOSED concretely. It closes for TWO independent,
reproducible reasons — and I have already screened BOTH (see Check):

  Skeleton:
    1. For a ZZ-minimal α of degree d, ∫w^k dμ_w = S_k(w)/d exactly, where
       S_k(w) = Σ_i w_i^k and μ_w is the conjugate measure of w=α(1-α). — by definition
       of the conjugate (counting) measure; S_k computed via Newton's identities from
       the coefficients of the (integer, if a=1) minimal polynomial of w.
    2. MECHANISM 1 (sign-indefinite — not a column). S_k/d is an EQUALITY to a
       polynomial-dependent number that takes BOTH signs across ZZ polys, so it cannot
       enter Flammang's LP as a sign-definite "≥0 drop-out" column. — by direct
       screen: S_1/d ∈ {-1, +1, -0.667, ...}, S_2/d ∈ {+1, +1, -0.667, ...} across
       a handful of ZZ-minimal polys (SCREENED, see Check). A Flammang column needs
       ∫log|Q(w)|dμ_w ≥ 0 uniformly; a power sum gives only an equality to a varying
       real, no ≥0 handle.
    3. MECHANISM 2 (not even integer for non-integer α — the a-penalty wall, identical
       to the OSS no-go). The dispatch/explorer-A premise "Σw_i^k are exact integers" is
       FALSE over the actual ZZ domain. ZZ ranges over ALL algebraic numbers, not just
       algebraic integers; for a primitive non-integer α (a_lead = a > 1) the conjugates
       w_i = α_i(1-α_i) are NOT algebraic integers, so S_k(w) carries a^{-power}
       denominators and is NOT an integer. — SCREENED: P = 10z^2-6z+1 (a=10) gives
       S_1 = 0.44, S_2 = 0.0936, S_3 = 0.0192 — none integers. This is the SAME a^{deg}
       leading-coefficient obstruction that retracted the OSS energy column (R1).
    4. MECHANISM 3 (vanishing even when integer). Even restricted to algebraic integers,
       the constraint ∫w^k dμ_w = S_k/d is an equality to integer/d, an unconstrained
       real as d→∞ (the constraint dissolves) — the same way the trace OBJECTIVE is the
       thing minimized, not a fixed constraint. — by the standard "penalty/constraint
       →0 as deg→∞" argument the run has used for the integer-locus reduction (R2) and
       FR06 circularity (R4).

  Hard step: showing the closure is COMPLETE and does not secretly leave a usable
  variant — specifically, that NO linear combination Σ_k a_k ∫w^k dμ_w (a fixed real
  moment functional) gives a degree-uniform ≥ δ lower contribution to h_Z for all
  ZZ-minimal α. — because any such functional is a polynomial in w integrated against
  μ_w, i.e. ∫P(w)dμ_w = (Σ_i P(w_i))/d = (an integer or a-denominator real)/d, which (i)
  is not sign-definite across polys (Mech 1), (ii) is not even integer off the integer
  locus (Mech 2), and (iii) → 0 as d→∞ on the integer locus (Mech 3). The ONLY way to
  get a ≥0 drop-out from w-data is via log|Q(w)| columns (the Flammang dictionary,
  R3-CEILINGed at 0.2487857) or the log-energy double integral ∫∫log|w_1-w_2| (barred).
  A power/moment column is neither, and supplies no inequality.

  Check (what the builder runs/derives to certify it):
    - A short reproducible screen (`screen_powersum.py`, ~seconds): (a) for ~6 ZZ-minimal
      polys, compute S_k(w)/d for k=1..4 and TABULATE the sign changes — shows the
      moment is sign-indefinite (Mech 1); (b) for P=10z^2-6z+1 (a=10) and one more
      non-integer primitive P, show S_k(w) ∉ Z (Mech 2); (c) a symbolic/Newton-identity
      check that S_k(w) for an integer-α poly equals an integer (so the closure is
      precise, not numerical noise). selftest + tamper (a bogus "≥0 column" claim must
      fail the sign-indefiniteness screen).
    - A one-paragraph structural argument (Hard step) that the moment-functional span
      is disjoint from both the log|Q| ≥0 cone and the energy cone, so it cannot enter
      the auxiliary-function LP at all.
    PRE-SCREENED ALREADY (outliner ran it): Zagier z^2-z-1 gives S_1..S_5 = -2,2,-2,2,-2
    (integer, a=1); palindromic deg4 gives S_1=S_2=4; z^2-z+1 gives S_1=S_2=1; deg3
    z^3-z-1 gives S_1/d=S_2/d=-0.667 — SIGN CHANGES confirmed. P=10z^2-6z+1 (a=10) gives
    S_1=0.44, S_2=0.0936 — NON-integer confirmed. The build is a tidy harness around this.

---

## Angle 2: Trace-transplant single-variable closure — verified-NEGATIVE (structural)

Type: verified-NEGATIVE (closes lever (b)). Does NOT move the bound. Lower-cost than
Angle 1's hard step but slightly higher reviewer-judgment risk (could read as digest).

What it closes: the SSS trace-problem auxiliary-function machinery has been pushed past
naive equidistribution (OSS / Aguirre-Peral / Flammang-trace); the dispatch asked whether
that "mean above min" technique transplants to ZZ to cash the persistent min-vs-mean gap
WITHOUT an energy column. Explorer A found it BREAKS at one clean structural point.

  Skeleton:
    1. Smyth's trace bound is MEAN-DIRECT: x ≥ λ_A + Σ_j c_j log|Q_j(x)|, integrate
       against μ → ∫x dμ ≥ λ_A, because (i) the objective ∫x dμ = (1/d)Σα_i = trace/d is
       a LINEAR functional and (ii) Σα_i = trace ∈ Z is an exact integer. — verbatim OSS
       eq. 2 (§1.1, read from PDF on disk).
    2. ZZ has neither handle: h_Z(α) = ∫σ_ZZ dμ_w with σ_ZZ(z) = log⁺|z| + log⁺|1-z|
       NON-linear, non-polynomial, and Σ_i σ_ZZ(z_i) = d·h_Z IS the unknown height — no
       exact-integer sum. Flammang is therefore FORCED into the min-reduction
       (1/d)Σf(z_i) ≥ min f. The min-vs-mean gap is intrinsic to ZZ and structurally
       ABSENT from the trace problem. — by the form of σ_ZZ vs the linear trace objective.
    3. The HALF of the trace machinery that beat naive equidistribution (OSS §1.2, the
       (x+y)/2 device with Q=x_1-x_2) IS the log-energy column ∫∫log|x_1-x_2|dμdμ — the
       barred OSS family (a^{deg} obstruction, I(ν)<0 for non-integer α). — OSS Thm 1.1,
       confirmed in both explorer reports.
    4. The "finite exceptional cases by hand" device raises only the all-but-finitely-many
       statement, NOT the asymptotic limit point — but C_82 (an essential minimum) IS the
       smallest limit point, so the device buys nothing. — conceptual role from OSS/AP.

  Hard step: none technical; the risk is reviewer judgment that this re-digests R4. It
  is NEW — R4 closed FR06/Petsche equidistribution; it did NOT examine the single-variable
  trace transplant or the objective-linearity argument. — frame it as the trace-machinery
  closure with a named structural reason (mean-direct ⟺ linear objective + integer trace;
  ZZ has neither), with the Σw_i^k integer-but-vanishing demo (shared with Angle 1) as the
  reproducible artifact tying the two halves (mean-direct needs an integer sum; the
  "past-equidistribution" half is the barred energy).

  Check: the structural argument is paper-prose; the reproducible artifact is the same
  `screen_powersum.py` (the exact-integer-on-integer-locus Σw_i^k demo, plus the
  non-integer-off-locus demo, are exactly what witnesses "there is no integer trace
  handle"). Reviewer re-reads OSS §1.1-1.2 to confirm Smyth eq. 2 is mean-direct and
  eq. 3 / Thm 1.1 is the energy column. MERGE NOTE: Angle 1 and Angle 2 share the
  `screen_powersum.py` artifact and the same a-penalty wall; the builder should deliver
  them as ONE certificate closing the "non-energy w-moment / trace-transplant" family,
  with the two mechanisms (sign-indefinite/non-integer moment column AND the
  objective-non-linearity blocking the mean-direct transplant) as the two cores. This is
  the strongest single milestone of the round.

---

## Angle 3: p-adic / non-archimedean residue refinement (lever (c)) — record OPEN longshot, NOT this round's build

Type: assess-and-record-OPEN (explorer B's Opening B). The dispatch asked whether
Zagier's local-height |Res|≥1 technique has ANY cashable screenable lever, or is a pure
longshot. Answer: longshot, no screenable lever this round — record it OPEN with the
single hard step named, do NOT build.

  Skeleton (why it is genuinely outside both closed walls but not cashable now):
    1. The contour LP uses only the SINGLE integrality fact |Res(P, P(1-x))| ≥ 1
       (resultant ∈ Z), collapsing all non-archimedean places into one inequality.
    2. Zagier's 1993 proof and the place decomposition use the finer p-adic structure:
       Σ_{v∤∞}(log⁺|α|_v + log⁺|1-α|_v) is controlled by the reduction of α(1-α) mod v.
       This is NOT a contour integral and NOT a log-energy column — genuinely outside.
    3. But Zagier's local argument is non-effective enough to reach only 0.2406
       (< Flammang 0.2487458). Pushing the local contribution past the +1e-4 gate with
       degree-uniformity is a from-scratch arithmetic argument.

  Hard step: turning "α(1-α) has constrained reduction mod p across conjugates" into a
  degree-UNIFORM additive gain Σ_{v∤∞}(...) ≥ δ·d for ALL ZZ-minimal α surviving to the
  essential minimum. — because no known tool delivers this (Zagier's only reaches 0.2406);
  it is open arithmetic research, not a script. Note that any attempt to make it
  effective via |disc| / |Res| moments re-enters the barred energy span — the explorer
  flagged this as the trap to avoid.

  Check: NONE this round — record OPEN. There is no screen that closes it (it is not a
  finite computation) and no construction that raises with it (Zagier's bound is below
  Flammang). The builder should write ONE paragraph in the approach doc naming this as
  the only genuinely-outside-both-walls residue and its single hard step, so a future
  round knows it is the open frontier, distinct from the (closed) contour LP and (barred)
  energy. Do NOT spend build effort here.

---

## Ranking

1. **Angle 1 + Angle 2 merged (top pick) — the non-energy w-moment / trace-transplant
   closure.** Highest expected verified-progress-per-round. It is a CONCRETE, fast,
   reproducible verified-NEGATIVE (the screen already runs and confirms all three
   mechanisms — sign-indefinite, non-integer off the integer locus, vanishing on it),
   closing the two previously-unexamined levers (a) and (b) the dispatch named, in one
   certificate. It corrects a factual error in explorer A's premise ("Σw_i^k are exact
   integers" — true only on the algebraic-integer locus; FALSE over the ZZ domain, where
   a>1 breaks it) and ties it to the exact a-penalty wall that retracted OSS — a genuinely
   new structural finding, not a re-digest. Lowest risk, highest certainty of a logged
   milestone. BUILD THIS.

2. **Angle 3 (record OPEN, no build).** The honest "what's left" — the only residue
   genuinely outside both closed walls (p-adic local-height refinement), but with no
   screenable/cashable lever this round and Zagier's only effective version below
   Flammang. Worth one paragraph in the approach doc to keep the frontier map honest;
   not a build.

Fall-back: if the reviewer judges the merged Angle 1+2 too close to R4's equidistribution
closure (it is NOT — R4 closed FR06; this closes the trace transplant + the power-sum
moment column, both untouched by R4), the builder can split them: Angle 1 (the power-sum
moment column, with the screened sign-indefinite + non-integer mechanisms) is the harder,
more clearly-new closure and stands alone as the milestone.

Honest strategic note (unchanged from R3/R4, reinforced by both R5 explorers): the lower
side has NO cheap or screenable RAISE; it is intrinsically stuck near Flammang inside the
R3-ceilinged contour span and the barred energy span. This round's deliverable is a
verified-NEGATIVE lever-closure (a milestone), not a record-break. The only conceivable
actual raise is the open p-adic/containment-lemma research (Angle 3 / the standing
min-vs-mean OPEN angle), a longshot with no known tool. If the user releases the
lower-bound focus, the upper side (held 0.2540419719, R11; six straight record-breaks
R5-R11) is the demonstrably pushable frontier.
