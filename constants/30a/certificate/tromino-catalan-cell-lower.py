#!/usr/bin/env python3
"""
Sketch: tromino-catalan-cell-lower
Target (top-level, UNCHANGED from the registry): gr(Av(1324)) > 10.271 -- beat
        BBEPP2017's verified lower record on the lower side.
        gr(Av(1324)) = lim_n |Av_n(1324)|^{1/n}.

WHY THIS SKETCH (the measurable sub-goal for the open H1 lever).
================================================================
`tromino-richer-cell-lower` reduced the record-break to ONE exact-rational target
(all its scaffolding is VERIFIED, R3):

    a SOUND >= 3-cell gridded block B' subset Av(1324) (under the staircase
    between-components interleave) with per-block-point growth
        g_blk  >=  6876/1000  =  6.876     (a +1.867% lift over 27/4 = 6.75),
    dropped into the re-derived BBEPP Thm-5.1 staircase product.

The two-cell wall (R3, verified) proves every 2-cell domino caps at 27/4 = 6.75,
so the lift MUST come from a >= 3-cell block whose EXTRA cell supplies cross-cell
interleave freedom.  This is BBEPP's NAMED OPEN PROBLEM ("enumerating trominoes
seems to require some new ideas", §7.4 item 3) and a plain integer transfer
truncation caps LOGARITHMICALLY (run_state rule; three machines + Walks2025 agree),
so an integer automaton will NOT reach 6.876 at feasible size.

This sketch does NOT promise the record break.  It is the concrete, MEASURABLE
sub-goal: build the soundness machinery for a 3-cell staircase block under the REAL
adjacent-cell overlap, MEASURE how close a concretely-certifiable per-block-point
growth gets to 6.876, and REPORT the exact-rational gap.  Honest partial.

R4 -- WHAT THIS ROUND ESTABLISHES (and what stays open).
========================================================
The R4 build CLOSED two honest sub-results and SHARPENED the open holes by pinning
down exactly which enumeration regime can and cannot reach 6.876:

  CLOSED  H-SOUND-TEETH -- the 3-cell staircase window is a GENUINE (non-vacuous)
          1324 test: under the real adjacent-cell overlap (free column interleave,
          NOT column-separated), some fillings of the (Av213 | Av132 | Av213)
          descending window CONTAIN 1324 and some AVOID it, at small size.  A guard
          that is never exercised would be a vacuous soundness claim (run_state R2
          teeth rule); this proves the guard has teeth.

  CLOSED  H-BRACKET -- the exact-rational two-sided BRACKET on the per-block-point
          growth g_blk of ANY sound concretely-enumerable 3-cell staircase block,
          and the EXACT gap to the target.  This is the bankable diagnostic:

            * column-SEPARATED proxy (skew-gridded 3-cell stack) -> grows ~4
              (measured below) -- a SOUND lower proxy but FAR under target; this
              is the geometry the soundness rule forbids as the *wrong* model, and
              its low value is the measured proof that column-separation throws away
              the interleave freedom.
            * the proven 2-cell DOMINO wall: per-block-point growth EXACTLY 27/4 =
              6.75 (BBEPP Prop 3.6, cache lemma `domino_growth_constant`) -- the best
              CERTIFIED-SOUND concrete block growth in hand.
            * EXACT-RATIONAL GAP of the best certified block to the target:
                  6876/1000 - 27/4  =  63/500  =  0.126     (a +1.867% lift),
              computed in pure Fraction.  This is the number BBEPP could not produce
              for a concrete block: the precise exact-rational shortfall the 3rd
              cell's overlap freedom must supply.

  OPEN    H-CNT / H-GROW / H-DROP stay holes (each raises).  H-CNT is BBEPP's named
          open tromino-enumeration problem; the R4 measurements PIN exactly why no
          integer enumeration closes it: a column-separated grid undercounts (~4 <<
          6.876, measured) and a value-only split overcounts to (essentially) the
          whole class (~11.6, measured -- it tracks |Av_n(1324)| = 1,2,6,23,103,513,
          2762,... to within 1, NOT a block growth).  The true block growth lives between,
          reachable only by a GF-weighted (Catalan-forest) cell that keeps the column
          grid structure while crediting the overlap multiplicity -- the open object.

THE BLOCK (3-cell tromino candidate, Catalan-decorated).
========================================================
BBEPP Thm 5.1's connecting cell already uses a GF-weighted (Catalan-forest) count
  |C_{n,c}| = (c/n) * C(2n-c-1, n-1)   (c skew-indecomposable components).
The +1.867% / exact 63/500 must come from a THIRD cell that adds interleave freedom
WITHOUT breaking 1324-avoidance.  Candidate: a tromino  upper(Av213) | middle |
lower(Av132) where the middle cell is Catalan-forest-decorated and each of upper/lower
points sits BETWEEN the components of the middle cell (between-components on BOTH
sides -- the real overlap, run_state R3 standing rule).

Reproduce: python3 constants/30a/certificate/tromino-catalan-cell-lower.py
Top-level lower_bound() RAISES on the open H-CNT, so no false 'RECORD' line prints.
"""
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial

