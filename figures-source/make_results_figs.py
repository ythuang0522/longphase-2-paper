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
    figures/supp/suppfig{10,11,12,14}_*.pdf
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
    for ax, s_ in [(a, l) for a, l in _LETTERS if a.get_figure(root=True) is fig]:
        tb = ax.get_tightbbox(r)
        fig.text(max(tb.x0, 0) / W, min(tb.y1, H) / H, s_, fontsize=8, fontweight="bold",
                 va="top", ha="left")
    fig.savefig(path)
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


# LongPhase 2 co-phasing SNVs and indels with SVs and 5mC added: the evidence WhatsHap cannot use.
# Dashed red in Fig. 2f only (author decision, 2026-10-09: "all four classes" in black, and in the
# SNV-only row, was hard for a reviewer to read).
PLUS = ("Indel+Mod+SV", "LongPhase 2, + SVs and 5mC")


def _path(ax, get, covs, color, ls, marker, msz, mfc="none", z=3):
    """Accuracy-contiguity path: mean SNV switch error rate against mean block N50, one
    point per coverage, joined from the lowest to the highest coverage."""
    xs = [ms(get(c), "sw_pct")[0] for c in covs]
    ys = [ms(get(c), "n50")[0] / 1e6 for c in covs]
    ax.plot(xs, ys, color=color, ls=ls, marker=marker, ms=msz, mfc=mfc, mew=0.8, lw=0.9, zorder=z)
    return xs, ys


