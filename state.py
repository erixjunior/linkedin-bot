"""Global state manager untuk LinkedIn Bot."""

from typing import Any
from concurrent_map import ConcurrentMap


class Global:
    """Static class untuk manage global state dengan ConcurrentMap."""

    _store: ConcurrentMap = ConcurrentMap()

    @staticmethod
    def set(key: str, value: Any) -> None:
        """Simpan value ke global store."""
        Global._store.insert(key, value)

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Ambil value dari global store."""
        return Global._store.value(key, default)

    @staticmethod
    def contains(key: str) -> bool:
        """Cek apakah key ada di global store."""
        return Global._store.contains(key)

    @staticmethod
    def remove(key: str) -> bool:
        """Hapus key dari global store."""
        return Global._store.remove(key)

    @staticmethod
    def clear() -> None:
        """Hapus semua entries dari global store."""
        Global._store.clear()
