#!/bin/bash
# restart the COLO829BL run after a container restart
cd /home/user/work
pgrep -x dockerd > /dev/null || { rm -f /var/run/docker.pid /var/run/docker/containerd/containerd.pid; nohup dockerd > logs/dockerd.log 2>&1 & }
for i in $(seq 60); do docker info > /dev/null 2>&1 && break; sleep 2; done
docker info > /dev/null 2>&1 || { echo "dockerd not up"; exit 1; }
for d in calls/*.out; do [[ -d $d ]] && rm -r "$d"; done
rm -f bam/*.tmp; rm -rf phase/claim_*
S=/home/user/longphase-2-paper/notes/colo829_validation/scripts/run_calls.sh
THREADS=2 CHRS=7 RUNS="10x_1 20x_1" nohup bash $S >> logs/run_calls.log 2>&1 &
sleep 3
THREADS=2 CHRS=7 RUNS=30x_1 nohup bash $S >> logs/run_calls_b.log 2>&1 &
nohup bash auto_score.sh >> logs/auto_score.log 2>&1 &
nohup bash compress_loop.sh > logs/compress.log 2>&1 &
echo restarted
