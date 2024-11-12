from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Satellite, Planet
from app.db.session import get_db_session
from app.schemas.satellite_schema import UpdateSatelliteRequest, CreateSatelliteRequest, SatelliteSchema


class SatelliteService:

    def __init__(self):
        pass

    async def add_new_satellite(self, satellite: CreateSatelliteRequest) -> SatelliteSchema:
        session: AsyncSession
        async with get_db_session() as session:
            parent_planet = (await session.execute(select(Planet).where(Planet.id == satellite.planet_id))).scalars().first()
            if parent_planet is None:
                raise HTTPException(status_code=400, detail="Planet not found")
            new_satellite = satellite.to_satellite()
            session.add(new_satellite)
            await session.flush()
            await session.refresh(new_satellite)
            satellite_schema = SatelliteSchema.from_satellite(new_satellite)
            await session.commit()
            return satellite_schema

    async def delete_satellite(self, id_: int):
        session: AsyncSession
        async with get_db_session() as session:
            await session.execute(delete(Satellite).where(Satellite.id == id_))
            await session.commit()

    async def get_satellite_by_id(self, id_: int) -> SatelliteSchema:
        session: AsyncSession
        async with get_db_session() as session:
            result = (await session.execute(select(Satellite).where(Satellite.id == id_))).scalars().first()
            return SatelliteSchema.from_satellite(result)

    async def get_satellites(self, limit: int = 50, offset: int = 0):
        session: AsyncSession
        async with get_db_session() as session:
            result = (await session.execute(select(Satellite).limit(limit).offset(offset))).scalars()
            return [SatelliteSchema.from_satellite(i) for i in result.all()]

    async def update_satellite(self, data: UpdateSatelliteRequest):
        session: AsyncSession
        values_to_update = {}
        if data.name:
            values_to_update['name'] = data.name
        if data.distance_from_planet:
            values_to_update['distance_from_planet'] = data.distance_from_planet
        if data.planet_id is not None:
            async with get_db_session() as session:
                if (await session.execute(select(Planet).where(Planet.id == data.planet_id))).scalars().first() is None:
                    raise HTTPException(status_code=400, detail="Planet not found")
                values_to_update['planet_id'] = data.planet_id
        async with get_db_session() as session:
            await session.execute(update(Satellite).values(**values_to_update).where(Satellite.id == data.id))
            new_satellite = await session.get_one(Satellite, data.id)
            satellite_schema = SatelliteSchema.from_satellite(new_satellite)
            await session.commit()
            return satellite_schema


_satellite_service = SatelliteService()


def get_satellite_service() -> SatelliteService:
    return _satellite_service
