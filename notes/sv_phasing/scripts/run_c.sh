#!/bin/bash
# Paper issue #10, comparators: WhatsHap 2.8 (--indels, one job per chromosome) on nanopore replicate 1 at
# 10-60x and HiFi 10-50x, and HiPhase 1.7.0 on HiFi, each on SNVs + SVs and on SNVs + indels + SVs.
# Their one input VCF is made with the paper's merge_sv.py (PEPPER calls + sequence-resolved Sniffles DEL/INS,
# chr1-22) from the new Sniffles calls (--reference) in /disk/research/v2.1.2; SNV-only = PEPPER records whose
# REF and every ALT are one base (as notes/competitors/scripts/run_hifi_snvonly.sh). Untimed environment
# (shares the machine with run_b.sh); /usr/bin/time -v is kept for every run as the issue asks.
set -uo pipefail
R=/disk/research; P=$R/pacbio; REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
O=$R/v2.1.2/issue10; mkdir -p $O; cd $O
PY=/disk/software/longhap_env/bin/python
MERGE=/disk/software/longphase-2-paper/notes/competitors/scripts/merge_sv.py
WH=/tmp/claude-1000/-disk-software-longphase/71da5d96-4a7e-438a-94f6-88eb87dc3db1/scratchpad/wsenv/bin/whatshap
HP=/disk/software/hiphase_v1.7.0/hiphase-v1.7.0-x86_64-unknown-linux-gnu/hiphase
paths() {  # platform coverage -> B V S
  if [[ $1 == ont ]]; then B=$R/bam/hg002.sup.$2x.1.bam; V=$R/pepper_calling/pepper_$2x_1.vcf.gz; S=$R/v2.1.2/sniffles/sniffles_$2x_1.vcf
  else B=$P/bam/hg002.hifi.$2x.1.bam; V=$P/pepper_calling/pepper_hifi_$2x.vcf.gz; S=$R/v2.1.2/pacbio/sniffles/sniffles_hifi_$2x.vcf; fi; }
prep() {  # platform coverage: SNV-only VCF and the two merged inputs
  local pf=$1 c=$2; paths $pf $c
  until [[ -s $S ]]; do sleep 60; done
  local n=${pf}_${c}x
  [[ -s snv_$n.vcf.gz.tbi ]] || { zcat $V | awk -F'\t' '/^#/ || (length($4)==1 && $5 ~ /^[ACGTacgt](,[ACGTacgt])*$/)' | bgzip > snv_$n.vcf.gz && tabix -f -p vcf snv_$n.vcf.gz; }
  for in in snv_sv snv_indel_sv; do
    [[ -s in_${in}_$n.vcf.gz.tbi ]] && continue
    [[ $in == snv_sv ]] && src=snv_$n.vcf.gz || src=$V
    $PY $MERGE $src $S $REF in_${in}_$n.vcf 2> in_${in}_$n.merge.log && bgzip -f in_${in}_$n.vcf && tabix -f -p vcf in_${in}_$n.vcf.gz \
      || echo "FAILED merge $in $n"
  done
  echo "$(date '+%F %T') inputs $n"; }
wh() {  # platform coverage input chrom
  local pf=$1 c=$2 in=$3 ch=$4 n=${1}_${2}x; paths $pf $c
  local d=wh_${in}_$n; mkdir -p $d
  [[ -s $d/$ch.vcf ]] && return
  /usr/bin/time -v -o $d/$ch.time $WH phase --indels --ignore-read-groups --reference=$REF --chromosome $ch -o $d/$ch.tmp.vcf in_${in}_$n.vcf.gz $B > $d/$ch.log 2>&1 \
    && mv $d/$ch.tmp.vcf $d/$ch.vcf || echo "FAILED whatshap $n $in $ch"; }
export -f paths prep wh; export R P REF O PY MERGE WH
echo "$(date '+%F %T') start"
RUNS="hifi 10;hifi 20;hifi 30;hifi 40;hifi 50;ont 10;ont 12;ont 14;ont 16;ont 18;ont 20;ont 30;ont 40;ont 50;ont 60"
echo "$RUNS" | tr ';' '\n' | xargs -P 4 -L1 bash -c 'prep $0 $1'
# HiPhase (HiFi only), one job at a time, 16 threads
for c in 10 20 30 40 50; do paths hifi $c; for in in snv_sv snv_indel_sv; do
  s=hp_${in}_hifi_${c}x_1; [[ -s $s.vcf.gz ]] && continue
  /usr/bin/time -v -o $s.time $HP --bam $B --vcf in_${in}_hifi_${c}x.vcf.gz --output-vcf $s.vcf.gz --reference $REF --threads 16 --ignore-read-groups \
      --stats-file $s.stats.csv --blocks-file $s.blocks.tsv > $s.log 2>&1 || echo "FAILED hiphase $s"
done; done
echo "$(date '+%F %T') hiphase done"
# WhatsHap, every run x input x chromosome, 20 jobs at a time
for r in $(echo "$RUNS" | tr ' ;' '_ '); do for in in snv_sv snv_indel_sv; do for i in $(seq 1 22); do echo "${r%_*} ${r#*_} $in chr$i"; done; done; done \
  | xargs -P 20 -L1 bash -c 'wh $0 $1 $2 $3'
for r in $(echo "$RUNS" | tr ' ;' '_ '); do pf=${r%_*}; c=${r#*_}; for in in snv_sv snv_indel_sv; do
  d=wh_${in}_${pf}_${c}x; out=wh_${in}_${pf}_${c}x_1.vcf
  ls $d/chr{1..22}.vcf > /dev/null 2>&1 || { echo "MISSING chromosomes $d"; continue; }
  # each job writes every record and phases only its chromosome: take chrN's records from chrN.vcf
  ( grep '^#' $d/chr1.vcf; for i in $(seq 1 22); do awk -F'\t' -v c=chr$i '!/^#/ && $1==c' $d/chr$i.vcf; done ) > $out
done; done
echo "$(date '+%F %T') all done"
