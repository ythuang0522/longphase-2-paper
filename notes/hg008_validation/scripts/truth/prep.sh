#!/bin/bash
# prep.sh: dipcall VCF -> sample HG008N, bcftools norm -c x against the exact reference (-c e stops at the records whose
# reference base is an IUPAC code: norm_w.log lists every REF check warning; only NON_ACGTN_REF occurred, excluded by -c x),
# then make_truth.py. bcftools from the workEnv container (ralphi_env).
set -euo pipefail
cd /disk/research/HG008/truth; REF=/disk/research/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
B() { docker exec -w /disk/research/HG008/truth workEnv bash -c "source /opt/miniconda/etc/profile.d/conda.sh; conda activate ralphi_env; $*"; }
printf 'HG008N\n' > HG008N.sample.txt
B "bcftools --version | head -1; bcftools reheader -s HG008N.sample.txt -o HG008N.named.vcf.gz HG008N_v6.3_GRCh38.dip.vcf.gz && bcftools norm -f $REF -c x -Oz -o HG008N.norm.vcf.gz HG008N.named.vcf.gz 2> norm.log; tail -2 norm.log"
B "bcftools view -m2 -M2 -v snps -g het -f '.,PASS' -Oz -o HG008N.het_snv.candidates.vcf.gz HG008N.norm.vcf.gz && bcftools index -t HG008N.het_snv.candidates.vcf.gz && bcftools view -H HG008N.het_snv.candidates.vcf.gz | wc -l"
/ssd/polyploid/env/bin/python make_truth.py HG008N.norm.vcf.gz HG008N_v6.3_GRCh38.dip.bed HG008N_v6.3_GRCh38.hap1.bam HG008N_v6.3_GRCh38.hap2.bam ../asm/hap1.gaps.bed ../asm/hap2.gaps.bed HG008N_v6.3_truth
