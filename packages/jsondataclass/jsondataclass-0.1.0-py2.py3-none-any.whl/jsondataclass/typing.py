from abc import ABCMeta
from dataclasses import is_dataclass
from typing import ClassVar


class Final(ABCMeta):
    def __new__(cls, name, bases, namespace):
        for b in bases:
            if isinstance(b, Final):
                raise TypeError(f"type '{b.__name__}' is not an acceptable base type")
        return super().__new__(cls, name, bases, dict(namespace))


class DataClass(metaclass=Final):
    """Internal indicator of dataclass for using with isinstance and issubclass."""

    __forward_refs__: ClassVar[dict]

    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls} cannot be used for instance creation")

    @classmethod
    def __subclasshook__(cls, C):
        return is_dataclass(C)
