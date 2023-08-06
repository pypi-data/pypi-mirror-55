# -*- coding: utf-8 -*-
import operator
import sortables.factory


class SortableDict(dict):
    """A dict with a `sorted` method. Should generally be instantiated via
    the Sortable factory rather than directly.
    """

    def sorted(self, by_value=False, reverse=False):
        """Return a sorted copy of the dictionary.

        Note: This returns a dictionary, not a series of k,v tuples. Thus for
        < Python 3.7 this is not expected to work correctly!

        Keyword arguments:
        by_value -- whether to sort by value (default False)
        reverse -- whether to reverse the sort (default False)
        """
        return self._operator_sorted(by_value=by_value, reverse=reverse)

    def _operator_sorted(self, by_value=False, reverse=False):
        if by_value:
            return dict(sorted(self.items(), key=operator.itemgetter(1), reverse=reverse))
        else:
            return dict(sorted(self.items(), reverse=reverse))

    def _lambda_sorted(self, by_value=False, reverse=False):
        """Initial timeit tests show operator-based sorting to have a slight
        advantage over lambda sorting. This is just here to document the lambda
        approach. This will probably go away at some point.
        """
        if by_value:
            return dict(sorted(self.items(), key=lambda x: x[1]), reverse=reverse)
        else:
            return dict(sorted(self.items(), reverse=reverse))

    def items(self):
        """Return a Sortable copy of the dict items."""
        return sortables.factory.Sortable(tuple(super().items()))

