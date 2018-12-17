import boto3
import pytest
from moto import mock_ssm


@pytest.fixture(scope='module')
def ssm_mock():
    mock_ssm().start()
    client = boto3.client('ssm', region_name='us-east-1')

    client.put_parameter(
        Name='/unit/product/subproduct/service/env/base/first',
        Description='A test parameter',
        Value='base_1',
        Type='SecureString')

    yield client

    mock_ssm().stop()


@pytest.fixture
def api_gateway_request():
    def _make_request(body=None, path_parameters=None, query_string_parameters=None):
        if body is None:
            body = {}
        return {
            'body': body,
            'pathParameters': path_parameters,
            'queryStringParameters': query_string_parameters
        }

    return _make_request
