"""Dev scratch: enumerate the admissible deg-4 bridge-support box, check P4=R0,
sanity-check the anchor margin reproduces r_R0=-0.0356, and count near-misses.
Run small/fast only; no heavy interval cert here."""
import sys, itertools, time
import numpy as np
import sympy as sp

sys.path.insert(0, "/home/agentuser/repo/constants/82a/certificate")
X = sp.Symbol("X")

POLY_COEFFS = {
    "P1": [1, 0],
    "P2": [-1, 1],
    "P4": [1, -2, 4, -3, 1],
    "P8": [1, -3, 7, -14, 30, -58, 96, -123, 114, -73, 31, -8, 1],
    "Q1": [1, -7, 30, -97, 269, -679, 1612, -3618, 7646, -15180, 28457, -50741,
           86189, -138288, 206152, -279897, 339335, -360911, 331775, -260367,
           172556, -95554, 43677, -16221, 4786, -1084, 178, -19, 1],
}

def _poly(coeffs):
    return sp.Poly.from_list([sp.Integer(c) for c in coeffs], gens=X, domain=sp.ZZ)

lib = {k: _poly(v) for k, v in POLY_COEFFS.items()}
core5 = (lib["P1"]**5) * (lib["P2"]**5)
Q1 = lib["Q1"]; P8 = lib["P8"]

def build_R_d(d_hl):
    """d_hl: high-to-low coeffs of the monic deg-4 multiplier d.
    R(d) = pp(Q1 - core5 * d * P8). Returns (content, pp) with positive LC."""
    d = _poly(d_hl)
    raw = Q1 - core5 * d * P8
    cont, pp = sp.Poly(raw.as_expr(), X, domain=sp.ZZ).primitive()
    if pp.LC() < 0:
        pp = sp.Poly(-pp.as_expr(), X, domain=sp.ZZ)
    return abs(int(cont)), pp

def admissible(d_hl):
    cont, pp = build_R_d(d_hl)
    if int(pp.degree()) != 28:
        return False, pp, cont, "deg!=28"
    if cont != 1:
        return False, pp, cont, "content!=1"
    if sp.gcd(pp, Q1).degree() != 0:
        return False, pp, cont, "not coprime Q1"
    if sp.gcd(pp, pp.diff(X)).degree() != 0:
        return False, pp, cont, "not squarefree"
    if not (pp.eval(0) == 1 and pp.eval(1) == 1):
        return False, pp, cont, "R(0)/R(1)!=1"
    return True, pp, cont, "OK"

# --- sanity: d=P4 reproduces R0 ---
P4_hl = [1, -2, 4, -3, 1]
ok, R0, cont0, msg = admissible(P4_hl)
print("P4 admissible:", ok, msg, "deg", int(R0.degree()), "cont", cont0)

# --- enumerate box: monic, c0=+1, |c1|,|c2|,|c3|<=4 ---
t0 = time.time()
box = []
for c3, c2, c1 in itertools.product(range(-4, 5), repeat=3):
    d_hl = [1, c3, c2, c1, 1]   # X^4 + c3 X^3 + c2 X^2 + c1 X + 1
    ok, pp, cont, msg = admissible(d_hl)
    if ok:
        box.append((d_hl, pp))
print(f"box raw=729, admissible={len(box)} ({time.time()-t0:.1f}s)")

# --- float anchor margins ---
def fev(coef_hl, chi):
    c = np.array([complex(int(x)) for x in coef_hl], dtype=np.complex128)
    v = np.zeros_like(chi) + c[0]
    for x in c[1:]:
        v = v * chi + x
    return v

NUMERATOR_Q = {"P1":26.511877484730615,"P2":23.782846008412744,"P3":0.9707094545190521,
    "P4":4.526072775020114,"P5":0.038326545650764404,"P6":4.173784226054273,"P8":1.685809173822071}
NUM_EXTRA = {"P3":[1,1,-2,1],"P5":[1,-2,4,-7,13,-16,12,-5,1]}
EXTRA_DENOM = {  # record denom blocks except Q1: Q2,R0,R2,P7,P9
    "P6":[1,-3,8,-16,26,-27,17,-6,1],
    "P7":[1,-3,8,-18,36,-62,97,-123,114,-73,31,-8,1],
    "P9":[1,-4,10,-17,26,-47,119,-298,592,-878,963,-780,464,-199,59,-11,1],
    "Q2":[1,-7,30,-96,255,-586,1212,-2360,4573,-9148,18749,-37783,71770,-124910,
          195848,-273368,335981,-359545,331349,-260271,172542,-95553,43677,-16221,
          4786,-1084,178,-19,1],
}
def coeffs_hl(name):
    if name in POLY_COEFFS: return POLY_COEFFS[name]
    if name in NUM_EXTRA: return NUM_EXTRA[name]
    return EXTRA_DENOM[name]

# Build R0,R2 for anchor denom (R2 = pp(Q2 + core5 P4 P7))
def build_R2():
    P7 = _poly(EXTRA_DENOM["P7"]); Q2 = _poly(EXTRA_DENOM["Q2"])
    raw = Q2 + core5*lib["P4"]*P7
    cont, pp = sp.Poly(raw.as_expr(), X, domain=sp.ZZ).primitive()
    if pp.LC()<0: pp = sp.Poly(-pp.as_expr(),X,domain=sp.ZZ)
    return pp
R2poly = build_R2()

Nfc = 2_000_000
edges = (np.arange(Nfc+1)/Nfc)*2*np.pi
m = 0.5*(edges[:-1]+edges[1:]); w = edges[1:]-edges[:-1]
z = np.exp(1j*m); chi = z*(1-z)
LOG_FLOOR=1e-300
Af = np.zeros_like(m)
for nm,q in NUMERATOR_Q.items():
    Af += q*np.log(np.maximum(np.abs(fev(coeffs_hl(nm),chi)),LOG_FLOOR))
denom_blocks = ["Q2","R0","R2","P7","P9"]  # anchor = record \ {Q1}
Bf = np.zeros_like(m)
for blk in denom_blocks:
    if blk=="R0": cf=[int(c) for c in R0.all_coeffs()]
    elif blk=="R2": cf=[int(c) for c in R2poly.all_coeffs()]
    else: cf=coeffs_hl(blk)
    Bf += np.log(np.maximum(np.abs(fev(cf,chi)),LOG_FLOOR))
om = Bf>Af
inv2pi=1/(2*np.pi); deg=28
def margin(pp):
    cf=[int(c) for c in pp.all_coeffs()]
    lP=np.log(np.maximum(np.abs(fev(cf,chi)),LOG_FLOOR))
    return (np.sum((w*lP)[om])*inv2pi)/deg
r_R0 = margin(R0)
print(f"r_R0 = {r_R0:+.5f}  (expect -0.03560)")

# margins over box
rows=[]
for d_hl,pp in box:
    rows.append((margin(pp), d_hl))
rows.sort()
print("\nTop 8 (most negative = strongest firing):")
for r,d in rows[:8]:
    print(f"  r_R={r:+.6f}  d={d}")
r_P4 = margin(R0)
gaps = [(r - r_P4, d) for r,d in rows]
nm3 = [g for g in gaps if g[0] < 3e-3]
print(f"\nP4 margin {r_P4:+.6f}; is P4 the unique min? {rows[0][1]==P4_hl}")
print(f"near-misses (float gap < 3e-3): {len(nm3)}")
for g,d in nm3:
    print(f"  gap={g:+.3e}  d={d}")
