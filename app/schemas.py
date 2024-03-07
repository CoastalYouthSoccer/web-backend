import uuid
from pydantic import BaseModel


class Base(BaseModel):
    id: uuid.UUID


class BaseCreate(Base):
    pass


class Address(Base):
    address1: str
    address2: str
    city: str
    state: str
    zip_code: str

    class Config:
        orm_mode = True


class SubVenue(Base):
    name: str
    plus_code: str
    active: bool
#    venue_id = Column(Integer, ForeignKey(VENUE_ID))
#    venue = relationship("Venue",
#                          back_populates="sub_venue")
#    games = relationship("Game",
#                          back_populates="sub_venue")


class Venue(Base):
    name: str
#    address_id = Column(Integer, ForeignKey('address.id'))
    active: bool
#    address = relationship("Address",
#                          back_populates="venue")
    sub_venues: list[SubVenue] = []

    
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True