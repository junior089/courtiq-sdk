from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Processo(BaseModel):
    numero: str
    tribunal: str
    classe: str | None = None
    assunto: str | None = None
    comarca: str | None = None
    vara: str | None = None
    juiz: str | None = None
    valor_causa: float | None = None
    data_distribuicao: datetime | None = None
    partes: list[Parte] = Field(default_factory=list)
    movimentacoes: list[Movimentacao] = Field(default_factory=list)


class Parte(BaseModel):
    nome: str
    tipo: str
    documento: str | None = None
    oab: str | None = None


class Movimentacao(BaseModel):
    data: datetime
    descricao: str
    tipo: str | None = None
    complemento: str | None = None


class Monitoramento(BaseModel):
    id: int
    numero_processo: str
    webhook_url: str | None = None
    eventos: list[str] = Field(default_factory=list)
    ativo: bool = True
    criado_em: datetime
    atualizado_em: datetime | None = None


class PaginatedResponse(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)
    total: int = 0
    pagina: int = 1
    limite: int = 20
    paginas: int = 1


Processo.model_rebuild()
