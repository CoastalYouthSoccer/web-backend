import enum
from uuid import uuid4
from typing import List, Optional
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (Boolean, ForeignKey, String, Date, DateTime,
                        Enum)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import expression

from database import Base

PERSON_ID = "person.id"
TEAM_ID = "team.id"
VENUE_ID = "venue.id"
SEASON_ID = "season.id"


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
    id: Mapped[uuid4] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))
    start_dt: Mapped[Date] = mapped_column(Date)
    end_dt: Mapped[Date] = mapped_column(Date)
    active: Mapped[bool] = mapped_column(Boolean, server_default=expression.true())
#    teams: Mapped[List["Team"]] = relationship(back_populates="season")
#    coaches: Mapped[List["Coach"]] = relationship(back_populates="season")
#    games: Mapped[List["Game"]] = relationship(back_populates="season")


class Address(Base):
    __tablename__ = 'address'
    id: Mapped[uuid4] = mapped_column(UUID, primary_key=True, default=uuid4)
    address1: Mapped[str] = mapped_column(String(100))
# Address2 is optional
    address2: Mapped[str]
    city: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(50))
    zip_code: Mapped[str] = mapped_column(String(15))
    venue: Mapped[List["Venue"]] = relationship(back_populates="address")


class Venue(Base):
    __tablename__ = 'venue'
    id: Mapped[uuid4] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50))
    address_id: Mapped[uuid4] = mapped_column(UUID, ForeignKey('address.id'))
    active: Mapped[bool] = mapped_column(Boolean, server_default=expression.true())
    address: Mapped["Address"] = relationship(back_populates="venue")
    sub_venue: Mapped[List["SubVenue"]] = relationship(
                            back_populates="venue")


class SubVenue(Base):
    """ Table for individual fields within a Venue """
    __tablename__ = 'sub_venue'
    id: Mapped[uuid4] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50))
    venue_id: Mapped[uuid4] = mapped_column(UUID, ForeignKey(VENUE_ID))
    active: Mapped[bool] = mapped_column(Boolean, server_default=expression.true())
    venue: Mapped["Venue"] = relationship(back_populates="sub_venue",
                          primaryjoin="SubVenue.venue_id==Venue.id")
    games: Mapped[List["Game"]] = relationship(back_populates="sub_venue")


class Division(Base):
    """ Table defining a division """
    __tablename__ = 'division'
    id: Mapped[uuid4] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(Boolean, default=True,
                                         server_default=expression.true())
    teams: Mapped[List["Team"]] = relationship(back_populates="division")


class Coach(Base):
    """ Table defining a coach """
    __tablename__ = 'coach'
    auth_id: Mapped[uuid4] = mapped_column(String(100), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str]
    season_id: Mapped[uuid4] = mapped_column(UUID, ForeignKey(SEASON_ID))
    active: Mapped[bool] = mapped_column(Boolean, default=True,
                                         server_default=expression.true())
    team: Mapped[List["Team"]] = relationship(back_populates="coaches")
    season: Mapped[List["Season"]] = relationship(back_populates="coaches")


class Team(Base):
    """ Table defining a team """
    __tablename__ = 'team'
    id: Mapped[uuid4] = mapped_column(UUID, primary_key=True, default=uuid4)
    division_id: Mapped[uuid4] = mapped_column(UUID, ForeignKey('division.id'))
    season_id: Mapped[uuid4] = mapped_column(UUID, ForeignKey(SEASON_ID))
    coach_id: Mapped[uuid4] = mapped_column(String, ForeignKey('coach.auth_id'))

    gender: Mapped[str] = mapped_column(String(5), default="Boys")
    name: Mapped[str] = mapped_column(String(100))
    division: Mapped["Division"] = relationship(back_populates="teams")
    coaches: Mapped["Coach"] = relationship(back_populates="team")
    season: Mapped["Season"] = relationship(back_populates="teams")
    active: Mapped[bool] = mapped_column(Boolean, default=True,
                                         server_default=expression.true())


class Game(Base):
    __tablename__ = 'game'
    id: Mapped[uuid4] = mapped_column(UUID, primary_key=True, default=uuid4)
    game_dt: Mapped[DateTime] = mapped_column(DateTime)
    sub_venue_id: Mapped[uuid4] = mapped_column(UUID, ForeignKey('sub_venue.id'))
    season_id: Mapped[uuid4] = mapped_column(UUID, ForeignKey(SEASON_ID))
    home_team_id: Mapped[uuid4] = mapped_column(UUID, ForeignKey(TEAM_ID))
    away_team_id: Mapped[uuid4] = mapped_column(UUID, ForeignKey(TEAM_ID))
    home_score: Mapped[int]
    away_score: Mapped[int]
    status: Mapped[Enum[GameStatus]] = mapped_column(Enum(GameStatus))
    sub_venue: Mapped["SubVenue"] = relationship(back_populates="games")
    home_team: Mapped["Team"] = relationship(back_populates="games",
                                             primaryjoin='Game.home_team_id == Team.id')
    away_team: Mapped["Team"] = relationship(back_populates="games",
                                             primaryjoin='Game.away_team_id == Team.id')
    season: Mapped["Season"] = relationship(back_populates="games")
