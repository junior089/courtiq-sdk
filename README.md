# CourtIQ SDKs

[![CI](https://github.com/junior089/courtiq-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/junior089/courtiq-sdk/actions/workflows/ci.yml)

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

## Development

```bash
# JavaScript/TypeScript
cd javascript && npm install && npm test

# Python
cd python && pip install -e ".[dev]" && pytest
```

## License

MIT — see [LICENSE](LICENSE).
