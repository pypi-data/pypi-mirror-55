import json
import sys
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

import pytest

from jsondataclass.mapper import DataClassMapper, from_dict, from_json, to_dict, to_json
from jsondataclass.serializers import StringSerializer


class BaseTestMapping(metaclass=ABCMeta):
    def setup(self):
        self._mapper = DataClassMapper()

    @property
    @abstractmethod
    def dataclass_type(self):
        ...

    @property
    @abstractmethod
    def dataclass_obj(self):
        ...

    @property
    @abstractmethod
    def json_string(self):
        ...

    def test_from_json(self):
        assert self._mapper.from_json(self.json_string, self.dataclass_type) == self.dataclass_obj

    def test_from_dict(self):
        data = json.loads(self.json_string)
        assert self._mapper.from_dict(data, self.dataclass_type) == self.dataclass_obj

    def test_to_json(self):
        assert self._mapper.to_json(self.dataclass_obj) == self.json_string

    def test_to_dict(self):
        data = json.loads(self.json_string)
        assert self._mapper.to_dict(self.dataclass_obj) == data


class TestMappingDataClassWithInt(BaseTestMapping):
    @dataclass
    class Data:
        foo: int

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=1)

    @property
    def json_string(self):
        return '{"foo": 1}'


class TestMappingDataClassWithDecimal(BaseTestMapping):
    @dataclass
    class Data:
        foo: Decimal

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=Decimal("11.22"))

    @property
    def json_string(self):
        return '{"foo": "11.22"}'


class TestMappingDataClassWithStr(BaseTestMapping):
    @dataclass
    class Data:
        foo: str

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo="bar")

    @property
    def json_string(self):
        return '{"foo": "bar"}'


class TestMappingDataClassWithBool(BaseTestMapping):
    @dataclass
    class Data:
        foo: bool

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=True)

    @property
    def json_string(self):
        return '{"foo": true}'


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
class TestMappingDataClassWithLiteral(BaseTestMapping):
    @property
    def dataclass_type(self):
        from typing import Literal

        if hasattr(self, "dataclass"):
            return self.dataclass

        @dataclass
        class Data:
            foo: Literal[1]

        self.dataclass = Data
        return Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=1)

    @property
    def json_string(self):
        return '{"foo": 1}'


class TestMappingDataClassWithFloat(BaseTestMapping):
    @dataclass
    class Data:
        foo: float

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=1.1)

    @property
    def json_string(self):
        return '{"foo": 1.1}'


class TestMappingDataClassWithDict(BaseTestMapping):
    @dataclass
    class Data:
        foo: dict

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo={"bar": "baz"})

    @property
    def json_string(self):
        return '{"foo": {"bar": "baz"}}'


class TestMappingDataClassWithGenericDict(BaseTestMapping):
    @dataclass
    class Data:
        foo: Dict[str, int]

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo={"bar": 1})

    @property
    def json_string(self):
        return '{"foo": {"bar": 1}}'


class TestMappingDataClassWithList(BaseTestMapping):
    @dataclass
    class Data:
        foo: list

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=[1, 2, 3])

    @property
    def json_string(self):
        return '{"foo": [1, 2, 3]}'


class TestMappingDataClassWithGenericList(BaseTestMapping):
    @dataclass
    class Data:
        foo: List[str]

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=["a", "b", "c"])

    @property
    def json_string(self):
        return '{"foo": ["a", "b", "c"]}'


class TestMappingDataClassWithTuple(BaseTestMapping):
    @dataclass
    class Data:
        foo: tuple

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=(1, 2, 3))

    @property
    def json_string(self):
        return '{"foo": [1, 2, 3]}'


class TestMappingDataClassWithGenericTuple(BaseTestMapping):
    @dataclass
    class Data:
        foo: Tuple[int, str, bool]

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=(1, "2", True))

    @property
    def json_string(self):
        return '{"foo": [1, "2", true]}'


class TestMappingDataClassWithOptional(BaseTestMapping):
    @dataclass
    class Data:
        foo: Optional[int]

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=1)

    @property
    def json_string(self):
        return '{"foo": 1}'


class TestMappingDataClassWithUnion(BaseTestMapping):
    @dataclass
    class Data:
        foo: Union[int, str]

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=1)

    @property
    def json_string(self):
        return '{"foo": 1}'


class TestMappingDataClassWithDateTime(BaseTestMapping):
    @dataclass
    class Data:
        foo: datetime

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=datetime(2010, 1, 1, 0, 0, 0))

    @property
    def json_string(self):
        return '{"foo": "2010-01-01T00:00:00"}'


class TestMappingDataClassWithDateTimeFormat(BaseTestMapping):
    @dataclass
    class Data:
        foo: datetime

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=datetime(2010, 1, 1, 0, 0, 0))

    @property
    def json_string(self):
        return '{"foo": "01/01/10 00:00:00"}'

    def setup(self):
        mapper = DataClassMapper()
        mapper.datetime_format = "%m/%d/%y %H:%M:%S"
        self._mapper = mapper


class TestMappingDataClassWithDate(BaseTestMapping):
    @dataclass
    class Data:
        foo: date

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=date(2010, 1, 1))

    @property
    def json_string(self):
        return '{"foo": "2010-01-01"}'


