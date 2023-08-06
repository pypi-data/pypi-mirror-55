# -*- coding: utf-8 -*-
import operator
from typing import Union, Iterable, Callable
import sortables.factory


def getter(key:Union[int, str, Iterable[int], Iterable[str], Callable, None]):
    if key is None:
        return None
    elif isinstance(key, int):
        return operator.itemgetter(key)
    elif isinstance(key, str):
        return operator.attrgetter(key)
    elif isinstance(key, tuple) and isinstance(key[0], int):
        return operator.itemgetter(*key)
    elif isinstance(key, tuple) and isinstance(key[0], str):
        return operator.attrgetter(*key)
    elif callable(key):
        return key
    else:
        raise TypeError('Cannot get by key of type: %s' % type(key))


class SortableSeries(object):
    """A series data structure with a `sorted` method.

    Keyword arguments:
    key -- Key to sort by (default None)
    method -- Method call to sort by (default None)
    reverse -- whether to reverse the sort (default False)

    `key` can be an integer index, or can be a string property name (e.g. for
    named tuples and for instance objects)

    `method` accepts a string name of a method to call. Argument passing is not
    currently supported.
    """

    def sorted(self,
               key:Union[int, str, Iterable[int], Iterable[str], Callable, None]=None,
               method=None, reverse=False):
        if method is not None:
            # TODO: support for method arguments
            return sortables.factory.Sortable(
                sorted(self, key=operator.methodcaller(method), reverse=reverse))
        else:
            return sortables.factory.Sortable(
                sorted(self, key=getter(key), reverse=reverse))


class SortableTuple(SortableSeries, tuple):
    pass


class SortableList(SortableSeries, list):
    pass


class SortableSet(SortableSeries, set):
    pass
