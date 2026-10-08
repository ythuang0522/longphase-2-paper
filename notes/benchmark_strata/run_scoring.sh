#!/bin/bash
# Score every VCF of the issue-1 slim archive with score_phase.py.
#
#   run_scoring.sh DATA_DIR [OUT_DIR]
#
# DATA_DIR holds the unpacked archive tarballs of data/benchmark_strata/release/:
# truth/ (issue1_truth_and_regions.tar) and vcf/<group>/ (issue1_vcf_<group>.tar).
# SNV-only runs (item 4) are scored against v5.0q and v4.2.1, co-phasing runs
# (item 3) against v5.0q. Needs Python 3 with numpy; JOBS sets parallelism.
set -uo pipefail
DATA=$(realpath "${1:?usage: run_scoring.sh DATA_DIR [OUT_DIR]}")
OUT=${2:-out}
HERE=$(dirname "$(realpath "$0")")
export ISSUE1_REGIONS=$DATA/truth HERE OUT
export V5=$DATA/truth/HG002_GRCh38_v5.0q_smvar.chr1_22.vcf.gz
export V4=$DATA/truth/HG002_GRCh38_1_22_v4.2.1_benchmark_hifiasm_v11_phasetransfer.noDirty.vcf.gz
mkdir -p "$OUT"/item4/v5 "$OUT"/item4/v4 "$OUT"/item3/v5
one() {  # truth item path
  local n=$(basename "$3" .vcf.gz) tv=$V5
  [[ $1 == v4 ]] && tv=$V4
  local o="$OUT/$2/$1/$n"
  [[ -f "$o.tsv" ]] && return 0
  python3 "$HERE/score_phase.py" "$tv" "$3" "$o.tmp" \
    && mv "$o.tmp.tsv" "$o.tsv" && mv "$o.tmp.sw.tsv" "$o.sw.tsv" || echo "FAILED $1 $2 $3"
}
export -f one
for f in "$DATA"/vcf/*/*.vcf.gz; do
  case $(basename "$(dirname "$f")") in
    longphase|longphase_gnn|whatshap_v2.8_onlySNVs|hapcut2_v1.3.4)
      echo "v5 item4 $f"; echo "v4 item4 $f" ;;
    *) echo "v5 item3 $f" ;;
  esac
done | xargs -P "${JOBS:-8}" -L 1 bash -c 'one "$@"' _
python3 "$HERE/aggregate.py" "$OUT"
