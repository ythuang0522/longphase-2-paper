#!/usr/bin/env python3
"""chunk_fasta.py: cut each assembly contig into non-overlapping pieces of at most CHUNK bp (default 20 Mb), named
<contig>:<0-based start>. The COLO829BL DSA v3.0.0 contigs are chromosome-scale (45 per haplotype, up to 249 Mb), and
minimap2 -x asm5 needed >20 GB for the 249 Mb contig on this 15 GB machine. Truth blocks therefore also end at every cut
(conservative: a cut can only shorten a block). Usage: chunk_fasta.py in.fa.gz out.fa.gz [chunk]"""
import gzip, sys
CH = int(sys.argv[3]) if len(sys.argv) > 3 else 20_000_000
def emit(o, name, seq):
    s = ''.join(seq)
    for a in range(0, len(s), CH):
        o.write(f'>{name}:{a}\n')
        for i in range(a, min(a + CH, len(s)), 80): o.write(s[i:min(i + 80, a + CH, len(s))] + '\n')
with gzip.open(sys.argv[1], 'rt') as f, gzip.open(sys.argv[2], 'wt', compresslevel=1) as o:
    name, seq = None, []
    for l in f:
        if l[0] == '>':
            if name: emit(o, name, seq)
            name, seq = l[1:].split()[0], []
        else: seq.append(l.strip())
    if name: emit(o, name, seq)
