#!/bin/bash
# Runtime figure / Supplementary Table 16 on ext4: SNV-only phasing, replicate 1, every coverage of the paper
# (nanopore 10-60x, HiFi 10-50x), LongPhase v2.1.2 static release (-t 24 and -t 1), WhatsHap 2.8 (1 thread),
# HapCUT2 1.3.4 (extractHAIRS + HAPCUT2, one timing). Same protocol as run.sh / run_wh.sh / run_t1.sh: inputs and
# outputs on ext4 nvme0, one run at a time on an idle machine, page cache dropped before every run, one run each.
# Commands as in the paper (notes/runtime/README.md). Every output is compared with the paper's VCF
# (LongPhase -t 1 with the -t 24 output; HapCUT2 on chrom, pos and sample column).
# times.tsv = label, coverage, run, wall s, user+sys CPU s, peak RSS GiB
set -uo pipefail
cd /home/twolinin/lp_ext4/bench_readme
I=/home/twolinin/lp_ext4/input; REF=$I/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa; R=/disk/research; P=$R/pacbio
WH=/tmp/claude-1000/-disk-software-longphase/71da5d96-4a7e-438a-94f6-88eb87dc3db1/scratchpad/wsenv/bin/whatshap
H=/disk/software/HapCUT2/build; export LD_LIBRARY_PATH=/disk/software/HapCUT2/htslib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
cpu_idle() { local a b t=0 k; a=($(head -1 /proc/stat)); sleep 10; b=($(head -1 /proc/stat)); for k in 1 2 3 4 5 6 7 8; do t=$((t + b[k] - a[k])); done; (( (b[4] - a[4]) * 100 >= t * 95 )); }
idle() { while pgrep -x 'longphase_linux|longphase_stati|whatshap|hiphase|sniffles|extractHAIRS|HAPCUT2' > /dev/null || ! cpu_idle; do sleep 5; done; }

# ---- inputs (untimed) ----
cpin() { [[ -s $I/$2 ]] || { echo "$(date '+%F %T') copy $2"; cp -L $1 $I/$2.tmp && mv $I/$2.tmp $I/$2; }; }
for c in 12 14 16 18; do
  cpin $R/bam/hg002.sup.${c}x.1.bam hg002.sup.${c}x.1.bam; cpin $R/bam/hg002.sup.${c}x.1.bam.bai hg002.sup.${c}x.1.bam.bai
  cpin $R/pepper_calling/pepper_${c}x_1.vcf.gz pepper_${c}x_1.vcf.gz; cpin $R/pepper_calling/pepper_${c}x_1.vcf.gz.tbi pepper_${c}x_1.vcf.gz.tbi; done
# HapCUT2 reads an unzipped VCF: the same calls as the other tools (pepper_calling/*.vcf.gz, SNVs and indels).
# Records whose GT is not two alleles from {0,1,2} are dropped, as HapCUT2 rejects them (as for the HiFi runs):
# refCall ./. at 12x and 20-60x (278-682) and one 2/3 at 12x; none at 10, 14, 16, 18x.
for c in 10 12 14 16 18 20 30 40 50 60; do [[ -s $I/hapcut_${c}x_1.vcf ]] || zcat $R/pepper_calling/pepper_${c}x_1.vcf.gz | awk -F'\t' '/^#/ || $10 ~ /^[012][\/|][012](:|$)/' > $I/hapcut_${c}x_1.vcf; done
for c in 10 20 40 50; do
  cpin $P/bam/hg002.hifi.${c}x.1.bam hg002.hifi.${c}x.1.bam; cpin $P/bam/hg002.hifi.${c}x.1.bam.bai hg002.hifi.${c}x.1.bam.bai
  cpin $P/pepper_calling/pepper_hifi_${c}x.vcf.gz pepper_hifi_${c}x.vcf.gz; cpin $P/pepper_calling/pepper_hifi_${c}x.vcf.gz.tbi pepper_hifi_${c}x.vcf.gz.tbi; done
