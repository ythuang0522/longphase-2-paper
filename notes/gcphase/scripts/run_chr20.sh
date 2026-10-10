#!/bin/bash
# GCphase on chr20 of HG002 20x replicate 1 with three inputs (issue: GCphase Hamming distance).
source /opt/miniconda/etc/profile.d/conda.sh; conda activate gcphase_env
W=/ssd/longphase_process/gcphase_check; cd /disk/software/GCphase
for a in control pass het; do
  ( /usr/bin/time -v python GCphase.py -vcf $W/$a.chr20.gtps.vcf -bam $W/chr20.20x_1.bam -outpath $W/out_$a > $W/$a.log 2>&1; echo "$a exit $?" >> $W/done.txt ) &
done
wait
