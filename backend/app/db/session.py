import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncConnection, AsyncSession

from app.core import settings


# cc: https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308
class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception as e:
            print(f'Rolling back due to exception: {e.with_traceback(e.__traceback__)}')
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(
    settings.database_url, {
        "pool_size": 30,  # Maximum number of connections in the pool
        "max_overflow": 30,  # Maximum number of connections that can be created beyond the pool_size
        "pool_timeout": 15,  # Maximum number of seconds to wait before giving up on getting a connection
        "pool_recycle": 900,  # Recycle connections after 15 minutes (to avoid stale connections)
        "pool_pre_ping": True  # Enable the connection pool "pre-ping" feature to detect stale connections
    }
)


@contextlib.asynccontextmanager
async def get_db_session():
    try:
        async with sessionmanager.session() as session:
            yield session
    except Exception as e:
        raise e
