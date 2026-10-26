# SV phasing accuracy against the T2T-HG002 assembly (issue #10)

Replicate 1 at every coverage of the paper (nanopore 10–60×, PacBio HiFi 10–50×), two inputs (SNVs + SVs;
SNVs + indels + SVs), LongPhase 2 with and without GNN correction, WhatsHap 2.8 and, on HiFi, HiPhase 1.7.0:
100 runs. SV phase is scored against the T2T-HG002 Q100 v1.1 dipcall VCF, SNVs against GIAB v5.0q (chr1–22),
as the issue asks.

## Files

- `sv_phasing.tsv`: one row per run × SV type (`DEL`, `INS`, `all`) × size class (`50-999`, `1000-9999`,
  `>=10000`, `all`); the columns of the issue plus `phased_no_block_snv` (phased SVs whose block has no
  SNV in the truth, or a tie, so they cannot be oriented). In every row
  `right + wrong + phased_hom_in_truth + phased_no_truth_match + phased_no_block_snv = sv_phased`.
- `snv.tsv`: the same runs, SNV results of `longphase compare` (v5.0q), with the path of every output VCF.
- `score_sv_phase.py`: the SV scoring of twolinin/longphase#136 (reproduces its values exactly, see Checks).
- `score_issue10.py`: scores all 100 runs and writes the two tables.
- `scripts/run_b.sh` (Sniffles, LongPhase), `scripts/run_c.sh` (inputs, WhatsHap, HiPhase), `scripts/run_c2.sh`
  (the last WhatsHap jobs of `run_c.sh`, moved off the hard disk to finish sooner; same command).

## Versions and differences from the issue

- **LongPhase 2 v2.1.2** (release, static binary), not #136 at `b521eb1`. v2.1.2 contains #136 and two
  further SV changes: a variant whose votes all come from SVs starts a new block (an SV is no longer the
  only link between two blocks), and `--sv-threshold` is 0.20 with `--ont` (0.10 with `--pb`). Its
  SNV-only and SNV + indel output is identical to v2.1.1.
- **Sniffles 2.8.0 with `--reference`** (and `--output-rnames`), on nanopore and HiFi, instead of "the same
  options as the nanopore calls in `sniffles_v2.8/`", which were made without `--reference`. All three
  tools phase the same new calls. Calls: `/disk/research/v2.1.2/sniffles/sniffles_{c}x_1.vcf`,
  `/disk/research/v2.1.2/pacbio/sniffles/sniffles_hifi_{c}x.vcf`.
- **LongPhase 2 input**: the PEPPER VCF and the Sniffles VCF unchanged, as in the paper (`-s` PEPPER VCF,
  `--sv-file`, `--indels` for the SNV + indel + SV input). Without `--indels` LongPhase does not phase
  indels, so the SNV + SV runs use the same SNVs as an SNV-only VCF would.
- **WhatsHap and HiPhase input**: one VCF made by `notes/competitors/scripts/merge_sv.py` (PEPPER calls,
  SNV-only for the SNV + SV input, plus the sequence-resolved Sniffles DEL/INS, chr1–22). This conversion
  is ours. Records left out (INV, DUP, BND, symbolic INS, N at POS), per run (the same for both inputs):
| Run | DEL | INS | left out |
|---|---|---|---|
| nanopore 10× | 9,099 | 12,187 | 296 |
| nanopore 12× | 9,715 | 12,842 | 326 |
| nanopore 14× | 10,106 | 13,088 | 349 |
| nanopore 16× | 10,278 | 13,331 | 332 |
| nanopore 18× | 10,499 | 13,401 | 367 |
| nanopore 20× | 10,609 | 13,440 | 347 |
| nanopore 30× | 10,996 | 13,569 | 369 |
| nanopore 40× | 11,207 | 13,489 | 354 |
| nanopore 50× | 11,227 | 13,425 | 346 |
| nanopore 60× | 11,254 | 13,361 | 349 |
| HiFi 10× | 8,027 | 11,052 | 377 |
| HiFi 20× | 9,682 | 13,389 | 509 |
| HiFi 30× | 10,146 | 13,807 | 580 |
| HiFi 40× | 10,315 | 13,956 | 564 |
| HiFi 50× | 10,408 | 14,016 | 578 |

  HiPhase kept every SV record in its output (for example 23,953 of 23,953 at HiFi 30×) and logged no
  rejected record.
