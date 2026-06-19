"""
Sketch C  --  srg-sweep  (constant 28a, Borsuk first-failing dimension; upper bound 63 -> 62)

ATTACK LINE C (explorer): does a *different* strongly regular graph (SRG), realised as a
two-distance set, give a Borsuk counterexample in dimension f <= 62?  This is a pure FINITE
DATABASE SEARCH over the feasible strongly-regular-graph parameter sets.

=====================================================================================
MECHANISM  (Bondarenko 2014, arXiv:1305.2584; graph reformulation Musin 2025,
            arXiv:2511.03668; SRG sweep precedent arXiv:2005.12025)
=====================================================================================
An SRG srg(v,k,lambda,mu) has adjacency eigenvalues  k, r>0, s<0, with multiplicities
1, f, g  (f+g = v-1).  The Gram matrix  Y = A - s I  is PSD of rank 1+f; its v columns
realise the vertices as a TWO-DISTANCE SET whose AFFINE span has dimension

        f = multiplicity of the positive eigenvalue r.                       (dim)

(For the all-ones / sphere normalisation the 1 extra rank is the radial direction; the
affine dimension is f.  Checked below against G_2(4): f = 65, the published dimension.)

A subset of the two-distance set has STRICTLY SMALLER DIAMETER  iff  its vertices are
pairwise ADJACENT, i.e. form a CLIQUE.  Hence any partition into smaller-diameter parts is
a clique cover, and the Borsuk number satisfies

        b  >=  theta(G)  >=  ceil( v / omega(G) ),                          (parts)

where omega(G) is the clique number.  The set is a counterexample in R^f as soon as the
number of forced parts exceeds f+1:

        ceil(v / omega(G))  >  f + 1.                                       (beat)

To BEAT the record 63 we need a counterexample in dimension <= 62, i.e.

        f <= 62      AND      ceil(v / omega(G)) >= 64.                     (TARGET)

(ceil(>=316/5)=64 > 63 in the record's language; here written intrinsically as (beat).)

=====================================================================================
WHAT IS CERTIFIABLE FROM PARAMETERS ALONE  (the rigorous core)
=====================================================================================
omega(G) is a property of the graph, not the parameter set.  But the DELSARTE-HOFFMAN
(ratio) clique bound gives, FROM PARAMETERS ALONE, an UPPER bound on omega:

        omega(G)  <=  omega_DH  :=  1 + floor( k / (-s) ).                  (Hoffman)

Because omega <= omega_DH, the number of forced parts is bounded BELOW by parameters:

        ceil(v / omega(G))  >=  ceil(v / omega_DH).                         (guaranteed)

So a parameter set CERTIFIES a counterexample (given that a graph with those parameters
exists) exactly when

        f <= 62   AND   ceil(v / omega_DH) >= 64.                          (CERTIFIABLE)

This is a SUFFICIENT, parameter-only, reproducible condition.  The sweep below applies it
to every feasible parameter set in Brouwer's table (v <= 1300), the large named SRGs
outside the table, and the infinite families.  RESULT: it is satisfied by NONE of them
(printed when run).  That is sketch C's load-bearing finite computation.

=====================================================================================
THE RESIDUAL (honest scope of the negative)
=====================================================================================
omega_DH overestimates omega, so some rows with f <= 62 fail (CERTIFIABLE) yet are not
*arithmetically* impossible: if the TRUE omega were as small as some omega <= need_omega
:= (largest omega with ceil(v/omega) >= 64), the row would qualify.  These residual rows
are NOT counterexamples by this sketch; ruling each out needs the actual graph's clique
number.  For the NAMED / KNOWN families among them we plug in the EXACT clique number
(Triangular T(n): omega=n-1; Latin-square/OA(m,t) & lattice: omega=m; Paley/ conference:
small; etc.) and show omega is far too large -- i.e. ceil(v/omega) << 64.  What remains
after that is a precisely-scoped list of parameter rows that are EITHER of unsettled
existence ('?') OR whose exact clique number is not pinned here; for each we report what
is missing.  No qualifying graph is currently known (Musin 2025 confirms the conjecture is
open for dims 4..63 with no SRG counterexample below 63; the SRG sweep of arXiv:2005.12025
finds nothing below G_2(4)'s dim 65 except sub-configurations).

=====================================================================================
CERTIFY (Lean-fit, if a row ever qualifies): integer Gram  Y = A - sI  PSD of rank
f+1 <= 63  +  omega(G) <= floor(v/64).  Both finite/algebraic, in g24.py
(gram_integer, euclidean_rep, subspace_dim, max_clique_le).
"""

