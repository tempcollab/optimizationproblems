# Approach `floorplus1-transversal-N30`

**Direction:** UPPER bound on C_5b. Target: a single indecomposable `N=30` (4,5)-set with
`h(A)=17`, giving `17/30 ≈ 0.5667 < 4/7 ≈ 0.5714286` (the first `N` where the
empirically-reachable `floor+1 = ⌈9N/17⌉+1` beats `4/7`).

**The obstacle this angle exists to solve:** certifying `h(A) ≤ m` for `N≈30` by the direct
route enumerates `C(30,17) ≈ 1.2·10⁸` subsets — far past kernel `decide`. The Lean-tractable
route is an **AP-transversal certificate**: bound `h(A) = N − τ` (τ = min transversal of the
3-AP hypergraph) by a cheap, `decide`-checkable hitting-set / matching certificate of cost
`O(|F|·N)`.

## Status (R3): MACHINERY BUILT + VALIDATED (sound, reusable) — but the fractional version is not tight

This round delivered the load-bearing **transversal soundness lemma**, fully proven in Lean
(`lean/Constants/C5bTransversal.lean`, namespace `C5bTransversal`), zero `sorry` / zero
smuggled axioms, and validated end-to-end on the record gadget `A_base`.

### What compiled (verified, `lake build Constants.C5bTransversal` PASS)

- `hLe_of_fracMatching` — **soundness lemma**: from a fractional-matching certificate
  (`edgesOK`: every listed edge a genuine 3-AP inside `A`; `loadOK`: every vertex load `≤ D`;
  `D*(N−m−1) < totalW`) it proves every sublist of `A` avoiding all listed APs has length
  `≤ m`. Cost `O(|F|·N)`. Proof = list double-counting (`totalW_le_loadSum`) +
  cardinality split. No `sorry`, no axiom beyond `propext, Classical.choice, Quot.sound`.
- Validation `Abase_avoiders_le_9`: a `decide`-checked certificate `Fcert_base` (12 APs of
  `A_base`, `D=6`, `T=27`, `ν*=4.5`) fires the lemma to certify `h(A_base) ≤ 9` by the
  transversal route — zero axioms on the `decide` facts.
- Re-runnable numerical check: `constants/5b/certificate/transversal/check_transversal_cert.py`
  (reproduces the 12 APs, the certificate, the soundness arithmetic, and the gap).

### Value claimed this round

- **Claim (machinery, verified):** a reusable, zero-axiom Lean **transversal soundness
  lemma** that certifies `h(A) ≤ m` at cost `O(|F|·N)` instead of `C(N,m+1)`, for ANY
  point list `A` and any fractional-matching certificate. Validated on `A_base`.
- **No bound improvement** this round (still `held = 4/7`, not beaten). The machinery is the
  prerequisite for the `N=30` beat, not the beat itself.

## The honest blocker found this round: the fractional matching is NOT tight on A_base

Key empirical finding (verified, in the checker): A_base's 3-AP hypergraph has an
**integrality gap**. The exact min transversal is `τ = 6` (so the tight value is
`h(A_base) = N − τ = 8`), but the **LP optimum** of the fractional matching is only
`ν* = 4.5` (exact — re-verified by `linprog`). So pure LP-duality certifies only `τ ≥ 5`,
i.e. `h(A_base) ≤ 9` — **one short of the tight `h ≤ 8`**.

Consequence: the *fractional*-matching certificate format, while sound and `O(|F|·N)`, can
**under-certify** by the integrality gap. For the `N=30` gadget the gap may or may not bite;
it must be checked. If the target hypergraph also has `ν* < τ`, the fractional lemma alone
will not reach `h ≤ 16`.

## Concretely what would push it further (next sub-goals, in priority order)

1. **Close the integrality gap — an INTEGRAL transversal certificate (high priority).**
   Strengthen `hLe_of_fracMatching` to a certificate that reaches the integral `τ`, still
   cheaply checkable:
   - *Branching certificate:* a small decision tree "vertex `v` in the transversal (cost 1,
     recurse on `H−v`) OR `v` out (every AP through `v` hit by its other two vertices)".
     Tight (= branch-and-bound), `decide`-checkable, size = tree nodes (small for A_base).
     Formalize as a structurally-recursive `Bool` predicate + a soundness lemma `τ ≥ k`.
   - *Odd-set / blossom inequality:* add LP constraints `Σ_{e⊆U} w_e ≤ ⌊|U|/2⌋`-style to the
     matching; lifts `ν*` toward `τ` on gap instances. Heavier to formalize.
   The branching route is the cleaner one-round increment; deliver it validated on `A_base`
   (must reach the tight `h ≤ 8` there to prove it closes the gap).
2. **The `N=30` gadget search (off-Lean, exact α).** Search for a 30-point (4,5)-set
   (difference condition!) with `h=17`, indecomposable (no well-separated 2-block split,
   Lemma 3.6). Reuse R2's exact branch-and-bound α machinery; seed from non-A_base regions.
   Then build its transversal certificate with the integral machinery from (1).
3. **Wire to the corrected engine.** The sibling's `engine-is45set-difference-fix` (R3) added
   the decidable `is45setB` (difference condition) to `C5b.lean`. A future `N=30` gadget
   certificate must use `is45setB` for the (4,5)-property AND the transversal lemma here for
   the `h`-bound — the two compose into a sub-4/7 Lean certificate.

## Why this is the right machinery despite the gap

The transversal route is the ONLY Lean path to `h`-certification at `N≥21` (`C(30,17)` is
hopeless for raw `decide`). The fractional lemma is the correct, reusable core; the
integrality-gap finding is exactly the kind of concrete obstacle that scopes the next round
(build the integral/branching strengthening, validate it reaches the tight bound on A_base,
then certify the N=30 gadget once the search finds it).

## Files

- `lean/Constants/C5bTransversal.lean` — the machinery + A_base validation (compiles, no
  `sorry`, axioms `{propext, Classical.choice, Quot.sound}` only).
- `constants/5b/certificate/transversal/README.md` — reviewer reproduction instructions.
- `constants/5b/certificate/transversal/check_transversal_cert.py` — numerical re-check.

## Source

Ma & Tang, arXiv:2602.23282 (Feb 2026) [MT26], Lemma 2.3 (Sidon ⟺ no 3-AP), Theorem 1.5
(c* = inf_n f(n)/n), Lemma 3.6 (indecomposability). LP-duality hitting-set bound: standard.
