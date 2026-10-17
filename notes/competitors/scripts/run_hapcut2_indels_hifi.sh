#!/bin/bash
# HapCUT2 1.3.4 with indels on PacBio HiFi, replicate 1, 10-50x (2026-10-17): the paper's HiFi
# HapCUT2 runs (run_hapcut2_hifi.sh: extractHAIRS --pacbio 1 + HAPCUT2, the same 0/1/2-genotype
# filtered PEPPER calls) with extractHAIRS --indels 1. Five coverages in parallel, not timed for the
# paper. Scored like the other HiFi rows. Starts after the nanopore HapCUT2 indel runs (memory).
set -uo pipefail
O=/disk/research/pacbio/hapcut2_v1.3.4/indels; cd $O
export LD_LIBRARY_PATH=/disk/software/HapCUT2/htslib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
until grep -qE "done$" /ssd/longphase_process/extra/run_hapcut2_indels.log 2>/dev/null; do sleep 60; done
echo "$(date '+%F %T') start; $(cat /proc/loadavg)"
H=/disk/software/HapCUT2/build; R=/disk/research; P=$R/pacbio
REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
TRUTH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
for c in 10 20 30 40 50; do
  (
    s=hapcut2_v134_hifi_indels_${c}x_1; V=$P/hapcut2_v1.3.4/pepper_hifi_${c}x.vcf
    /usr/bin/time -v -o $s.time bash -c "$H/extractHAIRS --pacbio 1 --indels 1 --bam $P/bam/hg002.hifi.${c}x.1.bam --ref $REF --VCF $V --out fragment_${c}x \
        && $H/HAPCUT2 --fragments fragment_${c}x --VCF $V --output $s" > $s.log 2>&1
    if [[ -s $s.phased.VCF ]]; then
        cp $s.phased.VCF $s.vcf; rm -f fragment_${c}x
        $CMP compare -t 4 --ignore-sample-name $TRUTH $s.vcf -o sw_$s > /dev/null 2>&1 && grep "^###" sw_$s.tsv | grep -v Sample || echo "FAILED compare ${c}x"
    else echo "FAILED ${c}x"; tail -3 $s.log; fi
  ) &
done
wait
echo "$(date '+%F %T') done"
