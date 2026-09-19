from __future__ import annotations

from typing import Any

import httpx

from ._version import __version__
from .exceptions import (
    AuthenticationError,
    CourtIQError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .resources.monitoramentos import AsyncMonitoramentosResource, MonitoramentosResource
from .resources.processos import AsyncProcessosResource, ProcessosResource
from .resources.webhooks import AsyncWebhooksResource, WebhooksResource

_ENVS = {
    "production": "https://api.courtiq.com.br/v1",
    "sandbox": "https://sandbox.courtiq.com.br/v1",
}


def _raise_for_status(response: httpx.Response) -> Any:
    if response.status_code == 401:
        raise AuthenticationError()
    if response.status_code == 404:
        data = response.json() if response.content else {}
        raise NotFoundError(data.get("detail", "Recurso não encontrado."))
    if response.status_code == 422:
        data = response.json() if response.content else {}
        raise ValidationError(
            data.get("detail", "Parâmetros inválidos."),
            errors=data.get("errors", []),
        )
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", "60"))
        raise RateLimitError(retry_after=retry_after)
    if response.status_code >= 500:
        raise ServerError()
    if response.status_code >= 400:
        data = response.json() if response.content else {}
        raise CourtIQError(
            message=data.get("detail", "Erro desconhecido."),
            status_code=response.status_code,
        )

    if response.status_code == 204 or not response.content:
        return None
    return response.json()


class CourtIQ:
    def __init__(
        self,
        api_key: str,
        *,
        environment: str = "production",
        base_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        if not api_key:
            raise ValueError("api_key é obrigatório.")

        self._api_key = api_key
        self._base_url = base_url or _ENVS.get(environment, _ENVS["production"])

        transport = httpx.HTTPTransport(retries=max_retries)
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"courtiq-python/{__version__}",
            },
            timeout=httpx.Timeout(timeout),
            transport=transport,
        )

        self.processos = ProcessosResource(self)
        self.monitoramentos = MonitoramentosResource(self)
        self.webhooks = WebhooksResource(self)

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        response = self._client.request(method, path, **kwargs)
        return _raise_for_status(response)

    def get(self, path: str, **kwargs: Any) -> Any:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Any:
        return self._request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Any:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self._request("DELETE", path, **kwargs)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> CourtIQ:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncCourtIQ:
    def __init__(
        self,
        api_key: str,
        *,
        environment: str = "production",
        base_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        if not api_key:
            raise ValueError("api_key é obrigatório.")

        self._api_key = api_key
        self._base_url = base_url or _ENVS.get(environment, _ENVS["production"])

        transport = httpx.AsyncHTTPTransport(retries=max_retries)
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"courtiq-python/{__version__}",
            },
            timeout=httpx.Timeout(timeout),
            transport=transport,
        )

        self.processos = AsyncProcessosResource(self)
        self.monitoramentos = AsyncMonitoramentosResource(self)
        self.webhooks = AsyncWebhooksResource(self)

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        response = await self._client.request(method, path, **kwargs)
        return _raise_for_status(response)

    async def get(self, path: str, **kwargs: Any) -> Any:
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> Any:
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> Any:
        return await self._request("PUT", path, **kwargs)

    async def patch(self, path: str, **kwargs: Any) -> Any:
        return await self._request("PATCH", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Any:
        return await self._request("DELETE", path, **kwargs)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncCourtIQ:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
