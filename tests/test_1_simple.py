"""
Base example.

for running tests:
    python -m pytest tests/test_simple.py

getting full diff:
    python -m pytest tests/test_1_simple.py -vv

running only tests which were marked as `slow`:
    python -m pytest -m slow

stop after first failure(could save time):
    python -m pytest -x

stop after two failures:
    python -m pytest --maxfail=2

profiling test duration:
    python -m pytest --durations=3 -vv

"""
import time

import pytest

from examples_for_testing.simple import add, is_divisible_by_3


def test_assert():
    assert [1, 2, 3] == [1, 2]


def test_assert2():
    assert {'name': 'Foo', 'age': 20, 'address': 'Kiev, Blvd. Shevchenko'} == \
           {'name': 'Foo', 'age': 21, 'address': 'Kiev, Blvd. Sholudenko'}


def test_assert3():
    assert True
    assert isinstance([1, 2], list)
    assert 'g' in 'age'


def test_add():
    assert add(1, 1) == 2


def test_exception():
    with pytest.raises(TypeError):
        add(1, {'key': 'value'})


@pytest.mark.slow
def test_marked():
    assert True


def test_profiling_1():
    time.sleep(0.1)


def test_profiling_2():
    time.sleep(0.2)


def test_profiling_3():
    time.sleep(0.3)


@pytest.mark.parametrize("number,result", [(5, False), (9, True), (-1, False)])
def test_calculate_number_of_consumers(number, result):
    assert is_divisible_by_3(number) == result
