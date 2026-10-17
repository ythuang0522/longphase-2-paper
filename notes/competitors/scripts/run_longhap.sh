#!/bin/bash
# LongHap 0.2.0 (pip, /disk/software/longhap_env) on HG002 nanopore, replicate 1, 10-60x: the coverages
# and inputs of the MethPhaser comparison (Fig. 2, issue #5). Same PEPPER calls and BAMs as LongPhase.
# 5mC: modkit 0.6.4 pileup of the BAM's MM/ML tags (README of LongHap: --combine-strands --cpg 5mC).
# LongHap options for ONT from its README: --ont --min_base_quality 10; --snvs_only (SNV + 5mC, as
# the LongPhase SNV+5mC and MethPhaser rows). Two modes: meth (with 5mC) and seq (sequence only).
# Per chromosome (chr1-22, the scored set), 8 at a time, then concatenated and scored like every
# other row: longphase compare (release v2.1) against v5.0q chr1-22, no BED, --ignore-sample-name.
set -uo pipefail
cd /ssd/longphase_process/longhap
R=/disk/research
REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
MK=/disk/software/modkit_v0.6.4/dist_modkit_v0.6.4_cd85862/modkit
LH=/disk/software/longhap_env/bin/longhap
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
TRUTH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
TABIX=$(command -v tabix || echo /disk/software/htslib/tabix)
export LH REF
for c in 10 20 30 40 50 60; do
    B=$R/bam/hg002.sup.${c}x.1.bam
    V=$R/pepper_calling/pepper_${c}x_1.vcf.gz
    d=${c}x; mkdir -p $d/chr
    if [[ ! -s $d/meth_${c}x.bed.gz.tbi ]]; then
        echo "$(date '+%F %T') modkit ${c}x"
        /usr/bin/time -v -o $d/modkit.time $MK pileup $B $d/meth_${c}x.bed.gz --combine-strands --modified-bases 5mC \
            --cpg --ref $REF --bgzf -t 16 --log-filepath $d/modkit.log > /dev/null 2>&1 \
            && $TABIX -p bed $d/meth_${c}x.bed.gz || { echo "FAILED modkit ${c}x"; continue; }
    fi
    for mode in meth seq; do
        out=$d/longhap_${mode}_${c}x_1.vcf
        [[ -s $out ]] && continue
        echo "$(date '+%F %T') longhap $mode ${c}x"
        m=""; [[ $mode == meth ]] && m="-m $d/meth_${c}x.bed.gz"
        export B V m d mode
        seq 1 22 | xargs -P 8 -I{} bash -c '/usr/bin/time -v -o $d/chr/${mode}_chr{}.time $LH --vcf $V -b $B -r $REF -c chr{} $m \
            --snvs_only --ont --min_base_quality 10 -o $d/chr/${mode}_chr{}.vcf.gz --log $d/chr/${mode}_chr{}.log > /dev/null 2>&1 \
            || echo "FAILED $mode $d chr{}"'
        if ls $d/chr/${mode}_chr{1..22}.vcf.gz > /dev/null 2>&1; then
            { zcat $d/chr/${mode}_chr1.vcf.gz | grep "^#"; for i in $(seq 1 22); do zcat $d/chr/${mode}_chr$i.vcf.gz | grep -v "^#"; done; } > $out
            $CMP compare -t 24 --ignore-sample-name $TRUTH $out -o $d/sw_longhap_${mode}_${c}x_1 > /dev/null 2>&1 \
                && grep "^###" $d/sw_longhap_${mode}_${c}x_1.tsv | grep -v Sample || echo "FAILED compare $mode ${c}x"
        else
            echo "FAILED $mode ${c}x: missing chromosomes"
        fi
    done
done
echo "$(date '+%F %T') done"
