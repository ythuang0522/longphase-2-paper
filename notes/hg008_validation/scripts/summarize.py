#!/usr/bin/env python3
"""summarize.py: per-run table of the HG008 issue #11 runs (score_all.sh outputs) -> score/hg008_runs.tsv,
score/hg008_gnn_effect.tsv, score/hg008_summary.tsv and score/hg008_fig.{pdf,png}.

Per run (truth = truth/HG008N_v6.3_truth.vcf, PS = truth block):
  from longphase compare v2.1 (genome line '###'): phased SNVs and %, SNV switch errors and rate, block-wise Hamming %,
  query blocks, block N50, block sum;
  from score_phase.py (region all, stratum any): assessed SNV pairs, SNV switch errors, phased SNVs (cross-check: must
  equal compare), Hamming numerator / denominator;
  denominator: truth heterozygous biallelic SNVs (0|1, 1|0) in the truth VCF.
GNN effect (LongPhase 2 with vs without GNN, same input): change in switch errors, assessed pairs, phased benchmark SNVs,
het SNV calls withheld (phased without GNN, unphased with GNN; all calls and benchmark-matched), blocks and N50.
"""
import gzip, os, sys, re
from collections import defaultdict
os.chdir('/disk/research/HG008')
TRUTH = 'truth/HG008N_v6.3_truth.vcf'
CHR = {f'chr{i}' for i in range(1, 23)}
RUNS = ['10x_1', '10x_2', '10x_3', '20x_1', '20x_2', '20x_3', '30x_1']
TOOLS = [('lp_gnn', 'LongPhase 2 (GNN)'), ('lp_nognn', 'LongPhase 2 --disableGNN'), ('wh', 'WhatsHap 2.8'), ('hapcut2', 'HapCUT2 1.3.4')]


def truth_snvs():
    s = set()
    for l in open(TRUTH):
        if l[0] == '#': continue
        x = l.split('\t', 10)
        if x[0] in CHR and len(x[3]) == 1 and len(x[4]) == 1 and x[9][:3] in ('0|1', '1|0'): s.add((x[0], int(x[1]), x[3], x[4]))
    return s


def compare(prefix):
    for l in open(prefix + '.tsv'):
        if l.startswith('###') and not l.startswith('###Sample'):
            v = l[3:].rstrip('\n').split('\t')
            return dict(phased_snv=int(v[1]), phased_snv_pct=float(v[2]), snv_sw=int(v[5]), snv_sw_pct=float(v[6]),
                        hamming_pct=float(v[7]), blocks=int(v[8]), n50=int(v[9]), block_sum=int(v[10]))
    raise ValueError(prefix)


def sp(prefix):
    L = open(prefix + '.sp.tsv').read().split('\n'); h = L[0].split('\t'); ham = dict(zip(h[0::2], h[1::2]))
    cols = L[1].split('\t')
    for l in L[2:]:
        v = l.split('\t')
        if v[:2] == ['all', 'any']:
            d = dict(zip(cols, v)); break
    return dict(sp_phased_snv=int(d['phased_snv']), snv_pairs=int(d['snv_pairs']), sp_snv_sw=int(d['snv_sw']),
                ham=int(ham['#ham_all']), ham_n=int(ham['ham_n']))


def het_snv_calls(vcf):
    """{key: phased?} for heterozygous biallelic SNV calls on chr1-22 of a phaser output."""
    out = {}; op = gzip.open if vcf.endswith('.gz') else open
    for l in op(vcf, 'rt'):
        if l[0] == '#': continue
        x = l.rstrip('\n').split('\t')
        if x[0] not in CHR or len(x[3]) != 1 or len(x[4]) != 1: continue
        fm = x[8].split(':'); gt = x[9].split(':')[fm.index('GT')] if 'GT' in fm else '.'
        if gt in ('0|1', '1|0'): out[(x[0], int(x[1]), x[3], x[4])] = True
        elif gt in ('0/1', '1/0'): out[(x[0], int(x[1]), x[3], x[4])] = False
    return out


def qfile(t, r):
    return f'phase/hapcut2_{r}.phased.VCF' if t == 'hapcut2' else f'phase/{t}_{r}.vcf'


TS = truth_snvs(); NT = len(TS)
rows = []; bad = []
for r in RUNS:
    for t, name in TOOLS:
        p = f'score/sw_{t}_{r}'
        if not os.path.exists(p + '.tsv'): bad.append(p); continue
        c = compare(p); s = sp(p)
        if (c['phased_snv'], c['snv_sw']) != (s['sp_phased_snv'], s['sp_snv_sw']): bad.append(f'{p}: compare != score_phase')
        rows.append(dict(run=r, coverage=r.split('_')[0], seed=r.split('_')[1], tool=t, tool_name=name, truth_het_snv=NT,
                         completeness_pct=100 * c['phased_snv'] / NT, ser_pct=100 * c['snv_sw'] / max(s['snv_pairs'], 1), **c, **s))