def fig2():
    """LongPhase 2 against other phasers for each evidence type and on HiFi data (v5.0q).
    Rows: SNV phasing (WhatsHap, HapCUT2), SNV and indel co-phasing (WhatsHap), SNV and
    5mC co-phasing (MethPhaser), all nanopore; SNV phasing of PacBio HiFi data (WhatsHap; former
    Fig. 5a-c, author decision, 2026-10-09: one message per main figure, HiFi completeness in
    Fig. 4b; one replicate per coverage). Columns: switch error rate, Hamming distance, and the
    switch error rate against block N50 across coverage. Each row compares the tools on the
    same input; panel f adds, dashed, LongPhase 2 with SVs and 5mC also co-phased. In the indel
    row the accuracy panels also score the indels themselves (Supplementary Table 14).
    The phased fractions are in Fig. 4 (author decision, 2026-10-09: accuracy and
    contiguity together, completeness with the analysis of what each tool leaves unphased)."""
    fig = plt.figure(figsize=(FIGW, 198 * MM), layout="constrained")
    fig.get_layout_engine().set(w_pad=2 * MM, h_pad=1.2 * MM, wspace=0.05, hspace=0.0)
    sfs = fig.subfigures(4, 1, hspace=0.035)
    snv = lambda tool: (lambda c: D["snv"]["ONT"][XLSX_TOOL[tool]].get(c))
    hifi = lambda tool: (lambda c: D["snv"]["HiFi"][XLSX_TOOL[tool]].get(c))
    ind = lambda tool: (lambda c: D["coph"]["Indel"][tool].get(c))
    plus = lambda c: D["coph"][PLUS[0]]["longphase_v2.1"].get(c)
    mod1 = lambda c: [r for r in D["coph"]["Mod"]["longphase_v2.1"][c] if r["rep"] == 1]
    meth = lambda c: [{k: meth_value(c, k) for k in ("sw_pct", "ham", "n50", "psnv_pct")}]
    rows = [  # title, coverages, tools (key, name, getter), add the + SVs and 5mC path
        ("SNV phasing", PLOT_COVS,
         [("lp_gnn", "LongPhase 2", snv("lp_gnn")), ("wh", "WhatsHap", snv("wh")), ("hc", "HapCUT2", snv("hc"))], False),
        ("SNV and indel co-phasing", PLOT_COVS,
         [("lp_gnn", "LongPhase 2", ind("longphase_v2.1")), ("wh", "WhatsHap", ind("whatshap_v28"))], True),
        ("SNV and 5mC co-phasing", BAR_COVS,
         [("lp_gnn", "LongPhase 2", mod1), ("meth", "MethPhaser", meth)], False),
        ("SNV phasing, PacBio HiFi", HIFI_COVS,
         [("lp_gnn", "LongPhase 2", hifi("lp_gnn")), ("wh", "WhatsHap", hifi("wh"))], False),
    ]
    last = len(rows) - 1
    indel = {"lp_gnn": _indel_runs("longphase_coh_indel_gnn"), "wh": _indel_runs("whatshap_v28")}
    letters = iter("abcdefghijkl")
    keys = []
    grid = []
    for r, (sf, (title, covs, tools, add_plus)) in enumerate(zip(sfs, rows)):
        axs = sf.subplots(1, 3)
        grid.append(axs)
        ax_tr = axs[2]
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
            st_ = STY[t]
            ex, ey = _path(ax_tr, get, covs, C[t], st_["ls"], st_["marker"], st_["ms"])
            if t in ("wh", "meth"):   # coverage of the first and last point, on the comparator
                for i, dy, va in ((0, -4, "top"), (-1, 4, "bottom")):
                    ax_tr.annotate(f"{covs[i]}×", (ex[i], ey[i]), xytext=(0, dy), textcoords="offset points",
                                   ha="center", va=va, fontsize=5.5, color="#555555")
        if add_plus:
            _path(ax_tr, plus, covs, C["lp_gnn"], (0, (4, 1.6)), STY["lp_gnn"]["marker"], STY["lp_gnn"]["ms"], z=2)
        if r == 1:
            _log_rate_axis(axs[0], ticks=(0.02, 0.05, 0.1, 0.2, 0.5, 1), lim=(0.018, 1.4))
            axs[1].set_ylabel("Indel Hamming distance (%)")
        else:
            _log_rate_axis(axs[0])
            axs[1].set_ylabel("Hamming distance (%)")
        axs[0].set_ylabel("Switch error rate (%)")
        axs[1].set_ylim(bottom=0)
        ax_tr.set_xscale("log"); ax_tr.minorticks_off()
        ax_tr.set_xticks([0.02, 0.05, 0.1, 0.2]); ax_tr.set_xticklabels(["0.02", "0.05", "0.1", "0.2"])
        ax_tr.set_xlim(0.018, 0.32)
        if covs is HIFI_COVS:   # HiFi blocks are 4-7 times shorter; own N50 scale
            ax_tr.set_ylim(0, 0.7); ax_tr.set_yticks([0, 0.2, 0.4, 0.6])
        else:
            ax_tr.set_ylim(0, 5.9); ax_tr.set_yticks([0, 1, 2, 3, 4, 5])   # MethPhaser reaches 5.5 Mb at 60x
        ax_tr.set_ylabel("Block N50 (Mb)")
        for ax, top in zip(axs[:2], grid[0][:2]):
            cov_axis(ax, HIFI_COVS if covs is HIFI_COVS else (10, 20, 30, 40, 50, 60))
            ax.set_xlim(top.get_xlim())   # same coverage scale in every row
            if r < last:
                ax.set_xlabel("")
        if r == last:
            ax_tr.set_xlabel("SNV switch error rate (%)")
        for ax in axs:
            letter(ax, next(letters))
        _row_header(sf, title)
        k = [thandle(t, name) for t, name, _ in tools]
        if add_plus:
            k.insert(1, Line2D([], [], color=C["lp_gnn"], ls=(0, (4, 1.6)), marker=STY["lp_gnn"]["marker"],
                               ms=STY["lp_gnn"]["ms"] + 0.4, mfc="none", mew=0.8, label=PLUS[1]))
        if r == 1:
            k += [Line2D([], [], color="#555555", ls="-", label="SNV pairs"),
                  Line2D([], [], color="#555555", ls=":", marker="o", ms=2.6, label="pairs with an indel")]
        keys.append(k)
    align_ylabels(fig, [[row[i] for row in grid] for i in range(3)])
    _row_keys(fig, sfs, keys)
    save(fig, os.path.join(OUT, "fig2_phaser_comparison.pdf"))


