#!/bin/bash
# Quick test of HiPhase 1.7.0 and TinkerHap 1.0.0 (2026-10-17): HG002 chr22, 30x replicate 1, nanopore
# and PacBio HiFi, same PEPPER calls and BAMs as the paper. Scored against v5.0q chr22 with
# longphase compare (release v2.1), --ignore-sample-name, no BED; the paper's LongPhase v2.1.1 and
# WhatsHap 2.8 outputs of the same runs are cut to chr22 and scored the same way for reference.
# Default parameters; HiPhase needs --ignore-read-groups (the BAM read groups do not name the VCF
# sample) and --reference. HiPhase targets PacBio data; the nanopore run is for information only. Starts after HapBridge.
set -uo pipefail
cd /ssd/longphase_process/quicktest
until grep -qE "done$" /ssd/longphase_process/hapbridge/run_hapbridge.log 2>/dev/null; do sleep 60; done
echo "$(date '+%F %T') start"
R=/disk/research
REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
HP=/disk/software/hiphase_v1.7.0/hiphase-v1.7.0-x86_64-unknown-linux-gnu/hiphase
TH=/disk/software/longhap_env/bin/tinkerhap
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
BG=$(command -v bgzip || echo /disk/software/htslib/bgzip); TB=$(command -v tabix || echo /disk/software/htslib/tabix)
[[ -s truth_chr22.vcf ]] || awk '/^#/ || $1=="chr22"' /ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf > truth_chr22.vcf
chr22() { zcat -f "$1" | awk '/^#/ || $1=="chr22"'; }
score() { $CMP compare -t 8 --ignore-sample-name truth_chr22.vcf "$1" -o "sw_$2" > /dev/null 2>&1 \
          && echo "$2 $(grep '^###' sw_$2.tsv | grep -v Sample | cut -f2-11)" || echo "FAILED compare $2"; }
for plat in ont hifi; do
    if [[ $plat == ont ]]; then V=$R/pepper_calling/pepper_30x_1.vcf.gz; B=$R/bam/hg002.sup.30x.1.bam
         LPV=$R/v2.1.1/longphase_gnn/longphase_gnn_30x_1.vcf; WHV=$R/whatshap_v2.8/only/whatshap_v28_onlySNVs_30x_1.vcf
    else V=$R/pacbio/pepper_calling/pepper_hifi_30x.vcf.gz; B=$R/pacbio/bam/hg002.hifi.30x.1.bam
         LPV=$R/v2.1.1/pacbio/longphase_hifi_30x_1.vcf; WHV=$R/pacbio/whatshap_v28_hifi_onlySNVs_30x_1.vcf
    fi
    [[ -s in_${plat}.vcf.gz.tbi ]] || { chr22 $V | $BG > in_${plat}.vcf.gz && $TB -p vcf in_${plat}.vcf.gz; }
    chr22 $LPV > longphase211_${plat}.vcf; score longphase211_${plat}.vcf longphase211_${plat}
    [[ -f $WHV ]] && { chr22 $WHV > whatshap_${plat}.vcf; score whatshap_${plat}.vcf whatshap_${plat}; }
    echo "$(date '+%F %T') tinkerhap $plat"
    /usr/bin/time -v -o tinkerhap_${plat}.time $TH -vi in_${plat}.vcf.gz -bi $B -r chr22 -vo tinkerhap_${plat}.vcf \
        -l tinkerhap_${plat}.log > tinkerhap_${plat}.out 2>&1 && score tinkerhap_${plat}.vcf tinkerhap_${plat} || echo "FAILED tinkerhap $plat"
    echo "$(date '+%F %T') hiphase $plat"
    /usr/bin/time -v -o hiphase_${plat}.time $HP --bam $B --vcf in_${plat}.vcf.gz --output-vcf hiphase_${plat}.vcf.gz \
        --reference $REF --threads 16 --ignore-read-groups \
        --stats-file hiphase_${plat}.stats.csv > hiphase_${plat}.log 2>&1 && score hiphase_${plat}.vcf.gz hiphase_${plat} || echo "FAILED hiphase $plat"
done
echo "$(date '+%F %T') done"
