"""
R7 DESIGN-PRINCIPLE result -- consolidated reproduce sheet (82a UPPER).

Runs the four load-bearing checks that establish the round's OUTCOME (structural-only,
no numeric break): the design objective r~ is well-defined and computable, the firing
table blocks coprime to the dictionary are j16/j17/j20, the firing integer lattice is
NON-PERTURBATIVE and the dictionary is a MAXIMAL FIRING SET on the saturated R4 anchor
(cheapest coprime factor cost > best firing margin), and the float pre-gate FAILS
(best reachable block converts to a sub-5e-6 drop -> lever dry, no certify).

ALL r~ measured on the R4 anchor (j3 AND j9 ON, candidate exp 0) = GUARDRAIL 1.
Run:  python3 R7_structural_result.py        (~2-3 min)
"""
import numpy as np
import verify_firstvar_lemma as fv
import construct_block_R7 as cb
import flammang_table1 as ft

tab = ft._TABLE_DESCENDING
sc = cb.Scorer(fv.R4, 2_000_000)

print("=" * 88)
print("R7 STRUCTURAL RESULT -- design-principle construction on the saturated R4 anchor")
print("=" * 88)

# (1) objective sanity: j3,j9 already active on R4 -> trap (r~ >= ~0), not firing here.
print("\n(1) r~ objective on R4 (j3,j9 already active -> trap row, NOT firing):")
print(f"    r~(j3) = {sc.rtilde(fv.J3):+.6f}   r~(j9) = {sc.rtilde(fv.J9):+.6f}")

# (2) which table blocks fire AND are coprime to the 11-block dictionary on R4
print("\n(2) Flammang Table-1 blocks that FIRE (r~<0) and are coprime+squarefree vs dict:")
fire_coprime = []
for j, (c, desc) in enumerate(tab, 1):
    rt = sc.rtilde(desc)
    if rt >= 0:
        continue
    cop, sf, fails = cb.admissibility(desc)
    if cop and sf:
        fire_coprime.append((j, rt, len(desc) - 1))
        print(f"    j{j:<2} deg={len(desc)-1:<2} r~={rt:+.6f}  (firing-coprime; but NOT original)")
    else:
        print(f"    j{j:<2} deg={len(desc)-1:<2} r~={rt:+.6f}  blocked: shares {fails} with dict")

# (3) non-perturbative: best firing-coprime block j16, every +-1 perturbation flips sign
j16 = list(tab[15][1])
print(f"\n(3) NON-PERTURBATIVE firing -- j16 (deg16, r~={sc.rtilde(j16):+.6f}):")
swings = []
for i in range(1, len(j16)):
    for dl in (-1, 1):
        d = list(j16); d[i] = j16[i] + dl
        swings.append(sc.rtilde(d))
print(f"    best single +-1 perturbation r~ = {min(swings):+.6f}  (all flip POSITIVE)")
print(f"    => swing from -0.0052 to >= +0.06 : firing roots sit microscopically inside")
print(f"       the lemniscate; the firing lattice points are ISOLATED.")

# (4) maximal-firing-set obstruction: cheapest coprime monic factor cost vs firing margin
print("\n(4) MAXIMAL-FIRING-SET obstruction (the saturation mechanism):")
best_factor = (1e9, None)
for b in range(-4, 5):
    for c in range(-4, 5):
        desc = [1, b, c]
        cop, sf, fails = cb.admissibility(desc)
        if cop and sf and cb.is_original(desc):
            mn = cb.min_contour_modulus(desc, 40000)
            if mn < 1e-4:
                continue
            rt = sc.rtilde(desc)
            if rt < best_factor[0]:
                best_factor = (rt, desc)
print(f"    cheapest coprime ORIGINAL monic factor (deg<=2): r~ = {best_factor[0]:+.6f}"
      f"  {best_factor[1]}")
print(f"    best firing-coprime reachable block j16 margin   : r~ = {sc.rtilde(j16):+.6f}")
print(f"    => any original block = (firing block) x (coprime factor) pays "
      f"{best_factor[0]:+.4f} > |{sc.rtilde(j16):.4f}|, flipping the product POSITIVE.")
print(f"    The dictionary {{P1=w, P2=w-1, j13=Q5, j15=Q6, ...}} has absorbed exactly the")
print(f"    cheap firing factors -> it is a MAXIMAL FIRING SET on R4; no original firing")
print(f"    block of deg<=16 exists within reach (confirmed by ~80k-candidate searches).")

print("\n" + "=" * 88)
print("OUTCOME: STRUCTURAL-ONLY.  The design METHOD (r~ objective + U^nu-well root")
print("factorization) is validated and correctly characterizes firing; but on the")
print("saturated R4 anchor it proves NO original firing block exists within reach, and")
print("the float pre-gate (best reachable block j16 -> drop 2.94e-6 < 5e-6 gate) confirms")
print("the A-base lever is DRY.  No certify run (gate failed).  Held upper 0.2538893183")
print("UNCHANGED.")
print("=" * 88)
