"""
Re-runnable STRICT-BEAT certificate for C_3a (Round 21):

    CLAIM:  C_3a  >=  20/17  =  1.176470588235...
            >  5877/5000 = 1.1754  (our previously HELD value, verified R18 / Lean R19)
            >  1.1740744476935212  (the historical [G2026] PR #71 record).

Construction (the record drop-1 alphabet, pushed to larger d):
    A = {0,2,3,4,5,6,7,8,9,10},  B = 21      (carry-free: B=21 > 2*max(A)=20)
    U = { sum_{i<d} a_i B^i : a_i in A, sum a_i <= T }
    value = 1 + log(|U-U| / |U+U|) / log(2*max(U)+1)        (GHR2007 lower bound on C_3a)

    PRIMARY  cell:  d=130, T=244 (density 1.8769)  ->  value ~ 1.1767830604497
    FIRST-RUNG   :  d=120, T=225 (density 1.8750)  ->  value ~ 1.1763975172306
    Both strictly beat held 5877/5000; the headline wedge is taken from the d=130 cell.

ALL load-bearing arithmetic is EXACT big-int -- no float decides anything:
  Step 1  recompute |U+U|, |U-U|, max(U) for the NEW d=130 cell from scratch (fast
          carry-free DP, engine/digit_dp.count_opset), and ALSO load the persisted integers
          from the climb run and require they agree bit-for-bit.
  Step 2  recompute the RECORD cell's three integers from scratch and cross-check them
          against record_baseline.json (PR #71) bit-for-bit.
  Step 3  independent Pareto-DP cross-check (engine/dp_engine) on small carry-free cells.
  Step 4  pick wedge c = 20/17.  Verify by exact integer-power inequalities:
            (a) value_new    >= c :  Nm_new^q  >= Np_new^q  * (2*M_new+1)^p
            (b) value_record <  c :  RNm^q     <  RNp^q     * (2*RM+1)^p
          where (c-1) = p/q in lowest terms (p=3, q=17 -- tiny, instant powers).
          (a) & (b)  =>  value_new >= c > value_record.
  Step 5  EXACT rational re-assertion that c strictly exceeds BOTH bars:
            c > Fraction(5877,5000)  (our HELD value) AND c > the record value.
          (The climb driver only compares against the record; this cert closes the trap.)

Run:  python3 verify_beat.py              (fast: loads the persisted d=130 integers,
                                           recomputes the RECORD cell + small cross-checks,
                                           re-derives the EXACT wedge from scratch; ~150s)
      python3 verify_beat.py --recompute  (also recomputes the d=130 cell from scratch via
                                           the DP, ~440s extra -- the full from-scratch path)

The d=130 sumset DP alone is ~440s; loading its persisted integers (each independently
re-checkable by --recompute) keeps the default re-check well under any single timeout while
every EXACT load-bearing step (the wedge inequalities, both bar comparisons, the record
recompute, the independent-engine cross-check) is re-run from scratch each time.

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

HELD = Fraction(5877, 5000)          # our previously held (verified) value, 1.1754
WEDGE = Fraction(20, 17)             # the new claimed bound, 1.176470588...

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

# ---- NEW d=130 cell -------------------------------------------------------
RECOMPUTE = "--recompute" in sys.argv
d_new, T_new = 130, 244
print(f"[3] NEW cell  d={d_new} T={T_new} (density {T_new/d_new:.4f})")
persisted = json.load(open(os.path.join(SWEEP, "climb_state.json")))["d130_T244"]
Np = int(persisted["Nplus"]); Nm = int(persisted["Nminus"]); M = int(persisted["maxU"])
if RECOMPUTE:
    print("    --recompute: recomputing d=130 integers from scratch (~440s) ...")
    Np2 = count_opset(A, d_new, T_new, '+')
    Nm2 = count_opset(A, d_new, T_new, '-')
    M2 = max_U(A, B, d_new, T_new)
    assert Np2 == Np and Nm2 == Nm and M2 == M, "d130 recompute disagrees with persisted"
    print("    d=130 from-scratch recompute matches persisted integers: OK")
else:
    print("    d=130 integers loaded from persisted climb_state.json "
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

# ---- EXACT comparison against BOTH bars ----------------------------------
print("[5] EXACT comparison of the wedge against both bars (rational, no float):")
beats_held = WEDGE > HELD
beats_rec_exact = (RNm ** q) < (RNp ** q) * ((2 * RM + 1) ** p)   # == rec_lt
print(f"    c > held 5877/5000 = 1.1754 (exact Fraction)         : {beats_held}"
      f"   (c - held = {float(WEDGE - HELD):.3e})")
print(f"    c > record 1.1740744476935212 (exact via rec_lt)     : {beats_rec_exact}")

all_ok = new_ge and rec_lt and beats_held and beats_rec_exact
print()
if all_ok:
    print(f"CERTIFICATE OK: C_3a >= {WEDGE} = {float(WEDGE):.12f}")
    print(f"  > held 5877/5000 = 1.1754           (strict beat of OUR held bound)")
    print(f"  > 1.1740744476935212                (strict beat of the G2026 record)")
    sys.exit(0)
else:
    print("CERTIFICATE FAILED")
    sys.exit(1)
