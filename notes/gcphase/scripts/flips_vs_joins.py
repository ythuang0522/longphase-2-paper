#!/usr/bin/env python3
"""Where GCphase's phase flips lie relative to its block joins (chr20).
Needs a run with scripts/premerge_dump.patch, which writes the blocks before the join step
(block-FM/premerge-chr20.txt). A long-range flip is a change of agreement with v5.0q between two
runs of at least 50 SNVs within one output PS. Usage: flips_vs_joins.py <outpath>"""
import sys, collections
W = sys.argv[1]
def rd(p, chrom='chr20'):
    d = {}
    for l in open(p):
        if l[0] == '#': continue
        t = l.rstrip('\n').split('\t')
        if t[0] != chrom: continue
        f = dict(zip(t[8].split(':'), t[9].split(':')))
        if f.get('GT') in ('0|1', '1|0'): d[(t[1], t[3], t[4])] = (f['GT'], f.get('PS'))
    return d
truth = rd('/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf'); q = rd(W + '/result/mine.vcf')
pre = {}
for i, l in enumerate(open(W + '/block-FM/premerge-chr20.txt')):
    for x in l.rstrip('\n').split('\t'): pre[int(x[:-2])] = i
by = collections.defaultdict(list)
for k, (gt, ps) in q.items():
    if k in truth: by[ps].append((int(k[0]), gt == truth[k][0]))
ch_j = ch_i = lj = li = 0
for v in by.values():
    v.sort(); runs = []
    for (p0, s0), (p1, s1) in zip(v, v[1:]):
        if s0 != s1:
            if pre.get(p0) != pre.get(p1): ch_j += 1
            else: ch_i += 1
    for p, s in v:
        if runs and runs[-1][0] == s: runs[-1][2] = p; runs[-1][3] += 1
        else: runs.append([s, p, p, 1])
    for x, y in zip(runs, runs[1:]):
        if x[3] >= 50 and y[3] >= 50:
            if pre.get(x[2]) != pre.get(y[1]): lj += 1
            else: li += 1
print(f'pre-join blocks {len(set(pre.values()))}')
print(f'state changes: at joins {ch_j}, inside pre-join blocks {ch_i}')
print(f'long-range flips: at joins {lj}, inside pre-join blocks {li}')
