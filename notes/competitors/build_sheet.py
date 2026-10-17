#!/usr/bin/env python3
"""Write the sheet `Other_phasers` of supplementary.xlsx: the phasers added on 2026-10-17 (LongHap,
HapBridge, TinkerHap, HiPhase) and the SNV+indel runs of LongPhase, WhatsHap and HapCUT2 that the
indel-phasing tools are compared with. One row per run (replicate 1), from the `longphase compare`
reports of the runs (scripts/, README.md). Columns as in SNV_Detail and co-phase_Detail. The sheet
is rebuilt from scratch; no other sheet changes.

    python3 build_sheet.py          (run on the lab server; needs openpyxl)
"""
import os
import openpyxl
from openpyxl.styles import Font

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
X = os.path.join(ROOT, 'supplementary.xlsx')
SHEET = 'Other_phasers'
ONT, HIFI = [10, 20, 30, 40, 50, 60], [10, 20, 30, 40, 50]
S = '/ssd/longphase_process'
# platform, variant set, tool, coverages, report path ({c} = coverage)
RUNS = [
    ('ONT R10.4.1', 'SNV + 5mC', 'LongHap 0.2.0 (SNVs, with 5mC)', ONT, S + '/longhap/{c}x/sw_longhap_meth_{c}x_1.tsv'),
    ('ONT R10.4.1', 'SNV + 5mC', 'LongHap 0.2.0 (SNVs, sequence only)', ONT, S + '/longhap/{c}x/sw_longhap_seq_{c}x_1.tsv'),
    ('ONT R10.4.1', 'SNV + 5mC', 'HapBridge ec48f02 (on LongPhase 2 SNV output, no GNN)', ONT, S + '/hapbridge/sw_hapbridge_{c}x_1.tsv'),
    ('ONT R10.4.1', 'SNV + indel', 'HapCUT2 1.3.4 (--indels 1)', ONT, '/disk/research/hapcut2_v1.3.4/indels/sw_hapcut2_v134_indels_{c}x_1.tsv'),
    ('ONT R10.4.1', 'SNV + indel', 'TinkerHap 1.0.0', ONT, S + '/others_ont/sw_tinkerhap_{c}x_1.tsv'),
    ('ONT R10.4.1', 'SNV + indel + SV + 5mC', 'LongHap 0.2.0 (all variants, with 5mC)', ONT, S + '/longhap/allvar/sw_longhap_all_{c}x_1.tsv'),
    ('PB HiFi Revio', 'SNV + indel', 'LongPhase 2.1.1 (--indels)', HIFI, '/disk/research/v2.1.1/pacbio/indels/sw_longphase_hifi_indel_{c}x_1.tsv'),
    ('PB HiFi Revio', 'SNV + indel', 'WhatsHap 2.8 (indels)', HIFI, '/disk/research/pacbio/whatshap_v2.8_indels/sw_whatshap_v28_hifi_indels_{c}x_1.tsv'),
    ('PB HiFi Revio', 'SNV + indel', 'HapCUT2 1.3.4 (--indels 1)', HIFI, '/disk/research/pacbio/hapcut2_v1.3.4/indels/sw_hapcut2_v134_hifi_indels_{c}x_1.tsv'),
    ('PB HiFi Revio', 'SNV + indel', 'HiPhase 1.7.0', HIFI, '/disk/research/pacbio/hiphase_v1.7.0/sw_hiphase_v170_hifi_{c}x_1.tsv'),
    ('PB HiFi Revio', 'SNV + indel', 'TinkerHap 1.0.0', HIFI, S + '/extra/sw_tinkerhap_hifi_{c}x_1.tsv'),
]
HEAD = ['No.', 'Platform', 'Variant set', 'Tool', 'Case', 'Phased_SNV', 'Phased_SNV(%)', 'Phased_INDEL',
        'Phased_INDEL(%)', 'SNV_SW', 'SNV_SW(%)', 'HM_Dis.(%)', 'No. Block', 'Block_N50(bp)', 'Block_Sum']


def report(path):
    for l in open(path):
        if l.startswith('###') and not l.startswith('###Sample'):
            t = l.rstrip('\n').split('\t')
            return [int(t[1]), float(t[2]), int(t[3]), float(t[4]), int(t[5]), float(t[6]), float(t[7]),
                    int(t[8]), int(t[9]), int(t[10])]
    raise ValueError(path)


wb = openpyxl.load_workbook(X)
if SHEET in wb.sheetnames:
    del wb[SHEET]
ws = wb.create_sheet(SHEET)
for j, h in enumerate(HEAD, 1):
    c = ws.cell(1, j, h)
    c.font = Font(bold=True)
n = 0
for plat, vset, tool, covs, path in RUNS:
    for cov in covs:
        n += 1
        row = [n, plat, vset, tool, f'{cov}x_1'] + report(path.format(c=cov))
        for j, v in enumerate(row, 1):
            ws.cell(n + 1, j, v)
for j, w in enumerate([5, 14, 22, 50, 7] + [14] * 10, 1):
    ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
ws.freeze_panes = 'F2'
wb.save(X)
print(f'wrote {n} rows to {SHEET} in {X}')
