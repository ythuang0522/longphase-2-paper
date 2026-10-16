#!/usr/bin/env python3
"""Wall-clock time (min) of SNV-only phasing per run, HG002 nanopore, all tools on /disk/research.

10-20x: the author's table (longphaseGNN-RunTime.tsv), except that
  - every value that has a log is re-read from it (in the source table the replicate-1 rows repeat
    replicate 10, and LongPhase_v2.0.1 differs from its logs by up to 0.5 min); values without a
    log (GCphase, ralphi) are kept as they are,
  - LongPhase_GNN is replaced by longphase_v2.1.1 (/disk/research/v2.1.1, one `phase` command, -t 24).
30-60x (replicate 1 only): read from the logs; tools without a run at that coverage are left empty
  (GCphase, ralphi, Margin). HapCUT2 at 30x and 40x: the original logs were overwritten by a rerun
  stopped after 3-5 s, so these two runs were re-timed on 2026-10-16 (RERUN; same commands and
  inputs, phased genotypes identical to the paper's VCFs).
Times are GNU time `elapsed` (or `Elapsed (wall clock)` from time -v), rounded to 0.1 min.
"""
import csv, re, sys
R = '/disk/research'
SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/twolinin/Downloads/longphaseGNN-RunTime.tsv'
LOG = {
    'whatsap_v2.8': R + '/whatshap_v2.8/only/whatshap_v28_onlySNVs_{}.log',
    'margin_v2.3.1': R + '/margin_v2.3.1/margin_v231_{}.log',
    'hapcut2_v1.3.4': R + '/hapcut2_v1.3.4/hapcut2_v134_{}.log',
    'LongPhase_v2.0.1': R + '/longphase/longphase_{}.log',
    'longphase_v2.1.1': R + '/v2.1.1/longphase_gnn/longphase_gnn_{}.log',
}
RERUN = {('hapcut2_v1.3.4', f'{c}x_1'): f'/ssd/longphase_process/runtime/hapcut2_rerun/hapcut2_v134_{c}x_1.log'
         for c in (30, 40)}
MIN_S = 60   # shorter runs did not finish (the overwritten HapCUT2 30x/40x logs)

def minutes(path):
    try:
        t = open(path, errors='ignore').read()
    except OSError:
        return None
    m = re.findall(r'([\d:.]+)elapsed', t) or re.findall(r'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([\d:.]+)', t)
    if not m:
        return None
    p = [float(x) for x in m[-1].split(':')]
    s = p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0] * 60 + p[1]
    return None if s < MIN_S else s / 60

def fmt(v):
    return '' if v is None else f'{v + 1e-9:.1f}'

rows = list(csv.reader(open(SRC, newline=''), delimiter='\t'))
head = rows[1][:7] + ['longphase_v2.1.1']          # drop LongPhase_GNN
out = []
for r in rows[2:]:
    run = r[0]; d = dict(zip(rows[1], r))
    for col in ('whatsap_v2.8', 'margin_v2.3.1', 'hapcut2_v1.3.4', 'LongPhase_v2.0.1'):
        v = minutes(LOG[col].format(run))         # a value with a log is taken from the log
        if v is not None:
            d[col] = fmt(v)
    d['longphase_v2.1.1'] = fmt(minutes(LOG['longphase_v2.1.1'].format(run)))
    out.append([d.get(c, '') for c in head])
for c in (30, 40, 50, 60):
    run = f'{c}x_1'
    out.append([run, '', ''] + [fmt(minutes(RERUN.get((col, run), LOG[col].format(run)))) if col in LOG else ''
                                for col in head[3:]])
w = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
w.writerow(['Time(min)']); w.writerow(head); w.writerows(out)
