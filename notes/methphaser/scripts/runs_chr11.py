#!/usr/bin/env python3
"""Issue 5: runs of consecutive phased heterozygous records with PS -1 on chr11, 30x, in the
output VCF written before the PS lookup fix, with their input PS and their PS after the fix."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ps_overlap import records

W = '/disk/research/methphaser/rerun_0.0.4/30x/'
pos_ps = lambda path: {p: ps for c, p, *_, ps in records(path) if c == 'chr11'}
inp = pos_ps('/disk/research/methphaser/test/30x/longphase_30x_1.vcf.gz')
fix = pos_ps(W + 'methphaser_30x_1.psfix.fixed.vcf')
recs = [(p, ps) for c, p, *_, ps in records(W + 'methphaser_30x_1.fixed.vcf') if c == 'chr11']
runs = []
for i, (p, ps) in enumerate(recs):
    if ps != '-1':
        continue
    if runs and runs[-1]['last'] == i - 1:
        r = runs[-1]; r['end'] = p; r['n'] += 1; r['last'] = i
    else:
        runs.append(dict(start=p, end=p, n=1, last=i, inp=set(), fix=set()))
    runs[-1]['inp'].add(inp[p]); runs[-1]['fix'].add(fix[p])
print('start\tend\trecords\tinput_PS\tPS_after_fix')
for r in runs:
    print(f"{r['start']}\t{r['end']}\t{r['n']}\t{','.join(sorted(r['inp']))}\t{','.join(sorted(r['fix']))}")
