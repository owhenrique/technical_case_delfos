import pandas as pd
from dagster import ConfigurableResource
from sqlalchemy import create_engine


class APIResource(ConfigurableResource):
    """
    Recurso de conexao do Dagster utilizado para invocar endpoints da Fonte.
    """

    api_url: str


class TargetDBResource(ConfigurableResource):
    """
    Recurso de conexao do Dagster contendo a DSN do banco de destino (Alvo).
    """

    db_alvo_url: str


class FonteDBResource(ConfigurableResource):
    """
    Recurso de conexao do Dagster para acesso direto ao banco de dados Fonte.
    """

    db_fonte_url: str

    def get_engine(self):
        return create_engine(self.db_fonte_url)

    def query_as_df(self, sql_query: str, params: dict = None):
        engine = self.get_engine()
        with engine.connect() as conn:
            return pd.read_sql(sql_query, conn, params=params)