- LongPhase ran with `-t 12`, several runs at a time, on a shared machine; these runs are not for timing. Every run
  has its `/usr/bin/time -v` output (`*.log` of LongPhase, `*.time` of WhatsHap per chromosome and HiPhase).

## Scoring

- Truth: dipcall records with an allele on both haplotypes (no `.`), chr1–22; SVs are DEL/INS of at
  least 50 bp; SNVs heterozygous one-base records.
- Scored set: the heterozygous Sniffles DEL/INS of the merged input (ID `Sniffles2.*`), the same records for
  every tool; each record is found in a tool's output by chromosome, position and ID (LongPhase: the
  `_SV.vcf`).
- A phased DEL/INS matches a truth SV of the same type, size within 70%, and position within 1 kb or, for
  a deletion, at least 50% reciprocal overlap (nearest match); its phase is compared with the truth after
  orienting its block by the majority of its SNVs.
- A first version of `score_sv_phase.py` took every record of 50 bp or more as an SV. With the
  SNV + indel + SV input this also scored PEPPER indels of 50 bp or more (about 840 at HiFi 30×) for
  WhatsHap and HiPhase but not for LongPhase, whose SV records are in the `_SV.vcf`; it also mixed up
  records that share a position. Both are fixed; the tables are from the fixed version.

## Checks

1. Against the values of #136 (right / wrong):

