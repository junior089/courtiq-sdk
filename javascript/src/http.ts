import {
  AuthenticationError,
  CourtIQError,
  NotFoundError,
  RateLimitError,
  ServerError,
  ValidationError,
} from "./errors";
import type { CourtIQConfig } from "./types";

const ENVS: Record<string, string> = {
  production: "https://api.courtiq.com.br/v1",
  sandbox: "https://sandbox.courtiq.com.br/v1",
};

type ErrorResponse = {
  detail?: string;
  errors?: Record<string, string>[];
};

export class HttpClient {
  private baseUrl: string;
  private headers: Record<string, string>;
  private timeout: number;
  private maxRetries: number;

  constructor(config: CourtIQConfig) {
    this.baseUrl =
      config.baseUrl ??
      ENVS[config.environment ?? "production"] ??
      ENVS.production;
    this.headers = {
      Authorization: `Bearer ${config.apiKey}`,
      "Content-Type": "application/json",
      "User-Agent": "@courtiq/sdk/0.1.0",
    };
    this.timeout = config.timeout ?? 30000;
    this.maxRetries = config.maxRetries ?? 3;
  }

  async request<T = unknown>(
    method: string,
    path: string,
    options?: {
      params?: Record<string, string | number | undefined>;
      body?: unknown;
    },
  ): Promise<T> {
    const url = new URL(path, this.baseUrl);
    if (options?.params) {
      for (const [key, value] of Object.entries(options.params)) {
        if (value !== undefined) {
          url.searchParams.set(key, String(value));
        }
      }
    }

    let lastError: Error | null = null;
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        const response = await fetch(url.toString(), {
          method,
          headers: this.headers,
          body: options?.body ? JSON.stringify(options.body) : undefined,
          signal: controller.signal,
        });

        clearTimeout(timeoutId);
        return this.handleResponse<T>(response);
      } catch (error) {
        if (error instanceof RateLimitError) {
          if (attempt >= this.maxRetries) throw error;
          const delay = (error.retryAfter || 1) * 1000;
          await new Promise((r) => setTimeout(r, delay));
          continue;
        }
        if (error instanceof ServerError) {
          if (attempt >= this.maxRetries) throw error;
          await new Promise((r) => setTimeout(r, 1000 * 2 ** attempt));
          continue;
        }
        if (error instanceof CourtIQError) throw error;

        lastError = error as Error;
        if (attempt < this.maxRetries) {
          await new Promise((r) => setTimeout(r, 1000 * 2 ** attempt));
        }
      }
    }

    throw new CourtIQError(
      `Falha após ${this.maxRetries + 1} tentativas: ${lastError?.message}`,
      "network_error",
    );
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (response.status === 401) throw new AuthenticationError();
    if (response.status === 404) {
      const data = (await response.json().catch(() => ({}))) as ErrorResponse;
      throw new NotFoundError(data.detail ?? "Recurso não encontrado.");
    }
    if (response.status === 422) {
      const data = (await response.json().catch(() => ({}))) as ErrorResponse;
      throw new ValidationError(data.detail, data.errors);
    }
    if (response.status === 429) {
      const retryAfter = parseInt(
        response.headers.get("Retry-After") ?? "60",
        10,
      );
      throw new RateLimitError(undefined, retryAfter);
    }
    if (response.status >= 500) throw new ServerError();
    if (response.status >= 400) {
      const data = (await response.json().catch(() => ({}))) as ErrorResponse;
      throw new CourtIQError(
        data.detail ?? "Erro desconhecido.",
        undefined,
        response.status,
      );
    }

    if (response.status === 204) return undefined as T;
    return response.json() as Promise<T>;
  }

  get<T = unknown>(
    path: string,
    params?: Record<string, string | number | undefined>,
  ): Promise<T> {
    return this.request<T>("GET", path, { params });
  }

  post<T = unknown>(path: string, body?: unknown): Promise<T> {
    return this.request<T>("POST", path, { body });
  }

  patch<T = unknown>(path: string, body?: unknown): Promise<T> {
    return this.request<T>("PATCH", path, { body });
  }

  delete<T = unknown>(path: string): Promise<T> {
    return this.request<T>("DELETE", path);
  }
}
