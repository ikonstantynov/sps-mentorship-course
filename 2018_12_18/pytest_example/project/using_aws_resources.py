import os

import boto3


def get_value_from_ssm(key):
    client = boto3.client("ssm", region_name=os.environ['AWS_REGION'])
    return client.get_parameter(Name=key, WithDecryption=True)['Parameter']['Value']
