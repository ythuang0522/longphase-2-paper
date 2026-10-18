#!/bin/bash
# HiPhase 1.7.0 and TinkerHap 1.0.0 SNV-only on PacBio HiFi, replicate 1, 10-50x (2026-10-18): the
# counterpart of the SNV_Detail HiFi rows (WhatsHap --only-snvs, LongPhase and HapCUT2 SNVs only).
# Neither tool has an SNV-only option, so both read the per-coverage PEPPER calls restricted to SNVs
# (REF and every ALT one base), the set WhatsHap --only-snvs phases. Otherwise as the indel runs:
# HiPhase defaults with --threads 16 --ignore-read-groups (one job at a time on an idle machine,
# timed with time -v); TinkerHap defaults, one run per chromosome, 8 at a time. Scored like the
# other HiFi rows (longphase compare release v2.1, --ignore-sample-name, v5.0q chr1-22, no BED).
set -uo pipefail
cd /ssd/longphase_process/hifi_snvonly
R=/disk/research; P=$R/pacbio
REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
HP=/disk/software/hiphase_v1.7.0/hiphase-v1.7.0-x86_64-unknown-linux-gnu/hiphase
export TH=/disk/software/longhap_env/bin/tinkerhap
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
TRUTH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
BG=$(command -v bgzip || echo /disk/software/htslib/bgzip); TB=$(command -v tabix || echo /disk/software/htslib/tabix)
score() { $CMP compare -t 16 --ignore-sample-name $TRUTH $1.vcf -o sw_$1 > /dev/null 2>&1 \
          && grep "^###" sw_$1.tsv | grep -v Sample || echo "FAILED compare $1"; }
echo "$(date '+%F %T') start; $(cat /proc/loadavg)"
for c in 10 20 30 40 50; do
    V=snv_hifi_${c}x.vcf.gz
    [[ -s $V.tbi ]] || { zcat $P/pepper_calling/pepper_hifi_${c}x.vcf.gz | awk -F'\t' '/^#/ || (length($4)==1 && $5 ~ /^[ACGTacgt](,[ACGTacgt])*$/)' \
                         | $BG > $V && $TB -f -p vcf $V; }
done
for c in 10 20 30 40 50; do
    o=hiphase_v170_hifi_snv_${c}x_1
    if [[ ! -s $o.vcf ]]; then
        echo "$(date '+%F %T') hiphase ${c}x"
        /usr/bin/time -v -o $o.time $HP --bam $P/bam/hg002.hifi.${c}x.1.bam --vcf snv_hifi_${c}x.vcf.gz --output-vcf $o.vcf.gz \
            --reference $REF --threads 16 --ignore-read-groups --stats-file $o.stats.csv --blocks-file $o.blocks.tsv > $o.log 2>&1 \
            && zcat $o.vcf.gz > $o.vcf || { echo "FAILED hiphase ${c}x"; tail -3 $o.log; continue; }
        grep -E "Elapsed|Maximum resident" $o.time
    fi
    score $o
done
for c in 10 20 30 40 50; do
    export V=snv_hifi_${c}x.vcf.gz B=$P/bam/hg002.hifi.${c}x.1.bam d=tinkerhap/${c}x
    mkdir -p $d; o=tinkerhap_hifi_snv_${c}x_1
    if [[ ! -s $o.vcf ]]; then
        echo "$(date '+%F %T') tinkerhap ${c}x"
        seq 1 22 | xargs -P 8 -I{} bash -c '$TH -vi $V -bi $B -r chr{} -vo $d/chr{}.vcf -l $d/chr{}.log -q > $d/chr{}.out 2>&1 || echo "FAILED tinkerhap $d chr{}"'
        { grep "^#" $d/chr1.vcf; for i in $(seq 1 22); do awk -v c=chr$i '!/^#/ && $1==c' $d/chr$i.vcf; done; } > $o.vcf
    fi
    score $o
done
echo "$(date '+%F %T') done"
