from __future__ import annotations

from typing import Any

from ..models import Monitoramento
from ..pagination import AsyncAutoPaginator, AutoPaginator
from .base import AsyncBaseResource, BaseResource


class MonitoramentosResource(BaseResource):
    def criar(
        self,
        numero_processo: str,
        *,
        webhook_url: str | None = None,
        eventos: list[str] | None = None,
    ) -> Monitoramento:
        payload: dict[str, Any] = {"numero_processo": numero_processo}
        if webhook_url:
            payload["webhook_url"] = webhook_url
        if eventos:
            payload["eventos"] = eventos
        return Monitoramento.model_validate(self._post("/monitoramentos", json=payload))

    def listar(
        self,
        *,
        pagina: int = 1,
        limite: int = 20,
    ) -> dict[str, Any]:
        return self._get("/monitoramentos", params={"pagina": pagina, "limite": limite})

    def iterar(self, **kwargs: Any) -> AutoPaginator[dict[str, Any]]:
        limite = kwargs.pop("limite", 50)
        kwargs.pop("pagina", None)
        return AutoPaginator(self._client, "/monitoramentos", params=kwargs, limit=limite)

    def obter(self, monitor_id: int) -> Monitoramento:
        return Monitoramento.model_validate(self._get(f"/monitoramentos/{monitor_id}"))

    def remover(self, monitor_id: int) -> None:
        self._delete(f"/monitoramentos/{monitor_id}")


class AsyncMonitoramentosResource(AsyncBaseResource):
    async def criar(
        self,
        numero_processo: str,
        *,
        webhook_url: str | None = None,
        eventos: list[str] | None = None,
    ) -> Monitoramento:
        payload: dict[str, Any] = {"numero_processo": numero_processo}
        if webhook_url:
            payload["webhook_url"] = webhook_url
        if eventos:
            payload["eventos"] = eventos
        return Monitoramento.model_validate(await self._post("/monitoramentos", json=payload))

    async def listar(self, *, pagina: int = 1, limite: int = 20) -> dict[str, Any]:
        return await self._get("/monitoramentos", params={"pagina": pagina, "limite": limite})

    def iterar(self, **kwargs: Any) -> AsyncAutoPaginator[dict[str, Any]]:
        limite = kwargs.pop("limite", 50)
        kwargs.pop("pagina", None)
        return AsyncAutoPaginator(self._client, "/monitoramentos", params=kwargs, limit=limite)

    async def obter(self, monitor_id: int) -> Monitoramento:
        return Monitoramento.model_validate(await self._get(f"/monitoramentos/{monitor_id}"))

    async def remover(self, monitor_id: int) -> None:
        await self._delete(f"/monitoramentos/{monitor_id}")
