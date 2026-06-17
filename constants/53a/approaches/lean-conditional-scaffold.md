# Approach: lean-conditional-scaffold

**Constant:** 53a — Davenport constant of `C_n^3`,
`C_53 = sup_{n>=2} (D(C_n^3)-1)/(n-1)`, repo bounds `3 <= C_53 <= 4`.
**Moves:** upper bound (re-derives, does NOT beat, `C_53 <= 4`).
**Type:** Lean-fit certificate scaffold. This is INFRASTRUCTURE, not a bound improvement.

## Idea

Formalize, as `lake build`-checked Lean 4, the load-bearing algebraic core of Grinsztajn's
upper bound `D(C_n^3) <= 4n - P(n) - 2` (=> `C_53 <= 4`), 2026
(https://github.com/maaxgrin/davenport-cn3-bound). Grinsztajn's own deduction ships as a
*conditional* Lean formalization that axiomatizes the zero-sum number-theory inputs; we mirror
that, but carry those inputs as explicit **hypotheses** (not axioms) so the conditional
boundary is visible and `#print axioms` shows no smuggled problem-specific axiom.

The single buildable sub-goal this round: the **integer recursion step** of the global
factorization induction, plus its load-bearing **comparison inequality**.

## What COMPILED this round (round 2)

File: `lean/Constants/C53a.lean`. Build target: `Constants` (in `lean/lakefile.toml`).
`lake build Constants` completes green against pinned Lean v4.31.0 / Mathlib
`fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`.

Theorems, all fully proved (no `sorry`):

- **`comparison_ineq`** (the load-bearing algebra):
  `2 <= p -> p <= Q -> p^2 - 2*p + 2 <= (p-1)*Q`  over ℤ.
  Mechanism: `(p-1)*Q >= (p-1)*p = p^2 - p` and `p^2 - p - (p^2-2p+2) = p-2 >= 0`.
  Proof: `nlinarith [mul_le_mul_of_nonneg_left hpQ ...]`.
- **`recursion_step`** (the inductive step, conditional):
  given `hstep : D(p*m) <= p*D(m) + p^2` (= Lemma 2.1 inductive method + Lemma 2.3 local
  estimate — the axiomatized zero-sum inputs, carried as a hypothesis) and the induction
  hypothesis `hm : D(m) <= 4*m - Q - 2`, with `2 <= p <= Q`, conclude
  `D(p*m) <= 4*(p*m) - Q - 2`. The derivation
  `p*D(m)+p^2 <= p*(4m-Q-2)+p^2 = 4pm - pQ - 2p + p^2 <= 4pm - Q - 2`
  (last `<=` is exactly `comparison_ineq`) is fully proved.
- **`base_in_form`**: the prime-power base case `D(C_Q^3) = 3Q-2` rewritten as `<= 4Q-Q-2`.

Axiom audit (`constants/53a/certificate/axioms.txt`):
`recursion_step` and `comparison_ineq` each depend on exactly
`[propext, Classical.choice, Quot.sound]` — the three Lean foundational axioms only.
**No `sorryAx`. No problem-specific axiom.** The hard step (the comparison inequality) is
inside the formalization and genuinely proved; the zero-sum facts are hypotheses, not axioms.

## The exact load-bearing lemma proved

`comparison_ineq (p Q : ℤ) (hp : 2 <= p) (hpQ : p <= Q) : p^2 - 2*p + 2 <= (p-1)*Q`

This is the single inequality that makes Grinsztajn's clean closed form `4pm - Q - 2` follow
from the additive `p^2` recursion. It is the "finite/algebraic" core the outline named.

## Certificate

Lean-fit. Reproduce with (see `constants/53a/certificate/README.md`):
```sh
export PATH="$HOME/.elan/bin:$PATH"
cd /home/agentuser/repo/lean
lake exe cache get        # one-time, fetches pinned Mathlib oleans
lake build Constants      # THE check
```

## Why this does NOT beat 4 (and that is expected)

`C_53 <= 4` is pinned by the leading coefficient `c = 3` of the eta-bound
`eta(C_p^3) <= 3p^2 - 4p - 3` (Bhowmik-Schlage-Puchta 2017), which enters Lemma 2.3 as the
`+p^2` additive term. The sup is carried by `n = p*q` with two large primes; only an
unconditional sub-`3p^2` eta-bound for all large p moves it (open — see
`eta-coefficient-barrier.md`). This scaffold re-derives 4 conditionally and is the seed any
future eta-win plugs into. **The `held` value is unchanged.**

## What is carried FORWARD (next rounds)

1. **Global factorization induction.** Lift `recursion_step` to the full induction over the
   prime multiset of `n` (`n = Q * p_1 * ... * p_s`, each `p_i <= Q = P(n)`), giving
   `D(C_n^3) <= 4n - P(n) - 2` for all `n >= 2`, then the `C_53 <= 4` corollary. Needs an
   induction over a `Multiset`/`List` of prime factors with `base_in_form` as base and
   `recursion_step` as step — pure Lean bookkeeping, no new math.
2. **Faithful statement of the eta input.** Replace the bare `hstep` hypothesis by deriving
   it inside Lean from named `Lemma 2.2` (extraction `D_k <= M + e(k-j)`) and `Lemma 2.3`
   (`D_k(C_p^3) <= p*k + p^2`) hypotheses, so the dependence on `eta(C_p^3) <= c*p^2` is
   syntactically exposed.
3. **The eta-coefficient lever (the only thing that beats 4).** State and prove in Lean the
   conditional `(forall large p, eta(C_p^3) <= c*p^2) => C_53 <= 3 + c/3`. Plugging an
   unconditional `c < 3` here is the single knob — and the research wall (see
   `eta-coefficient-barrier.md`).
