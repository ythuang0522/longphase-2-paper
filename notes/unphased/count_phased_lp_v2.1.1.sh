#!/bin/bash
# count_phased.sh for LongPhase 2 only (v2.1.1 runs), 8 VCFs at a time; WhatsHap rows are taken
# unchanged from the v2.1 table (its VCFs did not change). Same call definition and awk as count_phased.sh.
set -euo pipefail
cd /ssd/longphase_process/unphased_sets_v2.1.1
G=/disk/research/v2.1.1
count() {
    awk -F'\t' '!/^#/ && $1 ~ /^chr([1-9]|1[0-9]|2[0-2])$/ && length($4)==1 && length($5)==1 && $4 ~ /^[ACGT]$/ && $5 ~ /^[ACGT]$/ {
        n=split($9,f,":"); gi=0; for(i=1;i<=n;i++) if(f[i]=="GT") gi=i; if(!gi) next
        split($10,s,":"); if(s[gi]=="0|1" || s[gi]=="1|0") c++ } END {print c+0}' "$1"
}
export -f count; export G
{ for c in 10 12 14 16 18 20; do for r in $(seq 1 10); do echo "$c $r"; done; done; for c in 30 40 50 60; do echo "$c 1"; done; } |
  xargs -P 8 -L 1 bash -c 'printf "LongPhase 2\t%s\t%s\t%s\n" "$0" "$1" "$(count $G/longphase_gnn/longphase_gnn_${0}x_${1}.vcf)"' > lp_counts.tsv
{ printf 'tool\tcoverage\treplicate\tphased_het_snv_calls_chr1_22\n'
  { cat lp_counts.tsv; grep '^WhatsHap' /disk/software/longphase-2-paper/notes/unphased/phased_calls_chr1_22.tsv; } | sort -t$'\t' -k1,1 -k2,2n -k3,3n
} > phased_calls_chr1_22.tsv
echo "$(date '+%F %T') count_lp done"
