#!/bin/bash
# Speed-up of run_c.sh's WhatsHap stage (its xargs is paused with SIGSTOP; resumed at the end, when it finds every
# output present and goes on to concatenate). Same command and inputs as run_c.sh's wh(); only the BAM location differs:
#   nanopore 60x: BAM copied once to /ssd (one sequential HDD read, direct I/O to leave the page cache to run_b), 5 jobs
#   nanopore 50x, chromosomes not yet started: from the HDD as before, 4 jobs (BAM regions mostly in the page cache)
set -uo pipefail
R=/disk/research; REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa; O=$R/v2.1.2/issue10; cd $O
WH=/tmp/claude-1000/-disk-software-longphase/71da5d96-4a7e-438a-94f6-88eb87dc3db1/scratchpad/wsenv/bin/whatshap
L=/ssd/longphase_process/v2.1.2/wh_bam; mkdir -p $L
wh() {  # coverage input chrom bam
  local c=$1 in=$2 ch=$3 B=$4 d=wh_${2}_ont_${1}x
  mkdir -p $d; [[ -s $d/$ch.vcf ]] && return
  pgrep -f "$d/$ch.tmp.vcf" > /dev/null && return    # still running under run_c.sh
  /usr/bin/time -v -o $d/$ch.time $WH phase --indels --ignore-read-groups --reference=$REF --chromosome $ch -o $d/$ch.tmp.vcf in_${in}_ont_${c}x.vcf.gz $B > $d/$ch.log 2>&1 \
    && mv $d/$ch.tmp.vcf $d/$ch.vcf || echo "FAILED whatshap ont_${c}x $in $ch"; }
export -f wh; export REF WH
echo "$(date '+%F %T') start"
( for in in snv_sv snv_indel_sv; do for i in $(seq 1 22); do echo "50 $in chr$i $R/bam/hg002.sup.50x.1.bam"; done; done ) | xargs -P 4 -L1 bash -c 'wh $0 $1 $2 $3' &
p50=$!
[[ -s $L/hg002.sup.60x.1.bam.bai ]] || { dd if=$R/bam/hg002.sup.60x.1.bam of=$L/hg002.sup.60x.1.bam bs=64M iflag=direct oflag=direct status=none \
  && cp $R/bam/hg002.sup.60x.1.bam.bai $L/ && cmp -s <(stat -c %s $R/bam/hg002.sup.60x.1.bam) <(stat -c %s $L/hg002.sup.60x.1.bam) || { echo "FAILED copy"; exit 1; }; }
echo "$(date '+%F %T') 60x BAM copied"
( for in in snv_sv snv_indel_sv; do for i in $(seq 1 22); do echo "60 $in chr$i $L/hg002.sup.60x.1.bam"; done; done ) | xargs -P 5 -L1 bash -c 'wh $0 $1 $2 $3'
wait $p50
# jobs that were still running under run_c.sh when this started
while pgrep -f 'whatshap phase' > /dev/null; do sleep 30; done
echo "$(date '+%F %T') whatshap done: $(ls wh_*/chr*.vcf | grep -v tmp | wc -l)/660"
kill -CONT 2264421 && echo "resumed run_c.sh xargs"
