"""Phase scorer for issue #1 (items 3 and 4), stratified by region.

Records, matching and blocks follow `longphase compare` (CompareProcess.cpp,
release v2.1):
  - a record is kept when it has an ALT, a diploid GT that is 0/1 or 1/0
    (first ALT only); it is phased when the second allele carries '|';
    a phased record without a usable PS gets PS 1 (whole chromosome)
  - truth and query are matched by (CHROM, POS, REF, first ALT)
  - intersection blocks are the (truth PS, query PS) groups of variants
    phased in both, sorted by position; blocks with one variant are dropped
  - switches: consecutive pairs of a block whose switch encodings differ.
    'all' uses every variant of the block; 'snv' uses the SNV-only
    subsequence of the block (compare's SNV_SW); 'indel' is the subset of
    'all' pairs in which at least one member is an indel
  - Hamming per block = min(mismatches, block size - mismatches)

Each pair is assigned to every region set that contains both of its
variants; each phased-in-both variant to every set that contains it.

Usage: score_phase.py TRUTH QUERY OUT_PREFIX
  writes OUT_PREFIX.tsv (counts per region set) and OUT_PREFIX.sw.tsv
  (one line per switch error: chrom, pos1, pos2 (0-based), type)
"""
import gzip
import os
import sys
from collections import defaultdict

import numpy as np

# directory holding the benchmark and stratification BEDs; default: data/truth
# of the lab-server checkout (see README.md)
REF_DIR = os.environ.get('ISSUE1_REGIONS', os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'truth'))
CHROMS = [f'chr{i}' for i in range(1, 23)]
BASE = {   # region sets that define where the benchmarks differ
    'v5bed': f'{REF_DIR}/HG002_GRCh38_v5.0q_smvar.benchmark.bed',
    'v4bed': f'{REF_DIR}/HG002_GRCh38_1_22_v4.2.1_benchmark_noinconsistent.bed',
}
STRATA = {
    'segdup': 'GRCh38_segdups.bed.gz',
    'tandem_repeat': 'GRCh38_AllTandemRepeats.bed.gz',
    'homopolymer': 'GRCh38_AllHomopolymers_ge7bp_imperfectge11bp_slop5.bed.gz',
    'satellite': 'GRCh38_satellites_slop5.bed.gz',
    'lowmap_segdup': 'GRCh38_alllowmapandsegdupregions.bed.gz',
    'not_difficult': 'GRCh38_notinalldifficultregions.bed.gz',
}
# region (by benchmark BED) x stratum; a cell is the conjunction of both
REGIONS = ['all', 'v5bed', 'v4bed', 'shared', 'v5only', 'v4only', 'neither']
STRATA_ORDER = ['any'] + list(STRATA)


def load_bed(path):
    iv = defaultdict(list)
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as f:
        for line in f:
            if line[0] == '#' or line.startswith(('track', 'browser')):
                continue
            c = line.split('\t', 3)
            if c[0] in CHROMS:
                iv[c[0]].append((int(c[1]), int(c[2])))
    out = {}
    for ch, v in iv.items():   # merge overlapping intervals
        v.sort()
        s, e = [], []
        for a, b in v:
            if e and a <= e[-1]:
                e[-1] = max(e[-1], b)
            else:
                s.append(a); e.append(b)
        out[ch] = (np.array(s, dtype=np.int64), np.array(e, dtype=np.int64))
    return out


def inside(bed, ch, pos):
    """Boolean array: 0-based positions inside the merged intervals."""
    if ch not in bed:
        return np.zeros(len(pos), dtype=bool)
    s, e = bed[ch]
    i = np.searchsorted(s, pos, side='right') - 1
    ok = i >= 0
    res = np.zeros(len(pos), dtype=bool)
    res[ok] = e[i[ok]] > pos[ok]
    return res


def load_vcf(path):
    """{chrom: list of (pos0, ref, alt, h0, h1, ps)}; h0 = -1 if unphased."""
    out = defaultdict(list)
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as f:
        for line in f:
            if line[0] == '#':
                continue
            c = line.rstrip('\n').split('\t', 10)
            if c[0] not in CHROMS or c[4] == '.' or len(c) < 10:
                continue
            fmt = c[8].split(':')
            val = c[9].split(':')
            if fmt[0] == 'GT':
                gt = val[0]
            else:
                if 'GT' not in fmt:
                    continue
                gi = fmt.index('GT')
                gt = val[gi] if gi < len(val) else '.'
            if len(gt) != 3 or gt[1] not in '|/':
                continue          # not diploid with one-digit alleles
            a0, a1 = gt[0], gt[2]
            if not ((a0 == '0' and a1 == '1') or (a0 == '1' and a1 == '0')):
                continue
            alt = c[4].split(',', 1)[0]
            if gt[1] == '|':
                ps = 1
                if 'PS' in fmt:
                    pi = fmt.index('PS')
                    if pi < len(val):
                        try:
                            ps = int(val[pi]) or 1
                        except ValueError:
                            ps = 1
                out[c[0]].append((int(c[1]) - 1, c[3], alt, int(a0), int(a1), ps))
            else:
                out[c[0]].append((int(c[1]) - 1, c[3], alt, -1, -1, 0))
    return out


