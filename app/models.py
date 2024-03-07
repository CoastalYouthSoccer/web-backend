from datetime import date
import enum
import uuid
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, Date,
                        DateTime, Enum)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import expression

from .database import Base

PERSON_ID = "person.id"
TEAM_ID = "team.id"
VENUE_ID = "venue.id"


class Gender(enum.Enum):
    """Gender enum"""
    OTHER = 0
    MALE = 1
    FEMALE = 2
    UNDEFINED = 99


class GameStatus(enum.Enum):
    """ Level Type """
    UNDEFINED = 0
    SCHEDULED = 1
    COMPLETED = 2
    CANCELED = 3
    RESCHEDULED = 4
    FORFEIT = 5


class Season(Base):
    __tablename__ = 'season'
    id = Mapped[uuid.UUID] = mapped_column(primary_key=True)

    name = Column(String(100))
    start_dt = Column(Date)
    end_dt = Column(Date)
    teams = relationship("Team",
                          back_populates="season")
    coaches = relationship("Coach",
                           back_populates="season")
    games = relationship("Game",
                           back_populates="season")


class Address(Base):
    __tablename__ = 'address'
    id = Mapped[uuid.UUID] = mapped_column(primary_key=True)

    address1 = Column(String(100))
    address2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(15))
    venue = relationship("Venue",
                            back_populates="address")


class Venue(Base):
    __tablename__ = 'venue'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    name = Column(String(50))
    address_id = Column(Integer, ForeignKey('address.id'))
    active = Column(Boolean)
    address = relationship("Address",
                          back_populates="venue")
    sub_venue = relationship("SubVenue",
                            back_populates="venue")


class SubVenue(Base):
    """ Table for individual fields within a Venue """
    __tablename__ = 'sub_venue'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    name = Column(String(50))
    venue_id = Column(Integer, ForeignKey(VENUE_ID))
    plus_code = Column(String(50))
    active = Column(Boolean)
    venue = relationship("Venue",
                          back_populates="sub_venue")
    games = relationship("Game",
                          back_populates="sub_venue")

class Division(Base):
    """ Table defining a division """
    __tablename__ = 'division'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    name = Column(String(100))
    active = Column(Boolean, default=True, server_default=expression.true())
    teams = relationship("Team",
                          back_populates="division")

class Coach(Base):
    """ Table defining a coach """
    __tablename__ = 'coach'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    season_id = Column(Integer, ForeignKey('season.id'))
    active = Column(Boolean, default=True, server_default=expression.true())
    teams = relationship("Team",
                          back_populates="coach")

class Team(Base):
    """ Table defining a team """
    __tablename__ = 'team'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    division_id = Column(Integer, ForeignKey('division.id'))
    season_id = Column(Integer, ForeignKey('season.id'))

#    gender = Column(Enum(Gender))
    name = Column(String(100))
    division = relationship("Division",
                          back_populates="teams")
    coaches = relationship("Coach",
                           back_populates="teams")
    season = relationship("Season",
                          back_populates="teams")
    active = Column(Boolean, default=True, server_default=expression.true())


class Game(Base):
    __tablename__ = 'game'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    game_dt = Column(DateTime)
    location_id = Column(Integer, ForeignKey('location.id'))
    home_team_id = Column(Integer, ForeignKey(TEAM_ID))
    away_team_id = Column(Integer, ForeignKey(TEAM_ID))
    home_score = Column(Integer)
    away_score = Column(Integer)
    status = Column(Enum(GameStatus))
    location = relationship("Location",
                          back_populates="games")
    home_team = relationship("Team",
                          primaryjoin='Game.home_team_id == Team.id')
    away_team = relationship("Team",
                          primaryjoin='Game.away_team_id == Team.id')
    season = relationship("Season",
                          back_populates="games")