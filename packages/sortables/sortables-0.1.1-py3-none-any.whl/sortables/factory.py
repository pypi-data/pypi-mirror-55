from typing import Union
from .dictionaries import SortableDict
from .series import SortableTuple, SortableList, SortableSet


class Sortable(object):
    """Factory for producing sanely sortable data structures."""

    def __new__(self, obj:Union[dict, tuple, list]):
        if isinstance(obj, dict):
            return SortableDict(obj)
        elif isinstance(obj, tuple):
            return SortableTuple(obj)
        elif isinstance(obj, list):
            return SortableList(obj)
        elif isinstance(obj, set):
            return SortableSet(obj)
        else:
            raise TypeError('Unknown Sortable type: %s' % type(obj))

