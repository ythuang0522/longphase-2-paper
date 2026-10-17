#!/bin/bash
# Build the merged SNV/indel + sequence-resolved Sniffles SV VCFs (merge_sv.py) for 10-60x ahead of
# the LongHap and HiPhase all-variant runs, which both read them.
R=/disk/research; REF=$R/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
BG=$(command -v bgzip || echo /disk/software/htslib/bgzip); TB=$(command -v tabix || echo /disk/software/htslib/tabix)
for c in 10 20 30 40 50 60; do
    mkdir -p ${c}x; V=${c}x/in_${c}x.vcf.gz
    [[ -s $V.tbi ]] || { /disk/software/longhap_env/bin/python merge_sv.py $R/pepper_calling/pepper_${c}x_1.vcf.gz \
        $R/sniffles_v2.8/sniffles_${c}x_1.vcf $REF ${c}x/in_${c}x.vcf && $BG -f ${c}x/in_${c}x.vcf && $TB -f -p vcf $V; }
done
echo done
