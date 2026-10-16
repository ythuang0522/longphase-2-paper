import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

// SNV-only, seed 1. Variants phased by LongPhase but unphased by the GNN.
// n_* fields carry the absolute counts behind each percentage.
const A_DATA = [
  {cov:"10x", n:61389, fp:84.03, hom:5.08, het:10.89, n_fp:51585, n_hom:3120, n_het:6684},
  {cov:"12x", n:62268, fp:86.19, hom:4.77, het:9.04, n_fp:53670, n_hom:2968, n_het:5630},
  {cov:"14x", n:62373, fp:87.75, hom:4.31, het: 7.93, n_fp:54735, n_hom:2689, n_het:4949},
  {cov:"16x", n:63747, fp:89.02, hom:3.95, het: 7.03, n_fp:56749, n_hom:2516, n_het:4482},
  {cov:"18x", n:62883, fp:90.06, hom:3.73, het: 6.21, n_fp:56632, n_hom:2343, n_het:3908},
  {cov:"20x", n:64201, fp:91.28, hom:3.69, het: 5.03, n_fp:58602, n_hom:2371, n_het:3228},
  {cov:"30x", n:63611, fp:91.98, hom:3.41, het: 4.62, n_fp:58507, n_hom:2166, n_het:2938},
  {cov:"40x", n:62459, fp:92.79, hom:3.15, het: 4.06, n_fp:57957, n_hom:1966, n_het:2536},
  {cov:"50x", n:61888, fp:92.77, hom:3.36, het: 3.87, n_fp:57411, n_hom:2081, n_het:2396},
  {cov:"60x", n:62230, fp:93.56, hom:2.98, het: 3.46, n_fp:58222, n_hom:1852, n_het:2156},
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
