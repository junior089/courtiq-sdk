export class CourtIQError extends Error {
  readonly code: string;
  readonly statusCode: number | undefined;

  constructor(message: string, code?: string, statusCode?: number) {
    super(message);
    this.name = "CourtIQError";
    this.code = code ?? "unknown_error";
    this.statusCode = statusCode;
  }
}

export class AuthenticationError extends CourtIQError {
  constructor(message = "Autenticação falhou. Verifique sua API key.") {
    super(message, "authentication_error", 401);
    this.name = "AuthenticationError";
  }
}

export class RateLimitError extends CourtIQError {
  readonly retryAfter: number;

  constructor(message = "Rate limit excedido.", retryAfter = 60) {
    super(message, "rate_limit_exceeded", 429);
    this.name = "RateLimitError";
    this.retryAfter = retryAfter;
  }
}

export class NotFoundError extends CourtIQError {
  constructor(message = "Recurso não encontrado.") {
    super(message, "not_found", 404);
    this.name = "NotFoundError";
  }
}

export class ValidationError extends CourtIQError {
  readonly errors: Record<string, string>[];

  constructor(
    message = "Parâmetros inválidos.",
    errors: Record<string, string>[] = [],
  ) {
    super(message, "validation_error", 422);
    this.name = "ValidationError";
    this.errors = errors;
  }
}

export class ServerError extends CourtIQError {
  constructor(message = "Erro interno do servidor.") {
    super(message, "server_error", 500);
    this.name = "ServerError";
  }
}
