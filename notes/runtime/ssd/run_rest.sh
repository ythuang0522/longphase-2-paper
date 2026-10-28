#!/bin/bash
# Rest of run_all.sh after 2026-10-27 22:40: the user chose to keep the paper's HapCUT2 times where ext4 matched them
# (same input: 10, 14, 16, 18x within 2.5%), so HapCUT2 60x and HiFi are not re-timed. Finishes the running HapCUT2 50x
# (its time row is written here), then the WhatsHap runs that have no ext4 time (nanopore 12-18x, HiFi 10-50x).
set -uo pipefail
cd /home/twolinin/lp_ext4/bench_readme
I=/home/twolinin/lp_ext4/input; REF=$I/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa; R=/disk/research; P=$R/pacbio
WH=/tmp/claude-1000/-disk-software-longphase/71da5d96-4a7e-438a-94f6-88eb87dc3db1/scratchpad/wsenv/bin/whatshap
H=/disk/software/HapCUT2/build; export LD_LIBRARY_PATH=/disk/software/HapCUT2/htslib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
cpu_idle() { local a b t=0 k; a=($(head -1 /proc/stat)); sleep 10; b=($(head -1 /proc/stat)); for k in 1 2 3 4 5 6 7 8; do t=$((t + b[k] - a[k])); done; (( (b[4] - a[4]) * 100 >= t * 95 )); }
idle() { while pgrep -x 'longphase_linux|longphase_stati|whatshap|hiphase|sniffles|extractHAIRS|HAPCUT2' > /dev/null || ! cpu_idle; do sleep 5; done; }
one() { local lab=$1 c=$2 o=$3; shift 3
  idle
  docker run --rm --privileged ubuntu:22.04 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches' > /dev/null || { echo "FAILED drop_caches"; exit 1; }
  echo "$(date '+%F %T') $o"
  /usr/bin/time -v -o $o.time "$@" > $o.log 2>&1 || { echo "FAILED $o"; return 1; }
  awk -v l=$lab -v c=$c '/Elapsed/{split($NF,x,":"); w=(length(x)==3)?x[1]*3600+x[2]*60+x[3]:x[1]*60+x[2]}
      /User time/{u=$NF} /System time/{s=$NF} /Maximum resident/{m=$NF}
      END{printf "%s\t%s\t1\t%.1f\t%.1f\t%.2f\n", l, c, w, u+s, m/1048576}' $o.time >> times.tsv; }
same() { cmp -s <(grep -v '^##' $1) <(grep -v '^##' $2) && echo "SAME $1 vs $2" || echo "DIFF $1 vs $2"; }
while kill -0 484037 2>/dev/null; do sleep 30; done
o=out/hapcut2_50x_1
if [[ -s $o.phased.VCF ]]; then awk -v c=50 '/Elapsed/{split($NF,x,":"); w=(length(x)==3)?x[1]*3600+x[2]*60+x[3]:x[1]*60+x[2]}
  /User time/{u=$NF} /System time/{s=$NF} /Maximum resident/{m=$NF}
  END{printf "hapcut2\t%s\t1\t%.1f\t%.1f\t%.2f\n", c, w, u+s, m/1048576}' $o.time >> times.tsv; echo "NOREF $o (no paper VCF from the same input)"; else echo "FAILED $o"; fi
rm -f $o.frag
# ---- WhatsHap (hours) ----
for c in 12 14 16 18; do o=out/whatshap_${c}x_1; [[ -s $o.vcf ]] && continue
  one whatshap $c $o $WH phase --only-snvs --ignore-read-groups -o $o.tmp.vcf --reference=$REF $I/pepper_${c}x_1.vcf.gz $I/hg002.sup.${c}x.1.bam \
    && mv $o.tmp.vcf $o.vcf && same $o.vcf $R/whatshap_v2.8/only/whatshap_v28_onlySNVs_${c}x_1.vcf; done
for c in 10 20 30 40 50; do o=out/hifi_whatshap_${c}x_1; [[ -s $o.vcf ]] && continue
  one hifi_whatshap $c $o $WH phase --only-snvs --ignore-read-groups -o $o.tmp.vcf --reference=$REF $I/pepper_hifi_${c}x.vcf.gz $I/hg002.hifi.${c}x.1.bam \
    && mv $o.tmp.vcf $o.vcf && same $o.vcf $P/whatshap_v28_hifi_onlySNVs_${c}x_1.vcf; done
echo "$(date '+%F %T') all done"
