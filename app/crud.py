from sqlalchemy.orm import Session

from models import Season

def get_seasons(db: Session, skip: int=0, limit: int=100):
    return db.query(Season).offset(skip).limit(limit).all()
