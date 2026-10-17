#!/bin/bash
# HapCUT2 1.3.4 with indels on nanopore, replicate 1, 10-60x (2026-10-17): the paper's HapCUT2 runs
# (/disk/research/hapcut2_v1.3.4/run_hapcut2.sh: extractHAIRS --ont 1 + HAPCUT2) with extractHAIRS
# --indels 1 and the full PEPPER calls (pepper_calling/, SNVs and indels; the paper's SNV runs read
# pepper_calling3/, which holds the SNVs only), unzipped, records whose GT is not two alleles from
# {0,1,2} dropped (HapCUT2 rejects them), the HapCUT2 counterpart of the SNV+indel rows. The six coverages run in
# parallel (single-threaded each), alongside other jobs: not timed for the paper. Scored like every
# other row (longphase compare release v2.1, --ignore-sample-name, v5.0q chr1-22, no BED).
# Starts after the nanopore TinkerHap/HiPhase runs.
set -uo pipefail
O=/disk/research/hapcut2_v1.3.4/indels; cd $O
export LD_LIBRARY_PATH=/disk/software/HapCUT2/htslib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
until grep -qE "done$" /ssd/longphase_process/others_ont/run_others_ont.log 2>/dev/null; do sleep 60; done
echo "$(date '+%F %T') start; $(cat /proc/loadavg)"
H=/disk/software/HapCUT2/build
R=/disk/research; REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
TRUTH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
for c in 10 20 30 40 50 60; do
  (
    s=hapcut2_v134_indels_${c}x_1; V=pepper_${c}x_1.vcf
    [[ -s $V ]] || zcat $R/pepper_calling/pepper_${c}x_1.vcf.gz | awk -F'\t' '/^#/ || $10 ~ /^[012][\/|][012](:|$)/' > $V
    /usr/bin/time -v -o $s.time bash -c "$H/extractHAIRS --ont 1 --indels 1 --bam $R/bam/hg002.sup.${c}x.1.bam --ref $REF --VCF $V --out fragment_${c}x \
        && $H/HAPCUT2 --fragments fragment_${c}x --VCF $V --output $s" > $s.log 2>&1
    if [[ -s $s.phased.VCF ]]; then
        cp $s.phased.VCF $s.vcf; rm -f fragment_${c}x
        $CMP compare -t 4 --ignore-sample-name $TRUTH $s.vcf -o sw_$s > /dev/null 2>&1 && grep "^###" sw_$s.tsv | grep -v Sample || echo "FAILED compare ${c}x"
    else echo "FAILED ${c}x"; tail -3 $s.log; fi
  ) &
done
wait
echo "$(date '+%F %T') done"
