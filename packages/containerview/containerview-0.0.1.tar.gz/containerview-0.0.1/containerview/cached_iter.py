from itertools import islice
from typing import Iterable, TypeVar, Generic

T = TypeVar('T')


class CacheIter(Generic[T], Iterable[T]):
    # todo test
    """
    >>> from itertools import count, islice
    >>> x = CacheIter(i**2 for i in count())
    >>> x[5]
    25
    >>> x[5]
    25
    >>> x[9]
    81
    >>> x[2]
    4
    >>> list(islice(x, 13))
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]
    >>> x[12:16]
    [144, 169, 196, 225]
    """

    def __init__(self, iter_: Iterable[T]):
        self.cache = []
        self.iter = iter(iter_)

    def fill_to(self, new_len):
        if new_len is None:
            self.cache.extend(self.iter)
        elif new_len > len(self.cache):
            self.cache.extend(islice(self.iter, new_len - len(self.cache)))

    def __getitem__(self, item):
        if isinstance(item, slice):
            stop = item.stop
            if not stop or stop <= 0:
                stop = None
            self.fill_to(stop)
        elif isinstance(item, int):
            self.fill_to(item + 1)
        return self.cache[item]

    def __iter__(self):
        yield from self.cache
        for y in self.iter:
            self.cache.append(y)
            yield y
