import os

import pytest

pytest_plugins = ['aws_fixtures', 'docker_fixtures', 'postgres_fixtures', 'redis_fixtures']


def pytest_sessionstart(session):
    """ before session.main() is called. """
    os.environ['EVENT_STORE_STREAM_NAME'] = 'local-reporting-config-EventStream-N14A9MWPZ4J3'
    os.environ['AWS_REGION'] = 'us-east-1'
    os.environ['AWS_LAMBDA_FUNCTION_NAME'] = 'lambda_function_name'
    os.environ['AWS_LAMBDA_LOG_STREAM_NAME'] = 'lambda_log_stream_name'
    os.environ['BASE_SSM_PATH'] = '/unit/product/subproduct/service/env/base/'


@pytest.fixture(scope='session')
def simple_fixture():
    return 1


@pytest.fixture(params=[1, 2])
def positive_integer(request):
    return request.param


# @pytest.fixture(autouse=True)
# def reset_singleton():
#     yield
#     Singleton.reset()
