#!/usr/bin/env python3
"""Rewrite the LongPhase 2 (GNN correction) values of the JSX drafts at the repository root with
the v2.1.2 data (copy of notes/v2.1.1/update_jsx.py; only the values of runs with SVs or 5mC change,
the SNV-only and SNV + indel values are identical to v2.1.1 and are rewritten unchanged). The drafts are
JHL's working figures and are not used by the build; values of the other tools and of LongPhase 2
without correction are left as they are.

Sources: supplementary.xlsx (after update_xlsx.py), 20260924_GIAB421.txt (v4.2.1), the Fig. 4e
composition constants of figures-source/make_results_figs.py and notes/unphased/figure_data_*.js.

    python3 update_jsx.py          (run from anywhere; edits the .jsx files in place)
"""
import os, re, statistics as st
from collections import defaultdict
import openpyxl

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SNV = ['psnv', 'psnv_pct', 'sw', 'sw_pct', 'ham', 'nblock', 'n50', 'bsum']
COPH = ['psnv', 'psnv_pct', 'pindel', 'pindel_pct', 'sw', 'sw_pct', 'ham', 'nblock', 'n50', 'bsum']

wb = openpyxl.load_workbook(os.path.join(ROOT, 'supplementary.xlsx'), read_only=True, data_only=True)
runs = defaultdict(list)   # (platform, config, cov) -> list of dicts, LongPhase 2 with GNN correction
for sheet, cols, ci, off in (('SNV_Detail', SNV, None, 2), ('co-phase_Detail', COPH, 2, 3)):
    R = [r for r in wb[sheet].iter_rows(values_only=True)]
    i0 = [k for k, h in enumerate(R[0]) if h == 'longphase_v2.1.2'][0]
    for r in R[2:]:
        if not r[off] or 'x_' not in str(r[off]) or r[i0] is None:
            continue
        cov, rep = map(int, r[off].split('x_'))
        plat = 'HiFi' if r[1].startswith('PB') else 'ONT'
        runs[(plat, r[ci] if ci else 'SNV', cov)].append(dict(zip(cols, r[i0:i0 + len(cols)]), rep=rep))
v4 = defaultdict(list)
for line in open(os.path.join(ROOT, '20260924_GIAB421.txt')):
    if line.startswith('###') and not line.startswith('###Sample'):
        t = line[3:].split('\t')
        m = re.match(r'(.+)_(\d+)x_(\d+)\.', t[0])
        v4[(m.group(1), int(m.group(2)))].append(dict(zip(COPH, map(float, t[1:]))))


def mean(rs, k): return st.mean(float(x[k]) for x in rs)
def rep1(rs): return [x for x in rs if x['rep'] == 1]


def setval(line, key, val):
    if key.startswith('hc_') and not re.search(r'\b' + key + r':', line):   # HapCUT2 HiFi series, added 2026-10-16
        line = re.sub(r'\s*\},?\s*$', lambda m: f', {key}: 0' + m.group(0), line, count=1)
    new, n = re.subn(r'(\b' + re.escape(key) + r':\s*)[-0-9.]+', lambda m: m.group(1) + val, line)
    assert n <= 1, (key, line[:80])
    if n == 0 and not key.startswith('lp_'):
        raise KeyError((key, line[:80]))
    return new


def edit_rows(path, fields, rename=()):
    """fields(cov) -> {key: value string} for each data row `{ cov: ... }`."""
    p = os.path.join(ROOT, path)
    out = []
    for line in open(p).read().split('\n'):
        m = re.match(r'\s*\{\s*cov:\s*"?(\d+)x?"?,', line)
        if m:
            for k, v in fields(int(m.group(1))).items():
                line = setval(line, k, v)
        for a, b in rename:   # skip text already renamed, so the script can be rerun
            line = re.sub(re.escape(a) + (r'(?![.\d])' if a[-1].isdigit() else ''), b, line)
        out.append(line)
    open(p, 'w').write('\n'.join(out))
    print('updated', path)


g5 = lambda x: f'{x:.5f}'.rstrip('0').rstrip('.')
g4 = lambda x: f'{x:.4f}'.rstrip('0').rstrip('.')
CFG = {'lp': 'SNV', 'lp_sv': 'SV', 'lp_indel': 'Indel', 'lp_indel_sv': 'Indel+SV'}
V4N = {'SNV': 'longphase_gnn', 'Indel': 'longphase_coh_indel_gnn', 'Indel+SV': 'longphase_coh_indel_sv_gnn'}


