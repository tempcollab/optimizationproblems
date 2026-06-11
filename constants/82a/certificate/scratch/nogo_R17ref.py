"""
Tie the no-go directly to the EXISTING R17 improvement.

The R17 lower-bound improvement (0.2524) used the OSS ENERGY column (n=1) at a
frozen diffuse z->1-z symmetric reference mu0 (frozen_energy.npz): 15 arcs, L=0.057,
with C_1(mu0) = Ihat = -0.2112 < 0 (the energy cut binds, lambda0=0.0401).

DECISIVE: reconstruct THAT SAME reference mu0 and compute its HIGHER signed-sum
moments C_n(mu0) for n=2,3,4 (k=4,6,8). If C_1<0 but C_n>=0 for n>=2, it shows the
energy (n=1) is the UNIQUE useful member of the hierarchy and every higher moment is
interior even at the very reference that made n=1 work -> the rest of the hierarchy
adds nothing.
"""
import numpy as np
from scratch.nogo_Cmu0 import C_n_from_measure, conj_sym, zz_sym

d = np.load('frozen_energy.npz')
centers = d['centers']      # arc centers in t on (0,pi) half? check range
masses = d['masses']
L = float(d['L'])
print(f"R17 frozen mu0: {len(centers)} arcs, L={L:.5f}")
print(f"  centers (t): {np.round(centers,3)}")
print(f"  Ihat (= C_1 energy of mu0, reported) = {float(d['Ihat']):+.6f}")
print(f"  lambda0={float(d['lambda0']):.5f}  m_cut={float(d['m_cut']):.6f}\n")

# Reconstruct the diffuse measure: each arc center spread over its width L, then
# conj-symmetrize and z->1-z symmetrize (the frozen measure is already built that way
# in freeze_energy; here we rebuild atoms to feed the C_n FFT).
nper = 12
sub = (np.arange(nper) + 0.5) / nper * L - L / 2
t_atoms = (centers[:, None] + sub[None, :]).ravel()
m_atoms = (masses[:, None] * np.ones(nper)[None, :] / nper).ravel()
m_atoms /= m_atoms.sum()

# conj + z->1-z symmetrize
z, m = conj_sym(t_atoms, m_atoms)
pts, ms = zz_sym(z, m)

print("C_n(R17 mu0) for the SIGNED-SUM hierarchy (same reference that made n=1 work):")
for n in (1, 2, 3, 4):
    for G in (384, 512):
        c = C_n_from_measure(pts, ms, n, G=G)
        tag = "  (= energy, NEGATIVE -> R17 cut)" if n == 1 else ""
        print(f"  n={n} (k={2*n})  G={G}: C_n = {c:+.6f}{tag}")
print("\nIf n=1 < 0 but n>=2 >= 0: the energy is the unique useful moment; the higher")
print("signed-sum columns are interior at the very reference that powers R17 -> no-go.")
