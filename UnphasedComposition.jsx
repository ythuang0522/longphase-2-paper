import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

// SNV-only, seed 1. Variants phased by LongPhase but unphased by the GNN.
// n_* fields carry the absolute counts behind each percentage.
const A_DATA = [
  {cov:"10x", n:63797, fp:81.13, hom:5.27, het:13.59, n_fp:51760, n_hom:3364, n_het:8673},
  {cov:"12x", n:64428, fp:83.67, hom:4.81, het:11.52, n_fp:53909, n_hom:3100, n_het:7419},
  {cov:"14x", n:63987, fp:86.14, hom:4.35, het: 9.51, n_fp:55121, n_hom:2782, n_het:6084},
  {cov:"16x", n:63438, fp:87.92, hom:3.92, het: 8.16, n_fp:55776, n_hom:2486, n_het:5176},
  {cov:"18x", n:63102, fp:88.71, hom:3.75, het: 7.54, n_fp:55976, n_hom:2366, n_het:4760},
  {cov:"20x", n:63575, fp:90.06, hom:3.75, het: 6.19, n_fp:57256, n_hom:2382, n_het:3937},
  {cov:"30x", n:60442, fp:91.09, hom:3.55, het: 5.36, n_fp:55055, n_hom:2148, n_het:3239},
  {cov:"40x", n:60629, fp:92.11, hom:3.21, het: 4.68, n_fp:55848, n_hom:1944, n_het:2837},
  {cov:"50x", n:59445, fp:92.12, hom:3.34, het: 4.53, n_fp:54762, n_hom:1988, n_het:2695},
  {cov:"60x", n:60267, fp:93.03, hom:2.97, het: 4.00, n_fp:56069, n_hom:1787, n_het:2411},
];

const FONT = "'Libre Franklin','Helvetica Neue',Arial,sans-serif";
const axT = {fontFamily:FONT, fontSize:10, fill:"#525252"};
const axL = {stroke:"#a3a3a3"};

const A_SERIES = [
  {key:"fp",  label:"homozygous wildtype", color:"#d4d4d4"},
  {key:"hom", label:"homozygous mutant",   color:"#a3a3a3"},
  {key:"het", label:"heterozygous",        color:"#e11d48"},
];

const ATip = ({active, payload, label}) => {
  if (!active || !payload || !payload.length) return null;
  const d = payload[0].payload;
  return (
    <div style={{background:"#fff", border:"1px solid #d4d4d4", borderRadius:4,
      padding:"7px 11px", fontFamily:FONT, fontSize:10.5, lineHeight:1.55,
      boxShadow:"0 2px 8px rgba(0,0,0,0.08)"}}>
      <div style={{fontWeight:700, marginBottom:3}}>
        {label}
        <span style={{fontWeight:400, color:"#a3a3a3"}}>
          &nbsp;&middot; total unphased {d.n.toLocaleString()}
        </span>
      </div>
      {A_SERIES.map(s => (
        <div key={s.key} style={{color:s.color === "#d4d4d4" ? "#737373" : s.color}}>
          {s.label}: <strong>{d[s.key].toFixed(1)}%</strong>
          <span style={{color:"#a3a3a3"}}> ({d["n_" + s.key].toLocaleString()})</span>
        </div>
      ))}
    </div>
  );
};

export default function UnphasedComposition() {
  return (
    <div style={{fontFamily:FONT, background:"#fff", padding:"16px 20px 12px",
      maxWidth:640, margin:"0 auto"}}>
      <link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;500;600;700&display=swap" rel="stylesheet"/>

      <div style={{textAlign:"center", fontSize:14, fontWeight:700, color:"#0a0a0a",
        marginBottom:10}}>
        Composition of every unphased SNV
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={A_DATA} margin={{top:4, right:8, bottom:2, left:0}} barCategoryGap="18%">
          <CartesianGrid strokeDasharray="3 3" stroke="#eee" vertical={false} />
          <XAxis dataKey="cov" tick={axT} tickLine={axL} axisLine={axL} />
          <YAxis tick={axT} tickLine={axL} axisLine={axL} domain={[0,100]}
                 ticks={[0,20,40,60,80,100]} tickFormatter={v => v + "%"} />
          <Tooltip content={<ATip />} cursor={{fill:"rgba(0,0,0,0.03)"}} />
          {A_SERIES.map(s => (
            <Bar key={s.key} dataKey={s.key} stackId="a" fill={s.color}
                 stroke={s.key === "het" ? "#be123c" : "none"}
                 strokeWidth={s.key === "het" ? 0.6 : 0}
                 isAnimationActive={false} />
          ))}
        </BarChart>
      </ResponsiveContainer>

      <div style={{display:"flex", justifyContent:"center", gap:16, flexWrap:"wrap",
        fontSize:10.5, color:"#404040", marginTop:8}}>
        {A_SERIES.map(s => (
          <span key={s.key} style={{display:"flex", alignItems:"center", gap:4}}>
            <span style={{width:10, height:10, background:s.color, borderRadius:2,
              display:"inline-block"}} />
            {s.label}
          </span>
        ))}
      </div>
    </div>
  );
}
