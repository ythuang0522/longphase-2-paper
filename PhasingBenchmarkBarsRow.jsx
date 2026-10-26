import React from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

// HG002 ONT R10.4.1. 10-20x are means of 10 replicates; 30-60x are single runs.
// Phased SNV and block N50 come from the v5.0q report and are identical under
// either benchmark.
const data = [
  { cov: "10x", lp_sw50: 1503, lp_indel_sw50: 1708, lp_sv_sw50: 1694, wh_snv_sw50: 4383, wh_sw50: 5174, hc2_sw50: 5018, lp_ham50: 5.3932, lp_indel_ham50: 6.9844, lp_sv_ham50: 6.9502, wh_snv_ham50: 7.6036, wh_ham50: 12.1595, hc2_ham50: 7.772, lp_sw42: 1839, lp_indel_sw42: 2000, lp_sv_sw42: 1991, wh_snv_sw42: 2773, wh_sw42: 3538, hc2_sw42: 3050, lp_ham42: 5.372, lp_indel_ham42: 6.9489, lp_sv_ham42: 6.925, wh_snv_ham42: 7.4417, wh_ham42: 12.0044, hc2_ham42: 7.5926, lp_psnv: 1867178, lp_indel_psnv: 1865345, lp_sv_psnv: 1865138, wh_snv_psnv: 1888779, wh_psnv: 1888961, hc2_psnv: 1889811, lp_n50: 0.8449, lp_indel_n50: 0.9763, lp_sv_n50: 0.9746, wh_snv_n50: 0.945, wh_n50: 1.2415, hc2_n50: 0.9537 },
  { cov: "20x", lp_sw50: 804, lp_indel_sw50: 981, lp_sv_sw50: 970, wh_snv_sw50: 3067, wh_sw50: 3683, hc2_sw50: 3825, lp_ham50: 3.2152, lp_indel_ham50: 5.8449, lp_sv_ham50: 5.7826, wh_snv_ham50: 4.3969, wh_ham50: 11.449, hc2_ham50: 4.2654, lp_sw42: 1663, lp_indel_sw42: 1818, lp_sv_sw42: 1810, wh_snv_sw42: 1972, wh_sw42: 2580, hc2_sw42: 2346, lp_ham42: 3.1373, lp_indel_ham42: 5.8281, lp_sv_ham42: 5.7823, wh_snv_ham42: 4.2148, wh_ham42: 11.3426, hc2_ham42: 4.0931, lp_psnv: 2181602, lp_indel_psnv: 2180311, lp_sv_psnv: 2180131, wh_snv_psnv: 2199412, wh_psnv: 2199575, hc2_psnv: 2199832, lp_n50: 1.616, lp_indel_n50: 2.0311, lp_sv_n50: 2.0241, wh_snv_n50: 1.6532, wh_n50: 2.4878, hc2_n50: 1.6639 },
  { cov: "30x", lp_sw50: 648, lp_indel_sw50: 806, lp_sv_sw50: 812, wh_snv_sw50: 2524, wh_sw50: 3027, hc2_sw50: 3280, lp_ham50: 1.8516, lp_indel_ham50: 4.9647, lp_sv_ham50: 4.8308, wh_snv_ham50: 2.5556, wh_ham50: 9.7071, hc2_ham50: 2.6071, lp_sw42: 1641, lp_indel_sw42: 1789, lp_sv_sw42: 1789, wh_snv_sw42: 1850, wh_sw42: 2345, hc2_sw42: 2202, lp_ham42: 1.8326, lp_indel_ham42: 4.7719, lp_sv_ham42: 4.7168, wh_snv_ham42: 2.4456, wh_ham42: 9.6739, hc2_ham42: 2.4607, lp_psnv: 2194831, lp_indel_psnv: 2194193, lp_sv_psnv: 2194109, wh_snv_psnv: 2213304, wh_psnv: 2213472, hc2_psnv: 2213483, lp_n50: 1.9275, lp_indel_n50: 2.4795, lp_sv_n50: 2.4535, wh_snv_n50: 1.8769, wh_n50: 2.9802, hc2_n50: 1.8869 },
  { cov: "40x", lp_sw50: 594, lp_indel_sw50: 714, lp_sv_sw50: 727, wh_snv_sw50: 2139, wh_sw50: 2572, hc2_sw50: 2916, lp_ham50: 1.7146, lp_indel_ham50: 4.4873, lp_sv_ham50: 4.4531, wh_snv_ham50: 3.0464, wh_ham50: 10.4029, hc2_ham50: 2.8984, lp_sw42: 1667, lp_indel_sw42: 1766, lp_sv_sw42: 1765, wh_snv_sw42: 1810, wh_sw42: 2221, hc2_sw42: 2171, lp_ham42: 1.6438, lp_indel_ham42: 4.324, lp_sv_ham42: 4.2433, wh_snv_ham42: 2.919, wh_ham42: 10.4281, hc2_ham42: 2.7184, lp_psnv: 2195925, lp_indel_psnv: 2194982, lp_sv_psnv: 2194852, wh_snv_psnv: 2215519, wh_psnv: 2215645, hc2_psnv: 2215745, lp_n50: 2.1962, lp_indel_n50: 2.9286, lp_sv_n50: 2.9308, wh_snv_n50: 2.1509, wh_n50: 3.3907, hc2_n50: 2.164 },
  { cov: "50x", lp_sw50: 588, lp_indel_sw50: 671, lp_sv_sw50: 667, wh_snv_sw50: 2010, wh_sw50: 2346, hc2_sw50: 2568, lp_ham50: 1.5399, lp_indel_ham50: 3.4272, lp_sv_ham50: 3.3327, wh_snv_ham50: 2.3996, wh_ham50: 8.4587, hc2_ham50: 2.1974, lp_sw42: 1671, lp_indel_sw42: 1768, lp_sv_sw42: 1773, wh_snv_sw42: 1811, wh_sw42: 2171, hc2_sw42: 2133, lp_ham42: 1.4878, lp_indel_ham42: 3.2748, lp_sv_ham42: 3.2369, wh_snv_ham42: 2.2316, wh_ham42: 8.3245, hc2_ham42: 2.0336, lp_psnv: 2193849, lp_indel_psnv: 2192863, lp_sv_psnv: 2192814, wh_snv_psnv: 2215890, wh_psnv: 2216012, hc2_psnv: 2216082, lp_n50: 2.5276, lp_indel_n50: 3.2271, lp_sv_n50: 3.2193, wh_snv_n50: 2.4715, wh_n50: 3.6772, hc2_n50: 2.4615 },
  { cov: "60x", lp_sw50: 477, lp_indel_sw50: 588, lp_sv_sw50: 568, wh_snv_sw50: 1785, wh_sw50: 2139, hc2_sw50: 2309, lp_ham50: 1.5762, lp_indel_ham50: 3.5614, lp_sv_ham50: 3.5078, wh_snv_ham50: 2.7496, wh_ham50: 9.2926, hc2_ham50: 2.1106, lp_sw42: 1678, lp_indel_sw42: 1771, lp_sv_sw42: 1769, wh_snv_sw42: 1801, wh_sw42: 2156, hc2_sw42: 2088, lp_ham42: 1.5755, lp_indel_ham42: 3.614, lp_sv_ham42: 3.5605, wh_snv_ham42: 2.6087, wh_ham42: 9.1981, hc2_ham42: 2.0153, lp_psnv: 2191367, lp_indel_psnv: 2190529, lp_sv_psnv: 2190368, wh_snv_psnv: 2215068, wh_psnv: 2215208, hc2_psnv: 2215228, lp_n50: 2.8713, lp_indel_n50: 3.7435, lp_sv_n50: 3.6938, wh_snv_n50: 2.725, wh_n50: 4.196, hc2_n50: 2.725 },
];

