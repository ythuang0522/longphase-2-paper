#!/usr/bin/env bash
# Count phased heterozygous SNV calls on chr1-22 per HiFi SNV-only run (issue #9).
# count() as in count_phased.sh (issue #7): single-base REF and ALT, one ALT allele,
# GT 0|1 or 1|0, chr1-22. The VCFs are the ones scored for SNV_Detail and Other_phasers.
set -euo pipefail
count() {
    awk -F'\t' '!/^#/ && $1 ~ /^chr([1-9]|1[0-9]|2[0-2])$/ && length($4)==1 && length($5)==1 && $4 ~ /^[ACGT]$/ && $5 ~ /^[ACGT]$/ {
        n=split($9,f,":"); gi=0; for(i=1;i<=n;i++) if(f[i]=="GT") gi=i; if(!gi) next
        split($10,s,":"); if(s[gi]=="0|1" || s[gi]=="1|0") c++ } END {print c+0}' "$1"
}
LP=/disk/research/v2.1.1/pacbio                  # LongPhase 2 v2.1.1 with GNN (--pb)
WH=/disk/research/pacbio                         # WhatsHap 2.8 --only-snvs
HP=/ssd/longphase_process/hifi_snvonly           # HiPhase 1.7.0, SNV-only input VCF
{
    printf 'tool\tcoverage\treplicate\tphased_het_snv_calls_chr1_22\n'
    for c in 10 20 30 40 50; do
        printf 'LongPhase 2\t%s\t1\t%s\n' "$c" "$(count $LP/longphase_hifi_${c}x_1.vcf)" &
        printf 'WhatsHap\t%s\t1\t%s\n' "$c" "$(count $WH/whatshap_v28_hifi_onlySNVs_${c}x_1.vcf)" &
        printf 'HiPhase\t%s\t1\t%s\n' "$c" "$(count $HP/hiphase_v170_hifi_snv_${c}x_1.vcf)" &
        wait
    done | sort -t$'\t' -k1,1 -k2,2n
} > phased_calls_hifi_chr1_22.tsv
