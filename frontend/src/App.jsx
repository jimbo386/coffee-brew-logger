import React, { useEffect, useState } from "react";
import LogForm from "./components/LogForm";
import Suggestions from "./components/Suggestions";
import BrewList from "./components/BrewList";
import Dashboard from "./components/Dashboard";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App(){
  const [brews, setBrews] = useState([]);
  const [suggestions, setSuggestions] = useState(null);

  async function fetchBrews(){
    try{
      const res = await fetch(`${API}/brews?limit=200`);
      const j = await res.json();
      setBrews(j.brews || []);
    }catch(e){
      console.warn(e);
    }
  }

  async function fetchSuggestions(){
    try{
      const res = await fetch(`${API}/suggestions`);
      if(!res.ok) return setSuggestions(null);
      const j = await res.json();
      setSuggestions(j.suggestions || j.suggestions || []);
    }catch(e){
      setSuggestions(null);
    }
  }

  useEffect(()=>{ fetchBrews(); fetchSuggestions(); },[]);

  return (
    <div className="app-root">
      <header className="topbar">
        <h1>Coffee Brew Logger</h1>
      </header>
      <main className="container">
        <section className="left">
          <h2>Log a Brew</h2>
          <LogForm onSaved={() => { fetchBrews(); fetchSuggestions(); }} />

          <h2 style={{marginTop:20}}>Recent Brews</h2>
          <BrewList brews={brews} />
        </section>
        <aside className="right">
          <h2>Suggestions</h2>
          <Suggestions suggestions={suggestions} />

          <h2 style={{marginTop:20}}>Dashboard</h2>
          <Dashboard brews={brews} />
        </aside>
      </main>
    </div>
  );
}
