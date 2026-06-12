"""
R5 BLOCK-SWAP screen for the 82a UPPER bound (Angle 1 of the R5 outline).

Held R4 active dictionary:
  base  (A-branch, prod-P^q side): {P1,P2,P4,P6,P8, j3, j9}
  perturber (B-branch):            {Q1,Q2, Q5=j13, Q6=j15}
held R4 optimum float = 0.2538891201 (N-stable 400k/4M); certified 0.2538893183.

This screen takes a SWAP candidate: remove a weak active block (default the thin
deg-8 A-base block j9, qH=0.066860) and substitute a different ADMISSIBLE Flammang
Table-1 block as the A-base block in its slot, then JOINTLY re-optimize all 9
free exponents (5 q's + qE,qF,qG + the swapped slot exponent qX) by Nelder-Mead.

It reuses bound_07_block_j9.float_value_q8A but substitutes Q8 (the j9 slot) by the
swap-in block's coefficient list.  Because float_value_q8A reads the module globals
Q7 (j3) and Q8 (the swap slot), we monkeypatch q8.Q8 / q8.DEG_Q8 etc. for each
candidate.  (The certified harness will be cloned separately for any winner.)

CHEAP-FIRST per the anti-stall rule:
  - sympy admissibility (coprimality to the rest of the dictionary, Doc01a cond (4))
    is checked BEFORE any float work; an inadmissible candidate is skipped.
  - joint float re-opt at N=400k (optimizer), then re-eval best at N=400k AND N=4M.
  - the >=5e-6 N-STABLE drop gate over 0.2538893183 (current held cert) is read.

A BASE block need NOT satisfy P(0)=P(1)=1 (Doc01a: only condition (4) +
coprimality).  We DO require: deg>0, squarefree, coprime to every other active
factor {P1,P2,P4,P6,P8,j3} base side and {Q1,Q2,Q5,Q6} perturber side, and != j9
itself (a no-op swap).

Usage:
  python3 screen_swap_R5.py admiss            # admissibility table for all candidates
  python3 screen_swap_R5.py float <jname> <startidx>   # one candidate, one start
  python3 screen_swap_R5.py baseline          # re-eval R4 held float (j9 in slot)

jname is one of the Flammang Table-1 block ids: j4,j5,j6,j7,j8,j10,j11,j12,j14, ...
"""
import os
import sys
import time
import numpy as np
import sympy as sp

import bound_01_doche_base as vu
import bound_07_block_j9 as q8
import flammang_table1 as ft

# ---- the current held CERT value to beat (R4), and the N-stable gate ----
HELD_R4_CERT = 0.2538893183
GATE = 5e-6

# R4 held optimum (j9 in the swap slot), the seed for re-optimization
R4_Q = [14.011500, 13.443930, 2.643590, 2.299880, 0.252420]
R4_QE, R4_QF, R4_QG, R4_QH = 0.575080, 0.568800, 0.891590, 0.066860

# Flammang Table-1 descending-coeff blocks, by j index (descending = q8 convention)
_TAB = {j + 1: desc for j, (c, desc) in enumerate(ft._TABLE_DESCENDING)}

# The active dictionary OTHER than the swap slot (j9):
#   base side keeps {P1,P2,P4,P6,P8, j3};  perturber side {Q1,Q2,Q5,Q6}
J3 = [1, 1, -2, 1]
J9 = [1, -1, 0, -3, 15, -22, 16, -6, 1]


def _sym(desc):
    X = sp.symbols('X')
    n = len(desc) - 1
    return sum(int(v) * X**(n - i) for i, v in enumerate(desc)), X


def admissibility(desc, name, verbose=True):
    """Return (ok, info) for using `desc` as the A-base swap-in block, replacing j9.

    Active dictionary (j9 removed, candidate added):
      base side:  P1,P2,P4,P6,P8, j3, CAND
      pert side:  Q1,Q2,Q5,Q6
    Doche cond (4): the whole integer-poly dictionary pairwise coprime, CAND deg>0,
    squarefree.  A base block need NOT have P(0)=P(1)=1.
    """
    X = sp.symbols('X')

    def sym(c):
        n = len(c) - 1
        return sum(int(v) * X**(n - i) for i, v in enumerate(c))
    cand = sym(desc)
    deg = len(desc) - 1
    info = {}
    info['deg'] = deg
    info['deg>0'] = deg > 0
    sq = (sp.gcd(cand, sp.diff(cand, X)) == 1)
    info['squarefree'] = bool(sq)
    info['not_j9'] = (sp.expand(cand - sym(J9)) != 0)
    info['not_j3'] = (sp.expand(cand - sym(J3)) != 0)
    # coprime to base side {P1,P2,P4,P6,P8, j3}
    base_polys = [("P1", vu.P1), ("P2", vu.P2), ("P4", vu.P4),
                  ("P6", vu.P6), ("P8", vu.P8), ("j3", J3)]
    base_ok = True
    for nm, pc in base_polys:
        g = (sp.gcd(cand, sym(pc)) == 1)
        base_ok = base_ok and bool(g)
        info[f'cop_{nm}'] = bool(g)
    # coprime to perturbers {Q1,Q2,Q5,Q6}
    Q5 = list(q8.Q5); Q6 = list(q8.Q6)
    pert_polys = [("Q1", list(vu.Q1)), ("Q2", list(vu.Q2)),
                  ("Q5", Q5), ("Q6", Q6)]
    pert_ok = True
    for nm, pc in pert_polys:
        g = (sp.gcd(cand, sym(pc)) == 1)
        pert_ok = pert_ok and bool(g)
        info[f'cop_{nm}'] = bool(g)
    ok = (info['deg>0'] and info['squarefree'] and info['not_j9']
          and info['not_j3'] and base_ok and pert_ok)
    info['ADMISSIBLE'] = ok
    if verbose:
        print(f"  [{name}] deg={deg} sqfree={info['squarefree']} "
              f"!=j9={info['not_j9']} base_cop={base_ok} pert_cop={pert_ok} "
              f"-> ADMISSIBLE={ok}")
    return ok, info


