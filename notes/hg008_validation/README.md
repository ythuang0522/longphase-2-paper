# HG008-N external validation of the frozen GNN (issue #11)

Minimum experiment of issue #11: the LongPhase 2 v2.1.2 release (GNN trained on HG002, threshold 0.35) on a second
individual, HG008-N (normal pancreas, nanopore). There are 7 inputs × 4 configurations = 28 phasing runs, scored
against assembly-derived phase from the frozen HG008-N v6.3 assembly. Nothing was retrained, tuned, re-thresholded or
re-masked on HG008. The truth rules were fixed on 2026-11-10, before any phasing output existed. Run 2026-11-10 to
2026-11-13 on the lab server. Results were posted to the issue on 2026-11-13.

## Result

| coverage | seeds | LongPhase 2 (GNN) | `--disableGNN` | WhatsHap 2.8 | HapCUT2 1.3.4 |
|---|--:|--:|--:|--:|--:|
| **SNV switch error rate (%), mean** | | | | | |
| 10× | 3 | **0.058** | 0.069 | 0.107 | 0.142 |
| 20× | 3 | **0.036** | 0.044 | 0.103 | 0.144 |
| 30× | 1 | **0.026** | 0.032 | 0.091 | 0.137 |
| **Completeness (%), mean** | | | | | |
| 10× | 3 | 67.63 | 67.71 | 68.24 | 68.23 |
| 20× | 3 | 92.37 | 92.47 | 93.02 | 93.01 |
| 30× | 1 | 95.56 | 95.65 | 96.21 | 96.21 |
| **Block-wise Hamming (%), mean** | | | | | |
| 10× | 3 | 1.29 | 1.45 | 1.33 | 1.38 |
| 20× | 3 | 1.54 | 1.73 | 1.78 | 1.79 |
| 30× | 1 | 0.94 | 1.13 | 1.47 | 1.29 |
| **Block N50 (kb), mean** | | | | | |
| 10× | 3 | 226 | 231 | 226 | 227 |
| 20× | 3 | 763 | 788 | 772 | 777 |
| 30× | 1 | 1,062 | 1,079 | 1,062 | 1,070 |

### 1. Does the HG002-trained GNN reduce HG008 phase errors?

Yes, in every run. Compared with the identical `--disableGNN` run:

- **Switch errors:** 15–17% fewer at 10× and 18–20% fewer at 20× and 30×.
- **Hamming distance:** lower in every run.
- **Cost:**
  - completeness is 0.08–0.11 percentage point lower (1,740–2,410 fewer benchmark SNVs phased);
  - there are 3.8–15.8% more blocks;
  - block N50 is 1.5–3.6% lower.

The GNN leaves 49–69k calls unphased per run. Of these, 1.7–2.4k (3–4%) are benchmark heterozygous SNVs.

### 2. Does the full method keep its advantage over WhatsHap and HapCUT2?

Yes.

- **Switch error rate:** 1.8–3.6-fold lower than WhatsHap and 2.4–5.4-fold lower than HapCUT2 (means), with no overlap between seeds.
- **Completeness:** about 0.6 percentage point lower than both.
- **Block N50:** comparable to both.

### Results against the method

- **10x_1 Hamming distance:** WhatsHap's (1.364%) is marginally below LongPhase 2 with GNN (1.366%).
- **30× seeds:** one seed only. The downsampling seeds measure sampling variability within one individual, not independent genomes.

## Files

| path | content |
|---|---|
| `results/hg008_runs.tsv` | per-run metrics, 28 rows (`longphase compare` and `score_phase.py` columns) |
| `results/hg008_summary.tsv` | means and ranges per coverage and tool |
| `results/hg008_gnn_effect.tsv` | GNN vs `--disableGNN` per run: Δ switch errors, withheld calls and benchmark SNVs, blocks, N50 |
| `results/hg008_fig.pdf` | switch error rate / completeness / block N50 against coverage, seeds as points (draft panel, not in Nature style yet) |
| `truth/HG008N_v6.3_truth.blocks.bed` | scoring mask = truth phase blocks on GRCh38 (2,781 intervals, 4th column = PS) |
| `truth/HG008N_v6.3_GRCh38.dip.bed` | dipcall confidence BED |
| `truth/HG008N_v6.3_hap{1,2}.gaps.bed` | assembly N-gaps in assembly coordinates (`scripts/truth/gaps.py`) |
| `truth/HG008N_v6.3_truth.counts.tsv` | exclusion counts |
| `truth/check_truth.txt`, `truth/validated` | truth checks (sample, chromosomes, GT, alleles, PS, swap test) |
| `scripts/` | every script, in run order below; copies of `/disk/research/HG008/*.sh`, `truth/*` |

