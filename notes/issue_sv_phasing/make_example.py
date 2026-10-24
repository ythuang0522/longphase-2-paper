"""Example layout of the SV phasing figure (issue: SV phasing accuracy). PLACEHOLDER VALUES ONLY.

The values below are invented to show the layout. They follow the shape of the
v2.1.1 / WhatsHap 2.8 numbers in twolinin/longphase#136 (ONT 10x and 30x, HiFi 30x),
but every other point is made up. Do not cite them.

The real figure reads `notes/sv_phasing/sv_phasing.tsv` (columns in the issue).
Style follows figures-source/make_results_figs.py (Fig. 2).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

MM = 1 / 25.4
plt.rcParams.update({
    "font.family": "Arial", "font.size": 6.5, "axes.titlesize": 6.5, "axes.labelsize": 6.5,
    "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6, "axes.linewidth": 0.5,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5, "xtick.major.size": 2.5,
    "ytick.major.size": 2.5, "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "savefig.dpi": 300, "axes.labelpad": 2.5, "axes.titlepad": 3,
})
C = {"lp": "#B2182B", "wh": "#2166AC", "hp": "#35978F"}
MK = {"lp": ("o", 3.0), "wh": ("D", 2.8), "hp": ("v", 3.4)}
NAME = {"lp": "LongPhase 2", "wh": "WhatsHap", "hp": "HiPhase"}

ONT = [10, 12, 14, 16, 18, 20, 30, 40, 50, 60]
HIFI = [10, 20, 30, 40, 50]
# column -> tool -> (error rate %, SVs phased right) per coverage. PLACEHOLDERS.
D = {
    "Nanopore, SNVs + SVs": (ONT, {
        "lp": ([10.0, 9.3, 8.7, 8.2, 7.8, 7.5, 6.9, 6.8, 6.7, 6.7],
               [7350, 7900, 8350, 8700, 8950, 9100, 9460, 9440, 9400, 9354]),
        "wh": ([16.7, 15.6, 14.7, 14.0, 13.4, 13.0, 12.0, 11.7, 11.5, 11.4],
               [8099, 8650, 9100, 9450, 9700, 9850, 10008, 10050, 10060, 10050])}),
    "Nanopore, SNVs + indels + SVs": (ONT, {
        "lp": ([13.6, 12.7, 12.0, 11.4, 11.0, 10.7, 9.8, 9.6, 9.5, 9.4],
               [6600, 7100, 7500, 7800, 8000, 8150, 8553, 8540, 8510, 8480]),
        "wh": ([22.0, 20.8, 19.8, 19.0, 18.3, 17.9, 16.5, 16.1, 15.9, 15.8],
               [6800, 7250, 7600, 7850, 8000, 8100, 8376, 8400, 8410, 8400])}),
    "PacBio HiFi, SNVs + SVs": (HIFI, {
        "lp": ([8.4, 7.0, 6.6, 6.5, 6.4], [8900, 9700, 9878, 9900, 9890]),
        "hp": ([10.2, 8.6, 8.2, 8.1, 8.0], [9100, 9950, 10150, 10170, 10160]),
        "wh": ([11.8, 10.0, 9.6, 9.5, 9.4], [9300, 10200, 10405, 10430, 10420])}),
    "PacBio HiFi, SNVs + indels + SVs": (HIFI, {
        "lp": ([9.6, 8.1, 7.7, 7.6, 7.5], [8000, 8700, 8850, 8870, 8860]),
        "hp": ([11.4, 9.8, 9.4, 9.3, 9.2], [7900, 8600, 8780, 8800, 8790]),
        "wh": ([13.4, 11.5, 11.0, 10.9, 10.8], [7800, 8500, 8685, 8700, 8690])}),
}

fig, axs = plt.subplots(2, 4, figsize=(183 * MM, 96 * MM), layout="constrained")
for j, (title, (covs, tools)) in enumerate(D.items()):
    a, b = axs[0, j], axs[1, j]
    for t, (err, right) in tools.items():
        m, ms = MK[t]
        a.plot(covs, err, color=C[t], marker=m, ms=ms, mfc="none", mew=0.8, lw=0.9)
        b.plot([r / 1000 for r in right], err, color=C[t], marker=m, ms=ms, mfc="none", mew=0.8, lw=0.9)
        for k, va in ((0, "top"), (-1, "bottom")):   # label the path ends with their coverage
            b.annotate(f"{covs[k]}×", (right[k] / 1000, err[k]), xytext=(0, -4 if va == "top" else 4),
                       textcoords="offset points", ha="center", va=va, fontsize=5.5, color="#555555")
    a.set_title(title, fontsize=6.5)
    a.set_xticks(covs if len(covs) < 6 else [10, 20, 30, 40, 50, 60])
    a.set_xlabel("Coverage (×)")
    b.set_xlabel("SVs phased correctly (thousands)")
    for ax in (a, b):
        ax.set_ylim(0, 24)
        ax.set_ylabel("SV phasing error rate (%)")
for ax, L in zip([*axs[0], *axs[1]], "abcdefgh"):
    ax.text(-0.22, 1.08, L, transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom")
fig.legend(handles=[Line2D([], [], color=C[t], marker=MK[t][0], ms=MK[t][1] + 0.4, mfc="none",
                           mew=0.8, label=NAME[t] + (" (HiFi only)" if t == "hp" else ""))
                    for t in ("lp", "wh", "hp")],
           loc="outside upper center", ncol=3)
fig.text(0.5, 0.45, "EXAMPLE LAYOUT — PLACEHOLDER VALUES, NOT DATA", ha="center", va="center",
         fontsize=14, color="#BBBBBB", alpha=0.6, rotation=12, fontweight="bold", zorder=10)
fig.savefig("example_sv_phasing.png")
