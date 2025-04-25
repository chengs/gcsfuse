import argparse
import os
import socket
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
# from bigquery import constants

from bigquery import experiments_gcsfuse_bq
from google.cloud.bigquery import table
from gsheet import gsheet
from google.api_core.exceptions import NotFound


"""Contains constants for bigquery."""

DEFAULT_PROJECT_ID = "gcs-fuse-test-ml"
DEFAULT_DATASET_ID = "gargnitin_test_dataset"
DEFAULT_TABLE_ID = "fio_test_tool_output"


def fetch_dataset(
    project_id: str, dataset_id: str
) -> experiments_gcsfuse_bq.ExperimentsGCSFuseBQ:
  dataset = experiments_gcsfuse_bq.ExperimentsGCSFuseBQ(project_id, dataset_id)
  print(f"Fetched dataset: {dataset} of type {type(dataset)}")
  return dataset


def parse_arguments() -> object:
  parser = argparse.ArgumentParser(
      prog="",
      description=(),
  )
  parser.add_argument(
      "--project-id",
      metavar="GCP Project ID/name",
      help=(),
      default=DEFAULT_PROJECT_ID,
      required=False,
  )
  parser.add_argument(
      "--dataset-id",
      help="",
      default=DEFAULT_DATASET_ID,
      required=False,
  )
  parser.add_argument(
      "--table-name",
      help="Optional table name. Default=khregrh",
      default=DEFAULT_TABLE_ID,
      required=False,
  )
  return parser.parse_args()


def create_or_fetch_table(
    args: [],
    # dataset: experiments_gcsfuse_bq.ExperimentsGCSFuseBQ,
) -> table.Table:
  try:
    dataset = fetch_dataset(args.project_id, args.dataset_id)
  except NotFound as nf:
    print(f"dataset not found !")
    print(f"Should create dataset now, but not implemented!")
    # # Create dataset if not exists
    # dataset = bigquery.Dataset(f"{args.project_id}.{args.dataset_id}")
    # self.client.create_dataset(dataset, exists_ok=True)
    # # Wait for the dataset to be created and ready to be referenced
    # time.sleep(120)
    sys.exit(1)
  except Exception as e:
    print(f"Failed to fetch dataset of type {type(e)}")
    sys.exit(1)

  try:
    table = dataset._get_table_from_table_id(args.table_name)
    print(f"Fetched table={table} of type {type(table)}")
  except NotFound as e:
    print(f"Table {args.table_name} not found !")
    print(f"Will create table {args.table_name} now ...")
    create_table_query = """
      CREATE TABLE IF NOT EXISTS {}.{}.{} (
        workload_id STRING, 
        instance_id STRING, 
        epoch INT64,
        read_type string,
        num_threads INT64,
        file_size string,
        block_size string,
        file_size_in_bytes string,
        block_size_in_bytes string,
        num_threads INT64,
        files_per_thread INT64,
        bucket_name STRING,
        machine_type STRING,
        PRIMARY KEY (workload_id) NOT ENFORCED
      ) OPTIONS (description = 'Table for storing output metrics of FIO workloads');
    """.format(args.project_id, args.dataset_id, args.table_name)
    print(f"Query={create_table_query}")
    try:
      dataset._execute_query(create_table_query)
    except Exception as e:
      print(f"Failed to create table: {e} of type {type(e)}")
      raise e
    try:
      # time.sleep(120)
      table = dataset._get_table_from_table_id(args.table_name)
      print(f"Fetched newly created table {table} of type {type(table)}")
    except Exception as e:
      print(f"Failed to fetch newly created table: {e} of type {type(e)}")
      raise e
  except Exception as e:
    print(f"Failed to fetch table {args.table_name}: {type(e)}")
    sys.exit(1)
  return table


if __name__ == "__main__":
  args = parse_arguments()

  # print(f"dataset.client={dataset.client}")
  # print(f"dataset.project_id={dataset.project_id}")
  # print(f"dataset.dataset_id={dataset.dataset_id}")
  # table = create_or_fetch_table(args, dataset)
  table = create_or_fetch_table(args)
