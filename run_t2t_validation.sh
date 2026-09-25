#!/bin/bash
# =====================================================================
# Validate GNN-unphased SNVs against the T2T-HG002 diploid assembly
# ---------------------------------------------------------------------
# Question: are the SNVs the GNN removes really variants at all?
#
# Every site the GNN unphases is classified by what the T2T-HG002 v1.1
# assembly says about that position in GRCh38 coordinates:
#
#   hom_wt     inside dip.bed, absent from dip.vcf.gz
#              -> both haplotypes align 1:1 and match the reference:
#                 HG002 carries no variant here, nothing was lost
#   variant    inside dip.bed, present in dip.vcf.gz
#              -> the assembly confirms a variant: information was lost
#   unassessed outside dip.bed
#              -> no 1:1 alignment between assembly and GRCh38
#                 (centromeres, satellites, segmental duplications)
#
# The same classification is applied to a random sample of all phased
# SNVs, which gives the background rate the removed set is compared to.
#
# Requires: awk, sort, join, comm, shuf, zcat.  No bcftools or bedtools.
#
# Usage (defaults shown; run from the directory holding the GIAB files):
#   bash run_t2t_validation.sh [BASELINE.vcf] [CORRECTED.vcf] [RESOURCE_DIR] [OUT_DIR]
#
# Everything the script prints also goes to
#   <OUT_DIR>/unphase_validation_results.txt
# =====================================================================
set -u

BASE=${1:-/disk/research/longphase/longphase_60x_1.vcf}
CORR=${2:-/disk/research/longphase_gnn/longphase_gnn_60x_1.vcf}
RES=${3:-.}
OUT=${4:-.}
SAMPLE_N=${SAMPLE_N:-50000}     # background sample size
P=unphase_validation            # prefix for every output file

DIPBED=$RES/GRCh38_HG2-T2TQ100-V1.1_dipcall-z2k.dip.bed
DIPVCF=$RES/GRCh38_HG2-T2TQ100-V1.1_dipcall-z2k.dip.vcf.gz
BMBED=$RES/HG002_GRCh38_v5.0q_smvar.benchmark.bed

for f in "$BASE" "$CORR" "$DIPBED" "$DIPVCF"; do
    [ -r "$f" ] || { echo "ERROR: cannot read $f" >&2; exit 1; }
done
mkdir -p "$OUT"
RESULTS=$OUT/${P}_results.txt
exec > >(tee "$RESULTS") 2>&1     # capture the whole run

echo "# GNN-unphased SNVs vs the T2T-HG002 assembly"
echo "# generated: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo
echo "baseline  : $BASE"
echo "corrected : $CORR"
echo "resources : $RES"
echo "output    : $OUT"
echo

# --- 1. site lists -----------------------------------------------------
# GT is the first ':'-separated subfield of column 10.  A phased genotype
# contains '|', an unphased one '/'.  SNVs only (single-base REF and ALT).
echo "[1/5] extracting SNV sites"
awk '/^#/ {next} length($4)==1 && length($5)==1 {
        split($10, f, ":"); if (index(f[1], "|")) print $1"\t"$2
     }' "$BASE" | sort -u > "$OUT/${P}_phased.txt"

awk '/^#/ {next} length($4)==1 && length($5)==1 {
        split($10, f, ":");
        if (index(f[1], "/") && f[1] !~ /^\./) print $1"\t"$2
     }' "$CORR" | sort -u > "$OUT/${P}_unphased_all.txt"

# phased before, unphased after == removed by the GNN
comm -12 "$OUT/${P}_phased.txt" "$OUT/${P}_unphased_all.txt" > "$OUT/${P}_removed.txt"

# background: random sample of sites that stayed phased
# Deterministic but well-mixed random source (coreutils' documented recipe);
# `yes` has too little entropy and biases the sample towards a few chromosomes.
rand_src () { openssl enc -aes-256-ctr -pass pass:"${SEED:-42}" -nosalt </dev/zero 2>/dev/null; }
if shuf -n1 --random-source=<(rand_src) /dev/null >/dev/null 2>&1; then
    shuf -n "$SAMPLE_N" --random-source=<(rand_src) "$OUT/${P}_phased.txt" \
        | sort -u > "$OUT/${P}_background.txt"
else
    shuf -n "$SAMPLE_N" "$OUT/${P}_phased.txt" | sort -u > "$OUT/${P}_background.txt"
fi

echo "      phased in baseline : $(wc -l < "$OUT/${P}_phased.txt")"
echo "      removed by GNN     : $(wc -l < "$OUT/${P}_removed.txt")"
echo "      background sample  : $(wc -l < "$OUT/${P}_background.txt")"

# --- 2. inside dip.bed? ------------------------------------------------
# BED is 0-based half-open, VCF POS is 1-based: inside when start < POS <= end.
# dip.bed holds only a few hundred intervals, so a per-site scan is fine.
in_bed () {   # $1 = bed, $2 = sites, $3 = out
    awk '
      NR==FNR { n[$1]++; s[$1,n[$1]]=$2; e[$1,n[$1]]=$3; next }
      { c=$1; p=$2; hit=0
        for (i=1; i<=n[c]; i++) if (s[c,i] < p && p <= e[c,i]) { hit=1; break }
        print c"\t"p"\t"hit }' "$1" "$2" > "$3"
}
echo "[2/5] testing against dip.bed"
in_bed "$DIPBED" "$OUT/${P}_removed.txt"    "$OUT/${P}_removed.inbed.txt"
in_bed "$DIPBED" "$OUT/${P}_background.txt" "$OUT/${P}_background.inbed.txt"

