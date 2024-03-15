import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update, select
from pydantic import UUID4
from app.models import (Association as AssociationModel)
from app.schemas import Association

logger = logging.getLogger(__name__)

def get_associations(db: Session, skip: int=0, limit: int=100):
    stmt = select(AssociationModel).where(AssociationModel.active == True). \
        limit(limit=limit).offset(offset=skip)
    return db.execute(stmt).all()

def get_association_by_name(db: Session, name: str):
    return db.execute(select(AssociationModel). \
                      where(AssociationModel.name == name)).all()

def deactivate_association(db: Session, id: UUID4):
    temp = db.get(Association, id)
    if temp:
        msg = f"Association, {temp.name}, doesn't exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)
    try:
        db.execute(
            update(AssociationModel), [{"id": id, "active": False}]
        )
    except Exception as e:
        logger.error(e)
        return True
    
    return False

def create_association(db: Session, item: Association):
    temp = get_association_by_name(db, name=item.name)
    if temp:
        msg = f"Association, {temp.name}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)
    active = True if item.active is None else item.active
    db_item = AssociationModel(name=item.name, assignor_id=item.assignor_id,
                               president_id=item.president_id,
                               registrar_id=item.registrar_id, active=active)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
