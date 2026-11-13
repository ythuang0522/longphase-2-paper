#!/usr/bin/env python3
"""gaps.py: assembly N-gaps of the HG008-N v6.3 haplotype FASTAs -> asm/hap{1,2}.gaps.bed (assembly coordinates,
0-based half-open), the input make_truth.py maps to GRCh38 through the dipcall alignments. Run in /disk/research/HG008/asm.
Reconstructed from the command run on 2026-11-10 (same logic; it was run inline, not from a file)."""
import gzip, re

for h in (1, 2):
    seqs, name = {}, None
    for l in gzip.open(f'HG008N_v6.3_hap{h}.fasta.gz', 'rt'):
        if l[0] == '>': name = l[1:].split()[0]; seqs[name] = []
        else: seqs[name].append(l.strip())
    with open(f'hap{h}.gaps.bed', 'w') as g:
        for n, v in seqs.items():
            for m in re.finditer('N+', ''.join(v).upper()): g.write(f'{n}\t{m.start()}\t{m.end()}\n')
