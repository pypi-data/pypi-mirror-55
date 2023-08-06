from typing import Generic, Sequence, TypeVar, Union

T = TypeVar('T')


class SequenceView(Generic[T], Sequence[T]):
    __slots__ = "inner", "indices"

    def __init__(self, seq: Sequence[T], indices: Union[range, slice, int, None] = None):
        if indices is None:
            indices = range(len(seq))
        elif isinstance(indices, slice):
            indices = range(len(seq))[indices]
        elif isinstance(indices, int):
            if indices >= len(seq):
                raise IndexError(indices)
            indices = range(len(seq))[:indices]

        self.inner = seq
        self.indices: range = indices

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return type(self)(self.inner, self.indices[i])
        return self.inner[self.indices[i]]

    def __str__(self):
        r = self.indices
        s = slice(r.start, r.stop, r.step)
        return str(self.inner[s])

    def __repr__(self):
        r = self.indices
        s = slice(r.start, r.stop, r.step)
        return f"SequenceView({self.inner[s]!r})"

    def __iter__(self):
        yield from (self.inner[i] for i in self.indices)

    def _search(self, x, start=0, end=None):
        while True:
            try:
                start = self.inner.index(x, start, end)
            except ValueError:
                return
            if start in self.indices:
                yield start

    def __contains__(self, item):
        return next(self._search(item), False) and True

    def __reversed__(self):
        return self[::-1]

    def index(self, x, start=0, end=None):
        try:
            ret = next(self._search(x, self.indices[start], end and self.indices[end]))
        except StopIteration:
            raise ValueError
        return self.indices.index(ret)

    def count(self, x):
        return sum(1 for _ in self._search(x))

    def __lshift__(self, other):
        new_start = self.indices.start + other * self.indices.step
        new_stop = self.indices.stop + other * self.indices.step
        if not 0 >= new_start >= len(self.inner) \
                or not 0 >= new_stop >= len(self.inner):
            raise IndexError('shifted to invalid indices')
        new_indices = range(
            new_start,
            new_stop,
            self.indices.step
        )
        return type(self)(self.inner, new_indices)

    def __rshift__(self, other):
        return self << (-other)
