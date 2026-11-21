# HG008-N and COLO829BL in the manuscript: options (2026-11-21)

Status: author chose option A on 2026-11-21 (implemented; `notes/log/2026-11-21-other-individuals-option-a.md`).
Data: `notes/hg008_validation/`, `notes/colo829_validation/` (ported from `claude/youthful-lovelace-gdc2ku`, commit 61e7d00).

## 1. Problems in the current text and on the branch

| Where | Problem |
|---|---|
| Results, subsection 2, current HG008 sentence | It is between the HiFi paragraph and the block-contiguity paragraph. The contiguity paragraph goes back to HG002, so the reader jumps HG002 → HG008 → HG002. |
| Results, subsection 2 title | "across variant classes and sequencing platforms" does not cover a second genome. |
| Supplementary Note 7 ("Effect of GNN-based unphasing") | It holds the HG008 comparison against WhatsHap and HapCUT2. That comparison is not a GNN effect. |
| Branch text | "GNN correction removed 15–20% …" in Results: old term, and it attributes a result to the GNN (not permitted in Results). |
| Branch numbering | It cites Supplementary Fig. 3 and Table 5 from Results and renumbers Supplementary Figs. 3–18 and Tables 5–19. Too much change for one paragraph. |
| Discussion, limitations | "the HG008 test … against phase from an assembly built in part from the evaluated reads" and "phase references independent of the evaluated reads, is needed". COLO829BL now gives such a reference (assembly from SMaHT data, not from the ONT open-data reads). |

## 2. What COLO829BL adds, scientifically

1. **An independent phase reference.** The HG008 assembly contains the evaluated reads; the COLO829BL assembly does not. This is the strongest new point.
2. **A different variant caller.** Clair3 v1.2.0, not PEPPER-Margin-DeepVariant. Transfer holds with a caller that the model never saw. It also means that genome and caller change together.
3. **The same pattern as HG002.** Lower switch error rate at every coverage, fold difference from WhatsHap grows with coverage, 0.6–1.0 point lower completeness, similar N50.
4. **Limits.** One seed per coverage; one chemistry; up to 30×; Hamming distance at 30× favours WhatsHap (0.46% vs 0.51%).

The GNN-effect numbers (HG008-N 15–20%, COLO829BL 19–20%) belong in Supplementary Note 7 next to the held-out-chromosome result (14–25%). They are not in Results.

## 3. Options

| | A (recommended) | B | C (branch layout) |
|---|---|---|---|
| Results | One closing paragraph at the **end of subsection 2**, after block contiguity | New **final subsection** after the unphased-calls subsection | Paragraph at end of subsection 2 |
| Title change | Subsection 2 title unchanged | New title: "\toolname keeps lower switch error rates in two further individuals" | none |
| Results cites | Supplementary Note 8 only | Supplementary Note 8 only | Supplementary Fig. 3, Table 5 |
| Supplementary | New **Note 8 "Phasing of two further individuals"** (data, truth, comparison); Fig. 17 → two rows (HG008-N, COLO829BL); Table 21 → both individuals; Note 7 keeps only the GNN effect | same as A | New Fig. 3, Table 5; renumber Figs. 3–18 → 4–19, Tables 5–19 → 6–20 |
| Renumbering | none | none | 31 items |
| Flow | HG002 nanopore → HiFi → contiguity → other genomes: one story "lower error rates" closes with generalization | Results end on generalization; subsection 2 stays HG002 only; a one-paragraph subsection | as A, but cites figures out of the usual order |

Why A: it keeps the HG002 story continuous, it puts the generalization next to the claim it supports (lower switch error rates), and it needs no renumbering. B gives more weight but leaves a one-paragraph subsection after the runtime sentence.

## 4. Draft paragraph (option A; for B the same text under the new title)

Replaces the current HG008 sentence (results.tex line 82) and goes after the block-contiguity paragraph.

> We then applied the released model, with no retraining and no change of threshold or parameter, to nanopore data of two further individuals (Supplementary Note~8). HG008-N is normal pancreatic tissue from a donor with pancreatic cancer\cite{mcdaniel2025hg008}, and COLO829BL is a lymphoblastoid cell line matched to the COLO829 melanoma line\cite{sohn2026colo829}. Phase was scored against phase derived from a diploid assembly of each individual; the COLO829BL assembly was built from data other than the evaluated reads (Methods). In HG008-N, with the variant caller used for HG002, \toolname had SNV switch error rates of 0.026--0.058\% at 10--30$\times$, compared with 0.091--0.107\% for \whatshap and 0.137--0.144\% for \hapcut. In COLO829BL, with variant calls from Clair3\cite{zheng2022clair3}, \toolname had 0.018--0.065\%, compared with 0.044--0.144\% and 0.089--0.206\%. These rates were 1.8--3.6- and 2.2--2.4-fold lower than those of \whatshap, and the difference increased with coverage in both individuals. As in HG002, \toolname phased 0.6--1.0 percentage points fewer benchmark heterozygous SNVs than \whatshap, at block N50 values within 5\% of those of \whatshap. Block-wise Hamming distances were lowest for \toolname, except in COLO829BL at 30$\times$ (0.51\% versus 0.46\% for \whatshap).

Numbers: `hg008_summary.tsv`, `colo829_runs.tsv` (WH/LP2: HG008-N 1.83, 2.90, 3.58; COLO829BL 2.21, 2.34, 2.42; HC/LP2 3.2–5.4 in Supplementary only). HG008-N Hamming: lower than WhatsHap in 6 of 7 runs (one 10× replicate 1.366% vs 1.364%) — stated in Note 8, not in Results.

## 5. Other changes (same for A and B)

- **Methods:** "Second individual" → "Further individuals" (data, callers, seeds, truth; independence of each truth); line 101 and Data availability get COLO829BL.
- **Discussion, limitations:** replace "the HG008 test covered … built in part from the evaluated reads" with both individuals; keep the limits (one chemistry, ≤30×, one or three seeds, Clair3 changes caller and genome together); shorten "phase references independent of the evaluated reads, is needed" because COLO829BL has one.
- **Supplementary software table:** COLO829BL reads, COLO829BL assembly, Clair3 1.2.0.
- **Generator:** `sfig_hg008()` and `hg008_table()` extended to read both `*_runs.tsv` files.
- **Abstract:** unchanged unless the author asks (150-word limit).
- **Still open from the branch:** SMaHT data-use policy check; HG008-N and COLO829BL rows in Supplementary Data 1.
