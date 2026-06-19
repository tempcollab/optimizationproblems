"""
Search for Z_7-orbit generators v in Z_7^4 such that the cyclic action
  w -> w + t*v (mod 7)
has every orbit internally INDEPENDENT (i.e. for t=1..6, the step t*v has some coordinate
with cdist>=2 from 0, equivalently t*v_i in {2,3,4,5} for some i).

A step vector s has cdist(0, s_i) >= 2 iff s_i in {2,3,4,5}.  So we need: for every t in
1..6, t*v (mod 7) has at least one coordinate in {2,3,4,5}.  Equivalently v is "good".

For a good generator the conflict relation is invariant under the orbit action, so the
orbit-union approach is clean.  We enumerate all v (excluding v with order <7, i.e. v=0)
and report the good ones up to scaling (t*v generate the same orbit-shift family).
"""

from itertools import product

N = 4
FAR = {2, 3, 4, 5}  # letters at cdist>=2 from 0


def step_ok(s):
    return any(c in FAR for c in s)


def is_good_generator(v):
    # every nonzero multiple t*v must have a far coordinate
    for t in range(1, 7):
        s = tuple((t * v[i]) % 7 for i in range(N))
        if not step_ok(s):
            return False
    return True


def scale_class(v):
    """Canonical key for the multiplicative class {t*v : t=1..6} (same shift-family)."""
    cls = []
    for t in range(1, 7):
        cls.append(tuple((t * v[i]) % 7 for i in range(N)))
    return min(cls)


if __name__ == "__main__":
    good = []
    classes = set()
    for v in product(range(7), repeat=N):
        if all(c == 0 for c in v):
            continue
        if is_good_generator(v):
            good.append(v)
            classes.add(scale_class(v))
    print("good generator vectors:", len(good))
    print("good generator scale-classes:", len(classes))
    for c in sorted(classes)[:20]:
        print("  ", c)
