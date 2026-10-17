#!/usr/bin/env python3
"""Merge the PEPPER calls (SNVs and indels) with the Sniffles 2.8 SVs that LongPhase takes as
--sv-file into one VCF for LongHap, which reads every variant type from one VCF and needs
sequence-resolved alleles. Sniffles writes deletions as <DEL> and insertions with REF N; these are
written with reference bases (DEL: REF = POS..POS+|SVLEN|, ALT = first base; INS: REF = base at POS,
ALT = that base + inserted sequence). Other SV types (INV, DUP, BND) have no sequence and are left
out. FORMAT of the SV records is GT only. Output: uncompressed VCF, sorted, chr1-22.

    merge_sv.py pepper.vcf.gz sniffles.vcf ref.fa out.vcf
"""
import gzip, sys
import pysam

pep, sv, ref, out = sys.argv[1:5]
fa = pysam.FastaFile(ref)
CHR = [f'chr{i}' for i in range(1, 23)]
recs = {c: [] for c in CHR}
head = []
with gzip.open(pep, 'rt') as f:
    for l in f:
        if l.startswith('#'):
            head.append(l)
            continue
        t = l.split('\t', 2)
        if t[0] in recs:
            recs[t[0]].append((int(t[1]), l))
n = {'DEL': 0, 'INS': 0, 'skip': 0}
for l in open(sv):
    if l.startswith('#'):
        continue
    t = l.rstrip('\n').split('\t')
    c, pos, alt = t[0], int(t[1]), t[4]
    if c not in recs:
        continue
    gt = t[9].split(':')[0]
    info = dict(x.split('=', 1) for x in t[7].split(';') if '=' in x)
    st = info.get('SVTYPE')
    if st == 'DEL' and alt == '<DEL>':
        L = abs(int(info['SVLEN']))
        r = fa.fetch(c, pos - 1, pos + L).upper(); a = r[0]
    elif st == 'DEL' and not alt.startswith('<') and t[3] != 'N':
        r, a = t[3], alt
    elif st == 'INS' and not alt.startswith('<'):
        b = fa.fetch(c, pos - 1, pos).upper()
        r, a = b, (alt if t[3] != 'N' else b + alt)
    else:
        n['skip'] += 1
        continue
    n[st] += 1
    recs[c].append((pos, '\t'.join([c, str(pos), t[2], r, a, t[5], 'PASS' if t[6] == 'PASS' else t[6], '.', 'GT', gt]) + '\n'))
with open(out, 'w') as o:
    o.writelines(head)
    for c in CHR:
        for _, l in sorted(recs[c], key=lambda x: x[0]):
            o.write(l)
print(out, n, file=sys.stderr)
