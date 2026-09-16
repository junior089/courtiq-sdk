from __future__ import annotations

from typing import Any, TypeVar, cast

T = TypeVar("T")


class BaseResource:
    def __init__(self, client: Any) -> None:
        self._client = client

    def _get(self, path: str, _response_type: type[T] | None = None, **kwargs: Any) -> T:
        return cast(T, self._client.get(path, **kwargs))

    def _post(self, path: str, _response_type: type[T] | None = None, **kwargs: Any) -> T:
        return cast(T, self._client.post(path, **kwargs))

    def _put(self, path: str, _response_type: type[T] | None = None, **kwargs: Any) -> T:
        return cast(T, self._client.put(path, **kwargs))

    def _patch(self, path: str, _response_type: type[T] | None = None, **kwargs: Any) -> T:
        return cast(T, self._client.patch(path, **kwargs))

    def _delete(self, path: str, _response_type: type[T] | None = None, **kwargs: Any) -> T:
        return cast(T, self._client.delete(path, **kwargs))


class AsyncBaseResource:
    def __init__(self, client: Any) -> None:
        self._client = client

    async def _get(self, path: str, **kwargs: Any) -> T:
        return cast(T, await self._client.get(path, **kwargs))

    async def _post(self, path: str, **kwargs: Any) -> T:
        return cast(T, await self._client.post(path, **kwargs))

    async def _put(self, path: str, **kwargs: Any) -> T:
        return cast(T, await self._client.put(path, **kwargs))

    async def _patch(self, path: str, **kwargs: Any) -> T:
        return cast(T, await self._client.patch(path, **kwargs))

    async def _delete(self, path: str, **kwargs: Any) -> T:
        return cast(T, await self._client.delete(path, **kwargs))
