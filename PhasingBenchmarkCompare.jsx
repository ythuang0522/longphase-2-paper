import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ReferenceLine, ReferenceDot, ResponsiveContainer,
} from "recharts";

// HG002 ONT R10.4.1. 10-20x are means of 10 replicates; 30-60x are single runs.
// Switch errors and phased SNVs are counts; phased SNV and Block N50 are
// taken from the v5.0q report.
const data = [
  { cov: 10, lp_sw50: 1518, lp_indel_sw50: 1704, lp_sv_sw50: 1711, wh_snv_sw50: 4383, wh_sw50: 5174, hc2_sw50: 5018, lp_ham50: 5.3269, lp_indel_ham50: 6.8463, lp_sv_ham50: 6.855, wh_snv_ham50: 7.6036, wh_ham50: 12.1595, hc2_ham50: 7.772, lp_sw42: 1820, lp_indel_sw42: 1972, lp_sv_sw42: 1977, wh_snv_sw42: 2773, wh_sw42: 3538, hc2_sw42: 3050, lp_ham42: 5.2965, lp_indel_ham42: 6.802, lp_sv_ham42: 6.8137, wh_snv_ham42: 7.4417, wh_ham42: 12.0044, hc2_ham42: 7.5926, lp_psnv: 1867140, lp_indel_psnv: 1865390, lp_sv_psnv: 1865322, wh_snv_psnv: 1888779, wh_psnv: 1888961, hc2_psnv: 1889811, lp_n50: 0.8417, lp_indel_n50: 0.9679, lp_sv_n50: 0.9757, wh_snv_n50: 0.945, wh_n50: 1.2415, hc2_n50: 0.9537 },
  { cov: 12, lp_sw50: 1335, lp_indel_sw50: 1501, lp_sv_sw50: 1510, wh_snv_sw50: 4229, wh_sw50: 4976, hc2_sw50: 4948, lp_ham50: 5.4089, lp_indel_ham50: 7.0303, lp_sv_ham50: 7.0818, wh_snv_ham50: 7.9899, wh_ham50: 13.4156, hc2_ham50: 8.0648, lp_sw42: 1804, lp_indel_sw42: 1925, lp_sv_sw42: 1929, wh_snv_sw42: 2590, wh_sw42: 3321, hc2_sw42: 2941, lp_ham42: 5.366, lp_indel_ham42: 7.0248, lp_sv_ham42: 7.0727, wh_snv_ham42: 7.8008, wh_ham42: 13.2648, hc2_ham42: 7.9021, lp_psnv: 2026576, lp_indel_psnv: 2024739, lp_sv_psnv: 2024600, wh_snv_psnv: 2047490, wh_psnv: 2047662, hc2_psnv: 2048860, lp_n50: 1.1041, lp_indel_n50: 1.2973, lp_sv_n50: 1.3001, wh_snv_n50: 1.2366, wh_n50: 1.7139, hc2_n50: 1.2495 },
  { cov: 14, lp_sw50: 1137, lp_indel_sw50: 1284, lp_sv_sw50: 1286, wh_snv_sw50: 3848, wh_sw50: 4590, hc2_sw50: 4652, lp_ham50: 4.885, lp_indel_ham50: 6.7346, lp_sv_ham50: 6.8663, wh_snv_ham50: 7.0128, wh_ham50: 13.297, hc2_ham50: 7.1013, lp_sw42: 1732, lp_indel_sw42: 1848, lp_sv_sw42: 1852, wh_snv_sw42: 2356, wh_sw42: 3060, hc2_sw42: 2721, lp_ham42: 4.8717, lp_indel_ham42: 6.7354, lp_sv_ham42: 6.8606, wh_snv_ham42: 6.8376, wh_ham42: 13.2046, hc2_ham42: 6.9333, lp_psnv: 2107989, lp_indel_psnv: 2106188, lp_sv_psnv: 2106051, wh_snv_psnv: 2127931, wh_psnv: 2128116, hc2_psnv: 2129334, lp_n50: 1.2899, lp_indel_n50: 1.5416, lp_sv_n50: 1.5485, wh_snv_n50: 1.4132, wh_n50: 2.06, hc2_n50: 1.4368 },
  { cov: 16, lp_sw50: 1011, lp_indel_sw50: 1167, lp_sv_sw50: 1173, wh_snv_sw50: 3561, wh_sw50: 4196, hc2_sw50: 4344, lp_ham50: 4.1973, lp_indel_ham50: 6.3768, lp_sv_ham50: 6.3804, wh_snv_ham50: 6.3691, wh_ham50: 12.9717, hc2_ham50: 6.1307, lp_sw42: 1699, lp_indel_sw42: 1827, lp_sv_sw42: 1834, wh_snv_sw42: 2190, wh_sw42: 2826, hc2_sw42: 2559, lp_ham42: 4.144, lp_indel_ham42: 6.3221, lp_sv_ham42: 6.3379, wh_snv_ham42: 6.1709, wh_ham42: 12.8493, hc2_ham42: 5.9384, lp_psnv: 2148971, lp_indel_psnv: 2147311, lp_sv_psnv: 2147173, wh_snv_psnv: 2167873, wh_psnv: 2168026, hc2_psnv: 2169516, lp_n50: 1.4384, lp_indel_n50: 1.7161, lp_sv_n50: 1.7262, wh_snv_n50: 1.5279, wh_n50: 2.2509, hc2_n50: 1.5424 },
  { cov: 18, lp_sw50: 918, lp_indel_sw50: 1087, lp_sv_sw50: 1091, wh_snv_sw50: 3291, wh_sw50: 3916, hc2_sw50: 4068, lp_ham50: 3.6381, lp_indel_ham50: 5.82, lp_sv_ham50: 5.9506, wh_snv_ham50: 5.228, wh_ham50: 11.8665, hc2_ham50: 5.3154, lp_sw42: 1671, lp_indel_sw42: 1814, lp_sv_sw42: 1818, wh_snv_sw42: 2073, wh_sw42: 2680, hc2_sw42: 2434, lp_ham42: 3.5845, lp_indel_ham42: 5.7958, lp_sv_ham42: 5.9095, wh_snv_ham42: 5.0399, wh_ham42: 11.7442, hc2_ham42: 5.1184, lp_psnv: 2171006, lp_indel_psnv: 2169604, lp_sv_psnv: 2169505, wh_snv_psnv: 2189349, wh_psnv: 2189536, hc2_psnv: 2190627, lp_n50: 1.532, lp_indel_n50: 1.8633, lp_sv_n50: 1.8752, wh_snv_n50: 1.5984, wh_n50: 2.402, hc2_n50: 1.6102 },
  { cov: 20, lp_sw50: 823, lp_indel_sw50: 996, lp_sv_sw50: 1001, wh_snv_sw50: 3067, wh_sw50: 3683, hc2_sw50: 3825, lp_ham50: 3.2075, lp_indel_ham50: 5.7753, lp_sv_ham50: 6.0583, wh_snv_ham50: 4.3969, wh_ham50: 11.449, hc2_ham50: 4.2654, lp_sw42: 1656, lp_indel_sw42: 1807, lp_sv_sw42: 1806, wh_snv_sw42: 1972, wh_sw42: 2580, hc2_sw42: 2346, lp_ham42: 3.1225, lp_indel_ham42: 5.7543, lp_sv_ham42: 6.0403, wh_snv_ham42: 4.2148, wh_ham42: 11.3426, hc2_ham42: 4.0931, lp_psnv: 2181624, lp_indel_psnv: 2180269, lp_sv_psnv: 2180166, wh_snv_psnv: 2199412, wh_psnv: 2199575, hc2_psnv: 2199832, lp_n50: 1.6117, lp_indel_n50: 2.0058, lp_sv_n50: 2.0352, wh_snv_n50: 1.6532, wh_n50: 2.4878, hc2_n50: 1.6639 },
  { cov: 30, lp_sw50: 680, lp_indel_sw50: 822, lp_sv_sw50: 838, wh_snv_sw50: 2524, wh_sw50: 3027, hc2_sw50: 3280, lp_ham50: 1.8226, lp_indel_ham50: 4.8583, lp_sv_ham50: 5.0689, wh_snv_ham50: 2.5556, wh_ham50: 9.7071, hc2_ham50: 2.6071, lp_sw42: 1635, lp_indel_sw42: 1777, lp_sv_sw42: 1778, wh_snv_sw42: 1850, wh_sw42: 2345, hc2_sw42: 2202, lp_ham42: 1.7992, lp_indel_ham42: 4.7248, lp_sv_ham42: 4.9848, wh_snv_ham42: 2.4456, wh_ham42: 9.6739, hc2_ham42: 2.4607, lp_psnv: 2194861, lp_indel_psnv: 2194079, lp_sv_psnv: 2193958, wh_snv_psnv: 2213304, wh_psnv: 2213472, hc2_psnv: 2213483, lp_n50: 1.9201, lp_indel_n50: 2.4445, lp_sv_n50: 2.4211, wh_snv_n50: 1.8769, wh_n50: 2.9802, hc2_n50: 1.8869 },
  { cov: 40, lp_sw50: 602, lp_indel_sw50: 724, lp_sv_sw50: 739, wh_snv_sw50: 2139, wh_sw50: 2572, hc2_sw50: 2916, lp_ham50: 1.7125, lp_indel_ham50: 4.3684, lp_sv_ham50: 4.3788, wh_snv_ham50: 3.0464, wh_ham50: 10.4029, hc2_ham50: 2.8984, lp_sw42: 1663, lp_indel_sw42: 1758, lp_sv_sw42: 1767, wh_snv_sw42: 1810, wh_sw42: 2221, hc2_sw42: 2171, lp_ham42: 1.6374, lp_indel_ham42: 4.2246, lp_sv_ham42: 4.1987, wh_snv_ham42: 2.919, wh_ham42: 10.4281, hc2_ham42: 2.7184, lp_psnv: 2196032, lp_indel_psnv: 2195030, lp_sv_psnv: 2194953, wh_snv_psnv: 2215519, wh_psnv: 2215645, hc2_psnv: 2215745, lp_n50: 2.1776, lp_indel_n50: 2.8646, lp_sv_n50: 2.9786, wh_snv_n50: 2.1509, wh_n50: 3.3907, hc2_n50: 2.164 },
  { cov: 50, lp_sw50: 588, lp_indel_sw50: 664, lp_sv_sw50: 673, wh_snv_sw50: 2010, wh_sw50: 2346, hc2_sw50: 2568, lp_ham50: 1.4808, lp_indel_ham50: 3.257, lp_sv_ham50: 3.3856, wh_snv_ham50: 2.3996, wh_ham50: 8.4587, hc2_ham50: 2.1974, lp_sw42: 1669, lp_indel_sw42: 1752, lp_sv_sw42: 1760, wh_snv_sw42: 1811, wh_sw42: 2171, hc2_sw42: 2133, lp_ham42: 1.4264, lp_indel_ham42: 3.1338, lp_sv_ham42: 3.2868, wh_snv_ham42: 2.2316, wh_ham42: 8.3245, hc2_ham42: 2.0336, lp_psnv: 2193915, lp_indel_psnv: 2192843, lp_sv_psnv: 2192667, wh_snv_psnv: 2215890, wh_psnv: 2216012, hc2_psnv: 2216082, lp_n50: 2.5129, lp_indel_n50: 3.1894, lp_sv_n50: 3.2168, wh_snv_n50: 2.4715, wh_n50: 3.6772, hc2_n50: 2.4615 },
  { cov: 60, lp_sw50: 496, lp_indel_sw50: 591, lp_sv_sw50: 592, wh_snv_sw50: 1785, wh_sw50: 2139, hc2_sw50: 2309, lp_ham50: 1.5344, lp_indel_ham50: 3.4613, lp_sv_ham50: 3.4578, wh_snv_ham50: 2.7496, wh_ham50: 9.2926, hc2_ham50: 2.1106, lp_sw42: 1676, lp_indel_sw42: 1765, lp_sv_sw42: 1772, wh_snv_sw42: 1801, wh_sw42: 2156, hc2_sw42: 2088, lp_ham42: 1.5368, lp_indel_ham42: 3.5264, lp_sv_ham42: 3.5016, wh_snv_ham42: 2.6087, wh_ham42: 9.1981, hc2_ham42: 2.0153, lp_psnv: 2191311, lp_indel_psnv: 2190434, lp_sv_psnv: 2190396, wh_snv_psnv: 2215068, wh_psnv: 2215208, hc2_psnv: 2215228, lp_n50: 2.8641, lp_indel_n50: 3.6938, lp_sv_n50: 3.7031, wh_snv_n50: 2.725, wh_n50: 4.196, hc2_n50: 2.725 },
];

