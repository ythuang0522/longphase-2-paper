#!/usr/bin/env python3
"""make_truth.py: HG008-N v6.3 dipcall output -> phase-block-annotated GRCh38 truth VCF for paper issue #11.

Rules fixed before any phasing output was scored (2026-11-10):
  1. Scope: chr1-22, inside the dipcall BED (regions covered by one hap1 and one hap2 alignment of the assembly).
  2. Phase continuity needs one contiguous piece of BOTH haplotypes: on GRCh38, a truth block is a maximal interval
     covered by one filtered dipcall alignment of hap1 and one of hap2 (hapN.bam, the alignments dipcall genotypes from),
     with no assembly N-gap of either haplotype inside it (gaps are mapped to GRCh38 through the alignment CIGAR).
     Any change of the hap1 or hap2 alignment, or a gap on either haplotype, starts a new block.
  3. A run of more than MAXGAP (100 kb) between consecutive heterozygous dipcall records also starts a new block: across
     such a homozygous stretch the assembly's haplotype assignment rests on the assembler's long-range (Hi-C) phasing,
     not on read-level linkage.
  4. dipcall FILTER must be '.' (unfiltered) or PASS: HET1/HET2 (a haplotype heterozygous, i.e. overlapping alignments)
     and GAP1/GAP2 (uncalled on a haplotype) are dropped.
  5. Kept records: heterozygous, fully called, phased GT (0|1, 1|0 and, for multi-allelic sites, as in the file) inside a
     block; PS = block number (1-based, genome-wide). Homozygous and other records are dropped. REF/ALT, GT unchanged.
Usage: make_truth.py dip.vcf.gz dip.bed hap1.bam hap2.bam hap1.gaps.bed hap2.gaps.bed out_prefix
Writes out_prefix.vcf (truth), out_prefix.blocks.bed (block intervals = scoring mask, with PS), out_prefix.counts.tsv.
"""
import gzip, sys
from collections import defaultdict
import pysam

MAXGAP = 100_000
CHR = [f'chr{i}' for i in range(1, 23)]
dvcf, dbed, b1, b2, g1, g2, out = sys.argv[1:8]


def load_bed(p):
    d = defaultdict(list)
    for l in open(p):
        c, a, b = l.split()[:3]; d[c].append((int(a), int(b)))
    for c in d: d[c].sort()
    return d


def aln_pieces(bam, gaps):
    """GRCh38 intervals of one haplotype's dipcall alignments (primary and supplementary records, each a contiguous piece
    of one contig), split where an assembly N-gap of that contig falls -> {chrom: [(start, end, piece id)]}."""
    G = load_bed(gaps); P = defaultdict(list); n = 0
    for r in pysam.AlignmentFile(bam):
        if r.is_unmapped or r.is_secondary or r.reference_name not in CHR: continue
        ct = r.cigartuples; ql = sum(l for o, l in ct if o in (0, 1, 4, 5, 7, 8))   # contig length (H and S included)
        # gap coordinates on the contig -> coordinates along the alignment's query (reverse strand flips them)
        qs = []
        for a, b in G.get(r.query_name, []):
            if r.is_reverse: a, b = ql - b, ql - a
            qs += [a, b]
        cuts = []
        if qs:
            qs.sort(); k = 0; qp = 0; rp = r.reference_start
            for op, ln in ct:
                cq = op in (0, 1, 4, 5, 7, 8); cr = op in (0, 2, 3, 7, 8)
                if cq:
                    while k < len(qs) and qs[k] < qp + ln:
                        if qs[k] >= qp and op in (0, 7, 8): cuts.append(rp + qs[k] - qp)
                        elif qs[k] >= qp and op == 1: cuts.append(rp)
                        k += 1
                qp += ln if cq else 0; rp += ln if cr else 0
        bounds = [r.reference_start] + sorted(c for c in cuts if r.reference_start < c < r.reference_end) + [r.reference_end]
        for a, b in zip(bounds[:-1], bounds[1:]):
            n += 1
            P[r.reference_name].append((a, b, n))  # the gap itself is its own piece (no calls in N)
    for c in P: P[c].sort()
    return P


