import React from "react";

// HG002 ONT R10.4.1, replicate 1. Heterozygous SNVs present in both output
// VCFs; "phase" and "gnn" split the LongPhase-only set by the stage that
// dropped the site. Depth histograms use 2x bins; the caller caps depth near
// 125x, so the last bin piles up everything at or above the cap.
// cross: share of each set inside the OTHER tool's switch-error intervals,
// against that tool's genome-wide rate.
const BIN = 2;
const CAP = 124;

const DATA = {
  "10x": {
    venn: { lp: 148573, phase: 125981, gnn: 22592, wh: 37676, both: 90210 },
    cross: [
      { label: "LongPhase only \u2014 phase", set: 9.82,  bg: 2.33, other: "WhatsHap",  color: "#dc2626" },
      { label: "LongPhase only \u2014 gnn",   set: 10.41, bg: 2.33, other: "WhatsHap",  color: "#dc2626" },
      { label: "WhatsHap only",               set: 3.38,  bg: 1.73, other: "LongPhase", color: "#2563eb" },
    ],
    hist: {
      lp: [
        0.00000,0.00361,0.02618,0.07843,0.13251,0.14561,0.11442,0.08404,0.06298,0.04712,0.03700,0.03087,
        0.02558,0.02130,0.01913,0.01930,0.01827,0.01574,0.01187,0.01238,0.01221,0.00894,0.00662,0.00658,
        0.00585,0.00507,0.00370,0.00311,0.00276,0.00244,0.00208,0.00193,0.00195,0.00133,0.00145,0.00145,
        0.00153,0.00208,0.00153,0.00162,0.00172,0.00188,0.00144,0.00139,0.00102,0.00071,0.00061,0.00045,
        0.00035,0.00031,0.00024,0.00037,0.00044,0.00035,0.00034,0.00026,0.00027,0.00033,0.00023,0.00028,
        0.00024,0.00026,0.00596
      ],
      wh: [
        0.00000,0.02336,0.05853,0.07976,0.09629,0.08618,0.08180,0.08135,0.07557,0.05653,0.04780,0.03782,
        0.02965,0.02551,0.02041,0.01842,0.01417,0.01407,0.01423,0.01383,0.01388,0.01202,0.01149,0.00942,
        0.00881,0.00865,0.00661,0.00658,0.00340,0.00305,0.00326,0.00595,0.00406,0.00271,0.00138,0.00236,
        0.00242,0.00143,0.00090,0.00165,0.00146,0.00074,0.00082,0.00090,0.00045,0.00037,0.00042,0.00032,
        0.00040,0.00061,0.00029,0.00040,0.00048,0.00021,0.00029,0.00027,0.00021,0.00011,0.00016,0.00008,
        0.00019,0.00016,0.00533
      ],
      both: [
        0.00000,0.01830,0.06585,0.10994,0.12435,0.11482,0.09363,0.07180,0.06228,0.04625,0.04036,0.03230,
        0.02403,0.01705,0.01805,0.01724,0.01610,0.01510,0.01479,0.01157,0.01021,0.00855,0.00619,0.00571,
        0.00547,0.00550,0.00411,0.00290,0.00280,0.00280,0.00306,0.00296,0.00219,0.00181,0.00142,0.00145,
        0.00181,0.00142,0.00147,0.00133,0.00109,0.00085,0.00083,0.00070,0.00050,0.00050,0.00048,0.00058,
        0.00030,0.00038,0.00039,0.00031,0.00032,0.00027,0.00027,0.00042,0.00025,0.00020,0.00028,0.00027,
        0.00021,0.00019,0.00347
      ],
    },
  },
  "30x": {
    venn: { lp: 132438, phase: 111718, gnn: 20720, wh: 52152, both: 96839 },
    cross: [
      { label: "LongPhase only \u2014 phase", set: 13.44, bg: 1.52, other: "WhatsHap",  color: "#dc2626" },
      { label: "LongPhase only \u2014 gnn",   set: 6.41,  bg: 1.52, other: "WhatsHap",  color: "#dc2626" },
      { label: "WhatsHap only",               set: 3.97,  bg: 0.94, other: "LongPhase", color: "#2563eb" },
    ],
    hist: {
      lp: [
        0.00000,0.00107,0.00526,0.00896,0.01722,0.02001,0.02560,0.02568,0.02843,0.02954,0.03040,0.02613,
        0.02801,0.03073,0.03482,0.03667,0.03661,0.03435,0.03189,0.03175,0.03161,0.02803,0.02440,0.02551,
        0.02392,0.02225,0.02111,0.02068,0.01864,0.01856,0.01934,0.01836,0.01570,0.01436,0.01188,0.01165,
        0.01346,0.01216,0.01068,0.00992,0.00907,0.00840,0.00817,0.00751,0.00754,0.00616,0.00479,0.00430,
        0.00489,0.00448,0.00427,0.00439,0.00464,0.00387,0.00322,0.00316,0.00254,0.00260,0.00239,0.00215,
        0.00175,0.00157,0.04280
      ],
      wh: [
        0.00000,0.01592,0.03538,0.04945,0.06548,0.10531,0.10661,0.08863,0.07702,0.05649,0.04236,0.03486,
        0.03227,0.02452,0.02382,0.01979,0.01772,0.01519,0.01371,0.01254,0.01032,0.01012,0.01103,0.01093,
        0.00846,0.00805,0.00861,0.00784,0.00654,0.00704,0.00606,0.00493,0.00493,0.00408,0.00395,0.00357,
        0.00412,0.00397,0.00453,0.00255,0.00221,0.00196,0.00138,0.00150,0.00109,0.00161,0.00203,0.00127,
        0.00094,0.00092,0.00058,0.00090,0.00079,0.00081,0.00067,0.00090,0.00052,0.00079,0.00061,0.00059,
        0.00063,0.00036,0.00828
      ],
      both: [
        0.00000,0.01083,0.03214,0.05563,0.07424,0.09238,0.09872,0.08465,0.07020,0.06326,0.04486,0.03707,
        0.03344,0.03004,0.02514,0.02327,0.02164,0.01665,0.01608,0.01481,0.01199,0.01161,0.01029,0.00869,
        0.00856,0.00730,0.00664,0.00535,0.00512,0.00508,0.00483,0.00472,0.00474,0.00399,0.00401,0.00341,
        0.00317,0.00336,0.00270,0.00243,0.00230,0.00213,0.00172,0.00169,0.00200,0.00176,0.00131,0.00149,
        0.00146,0.00106,0.00106,0.00103,0.00096,0.00103,0.00101,0.00109,0.00080,0.00080,0.00087,0.00058,
        0.00054,0.00060,0.00971
      ],
    },
  },
  "60x": {
    venn: { lp: 121991, phase: 99813, gnn: 22178, wh: 53621, both: 88692 },
    cross: [
      { label: "LongPhase only \u2014 phase", set: 11.70, bg: 1.12, other: "WhatsHap",  color: "#dc2626" },
      { label: "LongPhase only \u2014 gnn",   set: 6.52,  bg: 1.12, other: "WhatsHap",  color: "#dc2626" },
      { label: "WhatsHap only",               set: 10.10, bg: 1.06, other: "LongPhase", color: "#2563eb" },
    ],
    hist: {
      lp: [
        0.00000,0.00083,0.00362,0.00724,0.01385,0.01537,0.01889,0.02037,0.01960,0.01766,0.01780,0.01575,
        0.01399,0.01349,0.01349,0.01667,0.01788,0.01542,0.01378,0.01350,0.01272,0.01459,0.01448,0.01445,
        0.01612,0.01744,0.02027,0.02111,0.02288,0.02458,0.02494,0.02435,0.02416,0.02329,0.02082,0.02037,
        0.01966,0.01804,0.01622,0.01406,0.01356,0.01218,0.01114,0.01110,0.01112,0.00940,0.00896,0.00904,
        0.00844,0.00761,0.00783,0.00711,0.00634,0.00708,0.00650,0.00761,0.00836,0.00758,0.00789,0.00790,
        0.00693,0.00650,0.15607
      ],
      wh: [
        0.00000,0.01378,0.03292,0.05144,0.05772,0.07616,0.07827,0.08215,0.07303,0.06585,0.04558,0.04280,
        0.04179,0.03189,0.02743,0.02234,0.02488,0.01953,0.01412,0.01276,0.01376,0.01283,0.01195,0.00910,
        0.00893,0.00849,0.00962,0.00886,0.00877,0.00690,0.00731,0.00634,0.00459,0.00479,0.00388,0.00423,
        0.00328,0.00304,0.00304,0.00254,0.00201,0.00265,0.00241,0.00192,0.00188,0.00181,0.00144,0.00144,
        0.00117,0.00106,0.00110,0.00149,0.00116,0.00091,0.00117,0.00075,0.00099,0.00067,0.00093,0.00075,
        0.00039,0.00037,0.01483
      ],
      both: [
        0.00000,0.01213,0.02971,0.04411,0.06365,0.07355,0.06954,0.06806,0.05877,0.05058,0.04447,0.03792,
        0.03541,0.03423,0.03068,0.02751,0.02586,0.02346,0.02081,0.01894,0.01653,0.01500,0.01423,0.01426,
        0.01241,0.01178,0.01054,0.00917,0.00835,0.00785,0.00739,0.00749,0.00634,0.00539,0.00542,0.00454,
        0.00435,0.00483,0.00397,0.00405,0.00309,0.00286,0.00306,0.00240,0.00216,0.00203,0.00152,0.00161,
        0.00168,0.00162,0.00189,0.00136,0.00124,0.00112,0.00113,0.00115,0.00088,0.00074,0.00112,0.00103,
        0.00107,0.00072,0.02123
      ],
    },
  },
};

