from __future__ import annotations

import hashlib
import hmac
from typing import Any

from ..pagination import AsyncAutoPaginator, AutoPaginator
from .base import AsyncBaseResource, BaseResource


def verificar_assinatura(
    payload: bytes,
    signature: str,
    secret: str,
) -> bool:
    raw_secret = secret.removeprefix("whsec_")
    expected = hmac.new(
        raw_secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


class WebhooksResource(BaseResource):
    def listar(self, *, pagina: int = 1, limite: int = 20) -> dict[str, Any]:
        return self._get("/webhooks", params={"pagina": pagina, "limite": limite})

    def criar(
        self,
        url: str,
        *,
        eventos: list[str] | None = None,
        secret: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"url": url}
        if eventos:
            payload["eventos"] = eventos
        if secret:
            payload["secret"] = secret
        return self._post("/webhooks", json=payload)

    def iterar(self, **kwargs: Any) -> AutoPaginator[dict[str, Any]]:
        limite = kwargs.pop("limite", 50)
        kwargs.pop("pagina", None)
        return AutoPaginator(self._client, "/webhooks", params=kwargs, limit=limite)

    def remover(self, webhook_id: int) -> None:
        self._delete(f"/webhooks/{webhook_id}")


class AsyncWebhooksResource(AsyncBaseResource):
    async def listar(self, *, pagina: int = 1, limite: int = 20) -> dict[str, Any]:
        return await self._get("/webhooks", params={"pagina": pagina, "limite": limite})

    async def criar(
        self,
        url: str,
        *,
        eventos: list[str] | None = None,
        secret: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"url": url}
        if eventos:
            payload["eventos"] = eventos
        if secret:
            payload["secret"] = secret
        return await self._post("/webhooks", json=payload)

    def iterar(self, **kwargs: Any) -> AsyncAutoPaginator[dict[str, Any]]:
        limite = kwargs.pop("limite", 50)
        kwargs.pop("pagina", None)
        return AsyncAutoPaginator(self._client, "/webhooks", params=kwargs, limit=limite)

    async def remover(self, webhook_id: int) -> None:
        await self._delete(f"/webhooks/{webhook_id}")
