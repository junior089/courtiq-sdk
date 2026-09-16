from __future__ import annotations

from typing import Any


class CourtIQError(Exception):
    def __init__(self, message: str, code: str | None = None, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class AuthenticationError(CourtIQError):
    def __init__(self, message: str = "Autenticação falhou. Verifique sua API key."):
        super().__init__(message, code="authentication_error", status_code=401)


class RateLimitError(CourtIQError):
    def __init__(self, message: str = "Rate limit excedido.", retry_after: int = 60):
        super().__init__(message, code="rate_limit_exceeded", status_code=429)
        self.retry_after = retry_after


class NotFoundError(CourtIQError):
    def __init__(self, message: str = "Recurso não encontrado."):
        super().__init__(message, code="not_found", status_code=404)


class ValidationError(CourtIQError):
    def __init__(
        self,
        message: str = "Parâmetros inválidos.",
        errors: list[dict[str, Any]] | None = None,
    ):
        super().__init__(message, code="validation_error", status_code=422)
        self.errors = errors or []


class ServerError(CourtIQError):
    def __init__(self, message: str = "Erro interno do servidor."):
        super().__init__(message, code="server_error", status_code=500)
