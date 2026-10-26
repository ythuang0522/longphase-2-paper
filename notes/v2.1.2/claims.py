#!/usr/bin/env python3
"""Recompute the numbers quoted in the manuscript text from the data files of a repository root.

    python3 claims.py ROOT          # prints one line per claim: id, value(s)

Copy of notes/v2.1.1/claims.py for the v2.1.2 update (2026-10-26). Run on an export of the committed
v2.1.1 data and on the v2.1.2 working tree; the differences are the values to change in the text. Every value is computed the way the [provenance] comments of the .tex files describe.
"""
import csv, gzip, os, re, statistics as st, sys
from collections import defaultdict
import openpyxl

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
COVS = [10, 12, 14, 16, 18, 20, 30, 40, 50, 60]
SNV_COLS = ['psnv', 'psnv_pct', 'sw', 'sw_pct', 'ham', 'nblock', 'n50', 'bsum']
COPH_COLS = ['psnv', 'psnv_pct', 'pindel', 'pindel_pct', 'sw', 'sw_pct', 'ham', 'nblock', 'n50', 'bsum']
OUT = []


def say(cid, *vals):
    OUT.append((cid, vals))
    print(cid, *vals, sep='\t', flush=True)


def f1(x): return f'{x:.1f}'
def f2(x): return f'{x:.2f}'
def rng(xs, fmt=f1): return f'{fmt(min(xs))}--{fmt(max(xs))}'
def mean(xs): return st.mean(xs)


# ------------------------------------------------------------------ Supplementary Data 1
wb = openpyxl.load_workbook(os.path.join(ROOT, 'supplementary.xlsx'), data_only=True, read_only=True)


def rows(name):
    return [r for r in wb[name].iter_rows(values_only=True) if any(c is not None for c in r)]


def blocks(head, width, start):
    out = {}
    for i, h in enumerate(head):
        if h and i >= start:
            out[h] = i
    return out


snv = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))   # plat, tool, cov -> runs
R = rows('SNV_Detail')
for name, i0 in blocks(R[0], 8, 3).items():
    for r in R[2:]:
        if r[i0] is None:
            continue
        plat = 'ONT' if r[1].startswith('ONT') else 'HiFi'
        cov, rep = int(r[2].split('x_')[0]), int(r[2].split('x_')[1])
        snv[plat]['lp_gnn' if name.startswith('longphase_v2.1') else name][cov].append(
            dict(zip(SNV_COLS, r[i0:i0 + 8]), rep=rep))
coph = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # cfg, tool, cov
R = rows('co-phase_Detail')
for name, i0 in blocks(R[0], 10, 4).items():
    for r in R[2:]:
        if r[i0] is None:
            continue
        cov, rep = int(r[3].split('x_')[0]), int(r[3].split('x_')[1])
        coph[r[2]]['lp_gnn' if name.startswith('longphase_v2.1') else name][cov].append(
            dict(zip(COPH_COLS, r[i0:i0 + 10]), rep=rep))
meth = {}
for r in rows('MethPhaser')[2:]:
    meth[int(r[2].split('x_')[0])] = dict(zip(SNV_COLS, r[3:11]))
LP0, WH, HC = 'longphase_v2.0.1', 'whatshap_v28', 'hapcut2_v134'


def M(runs, k): return mean([float(x[k]) for x in runs])
def S(tool, cov, k, plat='ONT'): return M(snv[plat][tool][cov], k)


def C(cfg, tool, cov, k):
    if cfg == 'SNV':
        return S(tool, cov, k)
    return M(coph[cfg][tool][cov], k)


def rep1(cfg, tool, cov, k):
    runs = snv['ONT'][tool][cov] if cfg == 'SNV' else coph[cfg][tool][cov]
    return float([x for x in runs if x['rep'] == 1][0][k])


# P1 SNV-only
say('P1.lp_sw_10_60', f"{S('lp_gnn', 10, 'sw_pct'):.3f}", f"{S('lp_gnn', 60, 'sw_pct'):.3f}")
for o in (WH, HC):
    rat = {c: S(o, c, 'sw_pct') / S('lp_gnn', c, 'sw_pct') for c in COVS}
    say(f'P1.ratio_{o}', f'{rat[10]:.3f}', rng([rat[c] for c in COVS if c >= 20]), 'all:', rng(rat.values()))
    paired = [float(a['sw_pct']) / float(b['sw_pct']) for c in COVS[:6]
              for a in snv['ONT'][o][c] for b in snv['ONT']['lp_gnn'][c] if a['rep'] == b['rep']]
    say(f'P1.paired_{o}', rng(paired))
