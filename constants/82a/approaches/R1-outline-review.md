# Outline review — z-variable-columns.md (C_82a LOWER bound, round 1)

**Verdict: NEEDS REVISION** (the retraction is sound and must proceed; the forward
Angle 1 is *valid and non-dead-end* but its headroom is overstated — its two
sub-levers collapse to ONE unscreened gamble, and the honest expected outcome of
the round is **"retract + likely no forward gain yet."**)

Reviewer: outline-reviewer. All claims below were re-derived independently
(numpy/scipy/sympy), not taken on the outline's word.

---

## A) The retraction reasoning — CORRECT and SUFFICIENT. Proceed.

I independently confirmed both structural failures of the OSS certificate
(`verify_vec_energy.py`) and that the bound `sum_i f(alpha_i) >= d * min_plane f`
is what the method actually proves (the "locus reduction" is only a cheap *way to
compute* `min_plane f`, valid iff the global plane min sits on the circles).

1. **Wrong min-locus is decisive on its own.** For pure Flammang `f0`, the global
   plane minimum (grid) is 0.24876 attained at `|z|=0.99991` — essentially ON
   `|z|=1`; circle min 0.24875. The locus reduction is honest for `f0`. The OSS
   energy term `-2 lambda0 U_mu0` is superharmonic (R1: plane min ~ -0.06 near
   `|z|~1.38`, OUTSIDE the lens, where nu actually lives). So `min_plane f << 0.2487`
   and the certified 0.2524 is a wrong-locus artifact. **This reason alone retracts.**
2. **`I(nu) >= 0` independently fails.** `h_Z` is defined for all algebraic numbers
   (82a.md includes `(1/n)log|a|`), so the leading coeff `a` can exceed 1;
   `I(nu) = (1/d^2)[log|disc P| - (2d-2)log|a|]` can be negative, so the OSS column is
   not a valid `>=0` column for ZZ. Confirmed; matches the user's no-go directive.

**Salvage check (the outline did not need to, but I did):** certifying OSS honestly
on the locus where nu lives gives `<= -0.06 < 0.2487` — *below* Flammang — and the
column is mis-signed anyway. There is **no salvage** at the frozen `lambda0`, and
re-optimizing `lambda0 -> 0` just returns Flammang. **OSS is dead; do not revisit.**

**Action stands:** retract R14/R15/R17, reset held lower to 0.2487458 [F18], set
lower-side `Status: none`. Upper 0.2540419719 [R11] is independent and stands.

---

## B) The forward attack (Angle 1) — VALID but headroom overstated.

### B.1 — Is the both-circle certificate the CORRECT honest locus for z-columns? **YES.**
This was the load-bearing question and the outline gets it right, for the right reason.
A z-column `-d_k log|R_k(z)|`, `R_k in Z[z]`, `d_k>=0`, is **harmonic off the zeros of
`R_k`** (superharmonic in the lens, +inf at zeros) — structurally identical to
Flammang's `-c_j log|Q_j(w)|` and UNLIKE the superharmonic OSS potential. I verified
directly: with a z-column added (`R=z^3-z+1`, several weights `d`), the global plane
min stays ON the circle `|1-z|=1` (argmin has `|1-z|=1.000` to 3 digits) and
`both_circle_min ~= plane_min` to 1e-5. **The z-column min does NOT escape the lens
the way OSS did — the both-circle locus IS honest for z-columns.** The exact OSS
failure mode (mass off the certified locus) does **not** recur here. HS-B is sound.

### B.2 — Is the disqualification of bare asymmetric z-columns sound? **YES, reproduced exactly.**
I rebuilt both LPs (scipy linprog, 3000 control pts/circle, re-optimizing all 24 c_j):
- single-circle `|z|=1`-only LP + z-cols: raise **+1.9e-4**, weight `d=0.00335` —
  matches the outline's "+1.9e-4, c_R=0.0034" to the digit.
- honest both-circle LP + same z-cols: raise **-3.5e-9**, all `d -> 0` — matches the
  outline's "+5e-9 / noise floor."
The disqualification is correct: the asymmetric column lowers `f` on the un-certified
circle exactly as much as it raises it on the certified one. Bare z-columns buy nothing.

