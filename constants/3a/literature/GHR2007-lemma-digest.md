# GHR2007 — the load-bearing lemma (digest, R19)

Source: Gyarmati, Hennecart, Ruzsa, "Sums and differences of finite sets",
Funct. Approx. Comment. Math. 37(1):175–186, 2007.
PDF: `constants/3a/literature/pdfs/ghr2007.pdf` (extract via `pdfminer.high_level.extract_text`;
`pdf2txt.py` is NOT on PATH and the CLI binary streams empty — use the Python API).

## The Lemma (Section 2, inside the proof of Theorem 1) — the bridge every record uses

> **Lemma.** Let K > 1 be real and let U be a finite, non-empty set of non-negative integers
> containing 0. Set s = |2U| (= |U+U|), d = |U−U|, **q = 2·max(U)+1**, and
> **θ = 1 + log(d/s)/log q**. If d < q, then there exist pairs (A,B) of finite non-empty
> integer sets with |A| arbitrarily large such that |A+B| ≤ K|A| and |A−B| ≥ |A+B|^θ.

So a single finite U gives the lower bound **C_3a ≥ θ = 1 + log(|U−U|/|U+U|) / log(2·max(U)+1)**.
This is exactly the formula in `constants/3a.md` and the engine.

## The construction (how θ arises) — quoted/paraphrased from the proof

Fix k arbitrarily large. The lemma builds, in base q = 2·max(U)+1, the k-block digit set

    B = { Σ_{j=0}^{k−1} u_j q^j : u_j ∈ U,  j = 0,…,k−1 }     and    A = [1, …] (an interval).

Because q = 2·max(U)+1 > 2·max(U), the base-q addition/subtraction of two B-elements is
**carry-free**: the digit vectors (u_j ± u'_j) never overflow a base-q digit. Hence
  |B+B| = |U+U|^k = s^k     and     |B−B| = |U−U|^k = d^k.
The sumset/diffset of the *interval* A is controlled by |A| and K; the dominant growth is the
B-part, so asymptotically (k→∞)
  log|A−B| / log|A+B|  →  log(d) / log(s)   relative to the per-block normalization,
and the +1 / log q form arises because the relevant size scale is max(B) ≍ q^k, i.e.
log(scale) = k·log q. Collecting: θ = 1 + log(d/s)/log q. The condition d < q keeps the
difference-set digits inside one base-q block (no cross-block carries on the difference side).

**Carry-free ⇒ exact integer counts.** This is precisely why the digit-DP engine
(`certificate/engine/digit_dp.py::count_opset`) computes |U±U| exactly without enumerating
|U| ≈ |A|^d elements: the only cross-position coupling is the global digit-sum cap T.

## The upper bound 4/3 (Corollary 3, same paper)

> **Corollary 3.** If |A+B| ≤ K|A| then |A−B| ≤ |A+B|^{4/3}.
Hence θ ≤ 4/3 — the fixed upper bound in the table. (Movable side is the LOWER bound only.)

## The recorded 1.25 ceiling

`constants/3a.md` states the digit-set construction (this Lemma's U-route) "cannot exceed 1.25".
This is NOT re-derivable from Theorem 1/Corollary 3 directly (those give the 4/3 ceiling for
C_3a itself). Treat 1.25 as the repo's recorded ceiling on the *digit-set method's reach*, not a
bound on C_3a. The current frontier (1.1754) is well under it, so headroom remains.

## What is LOAD-BEARING vs ANALYTIC for a Lean cert

- **Discrete / Lean-checkable core:** the exact integers s=|U+U|, d=|U−U|, q−1=2·max(U), and the
  comparison θ ≥ c ⟺ d^Q ≥ s^Q·q^P (c−1 = P/Q). All big-int, all `decide`-able (verified R19).
- **Analytic bridge (the named trust boundary):** the Lemma's "θ ⇒ ∃ A,B with |A−B| ≥ |A+B|^θ
  and arbitrarily large" — the existence of the actual extremal sets and the limit. Mathlib has
  no C_3a object, so this is an honest named hypothesis (`GHR_lower_bound : ... → C_3a ≥ θ`),
  the analog of 9a's `ThetaGeFromIndep` and 5b's `MTThm15`. It is the trivial-to-state /
  hard-to-formalize step; keep it named, do NOT axiomatize the hard arithmetic into it.
