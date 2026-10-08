"""Write a slim copy of a phased VCF for issue #1: heterozygous (0/1, 1/0)
records only, FORMAT reduced to GT:PS, INFO dropped. `longphase compare` and
score_phase.py give identical results on the slim and the original file.

Usage: slim_vcf.py IN.vcf[.gz] OUT.vcf   (then bgzip OUT.vcf)
"""
import gzip, sys
src, dst = sys.argv[1], sys.argv[2]
op = gzip.open if src.endswith('.gz') else open
with op(src, 'rt') as f, open(dst, 'w') as o:
    for line in f:
        if line.startswith('##'):
            if line.startswith(('##fileformat', '##contig', '##longphase', '##commandline',
                                '##source', '##reference', '##FILTER')):
                o.write(line)
            continue
        if line[0] == '#':
            o.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n'
                    '##FORMAT=<ID=PS,Number=1,Type=Integer,Description="Phase set">\n')
            o.write('\t'.join(line.rstrip('\n').split('\t')[:10]) + '\n')
            continue
        c = line.rstrip('\n').split('\t')
        fmt = c[8].split(':'); val = c[9].split(':')
        gt = val[fmt.index('GT')] if 'GT' in fmt else '.'
        if gt not in ('0/1', '1/0', '0|1', '1|0'):
            continue
        ps = '.'
        if 'PS' in fmt:
            i = fmt.index('PS')
            if i < len(val):
                ps = val[i]
        o.write('\t'.join([c[0], c[1], c[2], c[3], c[4], c[5], c[6], '.', 'GT:PS', f'{gt}:{ps}']) + '\n')
