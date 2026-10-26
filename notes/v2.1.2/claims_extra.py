#!/usr/bin/env python3
"""Values of the text that notes/v2.1.1/claims.py does not compute (2026-10-26, v2.1.2 update):
co-phasing before GNN correction (Results, evidence-class paragraph), four-class blocks against SNV +
indel + 5mC and against WhatsHap with indels, and HapBridge / LongHap against LongPhase 2 (replicate 1).
    python claims_extra.py ROOT"""
import os, sys, statistics as st
from collections import defaultdict
import openpyxl
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
wb = openpyxl.load_workbook(os.path.join(ROOT, 'supplementary.xlsx'), read_only=True, data_only=True)
COVS = [10, 12, 14, 16, 18, 20, 30, 40, 50, 60]
COPH = ['psnv', 'psnv_pct', 'pindel', 'pindel_pct', 'sw', 'sw_pct', 'ham', 'nblock', 'n50', 'bsum']
d = defaultdict(list)
R = [r for r in wb['co-phase_Detail'].iter_rows(values_only=True)]
blk = {('gnn' if h.startswith('longphase_v2.1') else 'no' if h == 'longphase_v2.0.1' else h): i for i, h in enumerate(R[0]) if h}
for r in R[2:]:
    if r[2] and r[3]:
        c, rep = map(int, r[3].split('x_'))
        for name, i0 in blk.items():
            if r[i0] is not None:
                d[(r[2], name, c)].append(dict(zip(COPH, r[i0:i0 + 10]), rep=rep))
S = [r for r in wb['SNV_Detail'].iter_rows(values_only=True)]
sb = {('gnn' if h.startswith('longphase_v2.1') else 'no' if h == 'longphase_v2.0.1' else h): i for i, h in enumerate(S[0]) if h}
for r in S[2:]:
    if r[1] and str(r[1]).startswith('ONT'):
        c, rep = map(int, r[2].split('x_'))
        for name, i0 in sb.items():
            if r[i0] is not None:
                d[('SNV', name, c)].append(dict(psnv_pct=r[i0 + 1], sw_pct=r[i0 + 3], ham=r[i0 + 4], n50=r[i0 + 6], rep=rep))
m = lambda cfg, t, c, k: st.mean(float(x[k]) for x in d[(cfg, t, c)])
pct = lambda xs: f'{min(xs):.1f}--{max(xs):.1f}'
rel = lambda cfg, t, k, base='SNV': [100 * (m(cfg, t, c, k) / m(base, t, c, k) - 1) for c in COVS]
print('before.SV n50 +%', pct(rel('SV', 'no', 'n50')), 'rate %', pct(rel('SV', 'no', 'sw_pct')))
print('before.Mod n50 +%', pct(rel('Mod', 'no', 'n50')), 'rate %', pct(rel('Mod', 'no', 'sw_pct')))
print('before.Indel n50 +%', pct(rel('Indel', 'no', 'n50')), 'rate %', pct(rel('Indel', 'no', 'sw_pct')))
w = [x for cfg in ('Indel+SV', 'Mod+Indel', 'Indel+Mod+SV') for x in rel(cfg, 'no', 'n50')]
print('before.indel+SV/5mC n50 +%', pct(w))
print('before.all-indel-cfg rate %', pct([x for cfg in ('Indel', 'Indel+SV', 'Mod+Indel', 'Indel+Mod+SV') for x in rel(cfg, 'no', 'sw_pct')]))
print('four/ModIndel n50', ' '.join(f"{c}:{m('Indel+Mod+SV', 'gnn', c, 'n50') / m('Mod+Indel', 'gnn', c, 'n50'):.4f}" for c in COVS))
print('four/WHindel n50', ' '.join(f"{c}:{m('Indel+Mod+SV', 'gnn', c, 'n50') / m('Indel', 'whatshap_v28', c, 'n50'):.4f}" for c in COVS))
