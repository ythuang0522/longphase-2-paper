"""Issue #3 runtime table (notes/runtime/runtime.tsv).

WhatsHap, HapCUT2 and LongPhase at 24 threads: the GNU time output at the end
of the logs of the paper's own runs (lab server, /disk/research). LongPhase at
1 thread: timed 2026-10-09 with /usr/bin/time -v on the same
machine and disk, all other jobs stopped (/ssd/longphase_process/runtime/time)."""
import os, re
R = '/disk/research'
T = '/ssd/longphase_process/runtime/time'

def secs(s):
    return sum(float(v) * 60 ** i for i, v in enumerate(reversed(s.split(':'))))

def gnu(p):  # default GNU time line: wall, user+sys, peak RSS
    m = re.findall(r'([\d.]+)user ([\d.]+)system ([\d:.]+)elapsed \d+%CPU \(\d+avgtext\+\d+avgdata (\d+)maxresident',
                   open(p).read())[-1]
    return secs(m[2]), float(m[0]) + float(m[1]), int(m[3])

def gnu_v(p):  # time -v
    t = open(p).read()
    g = lambda k: re.search(re.escape(k) + r':\s*(.+)', t).group(1).strip()
    return (secs(g('Elapsed (wall clock) time (h:mm:ss or m:ss)')),
            float(g('User time (seconds)')) + float(g('System time (seconds)')),
            int(g('Maximum resident set size (kbytes)')))

rows = []
for c in (10, 12, 14, 16, 18, 20, 30, 40, 50, 60):  # replicate 1 at every coverage of the paper
    a, b = gnu(f'{R}/longphase/longphase_{c}x_1.log'), gnu_v(f'{R}/longphase_gnn/longphase_gnn_{c}x_1.log')
    rows.append(('LongPhase 2', 'phase + GNN', 24, c, a[0] + b[0], a[1] + b[1], max(a[2], b[2])))
    t1 = f'{T}/longphase_v2.1_gnn-t1_{c}.time'  # timed separately; skip coverages not yet timed
    if os.path.exists(t1):
        rows.append(('LongPhase 2', 'phase + GNN', 1, c, *gnu_v(t1)))
    rows.append(('WhatsHap 2.8', '--only-snvs', 1, c, *gnu(f'{R}/whatshap_v2.8/only/whatshap_v28_onlySNVs_{c}x_1.log')))
    h = f'{R}/hapcut2_v1.3.4/hapcut2_v134_{c}x_1.log'
    if 'Command terminated by signal' not in open(h).read():  # 30x, 40x: log overwritten by an interrupted rerun
        rows.append(('HapCUT2 1.3.4', 'extractHAIRS + HAPCUT2', 1, c, *gnu(h)))
with open('runtime.tsv', 'w') as f:
    f.write('tool\tconfiguration\tthreads\tcoverage\twall_s\tcpu_s\tmax_rss_kb\n')
    for r in rows:
        f.write(f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]:.0f}\t{r[5]:.0f}\t{r[6]}\n')
