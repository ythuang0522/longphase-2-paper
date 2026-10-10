"""Per-block Hamming errors of a chr20 query against v5.0q (min of mismatches and matches per PS)."""
import sys, collections
def rd(p, chrom='chr20'):
    d = {}
    for l in open(p):
        if l[0] == '#': continue
        t = l.rstrip('\n').split('\t')
        if t[0] != chrom: continue
        f = dict(zip(t[8].split(':'), t[9].split(':')))
        gt = f.get('GT', '')
        if gt in ('0|1', '1|0'): d[(t[1], t[3], t[4])] = (gt, f.get('PS'))
    return d
truth = rd('/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf'); q = rd(sys.argv[1])
blk = collections.defaultdict(lambda: [0, 0, 10**12, 0])
for k, (gt, ps) in q.items():
    if k not in truth: continue
    b = blk[ps]; b[0 if gt == truth[k][0] else 1] += 1; p = int(k[0]); b[2] = min(b[2], p); b[3] = max(b[3], p)
rows = sorted(((min(a, m), a + m, ps, s, e) for ps, (a, m, s, e) in blk.items()), reverse=True)
tot = sum(r[0] for r in rows); n = sum(r[1] for r in rows)
print(f'Hamming {tot}/{n} = {100*tot/n:.1f}% over {len(rows)} blocks')
acc = 0
for i, (h, size, ps, s, e) in enumerate(rows[:8]):
    acc += h; print(f'  block PS={ps} {s:,}-{e:,} ({(e-s)/1e6:.1f} Mb) assessed={size} hamming={h} ({100*h/size:.0f}% of block) cum {100*acc/tot:.0f}% of all')
