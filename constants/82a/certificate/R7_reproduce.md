# R7 reproduce sheet — design-principle construction (82a UPPER, STRUCTURAL-ONLY)

Outcome: **no numeric break, no original firing block on R4.** Held upper 0.2538893183
UNCHANGED. The round delivers a formalized design optimization + a sharp mechanistic
characterization of A-base saturation (the dictionary is a *maximal firing set*).

All r̃ measured on the **R4 anchor** (j3 AND j9 ON, candidate exponent 0) — the q_Q=0
base family for a THIRD A-base block (outline-review GUARDRAIL 1). HELD in the float
pre-gate = 0.2538893183 (GUARDRAIL 2).

## Primary check (consolidated, ~2 min)
```
cd constants/82a/certificate
python3 R7_structural_result.py
```
Establishes the four load-bearing facts:
1. r̃(j3)=−0.000031, r̃(j9)=+0.000123 on R4 (already-active trap rows).
2. firing-AND-coprime Table-1 blocks on R4 = j16 (deg16, −0.00521), j17 (−0.00374),
   j20 (deg20, −0.00827); all NON-ORIGINAL. Others blocked: Q5=j13, Q6=j15, P8=j12, P1=j1.
3. NON-PERTURBATIVE: best single ±1 perturbation of j16 → r̃=+0.0628 (all flip positive).
4. MAXIMAL-FIRING-SET: cheapest coprime original monic factor (w²−w+1) costs r̃=+0.01311 >
   |j16 margin −0.00521| → every original product flips positive. No original firing block
   of deg ≤ 16 within reach.

## Float pre-gate (GUARDRAIL 2; ~4–6 min)
```
python3 float_pregate_q9A.py j16 350000 4000000
```
Feeds the strongest reachable firing-coprime block (j16) as a hypothetical 3rd A-base
block; joint 10-exponent Nelder-Mead, N-stable re-eval at N=4M:
- re-optimized log h = 0.2538863828, qI*=0.06854, **drop below held = 2.94e−6 < 5e−6 gate**.
- **GATE FAIL** → lever dry → NO certify run.

## Design-problem solvers (each ~2–6 min; all return 0 original firing blocks)
```
python3 design_block.py 500000     # Angle 1: LLL/CVP energy min, monic deg 4..8
python3 design_block2.py 600000    # Angle 2/3: U^ν-well root-target rounding, deg ≤10 (~74k cands)
python3 design_block3.py 600000    # locus-hugging high-degree targets, deg ≤16
```

## Engine (R6, unchanged) — the criterion the objective rests on
```
python3 verify_firstvar_lemma.py 4000000 1e-4   # first-variation lemma (PASS)
python3 verify_firstvar_lemma.py roots 2000000  # r̃ = Σ U^ν(ρ) + deg·log|lead| (PASS, 5.2e−17)
```

## Notes
- `min|Q∘χ|` contour-root-free screen: j16 2.3e−5, j20 6.4e−6 (firing roots sit
  microscopically inside the lemniscate — that is why firing is a knife-edge).
- Non-monic is strictly worse: lead 2 pays +2·log2·arcfrac = +0.0951 in r̃ (the log|lead|
  boundedness term, GUARDRAIL 3). Monic search is therefore complete.
- The maximal-firing-set obstruction is anchor-specific (the R4 dictionary is firing-
  saturated). A further original firing block would need a SWAP, not an additive coprime
  factor; a numeric break almost certainly needs to leave the saturating Doche A-base family.
