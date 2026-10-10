# GCphase: why its Hamming distance is so high (`notes/SUSPECTED_ERRORS.md` item 5)

The paper runs of GCphase (`/disk/research/gcphase/`, 10–20×, replicates 1–10) have a Hamming
distance of 32–40% and a switch error rate 21–26 times that of LongPhase 2. Methods excludes
GCphase from the comparison. This note records what causes the high values, so that the decision
on GCphase can be discussed on measured data. Checked 2026-10-10.

GCphase: `github.com/baimawjy/GCphase` (commit `ffa7e8b`), `/disk/software/GCphase`, run in the
`workEnv` container (`gcphase_env`) as `python GCphase.py -vcf ... -bam ... -outpath ...`.

## Summary

1. **Input handling (confirmed, code and data).** GCphase loads every input record whose sample
   column does not start with `1` (`get_info.py`, `if line_split[-1][0] == '1': continue`) and never
   reads FILTER or checks that REF and ALT are single bases. With the PEPPER call sets it therefore
   phased `0/0` `refCall` records as heterozygous SNVs; `1/1` records stay `1/1`.
2. **Effect of (1), measured on chr20 at 20×:** removing the `refCall` records lowers the switch
   error rate from 1.40% to 0.51% and the Hamming distance from 35.0% to 16.1%. Keeping only PASS
   heterozygous single-base SNVs gives the same (0.51%, 16.0%).
3. **The rest is GCphase's own phasing.** With the clean input, the Hamming distance (16.0%) is still
   4.7 times WhatsHap's (3.4%) and 7.8 times LongPhase 2's (2.0%) on the same chromosome, and the
   switch error rate (0.51%) 2.4 and 7.6 times. The remaining Hamming errors come from long
   flipped segments inside GCphase's blocks, not from its block joins. No further code defect was
   identified.
4. **Output without PS (confirmed, not in the paper runs).** If the input FORMAT has no `PS` key,
   `outputResult.py` keeps `snp_block_num = -1` and writes the block ID over the last FORMAT value,
   so the output has no PS and every chromosome is scored as one block (Hamming 46–49%). The paper
   runs used `GT:PS` input and are not affected.

## 1. Genotypes in and out (`genotype_transitions_{10,20}x_1.tsv`, `scripts/genotype_transitions.py`)

Input `/disk/research/pepper_calling/pepper_{c}x_1.vcf.gz` against output
`/disk/research/gcphase/gcphase_{c}x_1.vcf.gz`, matched by CHROM, POS, REF and ALT (every output
record is in the input).

| Input | 10×_1 | 20×_1 |
|---|---|---|
| `0/1` PASS → phased | 2,275,801 | 2,619,383 |
| `0/0` refCall → phased | **1,194,969** (34% of phased) | **800,489** (23% of phased) |
| `0/0` refCall → `0/0` | 1,148,347 | 1,123,520 |
| `1/1` PASS → `1/1` | 1,853,668 | 2,028,965 |

The 10× value is the "about 1.2 million rejected reference calls per 10× genome" of Methods.

## 2. Controlled reruns on chr20, 20× replicate 1 (`chr20_20x_1.tsv`)

Same BAM (`/disk/research/bam/hg002.sup.20x.1.bam`, chr20 extracted; GCphase uses only primary
alignments, flag 0/16, so the extraction does not change its input), same GCphase install and
environment, scored with `longphase compare` (v2.1) against v5.0q with `--regions chr20`.

| Run (chr20) | Input | SW rate | Hamming | Blocks | N50 (Mb) |
|---|---|---|---|---|---|
| Paper run (chr20 row of the genome-wide run) | all records | 1.40% | 34.5% | 95 | 2.79 |
| Control | all records | 1.40% | 35.0% | 95 | 2.79 |
| refCall removed | FILTER PASS | 0.51% | 16.1% | 113 | 1.34 |
| Heterozygous SNVs only | PASS `0/1`, single-base REF/ALT | 0.51% | 16.0% | 115 | 1.26 |
| Same, second run | as above | 0.51% | 16.0% | 115 | 1.26 |
| LongPhase 2 (no GNN), paper run | all records | 0.07% | 2.0% | 91 | 1.48 |
| WhatsHap 2.8 `--only-snvs`, paper run | all records | 0.21% | 3.4% | 98 | 1.53 |

