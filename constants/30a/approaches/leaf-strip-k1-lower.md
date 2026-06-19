# leaf-strip-k1-lower — BBEPP §7.4 avenue #1 (k=1 leaf strips): relax the §7 staircase, beat 10.271

**Side / target.** Lower bound. Top-level target (registry-exact): `gr(Av(1324)) > 10.271`,
where `gr(Av(1324)) = lim_n |Av_n(1324)|^{1/n}`, beating BBEPP2017's verified record
10.271012 (Thm 7.1).

**Why this sketch (R5, new — explorer "Lever B", the softest record-lever this round).**
The tromino road (`tromino-richer-cell-lower` / `tromino-catalan-cell-lower`, avenue #3) has
been a wall for 4 rounds: BBEPP themselves say it "seems to require some new ideas" (a missing
3-cell enumeration). The explorer's R5 finding: BBEPP's **first** named improvement avenue
(§7.4 #1, k-leaf strips, k=1) is strictly easier — the authors rank it below trominoes — because
it is an **analysis task on already-built objects**, not a missing object. It refines the SAME
§7 staircase that produced 10.271.

**The mechanism.** BBEPP's 10.271 (Thm 7.1) relaxes the horizontal-domino interleave so only
NON-LEAVES sit between connecting-cell components; the non-leaves cut each cell into horizontal
**strips** (a *j-leaf strip* has j leaves). §6 proves the leaf proportion (5n/9) and empty-strip
proportion (5n/27) are concentrated; the master saddle **Lemma 7.4** (a law-of-large-numbers
radius-of-convergence estimate) turns the multivariate-GF product into 1/z0 = 10.271,
z0 ≈ 0.097361383, at (α,β,γ,κ) ≈ (5/9, 5/27, 0.9515, 0.4963). **The §7 optimum only ever uses
0-, 2-, and 3-leaf strips (e0,e2,e3)**: α ≥ 11/20 > 1/2 forces ≥1 leaf per non-empty strip, and
the equitable allocation never lands on exactly-1, so there are NO 1-leaf strips in the current
optimum. Admitting the e1 class with its own concentrated proportion **enlarges the feasible
allocation** — any old feasible point is feasible in the new (set the e1-proportion to 0), so the
re-optimised growth is ≥ 10.271; the deliverable is the strict gain.

**Borrows.** None structurally from a sketch file — this opens a fresh GF/saddle line. It reuses
the BBEPP §6/§7 machinery digested in `literature/BBEPP2017.md` (strip operators Ω^j / H_{a_i},
Prop 6.1–6.4 concentration, Lemma 7.4 saddle). Shares the *spirit* of the verified `held` line
(§7 refines the same 81/8 staircase) but does not import its product.

**Holes.**
- **H-REPRO** `reproduce_bbepp_baseline` — re-derive 10.271012 from Lemma 7.4 with the
  (e0,e2,e3)-only allocation. Baseline anchor: the e1 re-run must reproduce this with α_{e1}=0
  (the containment check). Low-risk, numerical.
- **H-FUNEQ (load-bearing #1)** `refined_domino_funeq_with_e1` — modify the domino functional
  equation to mark the number of 1-leaf strips with a new catalytic variable (Prop-6.3-marker
  analogue); yields the new GF factor F_{e1}. BBEPP's "modify the functional equation to record
  k-leaf strips".
- **H-EXTRACT (load-bearing #2, the BBEPP wall)** `extract_F_e1_factor` — extract a usable
  F_{e1}(x) (radius ρ_{e1}, saddle ratio x F'/F) from the refined funeq via resultant
  elimination (degree-7 / degree-104 flavour) + numeric. This is the exact step BBEPP "could not
  analyse, even for k=1."
- **H-CONC (load-bearing #3)** `prove_e1_concentration` — prove the 1-leaf-strip proportion is
  concentrated (Prop-6.4 analogue), giving a fixed α_{e1} for Lemma 7.4.
- **H-OPT (load-bearing #4, payoff)** `reoptimize_saddle_with_e1` — re-solve the Lemma-7.4
  saddle over (e0,e1,e2,e3); containment α_{e1}=0 → 10.271; report the strict gain g_new (or a
  certified tie = a real negative result on this avenue).
- **H-CERT** `assemble_numerical_certificate` — directed-rounded interval-arithmetic certificate
  that g_new > 10271012/1000000. Closes the record IFF g_new strictly beats it.

**Hard step.** H-EXTRACT — extracting a usable F_{e1} (radius + saddle ratio) from the modified
functional equation. This is the analysis bottleneck two expert authors could not push through in
2017. Mechanism: algebraic-GF / resultant elimination (CAS, sympy), same technique that produced
the degree-7 min-poly in Prop 6.1 and the degree-104 alternative number in footnote 3, followed
by a numeric saddle solve.

**Lean-fit.** HOSTILE. The load-bearing step is a multivariate-GF radius-of-convergence /
saddle-point optimisation with a law-of-large-numbers concentration input. Certificate path =
NUMERICAL (directed-rounded on the saddle equation + a hand-checked concentration bound), the 82a
kind, NOT a lake build.

**Honest risk.** This is a real record-angle for breadth with a concrete continuation on existing
machinery — but it is exactly the open analysis problem BBEPP flagged. Honest expectation: a
partial sketch (set up the modified funeq H-FUNEQ, attempt the H-EXTRACT factor) that may stall on
the same wall. The bankable near-term output is H-REPRO (the reproduced baseline harness) plus a
documented attempt at H-FUNEQ/H-EXTRACT.

**Sketch file.** `constants/30a/certificate/leaf-strip-k1-lower.py` (runs green, exits 0; prints
the plan and the BBEPP baseline; all holes raise via `lower_bound()` so no false RECORD line can
print). Reproduce: `python3 constants/30a/certificate/leaf-strip-k1-lower.py` (stdlib only).
