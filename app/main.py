from fastapi import Depends, FastAPI, Security, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from utils import VerifyToken

from crud import get_seasons
from schemas import Season
from database import SessionLocal, engine, get_db

#models.Base.metadata.create_all(bind=engine)

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

@app.get("/seasons", response_model=list[Season])
def read_users(db: Session = Depends(get_db), skip: int=0, limit: int=100):
    seasons = get_seasons(db=db, skip=skip, limit=limit)
    return seasons
