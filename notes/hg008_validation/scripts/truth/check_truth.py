#!/usr/bin/env python3
"""check_truth.py: checks of HG008N_v6.3_truth.vcf for paper issue #11 (written to check_truth.txt).
 1. sample name, chromosomes, GT values, FILTER;
 2. 300 random truth het SNVs (seed 1): the GT's left allele must be the hap1 base and the right allele the hap2 base at
    that position in the filtered dipcall haplotype alignments (hap1.bam / hap2.bam);
 3. every truth PS lies on one chromosome, PS intervals do not overlap."""
import random, pysam, collections
random.seed(1)
V = [l.rstrip('\n').split('\t') for l in open('HG008N_v6.3_truth.vcf') if l[0] != '#']
print('sample', [l for l in open('HG008N_v6.3_truth.vcf') if l.startswith('#CHROM')][0].split()[-1])
print('chromosomes', len({v[0] for v in V}))
print('GT', collections.Counter(v[9].split(':')[0] for v in V).most_common())
print('FILTER', collections.Counter(v[6] for v in V))
snv = [v for v in V if len(v[3]) == 1 and len(v[4]) == 1 and v[9][:3] in ('0|1', '1|0')]
H = {1: pysam.AlignmentFile('HG008N_v6.3_GRCh38.hap1.bam'), 2: pysam.AlignmentFile('HG008N_v6.3_GRCh38.hap2.bam')}
ok = bad = nocov = 0
for v in random.sample(snv, 300):
    c, p = v[0], int(v[1]) - 1; al = [v[3], v[4]]; g = v[9][:3]; exp = {1: al[int(g[0])], 2: al[int(g[2])]}; got = {}
    for h in (1, 2):
        bs = set()
        for r in H[h].fetch(c, p, p + 1):
            if r.is_secondary: continue
            for q, rp in r.get_aligned_pairs(matches_only=True):
                if rp == p: bs.add(r.query_sequence[q].upper()); break
        got[h] = bs
    if not got[1] or not got[2]: nocov += 1
    elif got[1] == {exp[1]} and got[2] == {exp[2]}: ok += 1
    else: bad += 1; print('mismatch', c, p + 1, g, al, got)
print('allele check, 300 random het SNVs: match', ok, 'mismatch', bad, 'no aligned base', nocov)
span = collections.defaultdict(lambda: [None, 0, 0]); chrom = collections.defaultdict(set)
for v in V:
    ps = int(v[9].split(':')[-1]); p = int(v[1]); chrom[ps].add(v[0]); s = span[ps]
    s[0] = v[0]; s[1] = p if not s[1] else min(s[1], p); s[2] = max(s[2], p)
print('PS on more than one chromosome', sum(len(x) > 1 for x in chrom.values()))
iv = sorted((c, a, b) for c, a, b in span.values()); ov = sum(1 for x, y in zip(iv, iv[1:]) if x[0] == y[0] and y[1] <= x[2])
print('overlapping PS intervals', ov, 'PS', len(iv))
