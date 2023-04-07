from google.cloud import bigquery
from collections import namedtuple
import os

# create an immutable context for all the src modules
Context = namedtuple("Context", "project dataset client")

project = os.getenv("BQ_PROJECT")
dataset = os.getenv("BQ_DATASET")
client = bigquery.Client(project=project)

context = Context(project, dataset, client)


