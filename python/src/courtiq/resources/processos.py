from __future__ import annotations

from typing import Any

from ..models import Processo
from ..pagination import AsyncAutoPaginator, AutoPaginator
from .base import AsyncBaseResource, BaseResource


def _list_params(
    *,
    tribunal: str | None,
    parte: str | None,
    advogado: str | None,
    data_inicio: str | None,
    data_fim: str | None,
    page: int,
    per_page: int,
    pagina: int | None,
    limite: int | None,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "page": pagina if pagina is not None else page,
        "per_page": limite if limite is not None else per_page,
    }
    if tribunal:
        params["tribunal"] = tribunal
    if parte:
        params["parte"] = parte
    if advogado:
        params["advogado"] = advogado
    if data_inicio:
        params["data_inicio"] = data_inicio
    if data_fim:
        params["data_fim"] = data_fim
    return params


class ProcessosResource(BaseResource):
    def buscar(self, numero: str) -> Processo:
        return Processo.model_validate(self._get(f"/processos/{numero}"))

    def listar(
        self,
        *,
        tribunal: str | None = None,
        parte: str | None = None,
        advogado: str | None = None,
        data_inicio: str | None = None,
        data_fim: str | None = None,
        page: int = 1,
        per_page: int = 20,
        pagina: int | None = None,
        limite: int | None = None,
    ) -> dict[str, Any]:
        params = _list_params(
            tribunal=tribunal,
            parte=parte,
            advogado=advogado,
            data_inicio=data_inicio,
            data_fim=data_fim,
            page=page,
            per_page=per_page,
            pagina=pagina,
            limite=limite,
        )
        return self._get("/processos", params=params)

    def iterar(self, **kwargs: Any) -> AutoPaginator[dict[str, Any]]:
        limite = kwargs.pop("limite", 50)
        kwargs.pop("pagina", None)
        return AutoPaginator(
            self._client,
            "/processos",
            params=kwargs,
            limit=limite,
            page_param="page",
            per_page_param="per_page",
            page_key="page",
            per_page_key="per_page",
            total_key="total",
        )

    def movimentacoes(
        self,
        numero: str,
        *,
        pagina: int = 1,
        limite: int = 50,
    ) -> dict[str, Any]:
        return self._get(
            f"/processos/{numero}/movimentacoes",
            params={"pagina": pagina, "limite": limite},
        )

    def buscar_lote(self, numeros: list[str]) -> list[Processo]:
        raw: list[dict[str, Any]] = self._post("/processos/batch", json={"numeros": numeros})
        return [Processo.model_validate(item) for item in raw]


class AsyncProcessosResource(AsyncBaseResource):
    async def buscar(self, numero: str) -> Processo:
        return Processo.model_validate(await self._get(f"/processos/{numero}"))

    async def listar(
        self,
        *,
        tribunal: str | None = None,
        parte: str | None = None,
        advogado: str | None = None,
        data_inicio: str | None = None,
        data_fim: str | None = None,
        page: int = 1,
        per_page: int = 20,
        pagina: int | None = None,
        limite: int | None = None,
    ) -> dict[str, Any]:
        params = _list_params(
            tribunal=tribunal,
            parte=parte,
            advogado=advogado,
            data_inicio=data_inicio,
            data_fim=data_fim,
            page=page,
            per_page=per_page,
            pagina=pagina,
            limite=limite,
        )
        return await self._get("/processos", params=params)

    def iterar(self, **kwargs: Any) -> AsyncAutoPaginator[dict[str, Any]]:
        limite = kwargs.pop("limite", 50)
        kwargs.pop("pagina", None)
        return AsyncAutoPaginator(
            self._client,
            "/processos",
            params=kwargs,
            limit=limite,
            page_param="page",
            per_page_param="per_page",
            page_key="page",
            per_page_key="per_page",
            total_key="total",
        )

    async def movimentacoes(
        self, numero: str, *, pagina: int = 1, limite: int = 50
    ) -> dict[str, Any]:
        return await self._get(
            f"/processos/{numero}/movimentacoes",
            params={"pagina": pagina, "limite": limite},
        )

    async def buscar_lote(self, numeros: list[str]) -> list[Processo]:
        raw: list[dict[str, Any]] = await self._post("/processos/batch", json={"numeros": numeros})
        return [Processo.model_validate(item) for item in raw]