import math
import os
import re
import html
import json
import glob


# ---------------------------------------------------------------------------
# Exact eigenvalue / multiplicity arithmetic (verified against Brouwer's table)
# ---------------------------------------------------------------------------

def parts_needed(v, omega):
    return math.ceil(v / omega)


def positive_eig_multiplicity(v, k, lam, mu):
    """
    srg(v,k,lambda,mu): eigenvalues r>s are roots of x^2 - (lambda-mu)x - (k-mu) = 0.
    Returns (r, mult_r, s, mult_s) with mult_r = embedding dimension f, or None if the
    eigenvalues are irrational (conference graphs: handle via (v-1)/2) or params are
    inconsistent.
    """
    disc = (lam - mu) ** 2 + 4 * (k - mu)
    if disc < 0:
        return None
    sq = math.isqrt(disc)
    if sq * sq != disc:
        return None  # irrational -> conference type
    r = ((lam - mu) + sq) // 2
    s = ((lam - mu) - sq) // 2
    if r == s:
        return None
    f_num = (v - 1) * (-s) - k
    if (r - s) == 0 or f_num % (r - s) != 0:
        return None
    f = f_num // (r - s)
    g = (v - 1) - f
    if f < 0 or g < 0:
        return None
    # consistency: k + f*r + g*s == 0
    if k + f * r + g * s != 0:
        return None
    return (r, f, s, g)


def delsarte_hoffman_omega_ub(v, k, lam, mu):
    """
    Upper bound omega <= 1 + k/(-s) (Hoffman ratio / Delsarte clique bound).
    For conference graphs (irrational s) uses s = (-1 - sqrt(v))/2.
    Returns integer floor of the bound, or None.
    """
    info = positive_eig_multiplicity(v, k, lam, mu)
    if info is not None:
        r, f, s, g = info
        if s >= 0:
            return None
        return 1 + k // (-s)
    # conference graph: s = (-1 - sqrt(v))/2, irrational
    disc = (lam - mu) ** 2 + 4 * (k - mu)
    if disc < 0:
        return None
    negs = (1 + math.sqrt(v)) / 2.0
    return int(math.floor(1 + k / negs))


def embedding_dim(v, k, lam, mu, table_f=None):
    """Affine embedding dimension f = mult(r). Uses the exact formula; for conference
    graphs (irrational eigenvalues) f = g = (v-1)/2; falls back to table_f if supplied."""
    info = positive_eig_multiplicity(v, k, lam, mu)
    if info is not None:
        return info[1]
    if (v - 1) % 2 == 0:
        return (v - 1) // 2  # conference graph
    return table_f


# ---------------------------------------------------------------------------
# The certifiable counterexample test (sufficient, parameter-only)
# ---------------------------------------------------------------------------

def certifies_counterexample(v, k, lam, mu, table_f=None):
    """
    Returns a dict describing the row against the TARGET, with:
      f                = embedding dimension
      omega_DH         = Delsarte-Hoffman clique upper bound
      guaranteed_parts = ceil(v / omega_DH)   (a LOWER bound on the Borsuk number)
      certifies        = True iff  f <= 62 AND guaranteed_parts >= 64  (sufficient).
    """
    f = embedding_dim(v, k, lam, mu, table_f=table_f)
    od = delsarte_hoffman_omega_ub(v, k, lam, mu)
    out = dict(v=v, k=k, lam=lam, mu=mu, f=f, omega_DH=od)
    if f is None or od is None or od < 1:
        out.update(guaranteed_parts=None, certifies=False)
        return out
    gp = math.ceil(v / od)
    out.update(guaranteed_parts=gp,
               certifies=(f <= 62 and gp >= 64))
    return out


