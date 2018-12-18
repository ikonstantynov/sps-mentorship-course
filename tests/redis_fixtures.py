import time

import pytest
import redis


@pytest.fixture(scope='session')
def redis_server(docker_client, session_id):
    docker_client.pull('redis:5.0.1')
    container = docker_client.create_container(
        image='redis:5.0.1',
        name='sharing-knowledge-redis-server-{}'.format(session_id),
        ports=[6379],
        detach=True,
        host_config=docker_client.create_host_config(port_bindings={6379: 6379})
    )

    docker_client.start(container=container['Id'])

    redis_params = dict(host='localhost', port=6379)

    ping_redis(**redis_params)

    container['redis_params'] = redis_params

    yield container

    docker_client.kill(container=container['Id'])
    docker_client.remove_container(container['Id'])


@pytest.fixture
def redis_client(redis_server):
    conn = redis.StrictRedis(**redis_server['redis_params'])
    yield conn
    conn.connection_pool.disconnect()


def ping_redis(**redis_params):
    delay = 0.001
    for i in range(100):
        try:
            redis.StrictRedis(**redis_params).ping()
            break
        except redis.exceptions.ConnectionError as e:
            time.sleep(delay)
            delay *= 2
    else:
        raise RuntimeError("Cannot start redis server")
