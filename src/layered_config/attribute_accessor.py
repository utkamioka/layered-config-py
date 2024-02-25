from __future__ import annotations
from abc import ABC
from typing import Mapping, Sequence


class AttributeAccessor(ABC):
    @classmethod
    def get(cls, obj):
        if isinstance(obj, Mapping):
            return AttributeMapping(**obj)
        if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray)):
            return AttributeSequence(obj)
        return obj


class AttributeMapping(Mapping, AttributeAccessor):
    def __init__(self, /, *args, **kwargs):
        self._store = dict(*args, **kwargs)

    def __repr__(self):
        return repr(self._store)

    def __len__(self):
        return len(self._store)

    def __iter__(self):
        return iter(self._store)

    def __getitem__(self, key):
        obj = self._store[key]
        return AttributeAccessor.get(obj)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            msg = f"{self.__class__.__name__!r} object has no attribute {item!r}"
            raise AttributeError(msg)


class AttributeSequence(Sequence, AttributeAccessor):
    def __init__(self, iterable=(), /):
        self._store = iterable

    def __repr__(self):
        return repr(self._store)

    def __len__(self):
        return len(self._store)

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            raise NotImplemented
        return list(self) == list(other)

    def __getitem__(self, index):
        obj = self._store[index]
        return AttributeAccessor.get(obj)