// Colour encodes the tool, darkening with the amount of co-phased data.
const SERIES = [
  { key: "lp",       name: "longphase v2.1.2",                        color: "#fca5a5" },
  { key: "lp_indel", name: "longphase v2.1.2 (--indels)",             color: "#dc2626" },
  { key: "lp_sv",    name: "longphase v2.1.2 (--indels + --sv-file)", color: "#7f1d1d" },
  { key: "wh_snv",   name: "whatshap v2.8 (--only-snvs)",           color: "#93c5fd" },
  { key: "wh",       name: "whatshap v2.8",                         color: "#1d4ed8" },
  { key: "hc2",      name: "hapcut2 v1.3.4",                        color: "#16a34a" },
];

const PANELS = [
  { title: "A. v5.0q  Switch errors",         suffix: "sw50",  unit: "",   tick: (v) => (v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v.toFixed(0)), fmt: (v) => v.toLocaleString() },
  { title: "B. v5.0q  Hamming Distance (%)",  suffix: "ham50", unit: "%",  tick: (v) => v.toFixed(0), fmt: (v) => `${v.toFixed(2)}%` },
  { title: "C. v4.2.1  Switch errors",        suffix: "sw42",  unit: "",   tick: (v) => (v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v.toFixed(0)), fmt: (v) => v.toLocaleString() },
  { title: "D. v4.2.1  Hamming Distance (%)", suffix: "ham42", unit: "%",  tick: (v) => v.toFixed(0), fmt: (v) => `${v.toFixed(2)}%` },
  { title: "E. Phased SNV",                   suffix: "psnv",  unit: "M",  tick: (v) => (v / 1e6).toFixed(2), fmt: (v) => v.toLocaleString(), domain: [1800000, 2250000] },
  { title: "F. Block N50",                    suffix: "n50",   unit: "Mb", tick: (v) => v.toFixed(0), fmt: (v) => `${v.toFixed(2)} Mb`, domain: [0, 5] },
];

