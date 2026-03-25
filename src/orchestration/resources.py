from dagster import ConfigurableResource


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
