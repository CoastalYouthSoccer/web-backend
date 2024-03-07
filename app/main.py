from fastapi import Depends, FastAPI, Security
from fastapi.security import HTTPBearer
from utils import VerifyToken

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
