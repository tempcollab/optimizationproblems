# R4 UPPER certificate — j9 as SECOND A-base block (verify_upper_q8A.py)

CERTIFIED  log h <= **0.2538893183**  (strict beat of held R2 0.2538925359, margin +3.218e-6).

## Exact exponent vector (q1..q5, qB, qC, qE, qF, qG, qH)
q  = [14.011500, 13.443930, 2.643590, 2.299880, 0.252420]
qB = 0   qC = 0
qE = 0.575080   qF = 0.568800   qG = 0.891590 (j3, deg3)   qH = 0.066860 (j9, deg8, NEW)

## D
A-branch arg = sum q_i deg P_i + qG*3 + qH*8 = 61.65784
B-branch arg = 56 + qE*12 + qF*16            = 72.00176   <- WINS (perturber branch)
D = max(61.65784, 72.00176) = 72.00176

## Final arithmetic (hand-checked)
int_0^2pi G dt <= 114.8596292764
int_0^1 G ds   <= 18.2804777610
18.2804777610 / 72.00176 = 0.2538893182749978  ->  0.2538893183

## B&B
frontier FULLY RESOLVED: 0 unresolved cells, 742266 leaves, 6 refine rounds, ~437s.
cert (0.2538893183) - independent N=4M float (0.2538891201) slack = +1.98e-7 (expected band).

## Reproduce
cd constants/82a/certificate
python3 verify_upper_q8A.py anchor      # qH=0 BIT-IDENTICAL to verify_upper_q7A (float==, D==, cell np.array_equal)
python3 verify_upper_q8A.py admiss      # Doche cond (4) for {P1,P2,P4,P6,P8,j3,j9} vs {Q1,Q2,Q5,Q6}
python3 verify_upper_q8A.py selftest 14.011500 13.443930 2.643590 2.299880 0.252420 0 0 0.575080 0.568800 0.891590 0.066860   # 0/200 both caps
python3 verify_upper_q8A.py certify  14.011500 13.443930 2.643590 2.299880 0.252420 0 0 0.575080 0.568800 0.891590 0.066860 200000 14 1e-10   # ~7.5 min
python3 verify_upper_q8A.py tamper   14.011500 13.443930 2.643590 2.299880 0.252420 0 0 0.575080 0.568800 0.891590 0.066860 0.2538893100   # -> BEATS=False

Float re-optimization (joint 9-exponent multistart, N=80k opt then N=4M re-eval):
python3 opt_q8_scratch.py 0   (and 1, 2 for additional starts; all converge to the same basin)
