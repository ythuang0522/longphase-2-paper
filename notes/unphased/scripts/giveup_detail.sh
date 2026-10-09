#!/bin/bash
# =====================================================================
# Why each tool gives a site up, split by mechanism
# ---------------------------------------------------------------------
#   wh_only     WhatsHap gave up, LongPhase phased it
#               -> LongPhase wrote PE/H1/H2, so both DP and PE are available
#   lp_gnn      phased by `longphase phase`, then removed by the GNN
#               -> PE survives in the INFO field; expect high PE
#   lp_phase    already unphased by `longphase phase`
#               -> PE is not emitted for unphased sites, so DP only
#               (mechanism: h1 == h2 while currPos < lastConnectPos, i.e.
#                no decisive vote reached the site inside a connected span)
#   background  phased by both tools
#
# Usage:
#   bash giveup_detail.sh SETS_DIR GNN_REMOVED.txt CALLSET.vcf [OUT_DIR]
# =====================================================================
set -u
SETS=${1:-.}
REMOVED=${2:?site list of GNN-removed variants}
CALL=${3:?LongPhase 2.1 VCF (INFO/PE, FORMAT/DP)}
OUT=${4:-.}
P=giveup_detail

RESULTS=$OUT/${P}_results.txt
exec > >(tee "$RESULTS") 2>&1
echo "# Give-up mechanisms, HG002 60x replicate 1"
echo "# generated: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo

tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT

# split lp_only by whether the GNN removed the site
LC_ALL=C sort -u "$SETS/unphase_venn_lp_only.txt" > "$tmp/lp_only.txt"
LC_ALL=C sort -u "$REMOVED"                       > "$tmp/removed.txt"
LC_ALL=C comm -12 "$tmp/lp_only.txt" "$tmp/removed.txt" > "$tmp/lp_gnn.txt"
LC_ALL=C comm -23 "$tmp/lp_only.txt" "$tmp/removed.txt" > "$tmp/lp_phase.txt"
LC_ALL=C sort -u "$SETS/unphase_venn_wh_only.txt" > "$tmp/wh_only.txt"

# per-site DP and PE (PE = -1 when the INFO field is absent)
awk '/^#/ {next} length($4)==1 && length($5)==1 {
        split($9,k,":"); split($10,v,":"); dp=-1
        for (i in k) if (k[i]=="DP") dp=v[i]+0
        pe=-1; if (match($8,/PE=[0-9.]+/)) pe=substr($8,RSTART+3,RLENGTH-3)+0
        print $1":"$2"\t"dp"\t"pe }' "$CALL" | LC_ALL=C sort -k1,1 > "$tmp/m.txt"

awk '/^#/ {next} length($4)==1 && length($5)==1 {
        split($10,f,":"); g=f[1]; gsub(/\|/,"/",g)
        if (g=="0/1"||g=="1/0") print $1"\t"$2 }' "$CALL" | LC_ALL=C sort -u > "$tmp/het.txt"
cat "$tmp/lp_only.txt" "$tmp/wh_only.txt" "$SETS/unphase_venn_shared.txt" \
  | LC_ALL=C sort -u > "$tmp/up.txt"
LC_ALL=C comm -23 "$tmp/het.txt" "$tmp/up.txt" | shuf -n 100000 \
  | LC_ALL=C sort -u > "$tmp/background.txt"

q () { sort -n | awk '{a[n++]=$1} END{ if(!n){print "NA NA NA"; exit}
        printf "%g %g %g", a[int(n*0.25)], a[int(n*0.5)], a[int(n*0.75)] }'; }

row () {   # $1 = site list, $2 = label
    local f=$1 lab=$2 n
    n=$(wc -l < "$f")
    LC_ALL=C join -t $'\t' -j 1 <(awk '{print $1":"$2}' "$f" | LC_ALL=C sort) "$tmp/m.txt" > "$tmp/j.txt"
    local dpq peq havepe
    dpq=$(awk -F'\t' '$2>=0{print $2}' "$tmp/j.txt" | q)
    havepe=$(awk -F'\t' 'BEGIN{t=0;h=0}{t++; if($3>=0) h++} END{printf "%.1f", (t?100*h/t:0)}' "$tmp/j.txt")
    peq=$(awk -F'\t' '$3>=0{print $3}' "$tmp/j.txt" | q)
    awk -F'\t' -v lab="$lab" -v n="$n" -v dpq="$dpq" -v peq="$peq" -v hp="$havepe" '
      BEGIN { split(dpq,d," "); split(peq,p," ") }
      $3>=0 { t++; if ($3==0) z++; else if ($3>=0.8) hi++; else mid++ }
      END { printf "%-11s %9d  %5s %5s %5s   %5s%%  %6s %6s %6s   %5.1f %5.1f %5.1f\n",
                   lab, n, d[1], d[2], d[3], hp,
                   (t?p[1]:"-"), (t?p[2]:"-"), (t?p[3]:"-"),
                   (t?100*z/t:0), (t?100*mid/t:0), (t?100*hi/t:0) }' "$tmp/j.txt"
}

printf "%-11s %9s  %17s   %6s  %20s   %17s\n" "" "" "read depth Q1/med/Q3" "PE" "PE Q1/med/Q3" "PE=0 / mid / >=.8 (%)"
row "$tmp/wh_only.txt"    wh_only
row "$tmp/lp_gnn.txt"     lp_gnn
row "$tmp/lp_phase.txt"   lp_phase
row "$tmp/background.txt" background

echo
echo "PE column: share of sites that carry an INFO/PE field. LongPhase emits"
echo "PE only for sites it phased, so lp_phase sites have none by construction."

# points for the figure: DP and PE per set
{
  echo "// [DP, PE, set]; PE = -1 when LongPhase emitted none"
  echo "export const POINTS = ["
  for s in wh_only lp_gnn lp_phase; do
    LC_ALL=C join -t $'\t' -j 1 <(shuf -n 3000 "$tmp/$s.txt" | awk '{print $1":"$2}' | LC_ALL=C sort) "$tmp/m.txt" \
      | awk -F'\t' -v k="$s" '$2>=0 { printf "  [%d,%.3f,\"%s\"],\n", ($2>120?120:$2), $3, k }'
  done
  echo "];"
} > "$OUT/${P}_points.js"

echo
echo "report : $RESULTS"
echo "points : $OUT/${P}_points.js"
