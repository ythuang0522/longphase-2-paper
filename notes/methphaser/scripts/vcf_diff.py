#!/usr/bin/env python3
"""Compare a MethPhaser output VCF with its input VCF (issue #5, step 2).
Records are matched by (CHROM, POS, REF, ALT). Reports records whose GT or PS changed,
and the number of phase blocks (distinct (CHROM, PS)) before and after."""
import gzip, sys

def load(path):
    op = gzip.open if path.endswith('.gz') else open
    d = {}
    with op(path, 'rt') as f:
        for line in f:
            if line[0] == '#':
                continue
            t = line.rstrip('\n').split('\t')
            fmt = t[8].split(':'); smp = t[9].split(':')
            v = dict(zip(fmt, smp))
            d[(t[0], t[1], t[3], t[4])] = (v.get('GT', '.'), v.get('PS', '.'))
    return d

cov, a, b = sys.argv[1], load(sys.argv[2]), load(sys.argv[3])
common = a.keys() & b.keys()
gt = sum(a[k][0] != b[k][0] for k in common)
ps = sum(a[k][1] != b[k][1] for k in common)
either = sum(a[k] != b[k] for k in common)
blocks = lambda d: len({(k[0], v[1]) for k, v in d.items() if v[1] not in ('.', '')})
print('\t'.join(map(str, [cov, len(a), len(b), len(common), gt, ps, either, blocks(a), blocks(b)])))
