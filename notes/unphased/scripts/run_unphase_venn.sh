#!/bin/bash
# =====================================================================
# Which heterozygous SNVs does each phaser give up?
# ---------------------------------------------------------------------
# LongPhase (with GNN correction) and WhatsHap both leave part of the
# callset unphased.  This script splits those give-ups into three sets:
#
#   shared   unphased by both tools
#   lp_only  unphased by LongPhase only (WhatsHap phased it)
#   wh_only  unphased by WhatsHap only  (LongPhase phased it)
#
# The denominator is the set of heterozygous SNVs present in BOTH output
# VCFs, so the three sets partition the same population for both tools.
#
# Each set is then classified against the T2T-HG002 v1.1 assembly
# (dipcall output in GRCh38 coordinates), as in run_t2t_validation.sh:
#   hom_wt      inside dip.bed, no assembly variant  -> no variant exists
#   variant     inside dip.bed, assembly variant     -> real site given up
#   unassessed  outside dip.bed                      -> no 1:1 alignment
#
# Requires: awk, sort, join, comm, zcat.  No bcftools, no bedtools.
#
# Usage (defaults shown):
#   bash run_unphase_venn.sh [LONGPHASE.vcf] [WHATSHAP.vcf] [RES_DIR] [OUT_DIR]
# =====================================================================
set -u

LP=${1:-/disk/research/longphase_gnn/longphase_gnn_60x_1.vcf}
WH=${2:-/disk/research/whatshap_v2.8/whatshap_v28_onlySNVs_60x_1.vcf}
RES=${3:-.}
OUT=${4:-.}
P=unphase_venn

DIPBED=$RES/GRCh38_HG2-T2TQ100-V1.1_dipcall-z2k.dip.bed
DIPVCF=$RES/GRCh38_HG2-T2TQ100-V1.1_dipcall-z2k.dip.vcf.gz

for f in "$LP" "$WH"; do
    [ -r "$f" ] || { echo "ERROR: cannot read $f" >&2; exit 1; }
done
mkdir -p "$OUT"
RESULTS=$OUT/${P}_results.txt
exec > >(tee "$RESULTS") 2>&1

echo "# Heterozygous SNVs given up by LongPhase vs WhatsHap"
echo "# generated: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo
echo "longphase : $LP"
echo "whatshap  : $WH"
echo

# --- 1. per-tool site lists -------------------------------------------
# Emit "chrom<TAB>pos<TAB>state" for every heterozygous SNV.
# state = P when the genotype is phased ('|'), U when it is not.
het_sites () {
    awk '/^#/ {next} length($4)==1 && length($5)==1 {
            split($10, f, ":"); gt = f[1]
            gsub(/\|/, "/", gt)                       # normalise for the het test
            if (gt != "0/1" && gt != "1/0") next      # het only
            print $1"\t"$2"\t"(index(f[1], "|") ? "P" : "U")
         }' "$1" | sort -u -k1,1 -k2,2n
}

echo "[1/4] extracting heterozygous SNVs"
het_sites "$LP" > "$OUT/${P}_lp.txt"
het_sites "$WH" > "$OUT/${P}_wh.txt"
echo "      longphase het SNVs : $(wc -l < "$OUT/${P}_lp.txt")"
echo "      whatshap  het SNVs : $(wc -l < "$OUT/${P}_wh.txt")"

# --- 2. common denominator and the three sets -------------------------
echo "[2/4] intersecting"
join -t $'\t' -j 1 -o 0,1.2,2.2 \
     <(awk '{print $1":"$2"\t"$3}' "$OUT/${P}_lp.txt" | sort -k1,1) \
     <(awk '{print $1":"$2"\t"$3}' "$OUT/${P}_wh.txt" | sort -k1,1) \
  | tr ':' '\t' | sort -k1,1 -k2,2n > "$OUT/${P}_joined.txt"
# columns: chrom pos lp_state wh_state

