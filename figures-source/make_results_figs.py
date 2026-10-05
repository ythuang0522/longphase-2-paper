#!/usr/bin/env python3
"""Generate the Results figures (Figs. 2-6), Supplementary Figs. 10-14 (except
13, which is the retained raster) and Supplementary Tables 7-12 for the
LongPhase 2 manuscript.

Every number is read from the files listed in results_data.py, from
unphase_validation_results.txt, or -- for the three data sets that exist only
as figure drafts -- from the constants below, each tagged with its source
draft. Nothing is read off a plot.

Run from the repository root with any Python that has matplotlib and openpyxl:
    python3 figures-source/make_results_figs.py
(On this machine the base miniforge numpy is broken; use
 ~/miniforge3/envs/gemini/bin/python3.)

Outputs:
    figures/fig{2..6}_*.pdf
    figures/supp/suppfig{10,11,12,14}_*.pdf
    figures-source/supp_tables.tex   (\\input by Supplementary.tex)
"""
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from results_data import load, ms, ROOT

D = load()
OUT = os.path.join(ROOT, "figures")
SUPP = os.path.join(OUT, "supp")

# ------------------------------------------------------------------ style ---
MM = 1 / 25.4
plt.rcParams.update({
    "font.family": "Arial",   # Helvetica.ttc exposes no bold face to matplotlib
    "font.size": 6.5,
    "axes.titlesize": 6.5,
    "axes.labelsize": 6.5,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "lines.linewidth": 1.0,
    "lines.markersize": 3,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
    "legend.frameon": False,
    "savefig.dpi": 300,
})

# Tool colours (colour-blind safe; LongPhase 2 in reds as in the drafts).
C = {
    "lp_gnn": "#B2182B",   # LongPhase 2 with correction
    "lp":     "#F4A582",   # LongPhase 2 without correction
    "wh":     "#2166AC",   # WhatsHap --only-snvs
    "wh_ind": "#92C5DE",   # WhatsHap default (co-phases indels)
    "hc":     "#525252",   # HapCUT2
    "margin": "#1B7837",
    "ralphi": "#762A83",
    "gc":     "#BF812D",
    "meth":   "#35978F",
}
NAME = {
    "lp_gnn": "LongPhase 2", "lp": "LongPhase 2 without GNN",
    "wh": "WhatsHap (SNVs only)", "wh_ind": "WhatsHap (SNVs + indels)",
    "hc": "HapCUT2", "margin": "Margin", "ralphi": "Ralphi", "gc": "GCphase",
    "meth": "MethPhaser",
}
XLSX_TOOL = {"lp": "longphase_v2.0.1", "lp_gnn": "longphase_v2.1",
             "wh": "whatshap_v28", "hc": "hapcut2_v134", "margin": "margin_v231",
             "ralphi": "ralphi", "gc": "gcphase"}
COVS = [10, 12, 14, 16, 18, 20, 30, 40, 50, 60]
BAR_COVS = [10, 20, 30, 40, 50, 60]
HIFI_COVS = [10, 20, 30, 40, 50]

# Co-phasing configurations: xlsx sheet label -> display name, colour.
CFG = [
    ("SNV", "SNV", "#4D4D4D"),
    ("SV", "+SV", "#80CDC1"),
    ("Mod", "+5mC", "#35978F"),
    ("Indel", "+indel", "#FDB863"),
    ("Indel+SV", "+indel+SV", "#E08214"),
    ("Mod+Indel", "+indel+5mC", "#B35806"),
    ("Indel+Mod+SV", "all four", "#542788"),
]


FIGW = 183 * MM          # Nature double-column width; figures are saved at exactly this width
_LETTERS = []


def letter(ax, s, **_):
    """Panel letter (8 pt bold), placed in save() at the left edge of the panel's
    tick labels / axis label, level with the top of the panel. An empty left title
    reserves the vertical space under constrained layout."""
    ax.set_title(" ", loc="left", fontsize=8)
    _LETTERS.append((ax, s))


def new_fig(h_mm, nrows=1, ncols=1, **kw):
    fig, axs = plt.subplots(nrows, ncols, figsize=(FIGW, h_mm * MM), layout="constrained", **kw)
    fig.get_layout_engine().set(w_pad=2 * MM, h_pad=1.5 * MM, wspace=0.04, hspace=0.06)
    return fig, axs


def single_band(ax, lo=25, hi=65):
    """No-op. Coverages with a single down-sampling run are explained in the legends and
    Methods instead of being shaded (author decision, 2026-10-06): subsamples of the
    70x data set would share 43-85% of reads at 30-60x, so replicates there add nothing."""
    return


PLOT_COVS = [10, 20, 30, 40, 50, 60]   # main/supp line plots; every coverage is in the tables


def snv_series(tool, key, plat="ONT", covs=PLOT_COVS):
    xs, m, s = [], [], []
    for c in covs:
        runs = D["snv"][plat][XLSX_TOOL[tool]].get(c)
        if not runs:
            continue
        a, b = ms(runs, key)
        xs.append(c); m.append(a); s.append(b)
    return xs, m, s


def coph_series(cfg, tool, key, covs=PLOT_COVS):
    if cfg == "SNV":
        return snv_series({"longphase_v2.0.1": "lp", "longphase_v2.1": "lp_gnn"}[tool], key, covs=covs)
    xs, m, s = [], [], []
    for c in covs:
        runs = D["coph"][cfg][tool].get(c)
        if not runs:
            continue
        a, b = ms(runs, key)
        xs.append(c); m.append(a); s.append(b)
    return xs, m, s


# Per-tool glyphs. HapCUT2 and WhatsHap nearly coincide in phased fraction, N50 and
# low-coverage Hamming distance, so they differ in marker and line style and are
# dodged by +-0.5x along the coverage axis to keep both visible.
STY = {
    "lp_gnn": dict(marker="o", ls="-", mfc=None, dx=0.0),
    "lp":     dict(marker="o", ls="--", mfc="white", dx=0.0),
    "wh":     dict(marker="D", ls="-", mfc=None, dx=0.0),
    "hc":     dict(marker="s", ls="--", mfc="white", dx=0.0),
    "margin": dict(marker="^", ls="-", mfc=None, dx=0.0),
    "ralphi": dict(marker="v", ls="-", mfc=None, dx=0.0),
    "gc":     dict(marker="P", ls="-", mfc=None, dx=0.0),
}


def tline(ax, t, xs, m, s, scale=1.0, label=None, ms_=2.6):
    st = STY[t]
    line(ax, [x + st["dx"] for x in xs], m, s, C[t], ls=st["ls"], marker=st["marker"],
         scale=scale, label=label, mfc=st["mfc"])


def thandle(t, label=None):
    st = STY[t]
    return Line2D([], [], color=C[t], ls=st["ls"], marker=st["marker"], ms=2.8,
                  mfc=st["mfc"] or C[t], label=label or NAME[t])


