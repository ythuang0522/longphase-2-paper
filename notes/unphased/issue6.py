"""Issue #6: benchmark composition of the unphased-SNV sets, the other tool's
accuracy at their benchmark sites, per-set depth histograms, and the
switch-error-interval definition check.

Same runs and sets as run_coverage.sh (UnphaseVenn3.jsx): HG002 ONT, SNV-only,
replicate 1 at 10x/30x/60x, LongPhase 2 with GNN against WhatsHap 2.8
--only-snvs. Truth: v5.0q chr1-22 (the file of the manuscript tables), no BED.

    python3 issue6.py OUTDIR      (writes OUTDIR/issue6_*.tsv)
"""
import bisect, glob, os, sys
from collections import defaultdict, Counter

R = '/disk/research'
TRUTH = '/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf'
SWDIR = glob.glob('/ssd/longphase_process/unphased_sets/out/tmp*')[0]  # --sw-bed of summarize_sets.py
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
XY = ('chrX', 'chrY')
BIN, NB = 2, 63            # run_coverage.sh histograms: 2x bins, last bin = DP >= 124


def gt_alleles(s):
    s = s.split(':')[0]
    sep = '|' if '|' in s else '/'
    a = s.split(sep)
    return a, sep == '|'


def read_call(vcf, info=False):
    """Two views of one output VCF.
    venn: (chrom, pos) -> phased, for single-base REF/ALT GT 0/1 (run_coverage.sh het()).
    cmp:  (chrom, pos, ref, alt1) -> (h0, ps) for every REF/first-ALT heterozygous
          record, phased or not, as CompareProcess.cpp reads a VCF (h0 = -1 unphased).
    dp:   (chrom, pos) -> FORMAT/DP (info=True only)."""
    venn, cmp_, dp = {}, {}, {}
    for l in open(vcf):
        if l[0] == '#':
            continue
        f = l.rstrip('\n').split('\t')
        c, p, ref, alts = f[0], int(f[1]), f[3], f[4].split(',')
        a, ph = gt_alleles(f[9])
        if len(a) != 2 or '.' in a:
            continue
        a0, a1 = int(a[0]), int(a[1])
        if {a0, a1} == {0, 1}:
            ps = 0
            if ph:
                k = f[8].split(':'); v = f[9].split(':')
                d = dict(zip(k, v))
                ps = int(d['PS']) if d.get('PS', '.') not in ('.', '0') else 1
            cmp_[(c, p, ref, alts[0])] = (a0 if ph else -1, ps, len(alts) > 1)
            if len(ref) == 1 and len(f[4]) == 1:
                venn[(c, p)] = ph
                if info:
                    k = f[8].split(':'); v = f[9].split(':')
                    d = dict(zip(k, v))
                    if 'DP' in d:
                        dp[(c, p)] = int(d['DP'])
    return venn, cmp_, dp


def read_truth():
    """het: (chrom, pos, ref, alt1) -> (h0, ps), as compare reads it.
    bypos: (chrom, pos) -> list of (ref, alts, kind) with kind het / hom / other."""
    het, bypos = {}, defaultdict(list)
    for l in open(TRUTH):
        if l[0] == '#':
            continue
        f = l.rstrip('\n').split('\t')
        c, p, ref, alts = f[0], int(f[1]), f[3], f[4].split(',')
        a, ph = gt_alleles(f[9])
        if len(a) != 2 or '.' in a:
            bypos[(c, p)].append((ref, alts, 'other')); continue
        a0, a1 = int(a[0]), int(a[1])
        kind = 'het' if a0 != a1 else ('hom' if a0 > 0 else 'other')
        bypos[(c, p)].append((ref, alts, kind))
        if {a0, a1} == {0, 1}:
            ps = 1 if ph else 0     # v5.0q has no PS: compare uses one block per chromosome
            het[(c, p, ref, alts[0])] = (a0 if ph else -1, ps)
    return het, bypos


def classify(site, ref, alt, bypos, truth_het):
    """(a) het_match: the truth has the call's POS, REF and ALT as a 0/1 genotype,
    the match compare uses; (b) het_other_allele: another heterozygous truth
    record at that POS (other alleles, or a 1/2 record that includes the call's
    ALT); (c) hom: a homozygous truth record there; (d) absent; chrX/chrY are
    outside the chr1-22 truth and reported separately."""
    c, p = site
    if c in XY:
        return 'chrXY'
    if (c, p, ref, alt) in truth_het:
        return 'het_match'
    recs = bypos.get(site)
    if not recs:
        return 'absent'
    if any(k == 'het' for r, al, k in recs):
        return 'het_other_allele'
    if any(k == 'hom' for r, al, k in recs):
        return 'hom'
    return 'absent'


