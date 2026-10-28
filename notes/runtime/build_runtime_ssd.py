"""runtime_ssd.tsv: SNV-only phasing re-timed with inputs and outputs on an SSD (2026-10-26 to 10-28).

Same workstation as runtime.tsv (Methods), but inputs and outputs on an ext4 file system on an NVMe SSD
(Crucial T710) instead of the hard-disk drive. Replicate 1, nanopore R10.4.1 10-60x and PacBio HiFi 10-50x;
one run at a time on an idle machine (no other phasing process, CPUs at least 95% idle over 10 s), page cache
cleared before every run, one run each; /usr/bin/time -v. Scripts in ssd/ (run.sh: LongPhase -t 24 at 10, 20,
..., 60x; run_wh.sh: WhatsHap at the same coverages; run_t1.sh: LongPhase -t 1; run_all.sh and run_rest.sh:
the remaining coverages, HiFi and HapCUT2).

  LongPhase 2  v2.1.2 release binary, `phase --ont` / `--pb`, -t 24 and -t 1; output identical to the paper's
               (-t 1 identical to -t 24)
  WhatsHap 2.8 `phase --only-snvs --ignore-read-groups`; output identical to the paper's VCFs
  HapCUT2      extractHAIRS (--ont 1 / --pacbio 1) + HAPCUT2, one timing over both. Input: the same calls as the
               other tools, unzipped, with the records whose GT is not two alleles from {0,1,2} removed by our
               script (HapCUT2 rejects them): nanopore refCall ./. (278-682 at 12x and 20-60x, none at 10, 14,
               16, 18x) and one 2/3 at 12x; HiFi as in runtime_hifi.tsv. Phased GT and PS identical to the
               paper's VCFs at 10, 14, 16 and 18x. Not re-timed (storage = HDD, values from runtime.tsv and
               runtime_hifi.tsv): nanopore 60x and HiFi 10-50x; at the coverages re-timed with the paper's
               input (10, 14, 16, 18x) the SSD times were within 2.5% of the HDD times.

Columns as runtime.tsv plus platform and storage."""
import os, re, csv
B = '/home/twolinin/lp_ext4/bench_readme/out'
HERE = os.path.dirname(os.path.abspath(__file__))

def secs(s):
    return sum(float(v) * 60 ** i for i, v in enumerate(reversed(s.split(':'))))

def gnu_v(p):
    t = open(p).read()
    g = lambda k: re.search(re.escape(k) + r':\s*(.+)', t).group(1).strip()
    return (round(secs(g('Elapsed (wall clock) time (h:mm:ss or m:ss)'))),
            round(float(g('User time (seconds)')) + float(g('System time (seconds)'))),
            int(g('Maximum resident set size (kbytes)')))

hdd = {}
for f, plat in (('runtime.tsv', 'nanopore'), ('runtime_hifi.tsv', 'HiFi')):
    for r in csv.DictReader(open(os.path.join(HERE, f)), delimiter='\t'):
        hdd[(plat, r['tool'], r['threads'], int(r['coverage']))] = r

TOOLS = (('LongPhase 2', 'phase + GNN', '24', 'static', 'hifi_static'),
         ('LongPhase 2', 'phase + GNN', '1', 'static_t1', 'hifi_static_t1'),
         ('WhatsHap 2.8', '--only-snvs', '1', 'whatshap', 'hifi_whatshap'),
         ('HapCUT2 1.3.4', 'extractHAIRS + HAPCUT2', '1', 'hapcut2', 'hifi_hapcut2'))
rows = []
for plat, covs in (('nanopore', (10, 12, 14, 16, 18, 20, 30, 40, 50, 60)), ('HiFi', (10, 20, 30, 40, 50))):
    for tool, conf, th, pre_n, pre_h in TOOLS:
        for c in covs:
            p = os.path.join(B, f'{pre_n if plat == "nanopore" else pre_h}_{c}x_1.time')
            if os.path.exists(p):
                rows.append([plat, tool, conf, th, c, *gnu_v(p), 'SSD'])
            elif (plat, tool, th, c) in hdd:
                r = hdd[(plat, tool, th, c)]
                rows.append([plat, tool, conf, th, c, r['wall_s'], r['cpu_s'], r['max_rss_kb'], 'HDD'])
with open(os.path.join(HERE, 'runtime_ssd.tsv'), 'w') as o:
    o.write('platform\ttool\tconfiguration\tthreads\tcoverage\twall_s\tcpu_s\tmax_rss_kb\tstorage\n')
    for r in rows:
        o.write('\t'.join(map(str, r)) + '\n')
print(len(rows), 'rows')
