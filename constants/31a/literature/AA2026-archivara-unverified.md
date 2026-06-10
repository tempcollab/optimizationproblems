# [AA2026] Archivara Agent — Monte Carlo Beam Search lower bound (2026, UNVERIFIED)

**Claim.** $C_{31a} = \gamma_2 \ge 0.79970$ (marked unverified / starred in the
README and table).

**Method (from the repo https://github.com/spicylemonade/constant).**
NOT Lueker's DP. Instead:
1. **Beam search** (width $W=100$) that, for a sampled pair of length-$n=1000$
   binary strings, produces a *valid* common subsequence by construction (so its
   length is a genuine lower bound on the LCS of that pair).
2. **Monte Carlo:** $M=10^6$ independent trials, average the beam-search LCS length
   $\bar Z$.
3. **Hoeffding concentration:** report
   $\gamma_2 \ge \mathbb{E}[Z]/n \ge \big(\bar Z - \sqrt{\ln(1/\delta)/(2M)}\big)/n$
   with $\delta = 10^{-12}$.

**Is this a valid lower bound?** Plausibly yes, and worth flagging for the outliner:
- LCS length is **superadditive**, so $\mathbb{E}[\lambda_n]/n$ is *increasing* in $n$
  and converges *up* to $\gamma_2$. Hence $\mathbb{E}[\lambda_n]/n \le \gamma_2$ for
  all finite $n$ — a high-confidence lower bound on $\mathbb{E}[\lambda_{1000}]/1000$
  IS a valid (probabilistic) lower bound on $\gamma_2$.
- The beam search underestimates the true LCS (it finds *a* common subsequence, not
  necessarily the longest), so $\bar Z \le \mathbb{E}[\lambda_{1000}]$ in expectation
  — only strengthens the direction.
- Caveat: the bound is *probabilistic* (holds w.p. $1-\delta$), not a deterministic
  certificate. For a repository record, the reviewer must decide whether a Hoeffding
  bound counts as "rigorous." This is exactly why it is starred/unverified.

**Why it matters for our run.** Two orthogonal, reproducible roads to beating the
verified record $0.792665992$:
  (A) Lueker/Heineman deterministic DP certificate — the gold standard;
  (B) the Monte-Carlo + concentration route — cheaper to run, but the reviewer may
      not accept a probabilistic bound, and 0.79970 is itself only *claimed*.
Do not treat 0.79970 as established; the number to strictly beat for a *verified*
milestone is **0.792665992** [H2024].

Source: https://archivara.org/paper/1a5c6a48-a106-40e4-a5f0-97833f3a25a7 ;
code https://github.com/spicylemonade/constant
