# Gibbs 2018, "An Upper Bound for Lebesgue's Covering Problem" (arXiv:1810.10089)

**Value:** upper bound a ≤ 0.8440935944, achieved at slant angle σ < 1.5494°.

**Method (construction).**
- Start: regular hexagon with unit distance between opposite sides (Pál's hexagon).
- P(σ): cut corners C and E along two sides of a regular dodecagon centred at the hexagon
  centre, at a *slant angle* σ (0 ≤ σ < 30°). σ=0 is Pál's original cut.
- S(σ): from P(σ) remove three "Sprague-like" regions C_S, E_S, A_S — areas no curve of
  constant width (orbiform) of unit diameter can enter. S(0) = Sprague's cover.
  Note: area of S(σ) is *smallest at σ=0*, so these reductions alone don't beat the record.
- H(σ): additionally remove regions A_H (near corner A) and E_H (near corner E). These
  are the regions removed by BBG2015; Gibbs pushes them "to their logical conclusion."
  Removability proved by reflection/rotation arguments (an orbiform entering A_H or E_H
  can be reflected/rotated to a congruent copy avoiding both).
- The improvement over BBG2015 (0.8441153) is ~2.2e-5; gain over the previous (Hansen) was
  also ~2.2e-5. **The upper bound is essentially fully squeezed.**

**Remaining slack (author's own words, "Future prospects").**
- Only the regions near the *existing* reductions E_H and A_H have further scope; "indications
  are that such further reductions are indeed possible at both locations" — but each is a
  sub-fraction of an already-microscopic region. Diminishing returns; needs heroic
  computational geometry for ~1e-5 gains.
- Verification: developed with John Baez, Karine Bagdasaryan, Greg Egan (BBG2015 value was
  high-precision verified by Egan). Gibbs2018's exact final number not independently
  re-certified in the record, but methodology is the established BBG line.

**Takeaway for us:** the UPPER bound is a poor target — fully optimized, microscopic gains,
heavy geometry. The LOWER bound side is the soft target (see brass-sharifi digest).