def emulate_compare(truth_het, query):
    """CompareProcess.cpp steps 3-6 on SNV-only output: common variants by
    (chrom, pos, ref, alt1), blocks by (truth PS, query PS) over variants phased
    in both, block-wise Hamming = min(m, n - m), switch pairs on h0.
    Returns per-site flags and totals."""
    by_block = defaultdict(list)
    for k, (qh, qps, _) in query.items():
        t = truth_het.get(k)
        if t is None or t[0] < 0 or qh < 0 or t[1] == 0 or qps == 0:
            continue
        by_block[(k[0], t[1], qps)].append((k[1], t[0], qh))
    ham_site, sw_end, assessed = set(), set(), set()
    tot_ham = tot_sw = tot_sw_snv_pairs = 0
    sw_pairs = []                       # (chrom, posA, posB)
    for (c, _, _), v in by_block.items():
        if len(v) < 2:
            continue
        v.sort()
        mism = [t != q for _, t, q in v]
        m = sum(mism); n = len(v)
        tot_ham += min(m, n - m)
        wrong_if = True if m <= n - m else False          # majority orientation; ties count as 'same'
        for (p, _, _), x in zip(v, mism):
            assessed.add((c, p))
            if x == wrong_if:
                ham_site.add((c, p))
        for i in range(n - 1):
            st = v[i][1] != v[i + 1][1]
            sq = v[i][2] != v[i + 1][2]
            if st != sq:
                tot_sw += 1
                sw_end.add((c, v[i][0])); sw_end.add((c, v[i + 1][0]))
                sw_pairs.append((c, v[i][0], v[i + 1][0]))
        tot_sw_snv_pairs += n - 1
    return assessed, ham_site, sw_end, tot_ham, tot_sw, sw_pairs


def read_swbed(path):
    iv = defaultdict(list)
    for l in open(path):
        if l.startswith(('#', 'track')):
            continue
        c, s, e = l.split('\t')[:3]
        iv[c].append((int(s), int(e)))
    for c in iv:
        iv[c].sort()
    return iv


def inside(iv, sites, extra=0):
    """run_coverage.sh: start < pos <= end (extra=1 also counts the second SNV)."""
    idx = {c: (L, [s for s, _ in L], [max(e for _, e in L[:i + 1]) for i in range(len(L))])
           for c, L in iv.items()}
    h = 0
    for c, p in sites:
        if c not in idx:
            continue
        L, S, M = idx[c]
        i = bisect.bisect_left(S, p) - 1
        if i >= 0 and M[i] + extra >= p:
            h += 1
    return h


truth_het, bypos = read_truth()
comp = open(f'{OUT}/issue6_composition.tsv', 'w')
comp.write('coverage\tset\tn\thet_match\thet_other_allele\thom\tabsent\tchrXY'
           '\tother_tool\tother_assessed\tother_hamming_err\tother_switch_endpoint\n')
recon = open(f'{OUT}/issue6_reconcile.tsv', 'w')
recon.write('coverage\tvenn_lp_only_minus_wh_only\thet_match_lp_only_minus_wh_only'
            '\tphased_snv_wh_minus_lp\tphased_snv_wh\tphased_snv_lp\tmultiallelic_first_alt_wh_minus_lp\n')
hist = open(f'{OUT}/issue6_depth_hist.tsv', 'w')
hist.write('coverage\tset\tn\tbin_start\tbin_end\tfraction\n')
chk = open(f'{OUT}/issue6_checks.tsv', 'w')
chk.write('coverage\ttool\tcheck\tthis_script\tcompare\n')
iv6 = open(f'{OUT}/issue6_intervals.tsv', 'w')
iv6.write('coverage\tset\tother_tool\tn\tin_other_sw_pct\tin_other_sw_incl_second_pct'
          '\tother_background_pct\tother_background_incl_second_pct\tenrichment\tenrichment_incl_second\n')

