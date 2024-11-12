from typing import Optional

from pydantic import BaseModel, Field

from app.db.models import Satellite


class SatelliteSchema(BaseModel):
    id: int
    name: str
    distance_from_planet: float
    planet_id: int

    @classmethod
    def from_satellite(cls, satellite: Satellite) -> 'SatelliteSchema':
        return cls(id=satellite.id, name=satellite.name, distance_from_planet=satellite.distance_from_planet, planet_id=satellite.planet_id)


class CreateSatelliteRequest(BaseModel):
    name: str
    distance_from_planet: float
    planet_id: int

    def to_satellite(self):
        return Satellite(name=self.name, distance_from_planet=self.distance_from_planet, planet_id=self.planet_id)


class UpdateSatelliteRequest(BaseModel):
    id: int
    name: Optional[str] = Field(None)
    distance_from_planet: Optional[float] = Field(None)
    planet_id: Optional[int] = Field(None)


class DeleteSatelliteRequest(BaseModel):
    id: int
