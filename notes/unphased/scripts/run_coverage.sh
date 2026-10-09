#!/bin/bash
# =====================================================================
# All numbers behind the give-up figure, for one coverage.
# Prints a JS block ready to paste into UnphaseVenn.jsx.
#
#   bash run_coverage.sh COV LP_PRE.vcf LP_GNN.vcf WH.vcf TRUTH.vcf.gz LONGPHASE [OUT]
# e.g.
#   bash run_coverage.sh 10x \
#       longphase/longphase_10x_1.vcf longphase_gnn/longphase_gnn_10x_1.vcf \
#       whatshap_v2.8/whatshap_v28_onlySNVs_10x_1.vcf \
#       /ssd/longphase_process/HG002_GRCh38_v5.0q_smvar.vcf.gz \
#       /disk/software/longphase/longphase
# =====================================================================
set -u
COV=${1:?coverage label, e.g. 10x}
LPPRE=${2:?LongPhase VCF before GNN}
LPGNN=${3:?LongPhase 2.1 VCF}
WH=${4:?WhatsHap VCF}
TRUTH=${5:?benchmark VCF}
LONGPHASE=${6:-longphase}
OUT=${7:-.}
BIN=2; CAPBINS=63

tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT

het () {   # $1 = vcf, $2 = "|" phased / "/" unphased
    awk -v sep="$2" '/^#/{next} length($4)==1 && length($5)==1 {
        split($10,f,":"); g=f[1]; gsub(/\|/,"/",g)
        if (g!="0/1" && g!="1/0") next
        if (index(f[1],sep)) print $1"\t"$2 }' "$1" | LC_ALL=C sort -u
}

het "$LPGNN" "|" > "$tmp/lp_p.txt";  het "$LPGNN" "/" > "$tmp/lp_u.txt"
het "$WH"    "|" > "$tmp/wh_p.txt";  het "$WH"    "/" > "$tmp/wh_u.txt"
het "$LPPRE" "|" > "$tmp/pre_p.txt"

LC_ALL=C comm -12 "$tmp/lp_u.txt" "$tmp/wh_u.txt" > "$tmp/both.txt"
LC_ALL=C comm -12 "$tmp/lp_u.txt" "$tmp/wh_p.txt" > "$tmp/lp_only.txt"
LC_ALL=C comm -12 "$tmp/wh_u.txt" "$tmp/lp_p.txt" > "$tmp/wh_only.txt"
# removed by the GNN: phased before, unphased after
LC_ALL=C comm -12 "$tmp/pre_p.txt" "$tmp/lp_u.txt" > "$tmp/gnn.txt"
LC_ALL=C comm -12 "$tmp/lp_only.txt" "$tmp/gnn.txt" > "$tmp/lp_gnn.txt"
LC_ALL=C comm -23 "$tmp/lp_only.txt" "$tmp/gnn.txt" > "$tmp/lp_phase.txt"

# --- switch-error intervals for both tools -----------------------------
"$LONGPHASE" compare "$TRUTH" "$WH"    --ignore-sample-name --sw-bed "$tmp/wh_sw.bed" -o "$tmp/c_wh" -t 24 >/dev/null 2>&1
"$LONGPHASE" compare "$TRUTH" "$LPGNN" --ignore-sample-name --sw-bed "$tmp/lp_sw.bed" -o "$tmp/c_lp" -t 24 >/dev/null 2>&1

inside () {   # $1 = sw bed, $2 = site list -> percentage
    awk 'NR==FNR { n[$1]++; s[$1,n[$1]]=$2; e[$1,n[$1]]=$3; next }
         { c=$1; p=$2; hit=0
           for (i=1;i<=n[c];i++) if (s[c,i] < p && p <= e[c,i]) { hit=1; break }
           t++; h+=hit }
         END { printf "%.2f", (t ? 100*h/t : 0) }' "$1" "$2"
}
wh_bg=$(inside "$tmp/wh_sw.bed" "$tmp/wh_p.txt")
lp_bg=$(inside "$tmp/lp_sw.bed" "$tmp/lp_p.txt")
lp_phase_x=$(inside "$tmp/wh_sw.bed" "$tmp/lp_phase.txt")
lp_gnn_x=$(inside "$tmp/wh_sw.bed" "$tmp/lp_gnn.txt")
wh_only_x=$(inside "$tmp/lp_sw.bed" "$tmp/wh_only.txt")

# --- depth histograms --------------------------------------------------
awk '/^#/{next} length($4)==1 && length($5)==1 {
       split($9,k,":"); split($10,v,":"); dp=-1
       for (i in k) if (k[i]=="DP") dp=v[i]+0
       if (dp>=0) print $1":"$2"\t"dp }' "$LPGNN" | LC_ALL=C sort -k1,1 > "$tmp/dp.txt"

hist () {
    LC_ALL=C join -t $'\t' -j 1 <(awk '{print $1":"$2}' "$1" | LC_ALL=C sort) "$tmp/dp.txt" \
      | awk -F'\t' -v b="$BIN" -v nb="$CAPBINS" '
          { i=int($2/b); if (i>=nb) i=nb-1; c[i]++; n++ }
          END { for (i=0;i<nb;i++) printf "%s%.5f", (i?",":""), (n?c[i]/n:0) }'
}

# --- emit --------------------------------------------------------------
{
echo "  \"$COV\": {"
echo "    venn: { lp: $(wc -l < "$tmp/lp_only.txt"), phase: $(wc -l < "$tmp/lp_phase.txt"), gnn: $(wc -l < "$tmp/lp_gnn.txt"), wh: $(wc -l < "$tmp/wh_only.txt"), both: $(wc -l < "$tmp/both.txt") },"
echo "    cross: ["
echo "      { label: \"LongPhase only — phase\", set: $lp_phase_x, bg: $wh_bg, other: \"WhatsHap\", color: \"#dc2626\" },"
echo "      { label: \"LongPhase only — gnn\",   set: $lp_gnn_x,   bg: $wh_bg, other: \"WhatsHap\", color: \"#dc2626\" },"
echo "      { label: \"WhatsHap only\",          set: $wh_only_x,  bg: $lp_bg, other: \"LongPhase\", color: \"#2563eb\" },"
echo "    ],"
echo "    hist: {"
echo "      lp:   [$(hist "$tmp/lp_only.txt")],"
echo "      wh:   [$(hist "$tmp/wh_only.txt")],"
echo "      both: [$(hist "$tmp/both.txt")],"
echo "    },"
echo "  },"
} | tee "$OUT/figure_data_${COV}.js"
