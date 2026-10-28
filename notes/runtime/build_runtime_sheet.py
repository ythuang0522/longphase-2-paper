#!/usr/bin/env python3
"""Write the Runtime sheet of supplementary.xlsx: SNV-only phasing time and peak memory, replicate 1, from
runtime.tsv and runtime_hifi.tsv (inputs and outputs on the hard-disk drive, the values of Supplementary
Table 16) and runtime_ssd.tsv (re-timed with inputs and outputs on an SSD). Column Storage gives the drive
of each value; in the SSD set, HapCUT2 at nanopore 60x and on HiFi data was not re-timed and keeps the HDD value."""
import csv, openpyxl
X = '../../supplementary.xlsx'
PLAT = {'nanopore': 'ONT R10.4.1', 'HiFi': 'PacBio HiFi'}
rows = []
for f, plat in (('runtime.tsv', 'nanopore'), ('runtime_hifi.tsv', 'HiFi'), ('runtime_ssd.tsv', None)):
    for r in csv.DictReader(open(f), delimiter='\t'):
        rows.append(['SSD' if plat is None else 'HDD', PLAT[r.get('platform', plat)], r['tool'], r['configuration'],
                     int(r['threads']), f"{r['coverage']}x_1", r.get('storage', 'HDD'), round(int(r['wall_s']) / 60, 2),
                     round(int(r['cpu_s']) / 60, 2), round(int(r['max_rss_kb']) / 1024 ** 2, 2)])
wb = openpyxl.load_workbook(X)
if 'Runtime' in wb.sheetnames: del wb['Runtime']
ws = wb.create_sheet('Runtime')
ws.append(['No.', 'Set', 'Platform', 'Tool', 'Configuration', 'Threads', 'Case', 'Storage',
           'Wall-clock (min)', 'CPU user+sys (min)', 'Peak RSS (GiB)'])
for n, r in enumerate(rows, 1):
    ws.append([n] + r)
for row in ws.iter_rows():
    for c in row: c.font = openpyxl.styles.Font(name='Arial', size=10)
ws.freeze_panes = 'H2'
wb.save(X)
print(len(rows), 'rows')