def set_swap_block(desc):
    """Monkeypatch the q8A module's Q8 slot (the swap slot) to `desc`."""
    q8.Q8 = list(desc)
    q8.DEG_Q8 = len(desc) - 1
    q8.ASC_Q8 = vu.asc(list(desc))


def float_swap(q, qE, qF, qG, qX, N):
    """float value of h with the swap block in the j9 slot (qX = its exponent)."""
    return q8.float_value_q8A(list(q), 0.0, 0.0, qE, qF, qG, qX, N=N)


def reopt(desc, name, startidx, N_opt=120_000):
    from scipy.optimize import minimize
    set_swap_block(desc)
    # seed: R4 optimum, swap-slot exponent seeded near j9's qH and a couple of scales
    base = np.array(R4_Q + [R4_QE, R4_QF, R4_QG, R4_QH])
    if startidx == 0:
        s = base.copy()
    elif startidx == 1:
        # larger swap-slot exponent (a heavier candidate may want more weight)
        s = base.copy(); s[8] = 0.3
    elif startidx == 2:
        s = base.copy(); s[8] = 0.0  # DRY-recovery start (recovers R2 q7A family)
    else:
        rng = np.random.default_rng(500 + startidx)
        s = base * (1 + rng.uniform(-0.05, 0.05, size=9))
        s[8] = abs(0.15 * (1 + rng.uniform(-0.8, 0.8)))

    def obj(x):
        q = x[:5]; qE = x[5]; qF = x[6]; qG = x[7]; qX = x[8]
        if min(q) < 0 or qE < 0 or qF < 0 or qG < 0 or qX < 0:
            return 1.0
        return float_swap(q, qE, qF, qG, qX, N_opt)
    # resume from checkpoint if present (warm-start a long descent across timeouts)
    ckpt = f'/tmp/swap_{name}_ckpt.npy'
    if startidx == 99 and os.path.exists(ckpt):
        s = np.load(ckpt)
        print(f"   [{name}] RESUMING from checkpoint {s.tolist()}", flush=True)
    t0 = time.time()
    state = {'n': 0, 'best': 1.0, 'bestx': s.copy()}

    def cb(xk):
        state['n'] += 1
        v = obj(xk)
        if v < state['best']:
            state['best'] = v
            state['bestx'] = xk.copy()
            np.save(ckpt, xk)  # checkpoint best-so-far so a timeout doesn't lose it
        if state['n'] % 50 == 0:
            print(f"   [{name} s{startidx}] iter {state['n']} best={state['best']:.10f} "
                  f"{time.time()-t0:.0f}s", flush=True)
    res = minimize(obj, s, method='Nelder-Mead', callback=cb,
                   options=dict(maxiter=4000, maxfev=4000, xatol=1e-8, fatol=1e-12))
    x = res.x if res.fun <= state['best'] else state['bestx']
    v400 = float_swap(x[:5], x[5], x[6], x[7], x[8], 400_000)
    v4M = float_swap(x[:5], x[5], x[6], x[7], x[8], 4_000_000)
    drop = HELD_R4_CERT - max(v400, v4M)  # conservative: use the larger float
    nstab = abs(v400 - v4M)
    print(f"[{name} start{startidx}] f(opt N={N_opt})={res.fun:.10f} "
          f"qX*={x[8]:.6f}  nfev={res.nfev}  {time.time()-t0:.0f}s", flush=True)
    print(f"   re-eval: N=400k={v400:.10f}  N=4M={v4M:.10f}  "
          f"|400k-4M|={nstab:.2e}  drop_vs_R4held={drop:.3e}  "
          f"GATE(>=5e-6 & stable)={'PASS' if (drop>=GATE and nstab<GATE/2) else 'fail'}",
          flush=True)
    print(f"   x={np.round(x,6).tolist()}", flush=True)
    # persist best
    bestfile = f'/tmp/swap_{name}_best.npy'
    np.save(bestfile, np.concatenate([x, [v400, v4M]]))
    return x, v400, v4M, drop, nstab


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "admiss"

    # candidate swap-in blocks: all Flammang Table-1 blocks not already active
    # (active base: j3, and the swap slot j9 we are replacing; active pert: j13,j15).
    # We screen a broad set ranked roughly by degree (low first) plus a few mid.
    CANDS = [4, 5, 6, 7, 8, 10, 11, 12, 14, 16, 17, 18, 19]

    if mode == "admiss":
        print("=== R5 SWAP admissibility screen (candidate replaces j9 as A-base) ===")
        for j in CANDS:
            desc = _TAB[j]
            admissibility(desc, f"j{j}")
    elif mode == "baseline":
        # re-eval R4 held float with j9 IN the slot (sanity)
        set_swap_block(J9)
        for N in (400_000, 4_000_000):
            v = float_swap(R4_Q, R4_QE, R4_QF, R4_QG, R4_QH, N)
            print(f"baseline (j9 in slot) N={N}: {v:.10f}")
    elif mode == "float":
        jname = sys.argv[2]
        j = int(jname[1:])
        startidx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        desc = _TAB[j]
        ok, info = admissibility(desc, jname)
        if not ok:
            print(f"  {jname} INADMISSIBLE -- skipping float.")
            sys.exit(1)
        reopt(desc, jname, startidx)
    else:
        print("unknown mode")
        sys.exit(1)
