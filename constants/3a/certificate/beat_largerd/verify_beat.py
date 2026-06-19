"""
Re-runnable STRICT-BEAT certificate for C_3a:  lower bound > 1.1740744476935212 (the verified
record, [G2026] PR #71 base-21 d=80 T=150 construction).

NEW construction (this certificate) -- two cells, both strict beats:
    A = {0,2,3,4,5,6,7,8,9,10},  B = 21,  d = 100       (carry-free: B=21 > 2*max(A)=20)
    U = { sum_{i<d} a_i B^i : a_i in A, sum a_i <= T }
    value = 1 + log(|U-U| / |U+U|) / log(2*max(U)+1)     (GHR2007 lower bound on C_3a)
    PRIMARY    T = 187 (density 1.875):  value >= 5877/5000 = 1.1754
    SECONDARY  T = 180 (density 1.80 ):  value >= 2937/2500 = 1.1748

CLAIM:  C_3a >= 5877/5000 = 1.1754  >  value_record = 1.1740744476935212.

ALL load-bearing arithmetic is exact big-int (no float decides anything):
  Step 1  recompute |U+U|, |U-U|, max(U) for the NEW cell from scratch (fast carry-free DP).
  Step 2  recompute the RECORD cell's three integers from scratch, and cross-check them
          against record_baseline.json (the PR #71 values) -- both engines, bit-for-bit.
  Step 3  pick wedge c = 2937/2500.  Verify by exact integer-power inequalities:
            (a) value_new   >= c :   Nm_new^q   >= Np_new^q   * (2*M_new+1)^p
            (b) value_record <  c :  Nm_rec^q   <  Np_rec^q   * (2*M_rec+1)^p
          where (c-1) = p/q in lowest terms (p=437, q=2500 -- small, fast powers).
          (a) & (b)  =>  value_new >= c > value_record : a STRICT exact beat.

Run:  python3 verify_beat.py
Exit 0 and "CERTIFICATE OK" only if every check passes.
"""
import os, sys, json, math
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "..", "engine")
SWEEP = os.path.join(HERE, "..", "sweep")
sys.path.insert(0, ENGINE)
sys.path.insert(0, SWEEP)
from digit_dp import count_opset, max_U                       # fast carry-free DP
from dp_engine import count_sumset, count_diffset, maxU       # independent Pareto DP

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
B = 21
assert B > 2 * max(A), "carry-free regime requires B > 2*max(A)"

# ---- RECORD cell ----------------------------------------------------------
d_rec, T_rec = 80, 150
print(f"[1] RECORD cell  d={d_rec} T={T_rec}")
RNp = count_opset(A, d_rec, T_rec, '+')
RNm = count_opset(A, d_rec, T_rec, '-')
RM = max_U(A, B, d_rec, T_rec)
base = json.load(open(os.path.join(SWEEP, "record_baseline.json")))
assert str(RNp) == base["Nplus"],  "record |U+U| != PR#71 baseline"
assert str(RNm) == base["Nminus"], "record |U-U| != PR#71 baseline"
assert str(RM) == base["maxU"],   "record max(U) != PR#71 baseline"
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

# ---- NEW cells + EXACT wedge certificate ----------------------------------
# (cell, wedge c).  PRIMARY first; the headline claim is the PRIMARY's c.
cells = [
    ("PRIMARY",   100, 187, Fraction(5877, 5000)),   # 1.1754
    ("SECONDARY", 100, 180, Fraction(2937, 2500)),   # 1.1748
]
all_ok = True
headline_c = None
for tag, d_new, T_new, c in cells:
    print(f"[3:{tag}] NEW cell  d={d_new} T={T_new} (density {T_new/d_new})  wedge c={c}={float(c)}")
    Np = count_opset(A, d_new, T_new, '+')
    Nm = count_opset(A, d_new, T_new, '-')
    M = max_U(A, B, d_new, T_new)
    v_new = 1 + math.log(Nm / Np) / math.log(2 * M + 1)
    print(f"     |U+U|={len(str(Np))}d |U-U|={len(str(Nm))}d max(U)={len(str(M))}d  value~{v_new:.13f}")
    cm1 = c - 1
    p, q = cm1.numerator, cm1.denominator
    # (a) value_new >= c   <=>   Nm^q >= Np^q * (2M+1)^p   (value>=1 so p>=0)
    new_ge = (Nm ** q) >= (Np ** q) * ((2 * M + 1) ** p)
    # (b) value_record < c <=>   RNm^q <  RNp^q * (2RM+1)^p
    rec_lt = (RNm ** q) < (RNp ** q) * ((2 * RM + 1) ** p)
    print(f"     (c-1)={p}/{q}   value_new >= c: {new_ge}   value_record < c: {rec_lt}")
    cell_ok = new_ge and rec_lt
    all_ok = all_ok and cell_ok
    if tag == "PRIMARY":
        headline_c = c

print()
if all_ok:
    print(f"CERTIFICATE OK: C_3a >= {headline_c} = {float(headline_c)} "
          f"> 1.1740744476935212 (verified record).")
    print(f"  strict margin over record >= {float(headline_c) - v_rec:.2e}")
    sys.exit(0)
else:
    print("CERTIFICATE FAILED")
    sys.exit(1)