const COVS = ["10x", "30x", "60x"];
const COLOR = { lp: "#dc2626", wh: "#2563eb", both: "#737373" };
const LABEL = { lp: "LongPhase only", wh: "WhatsHap only", both: "both" };
const ORDER = ["lp", "wh", "both"];
const FONT = "'Libre Franklin','Helvetica Neue',Arial,sans-serif";
const fmt = (n) => n.toLocaleString();

function Venn({ cov }) {
  const v = DATA[cov].venn;
  return (
    <svg width="100%" viewBox="0 0 400 230" style={{ display: "block" }}>
      <circle cx={158} cy={115} r={104} fill="#dc2626" fillOpacity={0.15} stroke="#dc2626" strokeWidth={1.5} />
      <circle cx={256} cy={115} r={82}  fill="#2563eb" fillOpacity={0.15} stroke="#2563eb" strokeWidth={1.5} />

      <text x={112} y={96}  textAnchor="middle" fontSize={11} fill="#171717">Longphase only</text>
      <text x={112} y={118} textAnchor="middle" fontSize={15} fontWeight={700} fill="#171717">{fmt(v.lp)}</text>
      <text x={112} y={136} textAnchor="middle" fontSize={10} fill="#525252">phase: {fmt(v.phase)}</text>
      <text x={112} y={150} textAnchor="middle" fontSize={10} fill="#525252">gnn: {fmt(v.gnn)}</text>

      <text x={212} y={108} textAnchor="middle" fontSize={11} fill="#171717">both</text>
      <text x={212} y={128} textAnchor="middle" fontSize={13} fontWeight={700} fill="#171717">{fmt(v.both)}</text>

      <text x={288} y={108} textAnchor="middle" fontSize={11} fill="#171717">WhatsHap only</text>
      <text x={288} y={128} textAnchor="middle" fontSize={15} fontWeight={700} fill="#171717">{fmt(v.wh)}</text>
    </svg>
  );
}

