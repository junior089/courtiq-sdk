# CourtIQ JavaScript/TypeScript SDK

SDK oficial para a API do CourtIQ em JavaScript e TypeScript.

## Instalação

```bash
npm install @courtiq/sdk
# ou
yarn add @courtiq/sdk
# ou
pnpm add @courtiq/sdk
```

## Quick Start

```typescript
import { CourtIQ } from "@courtiq/sdk";

const client = new CourtIQ({ apiKey: "sua-api-key" });

// Buscar processo por número
const processo = await client.processos.buscar("0001234-56.2024.8.26.0100");
console.log(processo.partes);

// Consultar múltiplos processos
const resultados = await client.processos.buscarLote([
  "0001234-56.2024.8.26.0100",
  "0005678-90.2024.8.26.0100",
]);

// Monitorar processo
const monitor = await client.monitoramentos.criar({
  numeroProcesso: "0001234-56.2024.8.26.0100",
  webhookUrl: "https://meu-servidor.com/webhook",
});
```

## Configuração

```typescript
const client = new CourtIQ({
  apiKey: "sua-api-key",
  environment: "production", // 'production' | 'sandbox'
  timeout: 30000, // timeout em ms
  maxRetries: 3, // retentativas automáticas
  baseUrl: undefined, // URL customizada (self-hosted)
});
```

## Recursos

### Processos

```typescript
// Buscar por número
const processo = await client.processos.buscar("0001234-56.2024.8.26.0100");

// Listar com filtros
const lista = await client.processos.listar({
  tribunal: "TJSP",
  parte: "João Silva",
  dataInicio: "2024-01-01",
  dataFim: "2024-12-31",
  pagina: 1,
  limite: 20,
});

// Movimentações
const movs = await client.processos.movimentacoes("0001234-56.2024.8.26.0100");
```

### Monitoramentos

```typescript
// Criar
const monitor = await client.monitoramentos.criar({
  numeroProcesso: "0001234-56.2024.8.26.0100",
  webhookUrl: "https://meu-servidor.com/webhook",
  eventos: ["movimentacao", "publicacao"],
});

// Listar
const monitores = await client.monitoramentos.listar();

// Remover
await client.monitoramentos.remover(123);
```

### Webhooks

```typescript
import { verificarAssinatura } from "@courtiq/sdk/webhooks";

const isValid = verificarAssinatura({
  payload: request.body,
  signature: request.headers["x-courtiq-signature"],
  secret: "seu-webhook-secret",
});
```

## Tratamento de Erros

```typescript
import {
  CourtIQError,
  AuthenticationError,
  RateLimitError,
  NotFoundError,
} from "@courtiq/sdk";

try {
  const processo = await client.processos.buscar("...");
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.error("API key inválida ou expirada");
  } else if (error instanceof RateLimitError) {
    console.error(`Tente novamente em ${error.retryAfter}s`);
  } else if (error instanceof NotFoundError) {
    console.error("Processo não encontrado");
  } else if (error instanceof CourtIQError) {
    console.error(`Erro ${error.code}: ${error.message}`);
  }
}
```

## Licença

MIT
