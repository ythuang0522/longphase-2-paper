#!/bin/bash
# Issue 2 (longphase-2-paper): rescore the existing phased VCFs on the GNN
# held-out chromosomes chr17, chr21 and chr22.  Same command as the 2026-09-24
# tables (release v2.1 compare, --ignore-sample-name, no BED), plus only
# --regions=chr17,chr21,chr22.  Check: without --regions, longphase_gnn_10x_1
# gives 1,510 SNV switch errors against v5.0q, as in 20260924_v50q.txt.
#
# Writes heldout_v50q.txt, heldout_cophase_v50q.txt, heldout_GIAB421.txt in
# the format of the 2026-09-24 tables (one ### summary line per run).
set -uo pipefail
cd /ssd/longphase_process/heldout
export LP=/disk/software/longphase_v2.1_release/longphase_linux-x64
export V5=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
export V4=/disk/research/HG002_GRCh38_1_22_v4.2.1_benchmark_hifiasm_v11_phasetransfer.noDirty.vcf
R=/disk/research
SNV="$R/longphase_gnn $R/longphase $R/whatshap_v2.8/only $R/hapcut2_v1.3.4 $R/margin_v2.3.1 $R/ralphi/output"
COPH="$R/longphase_gnn $R/longphase $R/whatshap_v2.8/only $R/whatshap_v2.8
      $R/longphase_cophasing $R/longphase_cophasing_gnn
      $R/longphase_coh_indel $R/longphase_coh_indel_gnn $R/longphase_coh_sv $R/longphase_coh_sv_gnn
      $R/longphase_coh_methyl $R/longphase_coh_methyl_gnn
      $R/longphase_coh_indel_sv $R/longphase_coh_indel_sv_gnn
      $R/longphase_coh_indel_methyl $R/longphase_coh_indel_methyl_gnn"
vcfs() { for d in "$@"; do find $d -maxdepth 1 -type f | grep -E "_[0-9]+x_[0-9]+(\.phased)?\.(vcf|VCF)(\.gz)?$"; done; }
one() {  # truth_tag vcf
    local t=$V5; [[ $1 == v4 ]] && t=$V4
    local n=$(basename "$2"); n=${n%.gz}; n=${n%.*}
    local o=out_$1/$n
    [[ -f $o.tsv ]] || $LP compare -t 4 --ignore-sample-name --regions=chr17,chr21,chr22 "$t" "$2" -o $o > /dev/null 2>&1 \
        || echo "FAILED $1 $2"
}
export -f one
mkdir -p out_v5 out_v4
{ for f in $(vcfs $SNV); do echo "v5 $f"; echo "v4 $f"; done
  for f in $(vcfs $COPH); do echo "v5 $f"; done; } | sort -u | xargs -P 6 -L 1 bash -c 'one "$@"' _
table() {  # truth_tag dirs... -> stdout
    local tag=$1; shift
    head -1 $(ls out_$tag/*.tsv | head -1) | grep -q . && grep -h "^###Sample" $(ls out_$tag/*.tsv | head -1)
    for f in $(vcfs "$@" | sort); do n=$(basename "$f"); n=${n%.gz}; n=${n%.*}
        grep -h "^###" out_$tag/$n.tsv | grep -v "^###Sample"; done
}
table v5 $SNV  > heldout_v50q.txt
table v5 $COPH > heldout_cophase_v50q.txt
table v4 $SNV  > heldout_GIAB421.txt
wc -l heldout_*.txt
echo "$(date '+%F %T') done"
