#!/bin/bash
# Issue 2, optional item: indel-pair metrics of item 3 (issue 1) on chr17/21/22,
# from the existing co-phasing VCFs (no new phasing).
cd /ssd/longphase_process/heldout/indel   # working directory on the lab server; score_heldout.py and aggregate_indel.py are next to this script
export V5=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf R=/disk/research
RUNS="$(for c in 10 12 14 16 18 20; do for s in $(seq 1 10); do echo ${c}x_$s; done; done) 30x_1 40x_1 50x_1 60x_1"
one() { [[ -f out/$1.tsv ]] && return 0
  /disk/software/gnn_env/bin/python3 score_heldout.py $V5 $2 out/$1.tmp 2> out/$1.err && mv out/$1.tmp.tsv out/$1.tsv && mv out/$1.tmp.sw.tsv out/$1.sw.tsv && rm -f out/$1.err || echo "FAILED $1"; }
export -f one
for run in $RUNS; do
  for cfg in coh_indel coh_indel_sv coh_indel_methyl cophasing; do
    echo "longphase_${cfg}_$run $R/longphase_${cfg}/longphase_${cfg}_$run.vcf"
    echo "longphase_${cfg}_gnn_$run $R/longphase_${cfg}_gnn/longphase_${cfg}_gnn_$run.vcf"
  done
  echo "whatshap_v28_$run $R/whatshap_v2.8/whatshap_v28_$run.vcf"
done | xargs -P 4 -L 1 bash -c 'one "$@"' _
echo "$(date '+%F %T') done"
