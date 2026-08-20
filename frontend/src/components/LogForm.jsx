import React, { useState } from "react";
const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function LogForm({onSaved}){
  const [form, setForm] = useState({
    bean_variety: "Ethiopian Yirgacheffe",
    brew_method: "v60",
    coffee_weight_g: 18,
    water_weight_g: 300,
    water_temp_c: 93,
    taste_rating: 8.0
  });

  const onChange = (k,v) => setForm(s=>({...s,[k]:v}));

  async function submit(e){
    e.preventDefault();
    const payload = {
      bean_variety: form.bean_variety,
      brew_method: form.brew_method,
      coffee_weight_g: Number(form.coffee_weight_g),
      water_weight_g: Number(form.water_weight_g),
      water_temp_c: Number(form.water_temp_c),
      taste_rating: Number(form.taste_rating)
    };
    try{
      const res = await fetch(`${API}/brews`, {method:"POST", headers:{"content-type":"application/json"}, body: JSON.stringify(payload)});
      if(!res.ok) throw new Error('Failed to save');
      setForm({bean_variety:"",brew_method:"",coffee_weight_g:18,water_weight_g:300,water_temp_c:93,taste_rating:8});
      if(onSaved) onSaved();
    }catch(err){
      alert('Could not save brew: '+err.message);
    }
  }

  return (
    <form onSubmit={submit} className="form">
      <label>Bean variety <input value={form.bean_variety} onChange={e=>onChange('bean_variety', e.target.value)} /></label>
      <label>Brew method <input value={form.brew_method} onChange={e=>onChange('brew_method', e.target.value)} /></label>
      <label>Coffee weight (g) <input type="number" value={form.coffee_weight_g} onChange={e=>onChange('coffee_weight_g', e.target.value)} /></label>
      <label>Water weight (g) <input type="number" value={form.water_weight_g} onChange={e=>onChange('water_weight_g', e.target.value)} /></label>
      <label>Water temp (°C) <input type="number" value={form.water_temp_c} onChange={e=>onChange('water_temp_c', e.target.value)} /></label>
      <label>Taste rating (0-10) <input type="number" step="0.1" value={form.taste_rating} onChange={e=>onChange('taste_rating', e.target.value)} /></label>
      <div><button type="submit" className="btn">Save Brew</button></div>
    </form>
  );
}
