import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

// HG002 PacBio HiFi, replicate 1, scored against GIAB v5.0q.
// Block N50 is in Mb; Phased SNV is the percentage of assessable
// heterozygous SNVs in the benchmark.
const data = [
  { cov: 10, wh_sw: 2655, wh_psnv: 87.42959, wh_ham: 1.03425, wh_n50: 0.3402, lpgnn_sw: 1070, lpgnn_psnv: 87.01973, lpgnn_ham: 0.7764, lpgnn_n50: 0.3409 },
  { cov: 20, wh_sw: 2667, wh_psnv: 87.50283, wh_ham: 1.45136, wh_n50: 0.4393, lpgnn_sw: 938, lpgnn_psnv: 87.0061, lpgnn_ham: 0.91996, lpgnn_n50: 0.4462 },
  { cov: 30, wh_sw: 2694, wh_psnv: 87.53093, wh_ham: 1.46712, wh_n50: 0.4841, lpgnn_sw: 854, lpgnn_psnv: 86.96187, lpgnn_ham: 1.01255, lpgnn_n50: 0.4917 },
  { cov: 40, wh_sw: 2778, wh_psnv: 87.54535, wh_ham: 1.66373, wh_n50: 0.5185, lpgnn_sw: 795, lpgnn_psnv: 86.90114, lpgnn_ham: 0.96916, lpgnn_n50: 0.5318 },
  { cov: 50, wh_sw: 2618, wh_psnv: 87.55007, wh_ham: 1.48431, wh_n50: 0.534, lpgnn_sw: 862, lpgnn_psnv: 86.88321, lpgnn_ham: 1.04906, lpgnn_n50: 0.5463 },
];

const SERIES = [
  { key: "wh",    name: "WhatsHap",      color: "#2563eb" },
  { key: "lpgnn", name: "LongPhase 2.1", color: "#dc2626" },
];

const PANELS = [
  { title: "A. 5.0q Switch errors",   suffix: "sw",   unit: "",   tick: (v) => (v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v.toFixed(0)), fmt: (v) => v.toLocaleString() },
  { title: "B. Phased SNV",           suffix: "psnv", unit: "%",  tick: (v) => v.toFixed(0), fmt: (v) => `${v.toFixed(2)}%`, domain: [86, 88], ticks: [86, 86.5, 87, 87.5, 88] },
  { title: "C. Hamming Distance (%)", suffix: "ham",  unit: "%",  tick: (v) => v.toFixed(1), fmt: (v) => `${v.toFixed(2)}%`, domain: [0, 2.5], ticks: [0, 0.5, 1, 1.5, 2, 2.5] },
  { title: "D. Block N50",            suffix: "n50",  unit: "Mb", tick: (v) => v.toFixed(2), fmt: (v) => `${(v * 1000).toFixed(0)} kb` },
];

function Panel({ title, suffix, unit, tick, fmt, domain, ticks }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: 230 }}>
      <div style={{ textAlign: "center", fontSize: 13.5, fontWeight: 600, color: "#111827", marginBottom: 6 }}>
        {title}
      </div>
      <div style={{ flex: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 4, right: 14, bottom: 22, left: 4 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="cov"
              type="number"
              domain={[10, 50]}
              ticks={[10, 20, 30, 40, 50]}
              tick={{ fontSize: 11, fill: "#374151" }}
              tickFormatter={(v) => `${v}x`}
              label={{ value: "Coverage", position: "insideBottom", offset: -12, fontSize: 11.5, fill: "#374151" }}
            />
            <YAxis
              tick={{ fontSize: 11, fill: "#374151" }}
              width={50}
              domain={domain || ["auto", "auto"]}
              ticks={ticks}
              tickFormatter={tick}
              label={{ value: unit || "count", angle: -90, position: "insideLeft", offset: 8, fontSize: 11.5, fill: "#374151" }}
            />
            <Tooltip
              formatter={(value, name) => [fmt(value), name]}
              labelFormatter={(v) => `${v}x coverage`}
              contentStyle={{ fontSize: 12, borderRadius: 6, border: "1px solid #d1d5db" }}
            />
            {SERIES.map((s) => (
              <Line
                key={s.key}
                type="linear"
                dataKey={`${s.key}_${suffix}`}
                name={s.name}
                stroke={s.color}
                strokeWidth={2}
                strokeDasharray={s.dash}
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

export default function HifiCompare() {
  return (
    <div style={{ width: "100%", background: "#ffffff", padding: "20px 24px", fontFamily: "Helvetica, Arial, sans-serif" }}>
      <div style={{ textAlign: "center", fontSize: 18, fontWeight: 700, color: "#111827", marginBottom: 12 }}>
        WhatsHap vs LongPhase 2.1 on PacBio HiFi
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "10px 24px", marginBottom: 18 }}>
        {SERIES.map((s) => (
          <div key={s.key} style={{ display: "flex", alignItems: "center", gap: 7 }}>
            <svg width={24} height={4}><line x1={0} y1={2} x2={24} y2={2} stroke={s.color} strokeWidth={3} strokeDasharray={s.dash} /></svg>
            <span style={{ fontSize: 12.5, color: "#111827" }}>{s.name}</span>
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: "22px 20px" }}>
        {PANELS.map((p) => <Panel key={p.suffix} {...p} />)}
      </div>
    </div>
  );
}