| Run | LongPhase 2 (#136 → v2.1.2) | `--disableGNN` | WhatsHap 2.8 |
|---|---|---|---|
| ONT 10×, SNV+SV | 7,497 / 830 → 7,613 / 778 | 7,627 / 1,118 → 7,757 / 1,040 | 8,099 / 1,625 → 8,096 / 1,622 |
| ONT 30×, SNV+SV | 9,649 / 720 → 9,702 / 683 | 9,666 / 919 → 9,664 / 923 | 10,008 / 1,361 → 10,027 / 1,332 |
| ONT 30×, SNV+indel+SV | 8,737 / 967 → 8,774 / 938 | | 8,376 / 1,660 → 8,386 / 1,644 |
| HiFi 30×, SNV+SV | 10,187 / 715 → 10,142 / 663 | 10,349 / 865 → 10,308 / 810 | 10,405 / 1,101 → 10,427 / 1,073 |
| HiFi 30×, SNV+indel+SV | 9,156 / 761 → 9,145 / 727 | | 8,685 / 1,069 → 8,692 / 1,069 |

   Right within 2% everywhere. LongPhase with GNN has 3–7% fewer wrong SVs (without GNN −7% to +0.4%), mostly
   from the block rule of v2.1.2; WhatsHap moves by at most 2.5%, from the new Sniffles calls. The scorer, run on the #136 WhatsHap output, gives
   the #136 values exactly (HiFi 30×: 10,405 / 1,101 and 8,685 / 1,069).
2. The sum in every row equals `sv_phased` (100 of 100 `all`/`all` rows).
3. LongPhase SNVs of the nanopore SNV + indel + SV runs against the `Indel+SV` rows of `co-phase_Detail`
   (v2.1.1, old Sniffles calls): phased SNVs within 0.006%, SNV switch error rate within ±2% (relative).

## Results

- **Nanopore.** LongPhase 2 has the lowest SV phasing error rate at every coverage with both inputs: SNVs + SVs
  5.8–11.3% against WhatsHap's 11.2–18.7%; SNVs + indels + SVs 7.2–12.1% against 16.3–22.1%. WhatsHap has
  1.8–2.3 times as many wrong SVs. With SNVs + SVs, WhatsHap phases 0.7–6.3% more SVs correctly; with
  indels LongPhase phases 0.9–8.2% more.
- **HiFi, against WhatsHap.** LongPhase 2 lower at every coverage (5.8–6.6% against 8.9–9.4%; with indels
  7.1–7.8% against 9.9–12.4%).
- **HiFi, against HiPhase.** With SNVs + SVs, HiPhase's error rate is about the same (5.4–6.4% against
  5.8–6.6%; lower at 10, 20, 40 and 50×, higher at 30×; 0.95–1.12 times LongPhase's wrong SVs) and it
  phases 6.8–9.0% more SVs correctly. With indels, LongPhase is lower at 10–30× (7.2–7.4% against
  7.7–8.6%) and HiPhase at 40 and 50× (7.1 and 6.9% against 7.8 and 7.1%); HiPhase phases 15–19% more SVs
  correctly.
- GNN correction lowers the LongPhase error rate at every coverage (nanopore by 0.7–5.6 points, HiFi by
  1.0–2.4 points); the number of correctly phased SVs changes by −1.9% to +2.5%.


**Nanopore, SNV+SV** — SV phasing error rate wrong / (right + wrong), % (right)

| Tool | 10× | 12× | 14× | 16× | 18× | 20× | 30× | 40× | 50× | 60× |
|---|---|---|---|---|---|---|---|---|---|---|
| LongPhase 2 | 9.3 (7,613) | 11.3 (8,196) | 10.0 (8,705) | 9.6 (8,953) | 9.0 (9,157) | 7.5 (9,380) | 6.6 (9,702) | 5.9 (9,811) | 5.8 (9,785) | 6.4 (9,673) |
| LongPhase 2 `--disableGNN` | 11.8 (7,757) | 14.2 (8,255) | 12.9 (8,709) | 11.6 (9,008) | 11.3 (9,174) | 9.4 (9,392) | 8.7 (9,664) | 6.6 (9,884) | 6.5 (9,849) | 7.2 (9,709) |
| WhatsHap 2.8 | 16.7 (8,096) | 18.7 (8,521) | 16.8 (9,021) | 15.6 (9,350) | 14.2 (9,619) | 12.9 (9,789) | 11.7 (10,027) | 12.3 (9,888) | 12.0 (9,849) | 11.2 (9,836) |

**Nanopore, SNV+indel+SV** — SV phasing error rate wrong / (right + wrong), % (right)

| Tool | 10× | 12× | 14× | 16× | 18× | 20× | 30× | 40× | 50× | 60× |
|---|---|---|---|---|---|---|---|---|---|---|
| LongPhase 2 | 10.8 (7,137) | 12.1 (7,683) | 11.2 (8,104) | 11.0 (8,250) | 9.9 (8,470) | 10.1 (8,536) | 9.7 (8,774) | 8.8 (8,869) | 7.2 (9,009) | 7.6 (8,881) |
| LongPhase 2 `--disableGNN` | 15.5 (7,170) | 17.8 (7,541) | 16.6 (7,937) | 16.1 (8,079) | 14.9 (8,287) | 14.3 (8,372) | 13.6 (8,581) | 11.6 (8,755) | 10.1 (8,876) | 11.5 (8,665) |
| WhatsHap 2.8 | 20.3 (7,071) | 21.6 (7,419) | 22.1 (7,592) | 20.8 (7,825) | 19.9 (8,015) | 17.1 (8,281) | 16.4 (8,386) | 17.5 (8,218) | 16.4 (8,267) | 16.3 (8,155) |

**PacBio HiFi, SNV+SV** — SV phasing error rate wrong / (right + wrong), % (right)

| Tool | 10× | 20× | 30× | 40× | 50× |
|---|---|---|---|---|---|
| LongPhase 2 | 5.8 (7,518) | 6.6 (9,650) | 6.1 (10,142) | 6.6 (10,214) | 6.0 (10,313) |
| LongPhase 2 `--disableGNN` | 6.8 (7,631) | 7.6 (9,839) | 7.3 (10,308) | 7.6 (10,372) | 7.3 (10,448) |
| WhatsHap 2.8 | 8.9 (7,887) | 9.4 (10,074) | 9.3 (10,427) | 9.0 (10,527) | 9.2 (10,514) |
| HiPhase 1.7.0 | 5.4 (8,029) | 6.3 (10,521) | 6.4 (10,930) | 5.8 (11,044) | 5.9 (11,028) |

**PacBio HiFi, SNV+indel+SV** — SV phasing error rate wrong / (right + wrong), % (right)

| Tool | 10× | 20× | 30× | 40× | 50× |
|---|---|---|---|---|---|
| LongPhase 2 | 7.2 (6,775) | 7.4 (8,717) | 7.4 (9,145) | 7.8 (9,245) | 7.1 (9,401) |
| LongPhase 2 `--disableGNN` | 9.6 (6,874) | 9.8 (8,857) | 9.2 (9,319) | 9.3 (9,424) | 8.7 (9,547) |
| WhatsHap 2.8 | 12.2 (6,590) | 12.4 (8,304) | 11.0 (8,692) | 9.9 (8,843) | 10.1 (8,838) |
| HiPhase 1.7.0 | 8.3 (7,824) | 8.6 (10,308) | 7.7 (10,857) | 7.1 (10,980) | 6.9 (11,010) |

