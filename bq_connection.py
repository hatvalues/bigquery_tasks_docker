from google.cloud import bigquery
from typing import TypedDict, Union, Literal, Optional
import os

bq_project = os.getenv("BQ_PROJECT")
bq_dataset = os.getenv("BQ_DATASET")
bq_client = bigquery.Client(project=bq_project)

class RangePartitionScheme(TypedDict):
    start: int
    end: int
    interval: int

class DefinedPartitionScheme(TypedDict):
    field_name: str
    scheme: Union[Literal["hour", "day", "month", "year"], RangePartitionScheme]
    
def create_replace_table(
        table_name: str,
        table_schema: list[bigquery.SchemaField], # list of bigquery.SchemaField objects
        dataset_name: str =bq_dataset,
        replace: bool =False,
        partition: Optional[DefinedPartitionScheme] = {}
    ) -> bool:
    """Creates a table in the target BQ project and dataset.
    Can force replace and existing table, so take extreme care!

    Args:
        table_name (str): Name of target table
        table_schema (list[bigquery.SchemaField]): A valid schema, list of SchemaField objects.
        replace (bool, optional): Kill and replace target table if exists? If False will error if exists. Defaults to False.
        partition (Optional[DefinedPartitionScheme], optional): If literal time unit (smallest is "hour") will require a date field. Otherwise an integer partition, which requires a named interger field. Defaults to {}.

    Returns:
        bool: True on success.
    """
    table_id = bq_client.dataset(dataset_name).table(table_name)
    if replace: # replace if exists
        bq_client.delete_table(table_id, not_found_ok=replace)
    else:
        try: # throws an error if there already
            bq_client.get_table(table_id)
            print(f"WARNING: Table {table_id} already exists. No action taken. Set replace=True to replace it.")
            return False
        except Exception as E:
            pass
    if type(table_schema)!=list:
        print(f"ERROR: Invalid table schema. Expected list of bigquery.SchemaField")
        return False
    elif not all([type(ts)==bigquery.SchemaField for ts in table_schema]):
        print(f"ERROR: Invalid table schema. Expected iterable of strictly bigquery.SchemaField objects.")
        return False
    elif table_schema: # non empty list of valid schema fields
        table = bigquery.Table(table_id, schema=table_schema)
        if partition:
            if type(partition["scheme"])==str:
                partition_types = {
                    "hour" : bigquery.TimePartitioningType.HOUR,
                    "day" : bigquery.TimePartitioningType.DAY,
                    "month" : bigquery.TimePartitioningType.MONTH,
                    "year" : bigquery.TimePartitioningType.YEAR
                    }
                table.time_partitioning = bigquery.TimePartitioning(
                type_=partition_types[partition["scheme"]],
                field=partition["field_name"]
            )
            elif type(partition["scheme"])==RangePartitionScheme:
                table.range_partitioning = bigquery.RangePartitioning(
                # To use integer range partitioning, select a top-level REQUIRED /
                # NULLABLE column with INTEGER / INT64 data type.
                field=partition["field_name"],
                range_=bigquery.PartitionRange(start=partition["scheme"]["start"],
                                                end=partition["scheme"]["end"],
                                                interval=partition["scheme"]["interval"])
            )
            else:
                print("WARNING: Invalid table partition scheme. Table will be created without partition scheme.")
    else: # empty schema
        print(f"Warning: Emtpy table schema. Will create table with no schema/fields.")
        table = bigquery.Table(table_id, schema=table_schema)
    table = bq_client.create_table(table)
    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
    return True