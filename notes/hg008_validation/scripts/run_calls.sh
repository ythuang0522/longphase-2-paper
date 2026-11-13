#!/bin/bash
# run_calls.sh: paper issue #11 minimum experiment, after align.sh. Seven inputs (10x seeds 1-3, 20x seeds 1-3, 30x seed 1)
# down-sampled from the full HG008-N-P alignment as the paper (samtools view -s seed.fraction; fraction = target / mean
# depth of chr1-22 from samtools coverage, 4 decimals), PEPPER-Margin-DeepVariant r0.8 --ont_r10_q20 on each (CPU: the
# image's PyTorch has no sm_120 kernels for the RTX 5090, as the HG005 calls), then four phasing configurations each with the
# paper's commands (/ssd/longphase_process/v2.1.2/run_a.sh, runtime/run_runtime.sh, hapcut2_v1.3.4/run_hapcut2.sh):
#   LongPhase 2 v2.1.2 release binary --ont -t 24 (frozen GNN, threshold 0.35 built in) | the same with --disableGNN |
#   WhatsHap 2.8 --only-snvs --ignore-read-groups --reference (workEnv whatshap-env) |
#   HapCUT2 1.3.4 extractHAIRS --ont 1 + HAPCUT2, on the PASS heterozygous SNVs of the PEPPER VCF (script-made subset).
# Every step is timed (/usr/bin/time -v); outputs in /disk/research/HG008/{bam,calls,phase}. Log logs/run_calls.log.
set -uo pipefail
cd /disk/research/HG008
REF=/disk/research/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
LP=/disk/software/longphase_v2.1.2_static/longphase_linux-x64; HC=/disk/software/HapCUT2/build
export LD_LIBRARY_PATH=/disk/software/HapCUT2/htslib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
RUNS=${RUNS:-"10x_1 10x_2 10x_3 20x_1 20x_2 20x_3 30x_1"}
until grep -q "align done" logs/align.log; do sleep 120; done
FULL=bam/HG008-N-P.full.bam; mkdir -p calls phase
DEP=$(awk '$1 ~ /^chr([1-9]|1[0-9]|2[0-2])$/ {s += $9 * ($3 - $2 + 1); l += $3 - $2 + 1} END {printf "%.3f", s / l}' bam/HG008-N-P.full.coverage.tsv)
echo "$(date '+%F %T') start; chr1-22 mean depth $DEP"
inwork() { docker exec -w /disk/research/HG008 workEnv bash -c "source /opt/miniconda/etc/profile.d/conda.sh; conda activate whatshap-env; $*"; }
for run in $RUNS; do c=${run%x_*}; s=${run#*x_}; B=bam/HG008-N-P.${c}x.$s.bam; V=calls/pepper_${run}
  fr=$(awk -v c=$c -v d=$DEP 'BEGIN {printf "%.4f", c / d}' | cut -d. -f2)
  [[ -s $B.bai ]] || { echo "$(date '+%F %T') $run view -s $s.$fr"; samtools view -@8 -b -s $s.$fr -o $B $FULL && samtools index -@8 $B; }
  [[ -s $V.vcf.gz ]] || { echo "$(date '+%F %T') $run pepper"
    /usr/bin/time -v -o $V.time docker run --rm -v /disk/research:/disk/research kishwars/pepper_deepvariant:r0.8-gpu \
      run_pepper_margin_deepvariant call_variant -b /disk/research/HG008/$B -f $REF -o /disk/research/HG008/calls/pepper_$run.out \
      -p pepper_$run -t 32 --ont_r10_q20 > $V.log 2>&1 && mv calls/pepper_$run.out/pepper_$run.vcf.gz $V.vcf.gz &&
      mv calls/pepper_$run.out/pepper_$run.vcf.gz.tbi $V.vcf.gz.tbi || { echo "FAILED pepper $run"; continue; }; }
  # HapCUT2 input: PASS heterozygous SNVs (single-base REF and ALT, GT 0/1 or 1/0 or 0|1 or 1|0)
  [[ -s $V.pass_het_snv.vcf ]] || zcat $V.vcf.gz | awk -F'\t' '/^#/ {print; next} $7 == "PASS" && length($4) == 1 && length($5) == 1 {
      split($10, g, ":"); if (g[1] ~ /^(0[\/|]1|1[\/|]0)$/) print}' > $V.pass_het_snv.vcf
  T() { local o=$1; shift; [[ -e $o.done ]] && return 0; /usr/bin/time -v -o $o.time "$@" > $o.log 2>&1 && touch $o.done || echo "FAILED $o"; }
  echo "$(date '+%F %T') $run phase"
  T phase/lp_gnn_$run $LP phase --ont -t 24 -s $V.vcf.gz -b $B -r $REF -o phase/lp_gnn_$run
  T phase/lp_nognn_$run $LP phase --ont -t 24 --disableGNN -s $V.vcf.gz -b $B -r $REF -o phase/lp_nognn_$run
  [[ -e phase/wh_$run.done ]] || { inwork "/usr/bin/time -v -o phase/wh_$run.time whatshap phase --only-snvs --ignore-read-groups --reference=$REF -o phase/wh_$run.vcf $V.vcf.gz $B > phase/wh_$run.log 2>&1" && touch phase/wh_$run.done || echo "FAILED wh $run"; }
  T phase/hc_frag_$run $HC/extractHAIRS --ont 1 --bam $B --ref $REF --VCF $V.pass_het_snv.vcf --out phase/hc_fragments_$run
  [[ -e phase/hc_frag_$run.done ]] && T phase/hc_$run $HC/HAPCUT2 --fragments phase/hc_fragments_$run --VCF $V.pass_het_snv.vcf --output phase/hapcut2_$run
  echo "$(date '+%F %T') $run done"
done
echo "$(date '+%F %T') all done"
