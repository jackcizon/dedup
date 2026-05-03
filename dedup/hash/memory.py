from collections.abc import Callable
from typing import Any, AnyStr

from dedup.hash.base import BaseDedup


class MemoryDedup(BaseDedup):
    def __init__(self, hashed_func: Callable[[AnyStr], str] | None = None):
        super().__init__(hashed_func)

    def _sync_is_exists(self, hashed_data: str) -> bool:
        return hashed_data in self.storage

    def _sync_save(self, hashed_data: str) -> Any:
        self._storage.add(hashed_data)

    def ensure_storage(self, storage: Any = None) -> None:
        if self.storage is None:
            self._storage = storage or set()
