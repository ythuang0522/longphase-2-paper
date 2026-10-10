# fix_methphaser_vcf.py  用法: python fix_methphaser_vcf.py in.vcf out.vcf
import re, sys, pysam

src, dst = sys.argv[1], sys.argv[2]
text = open(src).read()
# 在「非換行字元」後面緊接著 "chrXXX<TAB>數字<TAB>" 的地方補上換行
text = re.sub(r'(?<=[^\n])(?=chr\w+\t\d+\t)', '\n', text)

header, records = [], []
for line in text.splitlines():
    if not line.strip():
        continue
    (header if line.startswith('#') else records).append(line)

contigs = [m.group(1) for h in header
           for m in [re.match(r'##contig=<ID=([^,>]+)', h)] if m]
order = {c: i for i, c in enumerate(contigs)}
records.sort(key=lambda l: (order.get(l.split('\t')[0], len(order)),
                            int(l.split('\t')[1])))

with open(dst, 'w') as f:
    f.write('\n'.join(header + records) + '\n')
pysam.tabix_index(dst, preset='vcf', force=True)   # 輸出 dst.gz 與 dst.gz.tbi
