#!/bin/bash
# hc_catchup.sh: run_calls.sh (as launched 2026-11-10) never ran the HAPCUT2 step: it gated it on [[ -s hc_frag_$run.done ]]
# but .done files are empty (touch), so the test is always false and the step was skipped silently. This runs the same
# HAPCUT2 command, timed the same way, for every run whose extractHAIRS step is done, until run_calls.sh logs "all done".
# Log logs/hc_catchup.log; ends with "hc catchup done" (score_all.sh waits for it).
set -uo pipefail
cd /disk/research/HG008
HC=/disk/software/HapCUT2/build
export LD_LIBRARY_PATH=/disk/software/HapCUT2/htslib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
RUNS="10x_1 10x_2 10x_3 20x_1 20x_2 20x_3 30x_1"
while :; do
  fin=0; grep -q "all done" logs/run_calls.log && fin=1
  for run in $RUNS; do o=phase/hc_$run; V=calls/pepper_$run
    [[ -e phase/hc_frag_$run.done && ! -e $o.done ]] || continue
    echo "$(date '+%F %T') $run HAPCUT2"
    /usr/bin/time -v -o $o.time $HC/HAPCUT2 --fragments phase/hc_fragments_$run --VCF $V.pass_het_snv.vcf --output phase/hapcut2_$run > $o.log 2>&1 && touch $o.done || echo "FAILED $o"
  done
  [[ $fin == 1 ]] && break; sleep 120
done
echo "$(date '+%F %T') hc catchup done"
