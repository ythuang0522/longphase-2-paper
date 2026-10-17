#!/bin/bash
# LongHap 0.2.0 co-phasing all variant types (2026-10-17), HG002 nanopore replicate 1, 10-60x: the
# counterpart of LongPhase's Indel+Mod+SV row. One VCF per coverage = the PEPPER calls (SNVs and
# indels) + the Sniffles 2.8 SVs LongPhase takes as --sv-file, made sequence-resolved by merge_sv.py
# (LongHap reads every type from one VCF). 5mC: the modkit bedMethyl of ../<c>x. LongHap's default
# flow for ONT (README): --ont --min_base_quality 10 -m <bed>, no --snvs_only. Per chromosome, 8 at a
# time, concatenated and scored like every other row (longphase compare release v2.1,
# --ignore-sample-name, v5.0q chr1-22, no BED). Starts after the TinkerHap/HiPhase nanopore runs.
set -uo pipefail
cd /ssd/longphase_process/longhap/allvar
until grep -qE "done$" /ssd/longphase_process/others_ont/run_others_ont.log 2>/dev/null; do sleep 60; done
echo "$(date '+%F %T') start; $(cat /proc/loadavg)"
R=/disk/research
export REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa LH=/disk/software/longhap_env/bin/longhap
PY=/disk/software/longhap_env/bin/python
CMP=/disk/software/longphase_v2.1_release/longphase_linux-x64
TRUTH=/ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf
BG=$(command -v bgzip || echo /disk/software/htslib/bgzip); TB=$(command -v tabix || echo /disk/software/htslib/tabix)
for c in 10 20 30 40 50 60; do
    export d=${c}x V=${c}x/in_${c}x.vcf.gz B=$R/bam/hg002.sup.${c}x.1.bam M=../${c}x/meth_${c}x.bed.gz
    mkdir -p $d/chr
    out=longhap_all_${c}x_1.vcf
    [[ -s $out ]] && continue
    [[ -s $V.tbi ]] || { $PY merge_sv.py $R/pepper_calling/pepper_${c}x_1.vcf.gz $R/sniffles_v2.8/sniffles_${c}x_1.vcf $REF $d/in_${c}x.vcf \
                         && $BG -f $d/in_${c}x.vcf && $TB -f -p vcf $V; }
    echo "$(date '+%F %T') longhap all ${c}x"
    seq 1 22 | xargs -P 8 -I{} bash -c '/usr/bin/time -v -o $d/chr/chr{}.time $LH --vcf $V -b $B -r $REF -c chr{} -m $M \
        --ont --min_base_quality 10 -o $d/chr/chr{}.vcf.gz --log $d/chr/chr{}.log > /dev/null 2>&1 || echo "FAILED $d chr{}"'
    if ls $d/chr/chr{1..22}.vcf.gz > /dev/null 2>&1; then
        { zcat $d/chr/chr1.vcf.gz | grep "^#"; for i in $(seq 1 22); do zcat $d/chr/chr$i.vcf.gz | grep -v "^#"; done; } > $out
        $CMP compare -t 24 --ignore-sample-name $TRUTH $out -o sw_longhap_all_${c}x_1 > /dev/null 2>&1 \
            && grep "^###" sw_longhap_all_${c}x_1.tsv | grep -v Sample || echo "FAILED compare ${c}x"
    else
        echo "FAILED ${c}x: missing chromosomes"
    fi
done
echo "$(date '+%F %T') done"
