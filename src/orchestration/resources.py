from dagster import ConfigurableResource


class APIResource(ConfigurableResource):
    api_url: str


class TargetDBResource(ConfigurableResource):
    db_alvo_url: str