ham = [S(o, c, 'ham') / S('lp_gnn', c, 'ham') for o in (WH, HC) for c in COVS]
say('P1.ham_ratio', rng(ham))
# P2 N50
say('P2.n50_10', rng([S(t, 10, 'n50') / 1e6 for t in ('lp_gnn', WH, HC)], f2),
    'n50_60', rng([S(t, 60, 'n50') / 1e6 for t in ('lp_gnn', WH, HC)], f2))
rel = {c: S('lp_gnn', c, 'n50') / S(WH, c, 'n50') for c in COVS}
say('P2.lp_vs_wh_n50', 'shorter 10-20 up to', f1(100 * (1 - min(rel[c] for c in COVS[:6]))),
    'longer 30-60', rng([100 * (rel[c] - 1) for c in COVS[6:]]), 'all', ' '.join(f'{rel[c]:.3f}' for c in COVS))
fc = {c: C('Indel+Mod+SV', 'lp_gnn', c, 'n50') / S(WH, c, 'n50') for c in COVS}
fr = {c: S(WH, c, 'sw_pct') / C('Indel+Mod+SV', 'lp_gnn', c, 'sw_pct') for c in COVS}
say('P2.fourclass_vs_whsnv', 'n50 +%', rng([100 * (fc[c] - 1) for c in COVS], lambda x: f'{x:.0f}'),
    'rate ratio', rng(fr.values()), f'10x {fr[10]:.1f} 20x {fr[20]:.1f}')
# P4 Ralphi / Margin
say('P4.ralphi', rng([S('ralphi', c, 'sw_pct') / S('lp_gnn', c, 'sw_pct') for c in COVS[:6]]))
say('P4.margin', f"10x {S('margin_v231', 10, 'sw_pct'):.3f} vs {S('lp_gnn', 10, 'sw_pct'):.3f}",
    f"12x {S('margin_v231', 12, 'sw_pct'):.4f} vs {S('lp_gnn', 12, 'sw_pct'):.4f}",
    '14-20', rng([S('margin_v231', c, 'sw_pct') / S('lp_gnn', c, 'sw_pct') for c in (14, 16, 18, 20)]),
    'blocks', rng([S('lp_gnn', c, 'n50') / S('margin_v231', c, 'n50') for c in COVS[:6]]))
# P6/P7 indels
r = [S(WH, c, 'sw_pct') for c in COVS]
say('P6.lp_indel_vs_wh_indel', rng([C('Indel', WH, c, 'sw_pct') / C('Indel', 'lp_gnn', c, 'sw_pct') for c in COVS]))
w = {c: C('Indel', WH, c, 'n50') / C('Indel', 'lp_gnn', c, 'n50') for c in COVS}
say('P7.wh_indel_longer', '10-18', rng([100 * (w[c] - 1) for c in COVS[:5]], lambda x: f'{x:.0f}'),
    '60', f'{100 * (w[60] - 1):.0f}', 'all', ' '.join(f'{w[c]:.3f}' for c in COVS))
q = {c: C('Indel+Mod+SV', 'lp_gnn', c, 'n50') / C('Indel', WH, c, 'n50') for c in COVS}
say('P7.fourclass_vs_wh_indel', 'shorter', rng([100 * (1 - q[c]) for c in COVS], lambda x: f'{x:.0f}'),
    '50-60', rng([100 * (1 - q[c]) for c in (50, 60)], lambda x: f'{x:.0f}'),
    'rate ratio', rng([C('Indel', WH, c, 'sw_pct') / C('Indel+Mod+SV', 'lp_gnn', c, 'sw_pct') for c in COVS]),
    f"60x {C('Indel+Mod+SV', 'lp_gnn', 60, 'sw_pct'):.3f} vs {C('Indel', WH, 60, 'sw_pct'):.3f}")
# P8 MethPhaser (replicate 1)
BC = [10, 20, 30, 40, 50, 60]
mr = {c: float(meth[c]['sw_pct']) / rep1('Mod', 'lp_gnn', c, 'sw_pct') for c in BC}
mh = {c: float(meth[c]['ham']) / rep1('Mod', 'lp_gnn', c, 'ham') for c in BC}
mn = {c: float(meth[c]['n50']) / rep1('Mod', 'lp_gnn', c, 'n50') for c in BC}
say('P8.meth', 'rate', ' '.join(f'{mr[c]:.2f}' for c in BC), 'ham', ' '.join(f'{mh[c]:.2f}' for c in BC),
    'n50', ' '.join(f'{mn[c]:.2f}' for c in BC),
    'lp n50', rng([rep1('Mod', 'lp_gnn', c, 'n50') / 1e6 for c in BC], f2),
    'psnv gap', rng([float(meth[c]['psnv_pct']) - rep1('Mod', 'lp_gnn', c, 'psnv_pct') for c in BC], f2))
