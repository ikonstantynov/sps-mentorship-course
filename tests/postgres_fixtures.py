import os
import time

import psycopg2
import pytest


@pytest.fixture(scope='session')
def pg_server(docker_client, session_id):
    docker_client.pull('postgres:9.6.10')
    init_db_path = os.getcwd() + '/initdb'
    container = docker_client.create_container(
        image='postgres:9.6.10',
        name='sharing-knowledge-pg-server-{}'.format(session_id),
        ports=[5432],
        detach=True,
        volumes=[init_db_path],
        host_config=docker_client.create_host_config(
            port_bindings={5432: 5432},
            binds={
                init_db_path: {
                    'bind': '/docker-entrypoint-initdb.d',
                    'mode': 'ro'
                }
            }
        )
    )

    docker_client.start(container=container['Id'])

    pg_params = dict(database='postgres',
                     user='postgres',
                     password='mysecretpassword',
                     host='localhost',
                     port=5432)

    ping_postgres(**pg_params)

    container['pg_params'] = pg_params

    yield container

    docker_client.kill(container=container['Id'])
    docker_client.remove_container(container['Id'])


@pytest.fixture
def pg_client(pg_server):
    conn = psycopg2.connect(**pg_server['pg_params'])
    yield conn
    conn.close()


def ping_postgres(**pg_params):
    delay = 0.001
    for i in range(100):
        try:
            conn = psycopg2.connect(**pg_params)
            cur = conn.cursor()
            cur.execute("CREATE EXTENSION hstore;")
            cur.close()
            conn.close()
            break
        except psycopg2.Error as e:
            time.sleep(delay)
            delay *= 2
    else:
        raise RuntimeError("Cannot start postgres server")
