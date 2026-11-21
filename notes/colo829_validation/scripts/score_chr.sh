#!/bin/bash
# score_chr.sh CHR: score every finished run of one chromosome against the COLO829BL truth (PS = truth block) with the
# paper's scorer, longphase compare of release v2.1 (sha256 21e4f0f8...), and independently with
# notes/benchmark_strata/score_phase.py (region 'all'; ISSUE1_REGIONS points to empty BEDs, as no GIAB regions apply).
set -uo pipefail
W=/home/user/work; cd $W; E=$W/tools/env/bin; c=$1; mkdir -p score
[[ -s truth/truth_$c.vcf ]] || $E/bcftools view -r $c -Ov -o truth/truth_$c.vcf truth/COLO829BL_truth.vcf.gz
for t in lp_gnn lp_nognn wh hapcut2; do for r in 10x_1 20x_1 30x_1; do
  f=phase/${t}_${r}_$c.vcf; [[ $t == hapcut2 ]] && f=phase/hapcut2_${r}_$c.phased.VCF; [[ -s $f ]] || continue
  b=score/${c}_${t}_$r
  [[ -s $b.tsv ]] || tools/lp21/longphase_linux-x64 compare -t 4 --ignore-sample-name truth/truth_$c.vcf $f -o $b > $b.log 2>&1 || echo "FAILED compare $b"
  [[ -s $b.sp.tsv ]] || ISSUE1_REGIONS=tools/regions_empty $E/python /home/user/longphase-2-paper/notes/benchmark_strata/score_phase.py truth/truth_$c.vcf $f $b.sp > $b.sp.log 2>&1 || echo "FAILED score_phase $b"
done; done
