import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

// HG002 PacBio HiFi, replicate 1, scored against GIAB v5.0q.
// Block N50 is in Mb; Phased SNV is the percentage of assessable
// heterozygous SNVs in the benchmark.
const data = [
  { cov: 10, wh_sw: 2655, wh_psnv: 87.42959, wh_ham: 1.03425, wh_n50: 0.3402, lpgnn_sw: 1020, lpgnn_psnv: 87.00731, lpgnn_ham: 0.73414, lpgnn_n50: 0.3409, lp_sw: 1328, lp_psnv: 87.11632, lp_ham: 0.95944, lp_n50: 0.3465 },
  { cov: 20, wh_sw: 2504, wh_psnv: 92.19548, wh_ham: 1.20866, wh_n50: 0.4782, lpgnn_sw: 878, lpgnn_psnv: 91.71522, lpgnn_ham: 1.13262, lpgnn_n50: 0.488, lp_sw: 1268, lp_psnv: 91.83661, lp_ham: 1.28011, lp_n50: 0.4917 },
  { cov: 30, wh_sw: 2331, wh_psnv: 92.40225, wh_ham: 0.92098, wh_n50: 0.5245, lpgnn_sw: 829, lpgnn_psnv: 91.90218, lpgnn_ham: 0.80942, lpgnn_n50: 0.5403, lp_sw: 1137, lp_psnv: 92.01932, lp_ham: 1.0223, lp_n50: 0.5451 },
  { cov: 40, wh_sw: 1954, wh_psnv: 92.37269, wh_ham: 0.86784, wh_n50: 0.5609, lpgnn_sw: 815, lpgnn_psnv: 91.87433, lpgnn_ham: 0.77218, lpgnn_n50: 0.5728, lp_sw: 1153, lp_psnv: 91.97517, lp_ham: 0.97856, lp_n50: 0.5796 },
  { cov: 50, wh_sw: 1687, wh_psnv: 92.0457, wh_ham: 0.67536, wh_n50: 0.577, lpgnn_sw: 714, lpgnn_psnv: 91.55606, lpgnn_ham: 0.82454, lpgnn_n50: 0.5838, lp_sw: 988, lp_psnv: 91.65544, lp_ham: 1.10418, lp_n50: 0.5883 },
];

const SERIES = [
  { key: "wh",    name: "WhatsHap",                     color: "#2563eb" },
  { key: "lpgnn", name: "LongPhase 2.1.1",  color: "#dc2626" },
  { key: "lp",    name: "LongPhase 2.1.1 (--disableGNN)",        color: "#f97316", dash: "6 3" },
];

const PANELS = [
  { title: "A. 5.0q Switch errors",   suffix: "sw",   unit: "",   tick: (v) => (v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v.toFixed(0)), fmt: (v) => v.toLocaleString() },
  { title: "B. Phased SNV",           suffix: "psnv", unit: "%",  tick: (v) => v.toFixed(0), fmt: (v) => `${v.toFixed(2)}%`, domain: [86, 93], ticks: [86, 88, 90, 92] },
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

export default function HifiCompare3() {
  return (
    <div style={{ width: "100%", background: "#ffffff", padding: "20px 24px", fontFamily: "Helvetica, Arial, sans-serif" }}>
      <div style={{ textAlign: "center", fontSize: 18, fontWeight: 700, color: "#111827", marginBottom: 12 }}>
        WhatsHap vs LongPhase 2.1.1 on PacBio HiFi, with and without GNN correction
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
