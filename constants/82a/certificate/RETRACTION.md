# RETRACTION — OSS log-energy LOWER-bound certificate (R14 / R15 / R17) is INVALID

**Status: the held lower bound 0.2524001332 (R17), and its predecessors
0.2511300035 (R15) and 0.2509000289 (R14), are RETRACTED.**

**Corrected verified held lower bound = `0.2487458` = log(1.282416) [Flammang F18].**
(Reproduced from scratch in R1 by `verify_vec.py`; it does NOT beat the table —
it re-establishes the Flammang record.)

The upper-side held value `0.2540419719` (R11) is INDEPENDENT of this dispute and
**stands**.

Witness: `constants/82a/certificate/retract_oss_lower.py` (runs in ~20 s, no
network). It uses the SAME committed frozen data (`frozen_energy.npz`) and the SAME
`f`-formula as the retracted certificate (`verify_vec_energy.py`), and prints three
`PASS` lines, any one of the two FAILUREs being sufficient to retract.

---

## What the lower-bound method actually proves

For a minimal polynomial `P` of an algebraic number `alpha` (off the finite
exception set), with conjugate measure `nu` (mass `1/d` per conjugate, in `z`), the
Smyth/Flammang auxiliary-function argument gives

    (1/d) log Z(alpha) = INT g dnu  >=  min_{supp nu} f ,

where `f = g - sum_j c_j log|Q_j| - lambda0 (2 U_mu0 - Ihat)` is the certificate's
integrand. **The bound is `min f` over the support of `nu` (in general the whole
plane region the conjugates occupy), NOT `min f` over `|z|=1`.** Flammang's reduction
"min on `|z|=1`" is only a *cheap way to compute* `min_plane f`, and it is valid
**only if the global plane minimum of `f` sits on the unit circle(s)**. For
Flammang's pure `f0` this holds (`f0` is subharmonic off the circles, so the maximum
principle puts its min on `|z|=1`). The OSS certificate breaks it.

## FAILURE 1 (decisive on its own): wrong min-locus

The added term `-2 lambda0 U_mu0` is **superharmonic in the support band**:
`U_mu0` is the logarithmic potential of the mass `mu0` on `|z|=1`, so
`Delta U_mu0 = 2 pi mu0 >= 0` there (witness: discrete `Delta U_mu0 ~ +2.7e-7 > 0`
ON `|z|=1`, `~0` off it). A superharmonic perturbation destroys the
subharmonic-off-circles property, so the maximum principle no longer places `min f`
on `|z|=1`. Measured on the certificate's own `f` (frozen R17 data):

| locus | value |
|---|---|
| `min f` on `\|z\|=1` (what the cert certifies) | **0.252548** |
| `min f` over the 2-D plane (what the method needs) | **-0.19143** at `\|z\|~1.61` (near `phi=1.618`) |

So the method proves only `C_82 >= min_plane f = -0.19143`, which is **far below**
the Flammang record `0.2487458`. **The certificate bounds nothing.** The conjugate
measure `nu` of a Zhang–Zagier-minimal polynomial is not supported on `|z|=1`; the
conjugates spread over the plane (the `|z(1-z)|` lemniscate region), exactly where
`f` dips below 0.

## FAILURE 2 (independent): the OSS column premise `I(nu) >= 0` fails for ZZ

The OSS energy column is nonnegative only if `I(nu) = (1/d^2) log|disc(P)| >= 0`.
This holds for totally-real algebraic **integers** (leading coeff `a = 1`,
`disc(P)` a nonzero integer `>= 1`). But the Zhang–Zagier height is defined for **all
algebraic numbers**, so `P` is only primitive and its leading coefficient `a` can
exceed 1, with

    I(nu) = (1/d^2) [ log|disc(P)| - (2d-2) log|a| ] .

Concrete primitive irreducible counterexample (genuine ZZ-relevant non-integers):

    P(x) = 10 x^2 - 6 x + 1 ,  roots (3 +- i)/10 ,  a = 10 ,  |disc| = 4
    I(nu) = (log 4 - 2 log 10) / 4 = -0.804719  <  0 .

So the OSS column is **not a valid `>= 0` column for ZZ** — the `+0.0037` "raise" was
a mis-signed, mis-located artifact.

---

## Text the reviewer should enact (the reviewer owns these edits)

1. **`constants/82a.md` — "Known lower bounds" table:** strike (or annotate as
   WITHDRAWN) the three rows `0.25240 (R17)`, `0.25113 (R15)`, `0.25090 (R14)`.
   The best verified lower bound row becomes `0.24874 [F18]`.

2. **`constants/82a/current.md`:**
   - `## Status`: the lower side is no longer a record break. If the upper side is
     not separately flagged `improved`, set `## Status: none`.
   - `## Bounds … held:` set the lower held to `0.2487458` (Flammang [F18],
     R1-reproduced via `verify_vec.py`); keep the upper held `0.2540419719` (R11).
   - `## Progress log`: append an `- R<n>:` line recording the retraction as the
     verified advance of this round (an invalid held value corrected), pointing at
     `certificate/retract_oss_lower.py`.

3. **`README.md` table** (if it carries the disputed lower value): reset the 82a
   lower entry to `0.24874 [F18]`.

Reproduce the retraction: `python3 constants/82a/certificate/retract_oss_lower.py`
(prints `[a]` on-circle min ~0.2525, `[b]` plane min ~ -0.19, the superharmonic
mechanism, and `[c]` the `I(nu) < 0` counterexample; ends `RESULT: RETRACT`).
