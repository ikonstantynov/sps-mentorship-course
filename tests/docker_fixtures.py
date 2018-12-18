import uuid

import docker as libdocker
import pytest


@pytest.fixture(scope='session')
def session_id():
    return str(uuid.uuid4())


@pytest.fixture(scope='session')
def docker_client():
    return libdocker.APIClient(version='auto')