### Large files (lab server, not in Git)

All under `/disk/research/HG008/`:

- **Inputs:**
  - `ubam/`: 3 uBAMs, `checksum.md5` and GIAB READMEs
  - `asm/`: v6.3 haplotype FASTAs
- **Alignments:**
  - `bam/HG008-N-P.full.bam`
  - `bam/HG008-N-P.{10,20,30}x.{seed}.bam`
- **Calls:** `calls/pepper_<run>.vcf.gz`, `calls/pepper_<run>.pass_het_snv.vcf` (HapCUT2 input), plus `.time`, `.log`, `.out/`
- **Phasing:** `phase/{lp_gnn,lp_nognn,wh,hapcut2}_<run>*`, plus per-step `.time` (`/usr/bin/time -v`) and `.log`
- **Truth:**
  - `truth/HG008N_v6.3_truth.vcf` (161 MB)
  - `truth/HG008N_v6.3_GRCh38.dip.vcf.gz` and the dipcall intermediates
- **Scores:** `score/sw_<tool>_<run>.{tsv,log,sp.tsv}`
- **Logs:** `logs/`

## Versions and checksums

| item | version | checksum / source |
|---|---|---|
| LongPhase 2 | v2.1.2 release binary, tag `6b8f2dd` | `longphase_linux-x64` sha256 `d61a744bdbbdd3144a05f6924b1d482d351a803f9f068193758ad1621de6ae5b`, matches the release `SHA256SUMS` |
| GNN weights | embedded at build (`GNNWeights.h`, "LongPhase 2.1.1 GNN (retrained)", 687,358 float32) | `git show v2.1.2:GNNWeights.h \| sha256sum` = `48730a340818702a929bebf6bc2af2f6514c11f5aa1738326aca3224b5af9a73` |
| GNN threshold | 0.35 (default) | `Phasing.cpp:143`, `PhasingProcess.h:210` at v2.1.2 |
| WhatsHap | 2.8 (workEnv container, `whatshap-env`) | `phase --only-snvs --ignore-read-groups --reference` |
| HapCUT2 | 1.3.4 (`/disk/software/HapCUT2/build`) | `extractHAIRS --ont 1` + `HAPCUT2` defaults, on the PASS heterozygous SNVs of each call set |
| PEPPER-Margin-DeepVariant | r0.8 (`kishwars/pepper_deepvariant:r0.8-gpu`, run on CPU) | `call_variant --ont_r10_q20 -t 32` |
| minimap2 | 2.24-r1122 | `-y -ax map-ont`, reads with Dorado `qs >= 10` |
| dipcall | `dipcall.kit` (minimap2 2.20-r1061 inside) | `run-dipcall -t 16`, `scripts/truth/HG008N_v6.3_GRCh38.mak` |
| scorer | `longphase compare` of release v2.1 + `notes/benchmark_strata/score_phase.py` | agree on phased SNVs and switch errors in all 28 runs |
| reference | `GCA_000001405.15_GRCh38_no_alt_analysis_set.fa` (the paper's) | md5 `a6da8681616c05eb542f1d91606a7b2f` |
| HG008-N v6.3 hap1 / hap2 | frozen GIAB assembly (`nist-giab.s3…/NIST_asm_dev/HG008N_v6.3/`) | md5 `beeb11562553e23dd1117ca95187914b` / `9b264fcd02619cac7a1451e5ad45c651` |
| reads | HG008-N-P ONT-std, `03_13_24_R1041_GIAB_Normal_Pancreas{,_2,_3}`, Dorado 0.5.3 sup@v4.3.0 + 5mC_5hmC | GIAB `checksum.md5`, all OK |

The binary (dated 2026-10-25) is the one the manuscript's v2.1.2 runs used (`/ssd/longphase_process/v2.1.2/run_a.sh`). The comparator settings are those of the Supplementary software table (`tab:software` in `Supplementary.tex`).

## Phase reference

Built with `scripts/truth/prep.sh` and `make_truth.py`.

### Construction steps

1. **dipcall:** run on the two separate haplotype FASTAs (hap1 first) against the exact alignment reference. `0|1` means hap1 = REF. The labels carry no parental origin.
2. **Normalisation:** `bcftools reheader` to sample `HG008N`, then `bcftools norm -c x`. This deviates from the issue's `-c e`, which aborts at records whose GRCh38 base is an IUPAC code; `-c x` removes those 88 records (`norm_w.log`: only `NON_ACGTN_REF`).
3. **Scope and FILTER:** chr1–22 inside the dipcall BED. FILTER must be `.` or PASS; HET1/HET2/GAP1/GAP2 are dropped (280,892 records).
4. **Truth blocks:**
   - A block is a maximal GRCh38 interval covered by one hap1 and one hap2 dipcall alignment, with no assembly N-gap of either haplotype inside it. Gaps are mapped to GRCh38 through the alignment CIGAR.
   - A run of more than 100 kb without a heterozygous record also starts a new block (494 splits), because across such a run the assembly's phase rests on Hi-C rather than read linkage.
   - PS = block number.
   - Result: 2,320 reliable intervals, 2,655,599,900 bp, 2,781 blocks.
5. **Kept records:** heterozygous records only (2,876,008, of which 2,281,860 are SNVs). 15,611 heterozygous SNVs outside reliable intervals are dropped.

### Scored denominator

2,260,719 biallelic `0|1`/`1|0` SNVs. The 21,141 multiallelic `1|2` SNV records stay in the VCF but neither scorer counts them, matching the issue's `-m2 -M2` candidate set. Multiallelic records were not split.

### Checks (`truth/check_truth.txt`, `truth/validated`)

- **Format:** sample `HG008N`; 22 chromosomes; GT only `0|1`, `1|0`, `1|2`, `2|1`.
- **Alleles:** 300 random heterozygous SNVs all match the haplotype alignments.
- **PS:** no PS on two chromosomes, no overlapping PS intervals.
- **Swap test:** swapping hap1/hap2 in every odd block leaves both scorers' counts unchanged.

### Scoring rules

Blocks are truth PS × query PS, so no assessed pair crosses a truth block boundary. The somatic HG008-T benchmarks were not used.

### Independence of the reference

The truth is assembly-derived phase, not independent experimental truth.

- **Assembly inputs:** the v6.3 normal assembly used HiFi, HERRO-corrected ONT and Hi-C (Verkko). Its normal ONT data are from the pancreas and duodenum only; the normal tissues have no ultra-long reads.
- **Overlap with our reads:** the GIAB HERRO README lists the >25 kb reads of all three Normal Pancreas flow cells used here among the corrected reads. So the evaluation reads very likely contributed to the assembly, and no normal ONT-std run is known to be outside it.
- **Curation:** the normal assembly was curated with the matched tumour assembly.
- **Known limits:** the preprint reports remaining errors mainly around gaps; the mask excludes gaps and starts new blocks at them.

## Run order and commands

1. **Downloads** (`download.sh`, `download2.sh`): uBAMs from the GIAB mirror (md5 OK), READMEs and the v6.3 FASTAs.
2. **Gaps and dipcall** (`truth/gaps.py`, the dipcall `.mak`), then `truth/prep.sh`.
3. **Alignment** (`align.sh`): minimap2 as the paper, `qs >= 10` applied before alignment (same read set; the filter reads only the `qs` tag). Full-depth chr1–22 mean depth 56.491× (`samtools coverage`).
4. **Calling and phasing** (`run_calls.sh`):
   - Downsampling: `samtools view -s seed.fraction` with fraction = target / 56.491. Seeds 1–3 at 10× and 20×, seed 1 at 30×.
   - Variant calls: PEPPER per downsample. Its VCFs carry unphased genotypes only (no `|`, no PS).
   - Phasing: the four configurations on the same BAM, reference and VCF.
5. **HapCUT2 catch-up** (`hc_catchup.sh`): `run_calls_v0.sh` (the version launched first) gated HAPCUT2 on `[[ -s …done ]]` against empty `.done` files, so HAPCUT2 was skipped silently. `hc_catchup.sh` ran the identical command for every run. `run_calls.sh` is the fixed version; the diff to v0 is only that test (`-s` → `-e`).
6. **Resume after the controlling session ended** (`resume_20261112.sh`):
   - The session ended on 2026-11-12 at about 07:20 while the 20x_1 PEPPER container was still running.
   - The script waited for the container (exit 0), moved its VCF and reran `run_calls.sh`, which skips finished steps.
   - The 20x_1 PEPPER `.time` is therefore container start to exit, not `/usr/bin/time`.
7. **Scoring** (`score_all.sh`, then `summarize.py`): `longphase compare -t 4 --ignore-sample-name` and `score_phase.py`. The summary script checks that the two agree (`problems []`) and writes the TSVs and the figure.

## Runtime

Runtimes in `phase/*.time` are not comparable with the manuscript's runtime tables: other jobs (polyploid project) shared the machine throughout.

## Not done (out of scope of the minimum test, per the issue)

- HiFi data, the second normal tissue (duodenum), indels, SVs, methylation.
- A Nature-style version of the figure for the manuscript.