# ============================================================ Figure 4 =====
# What each tool phases and leaves unphased (former Fig. 6 merged with the phased
# fractions of former Fig. 2d,h; author decision, 2026-10-09; Fig. 3 until the swap with the
# two-benchmark figure, author decision, 2026-10-09).
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
    other = "whatshap_v28" if s.startswith("lp") else "longphase_v2.1"
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


def fig4():
    """What LongPhase 2 leaves unphased (author decisions, 2026-10-09 and 2026-10-10). Row 1, calls
    phased by LongPhase 2 and WhatsHap: one message -- LongPhase 2 phases about 1% fewer benchmark
    SNVs, but more of the calls it phases are benchmark SNVs, and fewer of them are genotype
    errors. a completeness (nanopore), b completeness (PacBio HiFi, former Fig. 5d), c precision
    (F1 in the text and Supplementary Table 8), d phased calls at positions where v5.0q is
    homozygous (genotype errors written onto a haplotype; GIAB v5.0q framing); c and d are
    nanopore only, because no HiFi precision or genotype-error counts exist. Row 2, SNVs unphased
    by GNN correction (former Supplementary Fig. 16, promoted 2026-10-10 so that a main figure
    shows what the network withholds): e v5.0q status by coverage, f T2T-HG002 assembly status at
    60x against a random sample of SNVs phased before correction, g the same by chromosome.
    Row 2 is a different set from row 1: GNN correction leaves unphased only about one sixth of
    the calls that LongPhase 2 alone leaves unphased. No numbers inside panels (author,
    2026-10-09); they are in the text and Supplementary Table 12. The calls left unphased by one
    tool only, their read depth and interval co-location are in the text, Supplementary Table 17
    and Supplementary Fig. 12; the regions added by v5.0q are in Fig. 3d,e."""
    fig = plt.figure(figsize=(FIGW, 136 * MM), layout="constrained")
    fig.get_layout_engine().set(w_pad=2 * MM, h_pad=1.2 * MM, wspace=0.05, hspace=0.0)
    sf1, sf2 = fig.subfigures(2, 1, height_ratios=[62, 74], hspace=0.035)
    # ---- row 1: LongPhase 2 and WhatsHap
    ax_a, ax_h, ax_b, ax_c = sf1.subplots(1, 4)
    TOOLS = (("wh", "WhatsHap"), ("lp_gnn", "LongPhase 2"))   # LongPhase 2 drawn last, on top
    snv = lambda tool, plat="ONT": (lambda c: D["snv"][plat][XLSX_TOOL[tool]].get(c))
    for t, _ in TOOLS:
        tline(ax_a, t, *_series(snv(t), PLOT_COVS)("psnv_pct"))
        tline(ax_h, t, *_series(snv(t, "HiFi"), HIFI_COVS)("psnv_pct"))
        tline(ax_b, t, *_series(precision_runs(t), PLOT_COVS)("prec"))
    ax_a.set_ylim(76, 94); ax_a.set_yticks([76, 80, 84, 88, 92])
    ax_a.set_ylabel("Benchmark het. SNVs phased (%)")
    ax_a.set_title("Completeness, nanopore", loc="center", fontsize=6.5)
    ax_h.set_ylim(86, 93); ax_h.set_yticks([86, 88, 90, 92])
    ax_h.set_ylabel("Benchmark het. SNVs phased (%)")
    ax_h.set_title("Completeness, PacBio HiFi", loc="center", fontsize=6.5)
    ax_b.set_ylim(84, 95); ax_b.set_yticks([85, 88, 91, 94])
    ax_b.set_ylabel("Phased calls that are\nbenchmark het. SNVs (%)")
    ax_b.set_title("Precision, nanopore", loc="center", fontsize=6.5)
    cov_axis(ax_a); cov_axis(ax_b); cov_axis(ax_h, HIFI_COVS)
    ax_h.set_xlim(ax_a.get_xlim())   # same coverage scale as a
    ax = ax_c   # d: grouped bars, both tools, replicate 1 at 10/30/60x
    for i, (t, _) in enumerate(reversed(TOOLS)):
        ax.bar([j + (i - 0.5) * 0.36 for j in range(3)], [phased_class(c, t, "hom") / 1000 for c in VENN_COVS],
               0.33, color=C[t], zorder=3)
    ax.set_xticks(range(3)); ax.set_xticklabels([f"{c}×" for c in VENN_COVS])
    ax.set_xlim(-0.6, 2.6); ax.set_ylim(0, 30); ax.set_yticks([0, 10, 20, 30])
    ax.set_xlabel("Coverage"); ax.set_ylabel("Phased het. calls at v5.0q\nhomozygous sites (thousands)")
    ax.set_title("Genotype errors phased, nanopore", loc="center", fontsize=6.5)
    # ---- row 2: SNVs unphased by GNN correction (LongPhase 2 only)
    T = t2t()
    ax_e, ax_f, ax_g = sf2.subplots(1, 3, width_ratios=[1.25, 1, 0.9])
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
    for ax, L in zip((ax_a, ax_h, ax_b, ax_c, ax_e, ax_f, ax_g), "abcdefg"):
        letter(ax, L)
    for ax in (ax_e, ax_f, ax_g):   # letter() resets the title pad of every title of the axes
        ax.set_title(ax.get_title(loc="center"), loc="center", fontsize=6.5, pad=KEYPAD)
    _row_header(sf1, "Calls phased by LongPhase 2 and WhatsHap")
    _row_header(sf2, "SNVs unphased by GNN correction")
    dot = lambda col, lab: Line2D([], [], color=col, ls="none", marker="o", ms=2.6, label=lab)
    _row_keys(fig, (sf1, sf2), ([thandle(t, n_) for t, n_ in reversed(TOOLS)],
                                [dot("#4D4D4D", "phased (random sample)"), dot(C["lp_gnn"], "unphased by GNN")]))
    save(fig, os.path.join(OUT, "fig4_phased_unphased.pdf"))


