#!/bin/bash
# score_all.sh: score the 28 HG008 phasing runs of run_calls.sh against truth/HG008N_v6.3_truth.vcf (make_truth.py: PS =
# truth phase block) with the paper's scorer, longphase compare of release v2.1 (blocks = truth PS x query PS pairs, so no
# pair crosses a truth block boundary), and independently with notes/benchmark_strata/score_phase.py (region 'all');
# then summarize.py -> score/hg008_runs.tsv. Waits for run_calls.sh "all done" and the truth VCF. Log logs/score.log.
set -uo pipefail
cd /disk/research/HG008
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
TRUTH=truth/HG008N_v6.3_truth.vcf; SP=/disk/software/longphase-2-paper/notes/benchmark_strata/score_phase.py
PY=/ssd/polyploid/env/bin/python
until grep -q "all done" logs/run_calls.log && grep -q "hc catchup done" logs/hc_catchup.log 2>/dev/null && [[ -s $TRUTH && -s truth/validated ]]; do sleep 300; done
mkdir -p score; echo "$(date '+%F %T') start"
for f in phase/lp_gnn_*x_[0-9].vcf phase/lp_nognn_*x_[0-9].vcf phase/wh_*x_[0-9].vcf phase/hapcut2_*x_[0-9].phased.VCF; do
  [[ -s $f ]] || { echo "missing $f"; continue; }
  b=score/sw_$(basename $f | sed 's/\.phased\.VCF$//; s/\.vcf$//')
  [[ -s $b.tsv ]] || $CMP compare -t 4 --ignore-sample-name $TRUTH $f -o $b > $b.log 2>&1 || echo "FAILED compare $f"
  [[ -s $b.sp.tsv ]] || $PY $SP $TRUTH $f $b.sp > $b.sp.log 2>&1 || echo "FAILED score_phase $f"
done
$PY summarize.py > logs/summarize.log 2>&1 && echo "$(date '+%F %T') all done" || echo "FAILED summarize"
