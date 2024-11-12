from sqlalchemy import Column, Integer, String, ForeignKey, Double
from sqlalchemy.orm import relationship

from .base import Base


class Satellite(Base):
    __tablename__ = 'satellite'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    distance_from_planet = Column(Double)
    planet_id = Column(Integer, ForeignKey('planet.id', ondelete='CASCADE'))  # ForeignKey to reference Planet

    # Relationship back to Planet
    planet = relationship("Planet", back_populates="satellites")
