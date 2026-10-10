#!/usr/bin/env python3
"""GCphase output against its input: for each input (GT, FILTER), how many records come out
phased (GT with |), unchanged or absent. Records matched by CHROM, POS, REF and ALT.
Usage: genotype_transitions.py <input.vcf.gz> <gcphase_output.vcf.gz>"""
import gzip, sys, collections
inp, out = sys.argv[1:3]
def rd(p):
    d = {}
    for l in gzip.open(p, 'rt'):
        if l[0] == '#': continue
        t = l.rstrip('\n').split('\t')
        d[(t[0], t[1], t[3], t[4])] = (t[6], t[9].split(':')[0])
    return d
a, b = rd(inp), rd(out)
tr = collections.Counter()
for k, (flt, gt) in a.items():
    o = b.get(k)
    g = o[1] if o else 'absent'
    g = 'phased' if '|' in g else g
    tr[(gt, flt, g)] += 1
for (gt, flt, g), n in sorted(tr.items(), key=lambda x: -x[1])[:12]:
    print(f'{gt}\t{flt}\t-> {g}\t{n}')
print('output records not in input:', sum(1 for k in b if k not in a))
