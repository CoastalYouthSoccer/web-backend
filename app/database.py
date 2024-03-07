import uuid
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .guid import GUID

engine = create_engine(
    environ.get("SQLALCHEMY_DATABASE_URL")
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    type_annotation_map = {
        uuid.UUID: GUID,
    }