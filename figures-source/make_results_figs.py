#!/usr/bin/env python3
"""Generate the Results figures (Figs. 2-4), Supplementary Figs. 9-15 and
Supplementary Tables 7-17 for the
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
    figures/fig{2..4}_*.pdf
    figures/supp/suppfig{10..16}_*.pdf and suppfig_runtime.pdf
    figures-source/supp_tables.tex   (\\input by Supplementary.tex)
"""
import os
import re
import statistics as st

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
    "xtick.major.pad": 2,
    "ytick.major.pad": 2,
    "axes.labelpad": 2.5,
    "axes.titlepad": 3,
    "legend.handletextpad": 0.5,
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
    "hp":     "#35978F",   # HiPhase (PacBio), HiFi only
    "hb":     "#E08214",   # HapBridge, nanopore SNV + 5mC only
    "lh":     "#4D9221",   # LongHap, nanopore SNV + 5mC only
}
NAME = {
    "lp_gnn": "LongPhase 2", "lp": "LongPhase 2 without GNN",
    "wh": "WhatsHap (SNVs only)", "wh_ind": "WhatsHap (SNVs + indels)",
    "hc": "HapCUT2", "margin": "Margin", "ralphi": "Ralphi", "gc": "GCphase",
    "meth": "MethPhaser", "hp": "HiPhase", "hb": "HapBridge", "lh": "LongHap",
}
XLSX_TOOL = {"lp": "longphase_v2.0.1", "lp_gnn": "longphase_v2.1.2",
             "wh": "whatshap_v28", "hc": "hapcut2_v134", "margin": "margin_v231",
             "ralphi": "ralphi", "gc": "gcphase"}
COVS = [10, 12, 14, 16, 18, 20, 30, 40, 50, 60]
BAR_COVS = [10, 20, 30, 40, 50, 60]
HIFI_COVS = [10, 20, 30, 40, 50]

# Co-phasing configurations: xlsx sheet label -> display name, colour.
# SNV, +5mC, +indel and all four as in Supplementary Figs. 14 and 15.
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
CFGM = {"SNV": "o", "SV": "v", "Mod": "^", "Indel": "s", "Indel+SV": "<", "Mod+Indel": ">", "Indel+Mod+SV": "D"}


FIGW = 183 * MM          # Nature double-column width; figures are saved at exactly this width
_LETTERS = []


def letter(ax, s, title=None, **_):
    """Panel letter (8 pt bold), placed in save() at the left edge of the panel's
    tick labels / axis label, level with the top of the panel. An empty left title
    reserves the vertical space under constrained layout. With `title`, a 7 pt bold panel
    title follows the letter on the same baseline (Fig. 2), above the axes."""
    if title:
        ax.set_title(" ", loc="left", fontsize=8, pad=6)
    else:
        ax.set_title(" ", loc="left", fontsize=8)
    _LETTERS.append((ax, s, title))


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
        return snv_series({"longphase_v2.0.1": "lp", "longphase_v2.1.2": "lp_gnn"}[tool], key, covs=covs)
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
    "hc":     dict(marker="s", ls="-", mfc="none", dx=0.0, ms=4.0),   # solid since 2026-10-13: dashed means "+ indels" in Fig. 2d
    "margin": dict(marker="^", ls="-", mfc="none", dx=0.0, ms=3.4),
    "ralphi": dict(marker="v", ls="-", mfc="none", dx=0.0, ms=3.4),
    "gc":     dict(marker="P", ls="-", mfc="none", dx=0.0, ms=3.4),
    "meth":   dict(marker="^", ls="-", mfc="none", dx=0.0, ms=3.4),
    "hp":     dict(marker="v", ls="-", mfc="none", dx=0.0, ms=3.4),
    "hb":     dict(marker="P", ls="-", mfc="none", dx=0.0, ms=3.6),
    "lh":     dict(marker="X", ls="-", mfc="none", dx=0.0, ms=3.6),
}


def hiphase(c):
    """HiPhase 1.7.0 on PacBio HiFi data, SNV-only phasing (replicate 1): sheet Other_phasers of
    Supplementary Data 1 (JHL, 2026-10-18). HiPhase has no SNV-only option, so it was given the call
    set restricted to SNVs. In Fig. 2c,g, Supplementary Fig. 16c and Table 11 since 2026-10-19
    (author decision: the PacBio phaser must be in the HiFi comparison)."""
    r = _other_phasers().get(("HiFi", "HiPhase 1.7.0 (SNV-only input VCF)", c))
    return [r] if r else None


def meth_other(t):
    """HapBridge (on the MethPhaser input) or LongHap (SNVs with 5mC) on nanopore data, replicate 1:
    sheet Other_phasers of Supplementary Data 1. With MethPhaser in Fig. 3 since 2026-10-20 (author
    decision: every methylation-aware phaser that the Introduction names and that phases variants;
    NanoMethPhase does not)."""
    label = {"hb": "HapBridge ec48f02 (on LongPhase 2 SNV output, no GNN)",
             "lh": "LongHap 0.2.0 (SNVs, with 5mC)"}[t]
    def get(c):
        r = _other_phasers().get(("ONT", label, c))
        return [r] if r else None
    return get


def _other(plat, label):
    """Getter cov -> [row] of one Other_phasers run (replicate 1), None where the run is absent."""
    def get(c):
        r = _other_phasers().get((plat, label, c))
        return [r] if r else None
    return get


def tline(ax, t, xs, m, s, scale=1.0, label=None, band=True):
    st = STY[t]
    line(ax, [x + st["dx"] for x in xs], m, s, C[t], ls=st["ls"], marker=st["marker"],
         scale=scale, label=label, mfc=st["mfc"], ms=st["ms"], band=band)


def thandle(t, label=None):
    st = STY[t]
    return Line2D([], [], color=C[t], ls=st["ls"], marker=st["marker"], ms=st["ms"] + 0.4,
                  mfc=st["mfc"], mew=0.8, label=label or NAME[t])


def line(ax, xs, m, s, color, ls="-", marker="o", label=None, scale=1.0, mfc=None, z=3, ms=2.6, band=True):
    """Mean line with markers; replicate s.d. as a light band (zero width for single runs)."""
    m = [v * scale for v in m]; s = [v * scale for v in s]
    if band and any(s):
        ax.fill_between(xs, [a - b for a, b in zip(m, s)], [a + b for a, b in zip(m, s)],
                        color=color, alpha=0.18, lw=0, zorder=z - 1)
    ax.plot(xs, m, color=color, ls=ls, marker=marker, ms=ms, mfc=mfc or color,
            mew=0.8 if mfc == "none" else 0.6, label=label, zorder=z)


def cov_axis(ax, covs=(10, 20, 30, 40, 50, 60)):
    ax.set_xticks(list(covs))
    ax.set_xticklabels([f"{c}" for c in covs])
    ax.set_xlabel("Coverage (×)")


