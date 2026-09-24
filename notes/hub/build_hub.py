#!/usr/bin/env python3
"""Build the claude.ai hub for the compiled manuscript: page images, PDFs, figure previews, index.html.

Mirrors ../multimodal/multimodal-diagnosis-paper/notes/hub/build_hub.py.

Usage (from the paper folder, after `make`):
    python3 notes/hub/build_hub.py            # writes hub-build/ (gitignored)
Then publish with the Artifact tool, keeping the SAME artifact URL:
    file_path = hub-build/index.html, root = hub-build, files = contents of hub-build/files.json
The PDFs and images are published as supporting files at fixed paths next to the page
(main.pdf, supplementary.pdf, pages/main-NN.jpg, pages/supp-NN.jpg, figures/figN.png,
figures/suppfigN.png), so every rebuild replaces them in place and the links never change.
Pages that no longer exist are removed by the nulls in files_with_removals.json. In a new
session, list the artifact's files first (Artifact tool: action "list", scope "files")
before republishing, or the replace is refused.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "hub-build"
ARTIFACT = "https://claude.ai/artifact/339iTVSwod8JqKgQASYfZm"
REPO = "https://github.com/ythuang0522/longphase-2-paper"
TOOL_REPO = "https://github.com/twolinin/longphase"
DPI = 110
MAX_PAGES = 80  # nulls are emitted up to this count so stale pages disappear on republish

# Main figures: (short name, source file under figures/). SVG sources are rasterized;
# PNG sources are copied as they are (Figs. 2-6 are raster exports, README item 9).
MAIN_FIGS = [
    ("fig1", "fig1_overview.svg", "Fig. 1",
     "Overview: heterogeneous evidence (SNVs, indels, SVs, 5mC) from the same reads enters one weighted phasing graph; "
     "evidence is calibrated by base quality and sequence context; a GATv2 + Transformer network scores every phased "
     "variant and unphases those predicted misphased; outputs are two haplotypes and haplotagged reads."),
    ("fig2", "fig2_snv_comparison.png", "Fig. 2",
     "SNV phasing against WhatsHap 2.8 and HapCUT2 1.3.4 on HG002 R10.4.1 at 10–60×, scored on the T2T-HG002 v5.0q "
     "benchmark: phased fraction, switch error rate, Hamming distance, block N50 and runtime."),
    ("fig3", "fig3_two_benchmarks.png", "Fig. 3",
     "The same phased VCFs scored against GIAB v4.2.1 (GRCh38) and v5.0q (T2T-HG002): switch errors the GRCh38 truth "
     "set conceals in segmental duplications and satellite arrays."),
    ("fig4", "fig4_cophasing.png", "Fig. 4",
     "Co-phasing of SNVs, indels, SVs and allele-specific methylation: phased fraction per class, and the SNV switch "
     "error rate and Hamming distance for SNV-only versus four-class runs, with and without correction."),
    ("fig5", "fig5_variant_combinations.png", "Fig. 5",
     "Neural-network correction across variant-class combinations: switch error rate, Hamming distance and N50 per run."),
    ("fig6", "fig6_unphased_analysis.png", "Fig. 6",
     "Composition of the SNVs the network unphases: benchmark-absent, homozygous or genuine heterozygous; depth and "
     "informativeness within each class; overlapping conditions (entropy 0 or ≥0.8, low GQ, clustered variants)."),
]
SUPP_FIGS = [
    ("suppfig1", "supp/suppfig1_observations.svg", "Supplementary Fig. 1", "Read-level allele observations and every pre-graph filter, including the copy-number state machine."),
    ("suppfig2", "supp/suppfig2_voting.svg", "Supplementary Fig. 2", "Pair support, vote rule, votes, single-read guard, phasing entropy and block formation."),
    ("suppfig3", "supp/suppfig3_read_correction.svg", "Supplementary Fig. 3", "Read-based correction of the initial haplotype assignment."),
    ("suppfig4", "supp/suppfig4_gnn_overview.svg", "Supplementary Fig. 4", "Where the graph neural network sits in the pipeline and what it is allowed to change."),
    ("suppfig5", "supp/suppfig5_gnn_window.svg", "Supplementary Fig. 5", "Window construction around a trigger variant, DOT export and the phase-set update after unphasing."),
    ("suppfig6", "supp/suppfig6_gnn_architecture.svg", "Supplementary Fig. 6", "GPS layer: GATv2 local branch, Transformer global branch, fusion, feed-forward and classifier."),
    ("suppfig7", "supp/suppfig7_modcall.svg", "Supplementary Fig. 7", "Allele-specific methylation calling (modcall): genotyping, co-segregation and CpG-run merging."),
    ("suppfig8", "supp/suppfig8_metrics.svg", "Supplementary Fig. 8", "Evaluation metrics: block intersection, switch encoding, flips, Hamming distance and N50."),
]


def run(*cmd: str) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def pages_of(pdf: Path) -> int:
    return int(re.search(r"Pages:\s+(\d+)", run("pdfinfo", str(pdf))).group(1))


def render_pages(pdf: Path, prefix: str) -> int:
    n = pages_of(pdf)
    tmp = OUT / "_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    run("pdftoppm", "-jpeg", "-jpegopt", "quality=82", "-r", str(DPI), str(pdf), str(tmp / prefix))
    (OUT / "pages").mkdir(exist_ok=True)
    for i in range(1, n + 1):
        cands = [tmp / f"{prefix}-{i}.jpg", tmp / f"{prefix}-{i:02d}.jpg", tmp / f"{prefix}-{i:03d}.jpg"]
        src = next(c for c in cands if c.exists())
        shutil.move(str(src), OUT / "pages" / f"{prefix}-{i:02d}.jpg")
    shutil.rmtree(tmp)
    return n


def export_figure(short: str, source: str) -> None:
    src = ROOT / "figures" / source
    dst = OUT / "figures" / f"{short}.png"
    if src.suffix == ".svg":
        run("rsvg-convert", "-f", "png", "-z", "1.6", "-o", str(dst), str(src))
    else:
        shutil.copy(src, dst)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "figures").mkdir(parents=True)
    shutil.copy(ROOT / "main.pdf", OUT / "main.pdf")
    shutil.copy(ROOT / "Supplementary.pdf", OUT / "supplementary.pdf")
    n_main = render_pages(ROOT / "main.pdf", "main")
    n_supp = render_pages(ROOT / "Supplementary.pdf", "supp")
    for short, source, _, _ in MAIN_FIGS + SUPP_FIGS:
        export_figure(short, source)

    tex = [ROOT / "main.tex", ROOT / "Supplementary.tex", *sorted((ROOT / "sections").glob("*.tex"))]
    # count only rendered marks: a \todo{ inside a % source comment does not render
    # (an unescaped % starts a LaTeX comment; \% is a literal percent sign)
    strip_comment = re.compile(r"(?<!\\)%.*$")
    todo = sum(
        sum(strip_comment.sub("", ln).count("\\todo{")
            for ln in t.read_text(encoding="utf-8").splitlines())
        for t in tex
    )
    refs = sum(1 for ln in (ROOT / "references.bib").read_text(encoding="utf-8").splitlines() if ln.startswith("@"))
    commit = run("git", "-C", str(ROOT), "log", "-1", "--format=%h").strip()
    dirty = bool(run("git", "-C", str(ROOT), "status", "--porcelain").strip())
    date = run("git", "-C", str(ROOT), "log", "-1", "--format=%ad", "--date=short").strip()

    def page_imgs(prefix: str, n: int, label: str) -> str:
        return "".join(
            f'<figure class="page"><img src="pages/{prefix}-{i:02d}.jpg" alt="{label} page {i}" loading="lazy" width="909" height="1286">'
            f'<figcaption>{label} · page {i} of {n}</figcaption></figure>'
            for i in range(1, n + 1))

    def fig_cards(figs: list[tuple[str, str, str, str]]) -> str:
        return "".join(
            f'<figure><img src="figures/{short}.png" alt="{label}" loading="lazy"><figcaption><b>{label}</b> {cap}</figcaption></figure>'
            for short, _, label, cap in figs)

    html = f"""<title>LongPhase 2 Manuscript</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