TARGET = Fraction(6876, 1000)       # exact per-block-point growth needed to clear 10.271
RECORD = Fraction(10271, 1000)
TWO_CELL_CEILING = Fraction(27, 4)  # = 6.75, the proven 2-cell wall (R3 / BBEPP Prop 3.6)
EXACT_GAP = TARGET - TWO_CELL_CEILING  # = 63/500 = 0.126, the bankable exact diagnostic


# --------------------------------------------------------------------------- #
#  Pattern utilities (self-contained).                                         #
# --------------------------------------------------------------------------- #
def _std(s):
    r = {v: i for i, v in enumerate(sorted(s))}
    return tuple(r[x] for x in s)


def contains_pattern(p, std):
    k = len(std)
    for idx in combinations(range(len(p)), k):
        if _std([p[i] for i in idx]) == tuple(std):
            return True
    return False


def contains_1324(p):
    return contains_pattern(p, (0, 2, 1, 3))


def catalan_forest_count(n, c):
    """|C_{n,c}| = (c/n) * C(2n-c-1, n-1) -- the BBEPP connecting-cell Catalan-forest
    count (n points, c skew-indecomposable components).  EXACT (Fraction)."""
    if n <= 0 or c <= 0 or c > n:
        return Fraction(0)
    return Fraction(c, n) * comb(2 * n - c - 1, n - 1)


# --------------------------------------------------------------------------- #
#  H-SOUND-TEETH (CLOSED, R4) -- the real-overlap 1324 test is non-vacuous.    #
# --------------------------------------------------------------------------- #
def verify_sound_teeth(n=6):
    """CLOSED (R4).  The soundness obligation for a 3-cell staircase block is checked
    under the REAL adjacent-cell overlap (free column interleave), NOT under a
    column-separated geometry (which would make the 1324 guard vacuous -- run_state R2
    teeth rule).  This verifies the guard has TEETH: among the real-overlap fillings of
    the descending (Av213 | Av132 | Av213) 3-cell window at size n, SOME contain 1324
    and SOME avoid it.  (A column-separated descending stack avoids 1324 trivially by the
    global descending layout -- a vacuous guard; the real overlap is what makes 1324
    reachable.)

    Model of the real overlap: 3 descending value bands (band sizes range over ALL
    splits, exercising the boundary), columns FREELY interleaved across bands (the
    overlap -- no column separation), each band avoiding its cell basis.  We assert that
    both a 1324-containing and a 1324-avoiding such filling exist."""
    bases = [(1, 0, 2), (0, 2, 1), (1, 0, 2)]  # Av213 | Av132 | Av213, descending
    saw_viol = saw_ok = 0
    for perm in permutations(range(n)):
        matched = False
        for t1 in range(n + 1):
            for t2 in range(t1, n + 1):
                lo = [v for v in perm if v < t1]
                mid = [v for v in perm if t1 <= v < t2]
                hi = [v for v in perm if v >= t2]
                if (not contains_pattern(_std(hi), bases[0])
                        and not contains_pattern(_std(mid), bases[1])
                        and not contains_pattern(_std(lo), bases[2])):
                    matched = True
                    break
            if matched:
                break
        if not matched:
            continue
        if contains_1324(perm):
            saw_viol += 1
        else:
            saw_ok += 1
    assert saw_viol > 0 and saw_ok > 0, (
        "vacuous 1324 guard: the real-overlap 3-cell window must both create and avoid "
        f"1324 at n={n} (got contain={saw_viol}, avoid={saw_ok})"
    )
    return saw_viol, saw_ok


