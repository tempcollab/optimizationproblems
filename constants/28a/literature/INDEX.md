# Literature digests — constant 28a (Borsuk first-failing dimension)

Round 1 (math-explorer). Read these before re-reading papers.

- `gri2026.md` — **record** `d_B<=63` (Grinsztajn May 2026). 321-pt set in R^63, margin exactly 1 part. Verify script re-run here: PASSES. Maximally Lean-fit.
- `jenrich-brouwer.md` — `d_B<=64` (arXiv:1308.0206). Contains the 63-dim "almost-counterexample" (Section 8) that Gri2026 fixed; pins exactly where the 63→62 wall is.
- `bondarenko.md` — origin of the SRG line, `d_B<=65` from G_2(4) (arXiv:1305.2584). The general SRG→two-distance→clique-cover mechanism and the levers for lowering dimension.
- `lower-bound-side.md` — why raising the LOWER bound (proving Borsuk in dim 4..62) is conjecture-hard and NOT a target.

PDFs + extracted text: `pdfs/` (1305.2584, 1308.0206, 1809.09612 [Jen2018 KK-construction detail], gri2026_borsuk63). Gri2026 verify script + DIMACS certs: upstream repo github.com/maaxgrin/borsuk-63-counterexample (cloned to /tmp/borsuk-63 during round 1; re-clone as needed).

## One-line state of the frontier
UPPER bound 63 is the live target; the only motion in 30 years has been 65→64→63 via sub-configurations of the SAME G_2(4) graph (ω=5). 62 needs >=316 points (ceil(316/5)=64 > 62+1) inside a 62-dim subspace with clique number still 5 — and the 320 C-points provably span exactly 63 dims with no near-degenerate hyperplane, so there is no free dimension to drop.