nog = {c: rep1('Mod', LP0, c, 'sw') for c in BC}
gn = {c: rep1('Mod', 'lp_gnn', c, 'sw') for c in BC}
say('P9.gnn_share', ' '.join(f'{(nog[c] - gn[c]) / (float(meth[c]["sw"]) - gn[c]):.2f}' for c in BC),
    'gnn sw', ' '.join(str(int(gn[c])) for c in BC))
# P10 HiFi
HC5 = [10, 20, 30, 40, 50]
h = {c: S(WH, c, 'sw_pct', 'HiFi') / S('lp_gnn', c, 'sw_pct', 'HiFi') for c in HC5}
say('P10.hifi', 'ratio', ' '.join(f'{h[c]:.2f}' for c in HC5),
    'lp', f"{S('lp_gnn', 10, 'sw_pct', 'HiFi'):.3f}->{S('lp_gnn', 50, 'sw_pct', 'HiFi'):.3f}",
    'wh', f"{S(WH, 10, 'sw_pct', 'HiFi'):.3f}->{S(WH, 50, 'sw_pct', 'HiFi'):.3f}",
    'ham lp', ' '.join(f"{S('lp_gnn', c, 'ham', 'HiFi'):.2f}" for c in HC5),
    'ham wh', ' '.join(f"{S(WH, c, 'ham', 'HiFi'):.2f}" for c in HC5),
    'n50 lp kb', ' '.join(f"{S('lp_gnn', c, 'n50', 'HiFi') / 1e3:.0f}" for c in HC5),
    'n50 wh kb', ' '.join(f"{S(WH, c, 'n50', 'HiFi') / 1e3:.0f}" for c in HC5),
    'n50 diff%', rng([100 * abs(S('lp_gnn', c, 'n50', 'HiFi') / S(WH, c, 'n50', 'HiFi') - 1) for c in HC5]),
    'ont/hifi', rng([S('lp_gnn', c, 'n50') / S('lp_gnn', c, 'n50', 'HiFi') for c in HC5]))
# P15 completeness
g = [S(o, c, 'psnv_pct') - S('lp_gnn', c, 'psnv_pct') for o in (WH, HC) for c in COVS]
say('P15.psnv_gap', rng(g), 'plateau', ' '.join(f"{S(t, c, 'psnv_pct'):.2f}" for t in ('lp_gnn',) for c in (16, 20, 60)),
    'gnn loss', rng([S(LP0, c, 'psnv_pct') - S('lp_gnn', c, 'psnv_pct') for c in COVS], f2),
    'hifi gap', rng([S(WH, c, 'psnv_pct', 'HiFi') - S('lp_gnn', c, 'psnv_pct', 'HiFi') for c in HC5], f2),
    'hifi lp', ' '.join(f"{S('lp_gnn', c, 'psnv_pct', 'HiFi'):.1f}" for c in HC5),
    'indel gap', rng([C('Indel', WH, c, 'pindel_pct') - C('Indel', 'lp_gnn', c, 'pindel_pct') for c in COVS], f2))
# P23 GNN effect, SNV-only
red = {c: 100 * (1 - S('lp_gnn', c, 'sw') / S(LP0, c, 'sw')) for c in COVS}
per = [100 * (1 - float(b['sw']) / float(a['sw'])) for c in COVS[:6]
       for a in snv['ONT'][LP0][c] for b in snv['ONT']['lp_gnn'][c] if a['rep'] == b['rep']]
say('P23.gnn_red', rng(red.values()), 'per rep', rng(per),
    'psnv loss 10x', f"{S(LP0, 10, 'psnv_pct') - S('lp_gnn', 10, 'psnv_pct'):.2f}",
    '30-60', rng([S(LP0, c, 'psnv_pct') - S('lp_gnn', c, 'psnv_pct') for c in COVS[6:]], f2),
    'n50 loss 10-20', rng([100 * (1 - S('lp_gnn', c, 'n50') / S(LP0, c, 'n50')) for c in COVS[:6]]),
    '30-60', rng([100 * (1 - S('lp_gnn', c, 'n50') / S(LP0, c, 'n50')) for c in COVS[6:]]))
pooled = lambda t, k: sum(float(x[k]) for c in COVS[:6] for x in snv['ONT'][t][c])
say('P23.pooled', f"removed {100 * (1 - pooled('lp_gnn', 'sw') / pooled(LP0, 'sw')):.1f}%",
    f"cost {(pooled(LP0, 'psnv') - pooled('lp_gnn', 'psnv')) / (pooled(LP0, 'sw') - pooled('lp_gnn', 'sw')):.2f}")
