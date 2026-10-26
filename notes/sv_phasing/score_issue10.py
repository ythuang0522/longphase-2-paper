#!/usr/bin/env python3
"""Paper issue #10: score every run (SV phase vs T2T dipcall with score_sv_phase.py; SNVs with longphase compare
against v5.0q) and write sv_phasing.tsv and snv.tsv. Runs: replicate 1, nanopore 10-60x and HiFi 10-50x;
LongPhase 2 v2.1.2 with and without GNN, WhatsHap 2.8, HiPhase 1.7.0 (HiFi); inputs SNV+SV and SNV+indel+SV."""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
R = '/disk/research'; O = R + '/v2.1.2'; I = O + '/issue10'
HERE = os.path.dirname(os.path.abspath(__file__))   # sv_phasing.tsv, snv.tsv and the truth cache are written here
CMP = '/disk/software/longphase_v2.1.1_static/longphase_linux-x64'
V50 = '/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf'
COV = {'ONT': [10, 12, 14, 16, 18, 20, 30, 40, 50, 60], 'HiFi': [10, 20, 30, 40, 50]}
INP = {'SNV+SV': ('sv', 'snv_sv'), 'SNV+indel+SV': ('indel_sv', 'snv_indel_sv')}


def runs():
    for pf, covs in COV.items():
        p = 'ont' if pf == 'ONT' else 'hifi'
        for c in covs:
            for inp, (cfg, tag) in INP.items():
                merged = f'{I}/in_{tag}_{p}_{c}x.vcf.gz'
                for g in ('yes', 'no'):
                    sfx = '_gnn' if g == 'yes' else ''
                    if pf == 'ONT':
                        d = {'sv': 'longphase_coh_sv', 'indel_sv': 'longphase_coh_indel_sv'}[cfg] + sfx
                        v = f'{O}/{d}/{d}_{c}x_1'
                    else:
                        d = f'longphase_hifi_{cfg}{sfx}'
                        v = f'{O}/pacbio/{d}/{d}_{c}x_1'
                    yield pf, inp, 'LongPhase 2', g, c, v + '.vcf', v + '_SV.vcf', merged
                w = f'{I}/wh_{tag}_{p}_{c}x_1.vcf'
                yield pf, inp, 'WhatsHap', '-', c, w, w, merged
                if pf == 'HiFi':
                    h = f'{I}/hp_{tag}_hifi_{c}x_1.vcf.gz'
                    yield pf, inp, 'HiPhase', '-', c, h, h, merged


def snv(vcf):
    base = os.path.join(os.path.dirname(vcf), 'sw_' + os.path.basename(vcf).replace('.vcf.gz', '').replace('.vcf', ''))
    if not os.path.exists(base + '.tsv'):
        subprocess.run([CMP, 'compare', '-t', '8', '--ignore-sample-name', V50, vcf, '-o', base],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for l in open(base + '.tsv'):
        if l.startswith('###') and not l.startswith('###Sample'):
            f = l[3:].rstrip('\n').split('\t')
            return {'phased_snv': f[1], 'snv_switch': f[5], 'snv_switch_rate_pct': f[6], 'hamming_pct': f[7],
                    'blocks': f[8], 'block_n50': f[9]}
    raise RuntimeError('no summary in ' + base + '.tsv')


def one(r):
    pf, inp, tool, g, c, vcf, svv, merged = r
    if not (os.path.exists(vcf) and os.path.exists(svv) and os.path.exists(merged)):
        return r, None, None
    out = subprocess.run([sys.executable, HERE + '/score_sv_phase.py', vcf, svv, merged], capture_output=True, text=True, check=True).stdout
    return r, out, snv(vcf)


if __name__ == '__main__':
    head = ['platform', 'input', 'tool', 'gnn', 'coverage', 'replicate']
    sv_cols = ['svtype', 'size_class', 'sv_input', 'sv_phased', 'right', 'wrong', 'phased_hom_in_truth',
               'phased_no_truth_match', 'phased_no_block_snv']
    snv_cols = ['phased_snv', 'snv_switch', 'snv_switch_rate_pct', 'hamming_pct', 'blocks', 'block_n50']
    with ThreadPoolExecutor(8) as ex, open(HERE + '/sv_phasing.tsv', 'w') as a, open(HERE + '/snv.tsv', 'w') as b:
        print('\t'.join(head + sv_cols), file=a); print('\t'.join(head + snv_cols + ['vcf']), file=b)
        for r, out, s in ex.map(one, list(runs())):
            key = [r[0], r[1], r[2], r[3], str(r[4]), '1']
            if out is None:
                print('MISSING', r[5], file=sys.stderr); continue
            for l in out.splitlines():
                print('\t'.join(key + l.split('\t')), file=a)
            print('\t'.join(key + [s[k] for k in snv_cols] + [r[5]]), file=b)
