# C_3a exact carry-free digit-DP count engine (record baseline)

This folder is the **search-immune machinery backbone** for C_3a (Gyarmati–Hennecart–Ruzsa
sum-difference constant), analogous to the 9a-367 Lean baseline. It is a **baseline, not a
beat**: it reproduces the current record lower bound `C_3a ≥ 1.1740744` exactly (gap 0). It is
the reusable exact-arithmetic engine that the parameter-sweep angle (and a later Lean cert)
calls.

## The bound

GHR2007 lemma: for any finite `U ⊆ ℤ≥0` with `0 ∈ U`,
```
C_3a ≥ 1 + log(|U−U| / |U+U|) / log(2·max(U)+1).
```
The record `U` is the base-`B` digit set
```
U(A,B,d,T) = { Σ_{i=0}^{d−1} a_i·B^i : a_i ∈ A, Σ a_i ≤ T },
A = {0,2,3,4,5,6,7,8,9,10},  B = 21,  d = 80,  T = 150.
```

## The load-bearing structure (verified, not assumed)

Because `B = 21 > 2·max(A) = 20`, addition/subtraction of two `U`-elements is **carry-free**:
- each `u ∈ U` has a unique base-`B` digit vector `(a_0..a_{d−1})`, `a_i ∈ A`;
- `u+v` has digit vector `(a_i+b_i)` over `A+A` (every entry `< B`, no carry);
- `u−v` has signed digit vector `(a_i−b_i)` over `A−A` (unique signed representation);
- the ONLY coupling across positions is the global digit-sum cap `Σ a_i ≤ T` (and the same
  for the other addend). Without the cap, `|U±U|` factors exactly as `|A±A|^d`
  (`selftest.py` confirms `|U+U| = 20^d`, `|U−U| = 21^d` with the cap removed).

So `|U+U|` = number of distinct **achievable** output digit vectors `c`, where `c` is
achievable iff there is a per-position split `c_i = a_i (op) b_i` (`a_i,b_i ∈ A`) with
`Σ a_i ≤ T` AND `Σ b_i ≤ T` simultaneously.

**Key simplification that makes the DP fast (load-bearing observation).** For a fixed output
vector with sums `Sa = Σ a_i`, `Sb = Σ b_i`, `Sc = Σ c_i`:
- sumset (`op = +`): `a_i+b_i = c_i ⇒ Sa+Sb = Sc`, so `Sb = Sc − Sa`;
- difference (`op = −`): `a_i−b_i = c_i ⇒ Sa−Sb = Sc`, so `Sb = Sa − Sc`.

Hence achievability needs only a reachable `Sa`:
- `+` : `Sa ≤ T` and `Sc − Sa ≤ T` ⇔ **max** reachable `Sa ≥ Sc − T`;
- `−` : `Sa ≤ T` and `Sa − Sc ≤ T` ⇔ **min** reachable `Sa ≤ T + Sc`.

The DP therefore tracks, per output prefix, the reachable `Sa` info plus the running `Sc`:
- **sumset** keeps the EXACT reachable-`Sa` set as a bitmask (boundary gaps are real — e.g.
  `Sa = 1` is unreachable since `1 ∉ A` — so the full mask is required for soundness);
- **difference** needs only the **min** reachable `Sa`, which transitions deterministically
  (`minSa += min(a-options of c)`), so its state is `(minSa, Sc)` — small and fast.

`max(U)` is a greedy top-down fill with the **largest alphabet digit ≤ remaining budget**
(optimal because `B > max(A)+1`; only digits actually in `A` are used).

## Files

| file | purpose |
| ---- | ------- |
| `digit_dp.py` | the engine: `count_opset`, `max_U`, value + certificate helpers |
| `run_record.py` | computes one of `N+`/`N−`/`max(U)` for the record, writes `record_*.txt` |
| `record_plus.txt` / `record_minus.txt` / `record_max.txt` | the exact record integers |
| `selftest.py` | DP-vs-brute cross-checks + no-cap factorization + record reproduction |
| `certify_record.py` | rigorous **directed-rounded** lower bound from the exact integers |

## Engine API (for the sibling sweep / next round)

```python
from digit_dp import count_opset, max_U, certifies_at_least, value_str

# Exact |U op U| in the carry-free regime (op = '+' or '-'). Requires B > 2*max(A).
# Returns an exact Python int. B does NOT enter the count (carry-free); pass via max_U only.
N_plus  = count_opset(A, d, T, '+')
N_minus = count_opset(A, d, T, '-')
M       = max_U(A, B, d, T)          # exact int

# Exact (no-float) integer-power certificate of  value >= c  (c a Fraction):
#   value >= c  <=>  N_minus^q >= N_plus^q * (2M+1)^p,  where  c-1 = p/q  in lowest terms.
# CHEAP only when q (= denominator of c-1) is small -> use for a FOUND BEAT (q ~ 40..155),
# NOT for the razor-thin record (q ~ 1.25e6, infeasible).
ok = certifies_at_least(N_plus, N_minus, M, Fraction(1175, 1000))
```

`count_opset` cost: sumset ~60 s, difference ~30 s at the record `(d=80, T=150, |A|=10)`;
both polynomial in `d·T` (no enumeration). Always call under a `timeout`.

## Reproduce

```bash
cd constants/3a/certificate/engine
python3 run_record.py plus        # writes record_plus.txt   (~60 s)
python3 run_record.py minus       # writes record_minus.txt  (~30 s)
python3 run_record.py max         # writes record_max.txt    (instant)
python3 selftest.py               # DP==brute on small cases + record reproduction (~60 s)
python3 certify_record.py         # rigorous directed-rounded lower bound (~2 s)
```

## Exact record counts (reproduced bit-for-bit vs PR #71)

```
N+ = |U+U| = 75448362167176243488362019935078206851619643198150854886920234689186981134888   (77 digits)
N- = |U-U| = 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415   (96 digits)
M  = max(U)= 2995805288150731620410662946668903948341032736664352641511848666717243994160370658179324073879212562136150   (106 digits)
```

## Value (directed-rounded, rigorous)

```
1 + log(N-/N+)/log(2M+1) = 1.174074447693521163363531806658755676...   (matches PR #71)
guaranteed lower bound (mpmath interval, outward rounding) > 1.1740744  ✓  (margin ~4.77e-8)
```

So **C_3a ≥ 1.1740744** is reproduced exactly. This is the baseline (gap 0, NOT a beat).

## Why no Lean certificate of the record this round

Rationalizing `value ≥ 1.1740744` to the pure integer inequality `N-^q ≥ N+^q·(2M+1)^p`
needs `q = denominator((c−1))`. For the conservative ledger value `c = 1.1740744`,
`c−1 = 217593/1250000` so `q = 1 250 000`, making `N-^q` a ~1.2·10^8-digit integer — a
`decide`/`norm_num` of that size is infeasible. (The outline-reviewer flagged this.) The
cheap Lean integer-inequality cert is reserved for a **found beat** with a fatter margin
(`q ≈ 40..155`), a later sub-goal. The engine's `certifies_at_least` already implements that
integer-power check, verified on small cases, ready for a beat.
