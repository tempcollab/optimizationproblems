"""First-variation diagnostic for the current record (Grinsztajn denominator-first bound).

NOTE ON RIGOR: the marginals here are fine-GRID evaluations, not interval certificates.
The paper states the corresponding Proposition as a numerical diagnostic, not a theorem.
A rigorous interval certificate of the Gri26 deg-140 bound in our own harness is a
separate, still-open milestone (it would upgrade the diagnostic to a certified statement).


The current record upper bound for mu^ess(h_Z), log h <= 0.2536331090 (certified by
the maaxgrin/zhang-zagier-c82-bound repository), is built denominator-first: a fixed
denominator Q = Q1 Q2 R0 R2 P7 P9 (deg 140) with two NEW near-cancellation factors

    R0 = primitive_part(Q1 - P1^5 P2^5 P4 . P8),
    R2 = primitive_part(Q2 + P1^5 P2^5 P4 . P7),

and an LP-tuned numerator A = sum_i q_i log|P_i| over P1..P6,P8. This script verifies,
to the resolution of a fine midpoint grid, three claims used in the paper's
"the criterion accounts for the record" section:

  (1) FUNCTIONAL IDENTITY. Their denominator-first value
      (log M(Q) + int_0^1 (A-B)^+ ds) / deg Q
      equals our Phi/D = int_0^1 max(A,B) ds / deg Q (Jensen: int B = log M(Q)),
      and both reproduce their reported candidate 0.2536269210.

  (2) ENTRY (firing) condition. Each denominator block R0, R2, P7, P9 fires by the
      perturbing-block criterion r_Q < log h evaluated at the CANDIDATE-FREE anchor
      (the family with that block removed): r_Q is strongly negative for all four,
      while generic non-construction blocks (P3, P5, X^2-X+1) are correctly dry.

  (3) OPTIMALITY (stationarity) reading. At their optimum the active perturbing
      blocks cluster on the criterion's stationarity locus r_Q ~ log h (KKT /
      complementary slackness), as the optimality statement of the criterion predicts;
      the small uniform offset is consistent with the denominator exponents being
      held at multiplicity one rather than driven to interior stationarity.

This is an EXPLANATORY check: the criterion fires on / accounts for their blocks. It
does NOT generate R0, R2 from scratch. No bound of this repository depends on it.

Run:  python3 firstvar_07_record_blocks.py
Requires:  numpy, sympy  (and the maaxgrin polynomial data, reproduced inline below
           so the check is self-contained and does not depend on an external clone).
"""

import math

import numpy as np
import sympy as sp

X = sp.Symbol("X")

# --- maaxgrin polynomial data (high-to-low integer coefficients), reproduced inline.
POLY_COEFFS = {
    "P1": [1, 0],
    "P2": [-1, 1],
    "P3": [1, 1, -2, 1],
    "P4": [1, -2, 4, -3, 1],
    "P5": [1, -2, 4, -7, 13, -16, 12, -5, 1],
    "P6": [1, -3, 8, -16, 26, -27, 17, -6, 1],
    "P7": [1, -3, 8, -18, 36, -62, 97, -123, 114, -73, 31, -8, 1],
    "P8": [1, -3, 7, -14, 30, -58, 96, -123, 114, -73, 31, -8, 1],
    "P9": [1, -4, 10, -17, 26, -47, 119, -298, 592, -878, 963, -780, 464, -199, 59, -11, 1],
    "Q1": [1, -7, 30, -97, 269, -679, 1612, -3618, 7646, -15180, 28457, -50741, 86189,
           -138288, 206152, -279897, 339335, -360911, 331775, -260367, 172556, -95554,
           43677, -16221, 4786, -1084, 178, -19, 1],
    "Q2": [1, -7, 30, -96, 255, -586, 1212, -2360, 4573, -9148, 18749, -37783, 71770,
           -124910, 195848, -273368, 335981, -359545, 331349, -260271, 172542, -95553,
           43677, -16221, 4786, -1084, 178, -19, 1],
}

# maaxgrin certified record (their run file qstar_cert_roots_262144_target253635.jsonl)
THEIR_CERTIFIED = 0.2536331090204145
THEIR_CANDIDATE = 0.2536269209592403

# maaxgrin LP-optimized numerator exponents at the record (their targeted_refined run)
NUMERATOR_Q = {
    "P1": 26.511877484730615,
    "P2": 23.782846008412744,
    "P3": 0.9707094545190521,
    "P4": 4.526072775020114,
    "P5": 0.038326545650764404,
    "P6": 4.173784226054273,
    "P8": 1.685809173822071,
}
DENOMINATOR = ["Q1", "Q2", "R0", "R2", "P7", "P9"]

GRID_N = 8_000_000
LOG_FLOOR = 1e-300
TWO_PI = 2.0 * math.pi
ENTRY_THRESHOLD_NEGATIVE = -0.01   # firing r_Q must be clearly below 0 (well under log h)
STATIONARY_TOL = 0.02              # active-block clustering tolerance for r_Q ~ log h


def _poly_from_coeffs(coeffs):
    return sp.Poly.from_list([sp.Integer(c) for c in coeffs], gens=X, domain=sp.ZZ)


