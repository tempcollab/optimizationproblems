"""
Orbit structure for the orbit-restricted search on C_7^box4.

The strong-power confusability relation on Z_7^4 is INVARIANT under coordinate-wise
translation by any vector s in Z_7^4 (cdist(a+s,b+s)=cdist(a,b)).  In particular it is
invariant under the DIAGONAL Z_7 action  t -> w + t*(1,1,1,1) mod 7.  This action is
free (no nonzero diagonal shift fixes a word), so every orbit has size exactly 7 and there
are 2401/7 = 343 orbits.  We pick the orbit whose representative is lexicographically
minimal; equivalently the canonical rep has first coordinate 0 (since adding t shifts coord0
by t, exactly one t in 0..6 makes coord0 = 0).

Because the relation is diagonal-translation invariant, the orbit-conflict structure is
clean: orbit A and orbit B (A != B) are "orbit-compatible" iff EVERY cross pair (a in A,
b in B) is independent; if SOME cross pair is confusable the two orbits clash on that shift.
A union of orbits is an independent set iff (1) each orbit is internally independent and
(2) every selected pair of orbits is orbit-compatible.  (Internal: an orbit is independent
iff w and w+t*(1,1,1,1) are non-confusable for all t in 1..6.)

This module builds the 343-orbit reduced conflict graph for the diagonal action.
"""

from itertools import product
from c7graph import confusable_word, N

DIAG = (1, 1, 1, 1)


def shift(w, t):
    return tuple((w[i] + t * DIAG[i]) % 7 for i in range(N))


def orbit_of(w):
    return [shift(w, t) for t in range(7)]


def canon(w):
    """Canonical representative of the diagonal orbit: the shift making coord0 == 0."""
    t = (-w[0]) % 7
    return shift(w, t)


def build_orbits():
    seen = set()
    reps = []
    for w in product(range(7), repeat=N):
        c = canon(w)
        if c not in seen:
            seen.add(c)
            reps.append(c)
    reps.sort()
    return reps


def orbit_internally_independent(rep):
    """An orbit is independent iff rep and rep+t*DIAG are non-confusable for t=1..6."""
    for t in range(1, 7):
        if confusable_word(rep, shift(rep, t)):
            return False
    return True


def orbits_compatible(repA, repB):
    """Every cross pair (a in orbit A, b in orbit B) independent."""
    obA = orbit_of(repA)
    obB = orbit_of(repB)
    for a in obA:
        for b in obB:
            if confusable_word(a, b):
                return False
    return True


if __name__ == "__main__":
    reps = build_orbits()
    print("num orbits:", len(reps))
    good = [r for r in reps if orbit_internally_independent(r)]
    print("internally-independent orbits (size-7 contributors):", len(good))
    print("example good orbit rep:", good[0] if good else None)
