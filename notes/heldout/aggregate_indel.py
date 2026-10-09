"""Held-out chr17/21/22 indel phase accuracy (issue #2), from out/<run>.tsv of
score_heldout.py. Writes heldout_indel.tsv (one row per run, the columns of
benchmark_strata/item3_indel.tsv, region = all) and prints, per configuration
and coverage, rates pooled over the replicates (sum of errors / sum of pairs)
next to the same pooled genome-wide rates from item3_indel.tsv."""
import glob, os, re, sys
from collections import defaultdict

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
GW = '/ssd/longphase_process/benchmark_strata/item3_indel.tsv'
CFG = ['longphase_coh_indel', 'longphase_coh_indel_gnn', 'longphase_coh_indel_sv',
       'longphase_coh_indel_sv_gnn', 'longphase_coh_indel_methyl', 'longphase_coh_indel_methyl_gnn',
       'longphase_cophasing', 'longphase_cophasing_gnn', 'whatshap_v28']
COVS = [10, 12, 14, 16, 18, 20, 30, 40, 50, 60]
KEYS = ['phased_snv', 'phased_indel', 'snv_pairs', 'snv_sw', 'all_pairs', 'all_sw',
        'indel_pairs', 'indel_sw', 'indel_hamming', 'indels_in_blocks']

def pct(a, b):
    return 100 * a / max(1, b)

held = {}
for f in glob.glob(f'{OUT}/*.tsv'):
    if f.endswith('.sw.tsv'):
        continue
    m = re.match(r'(.+)_(\d+)x_(\d+)$', os.path.basename(f)[:-4])
    cfg, cov, rep = m.group(1), int(m.group(2)), int(m.group(3))
    lines = open(f).read().split('\n')
    h = lines[0].split('\t')
    ham = dict(zip(h[0::2], h[1::2]))
    hdr = lines[1].split('\t')
    d = next(dict(zip(hdr, l.split('\t'))) for l in lines[2:] if l.startswith('all\tany\t'))
    d['indel_hamming'], d['indels_in_blocks'] = ham['ham_indel'], ham['ham_n_indel']
    held[(cfg, cov, rep)] = {k: int(d[k]) for k in KEYS}

with open('heldout_indel.tsv', 'w') as f:
    f.write('config\tcoverage\treplicate\tregion\t' + '\t'.join(KEYS[:8]) +
            '\tindel_sw_rate%\tsnv_indel_sw_rate%\tindel_hamming\tindels_in_blocks\tindel_hamming%\tsnv_sw_rate%\n')
    for (cfg, cov, rep), d in sorted(held.items(), key=lambda x: (CFG.index(x[0][0]), x[0][1], x[0][2])):
        f.write(f"{cfg}\t{cov}\t{rep}\tchr17_21_22\t" + '\t'.join(str(d[k]) for k in KEYS[:8]) +
                f"\t{pct(d['indel_sw'], d['indel_pairs']):.4f}\t{pct(d['all_sw'], d['all_pairs']):.4f}"
                f"\t{d['indel_hamming']}\t{d['indels_in_blocks']}\t{pct(d['indel_hamming'], d['indels_in_blocks']):.4f}"
                f"\t{pct(d['snv_sw'], d['snv_pairs']):.4f}\n")

gw = defaultdict(lambda: defaultdict(int))
hdr = None
for l in open(GW):
    l = l.rstrip('\n').split('\t')
    if hdr is None:
        hdr = l; continue
    r = dict(zip(hdr, l))
    if r['region'] != 'all':
        continue
    for k in KEYS:
        gw[(r['config'], int(r['coverage']))][k] += int(r[k])
hp = defaultdict(lambda: defaultdict(int))
n = defaultdict(int)
for (cfg, cov, rep), d in held.items():
    n[(cfg, cov)] += 1
    for k in KEYS:
        hp[(cfg, cov)][k] += d[k]

print('Held-out chr17/21/22 vs genome-wide (v5.0q, no BED); rates pooled over replicates')
print('config\tcov\truns\tphased_indel/run\tindel_sw/run\tindel_sw%\tsnv+indel_sw%\tindel_ham%'
      '\tGW_indel_sw%\tGW_snv+indel_sw%\tGW_indel_ham%')
for cfg in CFG:
    for cov in COVS:
        a, g, k = hp[(cfg, cov)], gw[(cfg, cov)], n[(cfg, cov)]
        if not k:
            continue
        print(f"{cfg}\t{cov}\t{k}\t{a['phased_indel'] / k:.0f}\t{a['indel_sw'] / k:.1f}"
              f"\t{pct(a['indel_sw'], a['indel_pairs']):.3f}\t{pct(a['all_sw'], a['all_pairs']):.3f}"
              f"\t{pct(a['indel_hamming'], a['indels_in_blocks']):.2f}"
              f"\t{pct(g['indel_sw'], g['indel_pairs']):.3f}\t{pct(g['all_sw'], g['all_pairs']):.3f}"
              f"\t{pct(g['indel_hamming'], g['indels_in_blocks']):.2f}")

def pool(src, cfg, covs):
    t = defaultdict(int)
    for c in covs:
        for k in KEYS:
            t[k] += src[(cfg, c)][k]
    return t
print('\nGNN reduction of indel switch errors (pairs with an indel), pooled')
print('pair\tcovs\theld-out\tgenome-wide')
for base in ['longphase_coh_indel', 'longphase_coh_indel_sv', 'longphase_coh_indel_methyl', 'longphase_cophasing']:
    for name, covs in (('10-20x', COVS[:6]), ('30-60x', COVS[6:])):
        r = [100 * (1 - pool(s, base + '_gnn', covs)['indel_sw'] / max(1, pool(s, base, covs)['indel_sw'])) for s in (hp, gw)]
        print(f"{base}\t{name}\t{r[0]:.1f}%\t{r[1]:.1f}%")
print('\nWhatsHap / LP2 four-class GNN, indel switch error rate')
for cov in COVS:
    r = []
    for s in (hp, gw):
        w, l = s[('whatshap_v28', cov)], s[('longphase_cophasing_gnn', cov)]
        r.append(pct(w['indel_sw'], w['indel_pairs']) / max(1e-9, pct(l['indel_sw'], l['indel_pairs'])))
    print(f"{cov}x\theld-out {r[0]:.1f}\tgenome-wide {r[1]:.1f}")
