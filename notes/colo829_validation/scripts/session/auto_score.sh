#!/bin/bash
# score each chromosome once its three runs are finished (hc done for 10x_1, 20x_1, 30x_1)
cd /home/user/work
while true; do left=0
  for i in $(seq 1 22); do c=chr$i
    [[ -e score/$c.scored ]] && continue; left=1
    [[ $(ls phase/hc_[0-9]*_$c.done 2>/dev/null | wc -l) -eq 3 ]] || continue
    bash /home/user/longphase-2-paper/notes/colo829_validation/scripts/score_chr.sh $c && touch score/$c.scored && echo "$(date '+%F %T') $c scored"
  done
  [[ $left -eq 0 ]] && { echo "$(date '+%F %T') all scored"; break; }
  sleep 300
done
