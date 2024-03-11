from sys import stdout
import logging
from typing import Annotated
from pydantic import UUID4

from fastapi import Depends, FastAPI, Security, HTTPException, Query
from fastapi.security import HTTPBearer, SecurityScopes
from sqlalchemy.orm import Session

from config import get_settings

from utils import VerifyToken

from crud import (get_seasons, create_season, create_association,
                  deactivate_season, get_associations,
                  deactivate_association)
from schemas import Season, SeasonCreate, Association

config = get_settings()

logging.basicConfig(stream=stdout,
                    level=config.log_level)
logger = logging.getLogger(__name__)

from database import get_db

token_auth_scheme = HTTPBearer()
auth = VerifyToken() 

app = FastAPI()

@app.get("/health")
def root():
    return {"message": "The API is LIVE!!"}

# season endpoints
@app.get("/seasons", response_model=list[Season])
def read_seasons(db: Session=Depends(get_db), skip: int=0, limit: int=100):
    return get_seasons(db, skip=skip, limit=limit)

@app.post("/season", response_model=SeasonCreate, status_code=201)
def new_season(season: SeasonCreate, db: Session=Depends(get_db),
               _: str = Security(auth.verify,
                                 scopes=['write:season'])):
    return create_season(db, item=season)

@app.delete("/season/{id}")
def delete_season(id: UUID4, db: Session=Depends(get_db),
                  _: str = Security(auth.verify,
                                    scopes=['delete:season'])):
    error = deactivate_season(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete, {id}!")
    return {"id": id}

# association endpoints
@app.get("/associations", response_model=list[Association])
def read_associations(db: Session=Depends(get_db), skip: int=0, limit: int=100):
    return get_associations(db, skip=skip, limit=limit)

@app.post("/association", response_model=Association, status_code=201)
def new_association(season: SeasonCreate, db: Session=Depends(get_db),
                    _: str = Security(auth.verify,
                    scopes=['write:association'])):
    return create_association(db, item=season)

@app.delete("/association/{id}")
def delete_association(id: UUID4, db: Session=Depends(get_db),
                        _: str = Security(auth.verify,
                        scopes=['delete:association'])):
    error = deactivate_association(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete, {id}!")
    return {"id": id}