const SERIES = [
  { key: "lp",       name: "longphase v2.1",                        color: "#dc2626", dash: "2 5"  },
  { key: "lp_indel", name: "longphase v2.1 (--indels)",             color: "#eab308", dash: "6 4"  },
  { key: "lp_sv",    name: "longphase v2.1 (--indels + --sv-file)", color: "#f97316", dash: "12 4" },
  { key: "wh_snv",   name: "whatshap v2.8 (--only-snvs)",           color: "#2563eb", dash: "2 5"  },
  { key: "wh",       name: "whatshap v2.8",                         color: "#93c5fd", dash: "6 4"  },
  { key: "hc2",      name: "hapcut2 v1.3.4",                        color: "#16a34a", dash: "12 4" },
];

const PANELS = [
  { title: "A. v5.0q  Switch errors",         suffix: "sw50",  unit: "",   fmt: (v) => v.toLocaleString() },
  { title: "C. v4.2.1  Switch errors",        suffix: "sw42",  unit: "",   fmt: (v) => v.toLocaleString() },
  { title: "E. Phased SNV",                   suffix: "psnv",  unit: "M",  fmt: (v) => v.toLocaleString(), domain: [1850000, 2250000], ticks: [1850000, 1950000, 2050000, 2150000, 2250000], dashed: true, callout: true },
  { title: "B. v5.0q  Hamming Distance (%)",  suffix: "ham50", unit: "%",  fmt: (v) => v.toFixed(2) },
  { title: "D. v4.2.1  Hamming Distance (%)", suffix: "ham42", unit: "%",  fmt: (v) => v.toFixed(2) },
  { title: "F. Block N50",                    suffix: "n50",   unit: "Mb", fmt: (v) => v.toFixed(2), domain: [0, 5], ticks: [0, 1, 2, 3, 4, 5] },
];