for cov in (10, 30, 60):
    lp_v, lp_c, dp = read_call(f'{R}/longphase_gnn/longphase_gnn_{cov}x_1.vcf', info=True)
    pre_v, _, _ = read_call(f'{R}/longphase/longphase_{cov}x_1.vcf')
    wh_v, wh_c, _ = read_call(f'{R}/whatshap_v2.8/only/whatshap_v28_onlySNVs_{cov}x_1.vcf')
    alt = {(k[0], k[1]): (k[2], k[3]) for k in lp_c if len(k[2]) == 1 and len(k[3]) == 1}
    lp_u = {s for s, p in lp_v.items() if not p}; lp_p = {s for s, p in lp_v.items() if p}
    wh_u = {s for s, p in wh_v.items() if not p}; wh_p = {s for s, p in wh_v.items() if p}
    both = lp_u & wh_u; lp_only = lp_u & wh_p; wh_only = wh_u & lp_p
    removed = {s for s, p in pre_v.items() if p} & lp_u
    sets = [('lp_only_phase', lp_only - removed), ('lp_only_gnn', lp_only & removed),
            ('lp_only', lp_only), ('wh_only', wh_only), ('both', both),
            ('background', set(lp_v) - lp_only - wh_only - both)]

    acc = {}
    for tool, q, swf in (('WhatsHap', wh_c, f'whatshap_v28_onlySNVs_{cov}x_1.vcf.sw.tsv'),
                         ('LongPhase 2', lp_c, f'longphase_gnn_{cov}x_1.vcf.sw.tsv')):
        assessed, hs, se, th, ts, _ = emulate_compare(truth_het, q)
        acc[tool] = (assessed, hs, se)
        # compare's Phased_SNV: phased in both, REF and first ALT single-base
        hits = [k for k, (qh, _, _) in q.items() if qh >= 0 and len(k[2]) == 1 and len(k[3]) == 1
                and k in truth_het and truth_het[k][0] >= 0]
        phased_snv = len(hits)
        acc[tool + '_psnv'] = phased_snv
        acc[tool + '_ma'] = sum(1 for k in hits if q[k][2])     # calls with two ALTs, outside the Venn universe
        # check against the manuscript table (compare, v5.0q chr1-22, no BED)
        name = ('whatshap_v28_onlySNVs' if tool == 'WhatsHap' else 'longphase_gnn') + f'_{cov}x_1.vcf'
        for l in open(f'{R}/20260924_v50q.txt'):
            if l.startswith('###' + name):
                t = l.split('\t')
                chk.write(f'{cov}x\t{tool}\tPhased_SNV\t{phased_snv}\t{t[1]}\n')
                chk.write(f'{cov}x\t{tool}\tSNV_SW\t{ts}\t{t[5]}\n')
                chk.write(f'{cov}x\t{tool}\tHamming_%\t{100 * th / max(1, len(assessed)):.5f}\t{t[7]}\n')

    for name, S in sets:
        cl = Counter(classify(s, alt[s][0], alt[s][1], bypos, truth_het) for s in S)
        other = 'WhatsHap' if name.startswith('lp_only') else ('LongPhase 2' if name == 'wh_only' else '')
        if other:
            a, hs, se = acc[other]
            hm = {s for s in S if classify(s, alt[s][0], alt[s][1], bypos, truth_het) == 'het_match'}
            cols = f'{other}\t{len(hm & a)}\t{len(hm & hs)}\t{len(hm & se)}'
        else:
            cols = '\tNA\tNA\tNA'
        comp.write(f'{cov}x\t{name}\t{len(S)}\t{cl["het_match"]}\t{cl["het_other_allele"]}\t{cl["hom"]}'
                   f'\t{cl["absent"]}\t{cl["chrXY"]}\t{cols}\n')
        if name in ('lp_only_phase', 'lp_only_gnn', 'lp_only', 'wh_only', 'both'):
            d = [dp[s] for s in S if s in dp]
            c = Counter(min(x // BIN, NB - 1) for x in d)
            for i in range(NB):
                hist.write(f'{cov}x\t{name}\t{len(d)}\t{i * BIN}\t{"" if i == NB - 1 else (i + 1) * BIN}'
                           f'\t{c[i] / len(d):.5f}\n')

    hm_lp = sum(1 for s in lp_only if classify(s, alt[s][0], alt[s][1], bypos, truth_het) == 'het_match')
    hm_wh = sum(1 for s in wh_only if classify(s, alt[s][0], alt[s][1], bypos, truth_het) == 'het_match')
    recon.write(f'{cov}x\t{len(lp_only) - len(wh_only)}\t{hm_lp - hm_wh}'
                f'\t{acc["WhatsHap_psnv"] - acc["LongPhase 2_psnv"]}\t{acc["WhatsHap_psnv"]}\t{acc["LongPhase 2_psnv"]}'
                f'\t{acc["WhatsHap_ma"] - acc["LongPhase 2_ma"]}\n')

    # Fig. 3e intervals: as run_coverage.sh (full v5.0q, start < pos <= end), and with the second SNV included
    sw = {'WhatsHap': read_swbed(f'{SWDIR}/whatshap_v28_onlySNVs_{cov}x_1.vcf.sw.bed'),
          'LongPhase 2': read_swbed(f'{SWDIR}/longphase_gnn_{cov}x_1.vcf.sw.bed')}
    for name, S, other, phased in (('lp_only_phase', sets[0][1], 'WhatsHap', wh_p),
                                   ('lp_only_gnn', sets[1][1], 'WhatsHap', wh_p),
                                   ('lp_only', lp_only, 'WhatsHap', wh_p),
                                   ('wh_only', wh_only, 'LongPhase 2', lp_p)):
        x0 = 100 * inside(sw[other], S) / len(S); x1 = 100 * inside(sw[other], S, 1) / len(S)
        b0 = 100 * inside(sw[other], phased) / len(phased); b1 = 100 * inside(sw[other], phased, 1) / len(phased)
        iv6.write(f'{cov}x\t{name}\t{other}\t{len(S)}\t{x0:.2f}\t{x1:.2f}\t{b0:.2f}\t{b1:.2f}\t{x0 / b0:.2f}\t{x1 / b1:.2f}\n')
    for f in (comp, recon, hist, chk, iv6):
        f.flush()
    print(f'{cov}x done', flush=True)
