import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update, select
from pydantic import UUID4
from app.models import (Season as SeasonModel)
from app.schemas import SeasonCreate
logger = logging.getLogger(__name__)

def get_seasons(db: Session, skip: int=0, limit: int=100):
    stmt = select(SeasonModel).where(SeasonModel.active == True). \
        limit(limit=limit).offset(offset=skip)
    return db.scalars(stmt).all()

def get_season_by_name(db: Session, name: str):
    return db.execute(select(SeasonModel). \
                      where(SeasonModel.name == name)).all()

def deactivate_season(db: Session, id: UUID4):
    try:
        temp = db.get(SeasonModel, id)
        if temp:
            msg = f"Season, {temp.name}, already exists!"
            logger.info(msg)
            raise HTTPException(status_code=400, detail=msg)
        db.execute(
            update(SeasonModel), [{"id": id, "active": False}]
        )
    except Exception as e:
        logger.error(e)
        return True
    
    return False

def create_season(db: Session, item: SeasonCreate):
    temp = get_season_by_name(db, name=item.name)
    if temp:
        msg = f"Season, {item.name}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)

    active = True if item.active is None else item.active
    db_item = SeasonModel(name=item.name, start_dt=item.start_dt,
                            end_dt=item.end_dt, active=active)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item