hr = {c: 100 * (1 - S('lp_gnn', c, 'sw', 'HiFi') / S(LP0, c, 'sw', 'HiFi')) for c in HC5}
say('P24.hifi_gnn', 'removed', rng(hr.values()),
    'psnv loss', rng([S(LP0, c, 'psnv_pct', 'HiFi') - S('lp_gnn', c, 'psnv_pct', 'HiFi') for c in HC5], f2),
    'n50 loss', rng([100 * (1 - S('lp_gnn', c, 'n50', 'HiFi') / S(LP0, c, 'n50', 'HiFi')) for c in HC5]))
# P25/P26 co-phasing configurations
NOI = ['SNV', 'SV', 'Mod']; WI = ['Indel', 'Indel+SV', 'Mod+Indel', 'Indel+Mod+SV']
cr = lambda cfg, c: 100 * (1 - C(cfg, 'lp_gnn', c, 'sw_pct') / C(cfg, LP0, c, 'sw_pct'))
say('P25.gnn_red', 'no indel', rng([cr(k, c) for k in NOI for c in COVS]), 'indel', rng([cr(k, c) for k in WI for c in COVS]))
add = [1 - (C(k, 'lp_gnn', c, 'sw_pct') - C('SNV', 'lp_gnn', c, 'sw_pct')) / (C(k, LP0, c, 'sw_pct') - C('SNV', LP0, c, 'sw_pct'))
       for k in WI for c in COVS]
say('P25.additional_removed', rng([100 * x for x in add], lambda x: f'{x:.0f}'))
nl = lambda cfg, c: 100 * (1 - C(cfg, 'lp_gnn', c, 'n50') / C(cfg, LP0, c, 'n50'))
say('P25.n50_loss', 'indel', rng([nl(k, c) for k in WI for c in COVS], lambda x: f'{x:.0f}'),
    'no indel', rng([nl(k, c) for k in NOI for c in COVS], lambda x: f'{x:.0f}'))
m5 = {c: C('Mod', 'lp_gnn', c, 'sw_pct') / C('SNV', 'lp_gnn', c, 'sw_pct') for c in COVS}
n5 = {c: C('Mod', 'lp_gnn', c, 'n50') / C('SNV', 'lp_gnn', c, 'n50') for c in COVS}
say('P26.mod', 'rate within %', f"{100 * max(abs(x - 1) for x in m5.values()):.1f}",
    'n50 10x', f'{100 * (n5[10] - 1):.1f}', '18x+', rng([100 * (n5[c] - 1) for c in COVS if c >= 18]),
    'all', ' '.join(f'{n5[c]:.3f}' for c in COVS))
ni = {c: C('Indel', 'lp_gnn', c, 'n50') / C('SNV', 'lp_gnn', c, 'n50') for c in COVS}
ri = {c: C('Indel', 'lp_gnn', c, 'sw_pct') / C('SNV', 'lp_gnn', c, 'sw_pct') for c in COVS}
say('P26.indel', 'n50 +%', rng([100 * (x - 1) for x in ni.values()], lambda x: f'{x:.0f}'),
    'rate +%', rng([100 * (x - 1) for x in ri.values()], lambda x: f'{x:.0f}'))
n4 = {c: C('Indel+Mod+SV', 'lp_gnn', c, 'n50') / C('SNV', 'lp_gnn', c, 'n50') for c in COVS}
r4 = {c: C('Indel+Mod+SV', 'lp_gnn', c, 'sw_pct') / C('SNV', 'lp_gnn', c, 'sw_pct') for c in COVS}
longest = all(C('Indel+Mod+SV', 'lp_gnn', c, 'n50') >= max(C(k, 'lp_gnn', c, 'n50') for k in NOI + WI) for c in COVS)
say('P26.four', 'n50 +%', rng([100 * (x - 1) for x in n4.values()], lambda x: f'{x:.0f}'),
    f"60x {C('Indel+Mod+SV', 'lp_gnn', 60, 'n50') / 1e6:.2f} vs {S('lp_gnn', 60, 'n50') / 1e6:.2f}",
    'abstract +%', f"{100 * (C('Indel+Mod+SV', 'lp_gnn', 60, 'n50') / S('lp_gnn', 60, 'n50') - 1):.0f}",
    'rate +%', rng([100 * (x - 1) for x in r4.values()], lambda x: f'{x:.0f}'), 'longest everywhere', longest,
    'not longest at', [(c, max(NOI + WI, key=lambda k: C(k, 'lp_gnn', c, 'n50'))) for c in COVS if C('Indel+Mod+SV', 'lp_gnn', c, 'n50') < max(C(k, 'lp_gnn', c, 'n50') for k in NOI + WI)])
