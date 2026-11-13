#!/bin/bash
# download2.sh: the three HG008-N-P uBAMs in parallel (one connection each, GIAB S3 mirror: ~13 MB/s per connection vs ~4 MB/s from the NCBI FTP; same files and sizes), then md5 check.
cd /disk/research/HG008/ubam
F=https://giab.s3.amazonaws.com/data_somatic/HG008/Liss_lab/Northeastern_ONT-std_20240422/HG008-N-P_ubams
for i in "" _2 _3; do f=03_13_24_R1041_GIAB_Normal_Pancreas$i.dorado_0.5.3_5mC_5hmC
  ( wget -q -c $F/$f.bam && wget -q -c $F/$f.summary.txt && echo "$(date '+%F %T') $f done" ) & done; wait
grep "HG008-N-P_ubams/.*\.bam$" checksum.md5 | sed 's|HG008-N-P_ubams/||' | md5sum -c - && echo "$(date '+%F %T') md5 OK" || echo "$(date '+%F %T') md5 FAILED"
echo "$(date '+%F %T') download done"
