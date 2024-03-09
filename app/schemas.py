from uuid import uuid4
from enum import Enum
from datetime import date, datetime
from pydantic import BaseModel
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
    id: uuid4


class BaseCreate(Base):
    pass


class Coach(Base):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    active: bool
    season_id: uuid4

    class Config:
        from_attributes = True


class Team(Base):
    name: str
    division_id: uuid4
    season_id: uuid4
    coach_id: uuid4
    active: bool

    class Config:
        from_attributes = True


class Game(Base):
    game_dt: datetime
    location_id: uuid4
    season_id: uuid4
    home_team_id: uuid4
    away_team_id: uuid4
    home_score: uuid4
    away_score: uuid4
    status: GameStatus


class Season(Base):
    name: str
    start_dt: date
    end_dt: date
    active: bool
    coaches: list[Coach] = []
    teams: list[Team] = []
    games: list[Game] = []

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
    venue_id: uuid4
    games: list[Game] = []

    class Config:
        from_attributes = True


class Venue(Base):
    name: str
    address_id: uuid4
    active: bool
    sub_venues: list[SubVenue] = []

    class Config:
        from_attributes = True


class Division(Base):
    name: str
    active: bool
    teams: list[Team] = []