allr = [min(S(WH, c, 'sw_pct'), C('Indel', WH, c, 'sw_pct')) / C(k, 'lp_gnn', c, 'sw_pct') for k in NOI + WI for c in COVS]
say('P26.vs_wh_min', f2(min(allr)))
say('ABS.ratio', rng([S(o, c, 'sw_pct') / S('lp_gnn', c, 'sw_pct') for o in (WH, HC) for c in COVS]),
    'hifi', rng(h.values()))

# ------------------------------------------------------------------ v4.2.1 (20260924_GIAB421.txt)
v4 = defaultdict(lambda: defaultdict(list))
for line in open(os.path.join(ROOT, '20260924_GIAB421.txt')):
    if line.startswith('###') and not line.startswith('###Sample'):
        t = line[3:].rstrip('\n').split('\t')
        m = re.match(r'(.+)_(\d+)x_(\d+)\.', t[0])
        v4[m.group(1)][int(m.group(2))].append(dict(zip(COPH_COLS, [float(x) for x in t[1:]])))
V4 = lambda t, c, k: M(v4[t][c], k)
say('P11.v4_lp_sw', rng([V4('longphase_gnn', c, 'sw') for c in COVS], lambda x: f'{x:,.0f}'))
sp = {c: max(V4(t, c, 'sw_pct') for t in ('longphase_gnn', 'whatshap_v28_onlySNVs', 'hapcut2_v134')) /
      min(V4(t, c, 'sw_pct') for t in ('longphase_gnn', 'whatshap_v28_onlySNVs', 'hapcut2_v134')) for c in COVS}
say('P11.v4_spread', f'10x {sp[10]:.1f}', '30-60', rng([sp[c] for c in COVS[6:]]))
sp5 = {c: max(S(t, c, 'sw_pct') for t in ('lp_gnn', WH, HC)) / min(S(t, c, 'sw_pct') for t in ('lp_gnn', WH, HC)) for c in COVS}
say('P11.v5_spread', f'10x {sp5[10]:.1f}', '30-60', rng([sp5[c] for c in COVS[6:]]),
    'lp v5 sw', f"{S('lp_gnn', 10, 'sw'):,.0f} -> {S('lp_gnn', 60, 'sw'):,.0f}",
    'v5<v4 for lp at all', all(S('lp_gnn', c, 'sw') < V4('longphase_gnn', c, 'sw') for c in COVS))

# ------------------------------------------------------------------ held-out (notes/heldout)
def heldout(fn):
    H = defaultdict(lambda: defaultdict(list))
    for line in open(os.path.join(ROOT, 'notes', 'heldout', fn)):
        if line.startswith('###') and not line.startswith('###Sample'):
            t = line[3:].rstrip('\n').split('\t')
            m = re.match(r'(.+)_(\d+)x_(\d+)\.', t[0])
            H[m.group(1)][int(m.group(2))].append(dict(zip(COPH_COLS, [float(x) for x in t[1:]])))
    return H
H5 = heldout('heldout_v50q.txt')
HM = lambda t, c, k: M(H5[t][c], k)
for o in ('whatshap_v28_onlySNVs', 'hapcut2_v134'):
    say(f'P3.heldout_{o}', '10-20', rng([HM(o, c, 'sw_pct') / HM('longphase_gnn', c, 'sw_pct') for c in COVS[:6]]),
        '30-60', rng([HM(o, c, 'sw_pct') / HM('longphase_gnn', c, 'sw_pct') for c in COVS[6:]]))
say('P3.heldout_lp_errors_30_60', rng([HM('longphase_gnn', c, 'sw') for c in COVS[6:]], lambda x: f'{x:.0f}'))
say('P4.heldout_margin', f"10x {HM('margin_v231', 10, 'sw_pct'):.3f} vs {HM('longphase_gnn', 10, 'sw_pct'):.3f}",
    'blocks', f"{HM('longphase_gnn', 10, 'n50') / HM('margin_v231', 10, 'n50'):.1f}",
    'lower at', [c for c in COVS[:6] if HM('margin_v231', c, 'sw_pct') < HM('longphase_gnn', c, 'sw_pct')])
hred = {c: 100 * (1 - HM('longphase_gnn', c, 'sw') / HM('longphase', c, 'sw')) for c in COVS}
pool = lambda t, k: sum(x[k] for c in COVS[:6] for x in H5[t][c])
say('P24.heldout', '10-20', rng([hred[c] for c in COVS[:6]], lambda x: f'{x:.0f}'),
    '30-60', rng([hred[c] for c in COVS[6:]], lambda x: f'{x:.0f}'),
    'per run removed 30-60', rng([HM('longphase', c, 'sw') - HM('longphase_gnn', c, 'sw') for c in COVS[6:]], lambda x: f'{x:.0f}'),
    f"pooled removed {100 * (1 - pool('longphase_gnn', 'sw') / pool('longphase', 'sw')):.1f}%",
    f"cost {(pool('longphase', 'psnv') - pool('longphase_gnn', 'psnv')) / (pool('longphase', 'sw') - pool('longphase_gnn', 'sw')):.2f}")

