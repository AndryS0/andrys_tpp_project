from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Planet, Star
from app.db.session import get_db_session
from app.schemas.planet_schema import UpdatePlanetRequest, CreatePlanetRequest, PlanetSchema


class PlanetService:

    def __init__(self):
        pass

    async def add_new_planet(self, planet: CreatePlanetRequest) -> PlanetSchema:
        session: AsyncSession
        async with get_db_session() as session:
            new_planet = planet.to_planet()
            parent_star = (await session.execute(select(Star).where(Star.id == planet.star_id))).scalars().first()
            if parent_star is None:
                raise HTTPException(status_code=400, detail="Star not found")
            session.add(new_planet)
            await session.flush()
            await session.refresh(new_planet)
            schema = PlanetSchema.from_planet(new_planet)
            await session.commit()
            return schema


    async def delete_planet(self, id_: int):
        session: AsyncSession
        async with get_db_session() as session:
            # noinspection PyTypeChecker
            await session.execute(delete(Planet).where(Planet.id == id_))
            await session.commit()

    async def get_planet_by_id(self, id_: int) -> PlanetSchema:
        session: AsyncSession
        async with get_db_session() as session:
            result = (await session.execute(select(Planet).where(Planet.id == id_))).scalars().first()
            return PlanetSchema.from_planet(result)

    async def get_planets(self, limit: int = 50, offset: int = 0):
        session: AsyncSession
        async with get_db_session() as session:
            result = (await session.execute(select(Planet).limit(limit).offset(offset))).scalars()
            return [PlanetSchema.from_planet(i) for i in result.all()]

    async def update_planet(self, data: UpdatePlanetRequest):
        session: AsyncSession
        values_to_update = {}
        if data.name:
            values_to_update['name'] = data.name
        if data.star_id:
            values_to_update['star_id'] = data.star_id
        if data.diameter_km:
            values_to_update['diameter_km'] = data.diameter_km
        async with get_db_session() as session:
            if data.star_id is not None:
                if (
                await session.execute(select(Star).limit(1).where(Star.id == data.star_id))).scalars().first() is None:
                    raise HTTPException(status_code=400, detail='Star not found')
            await session.execute(update(Planet).values(**values_to_update).where(Planet.id == data.id))
            planet = await session.get_one(Planet, data.id)
            schema = PlanetSchema.from_planet(planet)
            await session.commit()
            return schema


_planet_service = PlanetService()


def get_planet_service() -> PlanetService:
    return _planet_service
