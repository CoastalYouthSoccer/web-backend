from enum import Enum
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, StringConstraints, UUID4
from typing_extensions import Annotated

#from pydantic_extra_types import phone_numbers


class GameStatus(Enum):
    """ Level Type """
    UNDEFINED = 0
    SCHEDULED = 1
    COMPLETED = 2
    CANCELED = 3
    RESCHEDULED = 4
    FORFEIT = 5


class Base(BaseModel):
    id: UUID4


class BaseCreate(BaseModel):
    pass


class Coach(Base):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    active: bool

    class Config:
        from_attributes = True


class Team(Base):
    name: str
    division_id: UUID4
    season_id: UUID4
    coach_id: UUID4
    active: bool

    class Config:
        from_attributes = True


class Game(Base):
    game_dt: datetime
    location_id: UUID4
    season_id: UUID4
    home_team_id: UUID4
    away_team_id: UUID4
    home_score: UUID4
    away_score: UUID4
    status: GameStatus

    class Config:
        from_attributes = True


class Season(BaseModel):
    id: UUID4
    name: Annotated[str, StringConstraints(max_length=100)]
    start_dt: date
    end_dt: date
    active: bool
    teams: Optional[list[Team]] = []
    games: Optional[list[Game]] = []

    class Config:
        from_attributes = True

class SeasonCreate(BaseCreate):
    name: str
    start_dt: date
    end_dt: date
    active: Optional[bool] = True

    class Config:
        from_attributes = True


class Association(BaseModel):
    id: UUID4
    name: str
    assignor_id: Optional[UUID4]
    president_id: Optional[UUID4]
    registrar_id: Optional[UUID4]

    class Config:
        from_attributes = True


class Address(Base):
    address1: str
    address2: str
    city: str
    state: str
    zip_code: str

    class Config:
        from_attributes = True


class SubVenue(Base):
    name: str
    plus_code: str
    active: bool
    venue_id: UUID4
    games: list[Game] = []

    class Config:
        from_attributes = True


class Venue(Base):
    name: str
    address_id: UUID4
    active: bool
    sub_venues: list[SubVenue] = []

    class Config:
        from_attributes = True


class Division(Base):
    name: str
    active: bool
    teams: list[Team] = []

    class Config:
        from_attributes = True
