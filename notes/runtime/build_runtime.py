"""Issue #3 runtime table (notes/runtime/runtime.tsv).

WhatsHap and HapCUT2: the GNU time output at the end of the logs of the paper's own runs
(lab server, /disk/research). LongPhase 2 (v2.1.2 release binary, one `phase` command with GNN correction)
at 24 threads and at 1 thread (10x and 60x): /usr/bin/time -v of the 2026-10-26 runs
(/ssd/longphase_process/v2.1.2/run_a.sh: one run at a time on an idle machine, page cache cleared
before each run; output identical to v2.1.1). HapCUT2 at 30x and 40x: the
original logs were overwritten by an interrupted rerun, so both were re-timed on 2026-10-16 with the
same binaries, inputs and commands, one at a time on an idle machine (H2 below); the phased
genotypes are identical to the paper's VCFs (chrom, pos, sample column of every record).

runtime_hifi.tsv, PacBio HiFi (replicate 1, 10-50x), same columns: LongPhase 2 (v2.1.2, -t 24) from
run_a.sh as above. WhatsHap at 10x and 20x re-timed on 2026-10-16/17 (HR below; the original runs shared the machine
with other jobs, LongPhase 20x at 25% CPU and WhatsHap 10-20x at 73-82%), one at a time on an idle
machine with the BAM read once before each run; phased genotypes identical to the paper's VCFs.
WhatsHap 30-50x from the original logs (95-99% CPU). HapCUT2 (extractHAIRS --pacbio 1 + HAPCUT2)
from its 2026-10-16 runs, one at a time on an idle machine. The v2.1 and v2.1.1 rows are in git
history (v2.1: `phase` plus the separate `gnn` command)."""
import os, re
R = '/disk/research'
T = '/ssd/longphase_process/runtime/time'
G = '/disk/research/v2.1.2'
H2 = '/ssd/longphase_process/runtime/hapcut2_rerun'
HR = '/ssd/longphase_process/runtime/hifi_retime'
P = '/disk/research/pacbio'

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
    rows.append(('LongPhase 2', 'phase + GNN', 24, c, *gnu_v(f'{G}/longphase_gnn/longphase_gnn_{c}x_1.log')))
    t1 = f'{G}/longphase_gnn_t1/longphase_gnn_t1_{c}x_1.log'  # timed at 10x and 60x only
    if os.path.exists(t1):
        rows.append(('LongPhase 2', 'phase + GNN', 1, c, *gnu_v(t1)))
    rows.append(('WhatsHap 2.8', '--only-snvs', 1, c, *gnu(f'{R}/whatshap_v2.8/only/whatshap_v28_onlySNVs_{c}x_1.log')))
    h = f'{H2 if c in (30, 40) else R + "/hapcut2_v1.3.4"}/hapcut2_v134_{c}x_1.log'
    rows.append(('HapCUT2 1.3.4', 'extractHAIRS + HAPCUT2', 1, c, *gnu(h)))
with open('runtime.tsv', 'w') as f:
    f.write('tool\tconfiguration\tthreads\tcoverage\twall_s\tcpu_s\tmax_rss_kb\n')
    for r in rows:
        f.write(f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]:.0f}\t{r[5]:.0f}\t{r[6]}\n')

hifi = []
for c in (10, 20, 30, 40, 50):
    hifi.append(('LongPhase 2', 'phase + GNN', 24, c, *gnu_v(f'{G}/pacbio/longphase_hifi/longphase_hifi_{c}x_1.log')))
    wh = f'{HR}/whatshap_v28_hifi_onlySNVs_{c}x_1.time'
    hifi.append(('WhatsHap 2.8', '--only-snvs', 1, c, *(gnu_v(wh) if c in (10, 20) else
                 gnu(f'{P}/whatshap_v28_hifi_onlySNVs_{c}x_1.log'))))
    hifi.append(('HapCUT2 1.3.4', 'extractHAIRS + HAPCUT2', 1, c, *gnu(f'{P}/hapcut2_v1.3.4/hapcut2_v134_hifi_{c}x_1.log')))
with open('runtime_hifi.tsv', 'w') as f:
    f.write('tool\tconfiguration\tthreads\tcoverage\twall_s\tcpu_s\tmax_rss_kb\n')
    for r in hifi:
        f.write(f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]:.0f}\t{r[5]:.0f}\t{r[6]}\n')
