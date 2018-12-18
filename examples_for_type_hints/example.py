"""
mypy examples_for_type_hints/example.py
"""

from typing import List, Dict, Tuple

name_counts: Dict[str, int] = {
    "Adam": 10,
    "Guido": 12
}

list_of_dicts: List[Dict[str, int]] = [
    {"key1": 'asd'},    # wrong type, for mypy demo
    {"key2": 2}
]

my_data: Tuple[str, int, float] = ("Adam", 10, 5.7)


def greeting(name: str) -> str:
    return 'Hello ' + name


Vector = List[float]


def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]

