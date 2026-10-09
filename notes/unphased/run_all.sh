#!/bin/bash
# Rerun of the 2026-09-26/27 give-up analysis (scripts/ = the original
# scripts, unchanged) on replicate 1 at 10x, 30x and 60x.
set -u
cd /ssd/longphase_process/unphased_sets
R=/disk/research
RES=/home/twolinin/Downloads            # T2T dipcall BED/VCF used by run_unphase_venn.sh
TRUTH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.vcf.gz
LP=/disk/software/longphase_v2.1_release/longphase_linux-x64
one() {
    c=$1; O=out/${c}x; mkdir -p $O
    PRE=$R/longphase/longphase_${c}x_1.vcf; GNN=$R/longphase_gnn/longphase_gnn_${c}x_1.vcf
    WH=$R/whatshap_v2.8/only/whatshap_v28_onlySNVs_${c}x_1.vcf
    bash scripts/run_coverage.sh ${c}x $PRE $GNN $WH $TRUTH $LP $O > $O/run_coverage.log 2>&1
    bash scripts/run_unphase_venn.sh $GNN $WH $RES $O > $O/run_unphase_venn.log 2>&1
    # sites removed by the GNN: phased before, unphased after (as in run_coverage.sh)
    het() { awk -v sep="$2" '/^#/{next} length($4)==1 && length($5)==1 {
        split($10,f,":"); g=f[1]; gsub(/\|/,"/",g)
        if (g!="0/1" && g!="1/0") next
        if (index(f[1],sep)) print $1"\t"$2 }' "$1" | LC_ALL=C sort -u; }
    LC_ALL=C comm -12 <(het $PRE "|") <(het $GNN "/") > $O/gnn_removed.txt
    bash scripts/giveup_detail.sh $O $O/gnn_removed.txt $GNN $O > $O/giveup_detail.log 2>&1
    echo "$(date '+%F %T') ${c}x done"
}
for c in 10 30 60; do one $c & done; wait
