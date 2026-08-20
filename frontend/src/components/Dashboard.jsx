import React, { useMemo } from "react";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function Dashboard({brews}){
  const chartData = useMemo(()=>{
    if(!brews || brews.length===0) return {labels:[],datasets:[]};
    // aggregate average taste by brew_method (top 6)
    const map = {};
    brews.forEach(b=>{
      const m = b.brew_method || 'unknown';
      const t = Number(b.taste_rating) || null;
      if(t===null) return;
      if(!map[m]) map[m] = {sum:0,count:0};
      map[m].sum += t; map[m].count += 1;
    });
    const entries = Object.entries(map).map(([k,v])=>({method:k,avg:v.sum/v.count,count:v.count}));
    entries.sort((a,b)=>b.avg-a.avg);
    const top = entries.slice(0,6);
    return {
      labels: top.map(t=>t.method),
      datasets: [{label: 'Avg taste', data: top.map(t=>Number(t.avg.toFixed(2))), backgroundColor: 'rgba(75,192,192,0.6)'}]
    };
  },[brews]);

  if(!chartData.labels || chartData.labels.length===0) return <div className="muted">No data for dashboard yet.</div>;

  return (
    <div>
      <Bar data={chartData} />
    </div>
  );
}
