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
    venn: { lp: 150889, phase: 125981, gnn: 24908, wh: 34359, both: 93527 },
    cross: [
      { label: "LongPhase only \u2014 phase", set: 9.82,  bg: 2.33, other: "WhatsHap",  color: "#dc2626" },
      { label: "LongPhase only \u2014 gnn",   set: 11.09, bg: 2.33, other: "WhatsHap",  color: "#dc2626" },
      { label: "WhatsHap only",               set: 3.74,  bg: 1.59, other: "LongPhase", color: "#2563eb" },
    ],
    hist: {
      lp: [
        0.00000,0.00376,0.02604,0.07816,0.13231,0.14507,0.11446,0.08402,0.06326,0.04741,0.03726,0.03120,
        0.02594,0.02137,0.01935,0.01921,0.01789,0.01549,0.01186,0.01221,0.01219,0.00887,0.00655,0.00648,
        0.00577,0.00517,0.00372,0.00319,0.00284,0.00254,0.00205,0.00192,0.00195,0.00135,0.00146,0.00145,
        0.00155,0.00210,0.00152,0.00161,0.00171,0.00187,0.00142,0.00139,0.00103,0.00080,0.00058,0.00044,
        0.00034,0.00030,0.00025,0.00037,0.00043,0.00034,0.00035,0.00027,0.00027,0.00032,0.00023,0.00028,
        0.00024,0.00027,0.00594
      ],
      wh: [
        0.00000,0.01839,0.05376,0.07314,0.08851,0.08079,0.07835,0.08455,0.08135,0.06071,0.05035,0.03917,
        0.03149,0.02596,0.02165,0.01976,0.01531,0.01490,0.01522,0.01484,0.01493,0.01263,0.01275,0.01007,
        0.00949,0.00905,0.00710,0.00687,0.00341,0.00309,0.00346,0.00640,0.00460,0.00297,0.00148,0.00253,
        0.00256,0.00154,0.00087,0.00180,0.00160,0.00081,0.00090,0.00093,0.00038,0.00038,0.00041,0.00026,
        0.00044,0.00067,0.00029,0.00044,0.00052,0.00020,0.00026,0.00017,0.00017,0.00012,0.00017,0.00009,
        0.00020,0.00017,0.00457
      ],
      both: [
        0.00000,0.02030,0.06734,0.11130,0.12622,0.11578,0.09448,0.07096,0.06062,0.04508,0.03969,0.03200,
        0.02355,0.01718,0.01767,0.01679,0.01561,0.01476,0.01440,0.01128,0.00995,0.00845,0.00591,0.00560,
        0.00534,0.00546,0.00402,0.00293,0.00282,0.00280,0.00299,0.00290,0.00206,0.00174,0.00138,0.00142,
        0.00177,0.00138,0.00146,0.00128,0.00105,0.00082,0.00080,0.00069,0.00052,0.00049,0.00048,0.00059,
        0.00029,0.00036,0.00038,0.00030,0.00031,0.00027,0.00028,0.00045,0.00027,0.00019,0.00027,0.00026,
        0.00020,0.00018,0.00382
      ],
    },
  },
  "30x": {
    venn: { lp: 134583, phase: 111718, gnn: 22865, wh: 47788, both: 101203 },
    cross: [
      { label: "LongPhase only \u2014 phase", set: 13.44, bg: 1.52, other: "WhatsHap",  color: "#dc2626" },
      { label: "LongPhase only \u2014 gnn",   set: 6.67,  bg: 1.52, other: "WhatsHap",  color: "#dc2626" },
      { label: "WhatsHap only",               set: 3.77,  bg: 0.93, other: "LongPhase", color: "#2563eb" },
    ],
    hist: {
      lp: [
        0.00000,0.00114,0.00557,0.00964,0.01802,0.02078,0.02671,0.02636,0.02877,0.03001,0.03072,0.02655,
        0.02836,0.03050,0.03448,0.03654,0.03642,0.03399,0.03167,0.03144,0.03148,0.02782,0.02410,0.02514,
        0.02360,0.02185,0.02079,0.02045,0.01842,0.01839,0.01907,0.01826,0.01567,0.01425,0.01204,0.01152,
        0.01343,0.01203,0.01055,0.00985,0.00899,0.00834,0.00805,0.00747,0.00743,0.00614,0.00477,0.00431,
        0.00490,0.00443,0.00425,0.00438,0.00463,0.00386,0.00317,0.00317,0.00255,0.00256,0.00233,0.00212,
        0.00173,0.00151,0.04255
      ],
      wh: [
        0.00000,0.01440,0.03258,0.04558,0.05845,0.10275,0.10944,0.09117,0.07946,0.05663,0.04237,0.03472,
        0.03346,0.02526,0.02499,0.02065,0.01818,0.01525,0.01366,0.01197,0.01000,0.01057,0.01101,0.01145,
        0.00885,0.00837,0.00931,0.00835,0.00691,0.00743,0.00634,0.00525,0.00525,0.00435,0.00425,0.00370,
        0.00414,0.00421,0.00475,0.00266,0.00222,0.00209,0.00146,0.00161,0.00111,0.00167,0.00222,0.00138,
        0.00103,0.00092,0.00052,0.00088,0.00080,0.00086,0.00073,0.00094,0.00054,0.00080,0.00065,0.00061,
        0.00063,0.00040,0.00783
      ],
      both: [
        0.00000,0.01177,0.03360,0.05719,0.07718,0.09415,0.09772,0.08361,0.06935,0.06290,0.04474,0.03704,
        0.03283,0.02946,0.02453,0.02271,0.02125,0.01655,0.01600,0.01498,0.01206,0.01133,0.01033,0.00855,
        0.00837,0.00718,0.00639,0.00522,0.00501,0.00498,0.00475,0.00457,0.00459,0.00386,0.00386,0.00335,
        0.00320,0.00327,0.00267,0.00238,0.00229,0.00206,0.00167,0.00163,0.00196,0.00172,0.00125,0.00142,
        0.00139,0.00106,0.00107,0.00104,0.00095,0.00100,0.00097,0.00107,0.00077,0.00079,0.00084,0.00057,
        0.00054,0.00057,0.00986
      ],
    },
  },
  "60x": {
    venn: { lp: 124038, phase: 99813, gnn: 24225, wh: 49514, both: 92799 },
    cross: [
      { label: "LongPhase only \u2014 phase", set: 11.70, bg: 1.12, other: "WhatsHap",  color: "#dc2626" },
      { label: "LongPhase only \u2014 gnn",   set: 6.11,  bg: 1.12, other: "WhatsHap",  color: "#dc2626" },
      { label: "WhatsHap only",               set: 10.48, bg: 1.06, other: "LongPhase", color: "#2563eb" },
    ],
    hist: {
      lp: [
        0.00000,0.00101,0.00410,0.00797,0.01507,0.01670,0.01976,0.02149,0.01999,0.01758,0.01824,0.01597,
        0.01392,0.01346,0.01359,0.01674,0.01818,0.01543,0.01429,0.01362,0.01278,0.01479,0.01451,0.01441,
        0.01602,0.01731,0.02014,0.02094,0.02269,0.02417,0.02461,0.02392,0.02366,0.02285,0.02054,0.02011,
        0.01922,0.01776,0.01594,0.01376,0.01337,0.01213,0.01105,0.01100,0.01089,0.00923,0.00888,0.00889,
        0.00832,0.00763,0.00774,0.00701,0.00626,0.00698,0.00639,0.00756,0.00820,0.00750,0.00784,0.00780,
        0.00684,0.00647,0.15478
      ],
      wh: [
        0.00000,0.01184,0.02680,0.04671,0.05354,0.07119,0.07541,0.08268,0.07529,0.06883,0.04724,0.04449,
        0.04389,0.03294,0.02872,0.02385,0.02549,0.01997,0.01448,0.01315,0.01396,0.01317,0.01260,0.00933,
        0.00959,0.00866,0.00990,0.00933,0.00939,0.00727,0.00778,0.00677,0.00487,0.00495,0.00408,0.00444,
        0.00345,0.00309,0.00317,0.00273,0.00202,0.00261,0.00248,0.00204,0.00200,0.00194,0.00149,0.00149,
        0.00123,0.00109,0.00119,0.00156,0.00123,0.00095,0.00127,0.00081,0.00107,0.00073,0.00097,0.00085,
        0.00042,0.00034,0.01517
      ],
      both: [
        0.00000,0.01324,0.03311,0.04695,0.06561,0.07632,0.07146,0.06840,0.05819,0.04967,0.04363,0.03723,
        0.03458,0.03357,0.02985,0.02648,0.02550,0.02305,0.02032,0.01846,0.01630,0.01472,0.01378,0.01391,
        0.01191,0.01154,0.01036,0.00890,0.00804,0.00761,0.00713,0.00721,0.00611,0.00528,0.00525,0.00442,
        0.00421,0.00472,0.00386,0.00388,0.00304,0.00288,0.00298,0.00232,0.00209,0.00195,0.00149,0.00157,
        0.00163,0.00158,0.00181,0.00134,0.00120,0.00109,0.00108,0.00110,0.00084,0.00071,0.00109,0.00096,
        0.00102,0.00072,0.02077
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
  const W = 340, H = 150, L = 130, R = 38, T = 12, B = 32;   // L fits "LongPhase only — phase"
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
