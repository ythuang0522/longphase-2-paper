#!/bin/bash
# HiPhase 1.7.0 on PacBio HiFi, replicate 1 at 10-50x (2026-10-17): the inputs of the WhatsHap,
# HapCUT2 and LongPhase HiFi rows (per-coverage PEPPER calls, hg002.hifi.<c>x.1.bam). Default
# parameters; --ignore-read-groups is required (the BAM read groups do not name the VCF sample),
# --reference and --threads 16 are inputs. Timed with GNU time -v, one job at a time, after the
# chr22 quick test. Scored like the other HiFi rows: longphase compare --ignore-sample-name
# v5.0q chr1-22, no BED.
set -uo pipefail
R=/disk/research
O=$R/pacbio/hiphase_v1.7.0
HP=/disk/software/hiphase_v1.7.0/hiphase-v1.7.0-x86_64-unknown-linux-gnu/hiphase
LP=/disk/software/longphase_v2.1.1_static/longphase_linux-x64
BENCH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
cd $O
until grep -qE "done$" /ssd/longphase_process/quicktest/run_quicktest.log 2>/dev/null; do sleep 60; done
echo "$(date '+%F %T') start; $(cat /proc/loadavg)"
for c in 10 20 30 40 50; do
    s=hiphase_v170_hifi_${c}x_1
    [[ -s $s.vcf ]] && continue
    echo "$(date '+%F %T') ${c}x"
    /usr/bin/time -v -o $s.time $HP --bam $R/pacbio/bam/hg002.hifi.${c}x.1.bam --vcf $R/pacbio/pepper_calling/pepper_hifi_${c}x.vcf.gz \
        --output-vcf $s.vcf.gz --reference $REF --threads 16 --ignore-read-groups \
        --stats-file $s.stats.csv --blocks-file $s.blocks.tsv > $s.log 2>&1 || { echo "FAILED ${c}x"; tail -3 $s.log; continue; }
    zcat $s.vcf.gz > $s.vcf
    grep -E "Elapsed|Maximum resident" $s.time
    $LP compare -t 24 --ignore-sample-name $BENCH $s.vcf -o sw_$s > /dev/null 2>&1 && grep "^###$s" sw_$s.tsv || echo "COMPARE FAILED ${c}x"
done
echo "$(date '+%F %T') done"
