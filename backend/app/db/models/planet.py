from sqlalchemy import Column, Integer, String, ForeignKey, Double
from sqlalchemy.orm import relationship
# noinspection PyUnresolvedReferences
from .satellite import Satellite  # this import is used to avoid circular references in database

from .base import Base


class Planet(Base):
    __tablename__ = 'planet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    diameter_km = Column(Double)

    star_id = Column(Integer, ForeignKey('star.id', ondelete='CASCADE'))  # ForeignKey to reference the Star table

    # Link back to Star
    star = relationship("Star", back_populates="planets")
    # One-to-many relationship with Satellite
    satellites = relationship("Satellite", back_populates="planet", cascade="all, delete-orphan")
