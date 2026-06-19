# theta-cover-dual — fire Borsuk with theta(G_d) > ceil(v/omega), not ceil(v/5)

**NEW sketch (round 4); advanced round 4.** The one un-mined crack from the
round-4 survey (`literature/off-g24-sources.md` §3). Distinct from all five
existing sketches: every one of them assumes the part count is the WEAK bound
`theta = ceil(n/omega) = ceil(n/5)`, which forces `n >= 316`. This sketch fires
on the STRONGER quantity `theta(G_d) = chi(G_d)` via the vertex-transitive
fractional-chromatic pin.

## The lever
Musin's exact criterion (arXiv:2511.03668): a two-distance set is a Borsuk
counterexample iff `theta(G_d) + mu(G_d) > n`, where `theta(G_d) = chi(G_d)` is
the number of Borsuk parts and embedding dim `= n - mu - 1`. We fire on
`chi(G_d) >= chi_f(G_d) = |X|/alpha(G_d)` EXACT for vertex-transitive `G_d` (a
genuine lower bound on `chi`, a true theorem). Firing needs
`alpha(G_d) <= need_omega(v)` (= largest `w` with `ceil(v/w) >= 64`) in some
orientation, at embedding dim `<= 62`.

## KEY ARITHMETIC FACT clarified round 4 (sharpens the target)
For the *firing test* `chi(G_d) > d+1`, the fractional bound `chi_f = |X|/alpha`
is EQUIVALENT to `ceil(|X|/alpha) > d+1` (both say `|X|/alpha > d+1`). So the
vertex-transitive pin does NOT buy extra firing power over `ceil(v/omega)` —
**what it buys is EXACTNESS**: for a vertex-transitive graph the parameter-only
Delsarte-Hoffman upper bound `omega_DH` (used by srg-sweep) is replaced by the
TRUE `alpha`, settling rows the parameter-only sweep left OPEN. The escape from
the 316-wall is genuinely `alpha < 5` (alpha=4 needs `|X|>252`, alpha=3 `>189`),
NOT a fractional gain at alpha=5 (`|X|/5 > 63` still needs `|X|>=316`).

## What round 4 CLOSED (both holes, for the named existence-confirmed families)
The srg-sweep left **207 parameter rows OPEN** under the *parameter-only* `omega_DH`
test; **17 of them are existence-confirmed** (`ex='+'`, `f<=62`) — an explicit
vertex-transitive two-distance graph actually exists, so its TRUE clique number
can be tested. These 17 ARE exactly the families (a)/(c) this sketch's Hole 1
names. Round 4 settled **14 of them EXACTLY**, all NON-firing:

- **13 Steiner block-intersection rows** `S(2,3,n)` (n=37,39,43,45,49,51,55,57,
  61,63) and `S(2,4,n)` (n=49,52,61). Settled by CLOSED-FORM clique LOWER bounds
  (no construction needed):
  - `omega(A) >= r := (n-1)/(k-1)` — the `r` blocks through a fixed point pairwise
    meet there (PENCIL clique).
  - `omega(A-bar) >= ceil(r/k)` — max partial parallel class. RIGOROUS maximality
    argument: a maximal disjoint-block set `M` (|M|=m, covers `U`, |U|=mk) is met
    by every block (else extend); the `r` blocks through an uncovered point hit
    `r` DISTINCT points of `U` (Steiner: two blocks meet in <=1 pt), so `r <= mk`,
    i.e. `m >= r/k`.
  - BOTH exceed `need_omega(v)` for every `n <= 63`, so neither spherical
    orientation fires. Closed-form reason: A-orient needs `r <= v/64`, i.e.
    `n >= 64k` (>=192 for k=3, >=256 for k=4), but `f<=62` caps `n<=63`.
- **Cameron graph srg(231,30,9,3)** (M22-transitive): built EXACTLY from the
  Golay code → Witt `S(5,8,24)` → `S(3,6,22)` → Cameron graph (in
  `theta_designs.py`, network-free). `omega(A)=7` exact (g24.max_clique_le bitset
  b&b, matches Brouwer), greedy `alpha(A) >= 17` (Hoffman-exact 21). Both `> 3 =
  need_omega(231)` → does not fire.

Implemented in `theta-cover-dual.py`: `need_omega`, `fires_on` (the exact chi_f
firing test), `steiner_clique_lower_bounds`, `resolve_steiner_family`,
`resolve_cameron`, `resolve_named_families` (asserts `any_fire=False`). Runs green,
exit 0, `fired=False`.

## What REMAINS OPEN (the genuine discovery; honest residual hole)
`build_candidate_graph` still raises `NotImplementedError`. The residual target:
- **family (b):** a NEW off-SRG-table vertex-transitive two-distance set (Cayley
  two-distance graph on a group of order `<316`, rep dim `<=62`) with
  `min(omega(A),omega(A-bar)) <= need_omega(v)`. No such object is known.
- the **3 remaining dense 2-graph rows** (v=220 Tonchev quasisymmetric, v=276
  Conway-Goethals-Seidel, v=344) — both the graph and its complement are dense
  (`k≈v/2`), so both `omega` are expected LARGE; their exact clique numbers are
  not yet computed here (construction + exact clique on ~300-vertex dense graphs).
  Left as a precisely-scoped residual, NOT claimed.

## Why a firing object looks unlikely (not a proof — context)
The true point/clique ratio `v/alpha` of every settled row is far below 64
(Cameron `231/7=33`; Steiner rows smaller). G_2(4)'s `416/5=83.2` remains the
densest known ratio, and it only clears 64 at `>=316` points. The survey found no
off-G_2(4) small-omega source. So a sub-316 firing object would be a genuinely new
discovery; this round provides no such object.

## Status — claim
**NO bound.** Upper bound stays **63** (record, Gri2026); we have only verified a
CLEAN NEGATIVE on 14 named vertex-transitive families (no firing). This is an
informativeness advance, not a record-break. Nothing written to `current.md`
(`held` stays 63). **Claimed value: upper bound 63 (= table; NOT beaten).**

## Borrows
- `g24.max_clique_le` (exact-omega bitset) — exact `omega(A)` of Cameron.
- `theta_designs.py` (NEW, this round) — Steiner/Golay/Witt/Cameron constructors,
  exact & self-verifying, reusable by other sketches.
- `fresh-orthogonal-dir.exact_rank` — exact embedding dim (imported, used by
  `embedding_dim_exact`).

## Promotable lemmas
See the report; `steiner_clique_lower_bounds` (the pencil + partial-parallel-class
clique lower bounds for S(2,k,n) block graphs) is a clean reusable combinatorial
fact, but it is sketch-glue-sized; the reviewer may judge it below the cache bar.
The `theta_designs.py` Cameron/Witt constructors are reusable scaffold (like g24)
rather than a lemma.

## Certify
**Lean-fit** if a firing graph ever lands: the dual `w` is a finite rational
vector, `alpha` an exact bitset clique, embedding dim an exact rank. The closed
sub-cases are already Lean-shaped (closed-form integer clique bounds; exact bitset
clique for Cameron). First construction to land bootstraps `constants/28a/lean/`.