for c in 10 20 30 40 50; do cpin $P/hapcut2_v1.3.4/pepper_hifi_${c}x.vcf hapcut_hifi_${c}x.vcf; done
touch $I/*.bai $I/*.tbi $I/*.fai
echo "$(date '+%F %T') inputs ready"

# ---- one timed run: label coverage output-prefix command... ----
one() { local lab=$1 c=$2 o=$3; shift 3
  idle
  docker run --rm --privileged ubuntu:22.04 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches' > /dev/null || { echo "FAILED drop_caches"; exit 1; }
  echo "$(date '+%F %T') $o"
  /usr/bin/time -v -o $o.time "$@" > $o.log 2>&1 || { echo "FAILED $o"; return 1; }
  awk -v l=$lab -v c=$c '/Elapsed/{split($NF,x,":"); w=(length(x)==3)?x[1]*3600+x[2]*60+x[3]:x[1]*60+x[2]}
      /User time/{u=$NF} /System time/{s=$NF} /Maximum resident/{m=$NF}
      END{printf "%s\t%s\t1\t%.1f\t%.1f\t%.2f\n", l, c, w, u+s, m/1048576}' $o.time >> times.tsv; }
same() { cmp -s <(grep -v '^##' $1) <(grep -v '^##' $2) && echo "SAME $1 vs $2" || echo "DIFF $1 vs $2"; }
gtps() { awk -F'\t' '!/^#/{n=split($9,k,":"); split($10,v,":"); ps="."; for(i=1;i<=n;i++) if(k[i]=="PS") ps=v[i]; print $1"\t"$2"\t"v[1]"\t"ps}' "$1"; }   # the paper's HapCUT2 VCFs keep GT:PS only
same3() { cmp -s <(gtps $1) <(gtps $2) && echo "SAME $1 vs $2 (chrom pos GT PS)" || echo "DIFF $1 vs $2 (chrom pos GT PS)"; }
mkdir -p out

# ---- LongPhase (minutes) ----
for c in 12 14 16 18; do o=out/static_${c}x_1; [[ -s $o.vcf ]] || { one static $c $o ./longphase_static phase --ont -t 24 -r $REF -s $I/pepper_${c}x_1.vcf.gz -b $I/hg002.sup.${c}x.1.bam -o $o && same $o.vcf $R/v2.1.2/longphase_gnn/longphase_gnn_${c}x_1.vcf; }; done
for c in 12 14 16 18; do o=out/static_t1_${c}x_1; [[ -s $o.vcf ]] || { one static_t1 $c $o ./longphase_static phase --ont -t 1 -r $REF -s $I/pepper_${c}x_1.vcf.gz -b $I/hg002.sup.${c}x.1.bam -o $o && same $o.vcf out/static_${c}x_1.vcf; }; done
for c in 10 20 30 40 50; do o=out/hifi_static_${c}x_1; [[ -s $o.vcf ]] || { one hifi_static $c $o ./longphase_static phase --pb -t 24 -r $REF -s $I/pepper_hifi_${c}x.vcf.gz -b $I/hg002.hifi.${c}x.1.bam -o $o && same $o.vcf $R/v2.1.2/pacbio/longphase_hifi/longphase_hifi_${c}x_1.vcf; }; done
for c in 10 20 30 40 50; do o=out/hifi_static_t1_${c}x_1; [[ -s $o.vcf ]] || { one hifi_static_t1 $c $o ./longphase_static phase --pb -t 1 -r $REF -s $I/pepper_hifi_${c}x.vcf.gz -b $I/hg002.hifi.${c}x.1.bam -o $o && same $o.vcf out/hifi_static_${c}x_1.vcf; }; done

# ---- HapCUT2 (hours) ----
for c in 10 12 14 16 18 20 30 40 50 60; do o=out/hapcut2_${c}x_1; [[ -s $o.phased.VCF ]] && continue
  one hapcut2 $c $o bash -c "$H/extractHAIRS --ont 1 --bam $I/hg002.sup.${c}x.1.bam --ref $REF --VCF $I/hapcut_${c}x_1.vcf --out $o.frag && $H/HAPCUT2 --fragments $o.frag --VCF $I/hapcut_${c}x_1.vcf --output $o" \
    && { [[ " 10 14 16 18 " == *" $c "* ]] && same3 $o.phased.VCF <(zcat $R/hapcut2_v1.3.4/hapcut2_v134_${c}x_1.vcf.gz) || echo "NOREF $o (no paper VCF from the same input)"; }; rm -f $o.frag; done
for c in 10 20 30 40 50; do o=out/hifi_hapcut2_${c}x_1; [[ -s $o.phased.VCF ]] && continue
  one hifi_hapcut2 $c $o bash -c "$H/extractHAIRS --pacbio 1 --bam $I/hg002.hifi.${c}x.1.bam --ref $REF --VCF $I/hapcut_hifi_${c}x.vcf --out $o.frag && $H/HAPCUT2 --fragments $o.frag --VCF $I/hapcut_hifi_${c}x.vcf --output $o" \
    && same3 $o.phased.VCF $P/hapcut2_v1.3.4/hapcut2_v134_hifi_${c}x_1.vcf; rm -f $o.frag; done

# ---- WhatsHap (hours) ----
for c in 12 14 16 18; do o=out/whatshap_${c}x_1; [[ -s $o.vcf ]] && continue
  one whatshap $c $o $WH phase --only-snvs --ignore-read-groups -o $o.tmp.vcf --reference=$REF $I/pepper_${c}x_1.vcf.gz $I/hg002.sup.${c}x.1.bam \
    && mv $o.tmp.vcf $o.vcf && same $o.vcf $R/whatshap_v2.8/only/whatshap_v28_onlySNVs_${c}x_1.vcf; done
for c in 10 20 30 40 50; do o=out/hifi_whatshap_${c}x_1; [[ -s $o.vcf ]] && continue
  one hifi_whatshap $c $o $WH phase --only-snvs --ignore-read-groups -o $o.tmp.vcf --reference=$REF $I/pepper_hifi_${c}x.vcf.gz $I/hg002.hifi.${c}x.1.bam \
    && mv $o.tmp.vcf $o.vcf && same $o.vcf $P/whatshap_v28_hifi_onlySNVs_${c}x_1.vcf; done
echo "$(date '+%F %T') all done"
