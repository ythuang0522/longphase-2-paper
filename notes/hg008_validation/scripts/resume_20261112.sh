#!/bin/bash
# resume_20261112.sh: the Claude session that launched run_calls.sh, hc_catchup.sh and score_all.sh ended about 07:20 on
# 2026-11-12 and its background jobs were killed with it; only the 20x_1 PEPPER container (4d5715c5bf2b, started 03:28 CST,
# --rm) survived, without its docker client, so run_calls.sh never moved its VCF. This waits for that container, records
# its wall time (container start to exit; /usr/bin/time was killed with the client) in calls/pepper_20x_1.time, moves the
# VCF as run_calls.sh would, then reruns run_calls.sh (finished steps are skipped by their .done files). Launched with
# setsid nohup together with hc_catchup.sh and score_all.sh. Log logs/resume.log.
set -uo pipefail
cd /disk/research/HG008
CID=4d5715c5bf2b; START=$(date -d 2026-11-11T19:28:27Z +%s); run=20x_1; V=calls/pepper_$run
echo "$(date '+%F %T') waiting for container $CID"
if docker inspect $CID > /dev/null 2>&1; then rc=$(docker wait $CID); else rc=gone; fi
END=$(date +%s); el=$((END - START))
echo "$(date '+%F %T') container exit $rc"
printf 'Elapsed (wall clock) time (h:mm:ss or m:ss): %d:%02d:%02d\n# container start to exit, recorded by resume_20261112.sh (exit %s)\n' \
  $((el / 3600)) $((el % 3600 / 60)) $((el % 60)) "$rc" > $V.time
if [[ -s calls/pepper_$run.out/pepper_$run.vcf.gz ]]; then
  mv calls/pepper_$run.out/pepper_$run.vcf.gz $V.vcf.gz && mv calls/pepper_$run.out/pepper_$run.vcf.gz.tbi $V.vcf.gz.tbi
else echo "$(date '+%F %T') FAILED: no VCF from $run (exit $rc); run_calls.sh will skip it"; fi
echo "$(date '+%F %T') restart run_calls.sh"
./run_calls.sh >> logs/run_calls.log 2>&1
echo "$(date '+%F %T') resume done"
