#!/bin/bash
# run_calls.sh: COLO829BL phasing benchmark, chr1-22, one chromosome at a time (session disk); same design as
# notes/hg008_validation/scripts/run_calls.sh except the caller (Clair3, author decision 2026-11-16).
# Reads: ONT open data colo829_2024.03, COLO829BL sup BAM PAU59807 (R10.4.1, 5 kHz, Dorado 0.5.2 sup@v4.3.0, aligned to
#   GRCh38 by ONT; PAU61427 not used), streamed per chromosome and run, reads with qs >= 10, MM/ML/mv tags dropped.
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
RUNS=${RUNS:-"10x_1 20x_1 30x_1"}; CHRS=${CHRS:-$(seq 1 22)}
mkdir -p bam calls phase
X() { local o=$1; shift; [[ -e $o.done ]] && return 0; $E/time -v -o $o.time "$@" > $o.log 2>&1 && touch $o.done || echo "FAILED $o"; }
# Reads per run: streamed from the remote BAM, qs >= 10, tags dropped, down-sampled and written as CRAM against the
#   paper's reference (no full-depth file is kept: chr1 at full depth would not fit this session's disk). On chr21 10x,
#   LongPhase 2, WhatsHap and HapCUT2 gave byte-identical output from this CRAM and from the BAM (2026-11-16).
# Depth: streaming the whole BAM once only for depth would cost ~7 h, so the chr1-22 mean depth is estimated from the
#   remote index (samtools idxstats read counts per chromosome, scaled to the measured qs >= 10 depth of chr20, 59.302x):
#   51.895x. Each run's measured depth is written to bam/cov.<run>_chrN.tsv; the downsample fraction is the same
#   for every chromosome, as in a genome-wide run.
DEP=${DEP:-51.895}
echo "$(date '+%F %T') start; chr1-22 mean depth $DEP"
for i in $CHRS; do c=chr$i
  ls phase/hc_[0-9]*_$c.done 2>/dev/null | wc -l | grep -qx $(wc -w <<< "$RUNS") && continue
  # two loops share the machine: a chromosome is claimed by the first loop to reach it (rm -r phase/claim_* on restart)
  mkdir phase/claim_$c 2>/dev/null || continue
  for run in $RUNS; do cv=${run%x_*}; s=${run#*x_}; B=bam/$c.${cv}x.$s.cram; V=calls/clair3_${run}_$c; o=${run}_$c
    fr=$(awk -v c=$cv -v d=$DEP 'BEGIN {printf "%.4f", c / d}' | cut -d. -f2)
    [[ -e phase/hc_$o.done ]] && continue
    [[ -s $B.crai ]] || { echo "$(date '+%F %T') $o fetch"
      samtools view -u $SRC $c | samtools view -@2 -C -T $REF -e '[qs] >= 10' -s $s.$fr -x MM -x ML -x mv -o $B.tmp - &&
      mv $B.tmp $B && samtools index $B && samtools coverage -r $c $B | tail -1 > bam/cov.$o.tsv || { echo "FAILED fetch $o"; continue; }; }
    # Clair3 per 20 Mb window (--bed_fn), windows concatenated: the session container restarts every 1-2 h, and a
    #   whole-chromosome call of chr1-10 takes longer than that. chr1 and chr18-22 were called per whole chromosome
    #   (2026-11-16, before the restarts began); calls near window edges may differ slightly.
    [[ -s $V.vcf.gz ]] || { echo "$(date '+%F %T') $o clair3"; ok=1; ws=""
      len=$(awk -v c=$c '$1 == c {print $2}' $REF.fai)
      for ((st = 0; st < len; st += 20000000)); do k=$((st / 20000000)); Vw=$V.w$k; ws="$ws $Vw.vcf.gz"
        [[ -s $Vw.vcf.gz ]] && continue
        printf '%s\t%d\t%d\n' $c $st $(( st + 20000000 < len ? st + 20000000 : len )) > $Vw.bed
        rm -rf calls/clair3_$o.w$k.out
        $E/time -v -o $Vw.time docker run --rm -v $W:$W hkubal/clair3:v1.2.0 /opt/bin/run_clair3.sh --bam_fn=$W/$B \
          --ref_fn=$REF --threads=$T --platform=ont --model_path=$W/tools/models/r1041_e82_400bps_sup_v430 --ctg_name=$c \
          --bed_fn=$W/$Vw.bed --sample_name=COLO829BL --output=$W/calls/clair3_$o.w$k.out > $Vw.log 2>&1 &&
          mv calls/clair3_$o.w$k.out/merge_output.vcf.gz $Vw.vcf.gz && rm -r calls/clair3_$o.w$k.out || { ok=0; break; }
      done
      # Clair3 reports a few calls just past a window's end (they reappear in the next window), so each window keeps
      #   only records with POS inside it (1-based st+1..end).
      [[ $ok == 1 ]] && { zcat $V.w0.vcf.gz | grep '^#'; for ((st = 0; st < len; st += 20000000)); do
          zcat $V.w$((st / 20000000)).vcf.gz | awk -F'\t' -v a=$((st + 1)) -v b=$((st + 20000000)) '!/^#/ && $2 >= a && $2 <= b'
        done; } | bgzip > $V.vcf.gz.tmp && mv $V.vcf.gz.tmp $V.vcf.gz && tabix -p vcf $V.vcf.gz &&
        rm -f $ws $V.w*.bed || { echo "FAILED clair3 $o"; continue; }; }
    [[ -s $V.pass_het_snv.vcf ]] || zcat $V.vcf.gz | awk -F'\t' '/^#/ {print; next} $7 == "PASS" && length($4) == 1 && length($5) == 1 {
        split($10, g, ":"); if (g[1] ~ /^(0[\/|]1|1[\/|]0)$/) print}' > $V.pass_het_snv.vcf
    X phase/lp_gnn_$o $LP phase --ont -t $T -s $V.vcf.gz -b $B -r $REF -o phase/lp_gnn_$o
    X phase/lp_nognn_$o $LP phase --ont -t $T --disableGNN -s $V.vcf.gz -b $B -r $REF -o phase/lp_nognn_$o
    X phase/wh_$o whatshap phase --only-snvs --ignore-read-groups --reference=$REF -o phase/wh_$o.vcf $V.vcf.gz $B
    X phase/hc_frag_$o extractHAIRS --ont 1 --bam $B --ref $REF --VCF $V.pass_het_snv.vcf --out phase/hc_fragments_$o
    [[ -e phase/hc_frag_$o.done ]] && X phase/hc_$o HAPCUT2 --fragments phase/hc_fragments_$o --VCF $V.pass_het_snv.vcf --output phase/hapcut2_$o
    ls phase/{lp_gnn,lp_nognn,wh,hc}_$o.done > /dev/null 2>&1 && rm -f $B $B.crai phase/hc_fragments_$o
    echo "$(date '+%F %T') $o done"
  done
done
echo "$(date '+%F %T') all done"
