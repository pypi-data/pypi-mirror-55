## sortables


Not to be confused with `sortable`, which is a Grappelli admin UI sorter for Django.

**Note:** I have not yet sorted out (hee hee) the compatible Python versions, but this does use type hints, so it will end up being at least 3.5+. There are also some places in the code that depend on the new specification of retained order in dicts, being a Python 3.7+ specific feature. I have not yet decided whether to fix this for 3.5, 3.6 compatibility.

This initial (very alpha) state of the project was developed in Python 3.7.2.

### Sanely sortable Python data structures

Sort Python data structures without awkward itemgetter, attrgettr, or lambda syntax.

Python's sorting syntax is not always expressive or easy to remember. Why do this:

```
sorted(d, key=operator.itemgetter(1))
```

when you could do this?

```
d.sorted(by_value=True)
```

Or how about sorting a named tuple. Instead of this:

```
sorted(t, key=operator.attrgetter('myproperty'))
```

we can do this:

```
t.sorted(key='myproperty')
```

... and more.

### Sort a series of tuples by an internal index.

```
>>> t = ( ('apples', 3), ('oranges', 1), ('bananas', 2) )
>>> st = Sortable(t)
>>> st.sorted()
[('apples', 3), ('bananas', 2), ('oranges', 1)]
>>> st.sorted(key=1)
[('oranges', 1), ('bananas', 2), ('apples', 3)]
>>> st.sorted(key=1, reverse=True)
[('apples', 3), ('bananas', 2), ('oranges', 1)]
```

### Sort a dict by value.

```
>>> sd = Sortable(dict(t))
>>> sd.sorted()
{'apples': 3, 'bananas': 2, 'oranges': 1}
>>> sd.sorted(by_value=True)
{'oranges': 1, 'bananas': 2, 'apples': 3}
>>> sd.sorted(by_value=True, reverse=True)
{'apples': 3, 'bananas': 2, 'oranges': 1}
```

### Sort a series of named tuples by internal named property.

```
>>> from collections import namedtuple
>>> Fruit = namedtuple('Fruit', ['name', 'number'])
>>> sl = Sortable([ Fruit(name='apples', number=3), Fruit(name='bananas', number=2), Fruit(name='oranges', number=1) ])
>>> sl.sorted()
[Fruit(name='apples', number=3), Fruit(name='bananas', number=2), Fruit(name='oranges', number=1)]
>>> sl.sorted(key='number')
[Fruit(name='oranges', number=1), Fruit(name='bananas', number=2), Fruit(name='apples', number=3)]
>>> sl.sorted(key='number', reverse=True)
[Fruit(name='apples', number=3), Fruit(name='bananas', number=2), Fruit(name='oranges', number=1)]
```

### Sort by method call.

```
>>> class Fruit(object):
...     def __init__(self, name, number):
...         self.name = name
...         self.number = number
...     def get_name(self):
...         return self.name
...     def get_number(self):
...         return self.number
...     def __repr__(self):
...         return '%s:%s' % (self.name, self.number)
...
>>> s = Sortable(set([Fruit('apples', 3), Fruit('bananas', 2), Fruit('oranges', 1)]))
>>> s.sorted(method='get_name')
[apples:3, bananas:2, oranges:1]
>>> s.sorted(method='get_number')
[oranges:1, bananas:2, apples:3]
>>> s.sorted(method='get_name', reverse=True)
[oranges:1, bananas:2, apples:3]
```

## Goals & philsophy

 * create an intuitive and readable sorting syntax
 * be as unabtrusive as possible
 * don't break existing sort approaches
 * don't try to be all things to all sorting needs

Toward these ideals, sortables:

 * replaces awkward operator and lambda syntax with a simple readable syntax
 * uses a single Sortable factory for all series data structures and dicts
 * mimics (and internally utilizes) Python's `sorted` builtin, but does not replace it
 * focuses on the most common use cases. Fall back to the builtin `sorted` as needed.

## `sorted` returns a Sortable

A Sortable's sorted method, as well as a Sortable dict's `items` method return
a Sortable series. As with the `sorted` builtin, the series type is generally
a list.

## Regarding efficiency

In general, you can expect this to work as well as the `sorted` builtin since
that is what it uses internally.

Sortable `sorted` methods always return a copy of the data. This also goes for
the Sortable dict `items` method, which differs from the view-based `dict_items`
of a regular dictionary.

I have used operator getters rather than lambda based key interpretations mainly
because this was slightly faster for me in the few timeit tests that I ran to
make the decision.
