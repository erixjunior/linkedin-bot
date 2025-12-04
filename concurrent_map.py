"""Thread-safe concurrent map dengan Qt6 QMap style untuk LinkedIn Bot."""

import threading
from typing import Callable, Dict, Iterator, List, Optional, TypeVar, Generic

K = TypeVar("K")
V = TypeVar("V")


class ConcurrentMap(Generic[K, V]):
    """Thread-safe dictionary untuk concurrent access dari multiple threads."""

    def __init__(self) -> None:
        """Inisialisasi ConcurrentMap dengan empty internal dict dan lock."""
        self._data: Dict[K, V] = {}
        self._lock = threading.RLock()

    def insert(self, key: K, value: V) -> None:
        """Masukkan key-value pair ke dalam map."""
        with self._lock:
            self._data[key] = value

    def value(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Ambil value dari map berdasarkan key."""
        with self._lock:
            return self._data.get(key, default)

    def remove(self, key: K) -> bool:
        """Hapus key-value pair dari map, return True jika key ada."""
        with self._lock:
            if key in self._data:
                del self._data[key]
                return True
            return False

    def contains(self, key: K) -> bool:
        """Cek apakah key ada di dalam map."""
        with self._lock:
            return key in self._data

    def keys(self) -> List[K]:
        """Dapatkan list semua keys di map."""
        with self._lock:
            return list(self._data.keys())

    def values(self) -> List[V]:
        """Dapatkan list semua values di map."""
        with self._lock:
            return list(self._data.values())

    def items(self) -> List[tuple]:
        """Dapatkan list semua (key, value) pairs."""
        with self._lock:
            return list(self._data.items())

    def clear(self) -> None:
        """Hapus semua entries dari map."""
        with self._lock:
            self._data.clear()

    def count(self) -> int:
        """Dapatkan jumlah entries di dalam map."""
        with self._lock:
            return len(self._data)

    def isEmpty(self) -> bool:
        """Cek apakah map kosong."""
        with self._lock:
            return len(self._data) == 0

    def unite(self, other: Dict[K, V]) -> None:
        """Gabungkan semua entries dari dictionary lain ke dalam map."""
        with self._lock:
            self._data.update(other)

    def find(self, key: K) -> Optional[V]:
        """Cari value berdasarkan key, return None jika tidak ada."""
        with self._lock:
            return self._data.get(key)

    def insertMulti(self, key: K, value: V) -> None:
        """Masukkan key-value pair ke dalam map (overwrite jika ada)."""
        with self._lock:
            self._data[key] = value

    def take(self, key: K) -> Optional[V]:
        """Ambil dan hapus value dari map berdasarkan key."""
        with self._lock:
            return self._data.pop(key, None)

    def forEach(self, fn: Callable[[K, V], None]) -> None:
        """Eksekusi function untuk setiap key-value pair di map."""
        with self._lock:
            for key, value in self._data.items():
                fn(key, value)

    def __len__(self) -> int:
        """Return jumlah entries di map."""
        return self.count()

    def __getitem__(self, key: K) -> V:
        """Get value menggunakan bracket notation."""
        value = self.value(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key: K, value: V) -> None:
        """Set value menggunakan bracket notation."""
        self.insert(key, value)

    def __delitem__(self, key: K) -> None:
        """Delete key menggunakan del notation."""
        if not self.remove(key):
            raise KeyError(key)

    def __contains__(self, key: K) -> bool:
        """Check key existence menggunakan in operator."""
        return self.contains(key)

    def __iter__(self) -> Iterator[K]:
        """Iterate over keys."""
        with self._lock:
            return iter(list(self._data.keys()))

    def __repr__(self) -> str:
        """Return string representation dari ConcurrentMap."""
        with self._lock:
            return f"ConcurrentMap({self._data})"

    def __str__(self) -> str:
        """Return string output dari ConcurrentMap."""
        with self._lock:
            return str(self._data)
