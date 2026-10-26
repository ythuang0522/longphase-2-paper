#!/usr/bin/env python3
"""SV phasing accuracy against the T2T-HG002 Q100 v1.1 dipcall VCF (GRCh38), paper issue #10.

    score_sv_phase.py TOOL_VCF SV_VCF MERGED_INPUT  -> TSV rows (svtype x size_class) on stdout

TOOL_VCF      phased VCF whose SNVs orient the blocks (LongPhase main VCF; WhatsHap/HiPhase output)
SV_VCF        VCF with the tool's SV records (LongPhase *_SV.vcf; for WhatsHap/HiPhase the same as TOOL_VCF)
MERGED_INPUT  the merge_sv.py VCF given to WhatsHap and HiPhase: only its Sniffles DEL/INS records (ID Sniffles2.*)
              are scored, for every tool, as twolinin/longphase#136 (SVTYPE records only); PEPPER indels of 50 bp or
              more in the SNV+indel+SV input are not SVs here. Records are matched by chromosome, position and
              Sniffles ID (several SVs can share a position)

Rules (the scoring of twolinin/longphase#136, unchanged):
- Truth: dipcall records with an allele on both haplotypes (no '.'), chr1-22. Truth SVs are DEL/INS of
  at least 50 bp; truth SNVs are heterozygous one-base records.
- A phased DEL/INS of at least 50 bp matches a truth SV of the same type, size within 70%, and position within
  1 kb or, for a deletion, at least 50% reciprocal overlap; the nearest match is used.
- The phase is compared with the truth after orienting its block (PS) by the majority of its SNVs.
Categories of a phased SV: right, wrong, phased_hom_in_truth (the match is on both haplotypes),
phased_no_truth_match, phased_no_block_snv (no SNV of its block is in the truth, or a tie; cannot be oriented).
right + wrong + phased_hom_in_truth + phased_no_truth_match + phased_no_block_snv = sv_phased.
"""
import sys, gzip, bisect, pickle, os
from collections import defaultdict
TRUTH = '/disk/research/homo_mutant_test/GRCh38_HG2-T2TQ100-V1.1_dipcall-z2k.dip.vcf.gz'
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'truth.pkl')
CHROMS = {f'chr{i}' for i in range(1, 23)}
CLASSES = ('50-999', '1000-9999', '>=10000')
COLS = ['sv_input', 'sv_phased', 'right', 'wrong', 'phased_hom_in_truth', 'phased_no_truth_match', 'phased_no_block_snv']


def opener(p):
    return gzip.open(p, 'rt') if p.endswith('.gz') else open(p)


def load_truth():
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE, 'rb'))
    snv = defaultdict(dict)          # chr -> pos -> haplotype index of ALT (0 or 1)
    sv = defaultdict(list)           # chr -> [(pos, type, size, haps)]
    for line in opener(TRUTH):
        if line[0] == '#':
            continue
        f = line.split('\t', 10)
        c = f[0]
        if c not in CHROMS:
            continue
        gt = f[9].split(':')[0]
        if '|' not in gt:
            continue
        a = gt.split('|')
        if '.' in a:
            continue
        a = [int(x) for x in a]
        pos = int(f[1]); ref = f[3]; alts = f[4].split(',')
        if len(ref) == 1 and all(len(x) == 1 for x in alts):
            if sorted(a) == [0, 1]:
                snv[c][pos] = a.index(1)
            continue
        for k, alt in enumerate(alts, 1):
            d = len(alt) - len(ref)
            if abs(d) < 50:
                continue
            haps = tuple(h for h in (0, 1) if a[h] == k)
            if haps:
                sv[c].append((pos, 'INS' if d > 0 else 'DEL', abs(d), haps))
    for c in sv:
        sv[c].sort()
    t = (dict(snv), dict(sv))
    pickle.dump(t, open(CACHE, 'wb'))
    return t


def sv_of(f):
    """(type, size) of a DEL/INS record of at least 50 bp, or None."""
    info = dict(x.split('=', 1) if '=' in x else (x, '') for x in f[7].split(';'))
    typ = info.get('SVTYPE')
    if typ in ('DEL', 'INS') and 'SVLEN' in info:
        try:
            size = abs(int(info['SVLEN']))
        except ValueError:
            return None
    else:
        alts = f[4].split(',')
        if len(alts) != 1 or alts[0].startswith('<'):
            return None
        d = len(alts[0]) - len(f[3])
        typ, size = ('INS' if d > 0 else 'DEL'), abs(d)
    return (typ, size) if size >= 50 else None


