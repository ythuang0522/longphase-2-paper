"""Issue #6 Part B: one row per site of the four unphased-SNV sets
(lp_graph, lp_gnn, both, wh_only) at 10x, 30x and 60x, replicate 1.

Definitions are those of issue6.py (sets, truth class, compare emulation) and
run_coverage.sh (switch-error intervals, Fig. 3e). Region BEDs are 0-based
half-open; a site at 1-based POS is inside when start < POS <= end.

    python3 issue6_sites.py OUT.tsv.gz
"""
import bisect, gzip, sys
from collections import defaultdict
sys.argv, out_path = sys.argv[:1] + ['.'], sys.argv[1]
src = open('/ssd/longphase_process/unphased_sets/issue6.py').read()
exec(src.split('truth_het, bypos = read_truth()')[0])      # functions and paths of issue6.py

V5BED = '/disk/software/longphase-2-paper/data/truth/HG002_GRCh38_v5.0q_smvar.benchmark.bed'
SEGDUP = '/disk/software/longphase-2-paper/data/truth/GRCh38_segdups.bed.gz'
DIPBED = '/home/twolinin/Downloads/GRCh38_HG2-T2TQ100-V1.1_dipcall-z2k.dip.bed'


def load_bed(path):
    iv = defaultdict(list)
    op = gzip.open if path.endswith('.gz') else open
    for l in op(path, 'rt'):
        if l.startswith(('#', 'track', 'browser')):
            continue
        f = l.split('\t')
        iv[f[0]].append((int(f[1]), int(f[2])))
    idx = {}
    for c, L in iv.items():
        L.sort()
        S = [s for s, _ in L]; M = []
        m = -1
        for _, e in L:
            m = max(m, e); M.append(m)
        idx[c] = (S, M)
    return idx


def hit(idx, c, p):
    if c not in idx:
        return 0
    S, M = idx[c]
    i = bisect.bisect_left(S, p) - 1         # last interval with start < p
    return 1 if i >= 0 and M[i] >= p else 0


def swidx(path):
    iv = read_swbed(path)
    idx = {}
    for c, L in iv.items():
        S = [s for s, _ in L]; M = []; m = -1
        for _, e in L:
            m = max(m, e); M.append(m)
        idx[c] = (S, M)
    return idx


truth_het, bypos = read_truth()
v5, segdup, dip = load_bed(V5BED), load_bed(SEGDUP), load_bed(DIPBED)
out = gzip.open(out_path, 'wt')
out.write('coverage\tset\tchrom\tpos\tref\talt\tdepth\ttruth\tin_v5_bed\tin_segdup\tin_dipcall_1to1'
          '\tin_other_sw_interval\twh_wrong\twh_sw_endpoint\n')
for cov in (10, 30, 60):
    lp_v, lp_c, dp = read_call(f'{R}/longphase_gnn/longphase_gnn_{cov}x_1.vcf', info=True)
    pre_v, _, _ = read_call(f'{R}/longphase/longphase_{cov}x_1.vcf')
    wh_v, wh_c, _ = read_call(f'{R}/whatshap_v2.8/only/whatshap_v28_onlySNVs_{cov}x_1.vcf')
    alt = {(k[0], k[1]): (k[2], k[3]) for k in lp_c if len(k[2]) == 1 and len(k[3]) == 1}
    lp_u = {s for s, p in lp_v.items() if not p}
    wh_u = {s for s, p in wh_v.items() if not p}
    lp_only = {s for s in lp_u if wh_v.get(s)}
    wh_only = {s for s in wh_u if lp_v.get(s)}
    both = lp_u & wh_u
    removed = {s for s, p in pre_v.items() if p} & lp_u
    _, wh_ham, wh_end, _, _, _ = emulate_compare(truth_het, wh_c)
    sw = {'wh': swidx(f'{SWDIR}/whatshap_v28_onlySNVs_{cov}x_1.vcf.sw.bed'),
          'lp': swidx(f'{SWDIR}/longphase_gnn_{cov}x_1.vcf.sw.bed')}
    n = 0
    for name, S, other in (('lp_graph', lp_only - removed, 'wh'), ('lp_gnn', lp_only & removed, 'wh'),
                           ('both', both, None), ('wh_only', wh_only, 'lp')):
        for c, p in sorted(S, key=lambda s: (s[0], s[1])):
            ref, a = alt[(c, p)]
            t = classify((c, p), ref, a, bypos, truth_het)
            osw = 'NA' if other is None else hit(sw[other], c, p)
            if name.startswith('lp_') and t == 'het_match':
                ww = int((c, p) in wh_ham); we = int((c, p) in wh_end)
            else:
                ww = we = 'NA'
            out.write(f'{cov}\t{name}\t{c}\t{p}\t{ref}\t{a}\t{dp.get((c, p), "NA")}\t{t}\t{hit(v5, c, p)}'
                      f'\t{hit(segdup, c, p)}\t{hit(dip, c, p)}\t{osw}\t{ww}\t{we}\n')
            n += 1
    print(f'{cov}x: {n} rows', flush=True)
out.close()
