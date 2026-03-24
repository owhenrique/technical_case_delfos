# Delfos Energy - Pipeline ETL e API

Bem-vindo ao repositório do caso técnico da Delfos Energy. Este projeto implementa um pipeline de ETL simplificado que se comunica com duas instâncias locais de banco PostgreSQL (Fonte e Alvo) através de uma API FastAPI. 

## Como Rodar o Projeto

1. **Gere os Containers (Bancos de Dados e Inicializador)**:
   A infraestrutura principal é gerida pelo Docker. Execute o comando:
   ```bash
   docker-compose up -d --build
   ```
   > Esse comando sobe não apenas o `db_fonte` e `db_alvo`, mas também o `db_init`. O initializer é um container temporário em Python que cria as tabelas via SQLAlchemy e insere automaticamente 10 dias úteis de dados (15840 registros de minuto-a-minuto) no banco Fonte!

2. **Instale as as Dependências**:
   ```bash
   poetry install
   ```

3. **Inicie a API**:
   ```bash
   poetry run task dev
   ```
   O servidor estará ativo em `http://localhost:8000`.

4. **Testes Unitários**:
   O projeto conta com uma suíte de testes usando pytest. Para rodá-la (e gerar cobertura):
   ```bash
   poetry run task test
   ```

## Arquitetura e Estrutura de Diretórios
O repositório foi arquitetado respeitando o conceito de **Separation of Concerns** (Separação de Contextos) e DDD.

```text
src/
├── api/               # API isolada com o FastAPI, Rotas (endpoints) e Schemas do Pydantic
├── db/                # (Docker) Contém a base em SQLAlchemy
│   ├── models/        # Schemas representacionais das tabelas (ORM)
│   └── repositories/  # Classes exclusivas de acesso e consulta ao BD (FonteRepository, etc)
├── etl/               # Lógica pesada de Extração usando manipulações vetorizadas (Pandas)
├── orchestration/     # Onde ficam salvos os assets da DAG (Dagster)
└── scripts/           # Scripts isolados como `init_databases.py` e simuladores 
```

## Estrutura de Tabelas (Banco de Dados)

### 1. Banco **Fonte** (`db_fonte`: 5433)
O banco fonte simula os dados crus dos sistemas (ex: turbinas eólicas).
* **Tabela `data`**:
  * `timestamp` (DateTime, Primary Key)
  * `wind_speed` (Float) - Velocidade do vento
  * `power` (Float) - Energia gerada calculada
  * `ambient_temperature` (Float) - Um distrator térmico aleatório

### 2. Banco **Alvo** (`db_alvo`: 5434)
O banco alvo (construído cem por cento via SQLAlchemy) armazena os agregados e os sinais catalogados pelo ETL usando modelagem estrela minimalista.
* **Tabela `signal`**: Dicionário/domínio (Dimensão) das variáveis extraídas
  * `id` (Integer, Primary Key)
  * `name` (String, Unique) - Ex: `wind_speed_mean`, `power_max`, `wind_speed_std`
* **Tabela `data`**: Armazena as séries temporais consolidadas
  * `timestamp` (DateTime, Primary Key - Composta com `signal_id`)
  * `signal_id` (Integer, Foreign Key vinculando a tabela `signal`)
  * `value` (Float) - O valor agregado calculado pelo ETL

## Particularidades
- Optou-se por construir as agregações utilizando DataFrames em **Pandas** porque cálculos estatísticos sobre janelas extensas e séries temporais (`std`, agregação 10-minutes) performam melhor do que processar no motor RDBMS e deixam o ETL escalável via cluster.
- A orquestração agnóstica reside no módulo `orchestration`: O Dagster é responsável por gerenciar quando o script do ETL deverá bater na API de fonte e atualizar o Alvo. 
- Ferramentas de Lint e Formatação: O código baseia-se fortemente em formatação imperativa com **Ruff**.