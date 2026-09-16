import { HttpClient } from "./http";
import type {
  CourtIQConfig,
  ListarProcessosParams,
  CriarMonitoramentoParams,
  CriarWebhookParams,
  PaginationParams,
  Processo,
  Monitoramento,
  Webhook,
  PaginatedResponse,
} from "./types";
import { AutoPaginator } from "./pagination";

class ProcessosResource {
  constructor(private http: HttpClient) {}

  async buscar(numero: string) {
    return this.http.get<Processo>(`/processos/${numero}`);
  }

  async listar(params?: ListarProcessosParams) {
    const { pagina, limite, ...apiParams } = params ?? {};
    return this.http.get<PaginatedResponse<Processo>>(
      "/processos",
      {
        ...apiParams,
        page: apiParams.page ?? pagina,
        per_page: apiParams.per_page ?? limite,
      },
    );
  }

  iterar(params?: Omit<ListarProcessosParams, "pagina" | "limite">, limite = 50) {
    return new AutoPaginator<Processo>(
      this.http,
      "/processos",
      params as Record<string, string | number | undefined>,
      limite,
      { pageParam: "page", perPageParam: "per_page", pageKey: "page", perPageKey: "per_page", totalKey: "total" },
    );
  }

  async movimentacoes(numero: string, params?: PaginationParams) {
    return this.http.get<PaginatedResponse<Processo["movimentacoes"][number]>>(
      `/processos/${numero}/movimentacoes`,
      params as Record<string, string | number | undefined>,
    );
  }

  async buscarLote(numeros: string[]) {
    return this.http.post<Processo[]>("/processos/batch", { numeros });
  }
}

class MonitoramentosResource {
  constructor(private http: HttpClient) {}

  async criar(params: CriarMonitoramentoParams) {
    return this.http.post<Monitoramento>("/monitoramentos", params);
  }

  async listar(params?: PaginationParams) {
    return this.http.get<PaginatedResponse<Monitoramento>>(
      "/monitoramentos",
      params as Record<string, string | number | undefined>,
    );
  }

  iterar(params?: Omit<PaginationParams, "pagina" | "limite">, limite = 50) {
    return new AutoPaginator<Monitoramento>(
      this.http,
      "/monitoramentos",
      params as Record<string, string | number | undefined>,
      limite
    );
  }

  async obter(id: number) {
    return this.http.get<Monitoramento>(`/monitoramentos/${id}`);
  }

  async remover(id: number) {
    return this.http.delete<void>(`/monitoramentos/${id}`);
  }
}

class WebhooksResource {
  constructor(private http: HttpClient) {}

  async listar(params?: PaginationParams) {
    return this.http.get<PaginatedResponse<Webhook>>(
      "/webhooks",
      params as Record<string, string | number | undefined>,
    );
  }

  iterar(params?: Omit<PaginationParams, "pagina" | "limite">, limite = 50) {
    return new AutoPaginator<Webhook>(
      this.http,
      "/webhooks",
      params as Record<string, string | number | undefined>,
      limite
    );
  }

  async criar(params: CriarWebhookParams) {
    return this.http.post<Webhook>("/webhooks", params);
  }

  async remover(id: number) {
    return this.http.delete<void>(`/webhooks/${id}`);
  }
}

export class CourtIQ {
  readonly processos: ProcessosResource;
  readonly monitoramentos: MonitoramentosResource;
  readonly webhooks: WebhooksResource;

  constructor(config: CourtIQConfig) {
    if (!config.apiKey) {
      throw new Error("apiKey é obrigatório.");
    }
    const http = new HttpClient(config);
    this.processos = new ProcessosResource(http);
    this.monitoramentos = new MonitoramentosResource(http);
    this.webhooks = new WebhooksResource(http);
  }
}
