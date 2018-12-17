import json

import psycopg2
import redis


def get_config():
    """Just for demo, don't do like this in real project."""
    return {
        'postgres': {
            'database': 'postgres',
            'user': 'postgres',
            'password': 'mysecretpassword',
            'host': 'localhost',
            'port': 5432
        },
        'redis': {
            'host': 'localhost',
            'port': 6379
        }
    }


def add_new_route(route_info):
    """Just for demo, don't do like this in real project."""
    connection = psycopg2.connect(**get_config()['postgres'])
    cursor = connection.cursor()
    cursor.execute("INSERT INTO routes.route (id, route) VALUES (%s, %s);",
                   (route_info['route_id'], json.dumps(route_info)))
    connection.commit()
    cursor.close()
    connection.close()


def set_route_to_redis(route):
    """Just for demo, don't do like this in real project."""
    client = redis.StrictRedis(**get_config()['redis'])
    result = client.setnx(route['route_id'], json.dumps(route))
    client.connection_pool.disconnect()
    return result


def get_route_from_redis(route_id):
    """Just for demo, don't do like this in real project."""
    client = redis.StrictRedis(**get_config()['redis'])
    result = json.loads(client.get(route_id))
    client.connection_pool.disconnect()
    return result
