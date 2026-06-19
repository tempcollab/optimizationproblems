# C_3a d=150 strict-beat certificate (Round 24)

## Claim
C_3a >= 239/203 = 1.1773399014778... (LOWER bound), strictly beating the R23 held
1177/1000 = 1.1770. True cell GHR value (display only) = 1.1774136588225.

## Construction
Carry-free drop-1 base-21 GHR digit set:
  A = {0,2,3,4,5,6,7,8,9,10}, B = 21, d = 150, T = 282 (density 1.8800).
  Carry-free holds: B = 21 > 2*max(A) = 20.
  U = { sum_{i<150} a_i 21^i : a_i in A, sum a_i <= 282 }.
  value(U) = 1 + log(|U-U|/|U+U|) / log(2 max(U)+1)   (GHR2007 lower bound on C_3a).

## Exact integers (beat_d150.json, cell d150_T282)
  |U+U| = Nplus   (146 digits)
  |U-U| = Nminus  (181 digits)
  max(U)= maxU    (199 digits)

## Wedge (load-bearing exact big-int inequality)
  c = 239/203 = 1 + 36/203,  P = 36, Q = 203.
  (a) value_new   >= c :  |U-U|^Q >= |U+U|^Q * (2 max(U)+1)^P   PASSES
  (b) value_record <  c :  RNm^Q  <  RNp^Q  * (2 RM+1)^P        PASSES (d=80 record cell)
  => value_record < c <= value_new (strict beat of the record AND held).

## Reproduce
  # numerical certificate (loads persisted integers, ~80s):
  python3 verify_beat.py
  # full from-scratch (recomputes the d=150 DP, diff/max ~140s + sumset ~770s):
  python3 verify_beat.py --recompute
  # diff/max sweep over T in {281,282,283}:    python3 run_d150_diffmax.py
  # heavy sumset for chosen T:                 python3 run_d150_engine.py 282

## Lean certificate (gold standard)
  Build target:   lake build Constants.C3a   (1980 jobs, ~76s, PASS)
  Theorems added (lean/Constants/C3a.lean), all prior theorems left intact:
    newGE150, recLT150, Nplus150_pos, Nplus150_le_Nminus150, Q4_pos,
    c3a_ge_239_203, c3a_ge_239_203'
  Axiom audit (audit150.lean, via `lake env lean`):
    newGE150               : [propext]
    recLT150               : [propext]
    Nplus150_pos           : (no axioms)
    Nplus150_le_Nminus150  : (no axioms)
    Q4_pos                 : (no axioms)
    c3a_ge_239_203         : [propext, Classical.choice, Quot.sound]
    c3a_ge_239_203'        : [propext, Classical.choice, Quot.sound]
  NO sorryAx, NO native_decide/ofReduceBool, NO new/smuggled axiom.
  The only trust boundary is the named hypothesis GHR_lower (GHR2007 analytic
  theta-bridge), carried on the theorem signature — NOT an axiom.
