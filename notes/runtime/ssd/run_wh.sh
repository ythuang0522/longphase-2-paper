#!/bin/bash
# README comparison: WhatsHap 2.8 --only-snvs (single-threaded) on the same data and disk as the README speed table
# (HG002 ONT R10.4.1 replicate 1, 10x-60x, inputs and outputs on ext4 nvme0, page cache dropped before every run,
# one run each), with the paper's command. Starts after the paper timing (run_a.sh) on an idle machine.
# Output is compared with the paper's WhatsHap VCF. times.tsv = build, coverage, run, wall s, user+sys CPU s, peak RSS GiB
set -uo pipefail
cd /home/twolinin/lp_ext4/bench_readme
I=/home/twolinin/lp_ext4/input; REF=$I/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
WH=/tmp/claude-1000/-disk-software-longphase/71da5d96-4a7e-438a-94f6-88eb87dc3db1/scratchpad/wsenv/bin/whatshap
until grep -q "all done" /ssd/longphase_process/v2.1.2/run_a.log; do sleep 60; done
cpu_idle() { local a b t=0 k; a=($(head -1 /proc/stat)); sleep 10; b=($(head -1 /proc/stat)); for k in 1 2 3 4 5 6 7 8; do t=$((t + b[k] - a[k])); done; (( (b[4] - a[4]) * 100 >= t * 95 )); }
idle() { while pgrep -x 'longphase_linux|whatshap|hiphase|sniffles' > /dev/null || ! cpu_idle; do sleep 5; done; }   # process names (no self-match), CPUs >= 95% idle over 10 s
mkdir -p out
for c in 10 20 30 40 50 60; do o=out/whatshap_${c}x_1; [[ -s $o.vcf ]] && continue
  idle
  docker run --rm --privileged ubuntu:22.04 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches' > /dev/null || { echo "FAILED drop_caches"; exit 1; }
  echo "$(date '+%F %T') $o"
  /usr/bin/time -v -o $o.time $WH phase --only-snvs --ignore-read-groups -o $o.tmp.vcf --reference=$REF $I/pepper_${c}x_1.vcf.gz $I/hg002.sup.${c}x.1.bam > $o.log 2>&1 \
    && mv $o.tmp.vcf $o.vcf || { echo "FAILED $o"; continue; }
  awk -v c=$c '/Elapsed/{split($NF,x,":"); w=(length(x)==3)?x[1]*3600+x[2]*60+x[3]:x[1]*60+x[2]}
      /User time/{u=$NF} /System time/{s=$NF} /Maximum resident/{m=$NF}
      END{printf "whatshap\t%s\t1\t%.1f\t%.1f\t%.2f\n", c, w, u+s, m/1048576}' $o.time >> times.tsv
  cmp -s <(grep -v '^##' $o.vcf) <(grep -v '^##' /disk/research/whatshap_v2.8/only/whatshap_v28_onlySNVs_${c}x_1.vcf) && echo "SAME $o vs paper" || echo "DIFF $o vs paper"
done
echo "$(date '+%F %T') all done"
