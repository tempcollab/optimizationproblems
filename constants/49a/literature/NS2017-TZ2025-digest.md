# C_49 = Erdős–Szemerédi 3-sunflower-free capacity — literature digest (scout, R12)

## The constant
C_49 = μ^S_3 = lim_n f(n)^(1/n), f(n) = max size of a sunflower-free family in 2^[n].
- **Upper bound (movable side per population history, but Lean-HOSTILE):** 3/2^(2/3) ≈ 1.8899
  [NS2017]. Proved by the **polynomial / slice-rank method**: |F| ≤ 3(n+1)Σ_{k≤n/3} C(n,k) ≤
  (3/2^(2/3))^(n(1+o(1))). This is an asymptotic analytic bound (an o(1) exponent + a
  binomial-sum estimate) — there is NO finite certifying core; the load-bearing step is a
  cap-set-style polynomial-method rank bound. **Lean-hostile.**
- **Lower bound:** >1.551 [DEGKM1997] (Deuber–Erdős–Gunderson–Kostochka–Meyer construction;
  value stated in FPP2024/TZ2025). An unpublished ≥1.554* [NS2017 arXiv] is NOT a verified
  bound (starred/unpublished — not the bar).
- Gap ≈ 1.551 → 1.890, wide. Conjectured < 2 (Erdős–Szemerédi), proved <2 by NS2017.

## Lean-fitness — HONEST triage on the step
- **Lower bound side:** a sunflower-free family is a finite object; "F is sunflower-free of
  size M in 2^[n]" is a decidable check (no three distinct A,B,C with A∩B=A∩C=B∩C). BUT a
  single finite family gives only f(n) for one n; converting to a **capacity lower bound**
  M^(1/n) > 1.551 requires either (a) a very large M^(1/n) from a finite n, or (b) the
  Fekete/tensor-power limit argument. The existing >1.551 is itself an asymptotic
  construction (DEGKM growth rate), so beating it needs an explicit finite family whose
  per-element growth rate M^(1/n) strictly exceeds 1.551 — and 1.551^n grows fast (e.g.
  n=12 needs M ≥ 1.551^12 ≈ 124; n=20 needs M ≥ 1.551^20 ≈ 4750). The combinatorial search
  for such dense sunflower-free families is HARD and the construction has been static (DEGKM
  1997). TZ2025 (Tang–Zhang, arXiv:2512.20055, "Harmonic LCM patterns and sunflower-free
  capacity") is the freshest work — connects to LCM patterns; worth reading IF this becomes
  the target, but no new numeric lower bound for μ^S_3 was surfaced.
- **Upper bound side:** Lean-hostile (polynomial method, asymptotic).
- Net: less Lean-fit than C_9. The lower-bound construction is a finite object in principle,
  but the bar (beat an asymptotic 1.551 growth rate) needs a large explicit family AND the
  growth-rate framing, not a single clean small certificate.

## Verdict
Plausible Lean target ONLY on the lower side and only if a small explicit sunflower-free
family with growth rate > 1.551 can be found — historically hard, construction static since
1997. Weaker round-sized prospect than C_9. Upper side is Lean-hostile.
