#!/bin/bash
# README speed table for v2.1.2: phase --ont -t 24, SNVs only, HG002 ONT R10.4.1 replicate 1, 10x-60x.
# Inputs and outputs on ext4 (nvme0, Crucial T710 4 TB); page cache dropped before every run; one run each
# with the release (static) binary built from 95bf4f7 (= develop 55e98cc).
# times.tsv = build, coverage, run, wall s, user+sys CPU s, peak RSS GiB
set -uo pipefail
cd /home/twolinin/lp_ext4/bench_readme
I=/home/twolinin/lp_ext4/input; REF=$I/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
declare -A BIN=([static]=/disk/software/longphase_v2.1.2_static/longphase_linux-x64 [dyn]=/ssd/longphase_process/speedup/longphase_v212dyn)
cp ${BIN[static]} ./longphase_static; cp ${BIN[dyn]} ./longphase_dyn; BIN=([static]=./longphase_static [dyn]=./longphase_dyn)
one(){ b=$1 c=$2 r=$3; o=out/${b}_${c}x_$r; mkdir -p out
  docker run --rm --privileged ubuntu:22.04 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches' > /dev/null || { echo "FAILED drop_caches"; exit 1; }
  echo "$(date '+%F %T') $o"
  /usr/bin/time -v -o $o.time ${BIN[$b]} phase --ont -t 24 -r $REF -s $I/pepper_${c}x_1.vcf.gz -b $I/hg002.sup.${c}x.1.bam -o $o > $o.log 2>&1 || { echo "FAILED $o"; return; }
  awk -v b=$b -v c=$c -v r=$r '/Elapsed/{split($NF,x,":"); w=(length(x)==3)?x[1]*3600+x[2]*60+x[3]:x[1]*60+x[2]}
      /User time/{u=$NF} /System time/{s=$NF} /Maximum resident/{m=$NF}
      END{printf "%s\t%s\t%s\t%.1f\t%.1f\t%.2f\n", b, c, r, w, u+s, m/1048576}' $o.time >> times.tsv; }
until grep -q "copy3 finished" $I/copy3.log; do sleep 30; done
for c in 10 20 30 40 50 60; do
  one static $c 1
done
echo "$(date '+%F %T') all done"
