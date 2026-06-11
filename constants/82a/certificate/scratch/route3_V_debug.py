"""
Debug V_mu0 vs J consistency. The identity to hold:
   INT V_mu0(y) dmu0(y) = J(mu0),  V_mu0(y)=INT^3 log|y-x2-x3+x4| dmu0^3.
Test on a small atomic measure with brute force (no FFT), to find the structural
bug, THEN fix the FFT V_pot.
"""
import numpy as np
from itertools import product

rng = np.random.default_rng(0)
M = 6
pts = rng.uniform(-1, 1, M) + 1j * rng.uniform(-1, 1, M)
ms = rng.uniform(0.1, 1, M); ms /= ms.sum()


def J_brute(pts, ms, tol=1e-10):
    J = 0.0
    for a, b, c, d in product(range(len(pts)), repeat=4):
        v = pts[a] - pts[b] - pts[c] + pts[d]
        if abs(v) < tol:
            continue
        J += ms[a] * ms[b] * ms[c] * ms[d] * np.log(abs(v))
    return J


def V_brute(y, pts, ms, tol=1e-10):
    """V(y) = INT^3 log|y - x2 - x3 + x4| dmu^3 (x2,x3,x4 ~ mu)."""
    V = 0.0
    for b, c, d in product(range(len(pts)), repeat=3):
        v = y - pts[b] - pts[c] + pts[d]
        if abs(v) < tol:
            continue
        V += ms[b] * ms[c] * ms[d] * np.log(abs(v))
    return V


Jb = J_brute(pts, ms)
# INT V dmu0
IV = sum(ms[a] * V_brute(pts[a], pts, ms) for a in range(M))
print(f"J(mu0)            = {Jb:+.6f}")
print(f"INT V_mu0 dmu0    = {IV:+.6f}   (should equal J)")
print(f"match: {abs(Jb-IV)<1e-9}")

# So V(y)=INT log|y-x2-x3+x4| dmu^3. In terms of the S3 distribution:
# let S3 = x2 + x3 - x4 (NOTE sign!). Then y - x2 - x3 + x4 = y - S3. So
#   V(y) = INT log|y - S3| dP_{S3}(S3),  S3 = x2 + x3 - x4.
# My FFT used S3 = x4 - x2 - x3 and V=INT log|y+s| -> y+s = y + x4-x2-x3 = y -(x2+x3-x4).
# That's y - S3 with S3=x2+x3-x4. log|y+s| with s=x4-x2-x3 = log|y -(x2+x3-x4)| -> CORRECT.
# Check via the S3=x2+x3-x4 distribution directly (brute):
def V_via_S3(y, pts, ms):
    V = 0.0
    for b, c, d in product(range(len(pts)), repeat=3):
        s3 = pts[b] + pts[c] - pts[d]
        v = y - s3
        if abs(v) < 1e-10: continue
        V += ms[b]*ms[c]*ms[d]*np.log(abs(v))
    return V
IV2 = sum(ms[a]*V_via_S3(pts[a],pts,ms) for a in range(M))
print(f"INT V(S3=x2+x3-x4) dmu0 = {IV2:+.6f}  match J: {abs(Jb-IV2)<1e-9}")

# ---- now test the FFT V_pot from route3_cut_lowJ against brute ----
from scratch.route3_cut_lowJ import S3_dist, V_pot
# atomic measure as point masses
P3, h3, c03 = S3_dist(pts, ms, G=512, pad=1.4)
yq = pts.copy()
Vfft = V_pot(yq, P3, h3, c03)
Vbr = np.array([V_brute(y, pts, ms) for y in yq])
print("\nFFT V_pot vs brute V at the support points:")
for i in range(M):
    print(f"  y={yq[i]:+.3f}: FFT={Vfft[i]:+.5f}  brute={Vbr[i]:+.5f}  err={Vfft[i]-Vbr[i]:+.5f}")
IVfft = float(ms @ Vfft)
print(f"INT V_fft dmu0 = {IVfft:+.5f}  vs J={Jb:+.5f}  err={IVfft-Jb:+.5f}")
