import React from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

// HG002 ONT R10.4.1, GIAB v5.0q. 10x and 20x are means of 10 replicates;
// 30x-60x are single runs. All longphase runs include GNN correction.
const data = [
  { cov: "10x", lp_sw: 0.08156, lp_ham: 5.3269, lp_n50: 0.8417, lp_indel_sw: 0.09164, lp_indel_ham: 6.8463, lp_indel_n50: 0.9679, lp_sv_sw: 0.0828, lp_sv_ham: 5.4521, lp_sv_n50: 0.849, lp_indel_sv_sw: 0.092, lp_indel_sv_ham: 6.855, lp_indel_sv_n50: 0.9757, wh_snv_sw: 0.23273, wh_snv_ham: 7.6036, wh_snv_n50: 0.945, wh_sw: 0.27448, wh_ham: 12.1595, wh_n50: 1.2415 },
  { cov: "20x", lp_sw: 0.03778, lp_ham: 3.2075, lp_n50: 1.6117, lp_indel_sw: 0.04576, lp_indel_ham: 5.7753, lp_indel_n50: 2.0058, lp_sv_sw: 0.03866, lp_sv_ham: 3.5163, lp_sv_n50: 1.6321, lp_indel_sv_sw: 0.04598, lp_indel_sv_ham: 6.0583, lp_indel_sv_n50: 2.0352, wh_snv_sw: 0.13964, wh_snv_ham: 4.3969, wh_snv_n50: 1.6532, wh_sw: 0.1676, wh_ham: 11.449, wh_n50: 2.4878 },
  { cov: "30x", lp_sw: 0.03102, lp_ham: 1.8226, lp_n50: 1.9201, lp_indel_sw: 0.0375, lp_indel_ham: 4.8583, lp_indel_n50: 2.4445, lp_sv_sw: 0.03221, lp_sv_ham: 1.9649, lp_sv_n50: 1.9269, lp_indel_sv_sw: 0.03824, lp_indel_sv_ham: 5.0689, lp_indel_sv_n50: 2.4211, wh_snv_sw: 0.11418, wh_snv_ham: 2.5556, wh_snv_n50: 1.8769, wh_sw: 0.13687, wh_ham: 9.7071, wh_n50: 2.9802 },
  { cov: "40x", lp_sw: 0.02744, lp_ham: 1.7125, lp_n50: 2.1776, lp_indel_sw: 0.03301, lp_indel_ham: 4.3684, lp_indel_n50: 2.8646, lp_sv_sw: 0.02886, lp_sv_ham: 1.8444, lp_sv_n50: 2.2496, lp_indel_sv_sw: 0.0337, lp_indel_sv_ham: 4.3788, lp_indel_sv_n50: 2.9786, wh_snv_sw: 0.09665, wh_snv_ham: 3.0464, wh_snv_n50: 2.1509, wh_sw: 0.11617, wh_ham: 10.4029, wh_n50: 3.3907 },
  { cov: "50x", lp_sw: 0.02683, lp_ham: 1.4808, lp_n50: 2.5129, lp_indel_sw: 0.03031, lp_indel_ham: 3.257, lp_indel_n50: 3.1894, lp_sv_sw: 0.02793, lp_sv_ham: 1.6945, lp_sv_n50: 2.5546, lp_indel_sv_sw: 0.03072, lp_indel_sv_ham: 3.3856, lp_indel_sv_n50: 3.2168, wh_snv_sw: 0.0908, wh_snv_ham: 2.3996, wh_snv_n50: 2.4715, wh_sw: 0.10594, wh_ham: 8.4587, wh_n50: 3.6772 },
  { cov: "60x", lp_sw: 0.02266, lp_ham: 1.5344, lp_n50: 2.8641, lp_indel_sw: 0.027, lp_indel_ham: 3.4613, lp_indel_n50: 3.6938, lp_sv_sw: 0.02275, lp_sv_ham: 1.6792, lp_sv_n50: 2.8998, lp_indel_sv_sw: 0.02705, lp_indel_sv_ham: 3.4578, lp_indel_sv_n50: 3.7031, wh_snv_sw: 0.08066, wh_snv_ham: 2.7496, wh_snv_n50: 2.725, wh_sw: 0.09662, wh_ham: 9.2926, wh_n50: 4.196 },
];

