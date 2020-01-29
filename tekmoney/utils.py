import functools
import operator
from typing import Iterable, TypeVar

T = TypeVar('T')


def tek_sum(values: Iterable[T]) -> T:
    """ Return the sum of values in iterable"""
    return functools.reduce(operator.add, values)
