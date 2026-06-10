# Certificate — 82a lower bound (Flammang record re-certified)

**Claim certified:** `C_82 = ess.min h_Z  >=  0.24874`
for all algebraic integers outside a fixed FINITE exceptional set (below).
This rigorously re-establishes Flammang's record [F18] (log 1.282416 = 0.2487458)
with an independent, re-runnable interval branch-and-bound certificate — not a
float grid value.

## Reproduce

```
cd constants/82a/certificate
python3 verify_vec.py            # full rigorous certification (~30s)
python3 verify_vec.py selftest   # soundness check vs high-precision mpmath
```

Expected output of `verify_vec.py`:
```
[OK] 24 polynomials Q_j: all INTEGER coefficients, all c_j > 0.
[OK] CERTIFIED  min_t g(t) >= 0.24874
     worst certified cell lower bound = 0.2487400...
     cells = 184444,  max depth = 9,  time = ~30s
==> C_82 >= 0.24874 ...
```

There is also a scalar reference implementation `verify_flammang.py` (mpmath
verified-interval arithmetic, same bound, slower) and a single-precision-but-fast
scalar version `verify_fast.py`; `verify_vec.py` is the vectorized production
certifier and agrees with both to machine precision (see selftest).

## Files
- `flammang_table1.py` — the 24 integer polynomials Q_j(w) and coefficients c_j,
  transcribed from Flammang [F18] Table 1; loader asserts every Q_j ∈ Z[w].
- `verify_vec.py` — vectorized rigorous certifier (run this). `selftest` mode
  checks the interval lower bound never exceeds the true g on 400 random cells.
- `verify_flammang.py` — scalar mpmath-interval reference certifier (cross-check).
- `verify_fast.py` / `fastiv.py` — scalar fast float64-interval version (cross-check).
- `stageB_colgen.py` — Stage B column-generation break attempt (negative result;
  see ../approaches/lp-column-generation.md).

## The rigor chain (re-derivable)

Auxiliary function, w = z(1-z):
  f(z) = log max(1,|z|) + log max(1,|1-z|) - Σ_j c_j log|Q_j(w)|,  c_j>0, Q_j∈Z[w].

1. Σ over the d conjugates α_i of α:  Σ_i f(α_i) ≥ m·d,  m = min_z f(z).
2. ⇒ log Z(α) ≥ m·d + Σ_j c_j log|∏_i Q_j(α_i(1-α_i))|.
3. ∏_i Q_j(α_i(1-α_i)) = Res(P, Q_j(z(1-z))) is an INTEGER (det of an integer
   Sylvester matrix). PROVIDED P ∤ Q_j(z(1-z)) it is NONZERO, so |·|≥1,
   log|·|≥0, and the c_j-terms DROP OUT.
4. ⇒ h_Z(α) = (1/d) log Z(α) ≥ m  for every algebraic integer α whose minimal
   polynomial divides none of the Q_j(z(1-z)).

**Finite exception set E** (load-bearing): step 3 fails iff P | Q_j(z(1-z)) for
some j, i.e. α is a root of some Q_j(z(1-z)). Each Q_j(z(1-z)) is a fixed nonzero
polynomial with finitely many roots; E = ∪_j {roots of Q_j(z(1-z))} is FINITE.
The bound h_Z(α) ≥ m holds for all algebraic integers α ∉ E. Flammang writes E as
the roots of (z²-z)(z²-z+1)φ₁₀(z)φ₁₀(1-z).

**Why E does not lower C_82:** C_82 = sup{H : {α : h_Z(α) ≤ H} finite}. If
h_Z(α) ≥ m off the finite set E, then for any H < m, {α : h_Z(α) ≤ H} ⊆ E is
finite, so every H < m is admissible and C_82 ≥ m. A finite set cannot change
which sublevel sets are finite.

**Reduction to the unit circle:** f is harmonic off small disks around the roots
of the Q_j(z(1-z)); by the maximum principle min f over the lens {|z|≤1}∩{|1-z|≤1}
is on the boundary |z|=1 or |1-z|=1. f(z)=f(1-z) (z↦1-z fixes w, swaps circles),
so minimize on |z|=1, z=e^{it}, 0≤t≤π. There log max(1,|z|)=0 and |1-z|=|w|, so
f|_C = g(t) = log max(1,|w(t)|) − Σ_j c_j log|Q_j(w(t))|, w(t)=e^{it}−e^{2it}.

**The rigorous minimum (the closed hard step):** `verify_vec.py` certifies
min_{t∈[0,π]} g(t) ≥ 0.24874 by interval branch-and-bound. On each t-cell it
computes a GUARANTEED lower bound of g via a 2nd-order Taylor (mean-value) model
of each ρ_j(t)=|Q_j(w(t))|² (quadratic convergence in cell width), using only an
UPPER bound on |Q_j|² — finite even at the Q_j-zero singularities (where −c_j log|Q_j|
→+∞ and only HELPS), so the enclosure never blows up. All arithmetic uses
outward-directed rounding (np.nextafter / mpmath.iv). The certified worst-cell
bound is 0.2487400, the active minimizers cluster near t≈0.577 and across the
flat band t∈[0.5,1.5] (the LP-optimal near-equioscillation), all clear of the
finite exception points. The certified m = 0.24874 sits 6.2e-6 below the true
minimum 0.2487462, so the bound is valid with margin.
