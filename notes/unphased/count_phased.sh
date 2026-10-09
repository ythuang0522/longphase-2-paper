#!/usr/bin/env bash
# Count phased heterozygous SNV calls on chr1-22 per run (issue #7).
# Call definition as in issue #6: single-base REF and ALT, one ALT allele,
# GT 0|1 or 1|0, chr1-22.
set -euo pipefail
R=/disk/research
count() {
    awk -F'\t' '!/^#/ && $1 ~ /^chr([1-9]|1[0-9]|2[0-2])$/ && length($4)==1 && length($5)==1 && $4 ~ /^[ACGT]$/ && $5 ~ /^[ACGT]$/ {
        n=split($9,f,":"); gi=0; for(i=1;i<=n;i++) if(f[i]=="GT") gi=i; if(!gi) next
        split($10,s,":"); if(s[gi]=="0|1" || s[gi]=="1|0") c++ } END {print c+0}' "$1"
}
runs() {
    for c in 10 12 14 16 18 20; do for r in $(seq 1 10); do echo "$c $r"; done; done
    for c in 30 40 50 60; do echo "$c 1"; done
}
export -f count
{
    printf 'tool\tcoverage\treplicate\tphased_het_snv_calls_chr1_22\n'
    runs | while read c r; do
        printf 'LongPhase 2\t%s\t%s\t%s\n' "$c" "$r" "$(count $R/longphase_gnn/longphase_gnn_${c}x_${r}.vcf)" &
        printf 'WhatsHap\t%s\t%s\t%s\n' "$c" "$r" "$(count $R/whatshap_v2.8/only/whatshap_v28_onlySNVs_${c}x_${r}.vcf)" &
        wait
    done | sort -t$'\t' -k1,1 -k2,2n -k3,3n
} > phased_calls_chr1_22.tsv
