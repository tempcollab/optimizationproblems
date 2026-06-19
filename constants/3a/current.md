# current — Constant 3a (Gyarmati–Hennecart–Ruzsa sum-difference constant), LOWER bound

## Status
improved

## Bounds            table: 1.1740744 · held: 1.1741
Record to beat: C_3a > 1.1740744 (Griego 2026 [G2026]). Held (verified): C_3a > 1.1741 via exact big-integer certificate; computed θ = 1.1760055928 at (m,T)=(110,210).

## Progress log
- R3: VERIFIED record beat. Griego family A={0,2,..,10}, b=21, U={Σ x_i b^i : x∈A^m, Σx_i≤T}. Exact column DP for (|U+U|,|U−U|,max U) — independently cross-checked from-scratch against brute force on 12 cases (incl. clamp-exercising m=6,T=15 / m=4,T=9 / m=5,T=22). Load-bearing certificate is the pure big-integer inequality d^10000 > s^10000·(2M+1)^1741 ⟺ θ > 1.1741 > 1.1740744; reproduced independently with log-margin 6381.8 at (110,210). b=21>2·max(A)=20 makes g injective + carry-free, so digit-vector counts equal |U±U| exactly; GHR2007 gives C_3a ≥ θ. Anchor (80,150)=1.1740744477 reproduces Griego's record; first beat at (80,154)=1.1741714; best (110,210)=1.1760056. Negative control (80,148)=1.17393 correctly fails. Held: C_3a > 1.1741.