def line(ax, xs, m, s, color, ls="-", marker="o", label=None, scale=1.0, mfc=None, z=3):
    """Mean line with markers; replicate s.d. as a light band (zero width for single runs)."""
    m = [v * scale for v in m]; s = [v * scale for v in s]
    if any(s):
        ax.fill_between(xs, [a - b for a, b in zip(m, s)], [a + b for a, b in zip(m, s)],
                        color=color, alpha=0.18, lw=0, zorder=z - 1)
    ax.plot(xs, m, color=color, ls=ls, marker=marker, ms=2.6, mfc=mfc or color, mew=0.6,
            label=label, zorder=z)


def cov_axis(ax, covs=(10, 20, 30, 40, 50, 60)):
    ax.set_xticks(list(covs))
    ax.set_xticklabels([f"{c}" for c in covs])
    ax.set_xlabel("Coverage (×)")


def save(fig, path):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    fig.set_layout_engine("none")
    W, H = fig.get_size_inches() * fig.dpi
    for ax, s_ in [(a, l) for a, l in _LETTERS if a.figure is fig]:
        tb = ax.get_tightbbox(r)
        fig.text(max(tb.x0, 0) / W, min(tb.y1, H) / H, s_, fontsize=8, fontweight="bold",
                 va="top", ha="left")
    fig.savefig(path)
    w_mm = fig.get_size_inches()[0] * 25.4
    plt.close(fig)
    print(f"wrote {os.path.relpath(path, ROOT)} ({w_mm:.0f} mm wide)")


# ============================================================ Figure 2 =====
def fig2():
    """SNV-only phasing on nanopore data: LongPhase 2 (full method) vs other tools."""
    tools = ["wh", "hc", "lp_gnn"]   # HapCUT2 drawn over WhatsHap, where they coincide
    fig, axs = new_fig(100, 2, 3)
    specs = [
        ("psnv_pct", "Phased SNVs (%)", None, 1),
        ("sw_pct", "Switch error rate (%)", "log", 1),
        ("ham", "Hamming distance (%)", None, 1),
        ("n50", "Block N50 (Mb)", None, 1e-6),
    ]
    for ax, (key, lab, yscale, sc), L in zip(axs.flat, specs, "abcd"):
        single_band(ax)
        for t in tools:
            xs, m, s_ = snv_series(t, key)
            tline(ax, t, xs, m, s_, scale=sc, label=NAME[t])
        if yscale:
            ax.set_yscale(yscale)
            ax.set_yticks([0.02, 0.05, 0.1, 0.2, 0.3])
            ax.set_yticklabels(["0.02", "0.05", "0.1", "0.2", "0.3"])
            ax.minorticks_off()
        ax.set_ylabel(lab); cov_axis(ax); letter(ax, L)
    ax = axs.flat[4]
    single_band(ax)
    xs, q, _ = snv_series("lp_gnn", "sw_pct")
    for ref in ("wh", "hc"):
        _, r, _ = snv_series(ref, "sw_pct")
        st = STY[ref]
        ax.plot(xs, [a / b for a, b in zip(r, q)], color=C[ref], marker=st["marker"], ls=st["ls"],
                mfc=st["mfc"] or C[ref], ms=2.6)
    ax.set_ylim(0, 5.2); ax.set_ylabel("Switch-error-rate ratio\n(comparator / LongPhase 2)")
    cov_axis(ax); letter(ax, "e")
    ax.legend(handles=[thandle("wh", "WhatsHap"), thandle("hc", "HapCUT2")],
              loc="lower right", fontsize=5.5, handlelength=2.6)
    ax = axs.flat[5]
    for t in ["hc", "wh", "margin", "lp_gnn"]:
        runs = D["snv"]["ONT"][XLSX_TOOL[t]][10]
        x, sx = ms(runs, "sw_pct"); y, sy = ms(runs, "n50")
        ax.errorbar([x], [y / 1e6], xerr=[sx], yerr=[sy / 1e6], fmt=STY[t]["marker"], color=C[t], ms=3.2,
                    mfc=STY[t]["mfc"] or C[t], mew=0.8, elinewidth=0.6, capsize=0)
        off = {"hc": (0, 6), "wh": (-2, -7), "lp_gnn": (5, 0), "margin": (5, 0)}[t]
        ax.annotate({"wh": "WhatsHap"}.get(t, NAME[t]), (x, y / 1e6), xytext=off,
                    textcoords="offset points", fontsize=5.5, color=C[t], va="center",
                    ha="center" if t in ("hc", "wh") else "left")
    ax.set_xlim(0.04, 0.31); ax.set_ylim(0.15, 1.1)
    ax.set_xlabel("Switch error rate (%), 10×"); ax.set_ylabel("Block N50 (Mb), 10×")
    letter(ax, "f")
    h = [thandle(t) for t in tools]
    fig.legend(handles=h, loc="outside upper center", ncol=4, handlelength=2.6, columnspacing=1.2)
    save(fig, os.path.join(OUT, "fig2_snv_comparison.pdf"))


# ============================================================ Figure 3 =====
F3 = [  # key, label, colour, line style, marker, v5.0q source, v4.2.1 tool name
    ("lp_gnn", "LongPhase 2, SNVs", C["lp_gnn"], "-", "o", ("snv", "longphase_v2.1"), "longphase_gnn"),
    ("lp_ind", "LongPhase 2, +indels", C["lp_gnn"], "--", "s", ("coph", "Indel", "longphase_v2.1"), "longphase_coh_indel_gnn"),
    ("lp_isv", "LongPhase 2, +indels+SVs", C["lp_gnn"], ":", "^", ("coph", "Indel+SV", "longphase_v2.1"), "longphase_coh_indel_sv_gnn"),
    ("wh", "WhatsHap, SNVs only", C["wh"], "-", "o", ("snv", "whatshap_v28"), "whatshap_v28_onlySNVs"),
    ("wh_ind", "WhatsHap, SNVs + indels", C["wh"], "--", "s", ("coph", "Indel", "whatshap_v28"), "whatshap_v28"),
    ("hc", "HapCUT2", C["hc"], "-", "o", ("snv", "hapcut2_v134"), "hapcut2_v134"),
]


def f3_runs(src, cov):
    if src[0] == "snv":
        return D["snv"]["ONT"][src[1]][cov]
    return D["coph"][src[1]][src[2]][cov]


def fig3():
    """The same SNV-only VCFs under GIAB v4.2.1 and v5.0q."""
    fig, axs = new_fig(100, 2, 2)
    series = [x for x in F3 if x[0] in ("wh", "hc", "lp_gnn")]
    series.sort(key=lambda x: ["wh", "hc", "lp_gnn"].index(x[0]))
    panels = [("v421", "sw", "Switch errors", "a"), ("v50q", "sw", "Switch errors", "b"),
              ("v421", "ham", "Hamming distance (%)", "c"), ("v50q", "ham", "Hamming distance (%)", "d")]
    for ax, (bench, key, lab, L) in zip(axs.flat, panels):
        single_band(ax)
        for k, name, col, ls, mk, src, v421name in series:
            xs, m_, s_ = [], [], []
            for c in PLOT_COVS:
                runs = D["v421"][v421name][c] if bench == "v421" else f3_runs(src, c)
                a_, b_ = ms(runs, key)
                xs.append(c); m_.append(a_); s_.append(b_)
            tline(ax, k, xs, m_, s_, label=name)
        ax.set_ylabel(lab); cov_axis(ax); letter(ax, L)
        ax.set_title("GIAB v4.2.1" if bench == "v421" else "T2T-HG002-derived v5.0q", fontsize=6.5)
    for a_, b_ in ((axs[0, 0], axs[0, 1]), (axs[1, 0], axs[1, 1])):
        top = max(a_.get_ylim()[1], b_.get_ylim()[1])
        a_.set_ylim(0, top); b_.set_ylim(0, top)
    h = [thandle(t) for t in ("lp_gnn", "wh", "hc")]
    fig.legend(handles=h, loc="outside upper center", ncol=4, handlelength=2.6, columnspacing=1.2)
    save(fig, os.path.join(OUT, "fig3_two_benchmarks.pdf"))


