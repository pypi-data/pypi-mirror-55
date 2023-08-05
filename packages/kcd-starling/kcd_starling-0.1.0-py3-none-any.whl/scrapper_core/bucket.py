from enum import Enum
from functools import partial
from pprint import pprint
from typing import List, Any, Text
import boto3

from scrapper_core.config import Config
from scrapper_core.util import singleton
import json
import time


@singleton
class KinesisClient:
    def __init__(self, region: Text):
        self.client = boto3.client('kinesis', region_name=region)

    def get_client(self):
        return self.client


def _save_to_stdout(data: List[Any], config: Config):
    pprint(data)


def _save_to_sqs(data: List[Any], config: Config):
    # TODO Implementation required
    pass


def _save_to_kinesis(data: List[Any], config: Config):
    # TODO add retry logic and test cases
    client = KinesisClient(config['AWS_REGION']).get_client()
    response = client.put_records(
        Records=[
            {
                'Data': data,
                'PartitionKey': str(round(time.time() * 1000))
            },
        ],
        StreamName='kcd.scrapper'
    )
    print(response)


class Bucket(Enum):
    Stdout = partial(_save_to_stdout)
    Sqs = partial(_save_to_sqs)
    Kinesis = partial(_save_to_kinesis)

    def __call__(self, *args, **kwargs) -> None:
        self.value(*args, **kwargs)
