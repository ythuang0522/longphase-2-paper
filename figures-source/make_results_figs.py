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
    "meth":   "#6A3D9A",
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
# SNV, +5mC, +indel and all four share their colours with main Fig. 3 (STRAT).
CFG = [
    ("SNV", "SNV", "#B2182B"),
    ("SV", "+SV", "#80CDC1"),
    ("Mod", "+5mC", "#1B9E77"),
    ("Indel", "+indel", "#C66A00"),
    ("Indel+SV", "+indel+SV", "#FDB863"),
    ("Mod+Indel", "+indel+5mC", "#8C510A"),
    ("Indel+Mod+SV", "all four", "#1A1A1A"),
]
CFGC = {k: c for k, _, c in CFG}


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


PLOT_COVS = COVS   # every coverage, 10-20x in steps of 2 to show low-coverage differences


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
    # hollow markers of different shape and size nest inside each other where tools coincide
    "lp_gnn": dict(marker="o", ls="-", mfc="none", dx=0.0, ms=3.0),
    "lp":     dict(marker="o", ls="--", mfc="none", dx=0.0, ms=3.0),
    "wh":     dict(marker="D", ls="-", mfc="none", dx=0.0, ms=2.8),
    "hc":     dict(marker="s", ls="--", mfc="none", dx=0.0, ms=4.0),
    "margin": dict(marker="^", ls="-", mfc="none", dx=0.0, ms=3.4),
    "ralphi": dict(marker="v", ls="-", mfc="none", dx=0.0, ms=3.4),
    "gc":     dict(marker="P", ls="-", mfc="none", dx=0.0, ms=3.4),
    "meth":   dict(marker="^", ls="-", mfc="none", dx=0.0, ms=3.4),
}


def tline(ax, t, xs, m, s, scale=1.0, label=None):
    st = STY[t]
    line(ax, [x + st["dx"] for x in xs], m, s, C[t], ls=st["ls"], marker=st["marker"],
         scale=scale, label=label, mfc=st["mfc"], ms=st["ms"])


def thandle(t, label=None):
    st = STY[t]
    return Line2D([], [], color=C[t], ls=st["ls"], marker=st["marker"], ms=st["ms"] + 0.4,
                  mfc=st["mfc"], mew=0.8, label=label or NAME[t])


def line(ax, xs, m, s, color, ls="-", marker="o", label=None, scale=1.0, mfc=None, z=3, ms=2.6):
    """Mean line with markers; replicate s.d. as a light band (zero width for single runs)."""
    m = [v * scale for v in m]; s = [v * scale for v in s]
    if any(s):
        ax.fill_between(xs, [a - b for a, b in zip(m, s)], [a + b for a, b in zip(m, s)],
                        color=color, alpha=0.18, lw=0, zorder=z - 1)
    ax.plot(xs, m, color=color, ls=ls, marker=marker, ms=ms, mfc=mfc or color,
            mew=0.8 if mfc == "none" else 0.6, label=label, zorder=z)


def cov_axis(ax, covs=(10, 20, 30, 40, 50, 60)):
    ax.set_xticks(list(covs))
    ax.set_xticklabels([f"{c}" for c in covs])
    ax.set_xlabel("Coverage (×)")


def save(fig, path):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    fig.set_layout_engine("none")
    W, H = fig.get_size_inches() * fig.dpi
    for ax, s_ in [(a, l) for a, l in _LETTERS if a.get_figure(root=True) is fig]:
        tb = ax.get_tightbbox(r)
        fig.text(max(tb.x0, 0) / W, min(tb.y1, H) / H, s_, fontsize=8, fontweight="bold",
                 va="top", ha="left")
    fig.savefig(path)
    w_mm = fig.get_size_inches()[0] * 25.4
    plt.close(fig)
    print(f"wrote {os.path.relpath(path, ROOT)} ({w_mm:.0f} mm wide)")


# ============================================================ Figure 2 =====
# MethPhaser values: MethPhaserCompare.jsx (JHL, 2026-10-03). They are identical,
# to every printed digit, to the uncorrected SNV-only LongPhase 2 run that was
# MethPhaser's input (xlsx SNV_Detail, longphase_v2.0.1, replicate 1).
METH = {10: (2277, 78.11491, 6.92789, 0.9395), 20: (1311, 91.08722, 3.98836, 1.6993),
        30: (1004, 91.60825, 2.40328, 1.9689), 40: (878, 91.63726, 2.37294, 2.2887),
        50: (883, 91.5461, 1.8627, 2.5705), 60: (743, 91.43292, 1.75198, 2.9108)}


def rep1(cfg, tool, cov, key):
    runs = D["coph"][cfg][tool][cov]
    return [r for r in runs if r["rep"] == 1][0][key]


