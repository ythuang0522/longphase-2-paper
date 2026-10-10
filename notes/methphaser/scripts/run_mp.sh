#!/bin/bash
# Issue 5 (longphase-2-paper): rerun MethPhaser 0.0.4 on the LongPhase SNV-only,
# no-GNN replicate-1 phasing in /disk/research/methphaser/test.
#
# The first run there (MethPhaser 0.0.3, bioconda) wrote an output VCF equal to
# its input: every methphasing call crashed on secondary alignments, which have
# no SEQ but keep the MM tag ("MM tag refers to bases beyond sequence length",
# then AttributeError on mm.keys()), and meth_phaser_parallel ignores the exit
# status. The WhatsHap-input pipeline (../run_methphaser.sh) filtered -F 0x900;
# this rerun does the same.  meth_phaser_post_processing writes records without
# some newlines, so its VCF is repaired with ../fix_methphaser_vcf.py (as in the
# WhatsHap-input pipeline) into methphaser_<c>x_1.fixed.vcf.
#
# Runs inside the workEnv container (methphaser_env), with the 0.0.4 scripts of
# /disk/software/methphaser (git tag 0.0.4; meth_phaser_post_processing has the
# local patch scripts/meth_phaser_post_processing.patch) first on PATH.  Several instances may run at once on
# different coverages.
#
#   T=16 run_mp.sh 30 50
set -uo pipefail
source /opt/miniconda/etc/profile.d/conda.sh
conda activate methphaser_env
export PATH=/disk/software/methphaser:$PATH
T=${T:-16}
REF=/disk/research/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
IN=/disk/research/methphaser/test
OUT=/disk/research/methphaser/rerun_0.0.4
for c in "$@"; do
    W=$OUT/${c}x; mkdir -p $W
    B=$W/hg002.sup.${c}x.1.tagged.primary.bam
    G=$IN/${c}x/longphase_${c}x_1.gtf
    V=$IN/${c}x/longphase_${c}x_1.vcf.gz
    echo "$(date '+%F %T') ${c}x start (T=$T)"
    if [[ ! -f $B.bai ]]; then
        samtools view -@ $T -b -F 0x900 -o $B.tmp $IN/${c}x/hg002.sup.${c}x.1.tagged.bam && mv $B.tmp $B \
          && samtools index -@ $T $B || { echo "${c}x FAILED filter"; continue; }
    fi
    if [[ ! -f $W/parallel.done ]]; then
        # a meth_phaser_parallel left running by an earlier driver: wait for it
        while pgrep -f "[m]eth_phaser_parallel .*rerun_0.0.4/${c}x/" > /dev/null; do sleep 60; done
        if grep -q "Exit status: 0" $W/parallel.log 2> /dev/null; then
            touch $W/parallel.done
        else
            rm -rf $W/work
            /usr/bin/time -v meth_phaser_parallel -t $T -b $B -r $REF -g $G -vc $V -o $W/work/ \
                > $W/parallel.log 2>&1 && touch $W/parallel.done
        fi
    fi
    [[ -f $W/parallel.done ]] || { echo "${c}x FAILED parallel (see $W/parallel.log)"; continue; }
    if [[ ! -f $W/post.done ]]; then
        /usr/bin/time -v meth_phaser_post_processing -t $T -ib $B -if $W/work/ \
            -ov $W/methphaser_${c}x_1.vcf -ob $W/output -vc $V > $W/post.log 2>&1 \
          && touch $W/post.done \
          || { echo "${c}x FAILED post (see $W/post.log)"; continue; }
    fi
    (cd $W && python /disk/research/methphaser/fix_methphaser_vcf.py methphaser_${c}x_1.vcf methphaser_${c}x_1.fixed.vcf \
        && zcat methphaser_${c}x_1.fixed.vcf.gz > methphaser_${c}x_1.fixed.vcf) \
      || { echo "${c}x FAILED fix"; continue; }
    echo "$(date '+%F %T') ${c}x done: tracebacks=$(grep -c Traceback $W/parallel.log)" \
         "csv=$(find $W/work -name '*.csv' | wc -l)" \
         "bad_lines=$(awk -F'\t' '!/^#/ && NF!=10' $W/methphaser_${c}x_1.fixed.vcf | wc -l)"
done
