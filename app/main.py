from typing import Annotated
from pydantic import UUID4

from fastapi import Depends, FastAPI, Security, HTTPException, Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from utils import VerifyToken

from crud import get_seasons, create_season, get_season_by_name, deactivate_season
from schemas import Season, SeasonCreate
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
    """A valid access token is required to access this route"""
    return auth_result

@app.get("/seasons/", response_model=list[Season])
def read_seasons(db: Session = Depends(get_db), skip: int=0, limit: int=100):
    return get_seasons(db, skip=skip, limit=limit)

@app.post("/season/", response_model=SeasonCreate, status_code=201)
def new_season(season: SeasonCreate, db: Session = Depends(get_db)):
    temp = get_season_by_name(db, name=season.name)
    if temp:
        raise HTTPException(status_code=400,
                            detail=f"Season, {season.name}, already exists!")
    return create_season(db, season=season)

@app.delete("/season/{id}")
def delete_season(id: UUID4, season: Season, db: Session = Depends(get_db)):
    error = deactivate_season(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete, {id}!")
    return {"id": id}