# ============================================================ Figure 4 =====
F4 = [  # label, colour, style, marker, getter(cov) -> runs
    ("LongPhase 2, SNVs", C["lp_gnn"], "-", "o", lambda c: D["snv"]["ONT"]["longphase_v2.1"][c]),
    ("LongPhase 2, +indels", C["lp_gnn"], "--", "s", lambda c: D["coph"]["Indel"]["longphase_v2.1"][c]),
    ("LongPhase 2, all four classes", C["lp_gnn"], ":", "^", lambda c: D["coph"]["Indel+Mod+SV"]["longphase_v2.1"][c]),
    ("WhatsHap, SNVs", C["wh"], "-", "D", lambda c: D["snv"]["ONT"]["whatshap_v28"][c]),
    ("WhatsHap, +indels", C["wh"], "--", "D", lambda c: D["coph"]["Indel"]["whatshap_v28"][c]),
    ("HapCUT2, SNVs", C["hc"], "--", "s", lambda c: D["snv"]["ONT"]["hapcut2_v134"][c]),
]


def fig4():
    """Co-phasing compared with WhatsHap (and HapCUT2 for reference)."""
    fig, axs = new_fig(100, 2, 2)
    specs = [("sw_pct", "SNV switch error rate (%)", 1, "a"), ("n50", "Block N50 (Mb)", 1e-6, "b"),
             ("pindel_pct", "Phased indels (%)", 1, "c")]
    for ax, (key, lab, sc, L) in zip(axs.flat, specs):
        single_band(ax)
        for name, col, ls, mk, get in F4:
            if key == "pindel_pct" and "indel" not in name and "four" not in name:
                continue
            xs, m_, s_ = [], [], []
            for c in PLOT_COVS:
                a_, b_ = ms(get(c), key)
                xs.append(c); m_.append(a_); s_.append(b_)
            line(ax, xs, m_, s_, col, ls=ls, marker=mk, scale=sc, label=name)
        if key == "sw_pct":
            ax.set_yscale("log"); ax.minorticks_off()
            ax.set_yticks([0.02, 0.05, 0.1, 0.2, 0.3]); ax.set_yticklabels(["0.02", "0.05", "0.1", "0.2", "0.3"])
        ax.set_ylabel(lab); cov_axis(ax); letter(ax, L)
    ax = axs.flat[3]
    for name, col, ls, mk, get in F4:
        x, sx = ms(get(20), "sw_pct"); y, sy = ms(get(20), "n50")
        ax.errorbar([x], [y / 1e6], xerr=[sx], yerr=[sy / 1e6], fmt=mk, color=col, ms=3.4,
                    mfc=col if ls == "-" else "white", mew=0.8, elinewidth=0.6, capsize=0)
    ax.set_xlabel("SNV switch error rate (%), 20×"); ax.set_ylabel("Block N50 (Mb), 20×")
    letter(ax, "d")
    h = [Line2D([], [], color=col, ls=ls, marker=mk, ms=2.6, label=name) for name, col, ls, mk, _ in F4]
    fig.legend(handles=h, loc="outside upper center", ncol=4, handlelength=2.4, columnspacing=1.2)
    save(fig, os.path.join(OUT, "fig4_cophasing.pdf"))


# ============================================================ Figure 5 =====
def fig5():
    """PacBio HiFi: LongPhase 2 vs WhatsHap, laid out like Fig. 2 (one replicate per coverage)."""
    tools = ["wh", "lp_gnn"]
    fig, axs = new_fig(56, 1, 5)
    specs = [("psnv_pct", "Phased SNVs (%)", (80, 90), 1),
             ("sw_pct", "Switch error rate (%)", (0, 0.15), 1),
             ("ham", "Hamming distance (%)", (0, 2), 1),
             ("n50", "Block N50 (kb)", (0, 600), 1e-3)]
    for ax, (key, lab, ylim, sc), L in zip(axs, specs, "abcd"):
        for t in tools:
            xs, m, s_ = snv_series(t, key, plat="HiFi", covs=HIFI_COVS)
            tline(ax, t, xs, m, s_, scale=sc, label=NAME[t])
        ax.set_ylim(*ylim); ax.set_ylabel(lab); cov_axis(ax, HIFI_COVS); letter(ax, L)
    ax = axs[4]
    xs, q, _ = snv_series("lp_gnn", "sw_pct", plat="HiFi", covs=HIFI_COVS)
    _, r, _ = snv_series("wh", "sw_pct", plat="HiFi", covs=HIFI_COVS)
    ax.plot(xs, [a / b for a, b in zip(r, q)], color=C["wh"], marker="D", ms=2.6)
    ax.set_ylim(0, 4); ax.set_ylabel("Switch-error-rate ratio\n(WhatsHap / LongPhase 2)")
    cov_axis(ax, HIFI_COVS); letter(ax, "e")
    h = [thandle(t) for t in ("lp_gnn", "wh")]
    fig.legend(handles=h, loc="outside upper center", ncol=2, handlelength=2.2)
    save(fig, os.path.join(OUT, "fig5_hifi.pdf"))


# ============================================================ Figure 6 =====
# Source: UnphasedComposition.jsx (JHL, 2026-09-26). SNV-only, seed 1; SNVs
# phased by LongPhase 2 and unphased after correction, classified against the
# v5.0q benchmark VCF (records outside the benchmark BED included).
COMPOSITION = {  # cov: (absent, hom-alt, het)
    10: (51760, 3364, 8673), 12: (53909, 3100, 7419), 14: (55121, 2782, 6084),
    16: (55776, 2486, 5176), 18: (55976, 2366, 4760), 20: (57256, 2382, 3937),
    30: (55055, 2148, 3239), 40: (55848, 1944, 2837), 50: (54762, 1988, 2695),
    60: (56069, 1787, 2411),
}
# Source: UnphaseVenn3.jsx (JHL, 2026-09-27). Heterozygous SNVs present in both
# output VCFs, replicate 1; LongPhase 2 = with correction.
VENN = {
    10: dict(phase=125981, gnn=22592, both=90210, wh=37676,
             cross=[(9.82, 2.33), (10.41, 2.33), (3.38, 1.73)]),
    30: dict(phase=111718, gnn=20720, both=96839, wh=52152,
             cross=[(13.44, 1.52), (6.41, 1.52), (3.97, 0.94)]),
    60: dict(phase=99813, gnn=22178, both=88692, wh=53621,
             cross=[(11.70, 1.12), (6.52, 1.12), (10.10, 1.06)]),
}