# ------------------------------------------------------------------ issue #1 (notes/benchmark_strata)
def tsv(p): return list(csv.DictReader(open(os.path.join(ROOT, 'notes', p)), delimiter='\t'))
ov = {(r['truth'], r['run']): r for r in tsv('benchmark_strata/item4_overlap.tsv')}
sh = [100 * int(ov[('v4', f'{c}x_1')]['all3']) / int(ov[('v4', f'{c}x_1')]['LP2']) for c in COVS]
r60 = ov[('v4', '60x_1')]; r5 = ov[('v5', '60x_1')]
say('P12.coincident', f'{sh[0]:.0f}% -> {sh[-1]:.0f}%',
    '60x WH', f"{100 * int(r60['all3']) / int(r60['WH']):.0f}", 'HC', f"{100 * int(r60['all3']) / int(r60['HC2']):.0f}",
    'v5', f"{100 * int(r5['all3']) / int(r5['LP2']):.0f} {100 * int(r5['all3']) / int(r5['WH']):.0f} {100 * int(r5['all3']) / int(r5['HC2']):.0f}")
st4 = defaultdict(list)
for r in tsv('benchmark_strata/item4_strata.tsv'):
    st4[(r['tool'], int(r['coverage']), r['truth'], r['region'], r['stratum'])].append(r)
T4 = {'lp': 'longphase_gnn', 'wh': 'whatshap_v28_onlySNVs', 'hc': 'hapcut2_v134'}
def sw(t, c, tr, rg, sn, k='snv_sw'): return mean([float(x[k]) for x in st4[(T4[t], c, tr, rg, sn)]])
def rate(t, c, tr, rg, sn): return mean([float(x['snv_sw_rate%']) for x in st4[(T4[t], c, tr, rg, sn)]])
say('P12.shared_30_60', 'v4', rng([sw(t, c, 'v4', 'shared', 'any') for t in T4 for c in COVS[6:]], lambda x: f'{x:,.0f}'),
    'v5', rng([sw(t, c, 'v5', 'shared', 'any') for t in T4 for c in COVS[6:]], lambda x: f'{x:,.0f}'))
for o in ('wh', 'hc'):
    rr = {c: rate(o, c, 'v5', 'v5bed', 'any') / rate('lp', c, 'v5', 'v5bed', 'any') for c in COVS}
    sd = [rate(o, c, 'v5', 'v5bed', 'segdup') / rate('lp', c, 'v5', 'v5bed', 'segdup') for c in (10, 60)]
    nd = [rate(o, c, 'v5', 'v5bed', 'not_difficult') / rate('lp', c, 'v5', 'v5bed', 'not_difficult') for c in (10, 60)]
    nw = [rate(o, c, 'v5', 'v5only', 'any') / rate('lp', c, 'v5', 'v5only', 'any') for c in COVS]
    shd = [rate(o, c, 'v5', 'shared', 'any') / rate('lp', c, 'v5', 'shared', 'any') for c in COVS]
    say(f'P13.{o}', f'v5bed 10x {rr[10]:.1f}', '30-60', rng([rr[c] for c in COVS[6:]]), 'segdup', ' '.join(f2(x) for x in sd),
        'not_difficult', ' '.join(f2(x) for x in nd), 'new', rng(nw), 'shared', rng(shd))
say('P13.lp_new_errors', rng([sw('lp', c, 'v5', 'v5only', 'any') for c in COVS], lambda x: f'{x:.0f}'))
for t in T4:
    a = [sw(t, c, 'v5', 'neither', 'any') / sw(t, c, 'v5', 'all', 'any') for c in (10, 60)]
    say(f'P14.outside_{t}', ' '.join(f'{100 * x:.0f}%' for x in a),
        'rate', rng([rate(t, c, 'v5', 'neither', 'any') for c in COVS]))
for o in ('wh', 'hc'):
    d = [(sw(o, c, 'v5', 'neither', 'any') - sw('lp', c, 'v5', 'neither', 'any')) /
         (sw(o, c, 'v5', 'all', 'any') - sw('lp', c, 'v5', 'all', 'any')) for c in (10, 60)]
    say(f'P14.diff_share_{o}', ' '.join(f'{100 * x:.0f}%' for x in d))
ind = defaultdict(list)
for r in tsv('benchmark_strata/item3_indel.tsv'):
    ind[(r['config'], int(r['coverage']), r['region'])].append(r)