// Label for the leader line: anchored at its end and drawn leftwards so the
// text stays inside the panel.
function CalloutLabel({ viewBox, text }) {
  const { x, y } = viewBox;
  return (
    <text x={x + 5} y={y + 15} textAnchor="end" fontSize={11} fill="#374151">
      {text}
    </text>
  );
}

// 10x-20x ticks sit close together, so alternate them between two rows.
function StaggeredTick({ x, y, payload }) {
  const v = payload.value;
  const dy = v <= 20 && ((v - 10) / 2) % 2 === 1 ? 26 : 12;
  return (
    <text x={x} y={y + dy} textAnchor="middle" fontSize={11} fill="#374151">
      {`${v}x`}
    </text>
  );
}

function Panel({ title, suffix, unit, fmt, domain, ticks, dashed, callout }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: 275 }}>
      <div style={{ textAlign: "center", fontSize: 14, fontWeight: 600, color: "#111827", marginBottom: 6 }}>
        {title}
      </div>
      <div style={{ flex: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 4, right: 12, bottom: 30, left: 4 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="cov"
              type="number"
              domain={[10, 60]}
              ticks={[10, 12, 14, 16, 18, 20, 30, 40, 50, 60]}
              interval={0}
              tick={<StaggeredTick />}
              height={40}
              label={{ value: "Coverage", position: "insideBottom", offset: -4, fontSize: 12, fill: "#374151" }}
            />
            <YAxis
              tick={{ fontSize: 11, fill: "#374151" }}
              width={58}
              domain={domain || ["auto", "auto"]}
              ticks={ticks}
              allowDecimals={unit === "Mb"}
              tickFormatter={(v) =>
                unit === "Mb"
                  ? v.toFixed(0)
                  : unit === "M"
                  ? `${(v / 1e6).toFixed(2)}M`
                  : unit === "%"
                  ? v.toFixed(0)
                  : v >= 1000
                  ? `${(v / 1000).toFixed(0)}k`
                  : v.toFixed(0)
              }
              label={{ value: unit === "Mb" ? "Mb" : unit === "%" ? "%" : unit === "M" ? "M" : "count", angle: -90, position: "insideLeft", offset: 8, fontSize: 12, fill: "#374151" }}
            />
            <Tooltip
              formatter={(value, name) => [unit && unit !== "M" ? `${fmt(value)} ${unit}` : fmt(value), name]}
              labelFormatter={(v) => `${v}x coverage`}
              contentStyle={{ fontSize: 12, borderRadius: 6, border: "1px solid #d1d5db" }}
            />
            {callout && (
              <ReferenceLine
                segment={[{ x: 45, y: 2215000 }, { x: 47, y: 2120000 }]}
                stroke="#6b7280"
                strokeWidth={1}
                ifOverflow="visible"
              />
            )}
            {callout && (
              <ReferenceDot
                x={47}
                y={2120000}
                r={0}
                ifOverflow="visible"
                label={{ value: "whatshap and hapcut2", position: "bottom", fontSize: 11, fill: "#374151" }}
              />
            )}
            {callout && (
              <ReferenceLine
                segment={[{ x: 25, y: 2188000 }, { x: 27, y: 2095000 }]}
                stroke="#6b7280"
                strokeWidth={1}
                ifOverflow="visible"
              />
            )}
            {callout && (
              <ReferenceDot
                x={27}
                y={2095000}
                r={0}
                ifOverflow="visible"
                label={{ value: "longphase", position: "bottom", fontSize: 11, fill: "#374151" }}
              />
            )}
            {SERIES.map((s) => (
              <Line
                key={s.key}
                type="linear"
                dataKey={`${s.key}_${suffix}`}
                name={s.name}
                stroke={s.color}
                strokeWidth={2}
                strokeDasharray={dashed ? s.dash : undefined}
                dot={{ r: 3, fill: s.color, strokeWidth: 0 }}
                activeDot={{ r: 5 }}
                isAnimationActive={false}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default function PhasingBenchmarkCompare() {
  return (
    <div style={{ width: "100%", background: "#ffffff", padding: "20px 24px", fontFamily: "Helvetica, Arial, sans-serif" }}>
      <div style={{ textAlign: "center", fontSize: 19, fontWeight: 700, color: "#111827", marginBottom: 12 }}>
        Phasing tool Comparison under two GIAB benchmarks
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "10px 22px", marginBottom: 18 }}>
        {SERIES.map((s) => (
          <div key={s.key} style={{ display: "flex", alignItems: "center", gap: 7 }}>
            <span style={{ width: 22, height: 3, background: s.color, borderRadius: 2 }} />
            <span style={{ fontSize: 12.5, color: "#111827" }}>{s.name}</span>
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "20px 18px" }}>
        {PANELS.map((p) => (
          <Panel key={p.suffix} {...p} />
        ))}
      </div>
    </div>
  );
}