def t2t():
    txt = open(os.path.join(ROOT, "unphase_validation_results.txt")).read()
    cls = {k: int(v) for k, v in re.findall(r"^(variant|hom_wt|unassessed)\s+(\d+)", txt, re.M)}
    bg = re.search(r"background\s+(\d+) /\s+(\d+)", txt)
    rm = re.search(r"removed\s+(\d+) /\s+(\d+)", txt)
    chroms = []
    for m in re.finditer(r"^(chr\w+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)$", txt, re.M):
        chroms.append(dict(chrom=m.group(1), bg_out=int(m.group(2)), bg_n=int(m.group(3)),
                           bg_rate=float(m.group(4)), rm_out=int(m.group(5)), rm_n=int(m.group(6)),
                           rm_rate=float(m.group(7)), ratio=float(m.group(8))))
    bench = re.search(r"inside smvar.benchmark.bed: (\d+) sites\s+no variant (\d+).*?\n\s+variant\s+(\d+)", txt, re.S)
    return dict(cls=cls, bg_in=int(bg.group(1)), bg_n=int(bg.group(2)), rm_in=int(rm.group(1)),
                rm_n=int(rm.group(2)), chroms=chroms,
                bench=(int(bench.group(1)), int(bench.group(2)), int(bench.group(3))))


def venn_hist():
    src = open(os.path.join(ROOT, "UnphaseVenn3.jsx")).read()
    out = {}
    for cov in ("10x", "30x", "60x"):
        block = src.split(f'"{cov}": {{')[1].split("},\n  },")[0]
        h = {}
        for k in ("lp", "wh", "both"):
            arr = re.search(rf"\b{k}: \[([^\]]+)\]", block).group(1)
            h[k] = [float(x) for x in arr.replace("\n", "").split(",") if x.strip()]
        out[int(cov[:-1])] = h
    return out


def lp_only_enrichment(c):
    """Enrichment of all LongPhase 2-only sites (phase + GNN stage) in WhatsHap's intervals."""
    v = VENN[c]; (pp, bg), (pg, _), _ = v["cross"]
    return (v["phase"] * pp + v["gnn"] * pg) / (v["phase"] + v["gnn"]) / bg


def fig6():
    """SNVs left unphased by LongPhase 2 and by WhatsHap."""
    fig, axs = new_fig(58, 1, 3, width_ratios=[1.35, 0.8, 1])
    ax = axs[0]
    segs = [("lp", "LongPhase 2 only", C["lp_gnn"]), ("both", "both", "#969696"),
            ("wh", "WhatsHap only", C["wh"])]
    for y, c in enumerate([10, 30, 60]):
        left = 0
        vals = {"lp": VENN[c]["phase"] + VENN[c]["gnn"], "both": VENN[c]["both"], "wh": VENN[c]["wh"]}
        for k, lab, col in segs:
            v = vals[k] / 1000
            ax.barh(y, v, 0.62, left=left, color=col, label=lab if y == 0 else None, zorder=3)
            ax.text(left + v / 2, y, f"{v:.0f}", ha="center", va="center", fontsize=5.5, color="white")
            left += v
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels(["10×", "30×", "60×"]); ax.invert_yaxis()
    ax.set_xlabel("Heterozygous SNV calls left unphased (thousands)")
    fig.legend(handles=[Patch(color=col, label=lab) for _, lab, col in segs], loc="outside upper center", ncol=3)
    letter(ax, "a")
    ax = axs[1]
    w = 0.36
    for i, (lab, col, f) in enumerate([("LongPhase 2 only, in\nWhatsHap switch-error intervals", C["lp_gnn"], lp_only_enrichment),
                                       ("WhatsHap only, in\nLongPhase 2 switch-error intervals", C["wh"],
                                        lambda c: VENN[c]["cross"][2][0] / VENN[c]["cross"][2][1])]):
        ax.bar([j + (i - 0.5) * w for j in range(3)], [f(c) for c in (10, 30, 60)], w * 0.92,
               color=col, label=lab, zorder=3)
    ax.axhline(1, color="#999999", lw=0.5)
    ax.set_xticks(range(3)); ax.set_xticklabels(["10×", "30×", "60×"]); ax.set_ylim(0, 16)
    ax.set_ylabel("Enrichment (fold)")
    ax.legend(loc="upper left", fontsize=5, handlelength=1.2)
    letter(ax, "b")
    ax = axs[2]
    H = venn_hist()
    for k, col, lab in (("both", "#969696", "both"), ("wh", C["wh"], "WhatsHap only"),
                        ("lp", C["lp_gnn"], "LongPhase 2 only")):
        ax.plot([2 * i for i in range(len(H[60][k]))], H[60][k], color=col, lw=0.8, label=lab)
    ax.axvspan(123, 130, color="#EEEEEE", lw=0, zorder=0)
    ax.set_xlim(0, 130); ax.set_xlabel("Read depth at 60× (×); grey, ≥ depth cap"); ax.set_ylabel("Fraction of sites")
    letter(ax, "c")
    save(fig, os.path.join(OUT, "fig6_unphased_analysis.pdf"))


# ============================================== Supplementary Fig. 10 =====
def sfig10():
    """Margin, Ralphi and GCphase at 10-20x."""
    tools = ["hc", "wh", "ralphi", "gc", "margin", "lp_gnn"]
    covs = [10, 12, 14, 16, 18, 20]
    fig, axs = new_fig(52, 1, 4)
    specs = [("sw_pct", "Switch error rate (%)", "log", 1), ("ham", "Hamming distance (%)", "log", 1),
             ("n50", "Block N50 (Mb)", None, 1e-6), ("nblock", "Phase blocks (thousands)", None, 1e-3)]
    for ax, (key, lab, ysc, sc), L in zip(axs, specs, "abcd"):
        for t in tools:
            if key == "n50" and t == "ralphi":
                continue
            xs, m, s_ = snv_series(t, key, covs=covs)
            tline(ax, t, xs, m, s_, scale=sc, label=NAME[t])
        if ysc:
            ax.set_yscale(ysc)
        ax.set_ylabel(lab); cov_axis(ax, covs); letter(ax, L)
    h = [thandle(t) for t in tools]
    fig.legend(handles=h, loc="outside upper center", ncol=6, handlelength=2.6)
    save(fig, os.path.join(SUPP, "suppfig10_more_tools.pdf"))