IR = lambda cfg, c: mean([float(x['indel_sw_rate%']) for x in ind[(cfg, c, 'all')]])
say('P6.indel_pairs', 'lp', f"{IR('longphase_coh_indel_gnn', 10):.3f} -> {IR('longphase_coh_indel_gnn', 60):.3f}",
    'wh', rng([IR('whatshap_v28', c) for c in COVS], f2),
    'ratio', ' '.join(f"{IR('whatshap_v28', c) / IR('longphase_coh_indel_gnn', c):.0f}" for c in COVS))
ip = [100 * (1 - IR(f'longphase_{k}_gnn', c) / IR(f'longphase_{k}', c))
      for k in ('coh_indel', 'coh_indel_sv', 'coh_indel_methyl', 'cophasing') for c in COVS]
say('P25.indel_pair_removed', rng(ip, lambda x: f'{x:.0f}'), 'table covs', rng([100 * (1 - IR(f'longphase_{k}_gnn', c) / IR(f'longphase_{k}', c))
      for k in ('coh_indel', 'coh_indel_sv', 'coh_indel_methyl', 'cophasing') for c in (10, 20, 30, 60)], lambda x: f'{x:.0f}'),
    'per cfg', ' '.join(f"{k}:" + rng([100 * (1 - IR(f'longphase_{k}_gnn', c) / IR(f'longphase_{k}', c)) for c in COVS], lambda x: f'{x:.0f}') for k in ('coh_indel', 'coh_indel_sv', 'coh_indel_methyl', 'cophasing')))
ch = [abs(IR('longphase_cophasing_gnn', c) / IR('longphase_coh_indel_gnn', c) - 1) for c in COVS]
say('P26.indel_pair_change_fourclass_vs_indel', f'{100 * max(ch):.1f}%')
IH = lambda cfg, c: mean([float(x['indel_hamming%']) for x in ind[(cfg, c, 'all')]])
say('P6.indel_ham', 'lp', f"{IH('longphase_coh_indel_gnn', 10):.1f} -> {IH('longphase_coh_indel_gnn', 60):.1f}",
    'wh', rng([IH('whatshap_v28', c) for c in COVS]))

# ------------------------------------------------------------------ issue #6/#7 (notes/unphased)
comp = {(r['coverage'], r['set']): r for r in tsv('unphased/issue6_composition.tsv')}
intv = {(r['coverage'], r['set']): r for r in tsv('unphased/issue6_intervals.tsv')}
sets = {(r['coverage'], r['set']): r for r in tsv('unphased/unphased_sets.tsv')}
calls = defaultdict(list)
for r in tsv('unphased/phased_calls_chr1_22.tsv'):
    calls[(r['tool'], int(r['coverage']))].append(r)
CV = ('10x', '30x', '60x')
n = lambda c, s: int(comp[(c, s)]['n'])
say('P18.wh_phased_lp_unphased', rng([n(c, 'lp_only') for c in CV], lambda x: f'{x:,.0f}'),
    'match%', rng([100 * int(comp[(c, 'lp_only')]['het_match']) / n(c, 'lp_only') for c in CV]),
    'lp_only_gnn share', ' '.join(f"{100 * n(c, 'lp_only_gnn') / n(c, 'lp_only'):.1f}" for c in CV))
say('P18.lp_phased_wh_unphased', rng([n(c, 'wh_only') for c in CV], lambda x: f'{x:,.0f}'),
    'absent%', rng([100 * int(comp[(c, 'wh_only')]['absent']) / n(c, 'wh_only') for c in CV]))
for s, c2 in (('lp_only', 'WhatsHap'), ('wh_only', 'LongPhase 2')):
    w_ = [100 * int(comp[(c, s)]['other_hamming_err']) / int(comp[(c, s)]['other_assessed']) for c in CV]
    say(f'P18.wrong_{s}', ' '.join(f'{x:.1f}' for x in w_), 'assessed', ' '.join(comp[(c, s)]['other_assessed'] for c in CV),
        'enrich', ' '.join(f"{float(intv[(c, s)]['enrichment']):.1f}" for c in CV))
say('P19.depth', 'dp_at_cap lp_only 60x', sets[('60x', 'lp_only')]['dp_at_cap_pct'])
say('P21.gnn_share_lp_only', rng([100 * n(c, 'lp_only_gnn') / n(c, 'lp_only') for c in CV], lambda x: f'{x:.0f}'))
for tool in ('LongPhase 2', 'WhatsHap'):
    pass
# genotype errors (phased_class: background + this tool only)
def phased(c, k, tool):
    other_only = 'lp_only' if tool == 'WhatsHap' else 'wh_only'
    return int(comp[(c, 'background')][k]) + int(comp[(c, other_only)][k])
