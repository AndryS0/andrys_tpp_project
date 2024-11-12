from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Star, Planet
from app.db.session import get_db_session
from app.schemas.star_schema import UpdateStarRequest, CreateStarRequest, StarSchema


class StarService:

    def __init__(self):
        pass

    async def add_new_star(self, star: CreateStarRequest) -> StarSchema:
        session: AsyncSession
        async with get_db_session() as session:
            new_star = star.to_star()
            session.add(new_star)
            await session.flush()
            await session.refresh(new_star)
            star_schema = StarSchema.from_star(new_star)
            await session.commit()
            return star_schema

    async def delete_star(self, id_: int):
        session: AsyncSession
        async with get_db_session() as session:
            await session.execute(delete(Star).where(Star.id == id_))
            await session.commit()

    async def get_star_by_id(self, id_: int) -> StarSchema:
        session: AsyncSession
        async with get_db_session() as session:
            result = (await session.execute(select(Star).where(Star.id == id_))).scalars().first()
            return StarSchema.from_star(result)

    async def get_stars(self, limit: int = 50, offset: int = 0):
        session: AsyncSession
        async with get_db_session() as session:
            result = (await session.execute(select(Star).limit(limit).offset(offset))).scalars()
            return [StarSchema.from_star(i) for i in result.all()]

    async def update_star(self, data: UpdateStarRequest):
        session: AsyncSession
        values_to_update = {}
        if data.name:
            values_to_update['name'] = data.name
        if data.distance_ly:
            values_to_update['distance_ly'] = data.distance_ly
        if data.mass_sm:
            values_to_update['mass_sm'] = data.mass_sm
        async with get_db_session() as session:
            await session.execute(update(Star).values(**values_to_update).where(Star.id == data.id))
            updated_star = await session.get_one(Star, data.id)
            star_schema = StarSchema.from_star(updated_star)
            await session.commit()
            return star_schema


_star_service = StarService()


def get_star_service() -> StarService:
    return _star_service
