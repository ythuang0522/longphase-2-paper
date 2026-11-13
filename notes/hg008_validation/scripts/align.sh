#!/bin/bash
# align.sh: HG008-N-P ONT uBAMs -> GRCh38 as the paper's HG002 nanopore alignments (BAM @PG: minimap2 2.24-r1122
# -y -ax map-ont, samtools view -e '[qs] >= 10'). The qs filter is applied before alignment here (same read set, the
# filter reads only the Dorado qs tag); all uBAM tags (MM/ML/qs/RG...) are carried with samtools fastq -T '*' and -y.
# Waits for download2.sh (md5 OK). Output bam/HG008-N-P.full.bam (+ .bai), per-flow-cell BAMs deleted after merge.
set -euo pipefail
cd /disk/research/HG008
REF=/disk/research/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa; MM=/disk/software/minimap2-2.24/minimap2; T=${T:-24}
until grep -q "md5 OK" logs/download.log; do grep -q "md5 FAILED" logs/download.log && { echo "md5 FAILED, stop"; exit 1; }; sleep 60; done
mkdir -p bam; [[ -s bam/ref.mmi ]] || $MM -x map-ont -d bam/ref.mmi $REF 2> bam/ref.mmi.log
for f in ubam/*.bam; do o=bam/$(basename $f .bam).aln.bam; [[ -s $o ]] && continue
  echo "$(date '+%F %T') align $f"
  /usr/bin/time -v -o $o.time bash -c "samtools view -@4 -u -e '[qs] >= 10' $f | samtools fastq -@4 -T '*' - |
    $MM -y -t $T -ax map-ont bam/ref.mmi - | samtools sort -@8 -m 3G -o $o.tmp -" 2> $o.log && mv $o.tmp $o
done
echo "$(date '+%F %T') merge"
samtools merge -@16 -f bam/HG008-N-P.full.bam bam/*.aln.bam && samtools index -@16 bam/HG008-N-P.full.bam
samtools coverage bam/HG008-N-P.full.bam > bam/HG008-N-P.full.coverage.tsv
rm -f bam/*.aln.bam
echo "$(date '+%F %T') align done"
