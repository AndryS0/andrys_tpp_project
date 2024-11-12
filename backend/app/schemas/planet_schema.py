from typing import Optional

from pydantic import BaseModel, Field

from app.db.models import Planet


class PlanetSchema(BaseModel):
    id: int
    name: str
    diameter_km: float
    star_id: int

    @classmethod
    def from_planet(cls, planet: Planet) -> 'PlanetSchema':
        return cls(id=planet.id, name=planet.name, diameter_km=planet.diameter_km, star_id=planet.star_id)


class CreatePlanetRequest(BaseModel):
    name: str
    diameter_km: float
    star_id: int

    def to_planet(self):
        return Planet(name=self.name, diameter_km=self.diameter_km, star_id=self.star_id)


class UpdatePlanetRequest(BaseModel):
    id: int
    name: Optional[str] = Field(None)
    diameter_km: Optional[float] = Field(None)
    star_id: Optional[int] = Field(None)


class DeletePlanetRequest(BaseModel):
    id: int
