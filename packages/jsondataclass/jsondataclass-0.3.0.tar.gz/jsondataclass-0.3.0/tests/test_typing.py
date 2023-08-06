from dataclasses import dataclass

import pytest

from jsondataclass.typing import DataClass


def test_dataclass_issubclass():
    @dataclass
    class Foo:
        a: int
        b: str

    assert issubclass(Foo, DataClass)
    assert issubclass(int, DataClass) is False


def test_dataclass_isinstance():
    @dataclass
    class Foo:
        a: int
        b: str

    data = Foo(1, "2")
    assert isinstance(data, DataClass)
    assert isinstance(1, DataClass) is False


def test_dataclass_instance_creation():
    with pytest.raises(TypeError):
        DataClass()


def test_dataclass_subclass():
    with pytest.raises(TypeError):

        class Data(DataClass):
            ...