# ============================================== Supplementary Fig. 11 =====
def sfig11():
    """Effect of GNN correction on SNV-only phasing (nanopore and HiFi)."""
    fig, axs = new_fig(100, 2, 3)
    specs = [("psnv_pct", "Phased SNVs (%)", None, 1), ("sw_pct", "Switch error rate (%)", "log", 1),
             ("ham", "Hamming distance (%)", None, 1), ("n50", "Block N50 (Mb)", None, 1e-6)]
    for ax, (key, lab, ysc, sc), L in zip(axs.flat, specs, "abcd"):
        single_band(ax)
        for t, ls, mfc in (("lp", "--", "white"), ("lp_gnn", "-", None)):
            xs, m, s_ = snv_series(t, key)
            line(ax, xs, m, s_, C["lp_gnn"], ls=ls, mfc=mfc, scale=sc)
        if ysc:
            ax.set_yscale(ysc); ax.minorticks_off()
            ax.set_yticks([0.02, 0.05, 0.1]); ax.set_yticklabels(["0.02", "0.05", "0.1"])
        ax.set_ylabel(lab); cov_axis(ax); letter(ax, L)
    ax = axs.flat[4]
    for plat, covs, ls, mfc in (("ONT", PLOT_COVS, "-", "black"), ("HiFi", HIFI_COVS, "--", "white")):
        xs, a, _ = snv_series("lp", "sw", plat=plat, covs=covs)
        _, b, _ = snv_series("lp_gnn", "sw", plat=plat, covs=covs)
        ax.plot(xs, [100 * (1 - y / x) for x, y in zip(a, b)], color="black", ls=ls, marker="o",
                ms=2.6, mfc=mfc, label="nanopore" if plat == "ONT" else "PacBio HiFi")
    ax.set_ylim(0, 40); ax.set_ylabel("Switch errors removed\nby GNN correction (%)")
    cov_axis(ax); letter(ax, "e"); ax.legend(loc="lower right", fontsize=5.5)
    ax = axs.flat[5]
    for t, ls, mfc in (("lp", "--", "white"), ("lp_gnn", "-", None)):
        xs, m, s_ = snv_series(t, "sw", plat="HiFi", covs=HIFI_COVS)
        line(ax, xs, m, s_, C["lp_gnn"], ls=ls, mfc=mfc)
    ax.set_ylim(0, 1500); ax.set_ylabel("Switch errors, PacBio HiFi"); cov_axis(ax, HIFI_COVS)
    letter(ax, "f")
    h = [Line2D([], [], color=C["lp_gnn"], ls="--", marker="o", mfc="white", ms=2.6, label="without GNN correction"),
         Line2D([], [], color=C["lp_gnn"], marker="o", ms=2.6, label="with GNN correction")]
    fig.legend(handles=h, loc="outside upper center", ncol=3)
    save(fig, os.path.join(SUPP, "suppfig13_gnn_effect.pdf"))


# ============================================== Supplementary Fig. 12 =====
def sfig12():
    """Co-phasing configurations with and without GNN correction (former main Fig. 4)."""
    fig, axs = new_fig(118, 2, 2)
    for ax, cov, L in ((axs[0, 0], 10, "a"), (axs[0, 1], 60, "b")):
        for cfg, name, col in CFG:
            pts = []
            for tool in ("longphase_v2.0.1", "longphase_v2.1"):
                xs, sw, ssw = coph_series(cfg, tool, "sw_pct", covs=[cov])
                _, n50, sn50 = coph_series(cfg, tool, "n50", covs=[cov])
                pts.append((sw[0], n50[0] / 1e6, ssw[0], sn50[0] / 1e6))
            (x0, y0, ex0, ey0), (x1, y1, ex, ey) = pts
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=0.7, mutation_scale=6,
                                        shrinkA=2.5, shrinkB=2.5))
            ax.errorbar([x0], [y0], xerr=[ex0], yerr=[ey0], fmt="o", mfc="white", mec=col, mew=0.8,
                        ecolor=col, ms=3.6, elinewidth=0.5, capsize=0, zorder=4)
            ax.errorbar([x1], [y1], xerr=[ex], yerr=[ey], fmt="o", color=col, ms=3.6,
                        elinewidth=0.5, capsize=0, zorder=5)
        ax.set_xlabel("SNV switch error rate (%)"); ax.set_ylabel("Block N50 (Mb)")
        ax.set_title(f"{cov}×", loc="center", fontsize=6.5)
        letter(ax, L)
    for ax, key, lab, L in ((axs[1, 0], "sw_pct", "SNV switch error rate (%)", "c"),
                            (axs[1, 1], "ham", "Hamming distance (%)", "d")):
        single_band(ax)
        for cfg, col in (("SNV", "#4D4D4D"), ("Indel+Mod+SV", "#542788")):
            for tool, ls, mfc in (("longphase_v2.0.1", "--", "white"), ("longphase_v2.1", "-", None)):
                xs, m, s_ = coph_series(cfg, tool, key)
                line(ax, xs, m, s_, col, ls=ls, mfc=mfc)
        if key == "sw_pct":
            ax.set_yscale("log")
            ax.set_yticks([0.02, 0.05, 0.1, 0.15]); ax.set_yticklabels(["0.02", "0.05", "0.1", "0.15"])
            ax.minorticks_off()
        ax.set_ylabel(lab); cov_axis(ax); letter(ax, L)
    h = [Line2D([], [], color=col, marker="o", ls="", ms=3.6, label=name) for _, name, col in CFG]
    h += [Line2D([], [], color="k", marker="o", mfc="white", ls="", ms=3.6, label="without GNN"),
          Line2D([], [], color="k", marker="o", ls="", ms=3.6, label="with GNN")]
    axs[0, 1].legend(handles=h, loc="upper left", bbox_to_anchor=(1.03, 1.0))
    h2 = [Line2D([], [], color="#4D4D4D", label="SNV only"),
          Line2D([], [], color="#542788", label="all four classes"),
          Line2D([], [], color="k", ls="--", marker="o", mfc="white", ms=2.6, label="without GNN"),
          Line2D([], [], color="k", marker="o", ms=2.6, label="with GNN")]
    axs[1, 1].legend(handles=h2, loc="upper left", bbox_to_anchor=(1.03, 1.0))
    save(fig, os.path.join(SUPP, "suppfig14_cophase_gnn.pdf"))


# ============================================== Supplementary Fig. 13 =====
def sfig13():
    """All co-phasing configurations across coverage, without and with GNN correction."""
    fig, axs = new_fig(96, 2, 4)
    specs = [("sw_pct", "SNV switch error rate (%)", 1), ("ham", "Hamming distance (%)", 1),
             ("n50", "Block N50 (Mb)", 1e-6), ("psnv_pct", "Phased SNVs (%)", 1)]
    for row, tool, tag in ((0, "longphase_v2.0.1", "without GNN correction"), (1, "longphase_v2.1", "with GNN correction")):
        for col, (key, lab, sc) in enumerate(specs):
            ax = axs[row, col]; single_band(ax)
            for cfg, name, c in CFG:
                xs, m, s_ = coph_series(cfg, tool, key)
                line(ax, xs, m, s_, c, scale=sc, label=name)
            ax.set_ylabel(f"{tag.capitalize()}\n{lab}" if col == 0 else lab); cov_axis(ax)
            letter(ax, "abcdefgh"[row * 4 + col])
    for col in range(4):
        lo = min(axs[0, col].get_ylim()[0], axs[1, col].get_ylim()[0])
        hi = max(axs[0, col].get_ylim()[1], axs[1, col].get_ylim()[1])
        axs[0, col].set_ylim(lo, hi); axs[1, col].set_ylim(lo, hi)
    h = [Line2D([], [], color=c, marker="o", ms=2.6, label=name) for _, name, c in CFG]
    fig.legend(handles=h, loc="outside upper center", ncol=7)
    save(fig, os.path.join(SUPP, "suppfig15_cophasing_all.pdf"))


