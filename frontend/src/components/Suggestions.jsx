import React from "react";

export default function Suggestions({suggestions}){
  if(!suggestions) return <div className="muted">No suggestions yet. Run the ML trainer.</div>;
  if(!Array.isArray(suggestions) || suggestions.length===0) return <div>No suggestions.</div>;
  return (
    <div className="suggestions">
      {suggestions.map((s,i)=> (
        <div key={i} className="suggestion">
          <div className="title">#{i+1} — predicted {s.predicted_score ? s.predicted_score.toFixed(2) : '—'}</div>
          <div className="meta">Coffee: {s.coffee_weight_g} g · Temp: {s.water_temp_c} °C</div>
        </div>
      ))}
    </div>
  );
}
