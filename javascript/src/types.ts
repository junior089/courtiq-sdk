export interface CourtIQConfig {
  apiKey: string;
  environment?: "production" | "sandbox";
  baseUrl?: string;
  timeout?: number;
  maxRetries?: number;
}

export interface Processo {
  numero: string;
  tribunal: string;
  classe?: string;
  assunto?: string;
  comarca?: string;
  vara?: string;
  juiz?: string;
  valorCausa?: number;
  dataDistribuicao?: string;
  partes: Parte[];
  movimentacoes: Movimentacao[];
}

export interface Parte {
  nome: string;
  tipo: string;
  documento?: string;
  oab?: string;
}

export interface Movimentacao {
  data: string;
  descricao: string;
  tipo?: string;
  complemento?: string;
}

export interface Monitoramento {
  id: number;
  numeroProcesso: string;
  webhookUrl?: string;
  eventos: string[];
  ativo: boolean;
  criadoEm: string;
  atualizadoEm?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page?: number;
  per_page?: number;
  pagina?: number;
  limite?: number;
  paginas?: number;
}

export interface Webhook {
  id: number;
  url: string;
  eventos: string[];
  ativo?: boolean;
  criadoEm?: string;
}

export interface ListarProcessosParams {
  tribunal?: string;
  parte?: string;
  advogado?: string;
  data_inicio?: string;
  data_fim?: string;
  page?: number;
  per_page?: number;
  pagina?: number;
  limite?: number;
}

export interface CriarMonitoramentoParams {
  numeroProcesso: string;
  webhookUrl?: string;
  eventos?: string[];
}

export interface CriarWebhookParams {
  url: string;
  eventos?: string[];
  secret?: string;
}

export interface PaginationParams {
  pagina?: number;
  limite?: number;
}
