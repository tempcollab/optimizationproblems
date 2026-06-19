"""
Re-runnable STRICT-BEAT certificate for C_3a (Round 23):

    CLAIM:  C_3a  >=  1177/1000  =  1.1770   (matches the R23 Lean theorem
            C3a.c3a_ge_1177_1000', wedge Q=1000, P=177)
            >  2353/2000 = 1.1765  (our previously HELD value, verified R22 / Lean R22)
            >  5877/5000 = 1.1754  (R18/R19 held)
            >  1.1740744476935212  (the historical [G2026] PR #71 record).

Construction (the record drop-1 alphabet, pushed to larger d):
    A = {0,2,3,4,5,6,7,8,9,10},  B = 21      (carry-free: B=21 > 2*max(A)=20)
    U = { sum_{i<d} a_i B^i : a_i in A, sum a_i <= T }
    value = 1 + log(|U-U| / |U+U|) / log(2*max(U)+1)        (GHR2007 lower bound on C_3a)

    PRIMARY  cell:  d=140, T=263 (density 1.8786)  ->  value ~ 1.1771186319558
    strictly beats held 2353/2000; the headline wedge is taken from this cell.

ALL load-bearing arithmetic is EXACT big-int -- no float decides anything:
  Step 1  load the persisted d=140 integers (re-derivable from scratch with --recompute,
          ~650s: diff/max ~135s + sumset ~510s via engine/digit_dp.count_opset).
  Step 2  recompute the RECORD cell's three integers from scratch and cross-check them
          against record_baseline.json (PR #71) bit-for-bit.
  Step 3  independent Pareto-DP cross-check (engine/dp_engine) on small carry-free cells.
  Step 4  wedge c = 1177/1000.  Verify by EXACT integer-power inequalities:
            (a) value_new    >= c :  Nm_new^q  >= Np_new^q  * (2*M_new+1)^p
            (b) value_record <  c :  RNm^q     <  RNp^q     * (2*RM+1)^p
          where (c-1) = p/q in lowest terms (p=177, q=1000).
          (a) & (b)  =>  value_record < c <= value_new.
  Step 5  EXACT rational re-assertion that c strictly exceeds ALL prior bars:
            c > 2353/2000 (R22 HELD) AND c > 5877/5000 AND c > the record value.

Run:  python3 verify_beat.py              (loads persisted d=140 integers; recomputes the
                                           RECORD cell + small cross-checks; ~80s)
      python3 verify_beat.py --recompute  (also recomputes the d=140 cell from scratch via
                                           the DP, ~650s extra -- the full from-scratch path)

Exit 0 and "CERTIFICATE OK" only if every check passes.
"""
import os, sys, json, math
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "..", "engine")
SWEEP = os.path.join(HERE, "..", "sweep")
sys.path.insert(0, ENGINE)
sys.path.insert(0, SWEEP)
from digit_dp import count_opset, max_U
from dp_engine import count_sumset, count_diffset, maxU

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
B = 21
assert B > 2 * max(A), "carry-free regime requires B > 2*max(A)"

HELD   = Fraction(2353, 2000)   # R22 held (verified), 1.1765
HELD0  = Fraction(5877, 5000)   # R18/R19 held, 1.1754
WEDGE  = Fraction(1177, 1000)   # the new claimed bound, 1.1770 (matches the R23 Lean cert)

# ---- RECORD cell ----------------------------------------------------------
d_rec, T_rec = 80, 150
print(f"[1] RECORD cell  d={d_rec} T={T_rec}")
RNp = count_opset(A, d_rec, T_rec, '+')
RNm = count_opset(A, d_rec, T_rec, '-')
RM  = max_U(A, B, d_rec, T_rec)
base = json.load(open(os.path.join(SWEEP, "record_baseline.json")))
assert str(RNp) == base["Nplus"],  "record |U+U| != PR#71 baseline"
assert str(RNm) == base["Nminus"], "record |U-U| != PR#71 baseline"
assert str(RM)  == base["maxU"],   "record max(U) != PR#71 baseline"
print("    record integers match record_baseline.json (PR #71) bit-for-bit: OK")
v_rec = 1 + math.log(RNm / RNp) / math.log(2 * RM + 1)
print(f"    value_record (float, display only) = {v_rec:.13f}")

