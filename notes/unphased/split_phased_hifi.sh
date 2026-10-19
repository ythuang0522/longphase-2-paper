#!/usr/bin/env bash
# Issue #9: why the precision of phased HiFi calls is above the call-set precision. Per HiFi
# SNV-only run: het. SNV calls on chr1-22 (count_phased.sh definition), split into phased (0|1, 1|0)
# and unphased (0/1), and how many of each match a v5.0q heterozygous SNV by position and ALT.
set -euo pipefail
export T=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
sp() {
  awk -F'\t' -v tool="$1" -v cov="$2" 'NR==FNR { if(!/^#/ && length($4)==1 && length($5)==1) { split($10,s,":"); g=s[1]; if(g=="0|1"||g=="1|0"||g=="0/1"||g=="1/0") h[$1":"$2":"$5]=1 } next }
    !/^#/ && $1 ~ /^chr([1-9]|1[0-9]|2[0-2])$/ && length($4)==1 && length($5)==1 && $4 ~ /^[ACGT]$/ && $5 ~ /^[ACGT]$/ {
      n=split($9,f,":"); gi=0; for(i=1;i<=n;i++) if(f[i]=="GT") gi=i; if(!gi) next
      split($10,s,":"); g=s[gi]; k=$1":"$2":"$5
      if(g=="0|1"||g=="1|0") { p++; if(k in h) pt++ } else if(g=="0/1"||g=="1/0") { u++; if(k in h) ut++ } }
    END { printf "%s\t%s\t1\t%d\t%d\t%d\t%d\n", tool, cov, p, pt, u, ut }' $T "$3"
}
export -f sp
{
  printf 'tool\tcoverage\treplicate\tphased_calls\tphased_in_benchmark\tunphased_calls\tunphased_in_benchmark\n'
  for c in 10 20 30 40 50; do
    echo "LongPhase_2 $c /disk/research/v2.1.1/pacbio/longphase_hifi_${c}x_1.vcf"
    echo "WhatsHap $c /disk/research/pacbio/whatshap_v28_hifi_onlySNVs_${c}x_1.vcf"
    echo "HiPhase $c /ssd/longphase_process/hifi_snvonly/hiphase_v170_hifi_snv_${c}x_1.vcf"
  done | xargs -P 8 -L 1 bash -c 'sp "$@"' _ | sed 's/^LongPhase_2/LongPhase 2/' | sort -t$'\t' -k1,1 -k2,2n
} > phased_unphased_hifi_chr1_22.tsv
