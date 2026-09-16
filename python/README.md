# CourtIQ Python SDK

SDK Python oficial para a API do CourtIQ — consulta processual automatizada.

## Instalação

```bash
pip install courtiq
```

## Quick Start

```python
from courtiq import CourtIQ

client = CourtIQ(api_key="sua-api-key")

# Buscar processo por número
processo = client.processos.buscar(numero="0001234-56.2024.8.26.0100")
print(processo.partes)

# Consultar múltiplos processos
resultados = client.processos.buscar_lote(
    numeros=["0001234-56.2024.8.26.0100", "0005678-90.2024.8.26.0100"]
)

# Monitorar processo (receber webhooks quando houver movimentação)
monitor = client.monitoramentos.criar(
    numero_processo="0001234-56.2024.8.26.0100",
    webhook_url="https://meu-servidor.com/webhook",
)
```

## Configuração

```python
from courtiq import CourtIQ

# Configuração completa
client = CourtIQ(
    api_key="sua-api-key",
    environment="production",  # "production" ou "sandbox"
    timeout=30,                # timeout em segundos
    max_retries=3,             # retentativas automáticas
    base_url=None,             # URL customizada (self-hosted)
)
```

## Recursos

### Processos

```python
# Buscar por número
processo = client.processos.buscar(numero="0001234-56.2024.8.26.0100")

# Buscar com filtros
processos = client.processos.listar(
    tribunal="TJSP",
    parte="João Silva",
    data_inicio="2024-01-01",
    data_fim="2024-12-31",
    pagina=1,
    limite=20,
)

# Movimentações
movs = client.processos.movimentacoes(numero="0001234-56.2024.8.26.0100")
```

### Monitoramentos

```python
# Criar monitoramento
monitor = client.monitoramentos.criar(
    numero_processo="0001234-56.2024.8.26.0100",
    webhook_url="https://meu-servidor.com/webhook",
    eventos=["movimentacao", "publicacao"],
)

# Listar monitoramentos
monitores = client.monitoramentos.listar()

# Remover monitoramento
client.monitoramentos.remover(monitor_id=123)
```

### Webhooks

```python
# Validar assinatura de webhook
from courtiq.webhooks import verificar_assinatura

is_valid = verificar_assinatura(
    payload=request.body,
    signature=request.headers["X-CourtIQ-Signature"],
    secret="seu-webhook-secret",
)
```

## Tratamento de Erros

```python
from courtiq.exceptions import (
    CourtIQError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)

try:
    processo = client.processos.buscar(numero="...")
except AuthenticationError:
    print("API key inválida ou expirada")
except RateLimitError as e:
    print(f"Rate limit excedido. Tente novamente em {e.retry_after}s")
except NotFoundError:
    print("Processo não encontrado")
except CourtIQError as e:
    print(f"Erro: {e.message} (código: {e.code})")
```

## Ambientes

| Ambiente   | Base URL                          | Descrição             |
| ---------- | --------------------------------- | --------------------- |
| production | https://api.courtiq.com.br/v1     | Dados reais           |
| sandbox    | https://sandbox.courtiq.com.br/v1 | Dados mock para teste |

## Licença

MIT
