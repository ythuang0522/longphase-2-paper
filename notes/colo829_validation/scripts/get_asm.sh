#!/bin/bash
# get_asm.sh: stream each COLO829BL DSA v3.0.0 haplotype (SMaHT portal, login key via the session proxy) once:
# md5 check against the portal record, gzip copy, and minimap2 -x asm5 against GRCh38 chr20 alone to find chr20 contigs.
set -euo pipefail
W=/home/user/work; cd $W; E=$W/tools/env/bin; U=https://data.smaht.org/supplementary-files
get() { local name=$1 url=$2 md5=$3
  curl -sSL "$url" | tee >(md5sum > asm/$name.md5) >(gzip -1 > asm/$name.fa.gz) |
    $E/minimap2 -x asm5 -t 2 ref/chr20.fa - > asm/$name.vs_chr20.paf 2> asm/$name.vs_chr20.log
  sleep 5; echo "$name md5 $(cut -d' ' -f1 asm/$name.md5) expected $md5"; }
get hap1 "$U/f28aedfe-b998-45d0-ac4f-b3c644479dd4/@@download/SMASFTH1B2J6.fa" eb8e3e174b17dacc5a6ece720195fc7e   # hapX
get hap2 "$U/51206418-cd5d-4286-a1d2-c5312a9f97df/@@download/SMASFK4V33V8.fa" "$(curl -sS -H 'Accept: application/json' https://data.smaht.org/supplementary-files/51206418-cd5d-4286-a1d2-c5312a9f97df/ | python3 -c 'import sys,json;print(json.load(sys.stdin)["md5sum"])')"   # hapY
