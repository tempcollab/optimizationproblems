"""Self-test: FFT J vs brute-force 4-fold sum on a small measure."""
import numpy as np
from itertools import product
from scratch.route3_J_fft import J_from_measure


def J_brute(pts, masses, tol=1e-10):
    M = len(pts)
    J = 0.0
    for a, b, c, d in product(range(M), repeat=4):
        v = pts[a] - pts[b] - pts[c] + pts[d]
        if abs(v) < tol:
            continue
        J += masses[a] * masses[b] * masses[c] * masses[d] * np.log(abs(v))
    return J


rng = np.random.default_rng(1)
M = 7
pts = rng.uniform(-1, 1, M) + 1j * rng.uniform(-1, 1, M)
masses = rng.uniform(0.1, 1, M); masses /= masses.sum()

Jb = J_brute(pts, masses)
print(f"brute J = {Jb:+.6f}")
for G in (256, 512, 1024, 2048):
    Jf = J_from_measure(pts, masses, G=G, pad=1.3)
    print(f"FFT  G={G:5d}: J = {Jf:+.6f}  err {Jf-Jb:+.5f}")
