#!/usr/bin/env python3
"""Fill the HapCUT2 block (`hapcut2_v134`) of the PacBio HiFi rows of SNV_Detail in
supplementary.xlsx, which was empty, from the `longphase compare` reports of the HiFi HapCUT2
runs (2026-10-16, /ssd/longphase_process/runtime/run_hapcut2_hifi.sh):

    /disk/research/pacbio/hapcut2_v1.3.4/sw_hapcut2_v134_hifi_{c}x_1.tsv

Same columns and mapping as notes/v2.1.1/update_xlsx.py; each cell takes the style of the
WhatsHap cell of the same row. No other cell changes.

    python3 add_hapcut2.py          (run on the lab server)
"""
import copy, os
import openpyxl

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
X = os.path.join(ROOT, 'supplementary.xlsx')
SW = '/disk/research/pacbio/hapcut2_v1.3.4/sw_hapcut2_v134_hifi_{}.tsv'


def report(path):
    for l in open(path):
        if l.startswith('###') and not l.startswith('###Sample'):
            t = l.rstrip('\n').split('\t')
            return [int(t[1]), float(t[2]), int(t[5]), float(t[6]), float(t[7]), int(t[8]), int(t[9]), int(t[10])]
    raise ValueError(path)


wb = openpyxl.load_workbook(X)
ws = wb['SNV_Detail']
head = [c.value for c in ws[1]]
c0, cw = head.index('hapcut2_v134') + 1, head.index('whatshap_v28') + 1
n = 0
for r in range(3, ws.max_row + 1):
    if not str(ws.cell(r, 2).value or '').startswith('PB'):
        continue
    case = ws.cell(r, 3).value
    for i, v in enumerate(report(SW.format(case))):
        cell = ws.cell(r, c0 + i)
        assert cell.value is None or cell.value == v, (case, i, cell.value, v)
        cell.value = v
        cell._style = copy.copy(ws.cell(r, cw + i)._style)
    n += 1
wb.save(X)
print(f'filled {n} HiFi rows of hapcut2_v134 in {X}')
