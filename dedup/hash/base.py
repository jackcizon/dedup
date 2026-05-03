import hashlib
from collections.abc import Callable
from typing import Any, AnyStr

from dedup.hash._interface import DedupInterface


class BaseDedup(DedupInterface):
    def __init__(self, hash_func: Callable[[AnyStr], str] | None = None) -> None:
        self._hash_func = hash_func or self.md5_
        self._storage = None

    @property
    def storage(self) -> Any:
        return self._storage

    @staticmethod
    def md5_(data: AnyStr) -> str:
        if isinstance(data, str):
            data = data.encode()
        return hashlib.md5(data).hexdigest()

    def sync_ensure_storage(self, storage: Any = None) -> None:
        raise NotImplementedError

    async def async_ensure_storage(self, storage: Any = None) -> None:
        raise NotImplementedError

    def sync_is_exists(self, data: str) -> bool:
        hashed_data = self._hash_func(data)
        return self._sync_is_exists(hashed_data)

    def _sync_is_exists(self, hashed_data: str) -> bool:
        raise NotImplementedError

    async def async_is_exists(self, data: str) -> bool:
        hashed_data = self._hash_func(data)
        return await self._async_is_exists(hashed_data)

    async def _async_is_exists(self, hashed_data: str) -> bool:
        raise NotImplementedError

    def sync_save(self, data: AnyStr) -> Any:
        if self.storage is None:
            self.sync_ensure_storage()
        if self.storage is None:
            raise RuntimeError("storage not initialized")
        hashed_data = self._hash_func(data)
        return self._sync_save(hashed_data)

    def _sync_save(self, hashed_data: str) -> Any:
        raise NotImplementedError

    async def async_save(self, data: AnyStr) -> Any:
        if self.storage is None:
            await self.async_ensure_storage()
        if self.storage is None:
            raise RuntimeError("storage not initialized")
        hashed_data = self._hash_func(data)
        return await self._async_save(hashed_data)

    async def _async_save(self, hashed_data: str) -> Any:
        raise NotImplementedError
