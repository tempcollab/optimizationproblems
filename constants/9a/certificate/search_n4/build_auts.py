"""Precompute a pool of automorphism vertex-permutations for diversification."""
import numpy as np
import random
from core import NV, random_aut_vertex_perm

rng = random.Random(12345)
POOL = 400
perms = np.zeros((POOL, NV), dtype=np.int32)
for k in range(POOL):
    perms[k] = np.array(random_aut_vertex_perm(rng), dtype=np.int32)
np.savez_compressed("aut_cache.npz", perms=perms)
print("saved", POOL, "automorphism vertex-perms")
