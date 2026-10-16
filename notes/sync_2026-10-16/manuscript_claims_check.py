#!/usr/bin/env python3
"""Recompute merge-sensitive manuscript claims from the synced remote data.
Run with a Python environment containing openpyxl. Prints JSON; does not edit sources.
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.argv = ['claims.py', str(ROOT)]
with contextlib.redirect_stdout(io.StringIO()):
    d = runpy.run_path(str(ROOT / 'notes/v2.1.1/claims.py'))
S, C, WH, HC, covs = (d[k] for k in ('S', 'C', 'WH', 'HC', 'COVS'))
mean, ind = d['mean'], d['ind']
indel_ham = [mean([float(x['indel_hamming%']) for x in ind[('whatshap_v28', c, 'all')]]) /
             mean([float(x['indel_hamming%']) for x in ind[('longphase_coh_indel_gnn', c, 'all')]])
             for c in covs]
range_fmt = lambda xs, fmt='.1f': f'{min(xs):{fmt}}--{max(xs):{fmt}}'
checks = {
    'snv_switch_rate_percent': range_fmt([S('lp_gnn', c, 'sw_pct') for c in covs], '.3f'),
    'snv_whatshap_ratio': range_fmt([S(WH, c, 'sw_pct') / S('lp_gnn', c, 'sw_pct') for c in covs]),
    'snv_hapcut_ratio': range_fmt([S(HC, c, 'sw_pct') / S('lp_gnn', c, 'sw_pct') for c in covs]),
    'snv_n50_longer_percent_30_60': range_fmt([100 * (S('lp_gnn', c, 'n50') / S(WH, c, 'n50') - 1) for c in covs[6:]], '.0f'),
    'snv_hamming_ratio_30_60': range_fmt([S(WH, c, 'ham') / S('lp_gnn', c, 'ham') for c in covs[6:]]),
    'indel_n50_wh_longer_percent': range_fmt([100 * (C('Indel', WH, c, 'n50') / C('Indel', 'lp_gnn', c, 'n50') - 1) for c in covs], '.0f'),
    'indel_hamming_wh_ratio': range_fmt(indel_ham),
    'hifi_wh_ratio': range_fmt([S(WH, c, 'sw_pct', 'HiFi') / S('lp_gnn', c, 'sw_pct', 'HiFi') for c in (10, 20, 30, 40, 50)]),
    'hifi_hapcut_ratio': range_fmt([S(HC, c, 'sw_pct', 'HiFi') / S('lp_gnn', c, 'sw_pct', 'HiFi') for c in (10, 20, 30, 40, 50)]),
    'heldout_overall_ratio': range_fmt([d['HM'](t, c, 'sw_pct') / d['HM']('longphase_gnn', c, 'sw_pct') for t in ('whatshap_v28_onlySNVs', 'hapcut2_v134') for c in covs]),
    'all_indel_configurations_pair_error_reduction_percent': range_fmt(d['ip'], '.0f'),
    'workbook_sheet_count': len(d['wb'].sheetnames),
}
expected = {
    'snv_switch_rate_percent': '0.022--0.081', 'snv_whatshap_ratio': '2.9--3.9',
    'snv_hapcut_ratio': '3.3--5.0', 'snv_n50_longer_percent_30_60': '2--5',
    'snv_hamming_ratio_30_60': '1.4--1.8', 'indel_n50_wh_longer_percent': '12--33',
    'indel_hamming_wh_ratio': '1.8--2.7', 'hifi_wh_ratio': '2.4--2.8',
    'hifi_hapcut_ratio': '2.9--3.5', 'heldout_overall_ratio': '2.7--5.1',
    'all_indel_configurations_pair_error_reduction_percent': '22--40', 'workbook_sheet_count': 13,
}
assert checks == expected, (checks, expected)
texts = {f: (ROOT/f).read_text() for f in ['main.tex', 'Supplementary.tex', 'sections/results.tex', 'sections/methods.tex', 'sections/discussion.tex']}
for f, text in texts.items():
    assert all(marker not in text for marker in ('<<<<<<<', '>>>>>>>', '|||||||')), f
for key in ('snv_switch_rate_percent', 'snv_whatshap_ratio', 'snv_hapcut_ratio', 'hifi_wh_ratio', 'hifi_hapcut_ratio', 'heldout_overall_ratio', 'all_indel_configurations_pair_error_reduction_percent'):
    assert checks[key] in texts['sections/results.tex'], key
for key in ('snv_n50_longer_percent_30_60', 'snv_hamming_ratio_30_60', 'indel_n50_wh_longer_percent', 'indel_hamming_wh_ratio'):
    assert checks[key] in texts['sections/methods.tex'], key
assert 'The 13 sheets' in texts['Supplementary.tex']
assert '12, 30 and 50' in texts['sections/results.tex']
assert 'score threshold 0.35' in texts['sections/methods.tex']
assert 'f9962dddcf1f9153f81f87aa1b15d9c2c5c7d9dd' in texts['sections/methods.tex']
assert r'\textbf{e}, SNV phasing of PacBio HiFi data compared with \whatshap and \hapcut.' in texts['Supplementary.tex']
assert r'\textbf{d}, SNV and 5mC co-phasing compared with MethPhaser' in texts['main.tex']
assert r'\textbf{e}, Accuracy and contiguity by evidence type' in texts['main.tex']
sources = ['supplementary.xlsx', 'notes/benchmark_strata/item3_indel.tsv', 'notes/heldout/heldout_v50q.txt']
print(json.dumps({'status': 'PASS', 'claims': checks, 'source_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}}, indent=2))