:root{{
  --bg:#f5f7fa; --surface:#ffffff; --ink:#16233d; --ink-2:#465063; --muted:#76818f; --line:#dbe1e8;
  --hap1:#1687c9; --hap2:#dc2b23; --accent:#1687c9; --accent-ink:#ffffff; --accent-soft:#e2f1fa;
  --flag:#b3261e; --flag-soft:#fbeae8; --page-shadow:rgba(22,35,61,.12);
  color-scheme:light;
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --bg:#0e1420; --surface:#161d2b; --ink:#e9eef5; --ink-2:#b3bccb; --muted:#86909f; --line:#283244;
    --hap1:#6cc8ee; --hap2:#f0766c; --accent:#6cc8ee; --accent-ink:#0b1220; --accent-soft:#16304a;
    --flag:#f0766c; --flag-soft:#341a18; --page-shadow:rgba(0,0,0,.5);
    color-scheme:dark;
  }}
}}
:root[data-theme="dark"]{{
  --bg:#0e1420; --surface:#161d2b; --ink:#e9eef5; --ink-2:#b3bccb; --muted:#86909f; --line:#283244;
  --hap1:#6cc8ee; --hap2:#f0766c; --accent:#6cc8ee; --accent-ink:#0b1220; --accent-soft:#16304a;
  --flag:#f0766c; --flag-soft:#341a18; --page-shadow:rgba(0,0,0,.5);
  color-scheme:dark;
}}
body{{background:var(--bg); color:var(--ink); font-family:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif; font-size:16px; line-height:1.5;}}
.wrap{{max-width:1080px; margin:0 auto; padding-block:36px 64px; padding-inline:20px;}}
.eyebrow{{font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); font-weight:600;}}
h1{{font-family:"Newsreader",Georgia,"Times New Roman",serif; font-weight:600; font-size:clamp(25px,3.4vw,38px); line-height:1.18; margin:8px 0 12px; text-wrap:balance; max-width:32ch;}}
.haps{{display:flex; gap:4px; width:120px; height:4px; margin:0 0 16px;}}
.haps span{{flex:1; border-radius:2px;}} .haps .h1{{background:var(--hap1);}} .haps .h2{{background:var(--hap2);}}
.sub{{color:var(--ink-2); max-width:70ch; margin:0 0 22px;}}
.actions{{display:flex; flex-wrap:wrap; gap:10px; margin-bottom:28px;}}
.btn{{display:inline-flex; align-items:center; gap:8px; padding:10px 16px; border-radius:8px; border:1px solid var(--line); background:var(--surface); color:var(--ink); text-decoration:none; font-weight:600;}}
.btn:hover{{border-color:var(--accent);}} .btn:focus-visible{{outline:2px solid var(--accent); outline-offset:2px;}}
.btn.primary{{background:var(--accent); color:var(--accent-ink); border-color:var(--accent);}}
.grid{{display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin-bottom:28px;}}
@media (max-width:720px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr));}}}}
.stat{{background:var(--surface); border:1px solid var(--line); border-radius:10px; padding:14px 16px;}}
.stat .k{{font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; font-weight:600;}}
.stat .v{{font-size:26px; font-weight:600; font-variant-numeric:tabular-nums; margin-top:2px;}}
.stat .v.todo{{color:var(--flag);}}
.stat .n{{font-size:13px; color:var(--ink-2);}}
.tabs{{display:flex; gap:6px; border-bottom:1px solid var(--line); margin:8px 0 18px;}}
.tabs button{{appearance:none; background:none; border:0; border-bottom:2px solid transparent; padding:10px 14px; font:inherit; font-weight:600; color:var(--ink-2); cursor:pointer;}}
.tabs button[aria-selected="true"]{{color:var(--accent); border-bottom-color:var(--accent);}}
.tabs button:focus-visible{{outline:2px solid var(--accent); outline-offset:-2px;}}
.reader{{display:grid; gap:18px; justify-items:center;}}
.page{{margin:0; width:100%; max-width:820px; background:none; border:0; padding:0;}}
.page img{{display:block; width:100%; height:auto; background:#ffffff; border:1px solid var(--line); box-shadow:0 2px 12px var(--page-shadow); border-radius:3px;}}
.page figcaption{{font-size:12px; color:var(--muted); text-align:center; margin-top:6px; font-variant-numeric:tabular-nums;}}
h2{{font-family:"Newsreader",Georgia,serif; font-weight:600; font-size:23px; margin:36px 0 12px;}}
.flags{{display:grid; gap:10px;}}
.flag{{display:grid; grid-template-columns:auto 1fr; gap:12px; align-items:start; background:var(--flag-soft); border-left:3px solid var(--flag); border-radius:8px; padding:12px 14px;}}
.flag .tag{{font-size:12px; font-weight:600; color:var(--flag); text-transform:uppercase; letter-spacing:.08em; padding-top:3px; min-width:5.5em;}}
.flag p{{margin:0; color:var(--ink);}}
figure{{margin:0 0 26px; background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:14px;}}
figure img{{display:block; width:100%; height:auto; border-radius:6px; background:#ffffff;}}
figcaption{{font-size:14px; color:var(--ink-2); margin-top:10px;}}
.supp{{display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px;}}
.supp figure{{margin:0;}}
@media (max-width:820px){{.supp{{grid-template-columns:1fr;}}}}
.meta{{color:var(--muted); font-size:14px; margin-top:28px;}}
code{{font-family:"IBM Plex Mono","SF Mono",Menlo,Consolas,monospace; font-size:.9em; background:var(--accent-soft); padding:1px 5px; border-radius:4px;}}
a{{color:var(--accent);}}
@media (prefers-reduced-motion: no-preference){{ html{{scroll-behavior:smooth;}} }}
</style>
<div class="wrap">
  <div class="eyebrow">Manuscript draft · built {date} from <code>{commit}</code>{' (uncommitted edits present)' if dirty else ''}</div>
  <h1>Uncertainty-aware haplotype phasing of genetic and epigenetic variation from long reads</h1>
  <div class="haps" aria-hidden="true"><span class="h1"></span><span class="h2"></span></div>
  <p class="sub">LongPhase 2 co-phases SNVs, small indels, structural variants and 5mC in one weighted phasing graph, calibrates every read observation by base quality and sequence context, and scores each phased variant with a graph neural network that unphases, never flips, the assignments it predicts to be wrong. Benchmarked on HG002 nanopore R10.4.1 at 10–60× against the GIAB v4.2.1 and T2T-HG002 v5.0q truth sets. Items in red are the facts only the authors can supply before submission.</p>
  <div class="actions">
    <a class="btn primary" href="main.pdf" target="_blank" rel="noopener">Manuscript PDF</a>
    <a class="btn" href="supplementary.pdf" target="_blank" rel="noopener">Supplementary PDF</a>
    <a class="btn" href="{REPO}" target="_blank" rel="noopener">LaTeX sources on GitHub</a>
    <a class="btn" href="{TOOL_REPO}" target="_blank" rel="noopener">LongPhase source</a>
  </div>
  <div class="grid">
    <div class="stat"><div class="k">Main text</div><div class="v">{n_main} pp</div><div class="n">line-numbered, {len(MAIN_FIGS)} figures</div></div>
    <div class="stat"><div class="k">Supplementary</div><div class="v">{n_supp} pp</div><div class="n">6 methods, 2 notes, 6 tables, 9 figures</div></div>
    <div class="stat"><div class="k">Open marks</div><div class="v todo">{todo}</div><div class="n">red <code>\\todo</code> items blocking submission</div></div>
    <div class="stat"><div class="k">References</div><div class="v">{refs}</div><div class="n">resolved through Crossref</div></div>
  </div>

  <div class="tabs" role="tablist" aria-label="Document">
    <button id="tab-main" role="tab" aria-selected="true" aria-controls="reader-main">Main text ({n_main} pages)</button>
    <button id="tab-supp" role="tab" aria-selected="false" aria-controls="reader-supp">Supplementary ({n_supp} pages)</button>
  </div>
  <div id="reader-main" class="reader" role="tabpanel" aria-labelledby="tab-main">{page_imgs("main", n_main, "Main text")}</div>
  <div id="reader-supp" class="reader" role="tabpanel" aria-labelledby="tab-supp" hidden>{page_imgs("supp", n_supp, "Supplementary")}</div>

  <h2>Open before submission</h2>
  <div class="flags">
    <div class="flag"><span class="tag">Code</span><p><code>gnn</code> and <code>compare</code> exist only on branch <code>JH</code> (tip <code>cc17fb1</code>); tag v2.0.2 on <code>main</code> cannot reproduce any result here. Merge and tag before submission. Two working-tree fixes (vote-weight <code>else if</code> in <code>PhasingGraph.cpp</code>; the 7→6 edge-feature comment in <code>GNNModel.h</code>) are uncommitted.</p></div>
    <div class="flag"><span class="tag">Training</span><p>The complete GNN training chain (data preparation, training, ONNX export, weight embedding, checkpoint, log) exists only in the local <code>GNN source/</code> folder with absolute paths. It must be parameterized and deposited; Methods already describes it from those files.</p></div>
    <div class="flag"><span class="tag">Figures</span><p>Figs. 2–6 are raster exports from the 2026-09-02 slide deck; WhatsHap, HapCUT2 and LongPhase 1.0 values are read off the plots. Regenerate as vector figures from the <code>longphase compare</code> TSVs with exact values and 10–20× s.d. bands. Supplementary Fig. 9 (calibration) is a placeholder.</p></div>
    <div class="flag"><span class="tag">Scope</span><p>Every experiment is HG002, one chemistry, and the network was trained on it. No second individual, no PacBio HiFi, no downstream demonstration, and no matched comparison against HapCUT2's own confidence pruning yet.</p></div>
    <div class="flag"><span class="tag">Facts</span><p>Versions, accessions, command lines, hardware, seeds, thread count for Fig. 2e, seven cells of Supplementary Table 5, and the data and code deposition statements are the remaining red marks.</p></div>
  </div>

  <h2>Figures</h2>
  {fig_cards(MAIN_FIGS)}

  <h2>Supplementary figures</h2>
  <div class="supp">{fig_cards(SUPP_FIGS)}</div>

  <p class="meta">Page images are rendered at {DPI} dpi for reading here; the PDF buttons open the exact compiled files. Links keep the same addresses across rebuilds. Fig. 1 and the supplementary figures are generated by <code>figures-source/make_fig1.py</code> and <code>figures/supp/make_supp_figs.py</code>; the GNN training chain and <code>longphase compare</code> tables stay outside the repository.</p>
</div>
<script>
(function(){{
  var tabs=[["tab-main","reader-main"],["tab-supp","reader-supp"]];
  tabs.forEach(function(t){{
    document.getElementById(t[0]).addEventListener("click",function(){{
      tabs.forEach(function(u){{
        var sel=u[0]===t[0];
        document.getElementById(u[0]).setAttribute("aria-selected",sel?"true":"false");
        document.getElementById(u[1]).hidden=!sel;
      }});
      try{{localStorage.setItem("longphase2-hub-tab",t[0]);}}catch(e){{}}
    }});
  }});
  try{{var saved=localStorage.getItem("longphase2-hub-tab"); if(saved==="tab-supp"){{document.getElementById("tab-supp").click();}}}}catch(e){{}}
}})();
</script>
"""
    (OUT / "index.html").write_text(html, encoding="utf-8")

    files: dict[str, str | None] = {"main.pdf": "main.pdf", "supplementary.pdf": "supplementary.pdf"}
    for short, _, _, _ in MAIN_FIGS + SUPP_FIGS:
        files[f"figures/{short}.png"] = f"figures/{short}.png"
    removals: dict[str, None] = {}
    for prefix, n in (("main", n_main), ("supp", n_supp)):
        for i in range(1, MAX_PAGES + 1):
            if i <= n:
                files[f"pages/{prefix}-{i:02d}.jpg"] = f"pages/{prefix}-{i:02d}.jpg"
            else:
                removals[f"pages/{prefix}-{i:02d}.jpg"] = None
    # files.json: everything to publish now. files_with_removals.json: the same plus nulls that delete
    # page images left over from a longer earlier build (use it only after listing the artifact's files).
    (OUT / "files.json").write_text(json.dumps(files, indent=1), encoding="utf-8")
    (OUT / "files_with_removals.json").write_text(json.dumps({**files, **removals}, indent=1), encoding="utf-8")
    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"hub-build ready: main {n_main} pp, supp {n_supp} pp, todo {todo}, refs {refs}, commit {commit}{' (dirty)' if dirty else ''}; {total/1e6:.1f} MB")
    print(f"publish: file_path=hub-build/index.html root=hub-build url={ARTIFACT}")
    print("files:", json.dumps(sorted(files), separators=(",", ":")))


if __name__ == "__main__":
    sys.exit(main())