say('P17.hom', 'lp', ' '.join(f"{phased(c, 'hom', 'LongPhase 2'):,}" for c in CV),
    'wh', ' '.join(f"{phased(c, 'hom', 'WhatsHap'):,}" for c in CV),
    'ratio', ' '.join(f"{phased(c, 'hom', 'WhatsHap') / phased(c, 'hom', 'LongPhase 2'):.2f}" for c in CV))
say('P17.other', 'ratio other allele', ' '.join(f"{phased(c, 'het_other_allele', 'WhatsHap') / phased(c, 'het_other_allele', 'LongPhase 2'):.2f}" for c in CV),
    'absent', ' '.join(f"{phased(c, 'absent', 'WhatsHap') / phased(c, 'absent', 'LongPhase 2'):.2f}" for c in CV),
    '60x absent', f"{phased('60x', 'absent', 'WhatsHap'):,} {phased('60x', 'absent', 'LongPhase 2'):,}")
# precision (Phased_calls) and F1
prec = {}
for tool, key in (('LongPhase 2', 'lp_gnn'), ('WhatsHap', WH)):
    for c in COVS:
        for r in calls[(tool, c)]:
            ps = [x for x in snv['ONT'][key][c] if x['rep'] == int(r['replicate'])][0]
            pr = 100 * float(ps['psnv']) / int(r['phased_het_snv_calls_chr1_22'])
            rc = float(ps['psnv_pct'])
            prec[(tool, c, int(r['replicate']))] = (pr, 2 * pr * rc / (pr + rc))
pm = lambda t, c, i: mean([v[i] for (tt, cc, _), v in prec.items() if tt == t and cc == c])
say('P16.precision', 'lp', f"{pm('LongPhase 2', 10, 0):.1f} -> {pm('LongPhase 2', 60, 0):.1f}",
    'wh', f"{pm('WhatsHap', 10, 0):.1f} -> {pm('WhatsHap', 60, 0):.1f}",
    'diff', ' '.join(f"{pm('LongPhase 2', c, 0) - pm('WhatsHap', c, 0):.2f}" for c in COVS),
    'lp higher every rep', all(prec[('LongPhase 2', c, r)][0] > prec[('WhatsHap', c, r)][0] for (t, c, r) in prec if t == 'LongPhase 2'))
say('P16.f1', 'diff', ' '.join(f"{pm('LongPhase 2', c, 1) - pm('WhatsHap', c, 1):.2f}" for c in COVS),
    'lp', rng([pm('LongPhase 2', c, 1) for c in COVS]), 'wh', rng([pm('WhatsHap', c, 1) for c in COVS]),
    'lp higher every rep', all(prec[('LongPhase 2', c, r)][1] > prec[('WhatsHap', c, r)][1] for (t, c, r) in prec if t == 'LongPhase 2'))

# ------------------------------------------------------------------ T2T (unphase_validation_results.txt)
txt = open(os.path.join(ROOT, 'unphase_validation_results.txt')).read()
rm = re.search(r'removed\s+(\d+) /\s+(\d+)', txt); bg = re.search(r'background\s+(\d+) /\s+(\d+)', txt)
cls = {k: int(v) for k, v in re.findall(r'^(variant|hom_wt|unassessed)\s+(\d+)', txt, re.M)}
odds = re.search(r'odds ratio ([\d.]+)x', txt).group(1)
au = [m for m in re.finditer(r'^(chr\w+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)$', txt, re.M)
      if m.group(1) not in ('chrX', 'chrY')]
bo, bn = sum(int(m.group(2)) for m in au), sum(int(m.group(3)) for m in au)
ro, rn = sum(int(m.group(5)) for m in au), sum(int(m.group(6)) for m in au)
pa = (rn - ro) / rn; pb = (bn - bo) / bn
say('P22.t2t', f'removed {int(rm.group(2)):,}', f'in 1:1 {100 * int(rm.group(1)) / int(rm.group(2)):.1f}%',
    f'bg {100 * int(bg.group(1)) / int(bg.group(2)):.1f}%', f'odds {odds}',
    f'auto {100 * pa:.1f}% vs {100 * pb:.1f}% odds {((1 - pa) / pa) / ((1 - pb) / pb) if False else (ro / (rn - ro)) / (bo / (bn - bo)):.0f}',
    f"within {cls['variant'] + cls['hom_wt']:,} no variant {cls['hom_wt']:,} ({100 * cls['hom_wt'] / (cls['variant'] + cls['hom_wt']):.0f}%)",
    'every autosome enriched', all(float(m.group(8)) > 1 for m in au))