function Density({ cov }) {
  const H_ = DATA[cov].hist;
  const W = 360, H = 200, L = 44, B = 40, T = 10, R = 10;
  const pw = W - L - R, ph = H - T - B;
  const nb = Math.max(...ORDER.map((k) => H_[k].length), 1);
  const maxY = Math.max(...ORDER.flatMap((k) => H_[k]), 0.001);
  const x = (i) => L + (i / (nb - 1 || 1)) * pw;
  const y = (val) => T + (1 - val / maxY) * ph;
  const path = (a) => a.map((val, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(val).toFixed(1)}`).join("");
  const empty = ORDER.every((k) => H_[k].length === 0);

  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{ display: "block" }}>
      {[0, 0.25, 0.5, 0.75, 1].map((f) => (
        <line key={f} x1={L} y1={T + f * ph} x2={L + pw} y2={T + f * ph} stroke="#f0f0f0" strokeWidth={1} />
      ))}
      {[0, 40, 80, 120].map((d) => (
        <text key={d} x={x(d / BIN)} y={H - B + 15} textAnchor="middle" fontSize={9.5} fill="#525252">{d}</text>
      ))}
      {!empty && (
        <text x={x(CAP / BIN)} y={H - B + 27} textAnchor="end" fontSize={9} fill="#a3a3a3">depth cap</text>
      )}

      {!empty && ORDER.map((k) => (
        <g key={k}>
          <path d={`${path(H_[k])}L${x(H_[k].length - 1)},${y(0)}L${x(0)},${y(0)}Z`}
                fill={COLOR[k]} fillOpacity={0.12} />
          <path d={path(H_[k])} fill="none" stroke={COLOR[k]} strokeWidth={1.7} />
        </g>
      ))}
      {empty && (
        <text x={L + pw / 2} y={T + ph / 2} textAnchor="middle" fontSize={10.5} fill="#a3a3a3">
          run run_coverage.sh {cov}
        </text>
      )}

      <line x1={L} y1={T + ph} x2={L + pw} y2={T + ph} stroke="#a3a3a3" strokeWidth={0.9} />
      <line x1={L} y1={T} x2={L} y2={T + ph} stroke="#a3a3a3" strokeWidth={0.9} />
      <text x={L + pw / 2} y={H - 4} textAnchor="middle" fontSize={10.5} fill="#171717">read depth</text>
      <text x={12} y={T + ph / 2} textAnchor="middle" fontSize={10.5} fill="#171717"
            transform={`rotate(-90 12 ${T + ph / 2})`}>density</text>
    </svg>
  );
}

function Cross({ cov }) {
  const rowsData = DATA[cov].cross;
  const W = 340, H = 150, L = 118, R = 38, T = 12, B = 32;
  const pw = W - L - R, rows = rowsData.length, band = (H - T - B) / rows;
  const maxX = Math.max(14, ...rowsData.map((d) => d.set * 1.15));
  const x = (v) => L + (v / maxX) * pw;

  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{ display: "block" }}>
      {[0, 5, 10, 15].filter((v) => v <= maxX).map((v) => (
        <g key={v}>
          <line x1={x(v)} y1={T} x2={x(v)} y2={T + rows * band} stroke="#f0f0f0" strokeWidth={1} />
          <text x={x(v)} y={H - B + 15} textAnchor="middle" fontSize={9.5} fill="#525252">{v}%</text>
        </g>
      ))}
      {rowsData.map((d, i) => {
        const yc = T + i * band + band / 2;
        const fold = d.bg > 0 ? (d.set / d.bg).toFixed(1) : "–";
        return (
          <g key={d.label}>
            <text x={L - 7} y={yc - 3} textAnchor="end" fontSize={10} fill="#171717">{d.label}</text>
            <text x={L - 7} y={yc + 9} textAnchor="end" fontSize={8.5} fill="#a3a3a3">vs {d.other} background</text>
            <rect x={L} y={yc - 12} width={Math.max(x(d.set) - L, 0)} height={11} fill={d.color} fillOpacity={0.85} />
            <rect x={L} y={yc + 2}  width={Math.max(x(d.bg) - L, 1)}  height={6}  fill="#d4d4d4" />
            <text x={x(d.set) + 4} y={yc - 3} fontSize={10.5} fontWeight={700} fill={d.color}>{fold}&times;</text>
          </g>
        );
      })}
      <line x1={L} y1={T + rows * band} x2={L + pw} y2={T + rows * band} stroke="#a3a3a3" strokeWidth={0.9} />
      <line x1={L} y1={T} x2={L} y2={T + rows * band} stroke="#a3a3a3" strokeWidth={0.9} />
      <text x={L + pw / 2} y={H - 3} textAnchor="middle" fontSize={10} fill="#171717">
        inside the other tool&apos;s switch errors
      </text>
    </svg>
  );
}

function Panel({ title, render, legend }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ fontSize: 13.5, fontWeight: 700, color: "#0a0a0a", marginBottom: 2 }}>{title}</div>
      <div style={{ display: "grid", gridTemplateColumns: `repeat(${COVS.length}, 1fr)`, gap: 8 }}>
        {COVS.map((c) => (
          <div key={c}>
            <div style={{ textAlign: "center", fontSize: 11, fontWeight: 600, color: "#525252" }}>{c}</div>
            {render(c)}
          </div>
        ))}
      </div>
      {legend}
    </div>
  );
}

export default function UnphaseVenn() {
  const legendLines = (
    <div style={{ display: "flex", justifyContent: "center", gap: 20, flexWrap: "wrap",
      fontSize: 11, color: "#404040", marginTop: 2 }}>
      {ORDER.map((k) => (
        <span key={k} style={{ display: "flex", alignItems: "center", gap: 5 }}>
          <span style={{ width: 14, height: 3, background: COLOR[k], display: "inline-block" }} />
          {LABEL[k]}
        </span>
      ))}
    </div>
  );
  const legendCross = (
    <div style={{ display: "flex", justifyContent: "center", gap: 20, flexWrap: "wrap",
      fontSize: 11, color: "#404040", marginTop: 2 }}>
      <span style={{ display: "flex", alignItems: "center", gap: 5 }}>
        <span style={{ width: 14, height: 8, background: "#9ca3af", display: "inline-block" }} />
        the give-up set
      </span>
      <span style={{ display: "flex", alignItems: "center", gap: 5 }}>
        <span style={{ width: 14, height: 5, background: "#d4d4d4", display: "inline-block" }} />
        that tool&apos;s genome-wide rate
      </span>
    </div>
  );

  return (
    <div style={{ fontFamily: FONT, background: "#fff", padding: "18px 20px", maxWidth: 980, margin: "0 auto" }}>
      <link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <Panel title="A. Heterozygous SNVs left unphased by LongPhase and WhatsHap" render={(c) => <Venn cov={c} />} />
      <Panel title="B. Read depth of the sites each tool gives up" render={(c) => <Density cov={c} />} legend={legendLines} />
      <Panel title="C. Where one tool gives up, does the other get it right?" render={(c) => <Cross cov={c} />} legend={legendCross} />
    </div>
  );
}
