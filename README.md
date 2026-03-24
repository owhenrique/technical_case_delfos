# Delfos Energy - Pipeline ETL e API

Bem-vindo ao repositório do caso técnico da Delfos Energy. Este projeto consiste em um pipeline de ETL simplificado que conecta dois bancos de dados (Fonte e Alvo) operados em PostgreSQL através de uma API FastAPI. 

## Objetivo

O principal objetivo é consumir dados brutos de energia de uma tabela origem, agregar esses dados temporais utilizando bibliotecas como Pandas e carregá-los em uma nova tabela de sinais de forma otimizada utilizando a ORM SQLAlchemy, enquanto a orquestração do fluxo é guiada agnosticamente.

## Requisitos
- **Docker e Docker Compose**
- **Python 3.13+**
- **Poetry** (Gerenciador de Dependências)

## Instalação e Execução Básica
1. Instale as dependências:
   ```bash
   poetry install
   ```
2. Inicialize o serviço pelo Docker:
   ```bash
   docker-compose up -d --build
   ```
3. Rode a API via Taskipy:
   ```bash
   poetry run task dev
   ```

> *A documentação completa das tabelas e arquitetura foi mapeada e será atualizada na próxima revisão.*