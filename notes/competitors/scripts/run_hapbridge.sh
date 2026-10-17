#!/bin/bash
# HapBridge (Humonex/HapBridge ec48f02, local_counter.patch: two debug counters were never defined,
# so every bridge() call raised UnboundLocalError; phasing logic unchanged) on HG002 nanopore,
# replicate 1, 10-60x. Same input as MethPhaser (issue #5): LongPhase 2 SNV phasing without GNN
# (/disk/research/methphaser/test/<c>x/longphase_<c>x_1.vcf.gz) and its LongPhase-haplotagged BAM,
# primary alignments only (MM/ML, HP and PS tags kept). bridge.py -t 16 (switch-error correction and
# block bridging, the default bridge2). Scored like every other row: longphase compare (release v2.1)
# against v5.0q chr1-22, no BED, --ignore-sample-name. Starts after the LongHap runs.
set -uo pipefail
cd /ssd/longphase_process/hapbridge
until grep -qE "done$" /ssd/longphase_process/longhap/run_longhap.log 2>/dev/null; do sleep 60; done
PY=/disk/software/longhap_env/bin/python
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
TRUTH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
for c in 10 20 30 40 50 60; do
    V=/disk/research/methphaser/test/${c}x/longphase_${c}x_1.vcf.gz
    B=/disk/research/methphaser/rerun_0.0.4/${c}x/hg002.sup.${c}x.1.tagged.primary.bam
    o=hapbridge_${c}x_1
    if [[ ! -s $o.vcf ]]; then
        echo "$(date '+%F %T') hapbridge ${c}x"
        (cd /disk/software/HapBridge && /usr/bin/time -v -o /ssd/longphase_process/hapbridge/$o.time \
            $PY bridge.py $V $B /ssd/longphase_process/hapbridge/$o.vcf -t 16) > $o.log 2>&1 || { echo "FAILED ${c}x"; continue; }
    fi
    $CMP compare -t 24 --ignore-sample-name $TRUTH $o.vcf -o sw_$o > /dev/null 2>&1 \
        && grep "^###" sw_$o.tsv | grep -v Sample || echo "FAILED compare ${c}x"
done
echo "$(date '+%F %T') done"