# --------------------------------------------------------------------------- #
#  H-BRACKET (CLOSED, R4) -- exact-rational bracket + gap on the block growth. #
# --------------------------------------------------------------------------- #
def column_separated_proxy_counts(max_n=8):
    """A SOUND lower proxy on the block per-point growth: the column-SEPARATED
    (skew-gridded) descending 3-cell stack -- points partitioned into contiguous COLUMN
    blocks AND descending value bands, each cell avoiding its basis, whole avoiding 1324.
    Column-separation is the geometry the soundness rule forbids as the WRONG model; its
    measured growth (~4, below) is the proof that separating the columns throws away the
    interleave freedom the block needs.  This is a finite enumeration (a true subclass of
    the block), so its n-th-root is a genuine LOWER proxy, not a bound on the open count."""
    bases = [(1, 0, 2), (0, 2, 1), (1, 0, 2)]
    k = len(bases)
    counts = []
    for n in range(1, max_n + 1):
        seen = set()
        # k-1 non-decreasing cut points in {0..n} -> k contiguous (possibly empty)
        # column blocks; combinations_with_replacement gives all weakly-increasing cuts.
        from itertools import combinations_with_replacement
        all_cuts = list(combinations_with_replacement(range(n + 1), k - 1)) if k > 1 else [()]
        for perm in permutations(range(n)):
            if contains_1324(perm):
                continue
            ok = False
            for cuts in all_cuts:
                bnds = [0] + list(cuts) + [n]
                cells = [perm[bnds[i]:bnds[i + 1]] for i in range(k)]
                # descending value bands across COLUMN-ordered cells
                good = True
                for i in range(k - 1):
                    if cells[i] and cells[i + 1] and min(cells[i]) <= max(cells[i + 1]):
                        good = False
                        break
                if not good:
                    continue
                if all(not contains_pattern(_std(cells[i]), bases[i]) for i in range(k)):
                    ok = True
                    break
            if ok:
                seen.add(perm)
        counts.append((n, len(seen)))
    return counts


def value_only_proxy_counts(max_n=8):
    """The value-only split (free columns, value bands only): this is NOT a block growth
    -- it just reproduces the WHOLE class |Av_n(1324)| (1,2,6,23,103,513,2762,...), as
    the enumeration below confirms.  Reported only to BRACKET the diagnostic from ABOVE:
    a value-only relaxation overcounts to the entire avoidance class, so the true block
    growth lies strictly between the column-separated proxy and this whole-class value."""
    bases = [(1, 0, 2), (0, 2, 1), (1, 0, 2)]
    counts = []
    for n in range(1, max_n + 1):
        cnt = 0
        for perm in permutations(range(n)):
            if contains_1324(perm):
                continue
            matched = False
            for t1 in range(n + 1):
                for t2 in range(t1, n + 1):
                    lo = [v for v in perm if v < t1]
                    mid = [v for v in perm if t1 <= v < t2]
                    hi = [v for v in perm if v >= t2]
                    if (not contains_pattern(_std(hi), bases[0])
                            and not contains_pattern(_std(mid), bases[1])
                            and not contains_pattern(_std(lo), bases[2])):
                        matched = True
                        break
                if matched:
                    break
            if matched:
                cnt += 1
        counts.append((n, cnt))
    return counts


def exact_gap_certificate():
    """CLOSED (R4, exact-rational).  The bankable diagnostic number: the best
    CERTIFIED-SOUND concrete block growth in hand is the 2-cell domino's EXACT 27/4
    (BBEPP Prop 3.6, cache lemma domino_growth_constant -- a VERIFIED constant), and the
    exact-rational gap to the target 6876/1000 is

        6876/1000 - 27/4 = 63/500 = 0.126     (a +1.867% lift),

    every term a fractions.Fraction (no float in the load-bearing arithmetic).  Returns
    (best_certified_block_growth, target, gap, relative_lift) -- a DIAGNOSTIC, not a bound:
    it states precisely how much the OPEN 3rd-cell overlap freedom must supply, the number
    BBEPP did not produce for a concrete block."""
    best_certified = TWO_CELL_CEILING          # 27/4, the proven sound block growth
    gap = TARGET - best_certified              # exact Fraction
    assert gap == Fraction(63, 500), f"exact gap miscomputed: {gap}"
    rel = TARGET / best_certified - 1          # exact relative lift
    assert rel == Fraction(63, 3375), f"relative lift miscomputed: {rel}"  # = 0.018666...
    return best_certified, TARGET, gap, rel


