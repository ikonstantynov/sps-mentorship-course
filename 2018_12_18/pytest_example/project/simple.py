import logging

logger = logging.getLogger('examples_for_testing')
logger.setLevel(logging.DEBUG)


def add(x, y):
    return x + y


def is_divisible_by_3(number):
    return number % 3 == 0


def check_log():
    try:
        1/0
    except ZeroDivisionError:
        logger.warning('Wrong action.', exc_info=True)
