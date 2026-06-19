# current — Constant 3a (Gyarmati–Hennecart–Ruzsa sum-difference constant), LOWER bound

## Status
improved

## Bounds            table: 1.1740744 · held: 1.176
Record to beat: C_3a > 1.1740744 (Griego 2026 [G2026]). Held (verified): C_3a > 1.176 via exact big-integer certificate (tight rational 11760/10000 at den 10000); computed θ = 1.1760055928 at (m,T)=(110,210).

## Progress log
- R4: VERIFIED held tightened 1.1741 → 1.176. Same (110,210) point, finer certificate rational: the exact big-integer inequality d^10000 > s^10000·(2M+1)^1760 ⟺ θ > 11760/10000 = 1.176 HOLDS, and ^1761 FAILS (so 1.176 is the tight k/10000, negative control). Reviewer independently re-derived (s,d,M) at (110,210) via a from-scratch bitmask DP validated vs brute force on 10 cases (incl. clamp/non-contiguous); s (107 digits), d (133 digits), M match the builder's values exactly; both inequality legs reproduced. Held: C_3a > 1.176 > 1.1740744. Separately, a Lean sketch (lean-native-decide-smallmt) machine-checks (lake build + native_decide, no sorryAx) the integer core D^40 > S^40·Q^7 (θ > 47/40 = 1.175) at (100,190) — literals independently matched — but its bridge from that integer fact to C_3a is an assumed (cited GHR2007) hypothesis with opaque Cnum, so it is a minimally-verified (*) Lean cert, NOT a self-contained Lean proof of C_3a > 1.175; it does not raise held on its own.
- R3: VERIFIED record beat. Griego family A={0,2,..,10}, b=21, U={Σ x_i b^i : x∈A^m, Σx_i≤T}. Exact column DP for (|U+U|,|U−U|,max U) — independently cross-checked from-scratch against brute force on 12 cases (incl. clamp-exercising m=6,T=15 / m=4,T=9 / m=5,T=22). Load-bearing certificate is the pure big-integer inequality d^10000 > s^10000·(2M+1)^1741 ⟺ θ > 1.1741 > 1.1740744; reproduced independently with log-margin 6381.8 at (110,210). b=21>2·max(A)=20 makes g injective + carry-free, so digit-vector counts equal |U±U| exactly; GHR2007 gives C_3a ≥ θ. Anchor (80,150)=1.1740744477 reproduces Griego's record; first beat at (80,154)=1.1741714; best (110,210)=1.1760056. Negative control (80,148)=1.17393 correctly fails. Held: C_3a > 1.1741.
