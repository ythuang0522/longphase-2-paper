#!/bin/bash
# bgzip the phased VCFs of every chromosome once it is scored (disk); aggregation reads the .gz files
cd /home/user/work/phase
while true; do
  for s in ../score/chr*.scored; do c=$(basename $s .scored)
    for f in *_${c}.vcf *_${c}.phased.VCF; do [[ -e $f ]] && ../tools/env/bin/bgzip -f $f; done
  done
  sleep 600
done
