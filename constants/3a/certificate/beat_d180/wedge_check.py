"""Exact big-int / Fraction wedge confirmation for the d=180 beat.

Confirms, with NO floats on the load-bearing comparison:
  (a) d=180 cell PASSES   Nminus^Q >= Nplus^Q * (2*maxU+1)^P   (c-1 = P/Q)
  (b) d=80 RECORD cell FAILS the same wedge  (=> c strictly above true record)
  (c) chosen c > held 53/45 exactly via Fraction

Also scans for the largest-headline small-Q wedge above held and <= measured value.
"""
import os, json
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def passes(Nplus, Nminus, M, c):
    c = Fraction(c)
    cm1 = c - 1
    p, q = cm1.numerator, cm1.denominator
    assert q > 0
    if p < 0:
        return Nminus >= Nplus
    return Nminus ** q >= (Nplus ** q) * ((2 * M + 1) ** p)


# --- load beat cell (d=180) ---
beat = json.load(open(os.path.join(HERE, "beat_d180.json")))
Np = int(beat["Nplus"]); Nm = int(beat["Nminus"]); M = int(beat["maxU"])

# --- load record cell (d=80) ---
rec = json.load(open(os.path.join(HERE, "..", "sweep", "record_baseline.json")))
rNp = int(rec["Nplus"]); rNm = int(rec["Nminus"]); rM = int(rec["maxU"])

held = Fraction(53, 45)
print(f"held = 53/45 = {float(held):.13f}")
print(f"measured d=180 value (float) = {beat['value_float']:.13f}")
print(f"record value (float)         = {rec['value_float']:.13f}")
print()

# --- candidate wedges: recommended + a scan for larger headline (Q<=200) ---
candidates = [Fraction(139, 118)]
# scan all reduced k/Q with Q in [2..200], strictly above held, that pass the beat cell
best = None
for Q in range(2, 201):
    k = held.numerator * Q // held.denominator + 1
    while Fraction(k, Q) <= held:
        k += 1
    while True:
        c = Fraction(k, Q)
        if c.denominator != Q:   # not reduced -> skip (cheaper Q handles it)
            k += 1
            if float(c) > 1.20:
                break
            continue
        if float(c) > 1.20:       # safety: above any plausible value, stop
            break
        if c > held and passes(Np, Nm, M, c):
            if best is None or c > best:
                best = c
        k += 1
print(f"largest passing wedge with Q<=200, reduced, > held: {best} = {float(best):.13f}  (Q={best.denominator})")
candidates.append(best)

for c in candidates:
    cm1 = c - 1
    a = passes(Np, Nm, M, c)            # beat cell passes
    b = passes(rNp, rNm, rM, c)         # record cell passes? must be FALSE
    over = c > held
    print(f"\nc = {c} = {float(c):.13f}  (P/Q = {cm1.numerator}/{cm1.denominator})")
    print(f"  (a) d=180 cell passes wedge : {a}")
    print(f"  (b) d=80 record cell passes : {b}  (must be False => record FAILS => strict over record)")
    print(f"  (c) c > held 53/45          : {over}   margin = {float(c-held):.3e}")
    verdict = a and (not b) and over
    print(f"  VERDICT (valid strict beat) : {verdict}")
