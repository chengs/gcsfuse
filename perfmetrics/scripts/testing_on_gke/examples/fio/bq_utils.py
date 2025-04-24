import argparse
import os
import socket
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
# from bigquery import constants

from bigquery import experiments_gcsfuse_bq
from gsheet import gsheet


"""Contains constants for bigquery."""

PROJECT_ID = 'gcs-fuse-test-ml'
DATASET_ID = 'gargnitin_test_dataset'
TABLE_ID = 'fio_test_tool_output'


def create_table():
  dataset = experiments_gcsfuse_bq.ExperimentsGCSFuseBQ(PROJECT_ID, DATASET_ID)
  print(f'Created/accessed dataset: {dataset}')
  return
