# Certificates — 82a, essential minimum of the Zhang–Zagier height

This directory holds the re-runnable certificates behind the work on the essential
minimum `μ^ess(h_Z)` (Tao's constant 82a). The **upper-bound** work is the main
result; the lower-bound re-certification is recorded below it.

All programs print a `PASS`/`FAIL` verdict or a `CERTIFIED` value, use outward-directed
interval rounding, and reject a deliberately understated target (no grid fallback).
Run from this directory; the scientific Python stack (`numpy`, `scipy`, `mpmath`,
`sympy`) suffices.

---

## Upper bound — `μ^ess(h_Z) ≤ 0.2538893183`

A first-variation criterion for Doche's perturbed-polynomial construction, the
saturation theorem, and the improved record. Paper: `../upper_bound_paper.tex`.

### The record certificate

```
cd constants/82a/certificate
python3 bound_07_block_j9.py certify \
  14.011500 13.443930 2.643590 2.299880 0.252420 0 0 \
  0.575080 0.568800 0.891590 0.066860 200000 14 1e-10
# -> CERTIFIED  log h <= 0.2538893183   (frontier fully resolved, ~7 min)
```

### The bound chain (each block adjoined in turn)

The enriched Doche family is built one block at a time; setting a block's exponent to
zero recovers the previous certificate bit-identically (the `anchor` mode), so the
chain is a verified ladder up to the record.

| program | family / new block | certified `log h ≤` |
| --- | --- | --- |
| `bound_00_flammang_baseline.py` | Flammang lower-side interval machinery (shared) | — |
| `bound_01_doche_base.py` | Doche base `Q1·Q2`, `D=56` | `0.2543309112` |
| `bound_02_block_Qa.py` | `+ Qa` (deg 24) | `0.2543185491` |
| `bound_03_block_Qb.py` | `+ Qb` (deg 24) | `0.2542657872` |
| `bound_04_block_j13.py` | `+ Q5 = j13` (deg 12) | `0.2540639638` |
| `bound_05_block_j15.py` | `+ Q6 = j15` (deg 16) | `0.2540419719` |
| `bound_06_block_j3.py` | `+ j3` (deg 3, base branch) | `0.2538925359` |
| `bound_07_block_j9.py` | `+ j9` (deg 8, base branch) — **record** | `0.2538893183` |

(`bound_06a_block_j3_pre.py` is the pre-anchor variant of the `j3` step, kept for the
anchor cross-check.)

### The first-variation theory

| program | statement checked |
| --- | --- |
| `firstvar_01_lemma.py` | first-variation lemma: sign of `r_Q − log h` predicts fired/dry |
| `firstvar_02_hypotheses.py` | hypotheses (H1)–(H2): switching set finite, dominator `L¹` |
| `firstvar_03_unified.py` | unified one-sided marginal, all three regimes + tie kink |
| `firstvar_04_perturbing_marginal.py` | perturbing-branch marginal `m_B` vs finite difference |
| `firstvar_05_numerator_split.py` | exact active-set decomposition of the numerator |
| `firstvar_06_dictionary.py` | dictionary admissibility (pairwise coprime, squarefree) |

### Saturation (no admissible new block fires)

The design-objective searches and the potential-theoretic computations are in
`scratch/`: `R7_structural_result.py` (the maximal-firing-set obstruction — cheapest
coprime new factor `X²−X+1` costs `m=+0.013`), `design_block2.py` (~80k-candidate
enumeration, 0 firing originals), and `tfd_capacity2.py` (Robin constant `≈0.524`,
the not-an-equilibrium check).

---

## Lower bound — `μ^ess(h_Z) ≥ 0.24874` (Flammang, re-certified)

An independent, re-runnable interval branch-and-bound certificate of Flammang's record
[F18] (`log 1.282416 = 0.2487458`), not a float grid value.

```
python3 bound_00_flammang_baseline.py            # full rigorous certification (~30s)
python3 bound_00_flammang_baseline.py selftest   # soundness vs high-precision mpmath
```

Expected:
```
[OK] 24 polynomials Q_j: all INTEGER coefficients, all c_j > 0.
[OK] CERTIFIED  min_t g(t) >= 0.24874
     worst certified cell lower bound = 0.2487400...
     cells = 184444,  max depth = 9,  time = ~30s
```

Scalar cross-checks live in `scratch/`: `verify_flammang.py` (mpmath-interval
reference) and `verify_fast.py` / `fastiv.py` (fast float64-interval).
`scratch/verify_vec_energy.py` is the OSS log-energy lower-bound experiment.

### The rigor chain (re-derivable)

Auxiliary function, `w = z(1−z)`:
```
f(z) = log⁺|z| + log⁺|1−z| − Σ_j c_j log|Q_j(w)|,   c_j > 0,  Q_j ∈ Z[w].
```

1. Summing over the `d` conjugates `α_i` of `α`: `Σ_i f(α_i) ≥ m·d`, `m = min_z f`.
2. `⇒ log Z(α) ≥ m·d + Σ_j c_j log|∏_i Q_j(α_i(1−α_i))|`.
3. `∏_i Q_j(α_i(1−α_i)) = Res(P, Q_j(z(1−z)))` is an INTEGER; provided `P ∤ Q_j(z(1−z))`
   it is nonzero, so `|·| ≥ 1`, `log|·| ≥ 0`, and the `c_j`-terms drop out.
4. `⇒ h_Z(α) ≥ m` for every algebraic integer `α` whose minimal polynomial divides no
   `Q_j(z(1−z))`.

**Finite exception set E:** step 3 fails iff `P | Q_j(z(1−z))` for some `j`, i.e. `α`
is a root of some fixed nonzero `Q_j(z(1−z))`; `E = ∪_j {roots}` is finite. Since
`μ^ess` is defined by which sublevel sets are finite, a finite `E` cannot lower it:
for `H < m`, `{α : h_Z(α) ≤ H} ⊆ E` is finite, so `μ^ess ≥ m`.

**Reduction to `|z|=1`:** `f` is harmonic off small disks around the roots of the
`Q_j(z(1−z))`; by the maximum principle and `f(z)=f(1−z)`, minimize on `|z|=1`,
`z=e^{it}`, `0≤t≤π`, where `f|_C = g(t) = log⁺|w(t)| − Σ_j c_j log|Q_j(w(t))|`,
`w(t)=e^{it}−e^{2it}`.

**The rigorous minimum:** `bound_00_flammang_baseline.py` certifies
`min_{t∈[0,π]} g(t) ≥ 0.24874` by interval branch-and-bound, a guaranteed per-cell
2nd-order lower bound with outward rounding; the worst cell is `0.2487400`, minimizers
clustering near `t≈0.577`, clear of `E`. The certified `m=0.24874` sits `6.2e-6` below
the true minimum `0.2487462`.

---

## Files at a glance

- `bound_0*.py` — the upper-bound certificate ladder (run `bound_07_block_j9.py` for
  the record).
- `firstvar_0*.py` — the first-variation theory checks.
- `flammang_table1.py` — the 24 Flammang [F18] Table-1 integer polynomials `Q_j(w)`.
- `scratch/` — searches, probes, the saturation enumeration, the lower-side OSS
  experiment, and scalar cross-checks (the working record, not the certified set).
