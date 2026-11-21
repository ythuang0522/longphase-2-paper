#!/usr/bin/env python3
"""gaps.py: assembly N-gaps of a haplotype FASTA (gzip) -> BED in assembly coordinates (0-based half-open), as
notes/hg008_validation/scripts/truth/gaps.py. Usage: gaps.py hap.fa.gz out.bed"""
import gzip, re, sys
seqs, name = {}, None
for l in gzip.open(sys.argv[1], 'rt'):
    if l[0] == '>': name = l[1:].split()[0]; seqs[name] = []
    else: seqs[name].append(l.strip())
with open(sys.argv[2], 'w') as g:
    for n, v in seqs.items():
        for m in re.finditer('N+', ''.join(v).upper()): g.write(f'{n}\t{m.start()}\t{m.end()}\n')