def score(truth, query, sw_out):
    # counters keyed by (region, stratum, kind)
    cnt = defaultdict(int)
    tot = defaultdict(int)
    for ch in CHROMS:
        tv, qv = truth.get(ch, []), query.get(ch, [])
        qmap = {(p, r, a): (h0, ps) for p, r, a, h0, h1, ps in qv}
        common = []
        for p, r, a, h0, h1, ps in tv:
            m = qmap.get((p, r, a))
            if m is None or h0 < 0 or m[0] < 0:
                continue
            common.append((p, len(r) == 1 and len(a) == 1, h0, ps, m[0], m[1]))
        common.sort(key=lambda x: x[0])
        blocks = defaultdict(list)
        for x in common:
            blocks[(x[3], x[5])].append(x)
        # phased-in-both variants (all, including singleton blocks)
        P = np.array([x[0] for x in common], dtype=np.int64)
        S = np.array([x[1] for x in common], dtype=bool)
        pairs = []   # (pos1, pos2, kind, is_switch); kind 0 snv-subseq, 1 all-SNV-SNV, 2 all-with-indel
        ham_snv = ham_indel = ham_n = ham_n_indel = 0
        ham_all = 0
        for blk in blocks.values():
            n = len(blk)
            if n < 2:
                continue
            t = [x[2] for x in blk]; q = [x[4] for x in blk]
            mism = [t[k] != q[k] for k in range(n)]
            m = sum(mism)
            flip = m > n - m
            ham_all += min(m, n - m); ham_n += n
            ham_n_indel += sum(1 for x in blk if not x[1])
            for k in range(n):
                if mism[k] != flip:
                    if blk[k][1]: ham_snv += 1
                    else: ham_indel += 1
            for k in range(n - 1):
                sw = (t[k] ^ t[k + 1]) != (q[k] ^ q[k + 1])
                pairs.append((blk[k][0], blk[k + 1][0],
                              1 if blk[k][1] and blk[k + 1][1] else 2, sw))
            sidx = [k for k in range(n) if blk[k][1]]
            for a, b in zip(sidx, sidx[1:]):
                sw = (t[a] ^ t[b]) != (q[a] ^ q[b])
                pairs.append((blk[a][0], blk[b][0], 0, sw))
        tot['ham_all'] += ham_all; tot['ham_n'] += ham_n
        tot['ham_snv'] += ham_snv; tot['ham_indel'] += ham_indel
        tot['ham_n_indel'] += ham_n_indel
        # membership of variants and pair ends
        if not pairs:
            continue
        A = np.array(pairs, dtype=np.int64)
        p1, p2, kind, sw = A[:, 0], A[:, 1], A[:, 2], A[:, 3].astype(bool)

        def masks(pos):
            b5 = inside(BEDS['v5bed'], ch, pos); b4 = inside(BEDS['v4bed'], ch, pos)
            reg = {'all': np.ones(len(pos), bool), 'v5bed': b5, 'v4bed': b4,
                   'shared': b5 & b4, 'v5only': b5 & ~b4, 'v4only': b4 & ~b5,
                   'neither': ~b5 & ~b4}
            st = {'any': np.ones(len(pos), bool)}
            for k in STRATA:
                st[k] = inside(BEDS[k], ch, pos)
            return reg, st

        r1, s1 = masks(p1); r2, s2 = masks(p2); rv, sv = masks(P)
        for rg in REGIONS:
            for sn in STRATA_ORDER:
                pm = r1[rg] & r2[rg] & s1[sn] & s2[sn]
                vm = rv[rg] & sv[sn]
                cnt[(rg, sn, 'phased_snv')] += int((vm & S).sum())
                cnt[(rg, sn, 'phased_indel')] += int((vm & ~S).sum())
                for kname, km in (('snv', kind == 0), ('all', kind != 0),
                                  ('indel', kind == 2)):
                    mm = pm & km
                    cnt[(rg, sn, kname + '_pairs')] += int(mm.sum())
                    cnt[(rg, sn, kname + '_sw')] += int((mm & sw).sum())
        for i in np.nonzero(sw)[0]:
            sw_out.write(f'{ch}\t{p1[i]}\t{p2[i]}\t{("snv", "all_snv", "all_indel")[kind[i]]}\n')
    return cnt, tot


BEDS = {}


def init_beds():
    for k, p in BASE.items():
        BEDS[k] = load_bed(p)
    for k, f in STRATA.items():
        BEDS[k] = load_bed(f'{REF_DIR}/{f}')


KINDS = ['phased_snv', 'phased_indel', 'snv_pairs', 'snv_sw', 'all_pairs', 'all_sw',
         'indel_pairs', 'indel_sw']


def run(truth, query_path, prefix):
    query = load_vcf(query_path)
    with open(prefix + '.sw.tsv', 'w') as sw_out:
        cnt, tot = score(truth, query, sw_out)
    with open(prefix + '.tsv', 'w') as f:
        f.write('#ham_all\t%d\tham_n\t%d\tham_snv\t%d\tham_indel\t%d\tham_n_indel\t%d\n'
                % (tot['ham_all'], tot['ham_n'], tot['ham_snv'], tot['ham_indel'], tot['ham_n_indel']))
        f.write('region\tstratum\t' + '\t'.join(KINDS) + '\n')
        for rg in REGIONS:
            for sn in STRATA_ORDER:
                f.write(f'{rg}\t{sn}\t' + '\t'.join(str(cnt[(rg, sn, k)]) for k in KINDS) + '\n')


if __name__ == '__main__':
    init_beds()
    run(load_vcf(sys.argv[1]), sys.argv[2], sys.argv[3])
