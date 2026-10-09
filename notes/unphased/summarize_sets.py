"""Per-set summary of the heterozygous SNVs given up by LongPhase 2 and by
WhatsHap (replicate 1, 10x/30x/60x), with the definitions of the 2026-09-27
scripts (scripts/):

  sets         run_coverage.sh: het SNVs (single-base REF/ALT, GT 0/1) of the
               LongPhase 2 (GNN) and WhatsHap --only-snvs VCFs; lp_only =
               unphased by LongPhase, phased by WhatsHap, split into
               lp_only_gnn (phased before GNN correction, unphased after) and
               lp_only_phase (the rest); wh_only the reverse; both = unphased
               by both; background = het SNVs of the LongPhase VCF in none of
               the give-up sets (all of them, not a 100,000-site sample)
  depth        FORMAT/DP of the LongPhase VCF; quartiles as giveup_detail.sh
               (sorted a[int(n*q)]); at_cap = DP >= 124, the last 2x bin of
               the UnphaseVenn3 histograms
  PE           INFO/PE of the LongPhase VCF, over the sites that carry it
  enrichment   run_coverage.sh: share of the set inside the other tool's
               switch-error intervals (compare --sw-bed against v5.0q,
               start < pos <= end), divided by the same share for all het
               SNVs that tool phased

    python3 summarize_sets.py OUT_DIR > unphased_sets.tsv
"""
import bisect, os, subprocess, sys, tempfile
from collections import defaultdict
R = '/disk/research'
TRUTH = '/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.vcf.gz'
LP = '/disk/software/longphase_v2.1_release/longphase_linux-x64'
CAP = 124

def read(vcf, info=False):
    het = {}
    for l in open(vcf):
        if l[0] == '#':
            continue
        f = l.split('\t', 10)
        if len(f[3]) != 1 or len(f[4]) != 1:
            continue
        k = f[8].split(':'); v = f[9].rstrip('\n').split(':')
        g = v[0].replace('|', '/')
        if g not in ('0/1', '1/0'):
            continue
        dp = pe = None
        if info:
            d = dict(zip(k, v))
            if 'DP' in d:
                dp = int(d['DP'])
            for x in f[7].split(';'):
                if x.startswith('PE='):
                    pe = float(x[3:])
        het[(f[0], int(f[1]))] = ('|' in v[0], dp, pe)
    return het

def swbed(vcf, d):
    b = os.path.join(d, os.path.basename(vcf) + '.sw.bed')
    subprocess.run([LP, 'compare', TRUTH, vcf, '--ignore-sample-name', '--sw-bed', b,
                    '-o', b[:-4], '-t', '8'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    iv = defaultdict(list)
    for l in open(b):
        if l.startswith(('#', 'track')):
            continue
        c, s, e = l.split('\t')[:3]
        iv[c].append((int(s), int(e)))
    return iv

def inside(iv, sites):
    # run_coverage.sh: hit when any interval has start < pos <= end
    idx = {}
    for c, L in iv.items():
        L.sort(); idx[c] = (L, [s for s, _ in L], [max(e for _, e in L[:i + 1]) for i in range(len(L))])
    h = 0
    for c, p in sites:
        if c not in idx:
            continue
        L, S, M = idx[c]
        i = bisect.bisect_left(S, p) - 1      # last interval with start < p
        if i >= 0 and M[i] >= p:
            h += 1
    return h

def q(a):
    a = sorted(a); n = len(a)
    return (a[int(n * .25)], a[int(n * .5)], a[int(n * .75)]) if n else ('NA',) * 3

print('coverage\tset\tn\tdp_q1\tdp_median\tdp_q3\tdp_at_cap_pct\tpe_sites\tpe_zero_pct\tpe_ge_0.8_pct'
      '\tother_tool\tin_other_sw_pct\tother_tool_background_pct\tenrichment')
tmp = tempfile.mkdtemp(dir=sys.argv[1] if len(sys.argv) > 1 else '.')
for c in (10, 30, 60):
    pre = read(f'{R}/longphase/longphase_{c}x_1.vcf')
    gnn = read(f'{R}/longphase_gnn/longphase_gnn_{c}x_1.vcf', info=True)
    wh = read(f'{R}/whatshap_v2.8/only/whatshap_v28_onlySNVs_{c}x_1.vcf')
    lp_u = {s for s, x in gnn.items() if not x[0]}; lp_p = {s for s, x in gnn.items() if x[0]}
    wh_u = {s for s, x in wh.items() if not x[0]}; wh_p = {s for s, x in wh.items() if x[0]}
    both = lp_u & wh_u; lp_only = lp_u & wh_p; wh_only = wh_u & lp_p
    removed = {s for s, x in pre.items() if x[0]} & lp_u
    lp_gnn = lp_only & removed; lp_phase = lp_only - removed
    bg = set(gnn) - lp_only - wh_only - both
    sw_wh = swbed(f'{R}/whatshap_v2.8/only/whatshap_v28_onlySNVs_{c}x_1.vcf', tmp)
    sw_lp = swbed(f'{R}/longphase_gnn/longphase_gnn_{c}x_1.vcf', tmp)
    bg_wh = 100 * inside(sw_wh, wh_p) / len(wh_p); bg_lp = 100 * inside(sw_lp, lp_p) / len(lp_p)
    for name, S, other, sw, b in (('lp_only_phase', lp_phase, 'WhatsHap', sw_wh, bg_wh),
                                  ('lp_only_gnn', lp_gnn, 'WhatsHap', sw_wh, bg_wh),
                                  ('lp_only', lp_only, 'WhatsHap', sw_wh, bg_wh),
                                  ('wh_only', wh_only, 'LongPhase 2', sw_lp, bg_lp),
                                  ('both', both, '', None, None),
                                  ('background', bg, '', None, None)):
        dps = [gnn[s][1] for s in S if gnn[s][1] is not None]
        pes = [gnn[s][2] for s in S if gnn[s][2] is not None]
        d = q(dps)
        cap = 100 * sum(x >= CAP for x in dps) / len(dps)
        pz = f'{100 * sum(x == 0 for x in pes) / len(pes):.1f}' if pes else 'NA'
        ph = f'{100 * sum(x >= 0.8 for x in pes) / len(pes):.1f}' if pes else 'NA'
        if sw is not None:
            x = 100 * inside(sw, S) / len(S)
            cross = f'{other}\t{x:.2f}\t{b:.2f}\t{x / b:.1f}'
        else:
            cross = '\tNA\tNA\tNA'
        print(f'{c}x\t{name}\t{len(S)}\t{d[0]}\t{d[1]}\t{d[2]}\t{cap:.1f}\t{len(pes)}\t{pz}\t{ph}\t{cross}', flush=True)
