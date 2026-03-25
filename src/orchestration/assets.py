from dagster import DailyPartitionsDefinition, asset

from src.etl.process import run_etl
from src.orchestration.resources import APIResource, TargetDBResource

daily_partition = DailyPartitionsDefinition(start_date='2025-01-01')


@asset(partitions_def=daily_partition, compute_kind='python')
def etl_daily_asset(context, api: APIResource, target_db: TargetDBResource):
    """
    Asset particionado diário que aciona o pipeline completo de ETL.

    Consome a classe mestre de processamento extraindo os dados de `api` e
    escrevendo no `target_db` referenciado para o respectivo dia da particao.

    Args:
        context (OpExecutionContext): O contexto de processamento do Dagster.
        api (APIResource): O recurso contendo as URLs da Fonte.
        target_db (TargetDBResource): Recurso contendo DSN do banco Alvo.
    """
    partition_date_str = context.partition_key
    context.log.info(f'Running ETL for partition {partition_date_str}')

    run_etl(
        target_date=partition_date_str,
        api_url=api.api_url,
        db_alvo_url=target_db.db_alvo_url,
    )

    context.log.info(f'Finished ETL for partition {partition_date_str}')
