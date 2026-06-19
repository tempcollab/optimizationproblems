"""Build and cache the bitset + numpy adjacency once, so search chunks load fast."""
import numpy as np
import itertools
from core import N, DIM, NV, WORDS, CONF_LETTER

# numpy adjacency-list form: for fast LS we want, for each vertex, the array of
# its neighbors. Build NV x NV bool then convert.
arr = np.array(WORDS, dtype=np.int8)
CL = np.array(CONF_LETTER, dtype=bool)
adj = np.ones((NV, NV), dtype=bool)
for c in range(DIM):
    col = arr[:, c]
    cm = CL[np.ix_(col, col)]
    adj &= cm
np.fill_diagonal(adj, False)

print("edges", int(adj.sum()) // 2)
# neighbor lists (ragged) flattened with offsets
nbr_lists = [np.where(adj[i])[0].astype(np.int32) for i in range(NV)]
offsets = np.zeros(NV + 1, dtype=np.int64)
for i in range(NV):
    offsets[i + 1] = offsets[i] + len(nbr_lists[i])
flat = np.concatenate(nbr_lists).astype(np.int32)
np.savez_compressed("adj_cache.npz", flat=flat, offsets=offsets)
print("saved adj_cache.npz; total nbr entries", len(flat))
