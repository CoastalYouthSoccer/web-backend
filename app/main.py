from sys import stdout
import logging
from typing import Annotated
from pydantic import UUID4

from fastapi import Depends, FastAPI, Security, HTTPException, Query
from fastapi.security import HTTPBearer
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

@app.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! You don't need to be "
                "authenticated to see this.")
    }
    return result

@app.get("/api/private")
def private(auth_result: str = Security(auth.verify)):
    result = {
        "status": "success",
        "msg": ("Hello from a private endpoint! You need to be "
                "authenticated to see this.")
    }
    return result

# season endpoints
@app.get("/seasons", response_model=list[Season])
def read_seasons(db: Session=Depends(get_db), skip: int=0, limit: int=100):
    return get_seasons(db, skip=skip, limit=limit)

@app.post("/season", response_model=SeasonCreate, status_code=201)
def new_season(season: SeasonCreate, db: Session=Depends(get_db)):
    return create_season(db, season=season)

@app.delete("/season/{id}")
def delete_season(id: UUID4, db: Session=Depends(get_db)):
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
def new_association(season: SeasonCreate, db: Session=Depends(get_db)):
    return create_association(db, season=season)

@app.delete("/association/{id}")
def delete_association(id: UUID4, db: Session=Depends(get_db)):
    error = deactivate_association(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete, {id}!")
    return {"id": id}