awk -v out="$OUT" -v p="$P" '
    { key = $3 $4                                     # PP PU UP UU
      n[key]++
      if (key == "UU") print $1"\t"$2 > (out "/" p "_shared.txt")
      if (key == "UP") print $1"\t"$2 > (out "/" p "_lp_only.txt")
      if (key == "PU") print $1"\t"$2 > (out "/" p "_wh_only.txt")
    }
    END {
      t = n["PP"] + n["PU"] + n["UP"] + n["UU"]
      printf "\n# Venn over %d heterozygous SNVs present in both callsets\n", t
      printf "  %-32s %9d  %6.2f%%\n", "phased by both",            n["PP"], 100*n["PP"]/t
      printf "  %-32s %9d  %6.2f%%\n", "unphased by both (shared)", n["UU"], 100*n["UU"]/t
      printf "  %-32s %9d  %6.2f%%\n", "unphased by LongPhase only",n["UP"], 100*n["UP"]/t
      printf "  %-32s %9d  %6.2f%%\n", "unphased by WhatsHap only", n["PU"], 100*n["PU"]/t
      printf "\n  LongPhase gives up %d (%.2f%%), WhatsHap gives up %d (%.2f%%)\n",
             n["UU"]+n["UP"], 100*(n["UU"]+n["UP"])/t, n["UU"]+n["PU"], 100*(n["UU"]+n["PU"])/t
      printf "  Jaccard of the two give-up sets: %.3f\n",
             n["UU"] / (n["UU"] + n["UP"] + n["PU"])
    }' "$OUT/${P}_joined.txt"

# --- 3. classify each set against the assembly ------------------------
if [ -r "$DIPBED" ] && [ -r "$DIPVCF" ]; then
    echo
    echo "[3/4] classifying each set against the T2T assembly"
    zcat "$DIPVCF" | awk '!/^#/ {print $1":"$2}' | sort -u > "$OUT/${P}_asm.txt"

    classify () {   # $1 = site list, $2 = label
        [ -s "$1" ] || return
        awk -v lab="$2" '
          FILENAME == ARGV[1] { n[$1]++; s[$1,n[$1]]=$2; e[$1,n[$1]]=$3; next }
          FILENAME == ARGV[2] { v[$0]=1; next }
          { c=$1; p=$2; hit=0
            for (i=1; i<=n[c]; i++) if (s[c,i] < p && p <= e[c,i]) { hit=1; break }
            cls = (hit == 0) ? "unassessed" : ((c":"p in v) ? "variant" : "hom_wt")
            k[cls]++; t++ }
          END { printf "  %-10s n=%-8d", lab, t
                printf " hom_wt %6.2f%%  variant %6.2f%%  unassessed %6.2f%%\n",
                       100*k["hom_wt"]/t, 100*k["variant"]/t, 100*k["unassessed"]/t }' \
          "$DIPBED" "$OUT/${P}_asm.txt" "$1"
    }
    classify "$OUT/${P}_shared.txt"  shared
    classify "$OUT/${P}_lp_only.txt" lp_only
    classify "$OUT/${P}_wh_only.txt" wh_only
    rm -f "$OUT/${P}_asm.txt"
else
    echo
    echo "[3/4] assembly files not found in $RES, skipping classification"
fi

# --- 4. where the exclusive sets live ---------------------------------
echo
echo "[4/4] densest 1 Mb bins"
for set in lp_only wh_only shared; do
    f=$OUT/${P}_${set}.txt
    [ -s "$f" ] || continue
    echo "  $set:"
    awk '{printf "%s\t%d\n", $1, int($2/1e6)}' "$f" | sort | uniq -c | sort -rn | head -8 \
      | awk '{printf "    %8d  %s %s Mb\n", $1, $2, $3}'
done

rm -f "$OUT/${P}_joined.txt" "$OUT/${P}_lp.txt" "$OUT/${P}_wh.txt"
echo
echo "done"
echo "  report : $RESULTS"
echo "  sets   : ${P}_shared.txt, ${P}_lp_only.txt, ${P}_wh_only.txt"