# --- 3. present in the assembly VCF? -----------------------------------
echo "[3/5] testing against dip.vcf.gz"
zcat "$DIPVCF" | awk '!/^#/ {print $1":"$2}' | sort -u > "$OUT/${P}_asm_positions.txt"
awk 'NR==FNR { v[$0]=1; next }
     { key=$1":"$2
       print $1"\t"$2"\t"$3"\t"(key in v ? 1 : 0)"\t"($3==0 ? "unassessed" : (key in v ? "variant" : "hom_wt")) }' \
    "$OUT/${P}_asm_positions.txt" "$OUT/${P}_removed.inbed.txt" > "$OUT/${P}_removed_classified.tsv"

# --- 4. summary --------------------------------------------------------
echo "[4/5] summarising"
{
  echo "# GNN-removed SNVs classified by the T2T-HG002 assembly"
  awk '{ cls[$5]++; t++ }
       END { for (c in cls) printf "%-12s %8d %7.2f%%\n", c, cls[c], 100*cls[c]/t
             printf "%-12s %8d\n", "total", t }' "$OUT/${P}_removed_classified.tsv"
  echo
  echo "# inside dip.bed: removed vs background"
  awk 'FNR==NR { rt++; rh+=$3; next } { bt++; bh+=$3 }
       END { printf "removed    %7d / %7d  %6.2f%%\n", rh, rt, 100*rh/rt
             printf "background %7d / %7d  %6.2f%%\n", bh, bt, 100*bh/bt
             printf "odds ratio %.1fx depletion in the removed set\n",
                    ((bh/bt)/(1-bh/bt)) / ((rh/rt)/(1-rh/rt)) }' \
      "$OUT/${P}_removed.inbed.txt" "$OUT/${P}_background.inbed.txt"
}

# --- 5. per-chromosome enrichment --------------------------------------
echo
echo "[5/5] per-chromosome rates"
awk '{ t[$1]++; o[$1] += ($3==0) } END { for (c in t) printf "%s\t%d\t%d\t%.4f\n", c, o[c], t[c], o[c]/t[c] }' \
    "$OUT/${P}_background.inbed.txt" | sort -k1,1 > "$OUT/${P}_bg_per_chrom.txt"
awk '{ t[$1]++; o[$1] += ($3==0) } END { for (c in t) printf "%s\t%d\t%d\t%.4f\n", c, o[c], t[c], o[c]/t[c] }' \
    "$OUT/${P}_removed.inbed.txt"    | sort -k1,1 > "$OUT/${P}_rm_per_chrom.txt"

{
  printf "%-8s %8s %8s %9s %8s %8s %9s %8s\n" \
         chrom bg_out bg_n bg_rate rm_out rm_n rm_rate ratio
  join -t $'\t' "$OUT/${P}_bg_per_chrom.txt" "$OUT/${P}_rm_per_chrom.txt" \
    | awk '{ if ($4 > 0) printf "%-8s %8d %8d %9.4f %8d %8d %9.4f %8.1f\n", $1,$2,$3,$4,$5,$6,$7,$7/$4
             else          printf "%-8s %8d %8d %9.4f %8d %8d %9.4f %8s\n", $1,$2,$3,$4,$5,$6,$7,"inf" }' \
    | sort -k8,8gr
}

# hotspots: 1 Mb bins holding the unassessed sites
awk '$3==0 { printf "%s\t%d\n", $1, int($2/1e6) }' "$OUT/${P}_removed.inbed.txt" \
  | sort | uniq -c | sort -rn | head -20 > "$OUT/${P}_hotspots_1mb.txt"

# --- optional: restrict to the benchmark regions -----------------------
if [ -r "$BMBED" ]; then
  in_bed "$BMBED" "$OUT/${P}_removed.txt" "$OUT/${P}_removed.inbm.txt"
  awk 'NR==FNR { v[$0]=1; next }
       $3==1 { key=$1":"$2; if (key in v) a++; else w++ }
       END { t=a+w
             if (t>0) printf "\ninside smvar.benchmark.bed: %d sites\n  no variant %d (%.2f%%)\n  variant    %d (%.2f%%)\n",
                             t, w, 100*w/t, a, 100*a/t }' \
      "$OUT/${P}_asm_positions.txt" "$OUT/${P}_removed.inbm.txt"
fi

# hotspot table into the report as well
echo
echo "# densest 1 Mb bins among unassessed sites (count, chrom, Mb)"
cat "$OUT/${P}_hotspots_1mb.txt"

rm -f "$OUT/${P}_asm_positions.txt" "$OUT/${P}_unphased_all.txt" \
      "$OUT/${P}_phased.txt" "$OUT/${P}_bg_per_chrom.txt" "$OUT/${P}_rm_per_chrom.txt" \
      "$OUT/${P}_removed.inbm.txt"
echo
echo "done"
echo "  report    : $RESULTS"
echo "  per-site  : $OUT/${P}_removed_classified.tsv"