def size_class(s):
    return CLASSES[0] if s < 1000 else CLASSES[1] if s < 10000 else CLASSES[2]


def phased(sample):
    gt = sample.split(':')[0]
    if '|' not in gt:
        return None
    a = gt.split('|')
    if a[0] == a[1] or '.' in a:
        return None
    return a


def main(toolp, svp, mergedp):
    tsnv, tsv = load_truth()
    # the scored set: heterozygous DEL/INS >= 50 bp of the merged input, chr1-22
    scored = {}
    for line in opener(mergedp):
        if line[0] == '#':
            continue
        f = line.rstrip('\n').split('\t')
        if f[0] not in CHROMS or not f[2].startswith('Sniffles2'):   # Sniffles DEL/INS only, not the PEPPER indels >= 50 bp
            continue
        s = sv_of(f)
        if not s:
            continue
        gt = f[9].split(':')[0].replace('|', '/')
        if gt in ('0/1', '1/0'):
            scored[(f[0], int(f[1]), f[2])] = s
    agree = defaultdict(lambda: [0, 0])
    for line in opener(toolp):
        if line[0] == '#':
            continue
        f = line.rstrip('\n').split('\t')
        c = f[0]
        if c not in tsnv or len(f[3]) != 1 or len(f[4]) != 1:
            continue
        a = phased(f[9])
        if not a:
            continue
        keys = f[8].split(':'); vals = f[9].split(':')
        if 'PS' not in keys:
            continue
        h = tsnv[c].get(int(f[1]))
        if h is None or '1' not in a:
            continue
        agree[(c, vals[keys.index('PS')])][0 if a.index('1') == h else 1] += 1
    n = defaultdict(lambda: defaultdict(int))     # (svtype, class) -> column -> count

    def add(typ, size, k):
        for t in (typ, 'all'):
            for cl in (size_class(size), 'all'):
                n[(t, cl)][k] += 1
    for (c, pos, _), (typ, size) in scored.items():
        add(typ, size, 'sv_input')
    seen = set()
    for line in opener(svp):
        if line[0] == '#':
            continue
        f = line.rstrip('\n').split('\t')
        c, pos, key = f[0], int(f[1]), (f[0], int(f[1]), f[2])
        if key not in scored or key in seen:
            continue
        s = sv_of(f)
        if not s:
            continue
        typ, size = scored[key]
        a = phased(f[9])
        if not a:
            continue
        seen.add(key)
        add(typ, size, 'sv_phased')
        keys = f[8].split(':'); vals = f[9].split(':')
        ps = vals[keys.index('PS')] if 'PS' in keys else None
        q = a.index('1') if '1' in a else None
        best = None
        L = tsv.get(c, [])
        reach = max(1000, size) if typ == 'DEL' else 1000
        i = bisect.bisect_left(L, (pos - reach,))
        while i < len(L) and L[i][0] <= pos + reach:
            tp, tt, ts, th = L[i]
            if tt == typ and min(ts, size) / max(ts, size) >= 0.7:
                d = abs(tp - pos)
                ov = min(tp + ts, pos + size) - max(tp, pos)
                if d <= 1000 or (typ == 'DEL' and ov >= 0.5 * max(ts, size)):
                    if best is None or d < best[0]:
                        best = (d, th)
            i += 1
        if best is None:
            add(typ, size, 'phased_no_truth_match'); continue
        th = best[1]
        if len(th) == 2:
            add(typ, size, 'phased_hom_in_truth'); continue
        ag = agree.get((c, ps))
        if not ag or ag[0] == ag[1] or q is None:
            add(typ, size, 'phased_no_block_snv'); continue
        add(typ, size, 'right' if (q == th[0]) != (ag[1] > ag[0]) else 'wrong')
    for t in ('DEL', 'INS', 'all'):
        for cl in CLASSES + ('all',):
            print('\t'.join([t, cl] + [str(n[(t, cl)][k]) for k in COLS]))


if __name__ == '__main__':
    main(*sys.argv[1:4])
