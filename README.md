# Delfos Data Engineering Technical Test

Este repositório contém o código de um pipeline *ETL* orquestrado com o **Dagster**, conectando dados brutos de um banco PostgreSQL via API REST (criada com **FastAPI**) e entregando os dados transformados em outro banco PostgreSQL.   

O projeto adota o padrão **API-Models-Repositories** localizado na pasta `src/`.

## Requisitos
- Python 3.13
- Docker e Docker-Compose
- Poetry

---

## 🚀 Como Executar o Projeto

### 1. Inicializar os Bancos de Dados
Disponibilizamos o `db_fonte` (porta `5433`) e `db_alvo` (porta `5434`) através do `docker-compose.yml`.

Inicie a infraestrutura e os bancos PostgreSQL:
```bash
docker-compose up -d
```

### 2. Instalar Dependências
Com o Poetry instalado, garanta as dependências pelo comando:
```bash
poetry install
```

### 3. Popular Banco Fonte
Um script providenciado vai se conectar ao banco `db_fonte`, criar as tabelas necessárias e injetar dez dias de amostras (2025-01-01 até 2025-01-11):
```bash
poetry run populate-fonte
```
*(Certifique-se que o `.env` esteja na raiz com a variável `DB_FONTE_DSN=postgresql://delfos:delfos@localhost:5433/fonte` configurada).*

### 4. Subir a API (Conector Fonte)
Inicie o back-end que disponibiliza os dados do Banco Fonte para o ETL:
```bash
poetry run uvicorn src.api.main:app --reload --port 8000
```

### 5. Utilizar o Dagster (Orquestração do ETL)
Em um terminal separado, suba a UI do Dagster:
```bash
poetry run dagster dev -m src.dagster.definitions
```

Acesse [http://localhost:3000](http://localhost:3000), vá até a aba **Assets**, selecione o asset diário (`etl_daily_asset`) e aperte **Materialize**. Você pode selecionar a partição do dia com dados injetados (ex: `2025-01-01` ~ `2025-01-10`) para rodar e visualizar os resumos estísticos migrando da API local rumo ao banco Alvo.`

### Testes
Para rodar a suíte de testes unitários:
```bash
poetry run pytest
```