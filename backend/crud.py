from sqlmodel import Session, select
from .models import Brew, BrewCreate
import uuid
import datetime

def create_brew(session: Session, brew_in: BrewCreate):
    b = Brew(id=str(uuid.uuid4()), timestamp=datetime.datetime.utcnow(), **brew_in.dict())
    session.add(b)
    session.commit()
    session.refresh(b)
    return b

def get_brews(session: Session, limit: int = 200):
    statement = select(Brew).limit(limit)
    results = session.exec(statement).all()
    return results