# ============================================== Supplementary Fig. 14 =====
# MethPhaser values: MethPhaserCompare.jsx (JHL, 2026-10-03). They are identical,
# to every printed digit, to the uncorrected SNV-only LongPhase 2 run that was
# MethPhaser's input (xlsx SNV_Detail, longphase_v2.0.1, replicate 1).
METH = {10: (2277, 78.11491, 6.92789, 0.9395), 20: (1311, 91.08722, 3.98836, 1.6993),
        30: (1004, 91.60825, 2.40328, 1.9689), 40: (878, 91.63726, 2.37294, 2.2887),
        50: (883, 91.5461, 1.8627, 2.5705), 60: (743, 91.43292, 1.75198, 2.9108)}


def rep1(cfg, tool, cov, key):
    runs = D["coph"][cfg][tool][cov]
    return [r for r in runs if r["rep"] == 1][0][key]


def sfig14():
    """MethPhaser vs joint SNV+5mC co-phasing (replicate 1)."""
    fig, axs = new_fig(56, 1, 4)
    specs = [("sw", 0, "Switch errors", 1), ("psnv_pct", 1, "Phased SNVs (%)", 1),
             ("ham", 2, "Hamming distance (%)", 1), ("n50", 3, "Block N50 (Mb)", 1e-6)]
    covs = BAR_COVS
    for ax, (key, j, lab, sc), L in zip(axs, specs, "abcd"):
        ax.plot(covs, [METH[c][j] for c in covs], color=C["meth"], marker="o", ms=2.6,
                label="MethPhaser on LongPhase 2 SNV phasing without GNN")
        ax.plot(covs, [rep1("Mod", "longphase_v2.0.1", c, key) * sc for c in covs], color=C["lp_gnn"],
                ls="--", marker="o", mfc="white", ms=2.6, label="LongPhase 2, SNV+5mC, without GNN")
        ax.plot(covs, [rep1("Mod", "longphase_v2.1", c, key) * sc for c in covs], color=C["lp_gnn"],
                marker="o", ms=2.6, label="LongPhase 2, SNV+5mC")
        ax.set_ylabel(lab); cov_axis(ax); letter(ax, L)
    axs[1].set_ylim(75, 95)
    fig.legend(*axs[0].get_legend_handles_labels(), loc="outside upper center", ncol=3)
    save(fig, os.path.join(SUPP, "suppfig11_methphaser.pdf"))


# ============================================== Supplementary Fig. 15 =====
def sfig15():
    """SNVs unphased by GNN correction: benchmark composition and T2T assembly status."""
    T = t2t()
    fig, axs = new_fig(66, 1, 3, width_ratios=[1.15, 1, 1.05])
    ax = axs[0]
    cols = ["#D9D9D9", "#969696", "#B2182B"]
    labs = ["absent from benchmark", "homozygous in benchmark", "heterozygous in benchmark"]
    xs = range(len(COVS)); bottom = [0] * len(COVS)
    for i in range(3):
        v = [100 * COMPOSITION[c][i] / sum(COMPOSITION[c]) for c in COVS]
        ax.bar(xs, v, 0.75, bottom=bottom, color=cols[i], label=labs[i], zorder=3)
        bottom = [a + b for a, b in zip(bottom, v)]
    for x, c in zip(xs, COVS):
        ax.text(x, 101, f"{sum(COMPOSITION[c]) / 1000:.0f}k", ha="center", va="bottom", fontsize=5)
    ax.set_xticks(list(xs)); ax.set_xticklabels([str(c) for c in COVS])
    ax.set_xlabel("Coverage (×)"); ax.set_ylabel("SNVs unphased by GNN (%)")
    ax.set_ylim(0, 108); letter(ax, "a")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), fontsize=5.5)
    ax = axs[1]
    cls = T["cls"]; n = T["rm_n"]
    rm = [100 * cls["variant"] / n, 100 * cls["hom_wt"] / n, 100 * cls["unassessed"] / n]
    bgv = [100 * T["bg_in"] / T["bg_n"], 0, 100 * (1 - T["bg_in"] / T["bg_n"])]
    colsb = ["#B2182B", "#FDDBC7", "#BDBDBD"]
    labb = ["aligned, assembly record", "aligned, no record", "not aligned 1:1"]
    for j, (vals, y) in enumerate(((bgv, 1), (rm, 0))):
        left = 0
        for i, v in enumerate(vals):
            ax.barh(y, v, 0.6, left=left, color=colsb[i] if not (j == 0 and i == 0) else "#4D4D4D", zorder=3)
            left += v
    ax.set_yticks([0, 1]); ax.set_yticklabels([f"unphased by\nGNN\n(n = {n:,})",
                                               f"phased before\nGNN (sample,\nn = {T['bg_n']:,})"])
    ax.set_xlim(0, 100); ax.set_xlabel("SNVs at 60× (%)")
    ax.text(T["bg_in"] / T["bg_n"] * 50, 1, f"aligned\n{100 * T['bg_in'] / T['bg_n']:.1f}%",
            color="white", ha="center", va="center", fontsize=5.5)
    ax.text(100 - 100 * cls["unassessed"] / n / 2, 0, f"{100 * cls['unassessed'] / n:.1f}%",
            ha="center", va="center", fontsize=5.5)
    ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(colsb, labb)], loc="upper center",
              bbox_to_anchor=(0.4, -0.28), fontsize=5.5)
    letter(ax, "b")
    ax = axs[2]
    order = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
    ch = sorted(T["chroms"], key=lambda d: order.index(d["chrom"]))
    ys = range(len(ch))
    for y, d in zip(ys, ch):
        ax.plot([100 * d["bg_rate"], 100 * d["rm_rate"]], [y, y], color="#BDBDBD", lw=0.6, zorder=2)
    ax.plot([100 * d["bg_rate"] for d in ch], ys, "o", color="#4D4D4D", ms=2.2, label="phased before GNN", zorder=3)
    ax.plot([100 * d["rm_rate"] for d in ch], ys, "o", color="#B2182B", ms=2.2, label="unphased by GNN", zorder=3)
    ax.set_yticks(list(ys)); ax.set_yticklabels([d["chrom"].replace("chr", "") for d in ch], fontsize=5)
    ax.tick_params(axis="y", length=1.5, pad=1)
    ax.invert_yaxis(); ax.set_xlim(0, 100)
    ax.set_xlabel("Not aligned 1:1 (%)"); ax.set_ylabel("Chromosome")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), fontsize=5.5)
    letter(ax, "c")
    save(fig, os.path.join(SUPP, "suppfig16_gnn_removed.pdf"))