def meth_value(cov, key):
    """MethPhaser metric at one coverage. The draft gives counts, phased fraction, Hamming
    distance and N50 but not the switch error rate; because the output equals its input
    (checked here), the rate is taken from that input run."""
    run = [r for r in D["snv"]["ONT"]["longphase_v2.0.1"][cov] if r["rep"] == 1][0]
    sw, psnv, ham, n50 = METH[cov]
    assert run["sw"] == sw and abs(run["ham"] - ham) < 1e-3 and abs(run["n50"] / 1e6 - n50) < 1e-3
    return run[key]


def _series(get, covs):
    """(xs, means, s.d.) of a getter cov -> list of replicate dicts, for one metric key."""
    def f(key):
        xs, m, s = [], [], []
        for c in covs:
            runs = get(c)
            if not runs:
                continue
            a, b = ms(runs, key)
            xs.append(c); m.append(a); s.append(b)
        return xs, m, s
    return f


def _row_header(sf, title):
    """Bold row title, left-aligned; space for it is reserved by constrained layout."""
    sf.suptitle(title, x=0.0, ha="left", fontsize=7, fontweight="bold")


def _row_keys(fig, sfs, keys):
    """Each row's key on the line of its title, right-aligned. Placed after a first draw,
    outside constrained layout, so that it shares the line instead of adding one."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    H = fig.get_size_inches()[1] * fig.dpi
    for sf, handles in zip(sfs, keys):
        bb = sf._suptitle.get_window_extent(r)
        sf.legend(handles=handles, loc="center right", bbox_to_anchor=(1.0, (bb.y0 + bb.y1) / 2 / H),
                  bbox_transform=fig.transFigure, ncol=len(handles), handlelength=2.6,
                  columnspacing=1.6, borderaxespad=0.0, borderpad=0.0)


def _log_rate_axis(ax, ticks=(0.02, 0.05, 0.1, 0.2), lim=(0.018, 0.32)):
    ax.set_yscale("log"); ax.minorticks_off()
    ax.set_yticks(list(ticks)); ax.set_yticklabels([f"{t:g}" for t in ticks])
    ax.set_ylim(*lim)


def _indel_runs(config):
    """Per-replicate indel accuracy of one co-phasing run type (issue #1 item 3, whole genome)."""
    g = {}
    for r in _tsv("item3_indel.tsv"):
        if r["config"] == config and r["region"] == "all":
            g.setdefault(int(r["coverage"]), []).append(
                {"indel_sw_pct": float(r["indel_sw_rate%"]), "indel_ham": float(r["indel_hamming%"])})
    return lambda c: g.get(c)


def fig2():
    """LongPhase 2 against other phasers for each evidence type (nanopore, v5.0q).
    Rows: SNV phasing (WhatsHap, HapCUT2), SNV and indel co-phasing (WhatsHap), SNV and
    5mC co-phasing (MethPhaser). Columns: switch error rate, Hamming distance, block N50,
    phased fraction; in the indel row the accuracy panels also score the indels themselves
    (Supplementary Table 14)."""
    fig = plt.figure(figsize=(FIGW, 150 * MM), layout="constrained")
    fig.get_layout_engine().set(w_pad=2 * MM, h_pad=1.2 * MM, wspace=0.05, hspace=0.0)
    sfs = fig.subfigures(3, 1, hspace=0.035)
    snv = lambda tool: (lambda c: D["snv"]["ONT"][XLSX_TOOL[tool]].get(c))
    ind = lambda tool: (lambda c: D["coph"]["Indel"][tool].get(c))
    mod1 = lambda c: [r for r in D["coph"]["Mod"]["longphase_v2.1"][c] if r["rep"] == 1]
    meth = lambda c: [{k: meth_value(c, k) for k in ("sw_pct", "ham", "n50", "psnv_pct")}]
    rows = [  # title, coverages, tools (key, name, getter), phased-fraction key, label, limits
        ("SNV phasing", PLOT_COVS,
         [("lp_gnn", "LongPhase 2", snv("lp_gnn")), ("wh", "WhatsHap", snv("wh")), ("hc", "HapCUT2", snv("hc"))],
         "psnv_pct", "Phased SNVs (%)", (76, 94)),
        ("SNV and indel co-phasing", PLOT_COVS,
         [("lp_gnn", "LongPhase 2", ind("longphase_v2.1")), ("wh", "WhatsHap", ind("whatshap_v28"))],
         "pindel_pct", "Phased indels (%)", (28, 52)),
        ("SNV and 5mC co-phasing", BAR_COVS,
         [("lp_gnn", "LongPhase 2", mod1), ("meth", "MethPhaser", meth)],
         "psnv_pct", "Phased SNVs (%)", (76, 94)),
    ]
    indel = {"lp_gnn": _indel_runs("longphase_coh_indel_gnn"), "wh": _indel_runs("whatshap_v28")}
    letters = iter("abcdefghijkl")
    keys = []
    for r, (sf, (title, covs, tools, pkey, plab, plim)) in enumerate(zip(sfs, rows)):
        axs = sf.subplots(1, 4)
        for t, _name, get in reversed(tools):   # LongPhase 2 drawn last, on top
            f = _series(get, covs)
            tline(axs[0], t, *f("sw_pct"))
            if r == 1:   # indel row: indel-pair switch errors and indel Hamming distance
                g = _series(indel[t], covs)
                xs, m, s_ = g("indel_sw_pct")
                line(axs[0], xs, m, s_, C[t], ls=":", marker=STY[t]["marker"], ms=STY[t]["ms"])
                tline(axs[1], t, *g("indel_ham"))
            else:
                tline(axs[1], t, *f("ham"))
            tline(axs[2], t, *f("n50"), scale=1e-6)
            tline(axs[3], t, *f(pkey))
        if r == 1:
            _log_rate_axis(axs[0], ticks=(0.02, 0.05, 0.1, 0.2, 0.5, 1), lim=(0.018, 1.4))
            axs[0].set_ylabel("Switch error rate (%)")
            axs[1].set_ylabel("Indel Hamming distance (%)")
        else:
            _log_rate_axis(axs[0])
            axs[0].set_ylabel("Switch error rate (%)")
            axs[1].set_ylabel("Hamming distance (%)")
        axs[1].set_ylim(bottom=0)
        axs[2].set_ylim(0, 4.6); axs[2].set_yticks([0, 1, 2, 3, 4]); axs[2].set_ylabel("Block N50 (Mb)")
        axs[3].set_ylim(*plim); axs[3].set_ylabel(plab)
        if pkey == "psnv_pct":
            axs[3].set_yticks([76, 80, 84, 88, 92])
        for ax in axs:
            cov_axis(ax)
            if r < 2:
                ax.set_xlabel("")
            letter(ax, next(letters))
        _row_header(sf, title)
        k = [thandle(t, name) for t, name, _ in tools]
        if r == 1:
            k += [Line2D([], [], color="#555555", ls="-", label="SNV pairs"),
                  Line2D([], [], color="#555555", ls=":", marker="o", ms=2.6, label="pairs with an indel")]
        keys.append(k)
    _row_keys(fig, sfs, keys)
    save(fig, os.path.join(OUT, "fig2_phaser_comparison.pdf"))


# ============================================================ Figure 3 =====
# Evidence combinations of LongPhase 2 (GNN correction included). Colours validated with
# the dataviz palette checker against each other and WhatsHap blue (all pairs, light
# mode); the all-four line is neutral black by design. Shared with Supplementary
# Figs. 14 and 15 through CFG.
STRAT = [  # co-phase sheet configuration ("SNV" = SNV_Detail), label, colour, marker, marker size
    ("SNV", "SNVs", "#B2182B", "o", 3.0),
    ("Mod", "SNVs + 5mC", "#1B9E77", "^", 3.4),
    ("Indel", "SNVs + indels", "#C66A00", "s", 3.2),
    ("Indel+Mod+SV", "All four classes", "#1A1A1A", "D", 2.8),
]


def fig3():
    """SNV switch error rate and block N50 of LongPhase 2 as evidence classes are added,
    and the resulting accuracy-contiguity paths beside WhatsHap's."""
    fig, axs = new_fig(60, 1, 3, width_ratios=[1, 1, 1.15])
    ax_sw, ax_n50, ax_tr = axs
    for cfg, name, col, mk, msz in STRAT:
        for ax, key, sc in ((ax_sw, "sw_pct", 1), (ax_n50, "n50", 1e-6)):
            xs, m, s_ = coph_series(cfg, "longphase_v2.1", key)
            line(ax, xs, m, s_, col, marker=mk, mfc="none", ms=msz, scale=sc)
    _log_rate_axis(ax_sw, ticks=(0.02, 0.05, 0.1), lim=(0.018, 0.12))
    ax_sw.set_ylabel("SNV switch error rate (%)"); cov_axis(ax_sw); letter(ax_sw, "a")
    ax_n50.set_ylim(0, 4.6); ax_n50.set_yticks([0, 1, 2, 3, 4])
    ax_n50.set_ylabel("Block N50 (Mb)"); cov_axis(ax_n50); letter(ax_n50, "b")
    # c: one path per configuration over 10, 20, ..., 60x, with WhatsHap for reference
    paths = [(name, col, mk, msz, "-", "none",
              (lambda cfg: lambda c: (D["snv"]["ONT"]["longphase_v2.1"][c] if cfg == "SNV"
                                      else D["coph"][cfg]["longphase_v2.1"][c]))(cfg))
             for cfg, name, col, mk, msz in STRAT]
    paths += [("WhatsHap, SNVs", C["wh"], "D", 2.8, "-", "none", lambda c: D["snv"]["ONT"]["whatshap_v28"][c]),
              ("WhatsHap, SNVs + indels", C["wh"], "D", 2.8, "--", C["wh"], lambda c: D["coph"]["Indel"]["whatshap_v28"][c])]
    for name, col, mk, msz, ls, mfc, get in paths:
        xs = [ms(get(c), "sw_pct")[0] for c in BAR_COVS]
        ys = [ms(get(c), "n50")[0] / 1e6 for c in BAR_COVS]
        ax_tr.plot(xs, ys, color=col, ls=ls, marker=mk, ms=msz, mfc=mfc, mew=0.8)
    for c, dy, va in ((10, -4, "top"), (60, 4, "bottom")):
        get = paths[-1][-1]
        ax_tr.annotate(f"{c}×", (ms(get(c), "sw_pct")[0], ms(get(c), "n50")[0] / 1e6), xytext=(0, dy),
                       textcoords="offset points", ha="center", va=va, fontsize=5.5, color="#555555")
    ax_tr.set_xscale("log"); ax_tr.minorticks_off()
    ax_tr.set_xticks([0.02, 0.05, 0.1, 0.2]); ax_tr.set_xticklabels(["0.02", "0.05", "0.1", "0.2"])
    ax_tr.set_xlim(0.018, 0.32); ax_tr.set_ylim(0, 4.6); ax_tr.set_yticks([0, 1, 2, 3, 4])
    ax_tr.set_xlabel("SNV switch error rate (%)"); ax_tr.set_ylabel("Block N50 (Mb)")
    letter(ax_tr, "c")
    h = [Line2D([], [], color=col, ls=ls, marker=mk, ms=msz + 0.4, mfc=mfc, mew=0.8, label=name)
         for name, col, mk, msz, ls, mfc, _ in paths]
    fig.legend(handles=h, loc="outside upper center", ncol=6, handlelength=2.4, columnspacing=1.2)
    save(fig, os.path.join(OUT, "fig3_evidence_classes.pdf"))


# ============================================================ Figure 4 =====
F3 = [  # key, label, colour, line style, marker, v5.0q source, v4.2.1 tool name (Supplementary Table 9)
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


REGIONS = [  # (region, stratum) in item4_strata.tsv, label, y; truth v5.0q. Benchmark regions
    # first; the outside-both row, where the truth phase is least certain, is set apart as
    # exploratory (Discussion).
    (("v5bed", "any"), "v5.0q benchmark regions", 0),
    (("v5bed", "not_difficult"), "v5.0q regions, not difficult", 1),
    (("v5bed", "segdup"), "v5.0q regions, segmental duplications", 2),
    (("neither", "any"), "Outside both benchmarks' regions\n(exploratory)", 3.4),
]


def fig4():
    """The same SNV-only VCFs under GIAB v4.2.1 and v5.0q: switch errors by coverage; at 60x
    the switch errors that all three tools make at the same SNV pair; and v5.0q switch error
    rates by benchmark region and GIAB v3.6 stratum at 10x and 60x (issue #1 item 4)."""
    fig = plt.figure(figsize=(FIGW, 100 * MM), layout="constrained")
    fig.get_layout_engine().set(w_pad=2 * MM, h_pad=1.2 * MM, wspace=0.05, hspace=0.0)
    top, bottom = fig.subfigures(2, 1, height_ratios=[1.45, 1], hspace=0.03)
    axs = top.subplots(1, 3, width_ratios=[1, 1, 1.1])
    series = [x for x in F3 if x[0] in ("wh", "hc", "lp_gnn")]
    series.sort(key=lambda x: ["wh", "hc", "lp_gnn"].index(x[0]))
    for ax, bench, L in ((axs[0], "v421", "a"), (axs[1], "v50q", "b")):
        for k, name, col, ls, mk, src, v421name in series:
            xs, m_, s_ = [], [], []
            for c in PLOT_COVS:
                runs = D["v421"][v421name][c] if bench == "v421" else f3_runs(src, c)
                a_, b_ = ms(runs, "sw")
                xs.append(c); m_.append(a_ / 1000); s_.append(b_ / 1000)
            tline(ax, k, xs, m_, s_)
        ax.set_ylim(0, 5.3); ax.set_ylabel("Switch errors (thousands)"); cov_axis(ax); letter(ax, L)
        ax.set_title("GIAB v4.2.1" if bench == "v421" else "T2T-HG002-derived v5.0q", fontsize=6.5)
    ax = axs[2]   # item4_overlap.tsv (issue #1), replicate 1, 60x
    ov = {r["truth"]: r for r in _tsv("item4_overlap.tsv") if r["run"] == "60x_1"}
    rows = [("v4", "LP2", "lp_gnn"), ("v4", "WH", "wh"), ("v4", "HC2", "hc"),
            ("v5", "LP2", "lp_gnn"), ("v5", "WH", "wh"), ("v5", "HC2", "hc")]
    ys = [0, 1, 2, 3.6, 4.6, 5.6]
    for y, (truth, col, t) in zip(ys, rows):
        tot, shared = int(ov[truth][col]), int(ov[truth]["all3"])
        ax.barh(y, shared / 1000, 0.72, color="#BDBDBD", zorder=3)
        ax.barh(y, (tot - shared) / 1000, 0.72, left=shared / 1000, color=C[t], zorder=3)
        ax.text(tot / 1000 + 0.05, y, f"{100 * shared / tot:.0f}%", va="center", ha="left", fontsize=5.5)
    ax.set_yticks(ys); ax.set_yticklabels(["LongPhase 2", "WhatsHap", "HapCUT2"] * 2)
    ax.invert_yaxis(); ax.tick_params(axis="y", length=0)
    for y0, lab in ((-0.75, "GIAB v4.2.1"), (2.85, "T2T-HG002-derived v5.0q")):
        ax.text(0, y0, lab, fontsize=6, va="center", ha="left")
    ax.set_xlim(0, 2.75); ax.set_xlabel("Switch errors at 60× (thousands)")
    letter(ax, "c")
    S = _group(_tsv("item4_strata.tsv"),
               lambda r: (r["tool"], int(r["coverage"]), r["truth"], r["region"], r["stratum"]))
    tools = (("lp_gnn", "longphase_gnn"), ("wh", "whatshap_v28_onlySNVs"), ("hc", "hapcut2_v134"))
    axs2 = bottom.subplots(1, 2, sharey=True)
    for ax, cov, L, xl in ((axs2[0], 10, "d", (0.02, 8)), (axs2[1], 60, "e", (0.0008, 5))):
        for key, _lab, y in REGIONS:
            vals = []
            for t, name in tools:
                runs = S[(name, cov, "v5") + key]
                vals.append(sum(float(r["snv_sw_rate%"]) for r in runs) / len(runs))
            ax.plot([min(vals), max(vals)], [y, y], color="#D9D9D9", lw=1.6, zorder=1, solid_capstyle="round")
            for (t, _n), v in zip(tools, vals):
                st = STY[t]
                ax.plot([v], [y], ls="", marker=st["marker"], ms=st["ms"] + 0.6, mfc="none", mec=C[t],
                        mew=0.9, zorder=3)
        ax.set_xscale("log"); ax.minorticks_off()
        ticks = [t for t in (0.001, 0.01, 0.1, 1) if xl[0] <= t <= xl[1]]
        ax.set_xticks(ticks); ax.set_xticklabels([f"{t:g}" for t in ticks])
        ax.set_xlim(*xl)
        ax.set_xlabel("Switch error rate against v5.0q (%)")
        ax.set_title(f"{cov}×", fontsize=6.5)
        ax.grid(axis="x", color="#EEEEEE", lw=0.5, zorder=0)
        ax.axhline(2.7, color="#BDBDBD", lw=0.5, ls="--", zorder=0)
        letter(ax, L)
    axs2[0].set_yticks([y for _, _, y in REGIONS]); axs2[0].set_yticklabels([lab for _, lab, _ in REGIONS])
    axs2[0].invert_yaxis(); axs2[0].tick_params(axis="y", length=0)
    axs2[1].tick_params(axis="y", length=0)
    h = [thandle(t, {"wh": "WhatsHap"}.get(t)) for t in ("lp_gnn", "wh", "hc")]
    h.append(Patch(color="#BDBDBD", label="switch error shared by all three tools (c)"))
    top.legend(handles=h, loc="outside upper center", ncol=4, handlelength=2.6, columnspacing=1.4)
    save(fig, os.path.join(OUT, "fig4_two_benchmarks.pdf"))


# ============================================================ Figure 5 =====
def fig5():
    """PacBio HiFi: LongPhase 2 vs WhatsHap, columns as in Fig. 2 (one replicate per coverage)."""
    tools = ["wh", "lp_gnn"]
    fig, axs = new_fig(52, 1, 4)
    specs = [("sw_pct", "Switch error rate (%)", (0, 0.15), 1),
             ("ham", "Hamming distance (%)", (0, 2), 1),
             ("n50", "Block N50 (kb)", (0, 600), 1e-3),
             ("psnv_pct", "Phased SNVs (%)", (84, 94), 1)]
    for ax, (key, lab, ylim, sc), L in zip(axs, specs, "abcd"):
        for t in tools:
            xs, m, s_ = snv_series(t, key, plat="HiFi", covs=HIFI_COVS)
            tline(ax, t, xs, m, s_, scale=sc, label=NAME[t])
        ax.set_ylim(*ylim); ax.set_ylabel(lab); cov_axis(ax, HIFI_COVS); letter(ax, L)
    h = [thandle(t, {"wh": "WhatsHap"}.get(t)) for t in ("lp_gnn", "wh")]
    fig.legend(handles=h, loc="outside upper center", ncol=2, handlelength=2.6)
    save(fig, os.path.join(OUT, "fig5_hifi.pdf"))


# ============================================================ Figure 6 =====
# Source: gnn_prepare/unphased_e6/unphased_grid.tsv (analyze_unphased.py,
# 2026-10-07; final GNN model). SNV-only, seed 1; SNVs phased by LongPhase 2
# and unphased after correction, matched to the v5.0q benchmark VCF by position
# (no benchmark BED).
COMPOSITION = {  # cov: (absent, hom-alt, het)
    10: (46276, 2830, 6650), 12: (48906, 2613, 5734), 14: (49490, 2373, 4928),
    16: (50781, 2223, 4242), 18: (52143, 2151, 3868), 20: (52592, 2069, 3207),
    30: (52290, 1916, 2896), 40: (52775, 1845, 2425), 50: (51769, 1818, 2320),
    60: (52167, 1694, 2215),
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
    """Margin and Ralphi at 10-20x (GCphase not included; see Methods)."""
    tools = ["hc", "wh", "ralphi", "margin", "lp_gnn"]
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
        for cfg, col in (("SNV", CFGC["SNV"]), ("Indel+Mod+SV", CFGC["Indel+Mod+SV"])):
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
    h2 = [Line2D([], [], color=CFGC["SNV"], label="SNV only"),
          Line2D([], [], color=CFGC["Indel+Mod+SV"], label="all four classes"),
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


# ------------------------------------------- issue #1 tables (Tables 13-14) ---
STRATA = os.path.join(ROOT, "notes", "benchmark_strata")
S_TOOLS = (("longphase_gnn", "LongPhase 2"), ("whatshap_v28_onlySNVs", "WhatsHap"), ("hapcut2_v134", "HapCUT2"))
S_COVS = (10, 20, 30, 60)


def _tsv(name):
    import csv
    return list(csv.DictReader(open(os.path.join(STRATA, name)), delimiter="\t"))


def _group(rows, keyf):
    g = {}
    for r in rows:
        g.setdefault(keyf(r), []).append(r)
    return g


def strata_tables(w, L):
    S = _group(_tsv("item4_strata.tsv"),
               lambda r: (r["tool"], int(r["coverage"]), r["truth"], r["region"], r["stratum"]))
    # ---- Table 13a: switch errors by truth set and region
    w(r"{\scriptsize\setlength{\tabcolsep}{3.2pt}")
    w(r"\begin{longtable}{@{}llrrrrrrrr@{}}")
    w(r"\caption{\textbf{Location of SNV switch errors by truth set and benchmark region.} \textbf{a}, switch errors by truth set and region; \textbf{b}, by genomic stratum within the v5.0q benchmark regions; \textbf{c}, switch errors shared by the three tools. SNV-only phasing of HG002 nanopore R10.4.1 data; \toolname with GNN correction. A variant pair is assigned to a region when both of its variants lie in it, so region counts do not sum to the total. \emph{Shared}, inside both sets of benchmark regions; \emph{v5.0q only}, inside the v5.0q regions only; \emph{outside}, outside both. Means over ten replicates at 10 and 20$\times$; one replicate at 30 and 60$\times$. Rates are switch errors per assessed SNV pair. Per-run values for every coverage, region and stratum are in Supplementary Data~1.}\label{tab:strata}\\")
    hdr = (r"\toprule & & \multicolumn{2}{c}{v4.2.1} & \multicolumn{6}{c}{v5.0q} \\ \cmidrule(lr){3-4}\cmidrule(l){5-10}"
           r" Tool & Cov. & All & Shared & All & \shortstack[r]{Inside\\v5.0q} & \shortstack[r]{Rate inside\\v5.0q (\%)} & Shared & \shortstack[r]{v5.0q\\only} & \shortstack[r]{Outside\\(rate, \%)} \\ \midrule")
    w(hdr + r"\endfirsthead")
    w(hdr + r"\endhead")
    for tool, name in S_TOOLS:
        for c in S_COVS:
            def sw(truth, region, stratum="any", key="snv_sw", d=0):
                return f"{ms(S[(tool, c, truth, region, stratum)], key)[0]:,.{d}f}"
            w(f"{name if c == S_COVS[0] else ''} & {c}$\\times$ & {sw('v4', 'all')} & {sw('v4', 'shared')} & {sw('v5', 'all')} & "
              f"{sw('v5', 'v5bed')} & {sw('v5', 'v5bed', key='snv_sw_rate%', d=4)} & {sw('v5', 'shared')} & {sw('v5', 'v5only')} & "
              f"{sw('v5', 'neither')} ({sw('v5', 'neither', key='snv_sw_rate%', d=2)}) \\\\")
        w(r"\midrule")
    L[-1] = r"\bottomrule"
    w(r"\end{longtable}")
    # panel b: strata inside the v5.0q benchmark regions
    w(r"\par\medskip\noindent\textbf{b}\enspace Within the v5.0q benchmark regions, by GIAB v3.6 stratum\par\smallskip")
    w(r"\noindent\begin{tabular}{@{}llrrrrrr@{}}\toprule")
    w(r"Tool & Cov. & \shortstack[r]{Segmental\\duplication} & \shortstack[r]{Low mappability\\or seg.\ dup.} & \shortstack[r]{Tandem\\repeat} & Homopolymer & Satellite & \shortstack[r]{Not\\difficult} \\ \midrule")
    for tool, name in S_TOOLS:
        for c in S_COVS:
            cells = [f"{ms(S[(tool, c, 'v5', 'v5bed', st_)], 'snv_sw')[0]:,.0f}"
                     for st_ in ("segdup", "lowmap_segdup", "tandem_repeat", "homopolymer", "satellite", "not_difficult")]
            w(f"{name if c == S_COVS[0] else ''} & {c}$\\times$ & " + " & ".join(cells) + r" \\")
        w(r"\midrule")
    L[-1] = r"\bottomrule\end{tabular}"
    # panel c: coincident switch errors (replicate 1)
    O = {(r["truth"], r["run"]): r for r in _tsv("item4_overlap.tsv")}
    w(r"\par\medskip\noindent\textbf{c}\enspace Switch errors at identical SNV pairs across tools, replicate 1\par\smallskip")
    w(r"\noindent\begin{tabular}{@{}llrrrrr@{}}\toprule")
    w(r"Truth & Cov. & \toolname & \whatshap & \hapcut & All three & \shortstack[r]{All three\\(\% of \toolname)} \\ \midrule")
    for truth, lab in (("v4", "v4.2.1"), ("v5", "v5.0q")):
        for c in S_COVS:
            r = O[(truth, f"{c}x_1")]
            lp, a3 = int(r["LP2"]), int(r["all3"])
            w(f"{lab if c == S_COVS[0] else ''} & {c}$\\times$ & {lp:,} & {int(r['WH']):,} & {int(r['HC2']):,} & {a3:,} & {100 * a3 / lp:.0f} \\\\")
        w(r"\midrule")
    L[-1] = r"\bottomrule\end{tabular}}" + "\n"
    # ---- Table 14: indel phase accuracy
    I = _group(_tsv("item3_indel.tsv"), lambda r: (r["config"], int(r["coverage"]), r["region"]))
    cfgs = (("longphase_coh_indel_gnn", r"\toolname, +indel"), ("longphase_coh_indel", r"same, no GNN"),
            ("longphase_cophasing_gnn", r"\toolname, four classes"), ("whatshap_v28", r"\whatshap, +indel"))
    w(r"{\scriptsize\setlength{\tabcolsep}{2.5pt}")
    w(r"\begin{longtable}{@{}llrrrrrr@{}}")
    w(r"\caption{\textbf{Phase accuracy of indels against v5.0q.} HG002 nanopore R10.4.1 data, co-phasing runs. Indel-pair switch errors are counted over consecutive variant pairs of an intersected block that include at least one indel; the indel Hamming distance uses the block orientation chosen on all variants. Truth VCF used in full; the last column restricts the indel-pair rate to the v5.0q benchmark regions. Means (s.d.) over ten replicates at 10 and 20$\times$; one replicate at 30 and 60$\times$. Per-run values are in Supplementary Data~1.}\label{tab:indel}\\")
    hdr = (r"\toprule Configuration & Cov. & \shortstack[r]{Phased\\indels} & \shortstack[r]{Indel-pair\\switch errors} & \shortstack[r]{Indel-pair\\rate (\%)} & \shortstack[r]{SNV+indel\\rate (\%)} & \shortstack[r]{Indel\\Hamming (\%)} & \shortstack[r]{Indel-pair rate,\\inside v5.0q (\%)} \\ \midrule")
    w(hdr + r"\endfirsthead")
    w(hdr + r"\endhead")
    for cfg, name in cfgs:
        for c in S_COVS:
            a, b = I[(cfg, c, "all")], I[(cfg, c, "v5bed")]
            w(f"{name if c == S_COVS[0] else ''} & {c}$\\times$ & {cell(a, 'phased_indel', 0)} & {cell(a, 'indel_sw', 0)} & "
              f"{cell(a, 'indel_sw_rate%', 3)} & {cell(a, 'snv_indel_sw_rate%', 3)} & {cell(a, 'indel_hamming%', 2)} & {cell(b, 'indel_sw_rate%', 3)} \\\\")
        w(r"\midrule")
    w(r"\bottomrule")
    w(r"\end{longtable}}" + "\n")


# ================================================== Supplementary tables ===
# ------------------------------------------- issue #2 table (Table 15) ---
HELDOUT = os.path.join(ROOT, "notes", "heldout")
H_TOOLS = (("longphase_gnn", "LongPhase 2"), ("longphase", "without GNN"), ("whatshap_v28_onlySNVs", "WhatsHap"),
           ("hapcut2_v134", "HapCUT2"), ("margin_v231", "Margin"), ("ralphi", "Ralphi"))


def _heldout(name):
    """Per-run ### summary lines of a notes/heldout table -> {tool: {cov: [run dicts]}}."""
    d = {}
    for line in open(os.path.join(HELDOUT, name)):
        if not line.startswith("###") or line.startswith("###Sample"):
            continue
        f_ = line[3:].rstrip("\n").split("\t")
        m = re.match(r"(.+)_(\d+)x_(\d+)\.", f_[0])
        d.setdefault(m.group(1), {}).setdefault(int(m.group(2)), []).append(
            dict(psnv=float(f_[1]), sw=float(f_[5]), sw_pct=float(f_[6]), ham=float(f_[7]), n50=float(f_[9])))
    return d


def heldout_table(w):
    """SNV-only phasing on the chromosomes held out from GNN training (issue #2)."""
    w(r"{\scriptsize\setlength{\tabcolsep}{3pt}")
    w(r"\begin{longtable}{@{}llrrrrrrrrr@{}}")
    w(r"\caption{\textbf{SNV-only phasing on the chromosomes held out from GNN training (chr17, chr21 and chr22).} HG002 nanopore R10.4.1 data; the phased VCFs of the genome-wide analysis scored with \code{longphase compare --regions=chr17,chr21,chr22} against each truth VCF in full. Switch errors of \toolname as mean (s.d.); switch error rates in \%. \emph{Removed}, switch errors removed by GNN correction relative to \toolname without it; \emph{cost}, phased SNVs withheld per removed switch error (the deployment criterion requires at most 10; Supplementary Method~4). Means over ten replicates at 10--20$\times$; one replicate at 30--60$\times$. Margin and Ralphi were run at 10--20$\times$ only.}\label{tab:heldout}\\")
    head = (r"\toprule & & \multicolumn{2}{c}{\toolname} & \multicolumn{5}{c}{Switch error rate (\%)} & \multicolumn{2}{c}{GNN correction} \\"
            r" \cmidrule(lr){3-4}\cmidrule(lr){5-9}\cmidrule(l){10-11} Truth & Cov. & Switch errors & Rate (\%) & without GNN & \whatshap & \hapcut & Margin & Ralphi & Removed (\%) & Cost \\ \midrule")
    w(head + r"\endfirsthead")
    w(head + r"\endhead")
    for tag, fn in (("v5.0q", "heldout_v50q.txt"), ("v4.2.1", "heldout_GIAB421.txt")):
        H = _heldout(fn)
        for c in COVS:
            g, n = H["longphase_gnn"][c], H["longphase"][c]
            rate = lambda t: f(ms(H[t][c], "sw_pct")[0], 3) if c in H.get(t, {}) else "--"
            dsw = ms(n, "sw")[0] - ms(g, "sw")[0]
            dps = ms(n, "psnv")[0] - ms(g, "psnv")[0]
            removed = f"{100 * dsw / ms(n, 'sw')[0]:.1f}"
            cost = f"{dps / dsw:.1f}" if dsw > 0 else "--"
            w(f"{tag if c == COVS[0] else ''} & {c}$\\times$ & {cell(g, 'sw', 0)} & {rate('longphase_gnn')} & {rate('longphase')} & "
              f"{rate('whatshap_v28_onlySNVs')} & {rate('hapcut2_v134')} & {rate('margin_v231')} & {rate('ralphi')} & {removed} & {cost} \\\\")
        w(r"\midrule" if tag == "v5.0q" else "")
    w(r"\bottomrule\end{longtable}}")


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
    w(r"\caption{\textbf{Input call sets per coverage.} Heterozygous (het.) and homozygous (hom.) calls entering the phasing runs; nanopore values at 10--20$\times$ are means (s.d.) over ten down-sampling replicates. Small variants from PEPPER-Margin-DeepVariant, SVs from Sniffles2 2.8.0, allele-specific 5mC sites from \code{longphase modcall}. SVs and 5mC were not called on the HiFi data. Homozygous SNVs include the PEPPER candidates genotyped homozygous reference (\code{refCall}).}")
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
    w(r"\caption{\textbf{SNV-only phasing of HG002 nanopore R10.4.1 data by six configurations.} Scored against the v5.0q VCF (chr1--22, no benchmark BED applied). Values at 10--20$\times$ are means (s.d.) over ten down-sampling replicates; 30--60$\times$, one replicate. Phased SNVs are given as a percentage of the 2,398,880 heterozygous SNVs of the benchmark. Margin and Ralphi were run at 10--20$\times$ only; GCphase was not included (Methods). Ralphi's phase blocks sum to 4.3--5.8~Gb, more than the length of the autosomes, so its block N50 is not comparable with that of the other tools.}\label{tab:snvall}\\")
    w(r"\toprule Tool & Cov. & \shortstack[r]{Phased\\SNV (\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & Blocks & \shortstack[r]{N50\\(Mb)} \\ \midrule\endfirsthead")
    w(r"\toprule Tool & Cov. & \shortstack[r]{Phased\\SNV (\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & Blocks & \shortstack[r]{N50\\(Mb)} \\ \midrule\endhead")
    for t in ["lp_gnn", "lp", "wh", "hc", "margin", "ralphi"]:
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
    w(r"\caption{\textbf{SNV-only phasing of HG002 PacBio HiFi (Revio) data.} One replicate per coverage, scored against v5.0q. The network was trained on nanopore data only and applied without retraining. Variants were called separately at every coverage (Methods).}")
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
    strata_tables(w, L)
    heldout_table(w)
    path = os.path.join(ROOT, "figures-source", "supp_tables.tex")
    open(path, "w").write("\n".join(L) + "\n")
    print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    fig2(); fig3(); fig4(); fig5(); fig6()
    sfig10(); sfig11(); sfig12(); sfig13(); sfig14(); sfig15(); sfig17()
    tables()
