from typing import Optional

from pydantic import BaseModel, Field

from app.db.models import Star


class StarSchema(BaseModel):
    id: int
    name: str
    distance_ly: float
    mass_sm: float

    @classmethod
    def from_star(cls, star: Star) -> 'StarSchema':
        return cls(id=star.id, name=star.name, distance_ly=star.distance_ly, mass_sm=star.mass_sm)


class CreateStarRequest(BaseModel):
    name: str
    distance_ly: float
    mass_sm: float

    def to_star(self):
        return Star(name=self.name, distance_ly=self.distance_ly, mass_sm=self.mass_sm)


class UpdateStarRequest(BaseModel):
    id: int
    name: Optional[str] = Field(None)
    distance_ly: Optional[float] = Field(None)
    mass_sm: Optional[float] = Field(None)


class DeleteStarRequest(BaseModel):
    id: int
