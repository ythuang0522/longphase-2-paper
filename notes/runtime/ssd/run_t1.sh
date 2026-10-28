#!/bin/bash
# README comparison: LongPhase v2.1.2 (static release binary) phase --ont -t 1, same data, disk and protocol as
# run.sh / run_wh.sh (page cache dropped before every run, one run each). Starts after run_wh.sh on an idle machine.
# Output is compared with the -t 24 output. times.tsv rows: static_t1, coverage, run, wall s, CPU s, peak RSS GiB
set -uo pipefail
cd /home/twolinin/lp_ext4/bench_readme
I=/home/twolinin/lp_ext4/input; REF=$I/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
until grep -q "all done" run_wh.log; do sleep 60; done
cpu_idle() { local a b t=0 k; a=($(head -1 /proc/stat)); sleep 10; b=($(head -1 /proc/stat)); for k in 1 2 3 4 5 6 7 8; do t=$((t + b[k] - a[k])); done; (( (b[4] - a[4]) * 100 >= t * 95 )); }
idle() { while pgrep -x 'longphase_linux|longphase_stati|whatshap|hiphase|sniffles' > /dev/null || ! cpu_idle; do sleep 5; done; }
for c in 10 20 30 40 50 60; do o=out/static_t1_${c}x_1; [[ -s $o.vcf ]] && continue
  idle
  docker run --rm --privileged ubuntu:22.04 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches' > /dev/null || { echo "FAILED drop_caches"; exit 1; }
  echo "$(date '+%F %T') $o"
  /usr/bin/time -v -o $o.time ./longphase_static phase --ont -t 1 -r $REF -s $I/pepper_${c}x_1.vcf.gz -b $I/hg002.sup.${c}x.1.bam -o $o > $o.log 2>&1 || { echo "FAILED $o"; continue; }
  awk -v c=$c '/Elapsed/{split($NF,x,":"); w=(length(x)==3)?x[1]*3600+x[2]*60+x[3]:x[1]*60+x[2]}
      /User time/{u=$NF} /System time/{s=$NF} /Maximum resident/{m=$NF}
      END{printf "static_t1\t%s\t1\t%.1f\t%.1f\t%.2f\n", c, w, u+s, m/1048576}' $o.time >> times.tsv
  cmp -s <(grep -v '^##' $o.vcf) <(grep -v '^##' out/static_${c}x_1.vcf) && echo "SAME $o vs -t 24" || echo "DIFF $o vs -t 24"
done
echo "$(date '+%F %T') all done"
