from collections.abc import Callable
from typing import AnyStr, Any

from redis.asyncio import Redis

from dedup.hash.base import BaseDedup


class RedisDedup(BaseDedup):
    def __init__(
            self,
            hash_func: Callable[[AnyStr], str] | None = None,
            url: str | None = "redis://@localhost:6379/0",
            name: str | None = "dedup"
    ):
        super().__init__(hash_func=hash_func)
        self.url = url
        self.name = name

    def sync_ensure_storage(self, storage: Any = None) -> None:
        if self.storage is None:
            self._storage = storage or Redis.from_url(self.url)

    async def _async_save(self, hashed_datas: str) -> int:
        count = await self._storage.sadd(self.name, hashed_datas)
        return count

    async def _async_is_exists(self, hashed_data: str) -> bool:
        return bool(await self._storage.sismember(self.name, hashed_data))
