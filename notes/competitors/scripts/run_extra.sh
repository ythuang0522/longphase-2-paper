#!/bin/bash
# Added 2026-10-17, default parameters, replicate 1, scored like every other row (longphase compare
# release v2.1, --ignore-sample-name, v5.0q chr1-22, no BED). Starts after the nanopore
# TinkerHap/HiPhase runs; shares the machine with the LongHap all-variant runs (not timed for the paper).
#  1. TinkerHap 1.0.0 on PacBio HiFi 10-50x: the paper's HiFi inputs (per-coverage PEPPER calls,
#     hg002.hifi.<c>x.1.bam); one run per chromosome, 8 at a time, as on nanopore.
#  (HiPhase all-variant on nanopore dropped: HiPhase is a PacBio tool.)
set -uo pipefail
cd /ssd/longphase_process/extra
until grep -qE "done$" /ssd/longphase_process/others_ont/run_others_ont.log 2>/dev/null; do sleep 60; done
echo "$(date '+%F %T') start; $(cat /proc/loadavg)"
R=/disk/research; P=$R/pacbio
REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
HP=/disk/software/hiphase_v1.7.0/hiphase-v1.7.0-x86_64-unknown-linux-gnu/hiphase
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
TRUTH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
A=/ssd/longphase_process/longhap/allvar
score() { $CMP compare -t 16 --ignore-sample-name $TRUTH $1.vcf -o sw_$1 > /dev/null 2>&1 \
          && grep "^###" sw_$1.tsv | grep -v Sample || echo "FAILED compare $1"; }
export TH=/disk/software/longhap_env/bin/tinkerhap
for c in 10 20 30 40 50; do
    export V=$P/pepper_calling/pepper_hifi_${c}x.vcf.gz B=$P/bam/hg002.hifi.${c}x.1.bam d=tinkerhap_hifi/${c}x
    mkdir -p $d; o=tinkerhap_hifi_${c}x_1
    if [[ ! -s $o.vcf ]]; then
        echo "$(date '+%F %T') tinkerhap hifi ${c}x"
        seq 1 22 | xargs -P 8 -I{} bash -c '/usr/bin/time -v -o $d/chr{}.time $TH -vi $V -bi $B -r chr{} -vo $d/chr{}.vcf \
            -l $d/chr{}.log -q > $d/chr{}.out 2>&1 || echo "FAILED tinkerhap $d chr{}"'
        { grep "^#" $d/chr1.vcf; for i in $(seq 1 22); do awk -v c=chr$i '!/^#/ && $1==c' $d/chr$i.vcf; done; } > $o.vcf
    fi
    score $o
done
echo "$(date '+%F %T') done"