// Solid colours: longphase in reds, whatshap in blues, darkening with the
// amount of co-phased data.
const SERIES = [
  { key: "lp",          name: "longphase",                        color: "#fca5a5" },
  { key: "lp_sv",       name: "longphase (--sv-file)",            color: "#f87171" },
  { key: "lp_indel",    name: "longphase (--indels)",             color: "#dc2626" },
  { key: "lp_indel_sv", name: "longphase (--indels + --sv-file)", color: "#7f1d1d" },
  { key: "wh_snv",      name: "whatshap (--only-snvs)",           color: "#93c5fd" },
  { key: "wh",          name: "whatshap",                         color: "#1d4ed8" },
];

// Value printed inside each bar, right-aligned at the bar end.
function BarValue({ x, y, width, height, value, fmt }) {
  if (value == null) return null;
  const inside = width > 34;
  return (
    <text
      x={x + width - (inside ? 4 : -4)}
      y={y + height / 2}
      textAnchor={inside ? "end" : "start"}
      dominantBaseline="central"
      fontSize={10}
      fill={inside ? "#ffffff" : "#374151"}
    >
      {fmt(value)}
    </text>
  );
}

const PANELS = [
  { title: "A. SNV Switch Error Rate (%)", suffix: "sw",  unit: "%",  tick: (v) => v.toFixed(2), fmt: (v) => v.toFixed(5), label: (v) => v.toFixed(3) },
  { title: "B. Hamming Distance (%)",      suffix: "ham", unit: "%",  tick: (v) => v.toFixed(0), fmt: (v) => v.toFixed(3), label: (v) => v.toFixed(2) },
  { title: "C. Block N50 (bp)",            suffix: "n50", unit: "Mb", tick: (v) => v.toFixed(1), fmt: (v) => `${(v * 1e6).toLocaleString(undefined, { maximumFractionDigits: 0 })} bp`, label: (v) => v.toFixed(2) },
];

function Panel({ title, suffix, unit, tick, fmt, label }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: 860 }}>
      <div style={{ textAlign: "center", fontSize: 14, fontWeight: 600, color: "#111827", marginBottom: 6 }}>
        {title}
      </div>
      <div style={{ flex: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 4, right: 14, bottom: 18, left: 4 }}
            barGap={1}
            barCategoryGap="16%"
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" horizontal={false} />
            <XAxis
              type="number"
              tick={{ fontSize: 10, fill: "#374151" }}
              tickFormatter={tick}
              label={{ value: unit, position: "insideBottom", offset: -8, fontSize: 11, fill: "#374151" }}
            />
            <YAxis
              type="category"
              dataKey="cov"
              tick={{ fontSize: 12, fill: "#374151" }}
              width={38}
            />
            <Tooltip
              cursor={{ fill: "rgba(0,0,0,0.04)" }}
              formatter={(value, name) => [fmt(value), name]}
              labelFormatter={(v) => `${v} coverage`}
              contentStyle={{ fontSize: 12, borderRadius: 6, border: "1px solid #d1d5db" }}
            />
            {SERIES.map((s) => (
              <Bar
                key={s.key}
                dataKey={`${s.key}_${suffix}`}
                name={s.name}
                fill={s.color}
                isAnimationActive={false}
                label={(props) => <BarValue {...props} fmt={label} />}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default function CophaseGroupCompare() {
  return (
    <div style={{ width: "100%", background: "#ffffff", padding: "20px 24px", fontFamily: "Helvetica, Arial, sans-serif" }}>
      <div style={{ textAlign: "center", fontSize: 19, fontWeight: 700, color: "#111827", marginBottom: 12 }}>
        Co-phasing configuration comparison
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "10px 22px", marginBottom: 18 }}>
        {SERIES.map((s) => (
          <div key={s.key} style={{ display: "flex", alignItems: "center", gap: 7 }}>
            <span style={{ width: 14, height: 14, background: s.color, borderRadius: 3, border: "0.6px solid #9ca3af" }} />
            <span style={{ fontSize: 12.5, color: "#111827" }}>{s.name}</span>
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 18 }}>
        {PANELS.map((p) => (
          <Panel key={p.suffix} {...p} />
        ))}
      </div>
    </div>
  );
}
