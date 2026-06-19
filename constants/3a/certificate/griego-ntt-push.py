#!/usr/bin/env python3
"""
Sketch `griego-ntt-push` — fast convolution DP to push the Griego family to m=130-200.

Constant C_3a (Gyarmati-Hennecart-Ruzsa sum-difference exponent), LOWER bound.
Held (verified, R3/R4): C_3a > 1.176 at (m,T)=(110,210) on A={0,2,...,10}, b=21.
Goal of THIS sketch: reach m=130-200 on the SAME family to climb toward the family
supremum Lambda ~ 1.185 (conjectural curve fit, < 1.25 GHR cap), e.g. (per the scout's
power-law fit) m=130 ~ theta 1.1764, m=150 ~ 1.1770, m=200 ~ 1.1779.

WHY A NEW ALGORITHM IS NEEDED (the compute wall, scout R4):
The R3 dynamic-low-clamp sum-set bitmask DP closes m<=110 in seconds, but at m=130+ the
reachable-Sigma_x mask width grows with T and the clamp no longer keeps it tractable — a single
m=130 point did not finish in ~5 min of scouting. To go past m=110 the sum-set count must be
computed by a fast-convolution path where m enters LOGARITHMICALLY (repeated squaring) or the
per-layer convolution is FFT/NTT-accelerated.

PLAN (holes are NotImplementedError / TODO):
  HOLE 1 (fast_sumset_count): exact |U+U| via NTT/FFT-accelerated convolution along the
          digit-sum (cap) axis, with repeated squaring in m. The per-column generating object is
          the indicator over reachable Sigma_x; combining columns is a (max,+)/set convolution that
          must be done EXACTLY (no float rounding may corrupt an integer count) — so NTT over a
          prime modulus (or exact integer FFT) on the bitmask, NOT float FFT, unless float error is
          rigorously bounded below 0.5.
  HOLE 2 (validate_fast_dp): the fast count MUST be validated exactly against the R3 clamped-DP
          oracle (imported from griego-family-larger-mT) on a spread of (m,T) BEFORE any large-m
          number is trusted — Rule (R3): a fast-but-wrong DP fabricates a bound. Validate on
          contiguous AND non-contiguous alphabets and clamp-exercising cases.
  HOLE 3 (scan_large_m): with HOLE 1+2 done, scan m in 120..200 along the optimal ray T~1.9m,
          PRINTING EACH POINT INCREMENTALLY (Rule R2: never a single silent Bash > ~5 min;
          checkpoint per point), and emit the exact (s,d,M) + integer certificate at the best point.
  HOLE 4 (certify): at the best m, emit the cleared-denominator integer inequality
          d^den > s^den*(2M+1)^(num-den) with the largest k/10000 that holds — same certificate
          FORM as the held 1.176, just at a higher-theta point.

Run: python3 griego-ntt-push.py   (prints the plan; holes raise cleanly)
"""
import importlib.util
import os

# Import the verified R3/R4 clamped-DP oracle (the validation ground truth).
_L2 = os.path.join(os.path.dirname(__file__), "griego-family-larger-mT.py")
_spec = importlib.util.spec_from_file_location("griego_l2", _L2)
griego_l2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(griego_l2)

A_GRIEGO = griego_l2.A_GRIEGO   # [0,2,3,4,5,6,7,8,9,10]
B_GRIEGO = griego_l2.B_GRIEGO   # 21

# count_diffset and max_U already scale (the 2-D DP and greedy are cheap at m=200);
# only the SUM-SET count is the wall. Reuse the cheap ones:
count_diffset = griego_l2.count_diffset
max_U = griego_l2.max_U
clamped_sumset = griego_l2.count_sumset   # the R3 oracle, exact but slow past m~110


# ----------------------------------------------------------------- HOLE 1
def fast_sumset_count(A, m, T):
    """EXACT |U+U| via NTT/FFT-accelerated convolution + repeated squaring in m.
       Must be exact (no float rounding corrupting integer counts)."""
    raise NotImplementedError(
        "HOLE 1: implement exact fast sum-set count (NTT over a prime modulus or exact "
        "integer FFT on the reachable-Sigma_x bitmask, repeated squaring in m). "
        "Float FFT only if rounding error is rigorously bounded < 0.5.")


# ----------------------------------------------------------------- HOLE 2
def validate_fast_dp(cases=((2, 5), (3, 8), (4, 10), (4, 12), (5, 14), (3, 15),
                            (4, 40), (5, 20), (6, 18), (5, 22), (4, 9), (6, 15))):
    """Validate fast_sumset_count EXACTLY against the R3 clamped-DP oracle (and brute force
       for the smallest), BEFORE trusting any large-m count. Rule R3."""
    for (m, T) in cases:
        fast = fast_sumset_count(A_GRIEGO, m, T)   # raises until HOLE 1 done
        slow = clamped_sumset(A_GRIEGO, m, T)
        assert fast == slow, f"FAST DP MISMATCH at m={m} T={T}: fast={fast} oracle={slow}"
    print(f"[validate] fast sum-set DP matches the clamped-DP oracle on {len(cases)} cases.")


# ----------------------------------------------------------------- HOLE 3
def scan_large_m(m_lo=120, m_hi=200, step=10):
    """Scan m in [m_lo, m_hi] along the optimal ray T ~ 1.9*m; PRINT EACH POINT INCREMENTALLY
       (Rule R2). Find the highest-theta point; return its (m,T,s,d,M)."""
    raise NotImplementedError(
        "HOLE 3: scan m=120..200, T~1.9m, using fast_sumset_count (validated). Print each "
        "(m,T,theta,s,d,M) as it completes (checkpoint per point; no single silent >5min run).")


# ----------------------------------------------------------------- HOLE 4
def certify_best(m, T):
    """Emit the largest k/10000 with d^10000 > s^10000*(2M+1)^(k-10000) at the best (m,T) —
       same certificate form as the held 1.176, at a higher theta."""
    raise NotImplementedError(
        "HOLE 4: at the best (m,T), compute exact (s,d,M) and the largest k/10000 that the "
        "integer inequality holds for; that k/10000 is the new held candidate (> 1.176).")


def main():
    print("Sketch griego-ntt-push: fast convolution DP to reach m=130-200 on A={0,2,..,10}, b=21.")
    print("Held to beat: C_3a > 1.176 at (110,210). Target: m=130-200, theta toward Lambda~1.185.")
    print("Oracle for validation: griego-family-larger-mT clamped DP (imported).")
    print("Holes: 1 fast_sumset_count, 2 validate_fast_dp, 3 scan_large_m, 4 certify_best.")
    # Sanity: the imported oracle and cheap DPs still run at a small point.
    m, T = 6, 15
    print(f"  oracle sanity (m={m},T={T}): |U+U|={clamped_sumset(A_GRIEGO,m,T)} "
          f"|U-U|={count_diffset(A_GRIEGO,m,T)} max={max_U(A_GRIEGO,m,T,B_GRIEGO)}")
    print("  (fast_sumset_count / scan_large_m / certify_best are holes — NotImplementedError.)")


if __name__ == "__main__":
    main()
