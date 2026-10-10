#!/bin/bash
# Issue 5: rewrite the MethPhaser VCFs with the corrected PS lookup (VCF step only).
source /opt/miniconda/etc/profile.d/conda.sh; conda activate methphaser_env
c=$1; W=/disk/research/methphaser/rerun_0.0.4/${c}x
cd $W && /usr/bin/time -v python /ssd/longphase_process/methphaser_issue5/psfix/post_vcf_only.py -t 4 \
  -ib $W/hg002.sup.${c}x.1.tagged.primary.bam -if $W/work/ -ov $W/methphaser_${c}x_1.psfix.vcf -ob $W/unused \
  -vc /disk/research/methphaser/test/${c}x/longphase_${c}x_1.vcf.gz > $W/psfix.log 2>&1 \
 && python /disk/research/methphaser/fix_methphaser_vcf.py methphaser_${c}x_1.psfix.vcf methphaser_${c}x_1.psfix.fixed.vcf \
 && zcat methphaser_${c}x_1.psfix.fixed.vcf.gz > methphaser_${c}x_1.psfix.fixed.vcf && echo "${c}x done" || echo "${c}x FAILED"
