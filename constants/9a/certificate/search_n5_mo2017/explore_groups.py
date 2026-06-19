"""Explore which (perm, b) generators give non-trivial orbit-size distributions
and good orbit-MIS ceilings. Quick greedy scan, no CP-SAT."""
import itertools, json, sys, time
from engine import *
from solve_mis import greedy_weighted_mis

def gen_order(perm, b):
    x0 = (0,)*N
    # order = least k>0 with g^k = identity map; compute via tracking a basis word set is hard,
    # instead order = lcm of orbit lengths -> just compute max orbit length over all words is not order.
    # order of element = smallest k with apply^k(x)=x for all x; equals lcm of cycle structure.
    # Compute by applying to identity-tagged: track when (perm,b)^k = id. Apply to each coordinate basis.
    # Simpler: the group is generated, order = number of distinct group elements; but we just need orbit sizes.
    pass

def orbit_size_dist(perm, b):
    seen = set()
    sizes = {}
    for x in itertools.product(range(Q), repeat=N):
        if x in seen: continue
        orb = orbit_of(x, perm, b)
        for w in orb: seen.add(w)
        sizes[len(orb)] = sizes.get(len(orb),0)+1
    return sizes

# Candidate permutations and their cycle structure on 5 coords
PERMS = {
  'id': (0,1,2,3,4),
  '5cyc': (1,2,3,4,0),       # order 5
  '2cyc': (1,0,2,3,4),       # order 2 (swap 0,1)
  '3cyc': (1,2,0,3,4),       # order 3
  '2+2': (1,0,3,2,4),        # order 2
  '2+3': (1,0,3,4,2),        # order 6
  '4cyc': (1,2,3,0,4),       # order 4
}

if __name__ == '__main__':
    # For each perm, scan a few b vectors and report orbit-size dist
    out = []
    for pname, perm in PERMS.items():
        for trial in range(6):
            # deterministic small b vectors
            import random
            random.seed(hash((pname,trial)) & 0xffff)
            b = tuple(random.randrange(Q) for _ in range(N))
            dist = orbit_size_dist(perm, b)
            multiple_of_7 = all((s % 7 == 0) for s in dist) or (sum(k*v for k,v in dist.items())%7==0)
            out.append((pname, b, dist))
            print(pname, 'b=',b, 'sizes', dist)
    print('---done---')