- The control reproduces the paper run (724 against 728 switch errors, same blocks and N50), so
  the setup matches.
- All GCphase inputs were written with `FORMAT=GT:PS` (sample `GT:.`), as in the paper runs.
- GCphase is randomized (`random.shuffle` in `FM()`, `random.choice` in the join step); the two
  heterozygous-only runs differ in a few records and give the same scores.

## 3. Where the remaining Hamming errors are (`scripts/block_hamming.py`, `scripts/flips_vs_joins.py`)

Heterozygous-only input. Hamming errors per block (`min(mismatches, matches)` per PS):
75% of them are in four blocks of 2.3–4.6 Mb that are 33–50% wrong. Inside these blocks the
agreement with v5.0q changes only 1–24 times; for example, 14.67–19.31 Mb has one change at
17.66 Mb (2,951 SNVs flipped, 1,787 correct) and 7.88–10.25 Mb one change at 9.07 Mb (1,190 flipped,
1,208 correct). The errors are therefore long flipped segments, not scattered single sites.

GCphase builds blocks in `phasingSNP.py` (FM partition, switch correction by flipping every other
segment, then joining neighbouring blocks on the last and first SNP of each). To test the join
step, one run wrote the blocks before joining (`scripts/premerge_dump.patch`, output only, no
change to the algorithm):

| | At a block join | Inside a pre-join block |
|---|---|---|
| Changes of agreement with v5.0q (all) | 2 | 252 |
| Long-range flips (≥50 SNVs on both sides) | **0** | **16** |

All long-range flips lie inside the blocks before joining, so the join step does not cause them.
They arise in the earlier partition and switch-correction steps; the run gives no basis to call
them a code defect rather than a limitation of the method.

## Open for discussion

- How much the GCphase result matters for this paper.
- Whether to re-run GCphase genome-wide on a heterozygous-only input (about 4 h and 119 GB of
  memory per 10× genome with the original input; on chr20 at 20×, 8 min and 9 GB with the clean
  input against 42 min and 42 GB with the original). On chr20 that input halves its Hamming distance but leaves it far
  above WhatsHap and LongPhase 2.
- Methods says GCphase "treats every input record as a heterozygous SNV"; records called `1/1` are
  the exception (point 1), and the chr20 runs show that a heterozygous-only input does not make
  GCphase comparable.

## Commands

```sh
W=/ssd/longphase_process/gcphase_check
samtools view -@ 8 -b -o $W/chr20.20x_1.bam /disk/research/bam/hg002.sup.20x.1.bam chr20 && samtools index $W/chr20.20x_1.bam
zcat /disk/research/pepper_calling/pepper_20x_1.vcf.gz | awk -F'\t' '/^#/ || $1=="chr20"' > $W/control.chr20.vcf
awk -F'\t' '/^#/ || $7=="PASS"' $W/control.chr20.vcf > $W/pass.chr20.vcf
awk -F'\t' '/^#/ {print; next} {split($10,a,":"); if ($7=="PASS" && a[1]=="0/1" && length($4)==1 && length($5)==1) print}' \
    $W/control.chr20.vcf > $W/het.chr20.vcf
# FORMAT=GT:PS, sample GT:. (as in the paper runs)
for a in control pass het; do
  awk -F'\t' 'BEGIN{OFS="\t"} /^##FORMAT/ {next}
    /^#CHROM/ {print "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">";
               print "##FORMAT=<ID=PS,Number=1,Type=Integer,Description=\"Phase set identifier\">"; print; next}
    /^#/ {print; next} {split($10,v,":"); $9="GT:PS"; $10=v[1]":."; print}' $W/$a.chr20.vcf > $W/$a.chr20.gtps.vcf
done
docker exec workEnv bash $W/run.sh          # scripts/run_chr20.sh: the three arms in parallel
LP=/disk/software/longphase_v2.1_release/longphase_linux-x64
for a in control pass het; do
  $LP compare -t 4 --ignore-sample-name --regions chr20 HG002_GRCh38_v5.0q_smvar.chr1_22.vcf $W/out_$a/result/mine.vcf -o $W/cmp_$a
done
python3 scripts/block_hamming.py $W/out_het/result/mine.vcf
# join test: GCphase copy with scripts/premerge_dump.patch, heterozygous-only input, then
python3 scripts/flips_vs_joins.py $W/out_het_dbg
```
