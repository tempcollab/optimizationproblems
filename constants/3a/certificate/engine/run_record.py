"""
Compute ONE of the record counts (N+ or N-) for the C_3a base-21 record, with progress.

Usage:  python3 run_record.py plus    -> writes record_plus.txt
        python3 run_record.py minus   -> writes record_minus.txt
        python3 run_record.py max     -> writes record_max.txt

Record parameters: A={0,2,3,4,5,6,7,8,9,10}, B=21, d=80, T=150.
"""
import sys, time
from digit_dp import count_opset  # SINGLE source of truth for the DP (verified vs brute)

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
B = 21
d = 80
T = 150


def count(op):
    t = time.time()
    total = count_opset(A, d, T, op)
    print(f"  {op} DONE total digits={len(str(total))} elapsed {time.time()-t:.1f}s", flush=True)
    return total


def max_U():
    Amax = max(A)
    budget = T
    val = 0
    pos = d - 1
    while budget > 0 and pos >= 0:
        dig = min(Amax, budget)
        val += dig * (B ** pos)
        budget -= dig
        pos -= 1
    return val


if __name__ == "__main__":
    which = sys.argv[1]
    if which == 'plus':
        v = count('+')
        open('record_plus.txt', 'w').write(str(v) + '\n')
    elif which == 'minus':
        v = count('-')
        open('record_minus.txt', 'w').write(str(v) + '\n')
    elif which == 'max':
        v = max_U()
        open('record_max.txt', 'w').write(str(v) + '\n')
    print("WROTE", which, flush=True)
