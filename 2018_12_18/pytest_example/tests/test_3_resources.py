import psycopg2
import pytest

from examples_for_testing.using_db_resources import add_new_route, set_route_to_redis, get_route_from_redis


def test_create_new_route(pg_client):
    new_route = {
        "route_id": "as2-to-cvan-receiver_2",
        "origin": {
            "s3_object_key": "s3inbtest/incoming",
            "s3_bucket": "dev-datastore",
            "service": "s3_inbound_handler"
        }
    }
    assert add_new_route(new_route) is None


def test_duplicate_error(pg_client):
    new_route = {
        "route_id": "as2-to-cvan-receiver-exist",
        "origin": {
            "s3_object_key": "s3inbtest/incoming",
            "s3_bucket": "dev-datastore",
            "service": "s3_inbound_handler"
        }
    }
    with pytest.raises(psycopg2.IntegrityError) as exception:
        add_new_route(new_route)

    assert 'duplicate key value violates unique constraint' in exception.value.pgerror


def test_set_route(redis_client):
    route = {
        "route_id": "as2-to-cvan-redis_1",
        "origin": {
            "s3_object_key": "s3inbtest/incoming",
            "s3_bucket": "dev-datastore",
            "service": "s3_inbound_handler"
        }
    }
    assert set_route_to_redis(route) is True


def test_duplicate_redis(redis_client):
    route = {
        "route_id": "as2-to-cvan-redis_2",
        "origin": {
            "s3_object_key": "s3inbtest/incoming",
            "s3_bucket": "dev-datastore",
            "service": "s3_inbound_handler"
        }
    }
    assert set_route_to_redis(route) is True
    assert set_route_to_redis(route) is False


def test_get_route_from_redis(redis_client):
    route = {
        "route_id": "as2-to-cvan-redis_3",
        "origin": {
            "s3_object_key": "s3inbtest/incoming",
            "s3_bucket": "dev-datastore",
            "service": "s3_inbound_handler"
        }
    }
    assert set_route_to_redis(route) is True
    assert get_route_from_redis(route['route_id']) == route