def align_ylabels(fig, columns):
    """Place the y-labels of each column of panels at one x position, just left of the
    widest tick labels in that column, so that labels line up across rows."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    pad = plt.rcParams["axes.labelpad"] * fig.dpi / 72
    for col in columns:
        left = []
        for ax in col:
            bbs = [t.get_window_extent(r) for t in ax.get_yticklabels() if t.get_text()]
            left.append((min(b.x0 for b in bbs) - pad - ax.bbox.x0) / ax.bbox.width)
        for ax in col:
            ax.yaxis.set_label_coords(min(left), 0.5)


def _tidy_ticks(fig):
    """Automatic linear tick locators use steps of 1, 2 or 5 only, so that tick labels need
    as few decimals as possible (0, 0.05, 0.10 rather than 0.000, 0.025, 0.050)."""
    from matplotlib.ticker import AutoLocator, MaxNLocator
    for ax in fig.findobj(matplotlib.axes.Axes):
        for axis, scale in ((ax.xaxis, ax.get_xscale()), (ax.yaxis, ax.get_yscale())):
            if scale == "linear" and type(axis.get_major_locator()) is AutoLocator:
                axis.set_major_locator(MaxNLocator(nbins=6, steps=[1, 2, 5, 10]))


def log_ticks(ax, ticks, axis="y"):
    """Plain decimal labels on a log axis (no 10^x notation, no minor labels)."""
    a = ax.yaxis if axis == "y" else ax.xaxis
    ax.minorticks_off()
    a.set_ticks(list(ticks)); a.set_ticklabels([f"{t:g}" for t in ticks])


def save(fig, path):
    _tidy_ticks(fig)
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    fig.set_layout_engine("none")
    W, H = fig.get_size_inches() * fig.dpi
    for ax, s_, title in [x for x in _LETTERS if x[0].get_figure(root=True) is fig]:
        tb = ax.get_tightbbox(r)
        if not title:
            fig.text(max(tb.x0, 0) / W, min(tb.y1, H) / H, s_, fontsize=8, fontweight="bold",
                     va="top", ha="left")
            continue
        yb = (ax._left_title.get_window_extent(r).y1 - 8 * 0.74 * fig.dpi / 72) / H
        lt = fig.text(max(tb.x0, 0) / W, yb, s_, fontsize=8, fontweight="bold", va="baseline", ha="left")
        x = lt.get_window_extent(r).x1 + 1.6 * MM * fig.dpi
        fig.text(x / W, yb, title, fontsize=7, fontweight="bold", va="baseline", ha="left")
    fig.savefig(path, metadata={"CreationDate": None})   # no timestamp: unchanged figures stay byte-identical
    w_mm = fig.get_size_inches()[0] * 25.4
    plt.close(fig)
    print(f"wrote {os.path.relpath(path, ROOT)} ({w_mm:.0f} mm wide)")


# ============================================================ Figure 2 =====
# MethPhaser values: sheet MethPhaser of Supplementary Data 1 (issue #5, JHL 5fb01f5): the
# output of MethPhaser 0.0.4 with the PS-lookup patch, on the uncorrected SNV-only LongPhase 2
# run (xlsx SNV_Detail, longphase_v2.0.1, replicate 1). The earlier values here
# (MethPhaserCompare.jsx, 2026-10-03) were those of the input run.


def rep1(cfg, tool, cov, key):
    runs = D["coph"][cfg][tool][cov]
    return [r for r in runs if r["rep"] == 1][0][key]


def meth_value(cov, key):
    """MethPhaser metric at one coverage (replicate 1). MethPhaser phases the SNVs of its input."""
    run = [r for r in D["snv"]["ONT"]["longphase_v2.0.1"][cov] if r["rep"] == 1][0]
    assert D["meth"][cov]["psnv"] == run["psnv"]
    return D["meth"][cov][key]


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
    W, H = fig.get_size_inches() * fig.dpi
    for sf, handles in zip(sfs, keys):
        bb = sf._suptitle.get_window_extent(r)
        x1 = sf.bbox.x1 if sf.bbox.x1 < W - 1 else W   # a row narrower than the figure (Fig. 2a,b,d,e)
        x1 -= 3 * MM * fig.dpi * (x1 < W)              # ends 3 mm short of the next row title
        sf.legend(handles=handles, loc="center right", bbox_to_anchor=(x1 / W, (bb.y0 + bb.y1) / 2 / H),
                  bbox_transform=fig.transFigure, ncol=len(handles), handlelength=2.6,
                  columnspacing=1.6, borderaxespad=0.0, borderpad=0.0)


def _log_rate_axis(ax, ticks=(0.02, 0.05, 0.1, 0.2), lim=(0.018, 0.32)):
    ax.set_yscale("log"); ax.minorticks_off()
    ax.set_yticks(list(ticks)); ax.set_yticklabels([f"{t:g}" for t in ticks])
    ax.set_ylim(*lim)


def _indel_runs(config, tool):
    """Per-replicate SNV and indel accuracy of one SNV + indel co-phasing run type (issue #1
    item 3, whole genome). The SNV Hamming distance is calculated (author, 2026-10-12): the
    `co-phase_Detail` Hamming distance over all variants in blocks, minus the indel mismatches,
    over the phased SNVs. SNVs in one-variant blocks are not removed from the denominator
    (error < 0.3% of the value); the exact value needs ham_all and ham_n of out/*.tsv."""
    g = {}
    for r in _tsv("item3_indel.tsv"):
        if r["config"] == config and r["region"] == "all":
            c, rep_ = int(r["coverage"]), int(r["replicate"])
            x = [d for d in D["coph"]["Indel"][tool][c] if d["rep"] == rep_][0]
            assert x["psnv"] == int(r["phased_snv"])
            n_snv, n_ind, h_ind = int(r["phased_snv"]), int(r["indels_in_blocks"]), int(r["indel_hamming"])
            g.setdefault(c, []).append(
                {"snv_sw_pct": float(r["snv_sw_rate%"]), "indel_sw_pct": float(r["indel_sw_rate%"]),
                 "snv_ham": 100 * (x["ham"] / 100 * (n_snv + n_ind) - h_ind) / n_snv,
                 "indel_ham": float(r["indel_hamming%"])})
    return lambda c: g.get(c)


def _path(ax, get, covs, color, ls, marker, msz, mfc="none", z=3):
    """Accuracy-contiguity path: mean SNV switch error rate against mean block N50, one
    point per coverage, joined from the lowest to the highest coverage."""
    xs = [ms(get(c), "sw_pct")[0] for c in covs]
    ys = [ms(get(c), "n50")[0] / 1e6 for c in covs]
    ax.plot(xs, ys, color=color, ls=ls, marker=marker, ms=msz, mfc=mfc, mew=0.8, lw=0.9, zorder=z)
    return xs, ys


def _tradeoff_axis(ax, ylim=(0, 5.9), yticks=(0, 1, 2, 3, 4, 5), xlim=(0.018, 0.32)):
    """SNV switch error rate (log) against block N50 (Fig. 2 row 2, Fig. 3 row 1). The default N50
    range is that of nanopore data (MethPhaser reaches 5.5 Mb at 60x); HiFi panels pass their own."""
    ax.set_xscale("log"); ax.minorticks_off()
    xt = [t for t in (0.02, 0.03, 0.05, 0.1, 0.2, 0.5) if xlim[0] <= t <= xlim[1] and not (t == 0.03 and xlim[0] < 0.025)]
    ax.set_xticks(xt); ax.set_xticklabels([f"{t:g}" for t in xt]); ax.set_xlim(*xlim)
    ax.set_ylim(*ylim); ax.set_yticks(list(yticks))
    ax.set_ylabel("Block N50 (Mb)")
    ax.set_xlabel("SNV switch error rate (%)")


def _cov_ends(ax, covs, ex, ey):
    """Coverage of the first and last point of an accuracy-contiguity path."""
    for i, dy, va in ((0, -4, "top"), (-1, 4, "bottom")):
        ax.annotate(f"{covs[i]}×", (ex[i], ey[i]), xytext=(0, dy), textcoords="offset points",
                    ha="center", va=va, fontsize=5.5, color="#555555")


def _light(fig, handles=()):
    """Lighter lines and markers (Fig. 2, author decision, 2026-10-13): 0.75 pt lines,
    0.6 pt marker edges, markers at 0.8 of their size; applied to every line of the figure's
    axes and to the given key handles."""
    for h in [*(l for ax in fig.axes for l in ax.get_lines()), *handles]:
        h.set_linewidth(0.75); h.set_markeredgewidth(0.6); h.set_markersize(h.get_markersize() * 0.8)
    return list(handles)


def fig2():
    """LongPhase 2 against other phasers on sequence variants, nanopore and PacBio HiFi data (v5.0q).
    2 x 4 grid (author decision, 2026-10-20, option B: Fig. 2 for sequence variants, Fig. 3 for
    methylation; it replaces the 3 x 2 grid of 2026-10-13), one type of plot per row and one
    column per comparison: a/e nanopore SNVs (WhatsHap, HapCUT2), b/f nanopore SNVs and indels
    (WhatsHap, HapCUT2 with --indels 1, replicate 1; solid SNV pairs, dotted pairs with an indel for
    LongPhase 2 and WhatsHap, Supplementary Table 14), c/g HiFi SNVs (WhatsHap, HapCUT2, HiPhase),
    d/h HiFi SNVs and indels (the same tools on the full call sets, sheet Other_phasers; SNV pairs
    only, no indel-pair rate exists for HiFi). Row 1 switch error rate against coverage, row 2
    switch error rate against block N50 (author, 2026-10-20: not Hamming distance, which grows
    with block length; Hamming distances are Supplementary Fig. 16). TinkerHap stays in Table 18.
    HiFi panels have their own N50 axis. Title on the panel-letter line, one tool key at the top,
    lighter lines (`_light()`), no s.d. bands (author, 2026-10-12). The phased fractions are in
    Fig. 5."""
    fig, axs = plt.subplots(2, 4, figsize=(FIGW, 96 * MM), layout="constrained")
    fig.get_layout_engine().set(w_pad=2 * MM, h_pad=1.5 * MM, wspace=0.05, hspace=0.1)
    (a, b, c, d), (e, f, g, h) = axs
    snv = lambda plat, tool: (lambda c_: D["snv"][plat][XLSX_TOOL[tool]].get(c_))
    ind = lambda tool: (lambda c_: D["coph"]["Indel"][tool].get(c_))
    hc_ont = _other("ONT", "HapCUT2 1.3.4 (--indels 1)")
    hifi_snv = {"lp_gnn": snv("HiFi", "lp_gnn"), "wh": snv("HiFi", "wh"), "hc": snv("HiFi", "hc"), "hp": hiphase}
    hifi_ind = {"lp_gnn": _other("HiFi", "LongPhase 2.1.1 (--indels)"), "wh": _other("HiFi", "WhatsHap 2.8 (indels)"),
                "hc": _other("HiFi", "HapCUT2 1.3.4 (--indels 1)"), "hp": _other("HiFi", "HiPhase 1.7.0")}

    # row 1: switch error rate against coverage; LongPhase 2 drawn last, on top
    for t in ("hc", "wh", "lp_gnn"):
        tline(a, t, *_series(snv("ONT", t), PLOT_COVS)("sw_pct"), band=False)
    tline(b, "hc", *_series(hc_ont, BAR_COVS)("sw_pct"), band=False)
    for t, cfg, tool in (("wh", "whatshap_v28", "whatshap_v28"), ("lp_gnn", "longphase_coh_indel_gnn", "longphase_v2.1.2")):
        g_ = _series(_indel_runs(cfg, tool), PLOT_COVS)
        tline(b, t, *g_("snv_sw_pct"), band=False)
        line(b, *g_("indel_sw_pct"), C[t], ls=":", marker=STY[t]["marker"], ms=STY[t]["ms"], band=False,
             mfc="none")
    for ax, src in ((c, hifi_snv), (d, hifi_ind)):
        for t in ("hc", "wh", "hp", "lp_gnn"):
            tline(ax, t, *_series(src[t], HIFI_COVS)("sw_pct"), band=False)
    for ax in (a, c, d):
        _log_rate_axis(ax)
    _log_rate_axis(b, ticks=(0.02, 0.05, 0.1, 0.2, 0.5, 1), lim=(0.018, 1.4))
    cov_axis(a); cov_axis(b); cov_axis(c, HIFI_COVS); cov_axis(d, HIFI_COVS)
    c.set_xlim(7.5, 52.5); d.set_xlim(7.5, 52.5)
    a.set_ylabel("Switch error rate (%)")

    # row 2: switch error rate against block N50, one point per coverage; comparators first
    for t in ("hc", "wh", "lp_gnn"):
        ex, ey = _path(e, snv("ONT", t), PLOT_COVS, C[t], "-", STY[t]["marker"], STY[t]["ms"])
        if t == "wh":
            _cov_ends(e, PLOT_COVS, ex, ey)
    for get, covs, t in ((hc_ont, BAR_COVS, "hc"), (ind("whatshap_v28"), PLOT_COVS, "wh"),
                         (ind("longphase_v2.1.2"), PLOT_COVS, "lp_gnn")):
        _path(f, get, covs, C[t], "-", STY[t]["marker"], STY[t]["ms"])
    for ax, src in ((g, hifi_snv), (h, hifi_ind)):
        for t in ("hc", "wh", "hp", "lp_gnn"):
            ex, ey = _path(ax, src[t], HIFI_COVS, C[t], "-", STY[t]["marker"], STY[t]["ms"])
            if t == "wh":
                _cov_ends(ax, HIFI_COVS, ex, ey)
    _tradeoff_axis(e); _tradeoff_axis(f, xlim=(0.018, 0.45))
    _tradeoff_axis(g, (0, 0.85), [0, 0.2, 0.4, 0.6, 0.8], (0.025, 0.2))   # HiFi blocks are 4-7 times shorter
    _tradeoff_axis(h, (0, 0.85), [0, 0.2, 0.4, 0.6, 0.8], (0.025, 0.35))
    for ax in (f, g, h):
        ax.set_ylabel("")

    grey = "#555555"
    tools = [thandle(t, n) for t, n in (("lp_gnn", "LongPhase 2"), ("wh", "WhatsHap"), ("hc", "HapCUT2"),
                                        ("hp", "HiPhase"))]
    kb = [Line2D([], [], color=grey, ls="-", label="SNV pairs"), Line2D([], [], color=grey, ls=":", label="Pairs with an indel")]
    _light(fig, tools + kb)
    b.legend(handles=kb, loc="upper right", bbox_to_anchor=(1, 0.80), frameon=False, handlelength=2.6,
             borderaxespad=0.3, borderpad=0.0, labelspacing=0.3)
    fig.legend(handles=tools, loc="outside upper center", ncol=len(tools), frameon=False, handlelength=2.6,
               columnspacing=2.0)
    # platform first in every title (author, 2026-10-20)
    for ax, L, title in ((a, "a", "Nanopore: SNVs"), (b, "b", "Nanopore: SNVs and indels"),
                         (c, "c", "PacBio HiFi: SNVs"), (d, "d", "PacBio HiFi: SNVs and indels"),
                         (e, "e", "Nanopore: SNVs"), (f, "f", "Nanopore: SNVs and indels"),
                         (g, "g", "PacBio HiFi: SNVs"), (h, "h", "PacBio HiFi: SNVs and indels")):
        letter(ax, L, title=title)
    save(fig, os.path.join(OUT, "fig2_phaser_comparison.pdf"))


# ============================================================ Figure 3 =====
SV_TOOL = {"LongPhase 2": "lp_gnn", "WhatsHap": "wh", "HiPhase": "hp"}
SV_SIZES = (("50-999", "50 bp–1 kb"), ("1000-9999", "1–10 kb"), (">=10000", "≥10 kb"))


def sv_rows():
    """SV phasing accuracy against the T2T-HG002 Q100 v1.1 dipcall VCF (issue #10): notes/sv_phasing/
    sv_phasing.tsv when JH has delivered it, else sv_phasing_preliminary.tsv (the twolinin/longphase#136
    values: nanopore 10x and 30x, HiFi 30x, no HiPhase). Rows with the GNN (or a tool without one)."""
    d = os.path.join(ROOT, "notes", "sv_phasing")
    path = os.path.join(d, "sv_phasing.tsv")
    if not os.path.exists(path):
        path = os.path.join(d, "sv_phasing_preliminary.tsv")
    with open(path) as f:
        head = f.readline().rstrip("\n").split("\t")
        rows = [dict(zip(head, l.rstrip("\n").split("\t"))) for l in f if l.strip()]
    for r in rows:
        r["coverage"], r["right"], r["wrong"] = int(r["coverage"]), int(r["right"]), int(r["wrong"])
        r["err"] = 100 * r["wrong"] / (r["right"] + r["wrong"]) if r["right"] + r["wrong"] else float("nan")
    return [r for r in rows if r["gnn"] in ("yes", "-") and r["replicate"] == "1"]


SV_SIZE_ROWS = ((("50-999",), "50 bp–1 kb"), (("1000-9999", ">=10000"), "≥1 kb"))
SV_COVS = {"ONT": PLOT_COVS, "HiFi": HIFI_COVS}


def sv_err(sv, plat, inp, t, sizes=("50-999", "1000-9999", ">=10000")):
    """(coverage, SVs phased correctly, error rate %) per coverage over DEL + INS of the given size classes."""
    out = []
    for cov in SV_COVS[plat]:
        rs = [r for r in sv if r["platform"] == plat and r["input"] == inp and SV_TOOL[r["tool"]] == t
              and r["coverage"] == cov and r["svtype"] in ("DEL", "INS") and r["size_class"] in sizes]
        if rs:
            ri, w = sum(r["right"] for r in rs), sum(r["wrong"] for r in rs)
            out.append((cov, ri, 100 * w / (ri + w)))
    return out


def sv_tradeoff(ax, sv, plat, inp, ylim, yticks):
    """SV error rate against SVs phased correctly, one point per coverage joined from the lowest to the
    highest; coverage of the ends on WhatsHap."""
    for t in ("hp", "wh", "lp_gnn"):
        pts = sv_err(sv, plat, inp, t)
        if not pts:
            continue
        covs, xs, ys = zip(*pts)
        xs = [x / 1000 for x in xs]
        ax.plot(xs, ys, color=C[t], ls="-", marker=STY[t]["marker"], ms=STY[t]["ms"], mfc="none", mew=0.8, lw=0.9)
        if t == "wh":
            last = ((0, -4), "center", "top") if plat == "ONT" else ((4, 0), "left", "center")
            for i, off, ha, va in ((0, (-4, 0), "right", "center"), (-1, *last)):   # off the other paths
                ax.annotate(f"{covs[i]}×", (xs[i], ys[i]), xytext=off, textcoords="offset points",
                            ha=ha, va=va, fontsize=5.5, color="#555555")
    ax.margins(x=0.09)   # room for the coverage labels
    ax.set_ylim(0, ylim); ax.set_yticks(yticks); ax.set_ylabel("SV phasing error rate (%)")
    ax.set_xlabel("SVs phased correctly (thousands)")


def sv_sizes(ax, sv, inp):
    """Rows = platform x size class (1-10 kb and >=10 kb pooled: 20-47 SVs >=10 kb per run); marker =
    median over coverages, line = range over coverages (author decision, 2026-10-26, option B)."""
    y, ticks, labels = 0, [], []
    for plat, pname in (("ONT", "Nanopore"), ("HiFi", "PacBio HiFi")):
        ticks.append(y); labels.append(pname); y -= 1
        for sizes, lab in SV_SIZE_ROWS:
            tools = [t for t in ("lp_gnn", "wh", "hp") if sv_err(sv, plat, inp, t, sizes)]
            for i, t in enumerate(tools):
                e = [p_[2] for p_ in sv_err(sv, plat, inp, t, sizes)]
                yy = y + ((len(tools) - 1) / 2 - i) * 0.22   # LongPhase 2 on top
                ax.plot([min(e), max(e)], [yy, yy], color=C[t], lw=0.9, solid_capstyle="butt")
                ax.plot(st.median(e), yy, marker=STY[t]["marker"], ms=STY[t]["ms"] + 1, mfc="white", mew=0.9,
                        color=C[t], ls="none")
            ticks.append(y); labels.append(lab); y -= 1
        y -= 0.3
    ax.set_yticks(ticks, labels); ax.tick_params(axis="y", length=0)
    for tl in ax.get_yticklabels():
        if tl.get_text() in ("Nanopore", "PacBio HiFi"):
            tl.set_fontweight("bold")
    ax.set_ylim(y + 0.5, 0.6); ax.set_xlim(0, 22); ax.set_xticks([0, 5, 10, 15, 20])
    ax.set_xlabel("SV phasing error rate (%)")
    ax.grid(axis="x", color="#e6e6e6", lw=0.5); ax.set_axisbelow(True)


def fig3_sv_methylation():
    """Joint phasing beyond small variants: SVs and 5mC (author decisions, 2026-10-24: option C, one
    figure for SVs and 5mC; layout C2 after draft PNGs; 2026-10-26: SV row option B of three drafts, issue #10 data).
    2 x 3. Row 1, SVs (SNV + SV input; every tool received the same SNV and SV calls; the SNV + indel + SV
    input is Supplementary Fig. 17): a nanopore and b PacBio HiFi SV error rate against SVs phased
    correctly, one point per coverage joined from the lowest to the highest (the shared theme of Figs. 3
    and 5: fewer calls phased, a larger share of them correct); c SV error rate by platform and size
    (50 bp-1 kb, >=1 kb), median and range over coverages. Row 2, SNVs and 5mC on nanopore data (the panels of the former Fig. 3, author
    decisions of 2026-10-20 kept): d switch error rate against block N50 against MethPhaser, HapBridge
    and LongHap; e phased benchmark SNVs, markers side by side; f by evidence type, last as the
    conclusion. The Hamming panel of the former Fig. 3b is Supplementary Fig. 16e."""
    fig, axs = plt.subplots(2, 3, figsize=(FIGW, 112 * MM), layout="constrained")
    fig.get_layout_engine().set(w_pad=2 * MM, h_pad=1.5 * MM, wspace=0.06, hspace=0.1)
    (a, b, c), (d, e, f) = axs
    sv = sv_rows()
    sv_tools = [t for t in ("hp", "wh", "lp_gnn") if any(SV_TOOL[r["tool"]] == t for r in sv)]
    sv_tradeoff(a, sv, "ONT", "SNV+SV", 20, [0, 5, 10, 15, 20])   # a, b: SNVs + SVs; + indels in Supp. Fig. 17
    sv_tradeoff(b, sv, "HiFi", "SNV+SV", 12, [0, 3, 6, 9, 12])
    sv_sizes(c, sv, "SNV+SV")

    snv = lambda tool: (lambda c_: D["snv"]["ONT"][XLSX_TOOL[tool]].get(c_))
    ind = lambda tool: (lambda c_: D["coph"]["Indel"][tool].get(c_))
    all4 = lambda c_: D["coph"]["Indel+Mod+SV"]["longphase_v2.1.2"].get(c_)
    mod1 = lambda c_: [r for r in D["coph"]["Mod"]["longphase_v2.1.2"][c_] if r["rep"] == 1]
    meth = lambda c_: [{k: meth_value(c_, k) for k in ("sw_pct", "ham", "n50", "psnv_pct")}]
    tools = (("lh", meth_other("lh")), ("hb", meth_other("hb")), ("meth", meth), ("lp_gnn", mod1))
    for t, get in tools:   # d; comparators first, LongPhase 2 on top
        ex, ey = _path(d, get, BAR_COVS, C[t], "-", STY[t]["marker"], STY[t]["ms"])
        if t == "meth":
            _cov_ends(d, BAR_COVS, ex, ey)
    _tradeoff_axis(d)
    for i, (t, get) in enumerate(tools[::-1]):   # e: LongPhase 2, MethPhaser, HapBridge, LongHap from left
        st = STY[t]
        e.plot([c_ + (i - 1.5) * 1.6 for c_ in BAR_COVS], [ms(get(c_), "psnv_pct")[0] for c_ in BAR_COVS],
               ls="none", marker=st["marker"], ms=st["ms"] + 1.6, mfc="none", mew=0.9, color=C[t])
    cov_axis(e); e.set_ylim(55, 95); e.set_ylabel("Phased benchmark SNVs (%)"); e.set_xlim(5, 65)
    for get, covs, t, ls, filled in (   # f
            (ind("whatshap_v28"), PLOT_COVS, "wh", "--", False), (snv("wh"), PLOT_COVS, "wh", "-", False),
            (_other("ONT", "LongHap 0.2.0 (all variants, with 5mC)"), BAR_COVS, "lh", "-.", True),
            (all4, PLOT_COVS, "lp_gnn", "-.", True), (ind("longphase_v2.1.2"), PLOT_COVS, "lp_gnn", "--", False),
            (snv("lp_gnn"), PLOT_COVS, "lp_gnn", "-", False)):
        ex, ey = _path(f, get, covs, C[t], ls, STY[t]["marker"], STY[t]["ms"], mfc=C[t] if filled else "none")
        if t == "lh":   # 10x to the right: below it sits the 10x point of WhatsHap
            for i, off, ha, va in ((0, (5, 0), "left", "center"), (-1, (0, 4), "center", "bottom")):
                f.annotate(f"{covs[i]}×", (ex[i], ey[i]), xytext=off, textcoords="offset points",
                           ha=ha, va=va, fontsize=5.5, color="#555555")
    _tradeoff_axis(f, (0, 7.5), [0, 2, 4, 6])

    grey = "#555555"
    key = [thandle(t, n) for t, n in (("lp_gnn", "LongPhase 2"), ("wh", "WhatsHap"), ("hp", "HiPhase"),
                                      ("meth", "MethPhaser"), ("hb", "HapBridge"), ("lh", "LongHap"))
           if t not in ("hp",) or "hp" in sv_tools]
    ke = [Line2D([], [], color=grey, ls="-", label="SNVs"), Line2D([], [], color=grey, ls="--", label="+ indels"),
          Line2D([], [], color=grey, ls="-.", marker="o", ms=3.0, mfc=grey, label="+ indels, SVs and 5mC")]
    _light(fig, key + ke)
    for ax in (c, e):   # markers only (c: ranges); keep markers at full size
        for l_ in ax.get_lines():
            l_.set_markersize(l_.get_markersize() / 0.8)
    f.legend(handles=ke, loc="upper left", frameon=False, handlelength=2.6)
    fig.legend(handles=key, loc="outside upper center", ncol=len(key), frameon=False, handlelength=2.6,
               columnspacing=2.0)
    for ax, L, title in ((a, "a", "Nanopore: SV accuracy and completeness"),
                         (b, "b", "PacBio HiFi: SV accuracy and completeness"), (c, "c", "SVs by size"),
                         (d, "d", "SNVs and 5mC: accuracy and contiguity"), (e, "e", "SNVs and 5mC: phased SNVs"),
                         (f, "f", "By evidence type")):
        letter(ax, L, title=title)
    save(fig, os.path.join(OUT, "fig3_sv_methylation.pdf"))


# ============================================== Supplementary Fig. 17 =====
def sfig17_sv_indels():
    """SV phasing with SNVs, indels and SVs (issue #10), the input that Fig. 3a,b leave out (author
    decision, 2026-10-26, option B): a nanopore, b PacBio HiFi, as Fig. 3a,b."""
    sv = sv_rows()
    fig, (a, b) = new_fig(62, 1, 2)
    sv_tradeoff(a, sv, "ONT", "SNV+indel+SV", 24, [0, 5, 10, 15, 20])
    sv_tradeoff(b, sv, "HiFi", "SNV+indel+SV", 14, [0, 3, 6, 9, 12])
    key = [thandle(t, n) for t, n in (("lp_gnn", "LongPhase 2"), ("wh", "WhatsHap"), ("hp", "HiPhase"))]
    _light(fig, key)
    fig.legend(handles=key, loc="outside upper center", ncol=3, frameon=False, handlelength=2.6, columnspacing=2.0)
    letter(a, "a", title="Nanopore: SNVs, indels and SVs"); letter(b, "b", title="PacBio HiFi: SNVs, indels and SVs")
    save(fig, os.path.join(SUPP, "suppfig17_sv_indels.pdf"))


# ============================================== Supplementary Fig. 16 =====
def sfig16():
    """Block-wise Hamming distance of the Fig. 2 comparisons, against coverage (author decision,
    2026-10-13; the 5mC panels moved to Fig. 3 on 2026-10-20): a nanopore SNVs, b nanopore SNVs and
    indels (SNVs solid, indels dotted; SNV values calculated, see `_indel_runs()`; LongPhase 2 and
    WhatsHap only, because the HapCUT2 run has no separate SNV and indel values), c HiFi SNVs,
    d HiFi SNVs and indels (Hamming over SNVs and indels, sheet Other_phasers); e nanopore SNVs and
    5mC against MethPhaser, HapBridge and LongHap (the former Fig. 3b; moved here on 2026-10-24, when
    Fig. 3 became SVs and 5mC, layout C2)."""
    fig, axs = new_fig(50, 1, 5)
    snv = lambda plat, tool: (lambda c: D["snv"][plat][XLSX_TOOL[tool]].get(c))
    a, b, c_, d, e = axs
    mod1 = lambda c: [r for r in D["coph"]["Mod"]["longphase_v2.1.2"][c] if r["rep"] == 1]
    meth = lambda c: [{k: meth_value(c, k) for k in ("sw_pct", "ham", "n50", "psnv_pct")}]
    for t, get in (("lh", meth_other("lh")), ("hb", meth_other("hb")), ("meth", meth), ("lp_gnn", mod1)):
        tline(e, t, *_series(get, BAR_COVS)("ham"), band=False)
    for t in ("hc", "wh", "lp_gnn"):
        tline(a, t, *_series(snv("ONT", t), PLOT_COVS)("ham"), band=False)
    for t, cfg, tool in (("wh", "whatshap_v28", "whatshap_v28"), ("lp_gnn", "longphase_coh_indel_gnn", "longphase_v2.1.2")):
        g = _series(_indel_runs(cfg, tool), PLOT_COVS)
        tline(b, t, *g("snv_ham"), band=False)
        line(b, *g("indel_ham"), C[t], ls=":", marker=STY[t]["marker"], ms=STY[t]["ms"], band=False, mfc="none")
    hifi_ind = {"lp_gnn": _other("HiFi", "LongPhase 2.1.1 (--indels)"), "wh": _other("HiFi", "WhatsHap 2.8 (indels)"),
                "hc": _other("HiFi", "HapCUT2 1.3.4 (--indels 1)"), "hp": _other("HiFi", "HiPhase 1.7.0")}
    for t in ("hc", "wh", "hp", "lp_gnn"):
        tline(c_, t, *_series(hiphase if t == "hp" else snv("HiFi", t), HIFI_COVS)("ham"), band=False)
        tline(d, t, *_series(hifi_ind[t], HIFI_COVS)("ham"), band=False)
    for ax in axs:
        ax.set_ylim(bottom=0)
    a.set_ylabel("Hamming distance (%)")
    for ax, title, L in zip(axs, ("Nanopore:\nSNVs", "Nanopore:\nSNVs and indels", "PacBio HiFi:\nSNVs",
                                  "PacBio HiFi:\nSNVs and indels", "Nanopore:\nSNVs and 5mC"), "abcde"):   # two lines: five panels
        cov_axis(ax, HIFI_COVS if ax in (c_, d) else (10, 20, 30, 40, 50, 60))
        ax.set_title(title, fontsize=6.5)
        letter(ax, L)
    c_.set_xlim(7.5, 52.5); d.set_xlim(7.5, 52.5)
    e.set_xlim(5, 65)
    grey = "#555555"
    h = [thandle(t, NAME[t].split(" (")[0]) for t in ("lp_gnn", "wh", "hc", "hp")]
    h += [thandle(t, n) for t, n in (("meth", "MethPhaser"), ("hb", "HapBridge"), ("lh", "LongHap"))]
    h += [Line2D([], [], color=grey, ls="-", label="b: SNVs"),
          Line2D([], [], color=grey, ls=":", marker="o", ms=3.0, mfc="none", mew=0.8, label="b: indels")]
    _light(fig, h)
    fig.legend(handles=h, loc="outside upper center", ncol=len(h), handlelength=2.6, columnspacing=1.6)
    save(fig, os.path.join(SUPP, "suppfig16_fig2_coverage.pdf"))


# ============================================================ Figure 5 =====
# What each tool phases and leaves unphased (former Fig. 6 merged with the phased
# fractions of former Fig. 2d,h; author decision, 2026-10-09; Fig. 3 until the swap with the
# two-benchmark figure, author decision, 2026-10-09; Fig. 4 until the methylation figure became
# Fig. 3, author decision, 2026-10-20).
# Source: notes/unphased/ (JHL, issue #6, 2026-10-09; issue6.py and scripts/run_coverage.sh,
# which reproduce UnphaseVenn3.jsx). HG002 ONT, SNV-only, replicate 1, LongPhase 2 with GNN
# against WhatsHap --only-snvs. Universe: heterozygous SNV calls with single-base REF and ALT
# and GT 0/1, identical in both VCFs (chrX/Y included). Truth: v5.0q chr1-22, no BED.
UNPH = os.path.join(ROOT, "notes", "unphased")
VENN_COVS = (10, 30, 60)


def _unph(name):
    import csv
    return list(csv.DictReader(open(os.path.join(UNPH, name)), delimiter="\t"))


# (coverage, set) -> row; sets lp_only, lp_only_phase, lp_only_gnn, wh_only, both, background
# (= phased by both tools)
COMP = {(int(r["coverage"][:-1]), r["set"]): r for r in _unph("issue6_composition.tsv")}
INTV = {(int(r["coverage"][:-1]), r["set"]): r for r in _unph("issue6_intervals.tsv")}
CLASSES = ("het_match", "het_other_allele", "hom", "absent", "chrXY")


def comp(c, s, k="n"):
    return int(COMP[(c, s)][k])


def venn_hist():
    """Depth histograms per set, 2x bins, last bin DP >= 124 (issue6_depth_hist.tsv)."""
    out = {}
    for r in _unph("issue6_depth_hist.tsv"):
        k = {"lp_only": "lp", "wh_only": "wh", "both": "both"}.get(r["set"])
        if k:
            out.setdefault(int(r["coverage"][:-1]), {}).setdefault(k, []).append(
                (float(r["bin_start"]), float(r["fraction"])))
    return {c: {k: [f for _, f in sorted(v)] for k, v in d.items()} for c, d in out.items()}


def net_phased(c):
    """Net difference in phased calls, WhatsHap minus LongPhase 2 (= calls left unphased by
    LongPhase 2 only minus those left unphased by WhatsHap only), per benchmark class. The
    het_match difference equals the difference in Phased_SNV of longphase compare, checked here
    (issue6_reconcile.tsv)."""
    d = {k: comp(c, "lp_only", k) - comp(c, "wh_only", k) for k in ("n",) + CLASSES}
    rep1_ = lambda t: [r for r in D["snv"]["ONT"][XLSX_TOOL[t]][c] if r["rep"] == 1][0]["psnv"]
    assert d["het_match"] == rep1_("wh") - rep1_("lp_gnn")
    assert d["n"] == sum(d[k] for k in CLASSES)
    return d


def other_tool_errors(c, s):
    """The other tool's phase at the benchmark heterozygous SNVs (het_match) of a tool-only set:
    (assessed, wrongly phased = block-wise Hamming error, % wrong, that tool's genome-wide
    Hamming distance %)."""
    n, e = comp(c, s, "other_assessed"), comp(c, s, "other_hamming_err")
    other = "whatshap_v28" if s.startswith("lp") else "longphase_v2.1.2"
    gw = [r for r in D["snv"]["ONT"][other][c] if r["rep"] == 1][0]["ham"]
    return n, e, 100 * e / n, gw


ONLY = {"lp_gnn": "wh_only", "wh": "lp_only"}   # calls phased by this tool only = unphased by the other only


def phased_calls(c, t):
    """Calls phased by tool t (chr1-22): (all, benchmark het. SNVs). Phased by LongPhase 2 = phased by
    both + left unphased by WhatsHap only, and vice versa; chrX/Y excluded because the truth covers
    chr1-22. The het. count equals compare's Phased_SNV (checked)."""
    n = comp(c, "background") - comp(c, "background", "chrXY") + comp(c, ONLY[t]) - comp(c, ONLY[t], "chrXY")
    het = comp(c, "background", "het_match") + comp(c, ONLY[t], "het_match")
    assert het == [r for r in D["snv"]["ONT"][XLSX_TOOL[t]][c] if r["rep"] == 1][0]["psnv"]
    return n, het


def tint(col, f):
    """Mix a hex colour with white; f = share of white."""
    r, g, b = (int(col[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % tuple(round(v + (255 - v) * f) for v in (r, g, b))


# Issue #7 (JHL, notes/unphased/phased_calls_chr1_22.tsv, count_phased.sh): phased heterozygous
# SNV calls on chr1-22 (single-base, one ALT, GT 0|1 or 1|0) of every SNV-only run of LongPhase 2
# and WhatsHap. Precision = compare's Phased_SNV / this count; equals phased_calls() at 10/30/60x
# replicate 1 (checked).
PHASED_CALLS = {({"LongPhase 2": "lp_gnn", "WhatsHap": "wh"}[r["tool"]], int(r["coverage"]), int(r["replicate"])):
                int(r["phased_het_snv_calls_chr1_22"]) for r in _unph("phased_calls_chr1_22.tsv")}
# HiFi, replicate 1 (JHL, issue #9, 4393308): same call definition, LongPhase 2, WhatsHap and HiPhase.
PHASED_CALLS_HIFI = {({"LongPhase 2": "lp_gnn", "WhatsHap": "wh", "HiPhase": "hp"}[r["tool"]], int(r["coverage"])):
                     int(r["phased_het_snv_calls_chr1_22"]) for r in _unph("phased_calls_hifi_chr1_22.tsv")}


def precision_hifi(t):
    """Getter cov -> [{'prec': %}] for HiFi SNV-only phasing (one run per coverage): phased benchmark
    het. SNVs (SNV_Detail, or Other_phasers for HiPhase) over phased het. SNV calls on chr1-22."""
    def get(c):
        r = hiphase(c)[0] if t == "hp" else D["snv"]["HiFi"][XLSX_TOOL[t]][c][0]
        return [{"prec": 100 * r["psnv"] / PHASED_CALLS_HIFI[(t, c)]}]
    return get


def precision_runs(t):
    """Getter cov -> replicate dicts with 'prec' (%) and 'f1' (%, harmonic mean of precision and the
    phased fraction psnv_pct), for _series() and cell()."""
    def get(c):
        out = []
        for r in D["snv"]["ONT"][XLSX_TOOL[t]].get(c, []):
            n = PHASED_CALLS[(t, c, r["rep"])]
            if r["rep"] == 1 and c in VENN_COVS:
                assert n == phased_calls(c, t)[0]
            p_, r_ = r["psnv"] / n, r["psnv_pct"] / 100
            out.append({"prec": 100 * p_, "f1": 200 * p_ * r_ / (p_ + r_)})
        return out
    return get


def phased_class(c, t, k):
    """Calls phased by tool t on chr1-22 in v5.0q class k (issue6_composition.tsv): phased by both
    (background) + phased by t only. k = hom: v5.0q homozygous at the call's position, i.e. a
    heterozygous genotype error that the tool wrote onto a haplotype."""
    return comp(c, "background", k) + comp(c, ONLY[t], k)


def fig5():
    """What LongPhase 2 leaves unphased (author decisions, 2026-10-09 and 2026-10-10). Row 1, calls
    phased by LongPhase 2 and WhatsHap, and in b also HiPhase: one message -- LongPhase 2 phases about 1% fewer benchmark
    SNVs, but more of the calls it phases are benchmark SNVs, and fewer of them are genotype
    errors. Completeness and precision are paired by platform (author decision, 2026-10-19,
    option A): a completeness and b precision (nanopore; F1 in the text and Supplementary Table 8),
    c completeness and d precision (PacBio HiFi, with HiPhase, the PacBio phaser; HiFi phased-call
    counts from issue #9), e phased calls at positions where v5.0q is homozygous (genotype errors
    written onto a haplotype; GIAB v5.0q framing; nanopore only, no HiFi counts exist). Row 2, SNVs unphased
    by GNN correction (former Supplementary Fig. 16, promoted 2026-10-10 so that a main figure
    shows what the network withholds): f v5.0q status by coverage, g T2T-HG002 assembly status at
    60x against a random sample of SNVs phased before correction, h the same by chromosome.
    Row 2 is a different set from row 1: GNN correction leaves unphased only about one sixth of
    the calls that LongPhase 2 alone leaves unphased. No numbers inside panels (author,
    2026-10-09); they are in the text and Supplementary Table 12. The calls left unphased by one
    tool only, their read depth and interval co-location are in the text, Supplementary Table 17
    and Supplementary Fig. 12; the regions added by v5.0q are in Fig. 3d,e."""
    fig = plt.figure(figsize=(FIGW, 136 * MM), layout="constrained")
    fig.get_layout_engine().set(w_pad=2 * MM, h_pad=1.2 * MM, wspace=0.05, hspace=0.0)
    sf1, sf2 = fig.subfigures(2, 1, height_ratios=[62, 74], hspace=0.035)
    # ---- row 1: LongPhase 2 and WhatsHap
    # 4 x 2 grid (author decision, 2026-10-19): row 1 completeness and precision paired by platform,
    # row 2 likely errors, phased (genotype errors, both tools) or withheld (SNVs unphased by GNN)
    ax_a, ax_b, ax_h, ax_hp = sf1.subplots(1, 4)
    ax_c, ax_e, ax_f, ax_g = sf2.subplots(1, 4, width_ratios=[1, 1.15, 0.95, 0.9])
    TOOLS = (("wh", "WhatsHap"), ("lp_gnn", "LongPhase 2"))   # LongPhase 2 drawn last, on top
    snv = lambda tool, plat="ONT": (lambda c: D["snv"][plat][XLSX_TOOL[tool]].get(c))
    tline(ax_h, "hp", *_series(hiphase, HIFI_COVS)("psnv_pct"))   # HiFi panels only (author decision, 2026-10-19)
    tline(ax_hp, "hp", *_series(precision_hifi("hp"), HIFI_COVS)("prec"))
    for t, _ in TOOLS:
        tline(ax_a, t, *_series(snv(t), PLOT_COVS)("psnv_pct"))
        tline(ax_h, t, *_series(snv(t, "HiFi"), HIFI_COVS)("psnv_pct"))
        tline(ax_b, t, *_series(precision_runs(t), PLOT_COVS)("prec"))
        tline(ax_hp, t, *_series(precision_hifi(t), HIFI_COVS)("prec"))
    ax_a.set_ylim(76, 94); ax_a.set_yticks([76, 80, 84, 88, 92])
    ax_a.set_ylabel("Benchmark het. SNVs phased (%)")
    ax_a.set_title("Completeness, nanopore", loc="center", fontsize=6.5)
    ax_h.set_ylim(86, 93); ax_h.set_yticks([86, 88, 90, 92])
    ax_hp.set_ylim(89.5, 95.5); ax_hp.set_yticks([90, 92, 94])
    ax_hp.set_ylabel("Phased calls that are\nbenchmark het. SNVs (%)")
    ax_hp.set_title("Precision, PacBio HiFi", loc="center", fontsize=6.5)
    cov_axis(ax_hp, HIFI_COVS); ax_hp.set_xlim(7.5, 52.5)
    ax_h.set_ylabel("Benchmark het. SNVs phased (%)")
    ax_h.set_title("Completeness, PacBio HiFi", loc="center", fontsize=6.5)
    ax_b.set_ylim(84, 95); ax_b.set_yticks([85, 88, 91, 94])
    ax_b.set_ylabel("Phased calls that are\nbenchmark het. SNVs (%)")
    ax_b.set_title("Precision, nanopore", loc="center", fontsize=6.5)
    cov_axis(ax_a); cov_axis(ax_b); cov_axis(ax_h, HIFI_COVS)
    ax_h.set_xlim(7.5, 52.5)
    ax = ax_c   # d: grouped bars, both tools, replicate 1 at 10/30/60x
    for i, (t, _) in enumerate(reversed(TOOLS)):
        ax.bar([j + (i - 0.5) * 0.36 for j in range(3)], [phased_class(c, t, "hom") / 1000 for c in VENN_COVS],
               0.33, color=C[t], zorder=3)
    ax.set_xticks(range(3)); ax.set_xticklabels([f"{c}×" for c in VENN_COVS])
    ax.set_xlim(-0.6, 2.6); ax.set_ylim(0, 30); ax.set_yticks([0, 10, 20, 30])
    ax.set_xlabel("Coverage"); ax.set_ylabel("Phased het. calls at v5.0q\nhomozygous sites (thousands)")
    ax.set_title("Genotype errors, nanopore", loc="center", fontsize=6.5)
    # ---- row 2: SNVs unphased by GNN correction (LongPhase 2 only)
    T = t2t()
    GREYS = ("#D9D9D9", "#969696", "#4D4D4D")   # light = cannot be verified, dark = verified
    KEYPAD = 12   # points: titles of e-g sit above the one-line keys of e and f
    ax = ax_e
    xs = range(len(COVS)); bottom = [0] * len(COVS)
    for i, lab in enumerate(("absent", "homozygous", "heterozygous")):   # COMPOSITION order
        v = [100 * COMPOSITION[c][i] / sum(COMPOSITION[c]) for c in COVS]
        ax.bar(xs, v, 0.72, bottom=bottom, color=GREYS[i], label=lab, zorder=3)
        bottom = [x + y for x, y in zip(bottom, v)]
    ax.set_xticks(list(xs)); ax.set_xticklabels([str(c) for c in COVS])
    ax.set_xlabel("Coverage (×)"); ax.set_ylabel("SNVs unphased by GNN (%)")
    ax.set_ylim(0, 100); ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_title("Status in the v5.0q benchmark", loc="center", fontsize=6.5, pad=KEYPAD)
    h, l = ax.get_legend_handles_labels()
    ax.legend(h[::-1], l[::-1], loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=5.5,
              handlelength=1.0, columnspacing=1.0, borderaxespad=0.2)
    ax = ax_f
    n = T["rm_n"]; out_rm = 100 * T["cls"]["unassessed"] / n
    out_bg = 100 * (1 - T["bg_in"] / T["bg_n"])
    for y, out in ((1, out_bg), (0, out_rm)):
        ax.barh(y, 100 - out, 0.55, color=GREYS[2], zorder=3)
        ax.barh(y, out, 0.55, left=100 - out, color=GREYS[0], zorder=3)
    ax.set_yticks([0, 1]); ax.set_yticklabels(["Unphased\nby GNN", "Phased\n(random\nsample)"])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 100); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel("SNVs at 60× (%)")
    ax.set_title("T2T-HG002 assembly", loc="center", fontsize=6.5, pad=KEYPAD)
    ax.legend(handles=[Patch(color=GREYS[2], label="aligned 1:1"), Patch(color=GREYS[0], label="not aligned 1:1")],
              loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=5.5, handlelength=1.0,
              columnspacing=1.0, borderaxespad=0.2)
    ax = ax_g
    order = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
    ch = sorted(T["chroms"], key=lambda d: order.index(d["chrom"]))
    ys = range(len(ch))
    for y, d in zip(ys, ch):
        ax.plot([100 * d["bg_rate"], 100 * d["rm_rate"]], [y, y], color="#BDBDBD", lw=0.6, zorder=2)
    ax.plot([100 * d["bg_rate"] for d in ch], ys, "o", color="#4D4D4D", ms=2.2, zorder=3)
    ax.plot([100 * d["rm_rate"] for d in ch], ys, "o", color=C["lp_gnn"], ms=2.2, zorder=3)
    ax.set_yticks(list(ys)); ax.set_yticklabels([d["chrom"].replace("chr", "") for d in ch], fontsize=5)
    ax.tick_params(axis="y", length=1.5, pad=1)
    ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Not aligned 1:1 (%)"); ax.set_ylabel("Chromosome")
    ax.set_title("By chromosome, 60×", loc="center", fontsize=6.5, pad=KEYPAD)
    for ax, L in zip((ax_a, ax_b, ax_h, ax_hp, ax_c, ax_e, ax_f, ax_g), "abcdefgh"):
        letter(ax, L)
    for ax in (ax_c, ax_e, ax_f, ax_g):   # letter() resets the title pad of every title of the axes
        ax.set_title(ax.get_title(loc="center"), loc="center", fontsize=6.5, pad=KEYPAD)
    # no row titles (author, 2026-10-19); an empty title keeps the line on which _row_keys() places each key
    _row_header(sf1, " ")
    _row_header(sf2, " ")
    dot = lambda col, lab: Line2D([], [], color=col, ls="none", marker="o", ms=2.6, label=lab)
    _row_keys(fig, (sf1, sf2), ([thandle(t, n_) for t, n_ in reversed(TOOLS)] + [thandle("hp")],
                                [Patch(color=C["lp_gnn"], label="LongPhase 2"), Patch(color=C["wh"], label="WhatsHap"),
                                 dot("#4D4D4D", "phased (random sample)"), dot(C["lp_gnn"], "unphased by GNN")]))
    save(fig, os.path.join(OUT, "fig5_phased_unphased.pdf"))


# ============================================================ Figure 4 =====
# The two benchmarks (Fig. 3 until 2026-10-20, when the methylation figure became Fig. 3).
F3 = [  # key, label, colour, line style, marker, v5.0q source, v4.2.1 tool name (Supplementary Table 9)
    ("lp_gnn", "LongPhase 2, SNVs", C["lp_gnn"], "-", "o", ("snv", "longphase_v2.1.2"), "longphase_gnn"),
    ("lp_ind", "LongPhase 2, +indels", C["lp_gnn"], "--", "s", ("coph", "Indel", "longphase_v2.1.2"), "longphase_coh_indel_gnn"),
    ("lp_isv", "LongPhase 2, +indels+SVs", C["lp_gnn"], ":", "^", ("coph", "Indel+SV", "longphase_v2.1.2"), "longphase_coh_indel_sv_gnn"),
    ("wh", "WhatsHap, SNVs only", C["wh"], "-", "o", ("snv", "whatshap_v28"), "whatshap_v28_onlySNVs"),
    ("wh_ind", "WhatsHap, SNVs + indels", C["wh"], "--", "s", ("coph", "Indel", "whatshap_v28"), "whatshap_v28"),
    ("hc", "HapCUT2", C["hc"], "-", "o", ("snv", "hapcut2_v134"), "hapcut2_v134"),
]


def f3_runs(src, cov):
    if src[0] == "snv":
        return D["snv"]["ONT"][src[1]][cov]
    return D["coph"][src[1]][src[2]][cov]


REGIONS = [  # (region, stratum) in item4_strata.tsv, label, y, indent; truth v5.0q. The v5.0q
    # benchmark regions first, then (indented) subsets of them: two GIAB v3.6 strata and the parts
    # that v4.2.1 also covers or that v5.0q adds; the outside-both row, where the truth phase is
    # least certain, is set apart below a dashed line and called exploratory in the legend.
    (("v5bed", "any"), "v5.0q benchmark regions", 0, 0),
    (("v5bed", "not_difficult"), "Outside difficult regions", 1, 1),
    (("v5bed", "segdup"), "Segmental duplications", 2, 1),
    (("shared", "any"), "Shared with v4.2.1", 3, 1),
    (("v5only", "any"), "Added in v5.0q", 4, 1),
    (("neither", "any"), "Outside both benchmarks", 5.4, 0),
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
        if y == 0:
            ax.text(shared / 2000, y, "shared by all three tools", va="center", ha="center", fontsize=5.5,
                    color="#252525")
    ax.set_yticks(ys); ax.set_yticklabels(["LongPhase 2", "WhatsHap", "HapCUT2"] * 2)
    ax.invert_yaxis(); ax.tick_params(axis="y", length=0)
    for y0, lab in ((-0.8, "GIAB v4.2.1"), (2.8, "T2T-HG002-derived v5.0q")):
        ax.text(0.03, y0, lab, fontsize=6, va="center", ha="left", fontweight="bold")
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, 2.75); ax.set_xlabel("Switch errors at 60× (thousands)")
    letter(ax, "c")
    S = _group(_tsv("item4_strata.tsv"),
               lambda r: (r["tool"], int(r["coverage"]), r["truth"], r["region"], r["stratum"]))
    tools = (("lp_gnn", "longphase_gnn"), ("wh", "whatshap_v28_onlySNVs"), ("hc", "hapcut2_v134"))
    axs2 = bottom.subplots(1, 2, sharey=True)
    for ax, cov, L, xl in ((axs2[0], 10, "d", (0.02, 8)), (axs2[1], 60, "e", (0.0008, 5))):
        for key, _lab, y, _ind in REGIONS:
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
        ax.axhline(4.7, color="#BDBDBD", lw=0.5, ls="--", zorder=0)
        letter(ax, L)
    axs2[0].set_yticks([y for _, _, y, _ in REGIONS])
    axs2[0].set_yticklabels(["\u2002" * 2 * ind + lab for _, lab, _, ind in REGIONS])
    axs2[0].invert_yaxis(); axs2[0].tick_params(axis="y", length=0)
    fig.canvas.draw()   # left-align the row labels (subsets indented): pad = widest label
    r = fig.canvas.get_renderer()
    w = max(t.get_window_extent(r).width for t in axs2[0].get_yticklabels()) * 72 / fig.dpi
    for t in axs2[0].get_yticklabels():
        t.set_ha("left")
    axs2[0].tick_params(axis="y", pad=w + 3)
    axs2[1].tick_params(axis="y", length=0)
    h = [thandle(t, {"wh": "WhatsHap"}.get(t)) for t in ("lp_gnn", "wh", "hc")]
    top.legend(handles=h, loc="outside upper center", ncol=3, handlelength=2.6, columnspacing=1.6)
    save(fig, os.path.join(OUT, "fig4_two_benchmarks.pdf"))


# ======================= Fig. 4f-h (former Supplementary Fig. 16) and Table 12 data =====
# Source: unphased_grid.tsv of analyze_unphased.py + reclassify_unphased.py on the v2.1.1 runs
# (/ssd/longphase_process/unphased_grid_v2.1.1/run.sh, 2026-10-16; v2.1 values: gnn_prepare/unphased_e6/).
# SNV-only, seed 1; SNVs phased by LongPhase 2 and unphased after correction, matched to the v5.0q
# benchmark VCF by position (no benchmark BED).
COMPOSITION = {  # cov: (absent, hom-alt, het)
    10: (51585, 3120, 6684), 12: (53670, 2968, 5630), 14: (54735, 2689, 4949),
    16: (56749, 2516, 4482), 18: (56632, 2343, 3908), 20: (58602, 2371, 3228),
    30: (58507, 2166, 2938), 40: (57957, 1966, 2536), 50: (57411, 2081, 2396),
    60: (58222, 1852, 2156),
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


# ============================================== Supplementary Fig. 9 =====
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
    log_ticks(axs[0], (0.05, 0.1, 0.2))
    log_ticks(axs[1], (0.5, 1, 2, 5))
    h = [thandle(t, {"wh": "WhatsHap"}.get(t)) for t in ("lp_gnn", "wh", "hc", "margin", "ralphi")]
    fig.legend(handles=h, loc="outside upper center", ncol=5, handlelength=2.6, columnspacing=1.6)
    save(fig, os.path.join(SUPP, "suppfig10_more_tools.pdf"))


def _runtime(name="runtime.tsv"):
    """notes/runtime/runtime.tsv (issue #8): (tool, threads, coverage) -> (wall min, CPU min,
    peak RSS GiB). Replicate 1, GNU time of the paper runs; LongPhase 2 on one thread timed at
    10x and 60x only; HapCUT2 at 30x and 40x re-timed (original logs overwritten).
    runtime_hifi.tsv: the same for PacBio HiFi 10-50x (2026-10-17; see build_runtime.py)."""
    import csv
    rows = csv.DictReader(open(os.path.join(ROOT, "notes", "runtime", name)), delimiter="\t")
    return {(r["tool"], r["threads"], int(r["coverage"])):
            (int(r["wall_s"]) / 60, int(r["cpu_s"]) / 60, int(r["max_rss_kb"]) / 1024 ** 2) for r in rows}


# ============================================== Supplementary Fig. 10 =====
def sfig_runtime():
    """Runtime and peak memory of SNV-only phasing across coverage (issue #8). LongPhase 2 on one
    thread has points only."""
    rt = _runtime()
    fig, axs = new_fig(52, 1, 3)
    tools = (("hc", ("HapCUT2 1.3.4", "1")), ("wh", ("WhatsHap 2.8", "1")), ("lp_gnn", ("LongPhase 2", "24")))
    for ax, lab, j, L in zip(axs, ("Wall-clock time (min)", "CPU time (min)", "Peak memory (GiB)"), range(3), "abc"):
        for t, key in tools:
            st_ = STY[t]
            ax.plot(COVS, [rt[key + (c,)][j] if key + (c,) in rt else float("nan") for c in COVS], color=C[t],
                    ls=st_["ls"], marker=st_["marker"], ms=st_["ms"], mfc=st_["mfc"], mew=0.8)
        xs = [c for c in COVS if ("LongPhase 2", "1", c) in rt]
        ax.plot(xs, [rt[("LongPhase 2", "1", c)][j] for c in xs], ls="none", color=C["lp_gnn"], marker="o",
                ms=3.0, mew=0.8)
        ax.set_ylim(bottom=0); ax.set_ylabel(lab); cov_axis(ax); letter(ax, L)
    h = [thandle("lp_gnn", "LongPhase 2, 24 threads"),
         Line2D([], [], color=C["lp_gnn"], ls="none", marker="o", ms=3.4, label="LongPhase 2, 1 thread"),
         thandle("wh", "WhatsHap"), thandle("hc", "HapCUT2")]
    fig.legend(handles=h, loc="outside upper center", ncol=4, handlelength=2.6, columnspacing=1.6)
    save(fig, os.path.join(SUPP, "suppfig_runtime.pdf"))


# ============================================== Supplementary Fig. 13 =====
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
                ms=2.6, mfc=mfc, label="nanopore, genome-wide" if plat == "ONT" else "PacBio HiFi, genome-wide")
    Hh = _heldout("heldout_v50q.txt")   # issue #2: chromosomes held out from GNN training
    ax.plot(PLOT_COVS, [100 * (1 - ms(Hh["longphase_gnn"][c], "sw")[0] / ms(Hh["longphase"][c], "sw")[0])
                        for c in PLOT_COVS], color="#7F7F7F", ls=":", marker="s", ms=2.6, mfc="white",
            label="nanopore, chr17, chr21, chr22")
    ax.set_ylim(0, 52); ax.set_yticks([0, 10, 20, 30, 40]); ax.set_ylabel("Switch errors removed\nby GNN correction (%)")
    cov_axis(ax); letter(ax, "e"); ax.legend(loc="upper right", fontsize=5.5, borderaxespad=0.2)
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


# ============================================== Supplementary Fig. 14 =====
def sfig12():
    """Co-phasing configurations with and without GNN correction (former main Fig. 4)."""
    fig, axs = new_fig(118, 2, 2)
    for ax, cov, L in ((axs[0, 0], 10, "a"), (axs[0, 1], 60, "b")):
        for cfg, name, col in CFG:
            pts = []
            for tool in ("longphase_v2.0.1", "longphase_v2.1.2"):
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
            for tool, ls, mfc in (("longphase_v2.0.1", "--", "white"), ("longphase_v2.1.2", "-", None)):
                xs, m, s_ = coph_series(cfg, tool, key)
                line(ax, xs, m, s_, col, ls=ls, mfc=mfc)
        if key == "sw_pct":
            ax.set_yscale("log")
            ax.set_yticks([0.02, 0.05, 0.1, 0.15]); ax.set_yticklabels(["0.02", "0.05", "0.1", "0.15"])
            ax.minorticks_off()
        ax.set_ylabel(lab); cov_axis(ax); letter(ax, L)
    axs[1, 1].set_ylim(bottom=0)
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


# ============================================== Supplementary Fig. 15 =====
def sfig13():
    """All co-phasing configurations across coverage, without and with GNN correction."""
    fig, axs = new_fig(96, 2, 4)
    specs = [("sw_pct", "SNV switch error rate (%)", 1), ("ham", "Hamming distance (%)", 1),
             ("n50", "Block N50 (Mb)", 1e-6), ("psnv_pct", "Phased SNVs (%)", 1)]
    for row, tool, tag in ((0, "longphase_v2.0.1", "without GNN correction"), (1, "longphase_v2.1.2", "with GNN correction")):
        for col, (key, lab, sc) in enumerate(specs):
            ax = axs[row, col]; single_band(ax)
            for cfg, name, c in CFG:
                xs, m, s_ = coph_series(cfg, tool, key)
                line(ax, xs, m, s_, c, scale=sc, label=name, marker=CFGM[cfg], mfc="none", ms=2.6)
            ax.set_ylabel(f"{tag[0].upper() + tag[1:]}\n{lab}" if col == 0 else lab); cov_axis(ax)
            letter(ax, "abcdefgh"[row * 4 + col])
    for col in range(4):
        lo = min(axs[0, col].get_ylim()[0], axs[1, col].get_ylim()[0])
        hi = max(axs[0, col].get_ylim()[1], axs[1, col].get_ylim()[1])
        if col == 1:
            lo = 0   # Hamming distance from zero
        axs[0, col].set_ylim(lo, hi); axs[1, col].set_ylim(lo, hi)
    h = [Line2D([], [], color=c, marker=CFGM[k], mfc="none", mew=0.8, ms=3.0, label=name) for k, name, c in CFG]
    fig.legend(handles=h, loc="outside upper center", ncol=7, columnspacing=1.4)
    save(fig, os.path.join(SUPP, "suppfig15_cophasing_all.pdf"))


# ============================================== Supplementary Fig. 11 =====
def sfig14():
    """MethPhaser vs joint SNV+5mC co-phasing (replicate 1)."""
    fig, axs = new_fig(56, 1, 4)
    specs = [("sw", "Switch errors", 1), ("psnv_pct", "Phased SNVs (%)", 1),
             ("ham", "Hamming distance (%)", 1), ("n50", "Block N50 (Mb)", 1e-6)]
    covs = BAR_COVS
    for ax, (key, lab, sc), L in zip(axs, specs, "abcd"):
        ax.plot(covs, [rep1("Mod", "longphase_v2.1.2", c, key) * sc for c in covs], color=C["lp_gnn"],
                marker="o", ms=3.0, mfc="none", mew=0.8, label="LongPhase 2, SNVs + 5mC")
        ax.plot(covs, [rep1("Mod", "longphase_v2.0.1", c, key) * sc for c in covs], color=C["lp_gnn"],
                ls="--", marker="o", ms=3.0, mfc="none", mew=0.8, label="LongPhase 2, SNVs + 5mC, without GNN")
        ax.plot(covs, [meth_value(c, key) * sc for c in covs], color=C["meth"], marker="^", ms=3.4, mfc="none", mew=0.8,
                label="MethPhaser on LongPhase 2 SNV phasing without GNN")
        ax.set_ylabel(lab); cov_axis(ax); letter(ax, L)
    axs[1].set_ylim(76, 94)
    fig.legend(*axs[0].get_legend_handles_labels(), loc="outside upper center", ncol=3, handlelength=2.6,
               columnspacing=1.6)
    save(fig, os.path.join(SUPP, "suppfig11_methphaser.pdf"))


# ============================================== Supplementary Fig. 12 =====
def sfig17():
    """Read depth of the calls left unphased by one tool only and by both, 10/30/60x; sets named
    and coloured by the tool that left them unphased, as in Supplementary Table 17."""
    H = venn_hist()
    fig, axs = new_fig(50, 1, 3)
    for ax, cov, L in zip(axs, (10, 30, 60), "abc"):
        for k, col, lab in (("both", "#969696", "Left unphased by both"), ("wh", C["wh"], "Left unphased by WhatsHap only"),
                            ("lp", C["lp_gnn"], "Left unphased by LongPhase 2 only")):
            ax.plot([2 * i for i in range(len(H[cov][k]))], H[cov][k], color=col, lw=0.8, label=lab)
        ax.set_title(f"{cov}×", fontsize=6.5); ax.set_xlabel("Read depth (×)")
        ax.set_ylabel("Fraction of sites"); ax.set_xlim(0, 130)
        ax.axvspan(123, 130, color="#EEEEEE", lw=0, zorder=0)
        ax.text(127.8, ax.get_ylim()[1] * 0.5, "≥ cap (censored)", ha="center", va="center", fontsize=5,
                color="#555555", rotation=90)
        letter(ax, L)
    h = [Line2D([], [], color=c, label=l) for c, l in ((C["lp_gnn"], "Left unphased by LongPhase 2 only"),
                                                     (C["wh"], "Left unphased by WhatsHap only"),
                                                     ("#969696", "Left unphased by both"))]
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
    w(r"\caption{\textbf{SNV-only phasing on the chromosomes held out from GNN training (chr17, chr21 and chr22).} HG002 nanopore R10.4.1 data; the phased VCFs of the genome-wide analysis scored with \code{longphase compare --regions=chr17,chr21,chr22} against each truth VCF in full. Switch errors of \toolname as mean (s.d.); switch error rates in \%. \emph{Removed}, switch errors removed by GNN correction relative to \toolname without it; \emph{cost}, phased SNVs withheld per removed switch error (the deployment threshold was set on chr15 and chr16 to a cost of 6.35; Supplementary Method~4). Means over ten replicates at 10--20$\times$; one replicate at 30--60$\times$. Margin and Ralphi were run at 10--20$\times$ only.}\label{tab:heldout}\\")
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


# ------------------------------------------- issue #3 table (Table 16) ---
def runtime_table(w):
    """Runtime and peak memory of SNV-only phasing at every coverage (notes/runtime/runtime.tsv)."""
    from decimal import Decimal, ROUND_HALF_UP
    r1 = lambda x: str(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
    rt = _runtime()
    w(r"\begin{table}[h]")
    w(r"\caption{\textbf{Runtime and peak memory of SNV-only phasing.} HG002 nanopore R10.4.1 data (top) and PacBio HiFi data (bottom), replicate~1 at every coverage, on the workstation described in Methods (Supplementary Fig.~10). Wall-clock time and CPU time (user plus system) in minutes and peak resident memory in GiB, from \code{/usr/bin/time}. \toolname includes GNN correction, which runs within the \code{phase} command. \toolname was timed on one thread at 10 and 60$\times$ only (--, no value); \hapcut at 30 and 40$\times$ was re-timed (Methods). On HiFi data, \whatshap at 10 and 20$\times$ was re-timed with the alignment file already in the page cache (Methods). \hapcut includes fragment extraction.}\label{tab:runtime}")
    w(r"\small\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}rrrrrrrrrrrrr@{}}\toprule")
    groups = [(("LongPhase 2", "24"), r"\toolname, 24 threads"), (("LongPhase 2", "1"), r"\toolname, 1 thread"),
              (("WhatsHap 2.8", "1"), r"\whatshap"), (("HapCUT2 1.3.4", "1"), r"\hapcut")]
    w(" & " + " & ".join(rf"\multicolumn{{3}}{{c}}{{{n}}}" for _, n in groups) + r" \\ "
      + "".join(rf"\cmidrule({'lr' if i < 3 else 'l'}){{{2 + 3 * i}-{4 + 3 * i}}}" for i in range(4)))
    w("Coverage & " + " & ".join(["Wall & CPU & Memory"] * 4) + r" \\ \midrule")
    for blk, (rt, covs) in enumerate(((rt, COVS), (_runtime("runtime_hifi.tsv"), HIFI_COVS))):
        w(rf"\multicolumn{{13}}{{@{{}}l}}{{\textit{{{('Nanopore R10.4.1', 'PacBio HiFi')[blk]}}}}} \\")
        for c in covs:
            cells = []
            for key, _ in groups:
                v = rt.get(key + (c,))
                cells += [r1(x) for x in v] if v else ["--"] * 3
            w(rf"{c}$\times$ & " + " & ".join(cells) + r" \\")
        if blk == 0:
            w(r"\midrule")
    w(r"\bottomrule\end{tabular}\end{table}")


# ------------------------------------------- further phasers (Table 18) ---
# Sheet Other_phasers of Supplementary Data 1 (JHL, 2026-10-17/18; notes/competitors/README.md):
# replicate 1, ONT 10-60x in steps of 10x, HiFi 10-50x. LongPhase 2, WhatsHap and HapCUT2 rows of
# the same comparisons come from SNV_Detail, co-phase_Detail and the MethPhaser sheet.
OTHER_COVS = {"ONT": [10, 20, 30, 40, 50, 60], "HiFi": HIFI_COVS}


_OTHER = {}


def _other_phasers():
    """(platform, tool label in the sheet, coverage) -> metrics of one Other_phasers row."""
    if _OTHER:
        return _OTHER
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(ROOT, "supplementary.xlsx"), read_only=True)["Other_phasers"]
    out = {}
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if r[0] is None:
            continue
        plat = "ONT" if r[1].startswith("ONT") else "HiFi"
        out[(plat, r[3], int(r[4].split("x")[0]))] = dict(
            psnv=r[5], psnv_pct=r[6], pindel_pct=r[8], sw=r[9], sw_pct=r[10], ham=r[11], nblock=r[12], n50=r[13])
    _OTHER.update(out)
    return _OTHER


def sv_table():
    """Supplementary Table 20: SV phasing against the T2T-HG002 assembly (issue #10, notes/sv_phasing/),
    LongPhase 2 as released (no with/without-GNN split: author, 2026-10-26), WhatsHap and HiPhase.
    Written to its own file, input after Supplementary Table 19 so that no table is renumbered."""
    sv = sv_rows()
    L = []
    w = L.append
    w(r"{\scriptsize\setlength{\tabcolsep}{3.5pt}")
    w(r"\begin{longtable}{@{}rlrrrrrrrrrr@{}}")
    w(r"\caption{\textbf{SV phasing compared with other phasers.} HG002, replicate~1; nanopore R10.4.1 data at 10--60$\times$ and PacBio HiFi data at 10--50$\times$. Heterozygous deletions and insertions of at least 50~bp called by Sniffles2 on chr1--22, the same records for every tool, scored against the T2T-HG002 assembly (Methods). Given, heterozygous deletions and insertions in the input; phased, those phased; right and wrong, phased SVs that match an assembly SV with the correct and the wrong phase; error, wrong/(right + wrong); hom., phased SVs that match an SV homozygous in the assembly; no match, phased SVs with no matching assembly SV; DEL $\ge$10~kb, deletions of at least 10~kb phased right/wrong. Phased SVs whose block has no SNV in the assembly are not listed. Source: \code{notes/sv\_phasing/sv\_phasing.tsv}.}\label{tab:sv}\\")
    head = (r"\toprule Cov. & Tool & Given & Phased & Right & Wrong & \shortstack[r]{Error\\(\%)} & Hom. & \shortstack[r]{No\\match} & "
            r"\shortstack[r]{Error, 50~bp--1~kb\\(\%)} & \shortstack[r]{Error, $\ge$1~kb\\(\%)} & \shortstack[r]{DEL $\ge$10~kb\\right/wrong} \\ \midrule")
    w(head + r"\endfirsthead")
    w(head + r"\endhead")
    names = {"lp_gnn": r"\toolname", "wh": r"\whatshap", "hp": "HiPhase"}
    blocks = (("ONT", "SNV+SV", "Nanopore R10.4.1, SNVs and SVs"), ("ONT", "SNV+indel+SV", "Nanopore R10.4.1, SNVs, indels and SVs"),
              ("HiFi", "SNV+SV", "PacBio HiFi, SNVs and SVs"), ("HiFi", "SNV+indel+SV", "PacBio HiFi, SNVs, indels and SVs"))
    one = lambda plat, inp, t, cov, typ, size: next(r for r in sv if r["platform"] == plat and r["input"] == inp
                                                    and SV_TOOL[r["tool"]] == t and r["coverage"] == cov
                                                    and r["svtype"] == typ and r["size_class"] == size)
    for plat, inp, title in blocks:
        w(r"\multicolumn{12}{@{}l}{\textit{" + title + r"}} \\")
        for cov in SV_COVS[plat]:
            for i, t in enumerate(t for t in ("lp_gnn", "wh", "hp") if sv_err(sv, plat, inp, t)):
                r = one(plat, inp, t, cov, "all", "all")
                d = one(plat, inp, t, cov, "DEL", ">=10000")
                small = sv_err(sv, plat, inp, t, ("50-999",))
                large = sv_err(sv, plat, inp, t, ("1000-9999", ">=10000"))
                es = next(p_[2] for p_ in small if p_[0] == cov); el = next(p_[2] for p_ in large if p_[0] == cov)
                cl = f"{cov}$\\times$" if i == 0 else ""
                w(f"{cl} & {names[t]} & {int(r['sv_input']):,} & {int(r['sv_phased']):,} & "
                  f"{r['right']:,} & {r['wrong']:,} & {r['err']:.1f} & {int(r['phased_hom_in_truth']):,} & "
                  f"{int(r['phased_no_truth_match']):,} & {es:.1f} & {el:.1f} & {d['right']}/{d['wrong']} \\\\")
        w(r"\midrule")
    L[-1] = r"\bottomrule"
    w(r"\end{longtable}}")
    path = os.path.join(ROOT, "figures-source", "supp_table_sv.tex")
    open(path, "w").write("\n".join(L) + "\n")
    print("wrote", os.path.relpath(path, ROOT))


def other_phasers_table(w):
    """Every tool of the five further-phaser comparisons, with LongPhase 2 on the same input."""
    O = _other_phasers()
    rep = lambda runs: [x for x in runs if x["rep"] == 1][0]
    lp_snv = lambda p: lambda c: rep(D["snv"][p][XLSX_TOOL["lp_gnn"]][c]) if p == "ONT" else D["snv"][p][XLSX_TOOL["lp_gnn"]][c][0]
    snv = lambda p, t: lambda c: D["snv"][p][t][c][0]
    coph = lambda cfg, t: lambda c: rep(D["coph"][cfg][t][c])
    oth = lambda p, t: lambda c: O[(p, t, c)]
    blocks = [
        ("Nanopore R10.4.1, SNVs and 5mC", "ONT", [
            (r"\toolname", coph("Mod", "longphase_v2.1.2")),
            ("MethPhaser", lambda c: D["meth"][c]),
            ("HapBridge", oth("ONT", "HapBridge ec48f02 (on LongPhase 2 SNV output, no GNN)")),
            ("LongHap", oth("ONT", "LongHap 0.2.0 (SNVs, with 5mC)")),
            ("LongHap, without 5mC", oth("ONT", "LongHap 0.2.0 (SNVs, sequence only)"))]),
        ("Nanopore R10.4.1, SNVs and indels", "ONT", [
            (r"\toolname", coph("Indel", "longphase_v2.1.2")),
            (r"\whatshap", coph("Indel", "whatshap_v28")),
            (r"\hapcut", oth("ONT", "HapCUT2 1.3.4 (--indels 1)")),
            ("TinkerHap", oth("ONT", "TinkerHap 1.0.0"))]),
        ("Nanopore R10.4.1, SNVs, indels, SVs and 5mC", "ONT", [
            (r"\toolname", coph("Indel+Mod+SV", "longphase_v2.1.2")),
            ("LongHap", oth("ONT", "LongHap 0.2.0 (all variants, with 5mC)"))]),
        ("PacBio HiFi, SNVs", "HiFi", [
            (r"\toolname", lp_snv("HiFi")),
            (r"\whatshap", snv("HiFi", "whatshap_v28")),
            (r"\hapcut", snv("HiFi", "hapcut2_v134")),
            ("HiPhase", oth("HiFi", "HiPhase 1.7.0 (SNV-only input VCF)")),
            ("TinkerHap", oth("HiFi", "TinkerHap 1.0.0 (SNV-only input VCF)"))]),
        ("PacBio HiFi, SNVs and indels", "HiFi", [
            (r"\toolname", oth("HiFi", "LongPhase 2.1.1 (--indels)")),
            (r"\whatshap", oth("HiFi", "WhatsHap 2.8 (indels)")),
            (r"\hapcut", oth("HiFi", "HapCUT2 1.3.4 (--indels 1)")),
            ("HiPhase", oth("HiFi", "HiPhase 1.7.0")),
            ("TinkerHap", oth("HiFi", "TinkerHap 1.0.0"))]),
    ]
    w(r"\clearpage")   # flush Tables 12-17 (floats) so that the longtable follows them
    w(r"{\scriptsize\setlength{\tabcolsep}{4pt}")
    w(r"\begin{longtable}{@{}lrrrrrrr@{}}")
    w(r"\caption{\textbf{Phasing compared with further phasers.} HG002, replicate~1; nanopore R10.4.1 data at 10--60$\times$ in steps of 10$\times$ and PacBio HiFi data at 10--50$\times$. Each block compares tools given the same reads, variant calls and evidence classes; within a block, \toolname is listed first. MethPhaser and HapBridge were given the SNV-only output of \toolname without GNN correction. HiPhase and TinkerHap have no SNV-only mode, so their SNV-only rows used call sets restricted to SNVs. LongHap with indels, SVs and 5mC was given deletions and insertions from Sniffles2 as sequence-resolved records. Switch error rates are over consecutive SNV pairs; Hamming distance includes indels where both files contain them, so it is comparable only within a block. Phased fractions are percentages of benchmark heterozygous SNVs or indels; --, not applicable. Source: Supplementary Data~1, sheets \code{Other\_phasers}, \code{SNV\_Detail}, \code{co-phase\_Detail} and \code{MethPhaser}.}\label{tab:otherphasers}\\")
    head = (r"\toprule Tool & Cov. & \shortstack[r]{Phased\\SNVs (\%)} & \shortstack[r]{Phased\\indels (\%)} & "
            r"\shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Rate relative\\to \toolname} & \shortstack[r]{Hamming\\(\%)} & \shortstack[r]{N50\\(Mb)} \\ \midrule")
    w(head + r"\endfirsthead")
    w(head + r"\endhead")
    for bi, (title, plat, tools) in enumerate(blocks):
        w(rf"\multicolumn{{8}}{{@{{}}l}}{{\textit{{{title}}}}} \\")
        base = tools[0][1]
        for ti, (name, get) in enumerate(tools):
            for c in OTHER_COVS[plat]:
                r = get(c)
                ind = r.get("pindel_pct")
                rel = "--" if ti == 0 else f"{r['sw_pct'] / base(c)['sw_pct']:.2f}"
                w(f"{name if c == OTHER_COVS[plat][0] else ''} & {c}$\\times$ & {r['psnv_pct']:.2f} & "
                  f"{'--' if not ind else f'{ind:.2f}'} & {r['sw_pct']:.3f} & {rel} & {r['ham']:.2f} & {r['n50'] / 1e6:.2f} \\\\")
        if bi < len(blocks) - 1:
            w(r"\midrule")
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


def rate_ratio(t, c):
    """Switch error rate of tool t over that of LongPhase 2 (GNN correction) in the same
    down-sampling replicate; mean (s.d.) over the paired replicates at 10--20x."""
    if t == "lp_gnn":
        return "--"
    lp = {r["rep"]: r["sw_pct"] for r in D["snv"]["ONT"][XLSX_TOOL["lp_gnn"]][c]}
    xs = [r["sw_pct"] / lp[r["rep"]] for r in D["snv"]["ONT"][XLSX_TOOL[t]][c] if r["rep"] in lp]
    if len(xs) > 1:
        return f"{st.mean(xs):.2f} ({st.stdev(xs):.2f})"
    return f"{xs[0]:.2f}"


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
    w(r"{\scriptsize\setlength{\tabcolsep}{3pt}")
    w(r"\begin{longtable}{@{}lrrrrrrrrr@{}}")
    w(r"\caption{\textbf{SNV-only phasing of HG002 nanopore R10.4.1 data by six configurations.} Scored against the v5.0q VCF (chr1--22, no benchmark BED applied). Values at 10--20$\times$ are means (s.d.) over ten down-sampling replicates; 30--60$\times$, one replicate. Phased SNVs are given as a percentage of the 2,398,880 heterozygous SNVs of the benchmark. Precision, phased SNV calls that match a benchmark heterozygous SNV as a percentage of all phased heterozygous SNV calls on chr1--22 (\toolname and \whatshap only); F1, harmonic mean of precision and phased SNVs. Rate ratio, switch error rate divided by that of \toolname in the same down-sampling replicate. Margin and Ralphi were run at 10--20$\times$ only; GCphase was not included (Methods). Ralphi's phase blocks sum to 4.3--5.8~Gb, more than the length of the autosomes, so its block N50 is not comparable with that of the other tools.}\label{tab:snvall}\\")
    w(r"\toprule Cov. & \shortstack[r]{Phased\\SNV (\%)} & \shortstack[r]{Precision\\(\%)} & F1 (\%) & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Rate\\ratio} & \shortstack[r]{Hamming\\(\%)} & Blocks & \shortstack[r]{N50\\(Mb)} \\ \midrule\endfirsthead")
    w(r"\toprule Cov. & \shortstack[r]{Phased\\SNV (\%)} & \shortstack[r]{Precision\\(\%)} & F1 (\%) & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Rate\\ratio} & \shortstack[r]{Hamming\\(\%)} & Blocks & \shortstack[r]{N50\\(Mb)} \\ \midrule\endhead")
    for t in ["lp_gnn", "lp", "wh", "hc", "margin", "ralphi"]:
        for c in COVS:
            runs = D["snv"]["ONT"][XLSX_TOOL[t]].get(c)
            if not runs:
                continue
            prec = cell(precision_runs(t)(c), "prec", 2) if t in ("lp_gnn", "wh") else "--"
            f1 = cell(precision_runs(t)(c), "f1", 2) if t in ("lp_gnn", "wh") else "--"
            if c == COVS[0]:   # tool name on its own row, so that the long names do not widen the table
                w(r"\multicolumn{10}{@{}l}{\textit{" + NAME[t] + r"}} \\*")
            w(f"{c}$\\times$ & {cell(runs, 'psnv_pct', 2)} & {prec} & {f1} & {cell(runs, 'sw', 0)} & "
              f"{cell(runs, 'sw_pct', 3)} & {rate_ratio(t, c)} & {cell(runs, 'ham', 2)} & {cell(runs, 'nblock', 0)} & {cell(runs, 'n50', 2, 1e-6)} \\\\")
        w(r"\midrule")
    L[-1] = r"\bottomrule"
    w(r"\end{longtable}}" + "\n")
    # ---- Table 9: two benchmarks
    w(r"{\scriptsize\setlength{\tabcolsep}{3.5pt}")
    w(r"\begin{longtable}{@{}llrrrrr@{}}")
    w(r"\caption{\textbf{The same phased VCFs scored against GIAB v4.2.1 and the T2T-HG002-derived v5.0q benchmark.} Switch errors on SNVs; Hamming distance over SNVs and, where they are phased, indels. All \toolname runs with GNN correction, phasing SNVs alone or with indels (+indel) or indels and SVs (+indel+SV). Values at 10--20$\times$ are means (s.d.) over ten replicates. Phased indels as a percentage of benchmark heterozygous indels (v5.0q).}\label{tab:twobench}\\")
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
    w(r"\caption{\textbf{Co-phasing configurations of \toolname, without and with GNN correction.} Scored against v5.0q: switch errors on SNVs, Hamming distance over SNVs and, where they are phased, indels; phased indels as a percentage of benchmark heterozygous indels. Means (s.d.) over ten replicates at 10 and 20$\times$; one replicate at 30 and 60$\times$. Every coverage is in Supplementary Data~1.}\label{tab:cophase}\\")
    w(r"\toprule Classes & GNN & Cov. & \shortstack[r]{Phased\\indel (\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & \shortstack[r]{N50\\(Mb)} \\ \midrule\endfirsthead")
    w(r"\toprule Classes & GNN & Cov. & \shortstack[r]{Phased\\indel (\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & \shortstack[r]{N50\\(Mb)} \\ \midrule\endhead")
    for cfg, name, _ in CFG:
        for tool, tag in (("longphase_v2.0.1", "no"), ("longphase_v2.1.2", "yes")):
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
    w(r"\caption{\textbf{SNV-only phasing of HG002 PacBio HiFi (Revio) data.} One replicate per coverage, scored against v5.0q. The network was trained on nanopore data only and applied without retraining. Variants were called separately at every coverage (Methods). HiPhase has no SNV-only option and was given the call set restricted to SNVs. Precision, share of the phased heterozygous SNV calls on chr1--22 that match a benchmark heterozygous SNV (Fig.~5d); --, not computed.}")
    w(r"\label{tab:hifi}\scriptsize")
    w(r"\begin{tabular}{@{}llrrrrrrr@{}}\toprule")
    w(r"Tool & Cov. & \shortstack[r]{Phased\\SNV (\%)} & \shortstack[r]{Precision\\(\%)} & \shortstack[r]{Switch\\errors} & \shortstack[r]{Switch error\\rate (\%)} & \shortstack[r]{Hamming\\(\%)} & Blocks & \shortstack[r]{N50\\(kb)} \\ \midrule")
    for t in ["lp_gnn", "lp", "wh", "hc", "hp"]:
        for c in HIFI_COVS:
            r = hiphase(c) if t == "hp" else D["snv"]["HiFi"][XLSX_TOOL[t]][c]
            prec = f"{precision_hifi(t)(c)[0]['prec']:.2f}" if (t, c) in PHASED_CALLS_HIFI else "--"
            w(f"{NAME[t] if c == 10 else ''} & {c}$\\times$ & {cell(r, 'psnv_pct', 2)} & {prec} & {cell(r, 'sw', 0)} & {cell(r, 'sw_pct', 3)} & "
              f"{cell(r, 'ham', 2)} & {cell(r, 'nblock', 0)} & {cell(r, 'n50', 0, 1e-3)} \\\\")
        w(r"\midrule")
    L[-1] = r"\bottomrule\end{tabular}\end{table}" + "\n"
    # ---- Table 12: T2T assembly validation
    T = t2t()
    cls = T["cls"]; n = T["rm_n"]
    w(r"\begin{table}[h]")
    w(r"\caption{\textbf{SNVs unphased by GNN correction, classified by the T2T-HG002 v1.1 assembly.} Nanopore 60$\times$, replicate~1, SNV-only phasing. ``Aligned'' denotes sites within regions where both assembled haplotypes align one-to-one to GRCh38 (\code{GRCh38\_HG2-T2TQ100-V1.1\_dipcall-z2k.dip.bed}). For these sites, the table also records whether the matching dipcall VCF contains a variant at the same start coordinate; alleles were not compared. All chromosomes, including chrX and chrY, unless stated. The background is a random sample of 50,000 SNVs phased before GNN correction, including sites that GNN correction later unphased. Top, overall classes; bottom, share outside the 1:1 alignment per chromosome. v5.0q is derived from the same assembly, so this analysis extends coverage rather than providing an independent truth set.}")
    w(r"\label{tab:t2t}\small")
    w(r"\begin{tabular}{@{}lrr@{}}\toprule Class & SNVs & Share (\%) \\ \midrule")
    for k, lab in (("unassessed", "not aligned 1:1 (unassessed)"), ("hom_wt", "aligned, no assembly variant record at the same coordinate"),
                   ("variant", "aligned, assembly variant record at the same coordinate")):
        w(f"{lab} & {cls[k]:,} & {100 * cls[k] / n:.2f} \\\\")
    w(f"total & {n:,} & 100.00 \\\\ \\midrule")
    w(f"aligned 1:1, unphased by GNN correction & {T['rm_in']:,} / {n:,} & {100 * T['rm_in'] / n:.2f} \\\\")
    w(f"aligned 1:1, phased before GNN correction (sample) & {T['bg_in']:,} / {T['bg_n']:,} & {100 * T['bg_in'] / T['bg_n']:.2f} \\\\")
    auto = [d for d in T["chroms"] if re.fullmatch(r"chr\d+", d["chrom"])]
    a_rn = sum(d["rm_n"] for d in auto); a_ri = a_rn - sum(d["rm_out"] for d in auto)
    a_bn = sum(d["bg_n"] for d in auto); a_bi = a_bn - sum(d["bg_out"] for d in auto)
    w(f"\\quad autosomes only, unphased by GNN correction & {a_ri:,} / {a_rn:,} & {100 * a_ri / a_rn:.2f} \\\\")
    w(f"\\quad autosomes only, phased before GNN correction (sample) & {a_bi:,} / {a_bn:,} & {100 * a_bi / a_bn:.2f} \\\\")
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
    runtime_table(w)
    # ---- Table 17: SNV calls left unphased, their benchmark status, the other tool's phase at the
    # benchmark het. SNVs among them, and co-location with switch-error intervals (Fig. 4c net values; issue #6)
    w(r"\begin{table}[h]")
    w(r"\caption{\textbf{Heterozygous SNV calls phased by \toolname only, by \whatshap only, by both or by neither.} HG002 nanopore R10.4.1 data, SNV-only phasing, replicate~1; single-base calls with genotype 0/1, identical in both VCFs, including chrX and chrY. Calls phased by \whatshap only are split by the \toolname stage that left them unphased: the phasing graph before GNN correction or GNN correction. Benchmark status against the chr1--22 v5.0q VCF without a BED: het., same position, REF and ALT; other allele, another heterozygous record at the position; hom., homozygous; absent, no record; chrX/Y, outside the truth. \textbf{Top}, composition. \textbf{Middle}, benchmark het. SNVs among calls phased by one tool only, scored for that tool: \emph{assessed}, in a block with at least two assessed variants; \emph{all phased}, the tool's block-wise Hamming distance over all its phased SNVs; \emph{fold}, inside divided by expected. The definitions of wrong phase, switch-error intervals and expected share are in Methods, ``Analysis of unphased SNVs''. \textbf{Bottom}, additional calls phased by \whatshap: calls phased by \whatshap only minus calls phased by \toolname only.}")
    w(r"\label{tab:unphased}\scriptsize\setlength{\tabcolsep}{2.9pt}")
    w(r"\begin{tabular}{@{}llrrrrrr@{}}\toprule")
    w(r"Cov. & Phased by & Calls & Het. & Other allele & Hom. & Absent & chrX/Y \\ \midrule")
    snames = (("wh_only", r"\toolname only"), ("lp_only", r"\whatshap only"),
              ("lp_only_phase", r"\quad unphased by the \toolname graph"),
              ("lp_only_gnn", r"\quad unphased by GNN correction"),
              ("background", "both tools"), ("both", "neither tool"))
    for c in VENN_COVS:
        cl = f"{c}$\\times$"
        for i, (s_, lab) in enumerate(snames):
            w(f"{cl if i == 0 else ''} & {lab} & {comp(c, s_):,} & "
              + " & ".join(f"{comp(c, s_, k):,}" for k in CLASSES) + r" \\")
        if c != VENN_COVS[-1]:
            w(r"\midrule")
    w(r"\bottomrule\end{tabular}\par\medskip")
    w(r"\begin{tabular}{@{}lllrrrrrrr@{}}\toprule")
    w(r" & & & \multicolumn{4}{c}{Benchmark het.\ SNVs among them} & \multicolumn{3}{c}{The scored tool's switch-error intervals} \\ \cmidrule(lr){4-7}\cmidrule(l){8-10}")
    w(r"Cov. & Phased by & Scored tool & Assessed & Wrong & Wrong (\%) & All phased (\%) & Inside (\%) & Expected (\%) & Fold \\ \midrule")
    for c in VENN_COVS:
        cl = f"{c}$\\times$"
        for i, (s_, lab, other) in enumerate((("wh_only", r"\toolname only", r"\toolname"),
                                             ("lp_only", r"\whatshap only", r"\whatshap"))):
            n_, e_, pct, gw = other_tool_errors(c, s_)
            iv = INTV[(c, s_)]
            w(f"{cl if i == 0 else ''} & {lab} & {other} & {n_:,} & {e_:,} & {pct:.1f} & {gw:.2f} & "
              f"{float(iv['in_other_sw_pct']):.2f} & {float(iv['other_background_pct']):.2f} & {float(iv['enrichment']):.2f} \\\\")
    w(r"\bottomrule\end{tabular}\par\medskip")
    w(r"\begin{tabular}{@{}lrrrrrr@{}}\toprule")
    w(r"Cov. & \shortstack[r]{Additional calls\\phased by \whatshap} & Het. (\%) & Other allele & Hom. & Absent & chrX/Y \\ \midrule")
    for c in VENN_COVS:
        d = net_phased(c)
        w(f"{c}$\\times$ & {d['n']:,} & {d['het_match']:,} ({100 * d['het_match'] / d['n']:.0f}) & "
          + " & ".join(f"{d[k]:,}" for k in ("het_other_allele", "hom", "absent", "chrXY")) + r" \\")
    w(r"\bottomrule\end{tabular}\end{table}" + "\n")
    other_phasers_table(w)
    path = os.path.join(ROOT, "figures-source", "supp_tables.tex")
    open(path, "w").write("\n".join(L) + "\n")
    print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    fig2(); fig3_sv_methylation(); fig4(); fig5()
    sfig10(); sfig_runtime(); sfig11(); sfig12(); sfig13(); sfig14(); sfig17(); sfig16(); sfig17_sv_indels()
    tables(); sv_table()
