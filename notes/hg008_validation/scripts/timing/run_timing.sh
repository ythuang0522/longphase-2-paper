#!/bin/bash
# run_timing.sh: HG008 runtime with the paper's SSD protocol (notes/log/2026-10-28-runtime-ssd.md, notes/runtime/ssd/run_all.sh):
# inputs and outputs on ext4 nvme0 (/home/twolinin/lp_ext4/hg008), one run at a time on an idle machine, page cache dropped
# before every run, one run each, /usr/bin/time -v. Seed 1 at 10, 20, 30x (as the paper's replicate 1). Per coverage:
# LongPhase v2.1.2 static release -t 24 (GNN), -t 24 --disableGNN, -t 1 (GNN); WhatsHap 2.8 --only-snvs (1 thread);
# HapCUT2 1.3.4 extractHAIRS --ont 1 + HAPCUT2 timed together, input = the same calls as the other tools minus the records
# HapCUT2 rejects (GT not two alleles from {0,1,2}), as the paper's SSD runs. Outputs are compared with the accuracy runs
# (/disk/research/HG008/phase) where the input is the same. The polyploid jobs (session of
# /ssd/polyploid/potato/pavk/resume_20261112.sh) are paused for the timing: only their bash/xargs drivers get SIGSTOP, so the
# step running in each finishes normally (its own time and 6 h timeout untouched) and no new step starts; SIGCONT on exit.
# times.tsv = label, coverage, run, wall s, user+sys CPU s, peak RSS GiB. Log run_timing.log (next to this script).
set -uo pipefail
W=/home/twolinin/lp_ext4/hg008; I=$W/input; cd $W
R=/disk/research/HG008; REF=/home/twolinin/lp_ext4/input/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
WH=/tmp/claude-1000/-disk-software-longphase/71da5d96-4a7e-438a-94f6-88eb87dc3db1/scratchpad/wsenv/bin/whatshap
H=/disk/software/HapCUT2/build; export LD_LIBRARY_PATH=/disk/software/HapCUT2/htslib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
LP=$W/longphase_static; COV="10 20 30"
cpu_idle() { local a b t=0 k; a=($(head -1 /proc/stat)); sleep 10; b=($(head -1 /proc/stat)); for k in 1 2 3 4 5 6 7 8; do t=$((t + b[k] - a[k])); done; (( (b[4] - a[4]) * 100 >= t * 95 )); }
idle() { while pgrep -x 'longphase_linux|longphase_stati|whatshap|hiphase|sniffles|extractHAIRS|HAPCUT2' > /dev/null || ! cpu_idle; do sleep 5; done; }

# ---- inputs (untimed, polyploid still running) ----
cpin() { [[ -s $I/$2 ]] || { echo "$(date '+%F %T') copy $2"; cp -L $1 $I/$2.tmp && mv $I/$2.tmp $I/$2; }; }
[[ -x $LP ]] || cp /disk/software/longphase_v2.1.2_static/longphase_linux-x64 $LP
cmp -s $LP /disk/software/longphase_v2.1.2_static/longphase_linux-x64 || { echo "binary differs"; exit 1; }
for c in $COV; do
  cpin $R/bam/HG008-N-P.${c}x.1.bam ${c}x_1.bam; cpin $R/bam/HG008-N-P.${c}x.1.bam.bai ${c}x_1.bam.bai
  cpin $R/calls/pepper_${c}x_1.vcf.gz ${c}x_1.vcf.gz; cpin $R/calls/pepper_${c}x_1.vcf.gz.tbi ${c}x_1.vcf.gz.tbi
  [[ -s $I/hapcut_${c}x_1.vcf ]] || zcat $I/${c}x_1.vcf.gz | awk -F'\t' '/^#/ || $10 ~ /^[012][\/|][012](:|$)/' > $I/hapcut_${c}x_1.vcf
done
touch $I/*.bai $I/*.tbi
echo "$(date '+%F %T') inputs ready"

# ---- pause the polyploid drivers ----
PIDS=$(ps -eo pid=,sid=,comm= | awk '$2 == 370144 && $3 ~ /(\.sh$|^resume_|^xargs$|^bash$)/ {print $1}' | tr '\n' ' ')
resume() { [[ -n $PIDS ]] && kill -CONT $PIDS 2> /dev/null; echo "$(date '+%F %T') polyploid resumed: $PIDS"; }
trap resume EXIT; trap 'exit 1' INT TERM
[[ -n $PIDS ]] && kill -STOP $PIDS; echo "$(date '+%F %T') polyploid drivers paused: $PIDS"

one() { local lab=$1 c=$2 o=$3; shift 3
  idle
  docker run --rm --privileged ubuntu:22.04 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches' > /dev/null || { echo "FAILED drop_caches"; exit 1; }
  echo "$(date '+%F %T') $o"
  /usr/bin/time -v -o $o.time "$@" > $o.log 2>&1 || { echo "FAILED $o"; return 1; }
  awk -v l=$lab -v c=$c '/Elapsed/{split($NF,x,":"); w=(length(x)==3)?x[1]*3600+x[2]*60+x[3]:x[1]*60+x[2]}
      /User time/{u=$NF} /System time/{s=$NF} /Maximum resident/{m=$NF}
      END{printf "%s\t%s\t1\t%.1f\t%.1f\t%.2f\n", l, c, w, u+s, m/1048576}' $o.time >> times.tsv; }
same() { cmp -s <(grep -v '^##' $1) <(grep -v '^##' $2) && echo "SAME $1 vs $2" || echo "DIFF $1 vs $2"; }
mkdir -p out
for c in $COV; do B=$I/${c}x_1.bam; V=$I/${c}x_1.vcf.gz
  o=out/lp_gnn_${c}x_1; [[ -s $o.vcf ]] || { one lp_gnn_t24 $c $o $LP phase --ont -t 24 -r $REF -s $V -b $B -o $o && same $o.vcf $R/phase/lp_gnn_${c}x_1.vcf; }
  o=out/lp_nognn_${c}x_1; [[ -s $o.vcf ]] || { one lp_nognn_t24 $c $o $LP phase --ont -t 24 --disableGNN -r $REF -s $V -b $B -o $o && same $o.vcf $R/phase/lp_nognn_${c}x_1.vcf; }
  o=out/lp_gnn_t1_${c}x_1; [[ -s $o.vcf ]] || { one lp_gnn_t1 $c $o $LP phase --ont -t 1 -r $REF -s $V -b $B -o $o && same $o.vcf out/lp_gnn_${c}x_1.vcf; }
  o=out/wh_${c}x_1; [[ -s $o.vcf ]] || { one whatshap $c $o $WH phase --only-snvs --ignore-read-groups --reference=$REF -o $o.vcf $V $B && same $o.vcf $R/phase/wh_${c}x_1.vcf; }
  o=out/hapcut2_${c}x_1; [[ -s $o.phased.VCF ]] || { one hapcut2 $c $o bash -c "$H/extractHAIRS --ont 1 --bam $B --ref $REF --VCF $I/hapcut_${c}x_1.vcf --out $o.frag && $H/HAPCUT2 --fragments $o.frag --VCF $I/hapcut_${c}x_1.vcf --output $o"; rm -f $o.frag; }
done
echo "$(date '+%F %T') timing done"
