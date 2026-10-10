#!/usr/bin/env python3
"""Issue 5 follow-up: PS intervals (min POS..max POS of the records with one PS) that overlap
the interval of another PS on the same chromosome. chr1-22, phased heterozygous records.
For the unrepaired MethPhaser VCF the records are split as fix_methphaser_vcf.py splits them
(no sort). Also checks that the repaired VCF holds the same (CHROM,POS,REF,ALT,GT,PS) records."""
import gzip, re, sys, collections
AUT = {f'chr{i}' for i in range(1, 23)}
SPLIT = re.compile(r'(?<=[^\n])(?=chr\w+\t\d+\t)')

def records(path, raw=False):
    op = gzip.open if path.endswith('.gz') else open
    text = op(path, 'rt').read()
    if raw:
        text = SPLIT.sub('\n', text)
    for l in text.splitlines():
        if not l or l[0] == '#': continue
        t = l.split('\t')
        if t[0] not in AUT or len(t) < 10: continue
        f = dict(zip(t[8].split(':'), t[9].split(':')))
        gt, ps = f.get('GT', ''), f.get('PS')
        if '|' not in gt or ps in (None, '.') or len(set(gt.split('|'))) < 2: continue
        yield t[0], int(t[1]), t[3], t[4], gt, ps

def overlaps(recs):
    iv = {}
    for c, p, *_, ps in recs:
        k = (c, ps); a = iv.get(k)
        iv[k] = (min(a[0], p), max(a[1], p)) if a else (p, p)
    by = collections.defaultdict(list)
    for (c, ps), (s, e) in iv.items(): by[c].append((s, e, ps))
    n_ps, ov_bp, per = 0, 0, {}
    for c, L in by.items():
        L.sort()
        flag = set()
        # PS overlapping another PS: sweep keeping the furthest end so far
        best_e, best_ps = -1, None
        for s, e, ps in L:
            if s <= best_e: flag.add(ps); flag.add(best_ps)
            if e > best_e: best_e, best_ps = e, ps
        # bases covered by >= 2 intervals
        ev = sorted([(s, 1) for s, e, _ in L] + [(e + 1, -1) for s, e, _ in L])
        d, prev, bp = 0, None, 0
        for x, v in ev:
            if d >= 2: bp += x - prev
            d += v; prev = x
        n_ps += len(flag); ov_bp += bp; per[c] = (len(flag), bp)
    return len(iv), n_ps, ov_bp, per

if __name__ == '__main__':
    IN = '/disk/research/methphaser/test/{c}x/longphase_{c}x_1.vcf.gz'
    OUT = '/disk/research/methphaser/rerun_0.0.4/{c}x/methphaser_{c}x_1{s}.vcf'
    FIX = '/disk/research/methphaser/rerun_0.0.4/{c}x/methphaser_{c}x_1.psfix.fixed.vcf'
    print('coverage\tvcf\tPS_values\tPS_overlapping_another\toverlap_bp\trecords\tcheck')
    for c in map(int, sys.argv[1:] or (10, 20, 30, 40, 50, 60)):
        sets = {}
        for name, path, raw in (('input', IN.format(c=c), False),
                                ('unrepaired', OUT.format(c=c, s=''), True),
                                ('repaired', OUT.format(c=c, s='.fixed'), False),
                                ('PS_lookup_fixed', FIX.format(c=c), False)):
            R = list(records(path, raw)); sets[name] = collections.Counter(R)
            n, k, bp, per = overlaps(R)
            same = ''
            if name == 'repaired':
                same = f"same records as unrepaired: {sets['repaired'] == sets['unrepaired']}"
            elif name == 'PS_lookup_fixed':  # records that differ from the repaired VCF
                d = sets['repaired'] - sets[name]
                fixed = {r[:5] for r in d}
                same = (f"differs from repaired in {sum(d.values())} records, all PS -1 there: "
                        f"{all(r[-1] == '-1' for r in d)}; same POS/GT: "
                        f"{fixed == {r[:5] for r in sets[name] - sets['repaired']}}; PS -1 left: "
                        f"{sum(v for r, v in sets[name].items() if r[-1] == '-1')}")
            print(f'{c}x\t{name}\t{n}\t{k}\t{bp}\t{len(R)}\t{same}', flush=True)
