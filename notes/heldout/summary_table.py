# One row per coverage: held-out (chr17/21/22) SNV switch error rate (%) per tool,
# mean over replicates, against v5.0q and v4.2.1, plus ratios and the GNN reduction.
import statistics as st, re
def load(p):
    d = {}
    for l in open(p):
        if not l.startswith('###') or 'Sample' in l: continue
        f = l.rstrip('\n').split('\t')
        m = re.match(r'###(.+)_(\d+)x_(\d+)', f[0])
        d.setdefault(m.group(1), {}).setdefault(int(m.group(2)), []).append((int(f[5]), float(f[6]), int(f[1])))
    return d
G = ['longphase_gnn', 'longphase', 'whatshap_v28_onlySNVs', 'hapcut2_v134', 'margin_v231', 'ralphi']
out = open('heldout_summary.tsv', 'w')
out.write('truth\tcoverage\tn\t' + '\t'.join(f'{g}_SW%' for g in G) + '\tWhatsHap/LP2\tHapCUT2/LP2\tGNN_reduction_%\tGNN_cost_withheld_SNV_per_removed_SW\n')
for truth, f in (('v5.0q', 'heldout_v50q.txt'), ('v4.2.1', 'heldout_GIAB421.txt')):
    D = load(f)
    for c in (10, 12, 14, 16, 18, 20, 30, 40, 50, 60):
        m = {g: st.mean(x[1] for x in D[g][c]) if c in D.get(g, {}) else None for g in G}
        sw = {g: st.mean(x[0] for x in D[g][c]) for g in ('longphase_gnn', 'longphase')}
        ph = {g: st.mean(x[2] for x in D[g][c]) for g in ('longphase_gnn', 'longphase')}
        out.write('\t'.join([truth, f'{c}x', str(len(D['longphase_gnn'][c]))] + [f'{m[g]:.4f}' if m[g] is not None else '' for g in G]
                  + [f"{m['whatshap_v28_onlySNVs'] / m['longphase_gnn']:.2f}", f"{m['hapcut2_v134'] / m['longphase_gnn']:.2f}",
                     f"{100 * (1 - sw['longphase_gnn'] / sw['longphase']):.1f}",
                     f"{(ph['longphase'] - ph['longphase_gnn']) / (sw['longphase'] - sw['longphase_gnn']):.1f}" if sw['longphase'] > sw['longphase_gnn'] else '']) + '\n')
out.close(); print(open('heldout_summary.tsv').read())
