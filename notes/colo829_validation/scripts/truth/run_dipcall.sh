#!/bin/bash
# run_dipcall.sh: dipcall of COLO829BL DSA v3.0.0 (hap1 = hapX SMASFTH1B2J6, hap2 = hapY SMASFK4V33V8; hap1 first, so
# 0|1 means hap1 = REF) against the paper's GRCh38 no-alt reference, whole assembly vs whole reference, then gaps, norm
# (-c x, as HG008) and make_truth.py on chr1-22. Rules: notes/hg008_validation/README.md, Phase reference (unchanged).
set -euo pipefail
W=/home/user/work; E=$W/tools/env/bin; export PATH=$E:$PATH; S=$(dirname $(readlink -f $0))
cd $W/truth; REF=$W/ref/GRCh38.fa; P=COLO829BL_dsa3_GRCh38
[[ -s $P.mak ]] || run-dipcall -t ${THREADS:-4} $P $REF $W/asm/hap1.fa.gz $W/asm/hap2.fa.gz > $P.mak
make -j1 -f $P.mak
python3 $S/gaps.py $W/asm/hap1.fa.gz hap1.gaps.bed; python3 $S/gaps.py $W/asm/hap2.fa.gz hap2.gaps.bed
printf 'COLO829BL\n' > sample.txt
bcftools reheader -s sample.txt -o named.vcf.gz $P.dip.vcf.gz
bcftools norm -f $REF -c x -Oz -o norm.vcf.gz named.vcf.gz 2> norm.log; tail -2 norm.log
samtools index $P.hap1.bam; samtools index $P.hap2.bam
python3 $S/make_truth.py norm.vcf.gz $P.dip.bed $P.hap1.bam $P.hap2.bam hap1.gaps.bed hap2.gaps.bed COLO829BL_truth
python3 $S/check_truth.py COLO829BL_truth.vcf $P.hap1.bam $P.hap2.bam > check_truth.txt
bgzip -f COLO829BL_truth.vcf && tabix -f -p vcf COLO829BL_truth.vcf.gz
echo truth done
