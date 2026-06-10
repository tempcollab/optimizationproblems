# [L2009] Lueker — Improved bounds on the average length of LCS (JACM 56(3), 2009)

**What the method is.** Lueker's method is the standard machinery behind every
modern rigorous bound on the binary Chvátal–Sankoff constant $C_{31a}=\gamma_2$.
It works with a *finite-window dynamic program / recurrence on many variables*:

- For two random binary strings, consider the expected LCS computed over a sliding
  window of bounded length. The DP table value satisfies a recurrence; one tracks the
  expected per-step increment of the LCS as a function of a bounded "state" (the
  relevant suffix configuration of the DP frontier).
- **Lower bound:** exhibit a feasible potential / weighting on states such that the
  guaranteed expected per-step gain is provably $\ge$ a value $\Rightarrow$ that value
  is a rigorous lower bound on $\gamma_2$. (A linear-programming feasibility argument.)
- **Upper bound:** a dual construction giving a sequence of upper bounds converging
  to $\gamma_2$ from above.

**Values it gets.** Improved Dančík–Paterson's $0.773911 \le \gamma_2 \le 0.837623$
to $0.788071 \le \gamma_2 \le 0.826280$. The upper bound $0.826280$ is still the
table record for $C_{31a}$.

**Where the slack is.** Both bounds converge to $\gamma_2$ as the window length /
recurrence depth grows, but "computation time grows very quickly as better bounds
are guaranteed" (Lueker). The bound's tightness is governed by the window length $h$
(equivalently the number of state variables in the recurrence); the bottleneck is the
state-space size and memory. There is no analytic obstruction — only compute. This is
why the bound has been pushed purely by heavier computation since.

**Reproducibility.** The lower-bound certificate is a finite feasible LP solution
(a state weighting); a reviewer can re-check feasibility exactly in rational
arithmetic. This is the gold-standard reproducible certificate.

Source: Lueker, JACM 56(3), 2009. https://dl.acm.org/doi/pdf/10.1145/1516512.1516519
