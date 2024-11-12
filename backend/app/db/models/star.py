from sqlalchemy import Column, Integer, String, Double
from sqlalchemy.orm import relationship
# noinspection PyUnresolvedReferences
from .planet import Planet  # this import is used to avoid circular references in database

from .base import Base


class Star(Base):
    __tablename__ = 'star'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    # in light years
    distance_ly = Column(Double)
    # in solar mass
    mass_sm = Column(Double)

    # Establish one-to-many relationship with Planet
    planets = relationship("Planet", back_populates="star", cascade="all, delete-orphan")