# ============================================================ Figure 3 =====
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


def fig3():
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
    save(fig, os.path.join(OUT, "fig3_two_benchmarks.pdf"))


# ======================= Fig. 4e-g (former Supplementary Fig. 16) and Table 12 data =====
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


def _runtime():
    """notes/runtime/runtime.tsv (issue #8): (tool, threads, coverage) -> (wall min, CPU min,
    peak RSS GiB). Replicate 1, GNU time of the paper runs; LongPhase 2 on one thread timed at
    10x and 60x only; no HapCUT2 rows at 30x and 40x (logs overwritten)."""
    import csv
    rows = csv.DictReader(open(os.path.join(ROOT, "notes", "runtime", "runtime.tsv")), delimiter="\t")
    return {(r["tool"], r["threads"], int(r["coverage"])):
            (int(r["wall_s"]) / 60, int(r["cpu_s"]) / 60, int(r["max_rss_kb"]) / 1024 ** 2) for r in rows}


# ============================================== Supplementary Fig. 10 =====
def sfig_runtime():
    """Runtime and peak memory of SNV-only phasing across coverage (issue #8). The HapCUT2 line
    is broken at 30-40x, where no timing exists; LongPhase 2 on one thread has points only."""
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
    for row, tool, tag in ((0, "longphase_v2.0.1", "without GNN correction"), (1, "longphase_v2.1", "with GNN correction")):
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
        ax.plot(covs, [rep1("Mod", "longphase_v2.1", c, key) * sc for c in covs], color=C["lp_gnn"],
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


# ------------------------------------------- issue #3 table (Table 16) ---
def runtime_table(w):
    """Runtime and peak memory of SNV-only phasing at every coverage (notes/runtime/runtime.tsv)."""
    from decimal import Decimal, ROUND_HALF_UP
    r1 = lambda x: str(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
    rt = _runtime()
    w(r"\begin{table}[h]")
    w(r"\caption{\textbf{Runtime and peak memory of SNV-only phasing.} HG002 nanopore R10.4.1 data, replicate~1 at every coverage, on the workstation described in Methods (Supplementary Fig.~10). Wall-clock time and CPU time (user plus system) in minutes and peak resident memory in GiB, from \code{/usr/bin/time}. \toolname includes GNN correction; in the 24-thread runs, phasing and GNN correction were run as separate commands and their times summed (Methods). \toolname was timed on one thread at 10 and 60$\times$ only, and \hapcut times are not available at 30 and 40$\times$ (Methods); --, no value. \hapcut includes fragment extraction.}\label{tab:runtime}")
    w(r"\small\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}rrrrrrrrrrrrr@{}}\toprule")
    groups = [(("LongPhase 2", "24"), r"\toolname, 24 threads"), (("LongPhase 2", "1"), r"\toolname, 1 thread"),
              (("WhatsHap 2.8", "1"), r"\whatshap"), (("HapCUT2 1.3.4", "1"), r"\hapcut")]
    w(" & " + " & ".join(rf"\multicolumn{{3}}{{c}}{{{n}}}" for _, n in groups) + r" \\ "
      + "".join(rf"\cmidrule({'lr' if i < 3 else 'l'}){{{2 + 3 * i}-{4 + 3 * i}}}" for i in range(4)))
    w("Coverage & " + " & ".join(["Wall & CPU & Memory"] * 4) + r" \\ \midrule")
    for c in COVS:
        cells = []
        for key, _ in groups:
            v = rt.get(key + (c,))
            cells += [r1(x) for x in v] if v else ["--"] * 3
        w(rf"{c}$\times$ & " + " & ".join(cells) + r" \\")
    w(r"\bottomrule\end{tabular}\end{table}")

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
    w(r"\caption{\textbf{SNVs unphased by GNN correction, classified by the T2T-HG002 v1.1 assembly.} Nanopore 60$\times$, replicate~1, SNV-only phasing. ``Aligned'' means inside the dipcall BED in which both assembled haplotypes align 1:1 to GRCh38 (\code{GRCh38\_HG2-T2TQ100-V1.1\_dipcall-z2k.dip.bed}); presence of an assembly variant record at the same start coordinate in the matching dipcall VCF (alleles not compared). All chromosomes, including chrX and chrY, unless stated. The background is a random sample of 50,000 SNVs phased before GNN correction, including sites that GNN correction later unphased. Top, overall classes; bottom, share outside the 1:1 alignment per chromosome. v5.0q is derived from the same assembly, so this analysis extends coverage rather than providing an independent truth set.}")
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
    w(r"\caption{\textbf{Heterozygous SNV calls phased by \toolname only, by \whatshap only, by both or by neither.} HG002 nanopore R10.4.1 data, SNV-only phasing, replicate~1; heterozygous SNV calls with single-base alleles and genotype 0/1, identical in both output VCFs, chrX and chrY included. Calls phased by \whatshap only are split by the \toolname stage that left them unphased: the phasing graph (unphased before GNN correction) or GNN correction. Benchmark status against the v5.0q VCF (chr1--22, no BED): het., heterozygous with the same position, reference and alternative allele (the match used by \code{compare}); other allele, another heterozygous record at the position; hom., homozygous; absent, no record; chrX/Y, outside the chr1--22 truth. \textbf{Top}, composition. \textbf{Middle}, the benchmark heterozygous SNVs among the calls phased by one tool only, scored for that tool: assessed, in a block with at least two assessed variants; wrong, phase opposite to the block's majority orientation relative to the truth (block-wise Hamming error); all phased, the tool's block-wise Hamming distance over all its phased SNVs. Switch-error intervals of the scored tool run from the first SNV of one of its switch-error pairs to the base before the second; inside, the share of the calls phased by that tool only that lie in them; expected, the share of all heterozygous SNV calls phased by that tool. \textbf{Bottom}, additional calls phased by \whatshap: calls phased by \whatshap only minus calls phased by \toolname only.}")
    w(r"\label{tab:unphased}\scriptsize\setlength{\tabcolsep}{3.5pt}")
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
    path = os.path.join(ROOT, "figures-source", "supp_tables.tex")
    open(path, "w").write("\n".join(L) + "\n")
    print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    fig2(); fig3(); fig4()
    sfig10(); sfig_runtime(); sfig11(); sfig12(); sfig13(); sfig14(); sfig17()
    tables()
