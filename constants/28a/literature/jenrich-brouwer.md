# Jenrich–Brouwer 2014 — A 64-dimensional counterexample (arXiv:1308.0206)

Two versions: the EJC 4.29 short paper (Jenrich+Brouwer, no big computation) and the longer arXiv preprint (Jenrich, with the Pascal program G24CHK). PDF/txt saved under `pdfs/1308.0206.{pdf,txt}`. The long arXiv version is the most useful — it contains the **63-dim "almost-counterexample"** that Gri2026 later fixed.

## Result
`d_B <= 64`. The set `{y_i : i ∈ C ∪ B1}` of **352** vectors lies in a **64-dim** subspace; with `ω(G_2(4))=5`, needs `>= ceil(352/5) = 71 > 65 = 64+1` parts. (Bondarenko's remark: actually `>=72`.) **Margin 6 parts** — much looser than Gri2026's 1.

## Construction
- Uses `y_i = (A − sI)` columns, `s=−4`: `y_{ii}=4`, `y_{ij}=1` (adjacent), `0` (non-adjacent). `‖y_i−y_j‖^2 = 144`/`192`. Rank `f=65`. Same two-distance set as Bondarenko, different (integer) normalization.
- Same partition `B = {vertices containing isotropic pt #1}` → `B1,B2,B3` (32 each) + `C` (320). Degree facts identical to Gri's Lemma 1.
- **Dim drop 65→64.** Vector `p` with `p_j = +1` on `B2`, `−1` on `B3`, else 0. Then `⟨p,y_i⟩ = 0` for `i∈C∪B1`, `=±24` for `i∈B2∪B3`. So `p ⟂ {y_i : i∈C∪B1}` but not to all — `dim{y_i:i∈C∪B1} <= 64` (and `=64`).

## The crucial Section 8 — "a 63-dimensional ALMOST-counterexample"
- Vector `q`: `q_j = 2` on `B1`, `−1` on `B2∪B3`, else 0. `⟨q,y_i⟩ = 0` for `i∈C`, `=48`(B1)/`−24`(B2,B3). So `q ⟂ {y_i : i∈C}` ⇒ **`dim{y_i : i∈C} <= 63` (and exactly 63)**. (Re-verified numerically: rank is exactly 63.)
- BUT `|C| = 320` only, and **Jenrich explicitly partitions `C` into 64 5-cliques** ⇒ `{y_i:i∈C}` splits into 64 smaller-diameter parts. `64 = 63+1`, so this is **NOT** a counterexample. This is the exact wall.
- **This is the gap Gri2026 exploited:** the 320 C-points sit perfectly in 63 dims but `ceil(320/5)=64` is one short of beating `63+1=64`. Gri adds **one** projected point `p=t·z_b` to make 321 ⇒ `ceil(321/5)=65 > 64`. The whole 63→ improvement is "one extra point in the already-63-dim C-set."

## Why this scopes the dim-62 attack
- The 320 C-points span **exactly 63 dims** (verified). To reach dim 62 you must put `>=316` points (`ceil(316/5)=64 > 62+1=63`) into a **62-dim** subspace with max-part still 5. You cannot just project C: I checked the C-points are in general position w.r.t. every hyperplane (smallest singular values all equal ≈19.6; no hyperplane holds more than a handful exactly). There is **no free dimension to drop** the way there was at 64→63.
