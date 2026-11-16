#!/bin/bash
# run_calls.sh: COLO829BL phasing benchmark, chr1-22, one chromosome at a time (session disk); same design as
# notes/hg008_validation/scripts/run_calls.sh except the caller (Clair3, author decision 2026-11-16).
# Reads: ONT open data colo829_2024.03, COLO829BL sup BAM PAU59807 (R10.4.1, 5 kHz, Dorado 0.5.2 sup@v4.3.0, aligned to
#   GRCh38 by ONT; PAU61427 not used), streamed per chromosome, reads with qs >= 10, MM/ML/mv tags dropped.
# Down-sampling: samtools view -s seed.fraction, fraction = target / chr1-22 mean depth (from samtools coverage of every
#   chromosome). The subsample keeps a read by a hash of its name and the seed, so per-chromosome subsets with one seed
#   are the genome-wide subset. 10x seeds 1-3, 20x seeds 1-3, 30x seed 1.
# Calls: Clair3 v1.2.0 (hkubal/clair3:v1.2.0) with ONT model r1041_e82_400bps_sup_v430 (Clair3 v2 cannot load it),
#   --platform ont, per chromosome; output GTs unphased (no --enable_phasing).
# Phasing: LongPhase 2 v2.1.2 release binary (GNN, threshold 0.35) | --disableGNN | WhatsHap 2.8 --only-snvs |
#   HapCUT2 1.3.4 extractHAIRS --ont 1 + HAPCUT2 on the PASS heterozygous SNVs.
set -uo pipefail
W=/home/user/work; cd $W; E=$W/tools/env/bin; export PATH=$E:$PATH
REF=$W/ref/GRCh38.fa; LP=$W/tools/longphase_linux-x64; T=${THREADS:-4}
SRC=https://ont-open-data.s3.amazonaws.com/colo829_2024.03/basecalls/colo829bl/sup/PAU59807.d052sup4305mCG_5hmCGvHg38.bam
RUNS=${RUNS:-"10x_1 10x_2 10x_3 20x_1 20x_2 20x_3 30x_1"}; CHRS=${CHRS:-$(seq 1 22)}
mkdir -p bam calls phase
X() { local o=$1; shift; [[ -e $o.done ]] && return 0; $E/time -v -o $o.time "$@" > $o.log 2>&1 && touch $o.done || echo "FAILED $o"; }
fetch() { local c=chr$1 F=bam/full.chr$1.bam
  [[ -s $F.bai ]] || { samtools view -u $SRC $c | samtools view -@2 -b -e '[qs] >= 10' -x MM -x ML -x mv -o $F.tmp - &&
    mv $F.tmp $F && samtools index $F; } || return 1
  [[ -s bam/cov.chr$1.tsv ]] || samtools coverage -r $c $F | tail -1 > bam/cov.chr$1.tsv; }
# Depth: streaming the whole BAM once only for depth would cost ~7 h, so the chr1-22 mean depth is estimated from the
#   remote index (samtools idxstats read counts per chromosome, scaled to the measured qs >= 10 depth of chr20, 59.302x):
#   51.895x. Each fetched chromosome's measured depth is written to bam/cov.chrN.tsv; the downsample fraction is the same
#   for every chromosome, as in a genome-wide run.
DEP=${DEP:-51.895}
echo "$(date '+%F %T') start; chr1-22 mean depth $DEP"
for i in $CHRS; do c=chr$i; F=bam/full.$c.bam
  ls phase/hc_*_$c.done 2>/dev/null | wc -l | grep -qx $(wc -w <<< "$RUNS") && continue
  echo "$(date '+%F %T') $c fetch"; fetch $i || { echo "FAILED fetch $c"; continue; }
  for run in $RUNS; do cv=${run%x_*}; s=${run#*x_}; B=bam/$c.${cv}x.$s.bam; V=calls/clair3_${run}_$c; o=${run}_$c
    fr=$(awk -v c=$cv -v d=$DEP 'BEGIN {printf "%.4f", c / d}' | cut -d. -f2)
    [[ -e phase/hc_$o.done ]] && continue
    [[ -s $B.bai ]] || { samtools view -b -s $s.$fr -o $B $F && samtools index $B; }
    [[ -s $V.vcf.gz ]] || { echo "$(date '+%F %T') $o clair3"
      $E/time -v -o $V.time docker run --rm -v $W:$W hkubal/clair3:v1.2.0 /opt/bin/run_clair3.sh --bam_fn=$W/$B \
        --ref_fn=$REF --threads=$T --platform=ont --model_path=$W/tools/models/r1041_e82_400bps_sup_v430 --ctg_name=$c \
        --sample_name=COLO829BL --output=$W/calls/clair3_$o.out > $V.log 2>&1 &&
        mv calls/clair3_$o.out/merge_output.vcf.gz $V.vcf.gz && mv calls/clair3_$o.out/merge_output.vcf.gz.tbi $V.vcf.gz.tbi &&
        rm -rf calls/clair3_$o.out || { echo "FAILED clair3 $o"; continue; }; }
    [[ -s $V.pass_het_snv.vcf ]] || zcat $V.vcf.gz | awk -F'\t' '/^#/ {print; next} $7 == "PASS" && length($4) == 1 && length($5) == 1 {
        split($10, g, ":"); if (g[1] ~ /^(0[\/|]1|1[\/|]0)$/) print}' > $V.pass_het_snv.vcf
    X phase/lp_gnn_$o $LP phase --ont -t $T -s $V.vcf.gz -b $B -r $REF -o phase/lp_gnn_$o
    X phase/lp_nognn_$o $LP phase --ont -t $T --disableGNN -s $V.vcf.gz -b $B -r $REF -o phase/lp_nognn_$o
    X phase/wh_$o whatshap phase --only-snvs --ignore-read-groups --reference=$REF -o phase/wh_$o.vcf $V.vcf.gz $B
    X phase/hc_frag_$o extractHAIRS --ont 1 --bam $B --ref $REF --VCF $V.pass_het_snv.vcf --out phase/hc_fragments_$o
    [[ -e phase/hc_frag_$o.done ]] && X phase/hc_$o HAPCUT2 --fragments phase/hc_fragments_$o --VCF $V.pass_het_snv.vcf --output phase/hapcut2_$o
    ls phase/{lp_gnn,lp_nognn,wh,hc}_$o.done > /dev/null 2>&1 && rm -f $B $B.bai phase/hc_fragments_$o
    echo "$(date '+%F %T') $o done"
  done
  ls phase/hc_*_$c.done 2>/dev/null | wc -l | grep -qx $(wc -w <<< "$RUNS") && rm -f $F $F.bai
done
echo "$(date '+%F %T') all done"