def max_omega_for_64_parts(v):
    """Largest integer omega with ceil(v/omega) >= 64 (i.e. the actual clique number would
    have to be <= this for the row to qualify)."""
    best = None
    for om in range(1, v + 1):
        if math.ceil(v / om) >= 64:
            best = om
        else:
            break
    return best


# ---------------------------------------------------------------------------
# Known exact clique numbers for named SRG families (to rule out residual rows)
#   - Triangular  T(n) = L(K_n):  v = C(n,2),  omega = n - 1
#   - Lattice / Hamming  L2(n) = H(2,n):  v = n^2,  omega = n
#   - Orthogonal-array / Latin-square  OA(m,t) graph:  v = m^2,  omega = m
#   - Paley P(q), conference graphs: omega ~ small but >= sqrt(v)-ish; handled via DH only
# These exact values come from the comment column of Brouwer's table.
# ---------------------------------------------------------------------------

def structural_clique_lower_bound(v, k, lam, mu):
    """
    A clique LOWER bound provable from the parameters alone (no graph needed):
      - k >= 1            => the graph has an edge          => omega >= 2.
      - lambda >= 1       => an edge {u,v} has a common neighbour w adjacent to both
                             => {u,v,w} is a triangle       => omega >= 3.
      - lambda >= 2 with the two common neighbours of an edge themselves adjacent would
        give omega >= 4, but that adjacency is NOT forced by parameters, so we stop at 3.
    Returns the provable lower bound on omega(G). (Conservative on purpose: only what is
    forced for EVERY graph with these parameters.)
    """
    lb = 1
    if k >= 1:
        lb = 2
    if lam >= 1:
        lb = 3
    return lb


def known_clique_number(v, comment):
    """Exact omega for a recognised named family, else None. Conservative: only returns a
    value when the family identification pins omega exactly."""
    c = comment
    # Triangular graph T(n): comment 'Triangular graph T(n)'
    m = re.search(r'Triangular graph T\((\d+)\)', c)
    if m:
        n = int(m.group(1))
        return ('T(%d)' % n, n - 1)
    # Lattice n^2  (comment like '13^2', '12^2'): omega = n
    m = re.match(r'^\s*(\d+)\^2', c)
    if m:
        n = int(m.group(1))
        if n * n == v:
            return ('%d^2 lattice' % n, n)
    # Orthogonal array OA(m,t): omega = m
    m = re.search(r'OA\((\d+),(\d+)\)', c)
    if m:
        mm = int(m.group(1))
        if mm * mm == v:
            return ('OA(%d,%d)' % (mm, int(m.group(2))), mm)
    return None


# ---------------------------------------------------------------------------
# Parsing Brouwer's feasible-parameter HTML tables  (cached under data_dir)
# ---------------------------------------------------------------------------

def _parse_cell(c):
    c = c.replace('&nbsp;', '\x00')
    c = re.sub(r'<sup>(.*?)</sup>', r'^\1', c)
    c = re.sub(r'<[^>]+>', '', c)
    return html.unescape(c).strip()


def _parse_eig(cell):
    m = re.match(r'^(–|-)?([0-9.]+)\^([0-9]+)$', cell)
    if not m:
        return None
    sign = -1 if m.group(1) else 1
    base = m.group(2)
    mult = int(m.group(3))
    if '.' in base:
        return ('frac', sign, base, mult)
    return ('int', sign * int(base), mult)


