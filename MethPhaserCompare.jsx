import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

// HG002 ONT R10.4.1, replicate 1, scored against GIAB v5.0q.
// Block N50 is in Mb; Phased SNV is the percentage of assessable
// heterozygous SNVs in the benchmark.
const data = [
  { cov: 10, methphaser_sw: 2277, methphaser_psnv: 78.11491, methphaser_ham: 6.92789, methphaser_n50: 0.9395, lpgnn_sw: 1554, lpgnn_psnv: 77.89168, lpgnn_ham: 5.30991, lpgnn_n50: 0.8787 },
  { cov: 20, methphaser_sw: 1311, methphaser_psnv: 91.08722, methphaser_ham: 3.98836, methphaser_n50: 1.6993, lpgnn_sw: 910, lpgnn_psnv: 90.97687, lpgnn_ham: 3.39801, lpgnn_n50: 1.7425 },
  { cov: 30, methphaser_sw: 1004, methphaser_psnv: 91.60825, methphaser_ham: 2.40328, methphaser_n50: 1.9689, lpgnn_sw: 692, lpgnn_psnv: 91.50633, lpgnn_ham: 2.00896, lpgnn_n50: 2.073 },
  { cov: 40, methphaser_sw: 878, methphaser_psnv: 91.63726, methphaser_ham: 2.37294, methphaser_n50: 2.2887, lpgnn_sw: 611, lpgnn_psnv: 91.55014, lpgnn_ham: 2.19873, lpgnn_n50: 2.4705 },
  { cov: 50, methphaser_sw: 883, methphaser_psnv: 91.5461, methphaser_ham: 1.8627, methphaser_n50: 2.5705, lpgnn_sw: 610, lpgnn_psnv: 91.46514, lpgnn_ham: 1.8341, lpgnn_n50: 2.8654 },
  { cov: 60, methphaser_sw: 743, methphaser_psnv: 91.43292, methphaser_ham: 1.75198, methphaser_n50: 2.9108, lpgnn_sw: 497, lpgnn_psnv: 91.36455, lpgnn_ham: 1.5984, lpgnn_n50: 3.0871 },
];

const SERIES = [
  { key: "methphaser", name: "MethPhaser",     color: "#0891b2" },
  { key: "lpgnn",      name: "LongPhase 2.1",  color: "#dc2626" },
];

const PANELS = [
  { title: "A. 5.0q Switch errors",   suffix: "sw",   unit: "",   tick: (v) => (v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v.toFixed(0)), fmt: (v) => v.toLocaleString() },
  { title: "B. Phased SNV",           suffix: "psnv", unit: "%",  tick: (v) => v.toFixed(0), fmt: (v) => `${v.toFixed(2)}%`, domain: [75, 95], ticks: [75, 80, 85, 90, 95] },
  { title: "C. Hamming Distance (%)", suffix: "ham",  unit: "%",  tick: (v) => v.toFixed(0), fmt: (v) => `${v.toFixed(2)}%` },
  { title: "D. Block N50",            suffix: "n50",  unit: "Mb", tick: (v) => v.toFixed(1), fmt: (v) => `${v.toFixed(2)} Mb` },
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
              domain={[10, 60]}
              ticks={[10, 20, 30, 40, 50, 60]}
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

export default function MethPhaserCompare() {
  return (
    <div style={{ width: "100%", background: "#ffffff", padding: "20px 24px", fontFamily: "Helvetica, Arial, sans-serif" }}>
      <div style={{ textAlign: "center", fontSize: 18, fontWeight: 700, color: "#111827", marginBottom: 12 }}>
        MethPhaser vs LongPhase 2.1
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
