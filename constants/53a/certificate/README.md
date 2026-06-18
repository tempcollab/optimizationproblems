# Certificate — 53a, approach `lean-conditional-scaffold` (round 2)

This is a **Lean-fit** certificate: type-checking IS the check. It certifies the
load-bearing *integer recursion step* of Grinsztajn's `D(C_n^3) <= 4n - P(n) - 2`
argument (=> `C_53 <= 4`). It is NOT a new bound — it re-derives the existing
`held` upper bound conditionally, seeding the Lean certificate scaffold.

## What to run (reviewer reproduction)

```sh
export PATH="$HOME/.elan/bin:$PATH"
cd /home/agentuser/repo/lean
lake exe cache get          # one-time: fetch pinned Mathlib oleans (if not present)
lake build Constants        # THE check — must complete "Build completed successfully"
```

`lake build Constants` compiling clean **is** the certificate. The build emits the
`#print axioms` lines (see below) as `info` messages at the end.

## Pinned environment (committed, do not float)

- `lean/lean-toolchain`        : `leanprover/lean4:v4.31.0`
- `lean/lake-manifest.json`    : Mathlib pinned to commit
  `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` (tag `v4.31.0`)
- Build target                 : `Constants` (lean_lib in `lean/lakefile.toml`)
- Proof file                   : `lean/Constants/C53a.lean`

## Theorems and their axiom audit

The file ends with:

```lean
#print axioms Constants.C53a.recursion_step
#print axioms Constants.C53a.comparison_ineq
```

Observed output (captured `axioms.txt`):

```
'Constants.C53a.recursion_step' depends on axioms: [propext, Classical.choice, Quot.sound]
'Constants.C53a.comparison_ineq' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Only the three Lean **foundational** axioms — **no `sorryAx`, no smuggled
problem-specific axiom**. The zero-sum number-theory inputs are carried as ordinary
**hypotheses** of `recursion_step` (`hstep`, `hm`), not as axioms, so the conditional
nature is explicit and the load-bearing algebra is genuinely proved.

## What is proved vs. assumed

PROVED (fully, no sorry):
- `comparison_ineq : 2 <= p -> p <= Q -> p^2 - 2p + 2 <= (p-1)*Q`  (over ℤ, `nlinarith`).
- `recursion_step` : `D m <= 4m - Q - 2 -> D(p*m) <= p*D(m) + p^2 -> 2<=p -> p<=Q`
  `-> D(p*m) <= 4(p*m) - Q - 2`.
- `base_in_form` : the prime-power base case `D(C_Q^3) = 3Q-2` rewritten as `<= 4Q - Q - 2`.

ASSUMED (Grinsztajn's cited zero-sum inputs, carried as hypotheses, NOT proved here):
- `hstep` = Lemma 2.1 (inductive method) + Lemma 2.3 (local estimate `D_k(C_p^3) <= pk + p^2`).
- the base value `D(C_Q^3) = 3Q-2` (Gao-Geroldinger p-group lower bound).

## Update — round 3 + round 4 (later theorems in the same file)

The scaffold has since grown (same file, same pinned env, same reproduction command). The
authoritative axiom audit for ALL theorems is `axioms.txt`. Highlights:

- ROUND 3: `acc_cast_bridge`, `global_induction` (the List fold over the factor list), and
  `c53_le_4_per_n` (the per-`n` inequality `D n - 1 <= 4*((n:ℤ)-1)`). The global factorization
  induction is now formalized (over an abstract factor list).
- ROUND 4: `factors_bridge_max` — for a concrete `n >= 2`, ties that abstract list to the
  ACTUAL prime factorization `Nat.primeFactorsList n` (modulus `Q` = largest prime factor),
  concluding `D n - 1 <= 4*((n:ℤ)-1)`. Closes faithfulness-gap #1. Axioms
  `[propext, Classical.choice, Quot.sound]`, no `sorryAx`. Reuses `c53_le_4_per_n` verbatim.
  Honest note: `Q` = largest PRIME, not Grinsztajn's largest prime POWER `P(n)`; since
  largest-prime `<= P(n)` and both `>= 2`, `C_53 <= 4` is preserved. None of this moves
  `held` (still 4) — it is conditional infrastructure/faithfulness.