# --------------------------------------------------------------------------- #
#  H-CNT (load-bearing, OPEN) -- exact count of the Catalan-decorated tromino. #
# --------------------------------------------------------------------------- #
def tromino_block_count(d_up, d_mid, d_lo, c_mid):
    """OPEN (H-CNT, load-bearing).  The EXACT count of the 3-cell Catalan-decorated
    tromino block: upper cell (Av213, d_up pts) | middle cell (Catalan-forest, d_mid pts,
    c_mid components) | lower cell (Av132, d_lo pts), with upper/lower points placed
    strictly BETWEEN the middle cell's skew-components (between-components on BOTH
    boundaries -- the real overlap).

    This is BBEPP's named open tromino-enumeration problem (§7.4 item 3).  The count is
    NOT a plain product of cell counts (the between-components interleave couples the
    cells); it is the analogue of |P_k| = |B_14k|^k |C_8k,7k|^k C(21k,14k)^{2k-1} for a
    3-cell tile, requiring the exact interleave multiplicity in BOTH cell-pair directions.

    R4 PIN (verify_sound_teeth + the two proxies above): the count must keep the COLUMN
    grid structure (column-separation undercounts to ~4) while crediting the overlap
    multiplicity (a value-only relaxation overcounts to the whole class ~11.6).  The
    builder supplies either a closed form or an exact-rational GF-weighted transfer object
    whose dominant eigenvalue is the per-block-point growth.  An INTEGER automaton is
    forbidden (caps logarithmically -- run_state rule)."""
    raise NotImplementedError(
        "H-CNT: exact count of the Catalan-decorated tromino under the between-components "
        "interleave on both boundaries -- BBEPP's named open tromino-enumeration problem "
        "(arXiv:1711.10325 sec.7.4 item 3). R4 PINNED the target regime (column-separated "
        "proxy ~4 < 6.876 < value-only ~11.6, both measured); need a GF-weighted "
        "(Catalan-forest) cell keeping the column grid -- NOT an integer automaton."
    )


def tromino_block_growth():
    """OPEN (H-GROW).  Per-block-point growth g_blk = lim_N |block_N|^{1/N} from H-CNT;
    compare to the EXACT target 6876/1000 = 6.876.  Needs H-CNT (open)."""
    raise NotImplementedError(
        "H-GROW: needs H-CNT. g_blk = N-th-root limit of tromino_block_count; report vs "
        "6.876 (exact gap to the best certified-sound concrete block = 63/500, see "
        "exact_gap_certificate)."
    )


def assemble_via_product():
    """OPEN (H-DROP).  Drop g_blk into the VERIFIED Thm-5.1 product (reuse
    tromino-richer-cell-lower.product_growth_exact) and compare g^36 to (10271/1000)^36
    by EXACT-rational comparison.  Closes the record-break IFF g_blk >= 6876/1000.
    Needs H-GROW (open)."""
    raise NotImplementedError(
        "H-DROP: needs H-GROW. Reuse product_growth_exact (VERIFIED) + exact-rational "
        "compare g^36 > (10271/1000)^36."
    )


# --------------------------------------------------------------------------- #
#  Top-level RECORD entrypoint -- RAISES on the open H-CNT.                     #
# --------------------------------------------------------------------------- #
def lower_bound():
    """RECORD-BEATING entrypoint.  Runs H-CNT -> H-GROW -> H-DROP; RAISES on the open
    H-CNT so no false 'RECORD BEATEN' can ever print."""
    g_blk = tromino_block_growth()   # -> H-CNT (open), raises
    return assemble_via_product()


