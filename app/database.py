import uuid
from sqlalchemy import create_engine
from os import environ
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = environ.get("SQLALCHEMY_DATABASE_URL")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    type_annotation_map = {
        uuid.UUID: uuid.uuid4,
    }


def get_db():
    """Get a SQLAlchemy Session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