cols = ['run', 'coverage', 'seed', 'tool', 'tool_name', 'snv_sw', 'snv_pairs', 'ser_pct', 'snv_sw_pct', 'phased_snv',
        'truth_het_snv', 'completeness_pct', 'phased_snv_pct', 'ham', 'ham_n', 'hamming_pct', 'blocks', 'n50', 'block_sum']
os.makedirs('score', exist_ok=True)
with open('score/hg008_runs.tsv', 'w') as o:
    o.write('\t'.join(cols) + '\n')
    for d in rows: o.write('\t'.join(f'{d[k]:.5f}' if isinstance(d[k], float) else str(d[k]) for k in cols) + '\n')
# GNN effect
R = {(d['run'], d['tool']): d for d in rows}
with open('score/hg008_gnn_effect.tsv', 'w') as o:
    o.write('run\tsw_nognn\tsw_gnn\tdelta_sw\tdelta_sw_pct\tpairs_nognn\tpairs_gnn\tser_nognn\tser_gnn\tphased_bench_nognn\t'
            'phased_bench_gnn\twithheld_calls\twithheld_bench\tblocks_nognn\tblocks_gnn\tn50_nognn\tn50_gnn\tdelta_n50_pct\n')
    for r in RUNS:
        a, b = R.get((r, 'lp_nognn')), R.get((r, 'lp_gnn'))
        if not a or not b: continue
        A = het_snv_calls(qfile('lp_nognn', r)); B = het_snv_calls(qfile('lp_gnn', r))
        wh = [k for k, v in A.items() if v and not B.get(k, False)]
        o.write('\t'.join(map(str, [r, a['snv_sw'], b['snv_sw'], b['snv_sw'] - a['snv_sw'],
            f"{100 * (b['snv_sw'] - a['snv_sw']) / a['snv_sw']:.2f}", a['snv_pairs'], b['snv_pairs'], f"{a['ser_pct']:.4f}",
            f"{b['ser_pct']:.4f}", a['phased_snv'], b['phased_snv'], len(wh), sum(k in TS for k in wh), a['blocks'], b['blocks'],
            a['n50'], b['n50'], f"{100 * (b['n50'] - a['n50']) / a['n50']:.2f}"])) + '\n')
# summary per coverage x tool (mean over seeds, and min-max)
with open('score/hg008_summary.tsv', 'w') as o:
    o.write('coverage\ttool\tn_seeds\tser_pct_mean\tser_pct_min\tser_pct_max\tcompleteness_pct_mean\thamming_pct_mean\tn50_mean\tblocks_mean\n')
    for cv in ('10x', '20x', '30x'):
        for t, _ in TOOLS:
            D = [d for d in rows if d['coverage'] == cv and d['tool'] == t]
            if not D: continue
            m = lambda k: sum(d[k] for d in D) / len(D)
            o.write(f"{cv}\t{t}\t{len(D)}\t{m('ser_pct'):.4f}\t{min(d['ser_pct'] for d in D):.4f}\t{max(d['ser_pct'] for d in D):.4f}\t"
                    f"{m('completeness_pct'):.3f}\t{m('hamming_pct'):.3f}\t{m('n50'):.0f}\t{m('blocks'):.0f}\n")
# figure: switch error rate, completeness, block N50 against coverage; every seed a point, mean a line (skipped without matplotlib)
try:
    import matplotlib
except ImportError:
    matplotlib = None; print('matplotlib missing: no figure')
if matplotlib:
    matplotlib.use('Agg'); import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 6})
    COL = {'lp_gnn': '#1687C9', 'lp_nognn': '#7FB8DE', 'wh': '#DC2B23', 'hapcut2': '#555555'}
    fig, ax = plt.subplots(1, 3, figsize=(183 / 25.4, 2.0), constrained_layout=True)
    for k, (key, lab) in enumerate((('ser_pct', 'SNV switch error rate (%)'), ('completeness_pct', 'Benchmark het. SNVs phased (%)'),
                                    ('n50', 'Block N50 (Mb)'))):
        for t, name in TOOLS:
            D = [d for d in rows if d['tool'] == t]
            if not D: continue
            x = [int(d['coverage'][:-1]) for d in D]; y = [d[key] / (1e6 if key == 'n50' else 1) for d in D]
            ax[k].scatter(x, y, s=6, color=COL[t], alpha=0.7, lw=0)
            xs = sorted(set(x)); ax[k].plot(xs, [sum(v for u, v in zip(x, y) if u == c) / x.count(c) for c in xs], color=COL[t], lw=1,
                                            label=name, ls='--' if t == 'lp_nognn' else '-')
        ax[k].set_xlabel('Coverage (×)'); ax[k].set_ylabel(lab); ax[k].set_xticks([10, 20, 30])
        ax[k].text(-0.22, 1.02, 'abc'[k], transform=ax[k].transAxes, fontsize=8, fontweight='bold')
    ax[0].legend(frameon=False, fontsize=5)
    fig.suptitle('HG008-N-P nanopore, chr1–22, HG008-N v6.3 assembly-derived phase (seeds as points)', fontsize=6)
    fig.savefig('score/hg008_fig.pdf'); fig.savefig('score/hg008_fig.png', dpi=300)
print('runs', len(rows), 'truth het SNVs', NT, 'problems', bad)