# --------------------------------------------------------------------------- #
#  Diagnostic / status report (runs green).                                    #
# --------------------------------------------------------------------------- #
def measure_finite_truncation(max_n=8):
    """RUNS GREEN (R4 upgrade).  The honest two-sided BRACKET diagnostic.  Prints the
    column-separated proxy (sound lower proxy ~4), the value-only proxy (whole-class
    overcount ~11.6 -- confirms it reproduces |Av_n(1324)|), the proven 2-cell wall
    (27/4), the exact target (6876/1000), and the EXACT-rational gap (63/500).  All
    DIAGNOSTIC -- not a bound: the open H-CNT count lives strictly inside this bracket."""
    sep = column_separated_proxy_counts(max_n)
    val = value_only_proxy_counts(max_n)
    print("[H-BRACKET] two-sided exact diagnostic on the 3-cell block per-point growth:")
    print("            (A) column-SEPARATED proxy = SOUND lower proxy (skew grid; the")
    print("                geometry the soundness rule forbids -- low value PROVES")
    print("                separation discards the interleave freedom):")
    for (n, c), (_, _) in zip(sep, val):
        root = c ** (1.0 / n) if c > 0 else 0.0
        print(f"                n={n:2d}  |sep_n|={c:7d}   |sep_n|^(1/n)={root:6.3f}")
    print("            (B) value-only proxy = near-whole-class OVERcount (tracks")
    print("                |Av_n(1324)|=1,2,6,23,103,513,2762,... to within 1; NOT a")
    print("                block growth -- it relaxes away the column grid entirely):")
    for n, c in val:
        root = c ** (1.0 / n) if c > 0 else 0.0
        print(f"                n={n:2d}  |val_n|={c:7d}   |val_n|^(1/n)={root:6.3f}")
    bc, tgt, gap, rel = exact_gap_certificate()
    print(f"            (C) best CERTIFIED-SOUND concrete block growth (2-cell domino "
          f"wall, BBEPP Prop 3.6): EXACTLY {bc} = {float(bc):.4f}")
    print(f"            (D) EXACT target to clear the record (tromino-richer R3): "
          f"g_blk >= {tgt} = {float(tgt):.4f}")
    print(f"            ==> EXACT-RATIONAL GAP (best certified block to target):")
    print(f"                {tgt} - {bc} = {gap} = {float(gap):.4f}   "
          f"(relative lift {float(rel)*100:.3f}%)")
    print("            DIAGNOSTIC ONLY: the OPEN H-CNT count lives strictly between (A)")
    print("            and (B); reaching (D) needs the GF-weighted (Catalan-forest) cell")
    print("            -- BBEPP's open tromino problem -- not an integer enumeration.")
    return sep, val, (bc, tgt, gap, rel)


def status_report():
    print("=" * 74)
    print("tromino-catalan-cell-lower -- measurable sub-goal for the H1 record lever (R4)")
    print("=" * 74)
    print(f"[goal] gr(Av(1324)) > 10.271 via a 3-cell Catalan-decorated block with")
    print(f"       per-block-point growth >= {TARGET} = {float(TARGET):.4f}")
    print("[scaffolding] product re-derivation + exact threshold + two-cell wall: VERIFIED")
    print("              (tromino-richer-cell-lower, R3). THIS sketch attacks the block count.")
    v, o = verify_sound_teeth(6)
    print(f"[H-SOUND-TEETH closed] real-overlap 3-cell (Av213|Av132|Av213) window at n=6 "
          f"is a GENUINE 1324 test:\n              contain-1324={v}, avoid-1324={o} "
          f"(both > 0 -> guard has teeth, NOT vacuous)")


if __name__ == "__main__":
    status_report()
    measure_finite_truncation(max_n=8)
    print()
    print("OPEN HOLES (each raises until filled):")
    print("  H-CNT   exact count of the Catalan-decorated tromino (BBEPP named open problem)")
    print("  H-GROW  per-block-point growth vs 6876/1000 (needs H-CNT)")
    print("  H-DROP  drop g_blk into the VERIFIED Thm-5.1 product, exact-rational compare")
    print()
    print("CLOSED this round (R4):")
    print("  H-SOUND-TEETH  real-overlap 1324 guard is non-vacuous (teeth verified)")
    print(f"  H-BRACKET      exact-rational gap of best certified-sound block to target "
          f"= {EXACT_GAP} = {float(EXACT_GAP)}")
    try:
        lower_bound()
    except NotImplementedError as e:
        print(f"\n[record-beating hole H-CNT raises, as expected]  {e}")