function Panel({ title, suffix, unit, tick, fmt, domain }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: 470 }}>
      <div style={{ textAlign: "center", fontSize: 12, fontWeight: 600, color: "#111827", marginBottom: 6, lineHeight: 1.25, minHeight: 30 }}>
        {title}
      </div>
      <div style={{ flex: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 2, right: 8, bottom: 18, left: 0 }}
            barGap={0.5}
            barCategoryGap="6%"
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" horizontal={false} />
            <XAxis
              type="number"
              domain={domain || [0, "auto"]}
              allowDataOverflow={!!domain}
              tick={{ fontSize: 10, fill: "#374151" }}
              tickFormatter={tick}
              tickLine={false}
              axisLine={{ stroke: "#9ca3af" }}
              height={30}
              label={{ value: unit, position: "insideBottom", offset: -14, fontSize: 10, fill: "#374151" }}
            />
            <YAxis
              type="category"
              dataKey="cov"
              tick={{ fontSize: 11, fill: "#374151" }}
              width={34}
              tickLine={false}
              axisLine={false}
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
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default function PhasingBenchmarkBarsRow() {
  return (
    <div style={{ width: "100%", background: "#ffffff", padding: "14px 14px", fontFamily: "Helvetica, Arial, sans-serif" }}>
      <div style={{ textAlign: "center", fontSize: 15, fontWeight: 700, color: "#111827", marginBottom: 8 }}>
        Phasing tool comparison under two GIAB benchmarks
      </div>

      <div style={{ marginBottom: 10 }}>
        {[SERIES.slice(0, 3), SERIES.slice(3)].map((row, i) => (
          <div key={i} style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "4px 18px", marginBottom: 4 }}>
            {row.map((s) => (
              <div key={s.key} style={{ display: "flex", alignItems: "center", gap: 7 }}>
                <span style={{ width: 11, height: 11, background: s.color, borderRadius: 2, border: "0.6px solid #9ca3af" }} />
                <span style={{ fontSize: 11, color: "#111827" }}>{s.name}</span>
              </div>
            ))}
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: 10 }}>
        {PANELS.map((p) => <Panel key={p.suffix} {...p} />)}
      </div>
    </div>
  );
}