def overlay(A, B, D):
    """intersections of hap1 pieces, hap2 pieces and the dipcall BED: {chrom: [(start, end, (id1, id2))]}."""
    out = defaultdict(list)
    for c in CHR:
        ev = set()
        for L in (A.get(c, []), B.get(c, []), D.get(c, [])):
            for a, b, *_ in L: ev.add(a); ev.add(b)
        ev = sorted(ev)
        # sweep the elementary intervals (lists sorted by start)
        idx = {'A': 0, 'B': 0, 'D': 0}
        for a, b in zip(ev[:-1], ev[1:]):
            got = []
            for key, L in (('A', A.get(c, [])), ('B', B.get(c, [])), ('D', D.get(c, []))):
                i = idx[key]
                while i < len(L) and L[i][1] <= a: i += 1
                idx[key] = i; j = i; ids = []
                while j < len(L) and L[j][0] <= a:
                    if L[j][1] > a: ids.append(L[j][2] if len(L[j]) > 2 else 0)
                    j += 1
                got.append(ids)
            if all(len(g) == 1 for g in got):   # exactly one piece of each haplotype, inside the dipcall BED
                key = (got[0][0], got[1][0])
                if out[c] and out[c][-1][1] == a and out[c][-1][2] == key: out[c][-1] = (out[c][-1][0], b, key)
                else: out[c].append((a, b, key))
    return out


A = aln_pieces(b1, g1); B = aln_pieces(b2, g2); D = load_bed(dbed)
D = {c: [(a, b) for a, b in v] for c, v in D.items()}
R = overlay(A, B, D)
cnt = defaultdict(int)
# read heterozygous records, assign blocks, split at het deserts > MAXGAP
recs = defaultdict(list); hdr = []
with gzip.open(dvcf, 'rt') as f:
    for l in f:
        if l[0] == '#': hdr.append(l); continue
        x = l.rstrip('\n').split('\t'); c = x[0]
        if c not in CHR: continue
        gt = x[9].split(':')[0]; cnt['records chr1-22'] += 1
        if x[6] not in ('.', 'PASS'): cnt['dropped: dipcall FILTER (HET1/HET2/GAP1/GAP2)'] += 1; continue
        if '|' not in gt or '.' in gt: cnt['dropped: not fully called phased'] += 1; continue
        a1, a2 = gt.split('|')
        if a1 == a2: cnt['dropped: homozygous'] += 1; continue
        recs[c].append((int(x[1]) - 1, x))
ps = 0; blocks = []; kept = []
for c in CHR:
    L = R.get(c, []); i = 0; cur = None; last = None
    for p0, x in recs[c]:
        while i < len(L) and L[i][1] <= p0: i += 1
        # a record must lie wholly inside one interval (REF span)
        if i >= len(L) or L[i][0] > p0 or p0 + len(x[3]) > L[i][1]: cnt['dropped: outside reliable intervals'] += 1; continue
        if cur != i or last is None or p0 - last > MAXGAP:
            if cur == i and last is not None: cnt['block splits at het gaps > 100 kb'] += 1
            ps += 1; blocks.append([c, max(L[i][0], last + 1 if cur == i and last is not None else L[i][0]), None, ps]); cur = i
        last = p0; blocks[-1][2] = p0 + len(x[3])
        fmt = x[8].split(':'); val = x[9].split(':')
        if 'PS' in fmt: val[fmt.index('PS')] = str(ps)
        else: fmt.append('PS'); val.append(str(ps))
        kept.append('\t'.join(x[:8] + [':'.join(fmt), ':'.join(val)]))
        cnt['kept het records'] += 1
        cnt['kept het SNVs'] += len(x[3]) == 1 and all(len(a) == 1 for a in x[4].split(','))
with open(out + '.vcf', 'w') as o:
    for h in hdr:
        if h.startswith('#CHROM'):
            o.write('##FORMAT=<ID=PS,Number=1,Type=Integer,Description="Truth phase block (make_truth.py: one hap1 and one hap2 alignment piece, no assembly gap, no het gap > 100 kb)">\n')
        o.write(h)
    o.write('\n'.join(kept) + '\n')
with open(out + '.blocks.bed', 'w') as o:
    for c, a, b, p in blocks: o.write(f'{c}\t{a}\t{b}\t{p}\n')
iv_bp = sum(b - a for c in R for a, b, _ in R[c])
cnt['reliable interval bp (both haps, one piece each, in dipcall BED)'] = iv_bp
cnt['reliable intervals'] = sum(len(v) for v in R.values())
cnt['truth blocks (PS)'] = ps
with open(out + '.counts.tsv', 'w') as o:
    for k, v in cnt.items(): o.write(f'{k}\t{v}\n')
print(open(out + '.counts.tsv').read(), file=sys.stderr)