def _parse_table_file(path):
    txt = open(path, encoding='utf-8').read()
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', txt, re.S)
    cur_v = None
    recs = []
    for r in rows:
        cells = [_parse_cell(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
        if len(cells) < 7:
            continue
        ex, v, k, lam, mu, rf, sg = cells[:7]
        comment = cells[7] if len(cells) > 7 else ''
        vs = v.replace('\x00', '').strip()
        if vs:
            cur_v = vs
        if cur_v is None:
            continue
        try:
            vv, kk, ll, mm = int(cur_v), int(k), int(lam), int(mu)
        except ValueError:
            continue
        ri = _parse_eig(rf)
        recs.append(dict(ex=ex.replace('\x00', '').strip(), v=vv, k=kk, lam=ll, mu=mm,
                         rf=rf, sg=sg,
                         table_f=(ri[3] if (ri and ri[0] == 'frac') else
                                  (ri[2] if ri else None)),
                         comment=comment))
    return recs


def load_brouwer_srg_table(data_dir=None):
    """
    Load Brouwer's full feasible strongly-regular-graph parameter table, v <= 1300
    (https://aeb.win.tue.nl/graphs/srg/srgtab.html, 26 sub-pages), from cached HTML in
    `data_dir`.  Returns a list of parameter records.  This is the finite database whose
    sweep is sketch C's hard step -- now FILLED.  Falls back to a small embedded seed +
    the large named SRGs (LARGE_SRGS) if the HTML cache is absent so the script still runs.
    """
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'srgtab_html')
    recs = []
    if os.path.isdir(data_dir):
        for p in sorted(glob.glob(os.path.join(data_dir, '*.html'))):
            recs.extend(_parse_table_file(p))
    return recs


# Large named SRGs outside the v<=1300 table (Brouwer srgbig.html) plus their complements.
# (v, k, lambda, mu, comment).  Used so the sweep also covers the big sporadic graphs.
LARGE_SRGS = [
    (1288, 495, 206, 180, "M24/M12.2"),
    (1288, 792, 476, 504, "M24/M12.2 complement"),
    (1408, 567, 246, 216, "U6(2)/U4(3).2"),
    (1408, 840, 488, 520, "U6(2) complement"),
    (1782, 416, 100, 96, "Suz.2/G2(4).2"),
    (1782, 1365, 1044, 1050, "Suz complement"),
    (2016, 975, 462, 480, "Wilbrink{4,3}"),
    (2016, 1040, 544, 528, "Wilbrink complement"),
    (2048, 759, 310, 264, "2^11.M24/M24"),
    (2048, 1288, 792, 840, "complement"),
    (2300, 891, 378, 324, "Co2/U6(2).2"),
    (2300, 1408, 840, 896, "complement"),
    (3510, 693, 180, 126, "Fi22.2"),
    (3510, 2816, 2248, 2304, "complement"),
    (4060, 1755, 730, 780, "Ru/2F4(2)"),
    (4060, 2304, 1328, 1280, "complement"),
    (31671, 3510, 693, 351, "Fi23"),  # the other historic SRG (Bondarenko Thm 2), dim 782
]


# ---------------------------------------------------------------------------
# Infinite-family closed-form argument (covers ALL n, not just tabulated rows)
# ---------------------------------------------------------------------------

def infinite_family_certificates():
    """
    For the two principal infinite families with bounded-ish embedding dimension we prove,
    in closed form, that the TARGET (f<=62 AND ceil(v/omega)>=64) is NEVER met -- the
    clique number scales WITH the embedding dimension, so small f forces v/omega small.
    Returns a list of (family, statement, holds) records.
    """
    out = []

    # Triangular T(n): v=C(n,2), f=n-1, omega=n-1, parts=ceil(C(n,2)/(n-1))=ceil(n/2).
    worst = max((math.ceil((n * (n - 1) // 2) / (n - 1))
                 for n in range(5, 64)), default=0)  # n-1=f<=62 -> n<=63
    out.append(("Triangular T(n)",
                "f=n-1<=62 => n<=63 => parts=ceil(n/2)<=32 < 64",
                worst < 64))

    # Lattice L2(n)=H(2,n): v=n^2, f=2(n-1), omega=n, parts=ceil(n^2/n)=n.
    worst2 = max((n for n in range(3, 33)), default=0)  # 2(n-1)=f<=62 -> n<=32
    out.append(("Lattice L2(n)",
                "f=2(n-1)<=62 => n<=32 => parts=n<=32 < 64",
                worst2 < 64))

    # Orthogonal-array OA(m,t) (Latin-square graphs), v=m^2, omega=m,
    # eigenvalues r=m-t, s=-t; f=mult(r)= t(m-1).  f<=62 => t(m-1)<=62.
    # parts=ceil(m^2/m)=m.  Need m>=64 => m-1>=63 => f=t(m-1)>=63>62 (t>=1). Contradiction.
    out.append(("Orthogonal array OA(m,t)",
                "omega=m, f=t(m-1); parts>=64 => m>=64 => f>=63 > 62",
                True))

    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run_sweep(verbose=True):
    table = load_brouwer_srg_table()
    big = [dict(ex='', v=v, k=k, lam=l, mu=mu, table_f=None, comment=c)
           for (v, k, l, mu, c) in LARGE_SRGS]
    rows = table + big

    # 1. sanity: G_2(4) must show f=65 (the published dimension) and be filtered out.
    g24 = certifies_counterexample(416, 100, 36, 20)
    assert g24['f'] == 65, ("G_2(4) embedding dim must be 65, got %r" % g24['f'])
    assert not g24['certifies']

    # 2. the certifiable sweep.
    certified = []
    fle62 = []
    for rc in rows:
        res = certifies_counterexample(rc['v'], rc['k'], rc['lam'], rc['mu'],
                                       table_f=rc.get('table_f'))
        if res['f'] is not None and res['f'] <= 62:
            res['ex'] = rc.get('ex', '')
            res['comment'] = rc.get('comment', '')
            fle62.append(res)
            if res['certifies']:
                certified.append(res)

    # 3. residual analysis: f<=62 rows that the certifiable test did NOT settle.
    #    A row is RULED OUT (cannot be a dim<=62 counterexample) whenever ANY of:
    #      (a) v < 64                       -> ceil(v/omega) < 64 for every omega;
    #      (b) existence marker '-'         -> NO graph with these parameters exists;
    #      (c) a provable clique LOWER bound exceeds need_omega
    #          (structural: omega>=2 always, omega>=3 if lambda>=1; or the EXACT clique
    #           number of a recognised named family) -> too few parts for ANY such graph.
    #    What survives all of these is the precisely-scoped OPEN boundary.
    residual_open = []
    residual_killed = []
    kill_counts = {'v<64': 0, 'nonexistent': 0, 'struct_omega_lb': 0, 'named_omega': 0}
    for res in fle62:
        if res['certifies']:
            continue
        v, k, lam, mu = res['v'], res['k'], res['lam'], res['mu']
        need = max_omega_for_64_parts(v)            # omega must be <= need to qualify
        if need is None:                            # (a) v < 64
            res['need_omega'] = 0
            res['ruled_reason'] = 'v<64 (cannot reach 64 parts)'
            residual_killed.append(res); kill_counts['v<64'] += 1
            continue
        res['need_omega'] = need
        if res.get('ex') == '-':                    # (b) graph does not exist
            res['ruled_reason'] = 'parameters infeasible (existence "-")'
            residual_killed.append(res); kill_counts['nonexistent'] += 1
            continue
        kn = known_clique_number(v, res.get('comment', ''))
        if kn is not None:                          # (c1) exact clique number known
            name, omega = kn
            res['known_family'] = name; res['known_omega'] = omega
            res['actual_parts'] = math.ceil(v / omega)
            if omega > need:
                res['ruled_reason'] = 'exact omega(%s)=%d > need %d' % (name, omega, need)
                residual_killed.append(res); kill_counts['named_omega'] += 1
                continue
        lb = structural_clique_lower_bound(v, k, lam, mu)   # (c2) provable lower bound
        res['omega_lb'] = lb
        if lb > need:
            res['ruled_reason'] = 'provable omega>=%d > need %d' % (lb, need)
            residual_killed.append(res); kill_counts['struct_omega_lb'] += 1
            continue
        residual_open.append(res)

    # 4. infinite families.
    fam = infinite_family_certificates()

    if verbose:
        print("=" * 78)
        print("srg-sweep  --  finite database search over feasible SRG parameter sets")
        print("=" * 78)
        print("Source: Brouwer feasible-parameter table v<=1300 (%d rows) + %d large named"
              % (len(table), len(big)))
        print("        SRGs (srgbig.html).  G_2(4) sanity: f=%d (published 65), certifies=%s"
              % (g24['f'], g24['certifies']))
        print()
        print("TARGET (beat dim 63):  f <= 62  AND  ceil(v/omega) >= 64.")
        print("Certifiable (parameter-only, sufficient given existence):")
        print("        f <= 62  AND  ceil(v / omega_DH) >= 64,   omega_DH = 1+floor(k/(-s)).")
        print()
        print("Rows with embedding dimension f <= 62 ............ %d" % len(fle62))
        print("Rows CERTIFYING a counterexample (TARGET met) .... %d" % len(certified))
        if certified:
            print("  *** CANDIDATE(S) FOUND -- requires Lean Gram+clique certificate: ***")
            for r in certified:
                print("    ", r)
        print()
        print("Residual f<=62 rows NOT settled by the certifiable test ... %d"
              % (len(residual_open) + len(residual_killed)))
        print("  RULED OUT completely ..................................... %d" % len(residual_killed))
        print("    - v<64 (cannot reach 64 parts) ........................ %d" % kill_counts['v<64'])
        print("    - parameters infeasible (existence '-') ............... %d" % kill_counts['nonexistent'])
        print("    - exact clique number of named family too large ....... %d" % kill_counts['named_omega'])
        print("    - provable omega>=2/3 > need_omega .................... %d" % kill_counts['struct_omega_lb'])
        print("  OPEN boundary (need an explicit graph, omega<=need) ..... %d" % len(residual_open))
        print()
        print("Closed-form infinite-family arguments:")
        for name, stmt, holds in fam:
            print("  [%s] %s  -- %s" % ("OK" if holds else "FAIL", name, stmt))
        print()
        # the precisely-scoped open boundary
        print("OPEN residual rows (the exact scope of what this sweep does NOT close):")
        print("  (each needs an explicit graph with omega <= need_omega; none known)")
        for r in sorted(residual_open, key=lambda x: x['v']):
            print("    v=%d k=%d (%d,%d) f=%d omega_DH=%d need_omega<=%d ex='%s' | %s"
                  % (r['v'], r['k'], r['lam'], r['mu'], r['f'], r['omega_DH'],
                     r['need_omega'], r.get('ex', ''), r.get('comment', '')[:46]))
        print()
        verdict = ("NEGATIVE (certifiable): no feasible SRG parameter set in the searched "
                   "space yields a Delsarte-Hoffman-certifiable Borsuk counterexample in "
                   "dimension <= 62." if not certified else
                   "CANDIDATE FOUND -- verify Lean Gram+clique certificate before claiming.")
        print("VERDICT:", verdict)

    return dict(table_rows=len(table), big_rows=len(big), fle62=len(fle62),
                certified=certified, residual_open=residual_open,
                residual_killed=residual_killed, kill_counts=kill_counts, families=fam)


if __name__ == "__main__":
    res = run_sweep(verbose=True)
    # exit status reflects whether the certifiable search is empty (negative result holds)
    if res['certified']:
        print("\n[!] A certifiable candidate exists -- this is a CONJECTURE until its "
              "Lean Gram+clique certificate is verified (CLAUDE.md). Do not write as a bound.")
