#!/usr/bin/env python3
"""Phased SV and 5mC counts of the LongPhase 2 co-phasing runs, before and after GNN correction.
For each run: heterozygous records (GT 0|1, 1|0 or 0/1) and phased ones (0|1 or 1|0) in
<prefix>_SV.vcf and <prefix>_mod.vcf, on chr1-22 and on all contigs.
Usage: count_sv_mod.py <config> <coverage>x_<replicate>   (prints one TSV line)"""
import sys, re
R = '/disk/research'
AUTO = {f'chr{i}' for i in range(1, 23)}
def count(p):
    het = ph = het_a = ph_a = 0
    for l in open(p):
        if l[0] == '#': continue
        t = l.split('\t', 10)
        if len(t) < 10: continue
        gt = t[9].split(':', 1)[0].strip()
        if gt not in ('0|1', '1|0', '0/1'): continue
        p_ = gt != '0/1'
        het_a += 1; ph_a += p_
        if t[0] in AUTO: het += 1; ph += p_
    return het, ph, het_a, ph_a
cfg, run = sys.argv[1:3]
c, r = re.match(r'(\d+)x_(\d+)', run).groups()
out = [cfg, c, r]
for g in ('', '_gnn'):
    pre = f'{R}/longphase_{cfg}{g}/longphase_{cfg}{g}_{run}'
    for kind in ('SV', 'mod'):
        try: out += count(f'{pre}_{kind}.vcf')
        except FileNotFoundError: out += ['NA'] * 4
print('\t'.join(map(str, out)))
