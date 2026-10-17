#!/bin/bash
# PacBio HiFi SNV+indel phasing, replicate 1, 10-50x (2026-10-17), the counterpart of HiPhase and
# TinkerHap, which phase indels by default. Same commands, binaries and inputs as the paper's HiFi
# SNV rows with indels added: LongPhase v2.1.1 `phase --pb -t 24 --indels`; WhatsHap 2.8 without
# --only-snvs (it phases indels by default). Scored like the other HiFi rows (longphase compare
# release v2.1, --ignore-sample-name, v5.0q chr1-22, no BED). Not timed for the paper: the five
# WhatsHap runs go in parallel and share the machine with the nanopore TinkerHap/HiPhase runs.
set -uo pipefail
cd /ssd/longphase_process/hifi_indels
P=/disk/research/pacbio
LP=/disk/software/longphase_v2.1.1_static/longphase_linux-x64
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
REF=/disk/research/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
BENCH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
WO=$P/whatshap_v2.8_indels; LO=/disk/research/v2.1.1/pacbio/indels; mkdir -p $WO $LO
inwork() { docker exec -w /ssd/longphase_process/hifi_indels workEnv bash -c "source /opt/miniconda/etc/profile.d/conda.sh; conda activate whatshap-env; $*"; }
score() { $CMP compare -t 8 --ignore-sample-name $BENCH $1.vcf -o $(dirname $1)/sw_$(basename $1) > /dev/null 2>&1 \
          && grep "^###" $(dirname $1)/sw_$(basename $1).tsv | grep -v Sample || echo "FAILED compare $1"; }
echo "$(date '+%F %T') start"
for c in 10 20 30 40 50; do
    o=$WO/whatshap_v28_hifi_indels_${c}x_1
    [[ -s $o.vcf ]] || ( inwork "/usr/bin/time -v -o $o.time whatshap phase --ignore-read-groups -o $o.vcf --reference=$REF \
        $P/pepper_calling/pepper_hifi_${c}x.vcf.gz $P/bam/hg002.hifi.${c}x.1.bam > $o.log 2>&1" && score $o || echo "FAILED whatshap ${c}x" ) &
done
for c in 10 20 30 40 50; do
    o=$LO/longphase_hifi_indel_${c}x_1
    [[ -s $o.vcf ]] || /usr/bin/time -v -o $o.time $LP phase --pb -t 24 --indels -s $P/pepper_calling/pepper_hifi_${c}x.vcf.gz \
        -b $P/bam/hg002.hifi.${c}x.1.bam -r $REF -o $o > $o.log 2>&1 || echo "FAILED longphase ${c}x"
    score $o
done
wait
echo "$(date '+%F %T') done"
