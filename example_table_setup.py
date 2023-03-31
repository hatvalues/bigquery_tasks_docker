from google.cloud import bigquery
from bq_connection import create_replace_table

predicts_table = "predictive_analytics"
    
predicts_schema = [
    bigquery.SchemaField("predict_entity", "STRUCT", fields=[
            bigquery.SchemaField("id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("kind", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("sub_type", "STRING", mode="NULLABLE")
            ],
            mode="REQUIRED"
    ),
    bigquery.SchemaField("predict_date", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("predict_what", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("predict", "STRUCT", fields=[
            bigquery.SchemaField("score", "FLOAT64", mode="NULLABLE"),
            bigquery.SchemaField("category", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("segment", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("provided", "STRING", mode="REQUIRED")
            ],
            mode="REQUIRED"
    ),
    bigquery.SchemaField("model_info", "STRUCT", fields=[
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("version", "STRING", mode="REQUIRED")
            ],
            mode="REQUIRED"
    )
]

first_last_events_table = "ga_first_and_latest_events"

first_last_events_schema = [
    bigquery.SchemaField("id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("first_event_date", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("latest_event_date", "DATETIME", mode="REQUIRED")
]

create_replace_table(
    predicts_table, predicts_schema,
    dataset_name="analytics",
    replace=False,
    partition={
        "field_name": "predict_date",
        "scheme": "day"
    }
)

create_replace_table(
    first_last_events_table, first_last_events_schema,
)