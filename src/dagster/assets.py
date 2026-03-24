from dagster import DailyPartitionsDefinition, asset
from src.dagster.resources import APIResource, TargetDBResource
from src.etl.process import run_etl

daily_partition = DailyPartitionsDefinition(start_date='2025-01-01')


@asset(partitions_def=daily_partition, compute_kind='python')
def etl_daily_asset(context, api: APIResource, target_db: TargetDBResource):
    """
    Extracts daily data from Fonte API, transforms to 10-min bins,
    and loads to Alvo DB for the partition date.
    """
    partition_date_str = context.partition_key
    context.log.info(f'Running ETL for partition {partition_date_str}')

    run_etl(
        target_date=partition_date_str,
        api_url=api.api_url,
        db_alvo_url=target_db.db_alvo_url,
    )

    context.log.info(f'Finished ETL for partition {partition_date_str}')