# ---- independent engine cross-check on small cells ------------------------
print("[2] independent Pareto-engine cross-check on small cells:")
for (d, T) in [(20, 37), (30, 56), (40, 75)]:
    ok = (count_opset(A, d, T, '+') == count_sumset(A, B, d, T)
          and count_opset(A, d, T, '-') == count_diffset(A, B, d, T)
          and max_U(A, B, d, T) == maxU(A, B, d, T))
    print(f"     d={d} T={T}: two engines agree = {ok}")
    assert ok, "engine disagreement -- counts unreliable"

# ---- NEW d=140 cell -------------------------------------------------------
RECOMPUTE = "--recompute" in sys.argv
d_new, T_new = 140, 263
print(f"[3] NEW cell  d={d_new} T={T_new} (density {T_new/d_new:.4f})")
persisted = json.load(open(os.path.join(HERE, "beat_d140.json")))
Np = int(persisted["Nplus"]); Nm = int(persisted["Nminus"]); M = int(persisted["maxU"])
if RECOMPUTE:
    print("    --recompute: recomputing d=140 integers from scratch (~650s) ...")
    Nm2 = count_opset(A, d_new, T_new, '-')
    M2  = max_U(A, B, d_new, T_new)
    Np2 = count_opset(A, d_new, T_new, '+')
    assert Np2 == Np and Nm2 == Nm and M2 == M, "d140 recompute disagrees with persisted"
    print("    d=140 from-scratch recompute matches persisted integers: OK")
else:
    print("    d=140 integers loaded from persisted beat_d140.json "
          "(re-derivable with --recompute)")
v_new = 1 + math.log(Nm / Np) / math.log(2 * M + 1)
print(f"    |U+U|={len(str(Np))}d  |U-U|={len(str(Nm))}d  max(U)={len(str(M))}d")
print(f"    value_new (float, display only) = {v_new:.13f}")

# ---- EXACT wedge certificate ---------------------------------------------
print(f"[4] EXACT integer-power wedge  c = {WEDGE} = {float(WEDGE):.15f}")
cm1 = WEDGE - 1
p, q = cm1.numerator, cm1.denominator
new_ge = (Nm ** q) >= (Np ** q) * ((2 * M + 1) ** p)
rec_lt = (RNm ** q) < (RNp ** q) * ((2 * RM + 1) ** p)
print(f"    (c-1) = {p}/{q}")
print(f"    (a) value_new   >= c   [Nm^q >= Np^q*(2M+1)^p] : {new_ge}")
print(f"    (b) value_record <  c  [RNm^q <  RNp^q*(2RM+1)^p] : {rec_lt}")

# ---- EXACT comparison against ALL bars -----------------------------------
print("[5] EXACT comparison of the wedge against all bars (rational, no float):")
beats_held  = WEDGE > HELD
beats_held0 = WEDGE > HELD0
beats_rec   = rec_lt   # value_record < c, certified by the exact inequality above
print(f"    c > held 2353/2000 = 1.1765 (exact Fraction)  : {beats_held}"
      f"   (c - held = {float(WEDGE - HELD):.3e})")
print(f"    c > 5877/5000 = 1.1754 (exact Fraction)       : {beats_held0}")
print(f"    c > record 1.1740744476935212 (via rec_lt)    : {beats_rec}")

all_ok = new_ge and rec_lt and beats_held and beats_held0 and beats_rec
print()
if all_ok:
    print(f"CERTIFICATE OK: C_3a >= {WEDGE} = {float(WEDGE):.12f}")
    print(f"  > held 2353/2000 = 1.1765           (strict beat of OUR R22 held bound)")
    print(f"  > 5877/5000 = 1.1754                (strict beat of the R18/R19 held bound)")
    print(f"  > 1.1740744476935212                (strict beat of the G2026 record)")
    sys.exit(0)
else:
    print("CERTIFICATE FAILED")
    sys.exit(1)
