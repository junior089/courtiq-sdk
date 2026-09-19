# CourtIQ SDKs

[![CI](https://github.com/junior089/courtiq-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/junior089/courtiq-sdk/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/%40courtiq%2Fsdk.svg)](https://www.npmjs.com/package/@courtiq/sdk)
[![PyPI](https://img.shields.io/pypi/v/courtiq.svg)](https://pypi.org/project/courtiq/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Official client libraries for the [CourtIQ](https://courtiq.com.br) API — a platform for tracking judicial
processes across Brazilian courts (TJSP, TJRJ, TJMG, TRF1/3/5, and others).

This repo holds the public SDKs extracted from the main CourtIQ monorepo: a typed HTTP client, pagination
helpers, typed errors, and webhook signature verification, for both JavaScript/TypeScript and Python.

- [`javascript/`](javascript) — [`@courtiq/sdk`](javascript/README.md)
- [`python/`](python) — [`courtiq`](python/README.md)

## Why two SDKs, one repo

Both clients share the same API surface (`processos`, `monitoramentos`, `webhooks`) and the same design:
a small typed core, automatic pagination, typed exceptions per HTTP status, and an explicit sandbox vs.
production environment switch. Keeping them side by side makes the parity between the two easy to see.

## Quick start

**TypeScript**

```bash
npm install @courtiq/sdk
```

```typescript
import { CourtIQ } from "@courtiq/sdk";

const client = new CourtIQ({ apiKey: "your-api-key" });
const processo = await client.processos.buscar("0001234-56.2024.8.26.0100");
```

**Python**

```bash
pip install courtiq
```

```python
from courtiq import CourtIQ

client = CourtIQ(api_key="your-api-key")
processo = client.processos.buscar(numero="0001234-56.2024.8.26.0100")
```

See each package's own README for full usage, configuration, error handling, and webhook verification.

## Examples

### List with automatic pagination

**TypeScript**

```typescript
for await (const processo of client.processos.iterar({ tribunal: "TJSP" })) {
  console.log(processo.numero, processo.classe);
}
```

**Python**

```python
for processo in client.processos.iterar(tribunal="TJSP"):
    print(processo["numero"])
```

### Create a monitor and handle errors

**TypeScript**

```typescript
import { CourtIQError, RateLimitError } from "@courtiq/sdk";

try {
  const monitor = await client.monitoramentos.criar({
    numeroProcesso: "0001234-56.2024.8.26.0100",
    webhookUrl: "https://your-server.com/webhook",
    eventos: ["movimentacao"],
  });
} catch (error) {
  if (error instanceof RateLimitError) {
    console.error(`Retry after ${error.retryAfter}s`);
  } else if (error instanceof CourtIQError) {
    console.error(error.code, error.message);
  }
}
```

**Python**

```python
from courtiq.exceptions import CourtIQError, RateLimitError

try:
    monitor = client.monitoramentos.criar(
        numero_processo="0001234-56.2024.8.26.0100",
        webhook_url="https://your-server.com/webhook",
        eventos=["movimentacao"],
    )
except RateLimitError as e:
    print(f"Retry after {e.retry_after}s")
except CourtIQError as e:
    print(e.code, e.message)
```

### Verify an incoming webhook

**TypeScript**

```typescript
import { verificarAssinatura } from "@courtiq/sdk/webhooks";

const isValid = await verificarAssinatura({
  payload: rawRequestBody,
  signature: request.headers["x-courtiq-signature"],
  secret: "your-webhook-secret",
});
```

**Python**

```python
from courtiq.webhooks import verificar_assinatura

is_valid = verificar_assinatura(
    payload=request.body,
    signature=request.headers["X-CourtIQ-Signature"],
    secret="your-webhook-secret",
)
```

## Development

```bash
# JavaScript/TypeScript
cd javascript && npm install && npm test

# Python
cd python && pip install -e ".[dev]" && pytest
```

## License

MIT — see [LICENSE](LICENSE).