def _build_library():
    lib = {name: _poly_from_coeffs(c) for name, c in POLY_COEFFS.items()}
    bridge = (lib["P1"] ** 5) * (lib["P2"] ** 5) * lib["P4"]
    R0 = sp.Poly((lib["Q1"] - bridge * lib["P8"]).as_expr(), X, domain=sp.ZZ).primitive()[1]
    R2 = sp.Poly((lib["Q2"] + bridge * lib["P7"]).as_expr(), X, domain=sp.ZZ).primitive()[1]
    lib["R0"] = R0 if R0.LC() > 0 else sp.Poly(-R0.as_expr(), X, domain=sp.ZZ)
    lib["R2"] = R2 if R2.LC() > 0 else sp.Poly(-R2.as_expr(), X, domain=sp.ZZ)
    # X^2 - X + 1, the cheapest coprime control factor from the saturation section.
    lib["XX"] = _poly_from_coeffs([1, -1, 1])
    return lib


def _degree(poly):
    return int(poly.degree())


def _log_abs_on_chi(poly, chi):
    coeffs = np.array([complex(int(c)) for c in poly.all_coeffs()], dtype=np.complex128)
    val = np.zeros_like(chi) + coeffs[0]
    for c in coeffs[1:]:
        val = val * chi + c
    return np.log(np.maximum(np.abs(val), LOG_FLOOR))


def _log_mahler(poly):
    """log M(Q(z(1-z))) via the roots xi of Q and z^2 - z + xi = 0 for each xi."""
    coeffs = np.array([complex(int(c)) for c in poly.all_coeffs()], dtype=np.complex128)
    if len(coeffs) <= 1:
        return 0.0
    total = math.log(abs(coeffs[0].real)) if coeffs[0] != 0 else -math.inf
    for xi in np.roots(coeffs):
        root = np.sqrt(np.complex128(1.0 - 4.0 * xi))
        rp, rm = (1.0 + root) / 2.0, (1.0 - root) / 2.0
        total += math.log(max(1.0, abs(rp))) + math.log(max(1.0, abs(rm)))
    return float(total)


def main():
    lib = _build_library()
    t = (np.arange(GRID_N) + 0.5) / GRID_N
    u = np.exp(1j * TWO_PI * t)
    chi = u * (1.0 - u)

    log_abs = {name: _log_abs_on_chi(lib[name], chi) for name in set(NUMERATOR_Q) | set(DENOMINATOR) | {"P3", "P5", "XX"}}

    A = np.zeros(GRID_N)
    for name, q in NUMERATOR_Q.items():
        A += q * log_abs[name]
    deg_Q = sum(_degree(lib[b]) for b in DENOMINATOR)
    B = np.zeros(GRID_N)
    for b in DENOMINATOR:
        B += log_abs[b]

    ok = True

    # (1) Functional identity.
    our_phi_over_D = float(np.mean(np.maximum(A, B)) / deg_Q)
    log_M_Q = sum(_log_mahler(lib[b]) for b in DENOMINATOR)
    their_form = float((log_M_Q + np.mean(np.maximum(0.0, A - B))) / deg_Q)
    id_gap = abs(our_phi_over_D - their_form)
    cand_gap = abs(our_phi_over_D - THEIR_CANDIDATE)
    print("(1) FUNCTIONAL IDENTITY")
    print(f"    our  Phi/D                 = {our_phi_over_D:.10f}")
    print(f"    their (logM(Q)+int(A-B)+)/dQ = {their_form:.10f}")
    print(f"    |identity gap|             = {id_gap:.2e}   (Jensen: int B = log M(Q))")
    print(f"    vs their candidate         = {cand_gap:.2e}")
    ok &= id_gap < 1e-6 and cand_gap < 1e-6

    log_h = our_phi_over_D

    # (2) Entry (firing) condition at the candidate-free anchor.
    print("\n(2) ENTRY: r_Q < log h at the CANDIDATE-FREE anchor (block removed)")
    print(f"    {'block':6}{'deg':>4}{'r_Q (cand-free)':>18}{'fire?':>8}")
    for blk in ["R0", "R2", "P7", "P9"]:
        dQ = _degree(lib[blk])
        B_free = np.zeros(GRID_N)
        for b in DENOMINATOR:
            if b != blk:
                B_free += log_abs[b]
        mask = B_free > A
        r_free = float(np.mean(log_abs[blk][mask]) / dQ)
        fires = r_free < ENTRY_THRESHOLD_NEGATIVE
        print(f"    {blk:6}{dQ:>4}{r_free:>18.6f}{('YES' if fires else 'no'):>8}")
        ok &= fires

    print("    controls (generic non-construction blocks, full active set) should be DRY:")
    mask_full = B > A
    for blk in ["P3", "P5", "XX"]:
        dQ = _degree(lib[blk])
        r_ctrl = float(np.mean(log_abs[blk][mask_full]) / dQ)
        dry = r_ctrl >= log_h
        label = "X^2-X+1" if blk == "XX" else blk
        print(f"    {label:8} deg={dQ:<2} r_Q={r_ctrl:>10.6f}  dry (r_Q>=log h)? {dry}")
        ok &= dry

    # (3) Optimality (stationarity) reading at their optimum.
    print("\n(3) OPTIMALITY: active perturbing blocks cluster on r_Q ~ log h at their optimum")
    print(f"    log h = {log_h:.8f}")
    offsets = []
    for blk in DENOMINATOR:
        dQ = _degree(lib[blk])
        r_opt = float(np.mean(log_abs[blk][mask_full]) / dQ)
        offsets.append(r_opt - log_h)
        print(f"    {blk:6}{dQ:>4}  r_Q={r_opt:>10.6f}  r_Q - log h = {r_opt - log_h:+.6f}")
    spread = max(offsets) - min(offsets)
    print(f"    cluster spread = {spread:.6f}  (tight spread => common stationarity locus)")
    ok &= all(abs(o) < STATIONARY_TOL for o in offsets) and spread < 0.01

    print("\n" + ("PASS: the criterion diagnoses the current record (grid evaluation)." if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