# ============================================== Supplementary Fig. 17 =====
def sfig17():
    """Read depth of the sets each tool leaves unphased, 10/30/60x, LongPhase 2-only split by stage."""
    H = venn_hist()
    fig, axs = new_fig(50, 1, 3)
    for ax, cov, L in zip(axs, (10, 30, 60), "abc"):
        for k, col, lab in (("both", "#969696", "both"), ("wh", C["wh"], "WhatsHap only"),
                            ("lp", C["lp_gnn"], "LongPhase 2 only")):
            ax.plot([2 * i for i in range(len(H[cov][k]))], H[cov][k], color=col, lw=0.8, label=lab)
        ax.set_title(f"{cov}×", fontsize=6.5); ax.set_xlabel("Read depth (×)")
        ax.set_ylabel("Fraction of sites"); ax.set_xlim(0, 130)
        ax.axvspan(123, 130, color="#EEEEEE", lw=0, zorder=0)
        ax.text(126.5, ax.get_ylim()[1] * 0.97, "≥ cap\n(censored)", ha="center", va="top", fontsize=5)
        letter(ax, L)
    h = [Line2D([], [], color=c, label=l) for c, l in ((C["lp_gnn"], "LongPhase 2 only"),
                                                     ("#969696", "both"), (C["wh"], "WhatsHap only"))]
    fig.legend(handles=h, loc="outside upper center", ncol=3)
    save(fig, os.path.join(SUPP, "suppfig12_giveup_depth.pdf"))


# ================================================== Supplementary tables ===
def f(x, d=2):
    return f"{x:,.{d}f}"


def cell(runs, key, d, sc=1.0):
    a, b = ms(runs, key)
    if a is None:
        return "--"
    a *= sc; b *= sc
    if len(runs) > 1:
        return f"{a:,.{d}f} ({b:,.{d}f})"
    return f"{a:,.{d}f}"


