from google.cloud.bigquery import QueryJobConfig
from src.common.bq_context import context

class DryRunner(object):
  def __init__(self, sql) -> None:
    self.sql = sql
    # Construct a BigQuery client object.
    self.job_config = QueryJobConfig(dry_run=True, use_query_cache=False)

  def set_sql(self, sql):
    self.sql = sql
  
  def run_job(self):
    # Start the query, passing in the extra configuration.
    query_job = context.client.query(
      self.sql,
      job_config=self.job_config,
    )
    return query_job