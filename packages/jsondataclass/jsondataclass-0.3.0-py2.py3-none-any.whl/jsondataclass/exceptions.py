import sys
from dataclasses import Field
from typing import Any, Type

from .utils import extract_generic_args


class JsonDataClassError(Exception):
    ...


class MissingDefaultValueError(JsonDataClassError):
    def __init__(self, field: Field):
        self._field = field

    def __str__(self) -> str:
        return f"Missing default value for field: {self._field!r}"


class WrongTypeError(JsonDataClassError):
    def __init__(self, expected_type: Type, value: Any):
        self._expected_type = expected_type
        self._value = value

    def __str__(self) -> str:
        return f"Expected value of a type: {self._expected_type!r}, but received: {type(self._value)!r}"


class TupleTypeMatchError(JsonDataClassError):
    def __init__(self, tuple_type: Type, value: list):
        self._tuple_type = tuple_type
        self._value = value

    def __str__(self) -> str:
        expected_length = len(extract_generic_args(self._tuple_type))
        return f"Expected list with length: {expected_length}, but received: {len(self._value)}"


class UnionTypeMatchError(JsonDataClassError):
    def __init__(self, union: Type, value: Any):
        self._union = union
        self._value = value

    def __str__(self) -> str:
        return f"{type(self._value)} does not match any type of {self._union!r}"


if sys.version_info >= (3, 8):

    class LiteralTypeMatchError(JsonDataClassError):
        def __init__(self, literal: Type, value: Any):
            self._literal = literal
            self._value = value

        def __str__(self) -> str:
            return f"{self._value} does not match any value of {self._literal!r}"