### B.3 — THE CORRECTION (most important): the "symmetrized variable" sub-lever is NOT new — it IS the w-dictionary.
The outline sells Angle 1 as breeding in **w AND** in "the symmetrized variable
`R(z)R(1-z)`," presenting the latter as a distinct high-degree lever. **It is not.**
The involution `sigma: z -> 1-z` has invariant ring `C[z]^sigma = C[w]`, `w=z(1-z)`.
I verified symbolically (sympy, reducing mod `z^2-z+w`): for `R in Z[z]`,
`R(z)R(1-z)` reduces to a polynomial in `w` with **integer** coefficients (tested
monic and non-monic R; e.g. `(z^3-z+1)` symmetrized = `w^3+2w^2-3w+1`). So
**`R(z)R(1-z)` is literally an integer w-column `Q(w)`** — it lives in the SAME `Z[w]`
dictionary that R1 column-generation already searched (LP moved ~2e-11; cheap
dictionary exhausted). The symmetrized framing reaches **zero new columns**.

Consequently Angle 1's two advertised levers collapse to **one**: high-degree
(`k>32`) LLL breeding in `w`. Moreover, because every w-column is `z->1-z`-symmetric,
the **both-circle dual EQUALS the single-circle dual for w-columns** — so Angle 1's
"price against the both-circle dual" is, for w-columns, **identical** to pricing
against Flammang's own single-circle dual, which R1 already swept over thousands of
cheap candidates. The only genuinely new content in the entire angle is **LLL depth
`k = 33..40`**, an *unscreened* compute gamble — not a pre-validated source of slack.

### B.4 — Circular reasoning / missing exception case? None found.
- HS-A integrality is clean: `Res(P, R(z)) in Z\{0}` off `{P | R}` (a *fixed* integer
  polynomial, no `a_lead` discriminant factor) — genuinely unlike the OSS column.
  Adjoining `{P | R_k(z)}` and `{P | R_k(1-z)}` to Flammang's finite exception set is
  correct. (For symmetrized/w-columns this is moot — same as Flammang's existing clause.)
- No circularity; the pre-screen LP is honest. The one substantive error is B.3:
  treating `R(z)R(1-z)` as a new search space.

---

## Single most important correction
**Strike the "symmetrized variable `R(z)R(1-z)`" as a distinct lever — it is exactly
the integer `w`-dictionary already exhausted in R1. Angle 1 reduces to ONE lever:
high-degree (`k>32`) LLL breeding of `w`-columns, priced against Flammang's
(single = both-circle) dual.** State this honestly so the builder does not burn
compute re-deriving symmetrized columns expecting independence; the only open shot is
deeper LLL, and it is unscreened.

## Can Angle 1 realistically beat 0.2487458 this round? — Honest read: UNLIKELY this round.
- The retraction is a genuine, reviewer-loggable advance (corrects an invalid held
  value). Do it — that is the round's solid deliverable.
- The forward gain rests entirely on `k>32` LLL finding a w-column with improving
  reduced cost that survives re-optimization. The cheap dictionary is exhausted
  (~2e-11), the asymmetric route honestly collapses (~3e-9), and historical in-method
  gains were ~5e-4 only after *large* searches. There is real headroom vs the truth
  (~0.2527), but it lives only in deep columns pricing cannot cheaply reach.
- **Recommendation:** APPROVE the retraction unconditionally. For the forward work,
  build Angle 1 as a *bounded* LLL breeding pass (k up to ~40, seeded at the dual's
  binding band), with the explicit honest expectation logged as "retract + measure
  whether any k>32 column prices in." If a column earns `c>0` and the both-circle B&B
  clears the gate, great; if not, the round's milestone is the retraction, not a
  forward break. Do **not** let the outline's "+1e-4..+5e-4 realistic" framing set an
  expectation the pre-screen does not support.

## Builder must-dos (carry into the build)
1. Extend `verify_vec.py`'s B&B to BOTH circles `|z|=1` and `|1-z|=1` (it currently
   covers `|z|=1` only, line 285) for ANY z-column; selftest 0 violations; tamper
   above ceiling must FAIL. (For pure w-columns the single circle already suffices.)
2. If any z-column survives, adjoin `{P | R(z)}` and `{P | R(1-z)}` to the exception set.
3. Treat the held forward value as conjecture until the both-circle B&B certifies it;
   only the reviewer writes `held`.
