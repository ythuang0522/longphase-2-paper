# COLO829BL external validation of the frozen GNN

A third individual after HG002 and HG008-N. The LongPhase 2 v2.1.2 release (GNN trained on HG002, threshold 0.35) was run
on COLO829BL nanopore reads. COLO829BL is the lymphoblastoid line matched to the COLO829 melanoma line.

- **Runs:** 3 inputs (seed 1 at 10, 20 and 30×) × 4 configurations = 12 phasing runs on chr1–22.
- **Truth:** assembly-derived phase from the SMaHT COLO829BL DSA v3.0.0 assembly, built under the HG008 rules (fixed on
  2026-11-10, before any phasing output existed).
- **Frozen model:** nothing was retrained, tuned, re-thresholded or re-masked on COLO829BL.
- **Where and when:** run from 2026-11-16 to 2026-11-19 in a cloud container (4 cores, 15 GB RAM, about 39 GB of disk),
  one chromosome at a time.
- **In the manuscript:** since 2026-11-20, with HG008-N, as Supplementary Fig. 3 and Supplementary Table 5
  (`notes/log/2026-11-20-other-individuals-in-manuscript.md`).

**Difference from HG008:** the variant caller is Clair3 v1.2.0, not PEPPER-Margin-DeepVariant r0.8 (author: "Do it with
clair3"). This experiment therefore tests a new genome and a new caller together.

## Result

Genome-wide, chr1–22. Denominator: 2,254,361 truth heterozygous biallelic SNVs.

| coverage (measured) | LongPhase 2 (GNN) | `--disableGNN` | WhatsHap 2.8 | HapCUT2 1.3.4 |
|---|--:|--:|--:|--:|
| **SNV switch error rate (%)** | | | | |
| 10× (10.8×) | **0.065** | 0.081 | 0.144 | 0.206 |
| 20× (21.7×) | **0.023** | 0.029 | 0.054 | 0.114 |
| 30× (32.5×) | **0.018** | 0.022 | 0.044 | 0.089 |
| **SNV switch errors / assessed pairs** | | | | |
| 10× | 1,380 / 2,119,647 | 1,717 / 2,123,683 | 3,075 / 2,141,167 | 4,403 / 2,139,779 |
| 20× | 502 / 2,163,111 | 623 / 2,164,457 | 1,184 / 2,177,835 | 2,484 / 2,176,944 |
| 30× | 392 / 2,163,901 | 482 / 2,164,953 | 954 / 2,177,761 | 1,948 / 2,177,184 |
| **Completeness (%)** | | | | |
| 10× | 94.44 | 94.62 | 95.39 | 95.32 |
| 20× | 96.29 | 96.34 | 96.94 | 96.90 |
| 30× | 96.28 | 96.33 | 96.90 | 96.87 |
| **Block-wise Hamming (%)** | | | | |
| 10× | **2.78** | 3.07 | 3.41 | 3.33 |
| 20× | **0.55** | 0.66 | 0.74 | 0.97 |
| 30× | 0.51 | 0.53 | **0.46** | 0.61 |
| **Block N50 (kb)** | | | | |
| 10× | 714 | 741 | 745 | 750 |
| 20× | 1,004 | 1,028 | 1,002 | 1,001 |
| 30× | 1,229 | 1,239 | 1,191 | 1,192 |

Measured depth is the length-weighted `samtools coverage` mean of the downsampled reads over 21 chromosomes. chr21 was
fetched during the setup test and has no per-run coverage file.

### 1. Does the HG002-trained GNN reduce COLO829BL phase errors?

Yes. Compared with the identical `--disableGNN` run (`results/colo829_gnn_effect.tsv`):

- **Switch errors:** 19.6%, 19.4% and 18.7% fewer at 10, 20 and 30×.
- **Per chromosome:** the GNN never adds switch errors in any of the 66 chromosome × run pairs.
- **Hamming distance:** lower in every run.
- **Cost:**
  - completeness is 0.05–0.17 percentage point lower (1,022–3,912 fewer benchmark SNVs phased);
  - there are 9.7–13.6% more blocks;
  - block N50 is 0.8–3.6% lower.

The GNN leaves 38.7–40.6k calls unphased per run. Of these, 1.0–3.9k (2.5–9.9%) are benchmark heterozygous SNVs.

### 2. Does the full method keep its advantage over WhatsHap and HapCUT2?

Yes.

- **Switch error rate:** 2.2-, 2.3- and 2.4-fold lower than WhatsHap and 3.2-, 4.9- and 4.9-fold lower than HapCUT2 at
  10, 20 and 30×.
- **Per chromosome:** LongPhase 2 with GNN has the fewest switch errors in all 66 chromosome × run pairs
  (`results/colo829_by_chr.tsv`).
- **Completeness:** 0.95, 0.65 and 0.62 percentage point lower than WhatsHap.
- **Block N50:** 4% lower than WhatsHap and HapCUT2 at 10×, about equal at 20×, 3% higher at 30×.

These ratios are close to those of HG008-N (1.8–3.6-fold against WhatsHap, 2.4–5.4-fold against HapCUT2), with a
different caller.

### Results against the method

- **Hamming distance at 30×:** WhatsHap (0.463%) is below LongPhase 2 with GNN (0.507%).
- **Switch errors from 20× to 30×:** they rise on three chromosomes (chr7 51 → 60, chr16 20 → 36, chr21 4 → 5), while
  the genome-wide count falls (502 → 392). WhatsHap's chr16 count stays flat (54 → 53).
- **Seeds:** one seed per coverage, so there is no spread. A seed measures sampling variability within one individual,
  not an independent genome.

## Files

| path | content |
|---|---|
| `results/colo829_runs.tsv` | genome-wide metrics per run, 12 rows (`longphase compare` and `score_phase.py` columns; same columns as `hg008_runs.tsv`) |
| `results/colo829_by_chr.tsv` | per chromosome × tool × run: assessed SNV pairs, switch errors, phased SNVs (264 rows) |
| `results/colo829_gnn_effect.tsv` | GNN vs `--disableGNN` per run: Δ switch errors, withheld calls and benchmark SNVs, blocks, N50 |
| `results/colo829_fig.pdf` | switch error rate / completeness / block N50 against coverage (draft panel, not in Nature style yet) |
| `results/raw/by_chr/` | raw scorer output per chromosome × tool × run (264 runs): `longphase compare` (`.tsv`), `score_phase.py` (`.sp.tsv`) and its switch-error pairs (`.sp.sw.tsv`) |
| `results/raw/genome/` | the same for the 12 genome-wide (chr1–22) runs; `summarize.py` reads these |
| `results/raw/depth/` | `samtools coverage` of every downsampled run and chromosome (chr21 missing, see Result) |
| `truth/COLO829BL_truth.blocks.bed` | scoring mask = truth phase blocks on GRCh38 (2,723 blocks, 4th column = PS) |
| `truth/COLO829BL_dsa3_GRCh38.dip.bed` | dipcall confidence BED |
| `truth/hap{1,2}.gaps.bed` | assembly N-gaps in assembly coordinates |
| `truth/COLO829BL_truth.counts.tsv` | exclusion counts |
| `truth/check_truth.txt`, `truth/norm.log` | truth checks; normalisation log |
| `truth/hap{1,2}.md5`, `truth/hap2.expected_md5` | assembly checksums (computed while streaming, and the portal's record) |
| `scripts/` | every script, in run order below |
| `scripts/session/` | the container's restart, scoring and compression loops (`restart.sh`, `auto_score.sh`, `compress_loop.sh`) |

### Raw data

Only the scorer output is in Git (author, 2026-11-20: "just the raw numbers for generating figures"). The large
files were in `/home/user/work` of the cloud session `session_016MpzQAd54HaJjtG7j5Wqwe`
(https://claude.ai/code/session_016MpzQAd54HaJjtG7j5Wqwe), about 1 GB compressed:

- `phase/`: 12 runs × 22 chromosomes of phased VCFs (`{lp_gnn,lp_nognn,wh}_<run>_chrN.vcf.gz`,
  `hapcut2_<run>_chrN.phased.VCF.gz`) and per-step `.time`/`.log`; `genome/`: the concatenated per-run VCFs.
- `calls/`: Clair3 VCFs per run and chromosome (`clair3_<run>_chrN.vcf.gz`, `.pass_het_snv.vcf`).
- `truth/`: `COLO829BL_truth.vcf.gz`, the dipcall output and intermediates.

The session transcript records every command. The container is reclaimed after inactivity, after which these files
are gone; they can be rebuilt from `scripts/` (every input is public: the ONT reads, and the assembly, which needs a
free SMaHT portal login). The CRAMs were deleted after each run.

## Versions and checksums

| item | version | checksum / source |
|---|---|---|
| LongPhase 2 | v2.1.2 release binary, tag `6b8f2dd` | `longphase_linux-x64` sha256 `d61a744bdbbdd3144a05f6924b1d482d351a803f9f068193758ad1621de6ae5b` (the HG008 binary) |
| GNN | embedded weights, threshold 0.35 (default) | as HG008 |
| WhatsHap | 2.8 (bioconda `whatshap-2.8-py311h3cb736e_1`) | `phase --only-snvs --ignore-read-groups --reference` |
| HapCUT2 | 1.3.4 (bioconda `hapcut2-1.3.4-h577a1d6_1`) | `extractHAIRS --ont 1` + `HAPCUT2` defaults, on the PASS heterozygous SNVs of each call set |
| Clair3 | v1.2.0 (`hkubal/clair3@sha256:1430f7b520674bb282b5a1ba165e8555b012df67b9cdb22ff3d48f26cf1474a3`) | `run_clair3.sh --platform=ont`, model `r1041_e82_400bps_sup_v430` (Clair3 v2 cannot load it); unphased output |
| dipcall | 0.3 (bioconda), minimap2 2.31-r1302, k8 1.2 | `run-dipcall -t 2`, Makefile edits in `scripts/truth/run_dipcall.sh` |
| samtools / bcftools | 1.21 / 1.21 | |
| scorer | `longphase compare` of release v2.1 (sha256 `21e4f0f842af1d4765bc41bc7839656e6ee6e87dccc6ea7fff876aee411b2c65`) + `notes/benchmark_strata/score_phase.py` | agree on phased SNVs and switch errors in all 12 genome-wide runs and all 264 chromosome runs |
| reference | `GCA_000001405.15_GRCh38_no_alt_analysis_set.fa` (the paper's) | md5 `a6da8681616c05eb542f1d91606a7b2f` |
| COLO829BL DSA v3.0.0 hap1 / hap2 | SMaHT, hapX `SMASFTH1B2J6` / hapY `SMASFK4V33V8` (Verkko 2.1) | md5 `eb8e3e174b17dacc5a6ece720195fc7e` / `6ec3b743686d756a97400ece61080697`, both equal to the portal record |
| reads | ONT open data `colo829_2024.03`, COLO829BL sup BAM `PAU59807` (R10.4.1, 5 kHz, Dorado 0.5.2 sup@v4.3.0 + 5mCG_5hmCG, aligned to GRCh38 by ONT) | `s3://ont-open-data/colo829_2024.03/basecalls/colo829bl/sup/PAU59807.d052sup4305mCG_5hmCGvHg38.bam`; `PAU61427` not used |

## Phase reference

Built with `scripts/truth/run_dipcall.sh` and `make_truth.py`, a copy of the HG008 script with chromosomes read from the
environment. Rules: `notes/hg008_validation/README.md`, Phase reference.

### Differences from HG008

- **Contig cutting:** assembly contigs are cut into 20 Mb pieces before dipcall (`chunk_fasta.py`), so that minimap2
  fits in 15 GB. Truth blocks therefore also end at every cut. This is the only rule change, and it can only shorten
  blocks.
- **Memory settings:** minimap2 ran single-threaded with `-K100M`, after two out-of-memory kills, using an 8 GB swap
  file that was deleted after the truth was built.

### Construction

1. **dipcall:** hap1 = hapX first, so `0|1` means hap1 = REF. The labels carry no parental origin.
2. **Normalisation:** `bcftools norm -c x` (88 records with IUPAC reference bases removed).
3. **Scope and FILTER:** chr1–22 inside the dipcall BED. FILTER must be `.` or PASS; HET1/HET2/GAP1/GAP2 are dropped
   (287,434 records).
4. **Truth blocks:**
   - A block is one hap1 and one hap2 alignment, with no N-gap on either haplotype and no cut.
   - A run of more than 100 kb without a heterozygous record also starts a new block (224 splits).
   - Result: 2,536 reliable intervals, 2,654,584,732 bp, 2,723 blocks.
5. **Kept records:**
   - 2,884,068 heterozygous records, of which 2,274,723 are SNVs.
   - 29,385 records outside reliable intervals are dropped.
   - Scored denominator: the 2,254,361 biallelic `0|1`/`1|0` SNVs. Multiallelic `1|2` records stay in the VCF, but
     neither scorer counts them.

### Checks

`truth/check_truth.txt`:

- **Format:** sample `COLO829BL`; 22 chromosomes; GT only `0|1`, `1|0`, `1|2`, `2|1`.
- **Alleles:** 300 random heterozygous SNVs all match the haplotype alignments.
- **PS:** no PS on two chromosomes, no overlapping PS intervals.

### Scoring rules

- **Switch errors and Hamming distance:** blocks are truth PS × query PS, as for HG008.
- **Block count and N50:** each phaser's native values, from the query alone.

### Independence of the reference

The truth is assembly-derived phase, not independent experimental truth.

- **Whether our reads entered the assembly:** most likely not. The portal record of the hapX file (`SMASFTH1B2J6`,
  checked 2026-11-21) lists the assembly inputs as SMaHT data from UWSC GCC (ONT ultra-long, PacBio Revio, Hi-C,
  Fiber-seq; Verkko 2.1). The evaluation reads are ONT's own open-data run (`PAU59807`). The record cites Sohn et al.,
  Cell 189, 6630 (2026), doi:10.1016/j.cell.2026.09.033.
- **Cell line:** COLO829BL is a cell line, so the reads and the assembly come from different cultures.
- **Access:** the files are open access (`access_status: Open`); the record also gives a public S3 URL, so no login is
  needed to download them.

## Run order and commands

1. **Assembly** (`get_asm.sh`): each haplotype was streamed once from the SMaHT portal, using a login key held as a
   network secret of the session, never written to disk, with an md5 check.
2. **Truth** (`truth/chunk_fasta.py`, `truth/gaps.py`, `truth/run_dipcall.sh`, `make_truth.py`, `check_truth.py`).
3. **Reads, calls and phasing** (`run_calls.sh`), per chromosome and run:
   - **Reads:** streamed from the remote BAM with `qs >= 10`, MM/ML/mv tags dropped. Downsampled with
     `samtools view -s 1.<fraction>` and stored as CRAM against the paper's reference. Three download attempts.
   - **Downsampling fraction:** target / 51.895×. The chr1–22 depth was estimated from the remote index
     (`samtools idxstats` read counts, scaled to the measured `qs >= 10` depth of chr20), because streaming the whole BAM
     once just for depth would cost about 7 h. Seed 1 at each coverage: the author asked for one seed per coverage, to
     halve calling time.
   - **Clair3:**
     - chr1 and chr18–22 were called per whole chromosome.
     - chr2–17 were called per 20 Mb window (`--bed_fn`), each window keeping only records with POS inside it, and
       concatenated. The windows were added on 2026-11-17, because container restarts were killing whole-chromosome
       Clair3 runs.
   - **Phasing:** the four configurations on the same CRAM, reference and VCF. The CRAM was deleted after each run.
4. **Scoring:**
   - **Per chromosome** (`score_chr.sh`, triggered by `auto_score.sh`).
   - **Genome-wide** (`score_genome.sh`): the 22 outputs per run concatenated and scored against the whole truth.
   - **Summary** (`summarize.py`): checks that the two scorers agree and that genome-wide counts equal the per-chromosome
     sums (`problems []`).

### Incidents, all resolved before the final scores

- **Duplicate records at window edges:**
  - Clair3 emits records just past a `--bed_fn` window.
  - Before the POS filter was added: chr2 10x failed to index (unsorted), and chr17 20x/30x each had one duplicate
    record (POS 40,000,017).
  - Fix for chr17: deduplicated (kept the last occurrence), then the 20× and 30× runs were phased again.
  - The chr17 20×/30× scores had been written before the re-phasing and were not redone at the time. `summarize.py`
    caught this, because WhatsHap's genome-wide counts differed from the per-chromosome sums by one pair. chr17 20× and
    30× were then rescored from the current files.
  - Only WhatsHap changed (+1 phased SNV, +1 pair, the same switch errors), and the tables above use the rescored values.
- **Container restarts:**
  - The container restarted many times, roughly every 1–2 h while the session was idle. Each restart stopped every
    process and the Docker daemon.
  - `scripts/session/restart.sh` restarts Docker and the loops and removes partial outputs (`calls/*.out`, `bam/*.tmp`).
  - Finished steps are skipped by their `.done` files.
  - One per-chromosome scoring (chr8) was interrupted mid-write. Its score files were deleted and recomputed.
- **Download failures:** one network failure while fetching reads (chr12 30×) led to the three-attempt retry.

### Not checked

- **Clair3 from CRAM vs BAM:** on chr21 10×, LongPhase 2, WhatsHap and HapCUT2 gave byte-identical output from the CRAM
  and from the BAM. Clair3 itself was not compared between the two.

## Runtime

Not measured. The container's 4 cores were shared by two calling or phasing jobs at a time, and processes were restarted
many times, so `phase/*.time` is not comparable with the manuscript's runtime tables. HG008 has an SSD-protocol runtime
measurement.

## Not done

- HiFi data, the tumour line COLO829, indels, SVs, methylation.
- More seeds per coverage.
- A Nature-style figure for the manuscript.
