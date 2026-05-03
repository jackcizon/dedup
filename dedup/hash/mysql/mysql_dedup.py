from collections.abc import Callable
from typing import Any, AnyStr

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from dedup.hash.base import BaseDedup
from dedup.hash.mysql.models import Dedup
from dedup.hash.mysql.session import resources


class MysqlDedup(BaseDedup):
    def __init__(
            self,
            hash_func: Callable[[AnyStr], str] | None = None,
            url: str | None = None
    ) -> None:
        super().__init__(hash_func=hash_func)
        self.url = url

    async def async_ensure_storage(self, storage: Any = None) -> None:
        if storage is not None:
            self._storage = storage
        if self._storage is None:
            await resources.init(self.url)
            self._storage = resources.session_factory

    async def _async_save(self, hashed_data: str) -> Any:
        session: AsyncSession = self._storage()
        async with session as s:
            params = {'hashed_data': hashed_data}
            stat = insert(Dedup)
            await s.execute(stat, params)
            await s.commit()

    async def _async_is_exists(self, hashed_data: str) -> bool:
        session: AsyncSession = self._storage()
        async with session as s:
            stmt = select(Dedup).where(Dedup.hashed_data == hashed_data)
            result = await s.execute(stmt)
            return result.scalar_one_or_none() is not None
