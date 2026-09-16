from collections.abc import AsyncIterator, Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class AutoPaginator(Generic[T], Iterator[T]):
    def __init__(
        self,
        client: Any,
        path: str,
        params: dict[str, Any],
        limit: int = 50,
        *,
        page_param: str = "pagina",
        per_page_param: str = "limite",
        page_key: str = "pagina",
        per_page_key: str = "limite",
        total_key: str | None = None,
    ):
        self._client = client
        self._path = path
        self._params = params.copy()
        self._page_param = page_param
        self._per_page_param = per_page_param
        self._page_key = page_key
        self._per_page_key = per_page_key
        self._total_key = total_key
        self._params[per_page_param] = limit
        self._current_page = 1
        self._items: list[T] = []
        self._item_idx = 0
        self._total_pages = 1
        self._has_next = True
        self._fetched_first = False

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self._item_idx >= len(self._items):
            if self._fetched_first and not self._has_next:
                raise StopIteration

            self._params[self._page_param] = (
                self._current_page + 1 if self._fetched_first else self._current_page
            )
            resp = self._client.get(self._path, params=self._params)

            self._items = resp.get("items", [])
            self._current_page = resp.get(self._page_key, 1)
            self._total_pages = resp.get("paginas", 1)
            if self._total_key is not None:
                total = resp.get(self._total_key, 0)
                per_page = resp.get(self._per_page_key, self._params[self._per_page_param])
                self._has_next = self._current_page * per_page < total
            else:
                self._has_next = self._current_page < self._total_pages
            self._item_idx = 0
            self._fetched_first = True

            if not self._items:
                raise StopIteration

        item = self._items[self._item_idx]
        self._item_idx += 1
        return item


class AsyncAutoPaginator(Generic[T], AsyncIterator[T]):
    def __init__(
        self,
        async_client: Any,
        path: str,
        params: dict[str, Any],
        limit: int = 50,
        *,
        page_param: str = "pagina",
        per_page_param: str = "limite",
        page_key: str = "pagina",
        per_page_key: str = "limite",
        total_key: str | None = None,
    ):
        self._client = async_client
        self._path = path
        self._params = params.copy()
        self._page_param = page_param
        self._per_page_param = per_page_param
        self._page_key = page_key
        self._per_page_key = per_page_key
        self._total_key = total_key
        self._params[per_page_param] = limit
        self._current_page = 1
        self._items: list[T] = []
        self._item_idx = 0
        self._total_pages = 1
        self._has_next = True
        self._fetched_first = False

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        if self._item_idx >= len(self._items):
            if self._fetched_first and not self._has_next:
                raise StopAsyncIteration

            self._params[self._page_param] = (
                self._current_page + 1 if self._fetched_first else self._current_page
            )
            resp = await self._client.get(self._path, params=self._params)

            self._items = resp.get("items", [])
            self._current_page = resp.get(self._page_key, 1)
            self._total_pages = resp.get("paginas", 1)
            if self._total_key is not None:
                total = resp.get(self._total_key, 0)
                per_page = resp.get(self._per_page_key, self._params[self._per_page_param])
                self._has_next = self._current_page * per_page < total
            else:
                self._has_next = self._current_page < self._total_pages
            self._item_idx = 0
            self._fetched_first = True

            if not self._items:
                raise StopAsyncIteration

        item = self._items[self._item_idx]
        self._item_idx += 1
        return item
