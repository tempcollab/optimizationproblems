# Literature digests — constant 28a (Borsuk first-failing dimension)

Round 1 (math-explorer). Read these before re-reading papers.

- `gri2026.md` — **record** `d_B<=63` (Grinsztajn May 2026). 321-pt set in R^63, margin exactly 1 part. Verify script re-run here: PASSES. Maximally Lean-fit.
- `jenrich-brouwer.md` — `d_B<=64` (arXiv:1308.0206). Contains the 63-dim "almost-counterexample" (Section 8) that Gri2026 fixed; pins exactly where the 63→62 wall is.
- `bondarenko.md` — origin of the SRG line, `d_B<=65` from G_2(4) (arXiv:1305.2584). The general SRG→two-distance→clique-cover mechanism and the levers for lowering dimension.
- `lower-bound-side.md` — why raising the LOWER bound (proving Borsuk in dim 4..62) is conjecture-hard and NOT a target.
- `musin2025.md` — **NEW (R2)** Musin Nov 2025 (arXiv:2511.03668). Generalizes the SRG criterion to ANY graph: `G` is a Borsuk counterexample iff `θ(G)+μ(G)>n`, embedding dim `n−μ(G)−1`. §3.2 gives a generative search (fix a balanced clique skeleton C0, edge-flip between cliques to maximize μ) — a fresh construction angle distinct from the closed SRG-table sweep and the refuted G2(4) 4th-vector family. §3.3 s-distance version backs mixed-construction. No new sub-64 graph given.
- Two-distance counterexample survey arXiv:2005.12025 (More SRG counterexamples): scanned, NOT digested in full — all its constructions (Fi_23 descendants 779–781, a 2401-vtx graph → dim 240) are ≥64, none near the 63→62 frontier; induced-subgraph dimension-drop only loses points, same lever as Jenrich. Not worth a full digest unless an angle needs its 2401-vtx graph.

PDFs + extracted text: `pdfs/` (1305.2584, 1308.0206, 1809.09612 [Jen2018 KK-construction detail], gri2026_borsuk63). Gri2026 verify script + DIMACS certs: upstream repo github.com/maaxgrin/borsuk-63-counterexample (cloned to /tmp/borsuk-63 during round 1; re-clone as needed).

## One-line state of the frontier
UPPER bound 63 is the live target; the only motion in 30 years has been 65→64→63 via sub-configurations of the SAME G_2(4) graph (ω=5). 62 needs >=316 points (ceil(316/5)=64 > 62+1) inside a 62-dim subspace with clique number still 5 — and the 320 C-points provably span exactly 63 dims with no near-degenerate hyperplane, so there is no free dimension to drop.
