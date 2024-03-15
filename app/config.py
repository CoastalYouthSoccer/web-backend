from os import environ
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorithms: str
    sqlalchemy_database_url: str
    log_level: int = 30

    class Config:
        print(environ.get("ENV_FILE", ".env"))
        env_file = environ.get("ENV_FILE", ".env")

def get_settings():
    return Settings()
