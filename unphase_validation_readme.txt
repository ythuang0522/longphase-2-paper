# Validating GNN-unphased SNVs against the T2T-HG002 assembly

## Purpose

The GNN correction removes roughly 56,000–64,000 phased SNVs per genome. The
obvious objection is that fewer switch errors simply follow from scoring fewer
variants. This experiment answers a narrower and more decisive question:

**Are the removed SNVs variants at all?**

Rather than asking whether the GIAB benchmark contains them, it asks what the
T2T-HG002 v1.1 diploid assembly shows at those positions once it is aligned
back to GRCh38. If both haplotypes align to a position and both match the
reference, HG002 carries no variant there, and unphasing that call loses
nothing.

A note on independence: GIAB v5.0q is itself derived from this assembly, so
this is not an independent truth set. What it adds is **coverage**: the
assembly alignment extends well beyond the curated benchmark regions, so it
can speak about positions the benchmark leaves unassessed — which is where
most of the removed calls turn out to live.

## Input files

All from the GIAB v5.0q release:
`https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/v5.0q/`

| File | Role |
| --- | --- |
| `dipcall_output/GRCh38_HG2-T2TQ100-V1.1_dipcall-z2k.dip.bed` | regions where **both** assembled haplotypes align 1:1 to GRCh38. 409 intervals, 2.84 Gb. This is the raw dipcall output, before any benchmark curation. |
| `dipcall_output/GRCh38_HG2-T2TQ100-V1.1_dipcall-z2k.dip.vcf.gz` | variants called from that alignment, in GRCh38 coordinates. |
| `HG002_GRCh38_v5.0q_smvar.benchmark.bed` | the curated small-variant benchmark regions (optional, used for a conservative second pass). |

The assembly was aligned with dipcall v0.3 (minimap2, `-z200000,10000`); the
benchmark BED is that same alignment after excluding assembly gaps, breaks
inside satellites and segmental duplications, inversions, SV-affected regions
and known dipcall artefacts.

`dip.vcf.gz` and `HG002_GRCh38_v5.0q_smvar.vcf.gz` were verified to contain an
identical set of 5,945,525 records — the benchmark curation is applied to the
BED, not to the VCF. Either VCF can therefore be used; the script uses the
dipcall one to keep VCF and BED paired consistently.

Analysis inputs:

| File | Role |
| --- | --- |
| `longphase_60x_1.vcf` | LongPhase output before GNN correction |
| `longphase_gnn_60x_1.vcf` | the same run after GNN correction |

## Classification

A site counts as removed by the GNN when it is phased (`|`) in the baseline
and unphased (`/`) after correction. Only SNVs are considered. Each removed
site falls into exactly one class:

| Class | Condition | Interpretation |
| --- | --- | --- |
| `hom_wt` | inside `dip.bed`, absent from `dip.vcf.gz` | both haplotypes match GRCh38 — no variant exists, nothing lost |
| `variant` | inside `dip.bed`, present in `dip.vcf.gz` | the assembly confirms a variant — real phasing information lost |
| `unassessed` | outside `dip.bed` | no 1:1 assembly alignment: centromere, satellite or segmental duplication |

BED intervals are 0-based half-open and VCF positions 1-based, so a position
is inside an interval when `start < POS <= end`.

The same classification is applied to a random sample of SNVs that remained
phased. This background rate is what the removed set must be compared against:
without it, a high `unassessed` fraction could simply reflect the assembly's
own coverage gaps.

## Running it

Run it from the directory holding the three GIAB files; with no arguments it
uses the paths of this study:

```bash
bash run_t2t_validation.sh
```

Equivalent to:

```bash
bash run_t2t_validation.sh \
    /disk/research/longphase/longphase_60x_1.vcf \
    /disk/research/longphase_gnn/longphase_gnn_60x_1.vcf \
    . .
```

The four optional arguments are baseline VCF, corrected VCF, resource
directory and output directory. `SAMPLE_N` sets the background sample size
(default 50,000). Only awk, sort, join, comm, shuf and zcat are used — no
bcftools, no bedtools. A 60× genome takes a few minutes, dominated by reading
the 5.9 M-record assembly VCF.

Every output is prefixed `unphase_validation_`:

| File | Content |
| --- | --- |
| `unphase_validation_results.txt` | the full run report: class counts, removed-vs-background rates, odds ratio, per-chromosome enrichment, 1 Mb hotspots |
| `unphase_validation_removed_classified.tsv` | one row per removed site: chrom, pos, inside_dip_bed, assembly_variant, class |
| `unphase_validation_removed.txt`, `unphase_validation_background.txt` | the site lists the analysis ran on |
| `unphase_validation_*.inbed.txt` | per-site `dip.bed` membership for both sets |

The three files worth committing are this README, the script, and
`unphase_validation_results.txt`.

## Results (HG002 ONT R10.4.1, 60×, replicate 1)

56,076 SNVs were phased by LongPhase and unphased by the GNN.

| Class | Count | Share |
| --- | --- | --- |
| outside `dip.bed` (unassessed) | 49,475 | 88.23% |
| inside, assembly shows no variant (`hom_wt`) | 3,421 | 6.10% |
| inside, assembly confirms a variant | 3,180 | 5.67% |

Against a background of 50,000 randomly sampled SNVs that stayed phased:

| | inside `dip.bed` |
| --- | --- |
| stayed phased (background) | 92.61% |
| removed by the GNN | 11.77% |

Restricted to the curated benchmark regions, 549 removed sites remain, of which
136 (24.77%) have no benchmark variant and 413 (75.23%) do.

### Reading these numbers

**The removed calls are concentrated where the assembly cannot align.** 92.6%
of ordinary phased SNVs sit inside `dip.bed`, against 11.8% of the removed
ones. The enrichment holds on every autosome — 3.9× on chr18 up to 475× on
chr19 — so it does not come from a few chromosomes with poor assembly
coverage; if it did, the background rate would rise with it and the ratio
would stay near 1.

chr19 is the clearest single case: only 0.09% of its background SNVs fall
outside `dip.bed`, yet 42.8% of its removed ones do. chr19 carries no large
satellite arrays, so the model is responding to "the assembly cannot align
here", not to one particular chromosomal structure.

**The hotspots are pericentromeric.** The unassessed sites cluster at
chr11 51–54 Mb and chr18 15–20 Mb, the centromeric and satellite regions of
those chromosomes. GRCh38 represents these with modelled alpha-satellite
sequence rather than real individual sequence, which is why no assembly aligns
1:1 there and why read mapping in these regions is unreliable to begin with.

**Where the assembly can speak, most removals are not variants.** Of the 6,601
sites inside `dip.bed`, 51.8% are confirmed homozygous reference. The
remaining 3,180 are the genuine cost of the correction, in the same range as
the ~4% real-heterozygote figure obtained independently from the benchmark.

**chrY is the one reversal** (ratio 0.4). HG002 is male, chrY is haploid and
largely repetitive, and 50% of its background SNVs already fall outside
`dip.bed`. It is noted for completeness and does not affect the conclusion.

### Caveats

- v5.0q derives from this assembly, so the benchmark-based and
  assembly-based analyses are not independent. The assembly's value here is
  reach beyond the benchmark regions, not independent confirmation.
- `dip.bed` is raw dipcall output and does not exclude the assembly errors and
  mosaic variants that the benchmark curation removes. A small number of
  `hom_wt` calls could therefore reflect assembly error.
- `unassessed` means the assembly offers no 1:1 alignment, not that a variant
  is absent. The claim these sites support is about mappability, not about
  genotype.
