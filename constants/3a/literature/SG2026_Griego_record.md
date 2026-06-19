# SG2026 — Griego, base-21 non-uniform digit construction (PR #71, MERGED). RECORD = 1.1740744

Source: teorth/optimizationproblems PR #71 (merged, approved by teorth). No arXiv; the PR body
is the paper. **Reproduced locally** (script below runs in seconds): θ = 1.17407444769352116...

## THE RECORD CONSTRUCTION
Non-uniform digit alphabet with a GLOBAL digit-sum cap, encoded in base 21:
$$ A=\{0,2,3,4,5,6,7,8,9,10\},\quad B=21,\quad d=80,\quad T=150, $$
$$ U=\Big\{\sum_{i=0}^{79} a_i\,21^i:\ a_i\in A,\ \sum_{i=0}^{79} a_i\le 150\Big\}. $$
Note: the digit set runs $0\dots10$ but **omits 1** (and 11..20). Base $21=2\cdot10+1$ so digit
sums/differences stay in $[-20,20]$ → no carries (injectivity preserved). $T=150$ is a single
global cap on $\sum a_i$ (like Gerbicz's $L$, but with a custom alphabet, not $\{0..B\}$).

Exact values:
- $\max U = 10\sum_{i=65}^{79}21^i$ (top 15 digits =10).
- $|U+U| = 75448362167176243488362019935078206851619643198150854886920234689186981134888$
- $|U-U| = 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415$
- $\theta = 1+\log(|U-U|/|U+U|)/\log(2\max U+1)=1.174074447693521\ldots \ge 1.1740744$.

## HOW IT GENERALIZES Gerbicz/Zheng (the key conceptual step)
Gerbicz/Zheng use the **uniform** alphabet $\{0,1,\dots,B\}$ with cap $\sum x_i\le L$. Griego
uses an **arbitrary** alphabet $A$ (here non-uniform, omitting 1) with cap $\sum a_i\le T$.
This is a strictly larger search space. The counting is no longer a clean binomial sum — it is
done by **exact dynamic programming** (carries forbidden, so each digit position is
independent given the running constraint totals):
- **Sum count** $|U+U|$: per output sum-digit $y\in A+A$, the set $P_y=\{a\in A:y-a\in A\}$ of
  feasible carries-in. DP over $d$ positions tracking (sum of $y$ so far) and a **bitset** of
  reachable values of $\sum a_i$; feasible iff $\exists$ split with $\sum a_i\le T$ and
  $\sum(y_i-a_i)\le T$.
- **Diff count** $|U-U|$: per output diff-digit $\delta\in A-A$, the cheapest representative
  $q_\delta=\min\{b\in A:b+\delta\in A\}$; feature $(q_\delta,q_\delta+\delta)$. DP over $d$
  positions tracking (left total, right total), feasible iff both $\le T$. (This is the EXACT
  analogue of Gerbicz (2.5)/Zheng's $d(U)$ — but for the general alphabet.)
- **Certificate rigor:** $\log$ computed with rational $\text{atanh}$ series + explicit
  remainder bounds, $2\max U+1$ exact; the inequality
  $\log(d/s)-0.1740744\log q>0$ is verified with a directed-rounded margin
  $>1.16\times10^{-5}$, interval width $<2.4\times10^{-115}$. Fully reproducible, Lean-fittable
  (all-integer counting + a rational log bound).

## FREE PARAMETERS (the levers for beating 1.1740744)
1. **Digit alphabet $A$** — its size, which values it includes/omits (omitting 1 was the win).
   Subject only to $0\in A$ and base $\ge 2\max A+1$ (carry-free).
2. **Base** $=2\max A+1$ (forced by carry-free; here 21 since $\max A=10$).
3. **Number of digits $d$** (here 80) and **global sum cap $T$** (here 150). Ratios $T/d$,
   $\max A$ matter; in the asymptotic limit only $T/d$ and the alphabet shape survive.
4. Possibly a **per-position** alphabet/cap (inhomogeneous digits) — untried.

## WHY THIS IS THE PRIMARY ATTACK SURFACE
- The record is only ~0.00007 above Zheng's uniform limit — Griego found a small alphabet tweak
  ($\{0..10\}\setminus\{1\}$) that helps. The space of alphabets is large and barely explored:
  re-optimizing $A,T,d$ (or $T/d$ in the limit) is the most direct path to >1.1740744.
- The 1.25 ceiling (GHR, single-set route) leaves a wide corridor: 1.1740744 → 1.25.
- The exact-counting DP is cheap (seconds for $d=80,T=150$); a search over alphabets/caps is
  computationally feasible, and any improved triple yields an exact, re-runnable certificate.

## Reproduction
`pdfs/`-free: the verification script is in PR #71 body and was re-run here:
`|U+U|`, `|U-U|`, θ all match to the printed digits. The DP + rational-log-bound machinery is
the reusable certificate template for any new $(A,d,T)$.
