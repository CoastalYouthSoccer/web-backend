from sqlalchemy.orm import Session
from sqlalchemy import update
from pydantic import UUID4
from models import Season as SeasonModel
from schemas import Season, SeasonCreate

def get_seasons(db: Session, skip: int=0, limit: int=100):
    return db.query(SeasonModel).offset(skip).limit(limit).\
        filter(SeasonModel.active == True).all()

def get_season_by_name(db: Session, name: str):
    return db.query(SeasonModel).filter(SeasonModel.name == name).first()

def deactivate_season(db: Session, id: UUID4):
    try:
        db.execute(
            update(SeasonModel), [{"id": id, "active": False}]
        )
    except Exception as e:
        print(e)
        return True
    
    return False

def create_season(db: Session, season: SeasonCreate):
    active = True if season.active is None else season.active
    db_season = SeasonModel(name=season.name, start_dt=season.start_dt,
                            end_dt=season.end_dt, active=active)
    db.add(db_season)
    db.commit()
    db.refresh(db_season)
    return db_season
