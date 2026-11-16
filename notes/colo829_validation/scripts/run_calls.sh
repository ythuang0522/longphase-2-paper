#!/bin/bash
# run_calls.sh: COLO829BL chr20 phasing runs, same design as notes/hg008_validation/scripts/run_calls.sh.
# Reads: ONT open data colo829_2024.03, COLO829BL sup BAMs PAU59807 + PAU61427 (R10.4.1, 5 kHz, Dorado 0.5.2
# sup@v4.3.0, aligned to GRCh38 by ONT), chr20 only, reads with qs >= 10. Down-sampled as the paper (view -s seed.fraction,
# fraction = target / chr20 mean depth). PEPPER-Margin-DeepVariant r0.8 --ont_r10_q20 per down-sample (CPU), then
# LongPhase 2 v2.1.2 release binary (GNN, threshold 0.35) | --disableGNN | WhatsHap 2.8 --only-snvs | HapCUT2 1.3.4 --ont 1.
set -uo pipefail
W=/home/user/work; cd $W; E=$W/tools/env/bin; export PATH=$E:$PATH
REF=$W/ref/GRCh38.fa; LP=$W/tools/longphase_linux-x64; T=${THREADS:-4}
RUNS=${RUNS:-"10x_1 10x_2 10x_3 20x_1 20x_2 20x_3 30x_1"}
mkdir -p calls phase
FULL=bam/COLO829BL.chr20.bam
if [[ ! -s $FULL.bai ]]; then
  samtools merge -@$T -f -o bam/merged.tmp.bam bam/PAU59807.chr20.bam bam/PAU61427.chr20.bam &&
  samtools view -@$T -b -e '[qs] >= 10' -o $FULL bam/merged.tmp.bam && samtools index -@$T $FULL && rm bam/merged.tmp.bam
  samtools coverage -r chr20 $FULL > bam/COLO829BL.chr20.coverage.tsv
fi
DEP=$(awk 'NR == 2 {print $7}' bam/COLO829BL.chr20.coverage.tsv)
echo "$(date '+%F %T') start; chr20 mean depth $DEP"
for run in $RUNS; do c=${run%x_*}; s=${run#*x_}; B=bam/COLO829BL.chr20.${c}x.$s.bam; V=calls/pepper_${run}
  fr=$(awk -v c=$c -v d=$DEP 'BEGIN {printf "%.4f", c / d}' | cut -d. -f2)
  [[ -s $B.bai ]] || { echo "$(date '+%F %T') $run view -s $s.$fr"; samtools view -@$T -b -s $s.$fr -o $B $FULL && samtools index $B; }
  [[ -s $V.vcf.gz ]] || { echo "$(date '+%F %T') $run pepper"
    /usr/bin/time -v -o $V.time docker run --rm -v $W:$W kishwars/pepper_deepvariant:r0.8 \
      run_pepper_margin_deepvariant call_variant -b $W/$B -f $REF -o $W/calls/pepper_$run.out -r chr20 \
      -p pepper_$run -t $T --ont_r10_q20 > $V.log 2>&1 && mv calls/pepper_$run.out/pepper_$run.vcf.gz $V.vcf.gz &&
      mv calls/pepper_$run.out/pepper_$run.vcf.gz.tbi $V.vcf.gz.tbi && rm -rf calls/pepper_$run.out || { echo "FAILED pepper $run"; continue; }; }
  [[ -s $V.pass_het_snv.vcf ]] || zcat $V.vcf.gz | awk -F'\t' '/^#/ {print; next} $7 == "PASS" && length($4) == 1 && length($5) == 1 {
      split($10, g, ":"); if (g[1] ~ /^(0[\/|]1|1[\/|]0)$/) print}' > $V.pass_het_snv.vcf
  X() { local o=$1; shift; [[ -e $o.done ]] && return 0; /usr/bin/time -v -o $o.time "$@" > $o.log 2>&1 && touch $o.done || echo "FAILED $o"; }
  echo "$(date '+%F %T') $run phase"
  X phase/lp_gnn_$run $LP phase --ont -t $T -s $V.vcf.gz -b $B -r $REF -o phase/lp_gnn_$run
  X phase/lp_nognn_$run $LP phase --ont -t $T --disableGNN -s $V.vcf.gz -b $B -r $REF -o phase/lp_nognn_$run
  X phase/wh_$run whatshap phase --only-snvs --ignore-read-groups --reference=$REF -o phase/wh_$run.vcf $V.vcf.gz $B
  X phase/hc_frag_$run extractHAIRS --ont 1 --bam $B --ref $REF --VCF $V.pass_het_snv.vcf --out phase/hc_fragments_$run
  [[ -e phase/hc_frag_$run.done ]] && X phase/hc_$run HAPCUT2 --fragments phase/hc_fragments_$run --VCF $V.pass_het_snv.vcf --output phase/hapcut2_$run
  echo "$(date '+%F %T') $run done"
done
echo "$(date '+%F %T') all done"
