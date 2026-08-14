from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from .db import init_db, get_session
from .models import Brew, BrewCreate
from .crud import create_brew, get_brews
from pathlib import Path
import json

app = FastAPI(title="Coffee Brew Logger - Postgres Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUGGESTIONS_JSON = Path("data/suggestions.json")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/brews")
def list_brews(limit: int = 200, session: Session = Depends(get_session)):
    raws = get_brews(session, limit=limit)
    # convert to dicts
    return {"brews": [r.dict() for r in raws], "count": len(raws)}

@app.post("/brews", status_code=201)
def post_brew(brew_in: BrewCreate, session: Session = Depends(get_session)):
    b = create_brew(session, brew_in)
    return {"id": b.id}

@app.get("/suggestions")
def get_suggestions():
    if not SUGGESTIONS_JSON.exists():
        raise HTTPException(status_code=404, detail="suggestions.json not found - run ml/train.py to generate suggestions")
    with open(SUGGESTIONS_JSON, encoding='utf-8') as f:
        return json.load(f)
