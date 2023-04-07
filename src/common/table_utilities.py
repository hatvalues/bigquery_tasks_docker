from google.cloud.bigquery import Table, SchemaField, TimePartitioningType
from google.cloud.bigquery import TimePartitioning, RangePartitioning, PartitionRange
from typing import TypedDict, Union, Literal, Optional
from src.common.bq_context import context

class RangePartitionScheme(TypedDict):
    start: int
    end: int
    interval: int

class DefinedPartitionScheme(TypedDict):
    field_name: str
    scheme: Union[Literal["hour", "day", "month", "year"], RangePartitionScheme]

def create_overwrite_table(
        table_name: str,
        table_schema: list[SchemaField], # list of SchemaField objects
        dataset_name: str =context.dataset,
        overwrite_existing: bool =False,
        partition: Optional[DefinedPartitionScheme] = {}
    ) -> bool:
    """Creates a table in the target BQ project and dataset.
    Can force overwrite_existing and existing table, so take extreme care!

    Args:
        table_name (str): Name of target table
        table_schema (list[SchemaField]): A valid schema, list of SchemaField objects.
        overwrite_existing (bool, optional): Kill and overwrite target table if exists? If False will error if exists. Defaults to False.
        partition (Optional[DefinedPartitionScheme], optional): If literal time unit (smallest is "hour") will require a date field. Otherwise an integer partition, which requires a named interger field. Defaults to {}.

    Returns:
        bool: True on success.
    """
    table_id = context.client.dataset(dataset_name).table(table_name)
    if overwrite_existing: # replace if exists
        context.client.delete_table(table_id, not_found_ok=overwrite_existing)
    else:
        try: # throws an error if there already
            context.client.get_table(table_id)
            print(f"WARNING: Table {table_id} already exists. No action taken. Set overwrite_existing=True to replace it.")
            return False
        except Exception as E:
            pass
    if type(table_schema)!=list:
        print(f"ERROR: Invalid table schema. Expected list of SchemaField")
        return False
    elif not all([type(ts)==SchemaField for ts in table_schema]):
        print(f"ERROR: Invalid table schema. Expected iterable of strictly SchemaField objects.")
        return False
    elif table_schema: # non empty list of valid schema fields
        table = Table(table_id, schema=table_schema)
        if partition:
            if type(partition["scheme"])==str:
                partition_types = {
                    "hour" : TimePartitioningType.HOUR,
                    "day" : TimePartitioningType.DAY,
                    "month" : TimePartitioningType.MONTH,
                    "year" : TimePartitioningType.YEAR
                    }
                table.time_partitioning = TimePartitioning(
                type_=partition_types[partition["scheme"]],
                field=partition["field_name"]
            )
            elif type(partition["scheme"])==RangePartitionScheme:
                table.range_partitioning = RangePartitioning(
                # To use integer range partitioning, select a top-level REQUIRED /
                # NULLABLE column with INTEGER / INT64 data type.
                field=partition["field_name"],
                range_=PartitionRange(start=partition["scheme"]["start"],
                                                end=partition["scheme"]["end"],
                                                interval=partition["scheme"]["interval"])
            )
            else:
                print("WARNING: Invalid table partition scheme. Table will be created without partition scheme.")
    else: # empty schema
        print(f"Warning: Emtpy table schema. Will create table with no schema/fields.")
        table = Table(table_id, schema=table_schema)
    table = context.client.create_table(table)
    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
    return True