class TestMappingDataClassWithDateFormat(BaseTestMapping):
    @dataclass
    class Data:
        foo: date

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=date(2010, 1, 1))

    @property
    def json_string(self):
        return '{"foo": "01/01/10"}'

    def setup(self):
        mapper = DataClassMapper()
        mapper.date_format = "%m/%d/%y"
        self._mapper = mapper


class TestMappingDataClassWithTime(BaseTestMapping):
    @dataclass
    class Data:
        foo: time

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=datetime(2010, 1, 1, 0, 0, 0).time())

    @property
    def json_string(self):
        return '{"foo": "00:00:00"}'


class TestMappingDataClassWithTimeFormat(BaseTestMapping):
    @dataclass
    class Data:
        foo: time

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=datetime(2010, 1, 1, 0, 0, 0).time())

    @property
    def json_string(self):
        return '{"foo": "12:00 AM"}'

    def setup(self):
        mapper = DataClassMapper()
        mapper.time_format = "%I:%M %p"
        self._mapper = mapper


class TestMappingDataClassWithTimestamp(BaseTestMapping):
    @dataclass
    class Data:
        foo: datetime.timestamp

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=datetime.fromtimestamp(946728000))

    @property
    def json_string(self):
        return '{"foo": 946728000}'


class TestMappingDataClassWithEnum(BaseTestMapping):
    class Color(Enum):
        WHITE = 0
        BLACK = 1

    @property
    def dataclass_type(self):
        if hasattr(self, "_dataclass_type"):
            return self._dataclass_type

        @dataclass
        class Data:
            foo: self.Color

        self._dataclass_type = Data
        return self._dataclass_type

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=self.Color.WHITE)

    @property
    def json_string(self):
        return '{"foo": 0}'


class TestMappingDataClassWithNestedDataClass(BaseTestMapping):
    @dataclass
    class Nested:
        bar: str

    @property
    def dataclass_type(self):
        if hasattr(self, "_dataclass_type"):
            return self._dataclass_type

        @dataclass
        class Data:
            foo: self.Nested

        self._dataclass_type = Data
        return self._dataclass_type

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo=self.Nested("baz"))

    @property
    def json_string(self):
        return '{"foo": {"bar": "baz"}}'


class TestMappingWithDefultSerializer(BaseTestMapping):
    @dataclass
    class Data:
        foo: ...

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo="1")

    @property
    def json_string(self):
        return '{"foo": 1}'

    def setup(self):
        mapper = DataClassMapper()
        mapper.default_serializer_class = StringSerializer
        self._mapper = mapper

    def test_to_json(self):
        ...

    def test_to_dict(self):
        ...


class TestMappingWithRegisterSerializer(BaseTestMapping):
    @dataclass
    class Data:
        foo: int

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo="1")

    @property
    def json_string(self):
        return '{"foo": 1}'

    def setup(self):
        mapper = DataClassMapper()
        mapper.register_serializer(int, StringSerializer)
        self._mapper = mapper

    def test_to_json(self):
        ...

    def test_to_dict(self):
        ...


class TestMappingWithUnregisterSerializer(BaseTestMapping):
    @dataclass
    class Data:
        foo: time

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo="12:00:00")

    @property
    def json_string(self):
        return '{"foo": "12:00:00"}'

    def setup(self):
        mapper = DataClassMapper()
        mapper.unregister_serializer(time)
        self._mapper = mapper

    def test_to_json(self):
        ...

    def test_to_dict(self):
        ...


def test_set_datetime_format():
    format = "%Y-%m-%d %H:%M:%S%"
    mapper = DataClassMapper()
    mapper.datetime_format = format
    assert mapper.datetime_format == mapper._config.datetime_format == format


def test_set_date_format():
    format = "%Y %m %d"
    mapper = DataClassMapper()
    mapper.date_format = format
    assert mapper.date_format == mapper._config.date_format == format


def test_set_time_format():
    format = "%H:%M"
    mapper = DataClassMapper()
    mapper.time_format = format
    assert mapper.time_format == mapper._config.time_format == format


def test_set_default_serializer_class():
    serializer_class = StringSerializer
    mapper = DataClassMapper()
    mapper.default_serializer_class = serializer_class
    assert mapper.default_serializer_class == mapper._config.default_serializer_class == serializer_class


class TestMapping(BaseTestMapping):
    @dataclass
    class Data:
        foo: str

    @property
    def dataclass_type(self):
        return self.Data

    @property
    def dataclass_obj(self):
        return self.dataclass_type(foo="bar")

    @property
    def json_string(self):
        return '{"foo": "bar"}'

    def test_from_json(self):
        assert from_json(self.json_string, self.dataclass_type) == self.dataclass_obj

    def test_from_dict(self):
        data = json.loads(self.json_string)
        assert from_dict(data, self.dataclass_type) == self.dataclass_obj

    def test_to_json(self):
        assert to_json(self.dataclass_obj) == self.json_string

    def test_to_dict(self):
        data = json.loads(self.json_string)
        assert to_dict(self.dataclass_obj) == data