def tables():
    L = []
    w = L.append
    w("% Generated by figures-source/make_results_figs.py -- do not edit by hand.\n")
    # ---- Table 7: input call sets
    w(r"\begin{table}[h]")
    w(r"\caption{\textbf{Input call sets per coverage.} Heterozygous (het.) and homozygous (hom.) calls entering the phasing runs; nanopore values at 10--20$\times$ are means (s.d.) over ten down-sampling replicates. Small variants from PEPPER-Margin-DeepVariant, SVs from Sniffles2 2.8.0, allele-specific 5mC sites from \code{longphase modcall}. SVs and 5mC were not called on the HiFi data.\todo{The HiFi call sets are almost identical at every coverage (2,367,609--2,367,619 heterozygous SNVs from 10 to 50$\times$), which suggests that one call set was used for all down-sampled HiFi runs; confirm and state it in Methods.}}")
    w(r"\label{tab:calls}\scriptsize\setlength{\tabcolsep}{4pt}")
    w(r"\begin{tabular}{@{}llrrrrrr@{}}\toprule")
    w(r"Platform & Cov. & Het. SNV & Hom. SNV & Het. indel & Het. SV & Hom. SV & Het. 5mC \\ \midrule")
    keys = ["het_snv", "hom_snv", "het_indel", "het_sv", "hom_sv", "het_5mc"]
    for plat, covs in (("Nanopore", COVS), ("HiFi", HIFI_COVS)):
        for c in covs:
            runs = D["calls"]["ONT" if plat == "Nanopore" else "HiFi"][c]
            cells = []
            for k in keys:
                a, b = ms(runs, k)
                cells.append("--" if a is None else (f"{a:,.0f} ({b:,.0f})" if len(runs) > 1 else f"{a:,.0f}"))
            w(f"{plat} & {c}$\\times$ & " + " & ".join(cells) + r" \\")
        if plat == "Nanopore":
            w(r"\midrule")
    w(r"\bottomrule\end{tabular}\end{table}" + "\n")
    # ---- Table 8: SNV-only, all tools, nanopore
    w(r"{\scriptsize\setlength{\tabcolsep}{3.5pt}")
    w(r"\begin{longtable}{@{}llrrrrrr@{}}")
    w(r"\caption{\textbf{SNV-only phasing of HG002 nanopore R10.4.1 data by seven configurations.} Scored against v5.0q (chr1--22, benchmark BED). Values at 10--20$\times$ are means (s.d.) over ten down-sampling replicates; 30--60$\times$, one replicate. Phased SNVs are given as a percentage of the 2,398,880 heterozygous SNVs of the benchmark. Margin, Ralphi and GCphase were run at 10--20$\times$ only. Ralphi's phase blocks sum to 4.3--5.8~Gb, more than the length of the autosomes, so its block N50 is not comparable with that of the other tools.}\label{tab:snvall}\\")
    w(r"\toprule Tool & Cov. & \shortstack[r]{Phased\\SNV (\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & Blocks & \shortstack[r]{N50\\(Mb)} \\ \midrule\endfirsthead")
    w(r"\toprule Tool & Cov. & \shortstack[r]{Phased\\SNV (\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & Blocks & \shortstack[r]{N50\\(Mb)} \\ \midrule\endhead")
    for t in ["lp_gnn", "lp", "wh", "hc", "margin", "ralphi", "gc"]:
        for c in COVS:
            runs = D["snv"]["ONT"][XLSX_TOOL[t]].get(c)
            if not runs:
                continue
            w(f"{NAME[t] if c == COVS[0] else ''} & {c}$\\times$ & {cell(runs, 'psnv_pct', 2)} & {cell(runs, 'sw', 0)} & "
              f"{cell(runs, 'sw_pct', 3)} & {cell(runs, 'ham', 2)} & {cell(runs, 'nblock', 0)} & {cell(runs, 'n50', 2, 1e-6)} \\\\")
        w(r"\midrule")
    L[-1] = r"\bottomrule"
    w(r"\end{longtable}}" + "\n")
    # ---- Table 9: two benchmarks
    w(r"{\scriptsize\setlength{\tabcolsep}{3.5pt}")
    w(r"\begin{longtable}{@{}llrrrrr@{}}")
    w(r"\caption{\textbf{The same phased VCFs scored against GIAB v4.2.1 and the T2T-HG002-derived v5.0q benchmark.} Switch errors and Hamming distance on SNVs; all \toolname runs with GNN correction, phasing SNVs alone or with indels (+indel) or indels and SVs (+indel+SV). Values at 10--20$\times$ are means (s.d.) over ten replicates. Phased indels as a percentage of benchmark heterozygous indels (v5.0q).}\label{tab:twobench}\\")
    w(r"\toprule Configuration & Cov. & \shortstack[r]{Switch errors\\v4.2.1} & \shortstack[r]{Switch errors\\v5.0q} & \shortstack[r]{Hamming\\v4.2.1 (\%)} & \shortstack[r]{Hamming\\v5.0q (\%)} & \shortstack[r]{Phased\\indels (\%)} \\ \midrule\endfirsthead")
    w(r"\toprule Configuration & Cov. & \shortstack[r]{Switch errors\\v4.2.1} & \shortstack[r]{Switch errors\\v5.0q} & \shortstack[r]{Hamming\\v4.2.1 (\%)} & \shortstack[r]{Hamming\\v5.0q (\%)} & \shortstack[r]{Phased\\indels (\%)} \\ \midrule\endhead")
    for k, name, col, _ls, _mk, src, v421 in F3:
        for c in BAR_COVS:
            r4 = D["v421"][v421][c]; r5 = f3_runs(src, c)
            pind = cell(r5, "pindel_pct", 2) if src[0] == "coph" else "--"
            w(f"{name.replace('LongPhase 2 + correction, ', 'LongPhase 2, ') if c == 10 else ''} & {c}$\\times$ & {cell(r4, 'sw', 0)} & {cell(r5, 'sw', 0)} & "
              f"{cell(r4, 'ham', 2)} & {cell(r5, 'ham', 2)} & {pind} \\\\")
        w(r"\midrule")
    L[-1] = r"\bottomrule"
    w(r"\end{longtable}}" + "\n")
    # ---- Table 10: co-phasing configurations
    w(r"{\scriptsize\setlength{\tabcolsep}{3.5pt}")
    w(r"\begin{longtable}{@{}lllrrrrr@{}}")
    w(r"\caption{\textbf{Co-phasing configurations of \toolname, without and with GNN correction.} SNV metrics against v5.0q; phased indels as a percentage of benchmark heterozygous indels. Means (s.d.) over ten replicates at 10 and 20$\times$; one replicate at 30 and 60$\times$. Every coverage is in Supplementary Data~1.}\label{tab:cophase}\\")
    w(r"\toprule Classes & GNN & Cov. & \shortstack[r]{Phased\\indel (\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & \shortstack[r]{N50\\(Mb)} \\ \midrule\endfirsthead")
    w(r"\toprule Classes & GNN & Cov. & \shortstack[r]{Phased\\indel (\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & \shortstack[r]{N50\\(Mb)} \\ \midrule\endhead")
    for cfg, name, _ in CFG:
        for tool, tag in (("longphase_v2.0.1", "no"), ("longphase_v2.1", "yes")):
            for c in (10, 20, 30, 60):
                if cfg == "SNV":
                    runs = D["snv"]["ONT"][tool][c]
                    pind = "--"
                else:
                    runs = D["coph"][cfg][tool][c]
                    pind = cell(runs, "pindel_pct", 2) if "Indel" in cfg else "--"
                first = c == 10
                w(f"{name if (first and tag == 'no') else ''} & {tag if first else ''} & {c}$\\times$ & {pind} & {cell(runs, 'sw', 0)} & "
                  f"{cell(runs, 'sw_pct', 3)} & {cell(runs, 'ham', 2)} & {cell(runs, 'n50', 2, 1e-6)} \\\\")
        w(r"\midrule")
    L[-1] = r"\bottomrule"
    w(r"\end{longtable}}" + "\n")
    # ---- Table 11: HiFi
    w(r"\begin{table}[h]")
    w(r"\caption{\textbf{SNV-only phasing of HG002 PacBio HiFi (Revio) data.} One replicate per coverage, scored against v5.0q. The network was trained on nanopore data only and applied without retraining.\todo{HiFi read source, aligner settings, variant caller and \toolname/\whatshap options are not yet in Methods or Supplementary Table~5.}}")
    w(r"\label{tab:hifi}\scriptsize")
    w(r"\begin{tabular}{@{}llrrrrrr@{}}\toprule")
    w(r"Tool & Cov. & \shortstack[r]{Phased\\SNV (\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & Blocks & \shortstack[r]{N50\\(kb)} \\ \midrule")
    for t in ["lp_gnn", "lp", "wh"]:
        for c in HIFI_COVS:
            r = D["snv"]["HiFi"][XLSX_TOOL[t]][c]
            w(f"{NAME[t] if c == 10 else ''} & {c}$\\times$ & {cell(r, 'psnv_pct', 2)} & {cell(r, 'sw', 0)} & {cell(r, 'sw_pct', 3)} & "
              f"{cell(r, 'ham', 2)} & {cell(r, 'nblock', 0)} & {cell(r, 'n50', 0, 1e-3)} \\\\")
        w(r"\midrule")
    L[-1] = r"\bottomrule\end{tabular}\end{table}" + "\n"
    # ---- Table 12: T2T assembly validation
    T = t2t()
    cls = T["cls"]; n = T["rm_n"]
    w(r"\begin{table}[h]")
    w(r"\caption{\textbf{SNVs unphased by GNN correction, classified by the T2T-HG002 v1.1 assembly.} Nanopore 60$\times$, replicate~1, SNV-only phasing. ``Aligned'' means inside the dipcall BED in which both assembled haplotypes align 1:1 to GRCh38 (\code{GRCh38\_HG2-T2TQ100-V1.1\_dipcall-z2k.dip.bed}); variant status from the matching dipcall VCF. The background is a random sample of 50,000 SNVs that stayed phased. Top, overall classes; bottom, share outside the 1:1 alignment per chromosome. v5.0q is derived from the same assembly, so this analysis extends coverage rather than providing an independent truth set.}")
    w(r"\label{tab:t2t}\small")
    w(r"\begin{tabular}{@{}lrr@{}}\toprule Class & SNVs & Share (\%) \\ \midrule")
    for k, lab in (("unassessed", "not aligned 1:1 (unassessed)"), ("hom_wt", "aligned, assembly carries no variant"),
                   ("variant", "aligned, assembly confirms a variant")):
        w(f"{lab} & {cls[k]:,} & {100 * cls[k] / n:.2f} \\\\")
    w(f"total & {n:,} & 100.00 \\\\ \\midrule")
    w(f"aligned 1:1, unphased by GNN correction & {T['rm_in']:,} / {n:,} & {100 * T['rm_in'] / n:.2f} \\\\")
    w(f"aligned 1:1, phased before GNN correction (sample) & {T['bg_in']:,} / {T['bg_n']:,} & {100 * T['bg_in'] / T['bg_n']:.2f} \\\\")
    b = T["bench"]
    w(f"inside the v5.0q benchmark BED & {b[0]:,} & -- \\\\")
    w(f"\\quad of which benchmark variant & {b[2]:,} & {100 * b[2] / b[0]:.2f} \\\\")
    w(r"\bottomrule\end{tabular}\par\medskip")
    w(r"\begin{tabular}{@{}lrrrrr@{}}\toprule Chromosome & \multicolumn{2}{c}{Phased before GNN correction} & \multicolumn{2}{c}{Unphased by GNN correction} & Ratio \\")
    w(r" & $n$ & not aligned (\%) & $n$ & not aligned (\%) & \\ \midrule")
    order = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
    for d in sorted(T["chroms"], key=lambda d: order.index(d["chrom"])):
        w(f"{d['chrom']} & {d['bg_n']:,} & {100 * d['bg_rate']:.2f} & {d['rm_n']:,} & {100 * d['rm_rate']:.2f} & {d['ratio']:.1f} \\\\")
    w(r"\bottomrule\end{tabular}\end{table}" + "\n")
    path = os.path.join(ROOT, "figures-source", "supp_tables.tex")
    open(path, "w").write("\n".join(L) + "\n")
    print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    fig2(); fig3(); fig4(); fig5(); fig6()
    sfig10(); sfig11(); sfig12(); sfig13(); sfig14(); sfig15(); sfig17()
    tables()
