#!/bin/bash
# Paper rerun with LongPhase v2.1.2 (release binary, tree 95bf4f7 = develop 55e98cc), untimed part.
# HG002 nanopore: 64 runs (10-20x replicates 1-10, 30-60x replicate 1); HiFi: replicate 1 at 10-50x.
# Per BAM, while it is in the page cache:
#   1. Sniffles 2.8.0 with --reference (and --output-rnames, as the earlier calls)
#   2. nanopore only: longphase modcall v2.1.2 with the PEPPER SNP file (-s), as the paper's modcall VCFs
#   3. phase, with GNN and with --disableGNN: nanopore methyl, indel_methyl, sv, indel_sv, all
#      (the co-phasing configurations that take SVs or 5mC); HiFi sv and indel_sv (issue #10)
# SNV-only and SNV+indel phasing are not rerun here: without an SV file the output is identical to v2.1.1.
# Outputs on /disk/research/v2.1.2 (final location; /ssd has no room for 700 runs), logs with /usr/bin/time -v.
set -uo pipefail
R=/disk/research; P=$R/pacbio; REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
O=$R/v2.1.2
LP=/disk/software/longphase_v2.1.2_static/longphase_linux-x64
SN=/tmp/claude-1000/-disk-software-longphase/71da5d96-4a7e-438a-94f6-88eb87dc3db1/scratchpad/snenv/bin/sniffles
mkdir -p $O/sniffles $O/methyl $O/pacbio/sniffles
declare -A DIR=([methyl]=longphase_coh_methyl [indel_methyl]=longphase_coh_indel_methyl [sv]=longphase_coh_sv
                [indel_sv]=longphase_coh_indel_sv [all]=longphase_cophasing)
lp() {  # platform config run gnn(yes/no)
  local pf=$1 m=$2 run=$3 g=$4 c=${3%x_*} i=${3#*x_} extra="" d B V S M out
  if [[ $pf == ont ]]; then
    B=$R/bam/hg002.sup.${c}x.${i}.bam; V=$R/pepper_calling/pepper_$run.vcf.gz; S=$O/sniffles/sniffles_$run.vcf; M=$O/methyl/modcall_$run.vcf
    d=${DIR[$m]}; out=$O/${d}$([[ $g == yes ]] && echo _gnn)/${d}$([[ $g == yes ]] && echo _gnn)_$run
  else
    B=$P/bam/hg002.hifi.${c}x.1.bam; V=$P/pepper_calling/pepper_hifi_${c}x.vcf.gz; S=$O/pacbio/sniffles/sniffles_hifi_${c}x.vcf
    d=longphase_hifi_$m; out=$O/pacbio/${d}$([[ $g == yes ]] && echo _gnn)/${d}$([[ $g == yes ]] && echo _gnn)_${c}x_1
  fi
  case $m in
    methyl) extra="--mod-file $M";; indel_methyl) extra="--indels --mod-file $M";;
    sv) extra="--sv-file $S";; indel_sv) extra="--indels --sv-file $S";; all) extra="--indels --sv-file $S --mod-file $M";;
  esac
  [[ $g == no ]] && extra="$extra --disableGNN"
  mkdir -p $(dirname $out)
  [[ -s $out.vcf ]] && return
  /usr/bin/time -v $LP phase --$([[ $pf == ont ]] && echo ont || echo pb) -t 12 -s $V -b $B -r $REF $extra -o $out.tmp > $out.log 2>&1 \
    || { echo "FAILED phase $pf $m $run $g"; return; }
  for f in $out.tmp*.vcf; do mv $f ${f/.tmp/}; done
}
export -f lp; export R P REF O LP DIR_S="$(declare -p DIR)"
one() {  # platform run
  local pf=$1 run=$2 c=${2%x_*} i=${2#*x_} B S
  if [[ $pf == ont ]]; then B=$R/bam/hg002.sup.${c}x.${i}.bam; S=$O/sniffles/sniffles_$run.vcf
  else B=$P/bam/hg002.hifi.${c}x.1.bam; S=$O/pacbio/sniffles/sniffles_hifi_${c}x.vcf; fi
  [[ -s $S ]] || { /usr/bin/time -v $SN --threads 16 --output-rnames --reference $REF --input $B --vcf $S.tmp.vcf > ${S%.vcf}.log 2>&1 \
                   && mv $S.tmp.vcf $S || { echo "FAILED sniffles $pf $run"; return; }; }
  if [[ $pf == ont ]]; then
    local M=$O/methyl/modcall_$run
    [[ -s $M.vcf ]] || { /usr/bin/time -v $LP modcall -t 16 -b $B -r $REF -s $R/pepper_calling/pepper_$run.vcf.gz -o $M.tmp > $M.log 2>&1 \
                         && mv $M.tmp.vcf $M.vcf || { echo "FAILED modcall $run"; return; }; }
    for m in sv indel_sv all methyl indel_methyl; do for g in yes no; do echo "ont $m $run $g"; done; done
  else
    for m in sv indel_sv; do for g in yes no; do echo "hifi $m $run $g"; done; done
  fi | xargs -P 2 -L1 bash -c 'eval "$DIR_S"; lp $0 $1 $2 $3'
  echo "$(date '+%F %T') done $pf $run"
}
export -f one; export SN
echo "$(date '+%F %T') start"
# HiFi first (issue #10 needs it and it is short), then nanopore replicate 1 (issue #10), then the other replicates
( for c in 10 20 30 40 50; do echo "hifi ${c}x_1"; done ) | xargs -P 2 -L1 bash -c 'one $0 $1'
( for c in 10 12 14 16 18 20; do echo "ont ${c}x_1"; done ) | xargs -P 2 -L1 bash -c 'one $0 $1'
( for c in 30 40 50 60; do echo "ont ${c}x_1"; done ) | xargs -P 1 -L1 bash -c 'one $0 $1'
echo "$(date '+%F %T') replicate 1 done"
( for c in 10 12 14 16 18 20; do for r in 2 3 4 5 6 7 8 9 10; do echo "ont ${c}x_$r"; done; done ) | xargs -P 2 -L1 bash -c 'one $0 $1'
echo "$(date '+%F %T') all done"
