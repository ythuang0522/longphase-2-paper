#!/usr/bin/env python3
"""Replace the rows of LongPhase 2 runs with SVs (longphase_coh_sv_gnn, longphase_coh_indel_sv_gnn) in
20260924_v50q.txt, 20260924_cophase_v50q.txt (v5.0q) and 20260924_GIAB421.txt (v4.2.1) with the summary
lines of the v2.1.2 `longphase compare` reports (/disk/research/v2.1.2; release v2.1 compare, as before).
The other rows (SNV-only and SNV + indel runs, other tools) are unchanged.

    python3 update_txt.py check   # every replaced row equals the v2.1.1 report; no write
    python3 update_txt.py write
"""
import os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
NEW, OLD = '/disk/research/v2.1.2', '/disk/research/v2.1.1'
GROUPS = ('longphase_coh_sv_gnn', 'longphase_coh_indel_sv_gnn')
FILES = {'20260924_v50q.txt': 'sw_', '20260924_cophase_v50q.txt': 'sw_', '20260924_GIAB421.txt': 'sw421_'}


def line_of(base, d, prefix, name):
    p = f'{base}/{d}/{prefix}{name}.tsv'
    if prefix == 'sw421_' and base == OLD:
        return None   # the v2.1.1 v4.2.1 reports are not kept beside the VCFs
    for l in open(p):
        if l.startswith('###') and not l.startswith('###Sample'):
            return l.rstrip('\n')


mode = sys.argv[1] if len(sys.argv) > 1 else 'check'
for fn, prefix in FILES.items():
    p = os.path.join(ROOT, fn); out = []; n = bad = 0
    for l in open(p).read().split('\n'):
        m = re.match(r'###((' + '|'.join(GROUPS) + r')_\d+x_\d+)\.vcf\t', l)
        if m:
            name, d = m.groups()
            if mode == 'check':
                o = line_of(OLD, d, prefix, name)
                if o is not None and o != l:
                    bad += 1; print('differs', fn, name)
            else:
                l = line_of(NEW, d, prefix, name); n += 1
        out.append(l)
    if mode == 'write':
        open(p, 'w').write('\n'.join(out)); print(fn, 'rows replaced:', n)
    else:
        print(fn, 'mismatches:', bad)
