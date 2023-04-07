from src.common.dry_run import DryRunner

sql = """
SELECT * FROM `hatvalues-sandbox.jaffle_shop.customers`
"""

runner = DryRunner(sql)
job = runner.run_job()

# A dry run query completes immediately.
print(f'This query will process {round(job.total_bytes_processed/1024**2, 3)} MB.')