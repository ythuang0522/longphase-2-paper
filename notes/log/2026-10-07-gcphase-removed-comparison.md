# GCphase removed from the comparison, 2026-10-07 (author decision)

**GCphase removed from the comparison, 2026-10-07 (author decision).** GCphase was run with the
command from its README (`python GCphase.py -vcf … -bam … -output …`; GitHub `baimawjy/GCphase`
main `ffa7e8b`, 2023-10-17), on the full PEPPER-Margin-DeepVariant output. Its source shows why the
results were near random (read, not run): `get_info.py:18-19` is its only genotype test and skips
records whose genotype starts with `1`; it does not read FILTER, so refCall `0/0` records are kept;
`get_info.py:128-135` compares single read bases with the REF/ALT strings (indels and multi-allelic
sites cannot match); `phasingSNP.py:76-82` drops only sites with ≥85% one allele or a single
minority read; `outputResult.py` rewrites every phased position to `0|1`/`1|0`. In the 10× replicate-1
output, 1,194,969 of 3,470,770 phased sites (34.4%) were refCall `0/0`, 99.4% of them with a PEPPER
VAF ≥ 0.15. GCphase therefore needs a VCF of biallelic heterozygous (`0/1`) SNVs only. Changes:
Methods (comparison paragraph) states the exclusion and the reason; Results drops the GCphase
fold-change and its todo ("three" → "two further phasers"); Fig. 2 legend (f), Supplementary
Table 5 (row removed), Supplementary Fig. 10 caption, Supplementary Table 8 (rows removed, "seven" →
"six configurations") and `make_results_figs.py` (`sfig10` tools, Table 8 loop) updated. The
GCphase entry in Supplementary Table 6 (studies that use LongPhase) is unrelated and kept.
**Not yet regenerated** (no TeX/matplotlib on the analysis machine): `suppfig10_more_tools.pdf` still
draws GCphase — run `python3 figures-source/make_results_figs.py` and `make`. The `gcphase` columns
remain in `supplementary.xlsx` (Supplementary Data 1); delete them or mark them as excluded.
