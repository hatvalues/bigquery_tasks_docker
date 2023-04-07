# bigquery_tasks_docker
A Docker container for running tasks against GCP Big Query

## Usage

Python modules should import the immutable context object.

## Modules

### common.table_utilities

Convenience functions to simplify common ops against the API.

* create_overwrite_table
  * Given a table name and a schema (list of bigquery.SchemaField), will create a new Table
  * Defaults - context project, do not overwrite if exists
  * Optional - partition scheme

#### Try it

See example_table_setup.py

### common.dry_run

Convenience function get job execution stats. Create a runner, run a job with a SQL statement, check the processed MB.

#### Try it

See example_dry_run.py