def cophase_group(c):
    d = {}
    for k, cfg in CFG.items():
        rs = runs[('ONT', cfg, c)]
        d[f'{k}_sw'] = g5(mean(rs, 'sw_pct')); d[f'{k}_ham'] = g4(mean(rs, 'ham')); d[f'{k}_n50'] = g4(mean(rs, 'n50') / 1e6)
    return d


def bench(c):   # PhasingBenchmark*.jsx: lp = SNV, lp_indel = Indel, lp_sv = Indel+SV
    d = {}
    for k, cfg in (('lp', 'SNV'), ('lp_indel', 'Indel'), ('lp_sv', 'Indel+SV')):
        rs = runs[('ONT', cfg, c)]
        d[f'{k}_sw50'] = f"{mean(rs, 'sw'):.0f}"; d[f'{k}_ham50'] = g4(mean(rs, 'ham'))
        d[f'{k}_psnv'] = f"{mean(rs, 'psnv'):.0f}"; d[f'{k}_n50'] = g4(mean(rs, 'n50') / 1e6)
        d[f'{k}_sw42'] = f"{mean(v4[(V4N[cfg], c)], 'sw'):.0f}"; d[f'{k}_ham42'] = g4(mean(v4[(V4N[cfg], c)], 'ham'))
    return d


def hifi_other(name):
    """HiFi rows of another SNV_Detail block (WhatsHap, LongPhase 2 without correction)."""
    R = [r for r in wb['SNV_Detail'].iter_rows(values_only=True)]
    i0 = R[0].index(name)
    return {int(r[2].split('x_')[0]): dict(zip(SNV, r[i0:i0 + 8])) for r in R[2:] if r[1] and r[1].startswith('PB')}


HIFI_WH, HIFI_LP0, HIFI_HC = hifi_other('whatshap_v28'), hifi_other('longphase_v2.0.1'), hifi_other('hapcut2_v134')


# per-coverage HiFi calls phase 87% at 10x but 91.5-92.4% at 20-50x: widen the fixed axis
HIFI_AXIS = ('domain: [86, 88], ticks: [86, 86.5, 87, 87.5, 88]', 'domain: [86, 93], ticks: [86, 88, 90, 92]')


def hifi(c):
    """All three series: the drafts predate the per-coverage HiFi call sets (issue #4), so the
    WhatsHap and uncorrected values are refreshed from SNV_Detail too, not only the GNN ones."""
    d = {}
    for k, r in (('lpgnn', runs[('HiFi', 'SNV', c)][0]), ('wh', HIFI_WH[c]), ('lp', HIFI_LP0[c]), ('hc', HIFI_HC[c])):
        d.update({f'{k}_sw': f"{int(r['sw'])}", f'{k}_psnv': g5(float(r['psnv_pct'])),
                  f'{k}_ham': g5(float(r['ham'])), f'{k}_n50': g4(float(r['n50']) / 1e6)})
    return d


def add_hapcut2(path):
    """HapCUT2 on HiFi (2026-10-16): a fourth series and the title; the values come from hifi()."""
    p = os.path.join(ROOT, path)
    s = open(p).read()
    if 'key: "hc"' not in s:
        s = re.sub(r'(\n  \{ key: "wh",[^\n]*\n)', r'\1  { key: "hc",    name: "HapCUT2",       color: "#525252", dash: "2 2" },\n', s, count=1)
    s = s.replace('WhatsHap vs LongPhase 2.1.1 on PacBio HiFi', 'WhatsHap, HapCUT2 and LongPhase 2.1.1 on PacBio HiFi')
    open(p, 'w').write(s)


def meth(c):
    r = rep1(runs[('ONT', 'Mod', c)])[0]
    return {'lpgnn_sw': f"{int(r['sw'])}", 'lpgnn_psnv': g5(float(r['psnv_pct'])),
            'lpgnn_ham': g5(float(r['ham'])), 'lpgnn_n50': g4(float(r['n50']) / 1e6)}


