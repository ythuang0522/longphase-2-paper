#!/bin/bash
# score_genome.sh: genome-wide (chr1-22) scoring of every tool x run, once all 22 chromosomes are scored per chromosome
# (score_chr.sh). Per tool and run, the 22 per-chromosome phaser outputs are concatenated in chromosome order and scored
# against the whole truth VCF with the same two scorers as score_chr.sh (longphase compare of release v2.1, score_phase.py).
# Genome-wide block count and N50 come from this run; switch errors and phased SNVs must equal the per-chromosome sums
# (summarize.py checks it).
set -uo pipefail
W=/home/user/work; cd $W; E=$W/tools/env/bin; mkdir -p genome
[[ -s truth/COLO829BL_truth.vcf ]] || zcat truth/COLO829BL_truth.vcf.gz > truth/COLO829BL_truth.vcf
for t in lp_gnn lp_nognn wh hapcut2; do for r in 10x_1 20x_1 30x_1; do
  q=genome/${t}_$r.vcf; b=genome/${t}_$r
  if [[ ! -s $q ]]; then fs=""
    for i in $(seq 1 22); do c=chr$i
      f=phase/${t}_${r}_$c.vcf.gz; [[ $t == hapcut2 ]] && f=phase/hapcut2_${r}_$c.phased.VCF.gz
      [[ -s $f ]] || f=${f%.gz}; [[ -s $f ]] || { echo "MISSING $t $r $c"; exit 1; }; fs="$fs $f"
    done
    $E/bcftools concat -Ov -o $q.tmp $fs && mv $q.tmp $q || { echo "FAILED concat $t $r"; exit 1; }
  fi
  [[ -s $b.tsv ]] || tools/lp21/longphase_linux-x64 compare -t 4 --ignore-sample-name truth/COLO829BL_truth.vcf $q -o $b > $b.log 2>&1 || echo "FAILED compare $b"
  [[ -s $b.sp.tsv ]] || ISSUE1_REGIONS=tools/regions_empty $E/python /home/user/longphase-2-paper/notes/benchmark_strata/score_phase.py truth/COLO829BL_truth.vcf $q $b.sp > $b.sp.log 2>&1 || echo "FAILED score_phase $b"
  echo "$(date '+%F %T') $t $r scored"
done; done
