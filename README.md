# Delfos Energy - Pipeline ETL e API

Pipeline de ETL e API REST para processamento e exposição de dados de geração de energia eólica, desenvolvido como parte do processo seletivo técnico da Delfos Energy.

---

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e **Docker Compose**
- **Python 3.13+**
- **Poetry** — Gerenciador de dependências e ambientes virtuais.
  > Não tem o Poetry instalado? Siga a [documentação oficial](https://python-poetry.org/docs/#installation) para instalação.

---

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/owhenrique/technical_case_delfos.git
   cd technical_case_delfos
   ```

2. **Instale as dependências do projeto via Poetry:**
   ```bash
   poetry install
   ```

---

## Subindo a Infraestrutura (Docker)

O ambiente possui três serviços Docker declarados no `docker-compose.yml`:

| Serviço    | Descrição                                                          | Porta   |
|------------|--------------------------------------------------------------------|---------|
| `db_fonte` | Banco PostgreSQL de origem com dados brutos de geração eólica.     | `5433`  |
| `db_alvo`  | Banco PostgreSQL de destino com os dados agregados pelo ETL.       | `5434`  |
| `db_init`  | Container temporário (Python) que cria tabelas e popula o Fonte.   | —       |

```bash
# Sobe todos os containers, cria tabelas e insere os dados
docker-compose up -d --build
```

> O `db_init` inicializa automaticamente os dois bancos ao subir: cria todas as tabelas via SQLAlchemy e insere **15.840 registros** (minuto a minuto, 11 dias) no banco Fonte.

![Query Rows](./img/query_rows_print.png)

Para derrubar os containers:
```bash
docker-compose down
```

---

## Executando a API

Com os containers no ar, inicie o servidor de desenvolvimento:

```bash
poetry run task dev
```

A API estará disponível em `http://localhost:8000`.

### Documentação Interativa

O FastAPI expõe automaticamente dois endpoints de documentação:

| Interface   | URL                                     |
|-------------|----------------------------------------|
| **Swagger** | `http://localhost:8000/docs`           |
| **ReDoc**   | `http://localhost:8000/redoc`          |

### Endpoints Disponíveis

| Método | Rota        | Descrição                                          |
|--------|-------------|-----------------------------------------------------|
| `GET`  | `/health`   | Verifica se a API está ativa.                       |
| `GET`  | `/data`     | Retorna série temporal filtrada por variável e período. |

**Parâmetros do `/data`:**
- `start_time` — Data/hora de início (ex: `2025-01-01T00:00:00`)
- `end_time` — Data/hora de fim (ex: `2025-01-01T23:59:59`)
- `variables` — Lista de variáveis: `wind_speed`, `power`, `ambient_temperature`

---

## Testes

O projeto usa **pytest** com cobertura de código via `coverage`.

```bash
# Roda lint, testes e gera relatório de cobertura HTML
poetry run task test

# Gera o relatório de cobertura em htmlcov/index.html
# (executado automaticamente pelo post_test após os testes)
```

---

## Qualidade de Código (Ruff)

O projeto usa [Ruff](https://docs.astral.sh/ruff/) para lint e formatação com linha máxima de 79 caracteres.

```bash
# Verificar erros de lint
poetry run task lint

# Formatar o código automaticamente
poetry run task format

# Aplicar correções automáticas do lint + formatar (equivale a format completo)
poetry run ruff check --fix && poetry run ruff format
```

---

## Scripts Utilitários

### Popular o banco Fonte manualmente

Caso precise reseed dos dados sem recriar os containers:

```bash
# Via poetry script registrado:
poetry run populate-fonte

# Ou diretamente pelo Python:
poetry run python -m src.scripts.populate_fonte_db
```

### Inicializar bancos manualmente

```bash
poetry run python -m src.scripts.init_databases
```

> Requer que as variáveis `DB_FONTE_DSN` e `DB_ALVO_DSN` estejam configuradas no ambiente ou em um arquivo `.env`.

---

## Orquestração com Dagster

O módulo de orquestração utiliza o **Dagster** para agendar e disparar o pipeline ETL diariamente.

```bash
# Iniciar a UI do Dagster (Dagit)
poetry run dagster dev -f src/orchestration/definitions.py
```

A interface do Dagster estará disponível em `http://localhost:3000`, onde você pode:
- Visualizar e disparar o asset `etl_daily_asset` manualmente.
- Acompanhar o log de execução de cada partição diária.
- Ver o schedule configurado (`0 1 * * *` — toda madrugada à 1h).

![Dagster Automations](./img/dagster_automation.png)
![Dagster Catalog](./img/dagster_catalog.png)
![Dagster Jobs](./img/dagster_jobs.png)

---

## Variáveis de Ambiente

| Variável          | Padrão                                              | Descrição                         |
|------------------|-----------------------------------------------------|-------------------------------------|
| `DB_FONTE_DSN`    | `postgresql://delfos:delfos@localhost:5433/fonte`  | DSN do banco de origem             |
| `DB_ALVO_DSN`     | `postgresql://delfos:delfos@localhost:5434/alvo`   | DSN do banco de destino            |
| `CONECTOR_API_URL`| `http://localhost:8000`                             | URL base da API usada pelo Dagster |

---

## Estrutura de Tabelas

### Banco **Fonte** (`db_fonte`, porta 5433)

**Tabela `data`** — Dados brutos em formato Wide (minuto a minuto):

| Coluna                | Tipo       | Descrição                                  |
|-----------------------|------------|--------------------------------------------|
| `timestamp`           | DateTime PK| Momento exato da leitura                   |
| `wind_speed`          | Float      | Velocidade do vento (m/s)                  |
| `power`               | Float      | Potência gerada (calculada a partir do vento) |
| `ambient_temperature` | Float      | Temperatura ambiente (distrator aleatório) |

### Banco **Alvo** (`db_alvo`, porta 5434)

**Tabela `signal`** — Dicionário de sinais (dimensão):

| Coluna | Tipo        | Descrição                                            |
|--------|-------------|------------------------------------------------------|
| `id`   | Integer PK  | Identificador único do sinal                        |
| `name` | String Unique | Ex: `wind_speed_mean`, `power_max`, `wind_speed_std` |

**Tabela `data`** — Série temporal agregada em formato Long:

| Coluna      | Tipo         | Descrição                                    |
|-------------|--------------|----------------------------------------------|
| `timestamp` | DateTime PK  | Início da janela de 10 minutos               |
| `signal_id` | Integer PK FK| Referência ao sinal na tabela `signal`       |
| `value`     | Float        | Valor estatístico calculado pelo ETL          |

---

## Arquitetura e Estrutura de Diretórios

```text
src/
├── api/               # FastAPI: rotas, schemas Pydantic e injeção de dependência
├── db/                # ORM e acesso a dados
│   ├── models/        # Mapeamentos SQLAlchemy (DataFonte, DataAlvo, Signal)
│   └── repositories/  # Repositórios com a lógica de consulta e persistência
├── etl/               # Lógica de transformação: resample 10min com Pandas
├── orchestration/     # Assets, recursos e schedule do Dagster
└── scripts/           # Inicializador de banco e gerador de massa de dados
```

> **Nota sobre permissões Docker:** Os volumes `data_fonte/` e `data_alvo/` são gerenciados pelo Docker e podem exigir `sudo` dependendo da configuração do sistema host.