src = open(os.path.join(ROOT, 'figures-source', 'make_results_figs.py')).read()
COMP = {int(c): tuple(map(int, v)) for c, *v in
        re.findall(r'(\d+): \((\d+), (\d+), (\d+)\)', src[src.index('COMPOSITION = {'):src.index('def t2t():')])}


def comp_line(path):
    p = os.path.join(ROOT, path)
    out = []
    for line in open(p).read().split('\n'):
        m = re.match(r'\s*\{cov:"(\d+)x"', line)
        if m:
            a, h, e = COMP[int(m.group(1))]; n = a + h + e
            for k, v in (('n', n), ('fp', f'{100 * a / n:.2f}'), ('hom', f'{100 * h / n:.2f}'), ('het', f'{100 * e / n:.2f}'),
                         ('n_fp', a), ('n_hom', h), ('n_het', e)):
                line = re.sub(r'(\b' + k + r':\s*)[-0-9.]+', lambda mm: mm.group(1) + str(v), line, count=1)
        out.append(line)
    open(p, 'w').write('\n'.join(out))
    print('updated', path)


def venn(path):
    """Replace each coverage block of DATA with the values of notes/unphased/figure_data_<c>x.js."""
    p = os.path.join(ROOT, path)
    s = open(p).read()
    for c in ('10x', '30x', '60x'):
        f = open(os.path.join(ROOT, 'notes', 'unphased', f'figure_data_{c}.js')).read()
        new = {k: re.search(k + r':\s*(\{[^}]*\})', f).group(1) for k in ('venn',)}
        sets = re.findall(r'set:\s*([\d.]+),\s*bg:\s*([\d.]+)', f)
        hists = {k: re.search(k + r':\s*\[([^\]]*)\]', f[f.index('hist'):]).group(1) for k in ('lp', 'wh', 'both')}
        i = s.index(f'"{c}": {{'); j = s.find('\n  "', i + 5); j = len(s) if j < 0 else j
        blk = s[i:j]
        blk = re.sub(r'venn:\s*\{[^}]*\}', 'venn: ' + new['venn'], blk, count=1)
        it = iter(sets)
        blk = re.sub(r'set:\s*[\d.]+,(\s*)bg:\s*[\d.]+', lambda m: (lambda v: f'set: {v[0]},{m.group(1)}bg: {v[1]}')(next(it)), blk)
        for k, v in hists.items():
            vals = [x.strip() for x in v.split(',') if x.strip()]
            body = blk[blk.index('hist'):]
            m = re.search(r'(\b' + k + r':\s*\[)([^\]]*)(\])', body)
            old_vals = [x.strip() for x in m.group(2).split(',') if x.strip()]
            assert len(old_vals) == len(vals), (c, k)
            rows = ['        ' + ','.join(vals[q:q + 12]) for q in range(0, len(vals), 12)]
            body = body[:m.start(2)] + '\n' + ',\n'.join(rows) + '\n      ' + body[m.end(2):]
            blk = blk[:blk.index('hist')] + body
        s = s[:i] + blk + s[j:]
    open(p, 'w').write(s)
    print('updated', path)


if __name__ == '__main__':
    edit_rows('CophaseGroupCompare.jsx', cophase_group)
    for f in ('PhasingBenchmarkBars.jsx', 'PhasingBenchmarkBarsRow.jsx', 'PhasingBenchmarkCompare.jsx'):
        edit_rows(f, bench, rename=(('longphase v2.1.1 ', 'longphase v2.1.2 '), ('"longphase v2.1.1"', '"longphase v2.1.2"')))
    edit_rows('HifiCompare.jsx', hifi, rename=(('"LongPhase 2.1.1"', '"LongPhase 2.1.2"'), ('LongPhase 2.1.1 on', 'LongPhase 2.1.2 on')))
    edit_rows('HifiCompare3.jsx', hifi, rename=(('"LongPhase 2.1.1"', '"LongPhase 2.1.2"'),
                                                ('LongPhase 2.1.1 (--disableGNN)', 'LongPhase 2.1.2 (--disableGNN)'),
                                                ('LongPhase 2.1.1 on', 'LongPhase 2.1.2 on')))
    edit_rows('MethPhaserCompare.jsx', meth, rename=(('LongPhase 2.1.1', 'LongPhase 2.1.2'),))
    # UnphasedComposition.jsx and UnphaseVenn3.jsx come from SNV-only runs: unchanged
