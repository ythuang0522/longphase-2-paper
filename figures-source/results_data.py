"""Load the benchmark tables behind Figs. 2-6 and Supplementary Tables 7-11.

Sources (repo root):
  supplementary.xlsx        per-run v5.0q metrics (JHL, 2026-10-04)
  20260924_GIAB421.txt      per-run v4.2.1 metrics (`longphase compare`)
Coverage labels are ints (10, 12, ..., 60); ONT 10-20x carry ten replicates,
ONT 30-60x and every HiFi coverage a single run.
"""
import os
import re
import statistics as st
from collections import defaultdict

import openpyxl

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
XLSX = os.path.join(ROOT, "supplementary.xlsx")
V421 = os.path.join(ROOT, "20260924_GIAB421.txt")

SNV_TOOLS = ["longphase_v2.0.1", "longphase_v2.1", "whatshap_v28", "hapcut2_v134",
             "margin_v231", "ralphi", "gcphase"]
SNV_COLS = ["psnv", "psnv_pct", "sw", "sw_pct", "ham", "nblock", "n50", "bsum"]
COPH_COLS = ["psnv", "psnv_pct", "pindel", "pindel_pct", "sw", "sw_pct", "ham",
             "nblock", "n50", "bsum"]
COPH_TOOLS = ["longphase_v2.0.1", "longphase_v2.1", "whatshap_v28"]


def _rows(ws):
    return [r for r in ws.iter_rows(values_only=True) if any(c is not None for c in r)][2:]


def _case(s):
    cov, rep = s.split("_")
    return int(cov.rstrip("x")), int(rep)


def load():
    """Return dict with keys 'snv', 'coph', 'calls', 'v421'.

    snv[platform][tool][cov] -> list of dicts (one per replicate)
    coph[config][tool][cov]  -> list of dicts (ONT only)
    calls[platform][cov]     -> list of dicts
    v421[tool][cov]          -> list of dicts
    """
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    snv = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in _rows(wb["SNV_Detail"]):
        plat = "ONT" if r[1].startswith("ONT") else "HiFi"
        cov, rep = _case(r[2])
        for i, tool in enumerate(SNV_TOOLS):
            vals = r[3 + 8 * i: 3 + 8 * (i + 1)]
            if vals[0] is None:
                continue
            d = dict(zip(SNV_COLS, vals)); d["rep"] = rep
            snv[plat][tool][cov].append(d)
    coph = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in _rows(wb["co-phase_Detail"]):
        cfg = r[2]
        cov, rep = _case(r[3])
        for i, tool in enumerate(COPH_TOOLS):
            vals = r[4 + 10 * i: 4 + 10 * (i + 1)]
            if vals[0] is None:
                continue
            d = dict(zip(COPH_COLS, vals)); d["rep"] = rep
            coph[cfg][tool][cov].append(d)
    calls = defaultdict(lambda: defaultdict(list))
    for r in _rows(wb["Variant_Calling"]):
        plat = "ONT" if r[1].startswith("ONT") else "HiFi"
        cov, rep = _case(r[2])
        calls[plat][cov].append(dict(zip(
            ["het_snv", "hom_snv", "het_indel", "het_sv", "hom_sv", "het_5mc"], r[3:9])))
    v421 = defaultdict(lambda: defaultdict(list))
    for line in open(V421):
        if not line.startswith("###") or line.startswith("###Sample"):
            continue
        f = line[3:].rstrip("\n").split("\t")
        m = re.match(r"(.+)_(\d+)x_(\d+)\.", f[0])
        tool, cov = m.group(1), int(m.group(2))
        v = [float(x) for x in f[1:]]
        v421[tool][cov].append(dict(zip(COPH_COLS, v)))
    return {"snv": snv, "coph": coph, "calls": calls, "v421": v421}


def ms(runs, key):
    """Mean and s.d. (0 for a single run) of `key` over replicate dicts."""
    xs = [float(r[key]) for r in runs if r.get(key) is not None]
    if not xs:
        return None, None
    return st.mean(xs), (st.stdev(xs) if len(xs) > 1 else 0.0)
