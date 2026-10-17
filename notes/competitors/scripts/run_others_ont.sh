#!/bin/bash
# TinkerHap 1.0.0 and HiPhase 1.7.0 on HG002 nanopore, replicate 1, 10-60x (2026-10-17), for the
# Supplementary Data: the same PEPPER calls and BAMs as the paper's SNV rows. Default parameters, no
# tuning. TinkerHap: one run per chromosome (-r chr<i>, 8 at a time; it has no thread option),
# records of that chromosome taken from each output and concatenated. HiPhase: --threads 16,
# --ignore-read-groups (required: the BAM read groups do not name the VCF sample); HiPhase is
# written for PacBio HiFi, run on nanopore as is. Scored like every other row: longphase compare
# (release v2.1) --ignore-sample-name against v5.0q chr1-22, no BED. Starts after the HiPhase HiFi runs.
set -uo pipefail
cd /ssd/longphase_process/others_ont
until grep -qE "done$" /ssd/longphase_process/runtime/run_hiphase_hifi.log 2>/dev/null; do sleep 60; done
echo "$(date '+%F %T') start; $(cat /proc/loadavg)"
R=/disk/research
REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
HP=/disk/software/hiphase_v1.7.0/hiphase-v1.7.0-x86_64-unknown-linux-gnu/hiphase
TH=/disk/software/longhap_env/bin/tinkerhap
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
TRUTH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
score() { $CMP compare -t 24 --ignore-sample-name $TRUTH $1.vcf -o sw_$1 > /dev/null 2>&1 \
          && grep "^###" sw_$1.tsv | grep -v Sample || echo "FAILED compare $1"; }
export TH
for c in 10 20 30 40 50 60; do
    export V=$R/pepper_calling/pepper_${c}x_1.vcf.gz B=$R/bam/hg002.sup.${c}x.1.bam d=tinkerhap/${c}x
    mkdir -p $d
    o=tinkerhap_${c}x_1
    if [[ ! -s $o.vcf ]]; then
        echo "$(date '+%F %T') tinkerhap ${c}x"
        seq 1 22 | xargs -P 8 -I{} bash -c '/usr/bin/time -v -o $d/chr{}.time $TH -vi $V -bi $B -r chr{} -vo $d/chr{}.vcf \
            -l $d/chr{}.log -q > $d/chr{}.out 2>&1 || echo "FAILED tinkerhap $d chr{}"'
        { grep "^#" $d/chr1.vcf; for i in $(seq 1 22); do awk -v c=chr$i '!/^#/ && $1==c' $d/chr$i.vcf; done; } > $o.vcf
    fi
    score $o
    o=hiphase_${c}x_1
    if [[ ! -s $o.vcf ]]; then
        echo "$(date '+%F %T') hiphase ${c}x"
        /usr/bin/time -v -o $o.time $HP --bam $B --vcf $V --output-vcf $o.vcf.gz --reference $REF --threads 16 \
            --ignore-read-groups --stats-file $o.stats.csv --blocks-file $o.blocks.tsv > $o.log 2>&1 \
            && zcat $o.vcf.gz > $o.vcf || { echo "FAILED hiphase ${c}x"; tail -3 $o.log; }
    fi
    [[ -s $o.vcf ]] && score $o
done
echo "$(date '+%F %T') done"
