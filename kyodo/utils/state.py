"""
thread_safe_state.py
====================
Thread-safe and async-safe dict-like state containers with optional per-key TTL.

ThreadSafeState  — for multi-threaded code (uses threading.RLock).
AsyncSafeState   — for asyncio code (uses asyncio.Lock).

Both classes expose a full dict-like API.
Note: AsyncSafeState intentionally has no __getitem__ / __setitem__ / __contains__
because Python does not support ``await`` inside dunder methods. Use the explicit
coroutine equivalents instead:
    await state.get(key)
    await state.set(key, value)
    await state.contains(key)
"""

from __future__ import annotations

from asyncio import Lock as ALock
from threading import RLock
from time import time
from typing import Any, AsyncIterator, Hashable, Iterator



class ThreadSafeState:
    """
    Thread-safe dict-like container with per-key TTL support.

    Uses ``threading.RLock`` so the same thread may acquire the lock
    recursively without deadlocking.

    Example::

        state = ThreadSafeState({"x": 1})
        state["y"] = 2
        state.set("z", 3, ttl=5.0)   # expires in 5 seconds
        print(state.get("z"))         # 3
        state.update({"a": 10, "b": 20})
        print(state.to_dict())
    """

    def __init__(self, initial: dict | None = None) -> None:
        self._data: dict[Hashable, Any] = dict(initial or {})
        self._ttl: dict[Hashable, float] = {}
        self._lock = RLock()



    def _is_expired(self, key: Hashable) -> bool:
        """Return True if *key* has a TTL that has already passed."""
        expire = self._ttl.get(key)
        return expire is not None and expire < time()

    def _cleanup(self, key: Hashable) -> bool:
        """
        Evict *key* if it is expired.

        Returns True if the key was removed, False otherwise.
        Must be called with the lock held.
        """
        if self._is_expired(key):
            self._data.pop(key, None)
            self._ttl.pop(key, None)
            return True
        return False

    def _cleanup_all(self) -> None:
        """
        Evict all expired keys in one pass.

        Builds the list of expired keys first to avoid mutating the dict
        during iteration. Must be called with the lock held.
        """
        now = time()
        expired = [k for k, v in self._ttl.items() if v < now]
        for k in expired:
            self._data.pop(k, None)
            self._ttl.pop(k, None)


    def set(self, key: Hashable, value: Any, ttl: float | None = None) -> Any:
        """
        Store *value* under *key*.

        Args:
            key:   Storage key.
            value: Value to store.
            ttl:   Optional lifetime in seconds. Pass ``None`` to make the
                   key persistent (removes any existing TTL).

        Returns:
            The stored value — useful for chaining.
        """
        with self._lock:
            self._data[key] = value
            if ttl is not None:
                self._ttl[key] = time() + ttl
            elif key in self._ttl:
                del self._ttl[key]
            return value

    def get(self, key: Hashable, default: Any = None) -> Any:
        """Return the value for *key*, or *default* if the key is missing or expired."""
        with self._lock:
            self._cleanup(key)
            return self._data.get(key, default)

    def pop(self, key: Hashable, *args: Any) -> Any:
        """
        Remove *key* and return its value.

        Mirrors ``dict.pop`` signature: an optional second argument is returned
        when the key is absent; without it a ``KeyError`` is raised.
        """
        with self._lock:
            self._ttl.pop(key, None)
            if args:
                return self._data.pop(key, args[0])
            return self._data.pop(key)

    def setdefault(self, key: Hashable, default: Any = None, ttl: float | None = None) -> Any:
        """
        Return the value for *key* if it exists and has not expired.

        Otherwise store *default* (with optional *ttl*) and return it.
        The entire operation is atomic — no other thread can interleave.
        """
        with self._lock:
            self._cleanup(key)
            if key not in self._data:
                # Write directly to avoid re-acquiring the reentrant lock,
                # keeping the whole operation atomic.
                self._data[key] = default
                if ttl is not None:
                    self._ttl[key] = time() + ttl
            return self._data[key]

    def update(self, mapping: dict | None = None, ttl: float | None = None, **kwargs: Any) -> None:
        """
        Merge *mapping* and/or keyword arguments into the state atomically.

        The entire update is performed under a single lock acquisition,
        so no other thread can observe a partially-updated state.

        Args:
            mapping: Optional dict of key-value pairs to merge.
            ttl:     Optional TTL in seconds applied to every updated key.
                     Pass ``None`` to keep each key persistent (removes its
                     existing TTL if any).
            **kwargs: Additional key-value pairs merged after *mapping*.
        """
        data = dict(mapping or {}, **kwargs)
        now = time()
        with self._lock:
            for k, v in data.items():
                self._data[k] = v
                if ttl is not None:
                    self._ttl[k] = now + ttl
                elif k in self._ttl:
                    del self._ttl[k]

    def clear(self) -> None:
        """Remove all keys and their TTLs."""
        with self._lock:
            self._data.clear()
            self._ttl.clear()

    def keys(self) -> list[str]:
        """Return a snapshot of live (non-expired) keys."""
        with self._lock:
            self._cleanup_all()
            return list(self._data.keys())

    def values(self) -> list[Any]:
        """Return a snapshot of values for all live keys."""
        with self._lock:
            self._cleanup_all()
            return list(self._data.values())

    def items(self) -> list[tuple[str, Any]]:
        """Return a snapshot of ``(key, value)`` pairs for all live keys."""
        with self._lock:
            self._cleanup_all()
            return list(self._data.items())

    def to_dict(self) -> dict:
        """Return a plain-dict snapshot of the current live state."""
        with self._lock:
            self._cleanup_all()
            return dict(self._data)


    def ttl_of(self, key: Hashable) -> float | None:
        """
        Return the remaining TTL for *key* in seconds, or ``None`` if the key
        has no expiry set.

        Returns ``0.0`` (not negative) if the key is expired but not yet evicted.
        """
        with self._lock:
            expire = self._ttl.get(key)
            if expire is None:
                return None
            return max(expire - time(), 0.0)

    def expire(self, key: Hashable, ttl: float) -> bool:
        """
        Set or update the TTL for an existing *key*.

        Returns:
            True  if the key exists and the TTL was applied.
            False if the key does not exist (or has already expired).
        """
        with self._lock:
            self._cleanup(key)
            if key not in self._data:
                return False
            self._ttl[key] = time() + ttl
            return True

    def persist(self, key: Hashable) -> bool:
        """
        Remove the TTL from *key*, making it persistent.

        Returns:
            True  if a TTL was removed.
            False if the key had no TTL.
        """
        with self._lock:
            if key in self._ttl:
                del self._ttl[key]
                return True
            return False


    def __getitem__(self, key: Hashable) -> Any:
        """Return ``self[key]``, raising ``KeyError`` if missing or expired."""
        with self._lock:
            self._cleanup(key)
            return self._data[key]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """Set ``self[key] = value`` with no TTL."""
        self.set(key, value)

    def __delitem__(self, key: Hashable) -> None:
        """Delete ``self[key]``, raising ``KeyError`` if missing."""
        with self._lock:
            self._ttl.pop(key, None)
            del self._data[key]

    def __contains__(self, key: Hashable) -> bool:
        """Return ``key in self``, respecting TTL expiry."""
        with self._lock:
            self._cleanup(key)
            return key in self._data

    def __len__(self) -> int:
        """Return the number of live (non-expired) keys."""
        with self._lock:
            self._cleanup_all()
            return len(self._data)

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over a snapshot of live keys.

        The snapshot is taken once under the lock, so mutations during
        iteration are safe and will not affect the current loop.
        """
        with self._lock:
            self._cleanup_all()
            return iter(list(self._data.keys()))

    def __bool__(self) -> bool:
        """Return ``True`` if there is at least one live key."""
        with self._lock:
            self._cleanup_all()
            return bool(self._data)

    def __eq__(self, other: object) -> bool:
        """
        Compare live state with another ``ThreadSafeState`` or a plain dict.

        Expired keys are excluded from both sides before comparison.
        """
        if isinstance(other, ThreadSafeState):
            return self.to_dict() == other.to_dict()
        if isinstance(other, dict):
            return self.to_dict() == other
        return NotImplemented

    def __repr__(self) -> str:
        with self._lock:
            self._cleanup_all()
            return f"ThreadSafeState({self._data!r}, ttl={self._ttl!r})"


class AsyncSafeState:
    """
    Asyncio-safe dict-like container with per-key TTL support.

    Uses ``asyncio.Lock``, which must be acquired with ``async with`` and
    therefore cannot be used inside regular dunder methods.  For this reason
    the public API consists entirely of explicit coroutines:

    * ``await state.get(key)``        instead of ``state[key]``
    * ``await state.set(key, value)`` instead of ``state[key] = value``
    * ``await state.contains(key)``   instead of ``key in state``
    * ``await state.length()``        instead of ``len(state)``

    Async iteration is supported via ``__aiter__``::

        async for key in state:
            ...

    ``__repr__`` is intentionally **not** protected by the lock; use it only
    for quick debugging.  For a consistent snapshot call ``await state.to_dict()``.

    Example::

        state = AsyncSafeState({"x": 1})
        await state.set("y", 2)
        await state.set("z", 3, ttl=5.0)   # expires in 5 seconds
        print(await state.get("z"))         # 3
        await state.update({"a": 10})
        print(await state.to_dict())
    """

    def __init__(self, initial: dict | None = None) -> None:
        self._data: dict[Hashable, Any] = dict(initial or {})
        self._ttl: dict[Hashable, float] = {}
        self._lock = ALock()


    def _is_expired(self, key: Hashable) -> bool:
        """Return True if *key* has a TTL that has already passed."""
        expire = self._ttl.get(key)
        return expire is not None and expire < time()

    def _cleanup(self, key: Hashable) -> bool:
        """
        Evict *key* if it is expired.

        Returns True if the key was removed. Must be called with the lock held.
        """
        if self._is_expired(key):
            self._data.pop(key, None)
            self._ttl.pop(key, None)
            return True
        return False

    def _cleanup_all(self) -> None:
        """
        Evict all expired keys in one pass.

        Must be called with the lock held.
        """
        now = time()
        expired = [k for k, v in self._ttl.items() if v < now]
        for k in expired:
            self._data.pop(k, None)
            self._ttl.pop(k, None)


    async def set(self, key: Hashable, value: Any, ttl: float | None = None) -> Any:
        """
        Store *value* under *key*.

        Args:
            key:   Storage key.
            value: Value to store.
            ttl:   Optional lifetime in seconds. Pass ``None`` to make the
                   key persistent (removes any existing TTL).

        Returns:
            The stored value.
        """
        async with self._lock:
            self._data[key] = value
            if ttl is not None:
                self._ttl[key] = time() + ttl
            elif key in self._ttl:
                del self._ttl[key]
            return value

    async def get(self, key: Hashable, default: Any = None) -> Any:
        """Return the value for *key*, or *default* if missing or expired."""
        async with self._lock:
            self._cleanup(key)
            return self._data.get(key, default)

    async def delete(self, key: Hashable) -> None:
        """Remove *key* silently (no error if absent)."""
        async with self._lock:
            self._data.pop(key, None)
            self._ttl.pop(key, None)

    async def pop(self, key: Hashable, *args: Any) -> Any:
        """
        Remove *key* and return its value.

        Mirrors ``dict.pop``: optional default as second argument, or
        ``KeyError`` if absent and no default given.
        """
        async with self._lock:
            self._ttl.pop(key, None)
            if args:
                return self._data.pop(key, args[0])
            return self._data.pop(key)

    async def setdefault(self, key: Hashable, default: Any = None, ttl: float | None = None) -> Any:
        """
        Return the value for *key* if it exists and has not expired.

        Otherwise store *default* (with optional *ttl*) and return it.
        The entire operation is atomic.
        """
        async with self._lock:
            self._cleanup(key)
            if key not in self._data:
                self._data[key] = default
                if ttl is not None:
                    self._ttl[key] = time() + ttl
            return self._data[key]

    async def update(self, mapping: dict | None = None, ttl: float | None = None, **kwargs: Any) -> None:
        """
        Merge *mapping* and/or keyword arguments into the state atomically.

        The entire update is performed under a single lock acquisition.

        Args:
            mapping: Optional dict of key-value pairs to merge.
            ttl:     Optional TTL in seconds applied to every updated key.
                     Pass ``None`` to keep each key persistent.
            **kwargs: Additional key-value pairs merged after *mapping*.
        """
        data = dict(mapping or {}, **kwargs)
        now = time()
        async with self._lock:
            for k, v in data.items():
                self._data[k] = v
                if ttl is not None:
                    self._ttl[k] = now + ttl
                elif k in self._ttl:
                    del self._ttl[k]

    async def clear(self) -> None:
        """Remove all keys and their TTLs."""
        async with self._lock:
            self._data.clear()
            self._ttl.clear()

    async def contains(self, key: Hashable) -> bool:
        """
        Return ``True`` if *key* is present and has not expired.

        Use this instead of ``key in state`` (which is not awaitable).
        """
        async with self._lock:
            self._cleanup(key)
            return key in self._data

    async def keys(self) -> list[str]:
        """Return a snapshot of live (non-expired) keys."""
        async with self._lock:
            self._cleanup_all()
            return list(self._data.keys())

    async def values(self) -> list[Any]:
        """Return a snapshot of values for all live keys."""
        async with self._lock:
            self._cleanup_all()
            return list(self._data.values())

    async def items(self) -> list[tuple[str, Any]]:
        """Return a snapshot of ``(key, value)`` pairs for all live keys."""
        async with self._lock:
            self._cleanup_all()
            return list(self._data.items())

    async def to_dict(self) -> dict:
        """Return a plain-dict snapshot of the current live state."""
        async with self._lock:
            self._cleanup_all()
            return dict(self._data)

    async def length(self) -> int:
        """
        Return the number of live (non-expired) keys.

        Use this instead of ``len(state)`` (which is not awaitable).
        """
        async with self._lock:
            self._cleanup_all()
            return len(self._data)

    async def ttl_of(self, key: Hashable) -> float | None:
        """
        Return the remaining TTL for *key* in seconds, or ``None`` if no
        expiry is set. Returns ``0.0`` (not negative) for already-expired keys.
        """
        async with self._lock:
            expire = self._ttl.get(key)
            if expire is None:
                return None
            return max(expire - time(), 0.0)

    async def expire(self, key: Hashable, ttl: float) -> bool:
        """
        Set or update the TTL for an existing *key*.

        Returns:
            True  if the key exists and the TTL was applied.
            False if the key does not exist (or has already expired).
        """
        async with self._lock:
            self._cleanup(key)
            if key not in self._data:
                return False
            self._ttl[key] = time() + ttl
            return True

    async def persist(self, key: Hashable) -> bool:
        """
        Remove the TTL from *key*, making it persistent.

        Returns:
            True  if a TTL was removed.
            False if the key had no TTL.
        """
        async with self._lock:
            if key in self._ttl:
                del self._ttl[key]
                return True
            return False

    async def __aiter__(self) -> AsyncIterator[str]:
        """
        Async-iterate over a snapshot of live keys.

        The snapshot is taken once under the lock; mutations during
        iteration are safe and will not affect the current loop.
        """
        keys = await self.keys()
        for key in keys:
            yield key

    def __repr__(self) -> str:
        # Not lock-protected — for quick debugging only.
        # For a consistent snapshot use: await state.to_dict()
        return f"AsyncSafeState({self._data!r}, ttl={self._ttl!r})"