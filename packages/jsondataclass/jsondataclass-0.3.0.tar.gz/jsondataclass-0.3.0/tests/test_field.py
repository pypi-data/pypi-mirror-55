from dataclasses import Field, dataclass, fields
from typing import Optional

import pytest

from jsondataclass.exceptions import MissingDefaultValueError
from jsondataclass.field import _METADATA_KEY, JsonField, jsonfield
from jsondataclass.serializers import DefaultSerializer


def test_jsonfield_creation():
    field = jsonfield()
    assert isinstance(field, Field)


def test_jsonfield_serialized_name():
    field = jsonfield(serialized_name="field1")
    assert field.metadata[_METADATA_KEY].serialized_name == "field1"


def test_jsonfield_serializer_class():
    field = jsonfield(serializer_class=DefaultSerializer)
    assert field.metadata[_METADATA_KEY].serializer_class == DefaultSerializer


def test_jsonfield_serializer_args():
    field = jsonfield(serializer_args=[1, 2, 3])
    assert field.metadata[_METADATA_KEY].serializer_args == [1, 2, 3]


def test_jsonfield_serializer_kwargs():
    field = jsonfield(serializer_kwargs={"a": 1, "b": 2})
    assert field.metadata[_METADATA_KEY].serializer_kwargs == {"a": 1, "b": 2}


def test_field_default_value():
    @dataclass
    class Foo:
        a: Optional[str]
        b: str = "b"
        c: str = jsonfield(default="c")
        d: str = jsonfield(default_factory=lambda: "d")

    field_a = JsonField(fields(Foo)[0])
    field_b = JsonField(fields(Foo)[1])
    field_c = JsonField(fields(Foo)[2])
    field_d = JsonField(fields(Foo)[3])
    assert field_a.default_value is None
    assert field_b.default_value == "b"
    assert field_c.default_value == "c"
    assert field_d.default_value == "d"


def test_field_missing_default_value():
    @dataclass
    class Foo:
        a: str

    field = JsonField(fields(Foo)[0])

    with pytest.raises(MissingDefaultValueError):
        field.default_value
