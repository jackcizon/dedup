from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from dedup.hash.mysql.models import Base


class ResourceManager:
    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_factory = None

    async def init(self, db_url: str | None = None) -> None:
        if db_url and self.engine is None:
            self.engine = create_async_engine(db_url, pool_pre_ping=True)
            self.session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False)

            async with resources.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    async def aclose(self) -> None:
        if self.engine:
            await self.engine.dispose()


resources = ResourceManager()
