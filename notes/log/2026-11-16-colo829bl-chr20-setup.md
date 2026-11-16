# COLO829BL phasing benchmark: setup (chr1-22, Clair3; in progress)

Started a third-individual check modelled on `notes/hg008_validation/`, on chr20 only (cloud container: 4 cores,
15 GB RAM). Script: `notes/colo829_validation/scripts/run_calls.sh`. No manuscript text or figure changed.

- Reads: ONT open data `colo829_2024.03`, COLO829BL sup BAMs PAU59807 + PAU61427 (R10.4.1, 5 kHz, Dorado sup@v4.3.0,
  aligned to GRCh38 by ONT), chr20 region, `qs >= 10`.
- Reference md5 `a6da8681616c05eb542f1d91606a7b2f` (the paper's); LongPhase v2.1.2 binary sha256 `d61a744b…` (as HG008).
- Truth: SMaHT COLO829BL DSA v3.0.0 (Verkko 2.1; hapX SMASFTH1B2J6 md5 `eb8e3e174b17dacc5a6ece720195fc7e`, hapY
  SMASFK4V33V8). Open access but the portal requires a login; blocked until an access key is available. Truth rules
  will be those of HG008 (`notes/hg008_validation/README.md`, Phase reference), fixed before any phasing output is scored.

## Update (same day): chr1-22, Clair3, one seed

- Scope widened to chr1-22 (author), run one chromosome at a time on this machine; scores will be summed over chromosomes.
- Caller: Clair3 v1.2.0 with ONT model `r1041_e82_400bps_sup_v430` (author: "Do it with clair3"); the paper and HG008 used
  PEPPER-Margin-DeepVariant r0.8, so COLO829BL tests a new genome and a new caller together.
- Seeds: seed 1 only at 10, 20 and 30× (author, to halve calling time).
- Depth for the downsample fraction: 51.895×, estimated from the remote BAM index (scaled to the measured chr20 depth).
- dipcall: whole assembly against whole GRCh38; minimap2 single-threaded with `-K100M` and an 8 GB swap file after two
  out-of-memory kills.
