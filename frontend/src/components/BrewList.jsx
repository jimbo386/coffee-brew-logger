import React from "react";

export default function BrewList({brews}){
  if(!brews || brews.length===0) return <div className="muted">No brews yet.</div>;
  return (
    <div className="brew-list">
      {brews.slice(0,50).map(b => (
        <div key={b.id} className="brew-item">
          <div className="brew-title">{b.bean_variety} — {b.brew_method}</div>
          <div className="brew-meta">Taste: {b.taste_rating || '—'} · {new Date(b.timestamp).toLocaleString()}</div>
        </div>
      ))}
    </div>
  );
}
