# lean-cert-rational-power

## Idea

Convert the R18 verified *numerical* lower bound `C_3a ≥ 5877/5000 = 1.1754` into a
`lake build`-checked Lean theorem — the gold-standard certificate form the user emphasized.
This does NOT change the held bound number (stays 5877/5000); it upgrades the existing
verified beat to a machine-checked proof.

The GHR digit-set bound `θ(U) = 1 + log(|U−U|/|U+U|)/log(2·max(U)+1)` is rationalized
**log-free** (Route A): for a rational target `c = 1 + P/Q` (here `c = 5877/5000`, `P=877`,
`Q=5000`),

  `θ(U) ≥ c  ⟺  |U−U|^Q ≥ |U+U|^Q · (2·max(U)+1)^P`.

The right-hand integer inequality is `decide`-able over `ℕ` (GMP big-ints in the kernel);
no `Real.log`/`Real.rpow` enters the certified statement. The analytic existence step
(`θ(U) ≥ c ⟹ C_3a ≥ c`) is carried as a NAMED hypothesis `GHR_lower`, the honest trust
boundary — the analog of 9a's `ThetaGeFromIndep` and 5b's `MTThm15`.

## Status — R19: BUILT, `lake build` PASS, axiom footprint clean (claim, pending review)

`lean/Constants/C3a.lean` (namespace `C3a`). `lake build Constants.C3a` PASS (~4s), whole
tree `lake build` PASS (8574 jobs, Mathlib v4.31.0).

Claimed (pending proof-reviewer verification): the bound `C_3a ≥ 5877/5000` is now a
`lake build`-checked Lean theorem `c3a_ge_5877_5000'` resting only on the named `GHR_lower`
bridge plus axiom-free `decide` lemmas.

PROVED inside Lean (axiom-free `decide`, `#print axioms` = `[propext]` only — no `sorryAx`,
no `Classical.choice`, no `native_decide`/`ofReduceBool`):
- `newGE : Nplus^Q * (2*maxU+1)^P ≤ Nminus^Q` — the d=100 beat cell PASSES the wedge
  (`θ ≥ 5877/5000`). Load-bearing; ~2-million-bit `Nat` powers by pure kernel `decide`.
- `recLT : recNminus^Q < recNplus^Q * (2*recMaxU+1)^P` — the d=80 RECORD cell FAILS the same
  wedge (`value_record < c`), certifying the beat is STRICT.

Assembled (carry `[propext, Classical.choice, Quot.sound]`, the standard Mathlib trio from
the ℝ machinery — no new axiom, no sorry):
- `c3a_ge_5877_5000 (c3a) (hbridge : GHR_lower c3a) : c3a ≥ 1 + 877/5000`
- `c3a_ge_5877_5000' (c3a) (hbridge : GHR_lower c3a) : c3a ≥ 5877/5000`

NAMED TRUST BOUNDARY (the only non-`decide` content, a hypothesis NOT an axiom):
- `GHR_lower (c3a : ℝ) : Prop := ∀ (s d m p q : ℕ), 0 < s → 0 < q → s ≤ d →
   s^q*(2*m+1)^p ≤ d^q → c3a ≥ 1 + (p:ℝ)/q` — packages ONLY the GHR2007 existence step;
  supplies no arithmetic.

Integer literals copied verbatim from the verified numerical cert
(`certificate/beat_largerd/beat_d100.json` PRIMARY; `certificate/engine/record_*.txt`); NOT
recomputed in the Lean kernel (deliberate — kernel digit-DP is an unprobed OOM hazard, not
this round's increment; provenance re-derivable by `verify_beat.py`/`digit_dp.py`). 9a (R13)
precedent: codewords trusted as literals, provenance verified out of Lean.

Cert recorded at `constants/3a/certificate/lean_cert/README.md` (build target + axioms line).

### Claimed value

- Table / record to beat (verified): `1.1740744476935212` [G2026].
- Held by us (R18, verified numerical): `5877/5000 = 1.1754`.
- This round: SAME number `5877/5000`, now claimed as a `lake build`-checked Lean theorem
  (form upgrade, not a number change). Strictly beats the record: yes (certified by
  `newGE` + `recLT`, both axiom-free).

## How to push further

- **Larger-margin Lean cert (`push-d-further`):** a d=130–160 numerical beat (extrapolated
  ~1.1758–1.1763) ports through the SAME `GHR_lower` bridge — only the three `Nat` literals
  and the wedge `(P,Q)` change. The wedge `q` stays small (~few thousand) so the `decide`
  stays ~2s. Build the numerical beat first (R18 protocol: `count_opset`, one cell/Bash call,
  `timeout ≥ 600s`, JSON persist), then swap literals into a new theorem in `C3a.lean`.
- **Make the rearrangement visible in Lean (Route B, optional hardening):** if the reviewer
  wants the `θ ≥ c ⟺ d^Q ≥ s^Q·q^P` equivalence formalized inside Lean (so `GHR_lower`'s
  hypothesis is the literal `θ ≥ c` rather than the integer form), prove it via
  `Real.rpow` monotonicity (`Real.rpow_natCast`, `Real.rpow_le_rpow_left_iff`,
  `Real.log` monotonicity). This shrinks the trust boundary to purely the existence step but
  is NOT required — Route A's integer form is already a faithful, lighter cert.
- **Reduce the trust boundary entirely:** would require formalizing the GHR base-q
  block-digit construction and the `C_3a` sup definition in Mathlib — a large, separate
  project, not round-sized. Out of scope; `GHR_lower` is the accepted honest boundary
  (same as 9a/5b).

## Sources

- [GHR2007] Gyarmati, Hennecart, Ruzsa, "Sums and differences of finite sets",
  Funct. Approx. Comment. Math. 37(1):175–186, 2007 — the Lemma giving
  `C_3a ≥ 1 + log(|U−U|/|U+U|)/log(2·max(U)+1)` and the carry-free base-q construction.
  Digest: `constants/3a/literature/GHR2007-lemma-digest.md`.
- R18 numerical certificate: `constants/3a/certificate/beat_largerd/{verify_beat.py,beat_d100.json}`.
- Pattern: `lean/Constants/C9Cert367.lean` (`ThetaGeFromIndep`), `lean/Constants/C5b.lean` (`MTThm15`).
