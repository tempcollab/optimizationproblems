# bona-forbidden-factor-upper — UPPER bound by extending Bona's (w,z) word encoding

**Side / target.** Upper bound. Top-level target: `gr(Av(1324)) <= beta^2 < 13.5` where
`beta = 1/alpha`, `alpha` = smallest-modulus root of an explicit integer-coefficient
denominator polynomial. Beats BBEPP2017's record 13.5.

**Strategy (explorer angle A2 — most Lean-fit existing upper-bound machinery).**
Bona (B14a/B14b) injects `Av_n(1324)` into pairs of length-n words over {A,B,C,D} satisfying
local forbidden factors (no CB; `CAB^k =>` k B's in the z-segment). The admissible count has an
**explicit rational GF**; its smallest-modulus root `alpha` gives `beta = 1/alpha` and
`L(1324) <= beta^2`. Known: CB only -> 13.7595; +CAB^2 -> 13.73977. The method **saturates
~13.7** with local factors.

Plan: add **one more certified forbidden factor** — a local consequence of 1324-avoidance
beyond CB/CAB^k that Bona did not use — recompute the rational GF root, drive `beta^2 < 13.5`.

**Holes.**
- **H1 (the hard step)** the new forbidden factor, *provably forced* by 1324-avoidance.
- **H2** rational GF / integer denominator polynomial of word-pairs satisfying {CB, CAB^k, H1}.
- **H3** certified lower bound on `|alpha|` via Sturm / interval arithmetic => `beta^2 < 13.5`.

**Lean-fit.** High — "smallest root of integer polynomial >= rational r" is a finite Sturm
certificate; the injection is a finite word argument.

**Honest estimate.** The 13.7 -> 13.5 gap (~0.24) is a *large* ask for one local factor, and
this is exactly where Bona stalled — local factors discard global 1324-structure. Likely needs
several factors or a structural insight; multi-round, more speculative than
decorated-domino-upper but reuses fully-built GF/root machinery. Borrows nothing from other
sketches; shares the Sturm-root certify path with decorated-domino-upper.

**Sketch file.** `constants/30a/certificate/bona-forbidden-factor-upper.py` (runs; holes raise).
