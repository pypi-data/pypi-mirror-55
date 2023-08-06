import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

import pytest

from jsondataclass.exceptions import MissingDefaultValueError, UnionTypeMatchError, WrongTypeError
from jsondataclass.field import jsonfield
from jsondataclass.serializers import (
    DataClassSerializer,
    DateSerializer,
    DateTimeSerializer,
    DecimalSerializer,
    DefaultSerializer,
    DictSerializer,
    EnumSerializer,
    ListSerializer,
    OptionalSerializer,
    SerializerFactory,
    StringSerializer,
    TimeSerializer,
    TimestampSerializer,
    TupleSerializer,
    UnionSerializer,
)
from jsondataclass.utils import set_forward_refs


def test_default_serializer():
    serializer = DefaultSerializer()
    assert serializer.deserialize(1, int) == 1
    assert serializer.serialize(1) == 1


def test_serializer_factory_create_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.create_serializer(DefaultSerializer), DefaultSerializer)


def test_serializer_factory_get_serializer_class():
    factory = SerializerFactory()
    assert factory.get_serializer_class(int) is DefaultSerializer


def test_serializer_factory_get_default_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(int), DefaultSerializer)


def test_serializer_factory_get_string_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(str), StringSerializer)


def test_serializer_factory_get_list_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(list), ListSerializer)
    assert isinstance(factory.get_serializer(List), ListSerializer)
    assert isinstance(factory.get_serializer(List[int]), ListSerializer)


def test_serializer_factory_get_tuple_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(tuple), TupleSerializer)
    assert isinstance(factory.get_serializer(Tuple), TupleSerializer)
    assert isinstance(factory.get_serializer(Tuple[int, ...]), TupleSerializer)


def test_serializer_factory_get_dict_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(dict), DictSerializer)
    assert isinstance(factory.get_serializer(Dict), DictSerializer)
    assert isinstance(factory.get_serializer(Dict[str, int]), DictSerializer)


def test_serializer_factory_get_dataclass_serializer():
    @dataclass
    class Data:
        foo: int
        bar: str

    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(Data), DataClassSerializer)


def test_serializer_factory_get_optional_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(Optional[int]), OptionalSerializer)


def test_serializer_factory_get_union_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(Union[int, str]), UnionSerializer)


def test_serializer_factory_get_datetime_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(datetime), DateTimeSerializer)


def test_serializer_factory_get_date_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(date), DateSerializer)


def test_serializer_factory_get_time_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(time), TimeSerializer)


def test_serializer_factory_get_timestamp_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(datetime.timestamp), TimestampSerializer)


def test_serializer_factory_get_enum_serializer():
    class Foo(Enum):
        A = 1
        B = 2

    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(Enum), EnumSerializer)
    assert isinstance(factory.get_serializer(Foo), EnumSerializer)


def test_serializer_factory_get_decimal_serializer():
    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(Decimal), DecimalSerializer)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
def test_serializer_factory_get_literal_serializer():
    from typing import Literal

    from jsondataclass.serializers import LiteralSerializer

    factory = SerializerFactory()
    assert isinstance(factory.get_serializer(Literal[True]), LiteralSerializer)


def test_string_serializer():
    data = "foo"
    serializer = StringSerializer()
    assert serializer.deserialize(data, str) == data
    assert serializer.serialize(data) == data


def test_list_serializer():
    data = [1, 2, 3]
    serializer = ListSerializer()
    assert serializer.deserialize(data, list) == data
    assert serializer.deserialize(data, List) == data
    assert serializer.deserialize(data, List[int]) == data
    assert serializer.deserialize(data, List[str]) == ["1", "2", "3"]
    assert serializer.serialize(data) == data


def test_tuple_serializer():
    list_data = [1, 2, 3]
    tuple_data = (1, 2, 3)
    serializer = TupleSerializer()
    assert serializer.deserialize(list_data, tuple) == tuple_data
    assert serializer.deserialize(list_data, Tuple) == tuple_data
    assert serializer.deserialize(list_data, Tuple[int, ...]) == tuple_data
    assert serializer.deserialize(list_data, Tuple[int, int, int]) == tuple_data
    assert serializer.serialize(tuple_data) == list_data


def test_dict_serializer():
    data = {"a": 1, "b": 2, "c": 3}
    serializer = DictSerializer()
    assert serializer.deserialize(data, dict) == data
    assert serializer.deserialize(data, Dict) == data
    assert serializer.deserialize(data, Dict[str, int]) == data
    assert serializer.deserialize(data, Dict[str, str]) == {"a": "1", "b": "2", "c": "3"}
    assert serializer.serialize(data) == data


def test_dataclass_serializer():
    @dataclass
    class Data:
        foo: int
        bar: str

    data_dict = {"foo": 1, "bar": "2"}
    data = Data(foo=1, bar="2")
    serializer = DataClassSerializer()
    assert serializer.deserialize(data_dict, Data) == data
    assert serializer.serialize(data) == data_dict


def test_dataclass_serializer_wrong_data():
    @dataclass
    class Data:
        foo: int
        bar: str

    serializer = DataClassSerializer()
    with pytest.raises(WrongTypeError):
        serializer.deserialize(1, Data)


def test_dataclass_serializer_nested_dataclass():
    @dataclass
    class Nested:
        foo: int
        bar: str

    @dataclass
    class Data:
        foo: int
        bar: Nested

    data_dict = {"foo": 1, "bar": {"foo": 2, "bar": "3"}}
    data = Data(foo=1, bar=Nested(foo=2, bar="3"))
    serializer = DataClassSerializer()
    assert serializer.deserialize(data_dict, Data) == data
    assert serializer.serialize(data) == data_dict


def test_dataclass_serializer_field_forward_reference():
    @dataclass
    class Foo:
        foo: int
        bar: "Bar"

    @dataclass
    class Bar:
        foo: int
        bar: str

    set_forward_refs(Foo, {"Bar": Bar})
    data_dict = {"foo": 1, "bar": {"foo": 2, "bar": "3"}}
    data = Foo(foo=1, bar=Bar(foo=2, bar="3"))
    serializer = DataClassSerializer()
    assert serializer.deserialize(data_dict, Foo) == data
    assert serializer.serialize(data) == data_dict


def test_dataclass_serializer_field_serialized_name():
    @dataclass
    class Data:
        foo: int = jsonfield("foo_foo")
        bar: str

    data_dict = {"foo_foo": 1, "bar": "2"}
    data = Data(foo=1, bar="2")
    serializer = DataClassSerializer()
    assert serializer.deserialize(data_dict, Data) == data
    assert serializer.serialize(data) == data_dict


def test_dataclass_serializer_field_default():
    @dataclass
    class Data:
        foo: int
        bar: str = "2"

    data_dict = {"foo": 1}
    data = Data(foo=1, bar="2")
    serializer = DataClassSerializer()
    assert serializer.deserialize(data_dict, Data) == data
    data_dict["bar"] = "2"
    assert serializer.serialize(data) == data_dict


def test_dataclass_serializer_field_default_factory():
    @dataclass
    class Data:
        foo: int
        bar: str = jsonfield(default_factory=lambda: "2")

    data_dict = {"foo": 1}
    data = Data(foo=1, bar="2")
    serializer = DataClassSerializer()
    assert serializer.deserialize(data_dict, Data) == data
    data_dict["bar"] = "2"
    assert serializer.serialize(data) == data_dict


def test_dataclass_serializer_deserialize_missing_field():
    @dataclass
    class Data:
        foo: int
        bar: str

    data_dict = {"foo": 1}
    serializer = DataClassSerializer()
    with pytest.raises(MissingDefaultValueError):
        serializer.deserialize(data_dict, Data)


def test_dataclass_serializer_serialize_none_field():
    @dataclass
    class Data:
        foo: int
        bar: str

    data = Data(foo=1, bar=None)
    serializer = DataClassSerializer()
    with pytest.raises(MissingDefaultValueError):
        serializer.serialize(data)


def test_dataclass_serializer_field_serializer():
    @dataclass
    class Data:
        foo: int = jsonfield(serializer_class=StringSerializer)
        bar: str

    data_dict = {"foo": 1, "bar": "2"}
    data = Data(foo="1", bar="2")
    serializer = DataClassSerializer()
    assert serializer.deserialize(data_dict, Data) == data
    data_dict = {"foo": "1", "bar": "2"}
    data = Data(foo=1, bar="2")
    assert serializer.serialize(data) == data_dict


def test_optional_serializer():
    data = 1
    serializer = OptionalSerializer()
    assert serializer.deserialize(data, Optional[int]) == data
    assert serializer.deserialize(None, Optional[int]) is None
    assert serializer.serialize(data) == data
    assert serializer.serialize(None) is None


def test_union_serializer():
    data = [1, 2, 3]
    serializer = UnionSerializer()
    assert serializer.deserialize(data, Union[dict, list]) == data
    assert serializer.serialize(data) == data


def test_union_serializer_type_missmatch():
    data = 1
    serializer = UnionSerializer()
    with pytest.raises(UnionTypeMatchError):
        serializer.deserialize(data, Union[dict, list]) == data


def test_datetime_serializer_naive_datetime():
    data = "2000-01-01T12:00:00"
    date = datetime(2000, 1, 1, 12, 0, 0)
    serializer = DateTimeSerializer()
    assert serializer.deserialize(data, datetime) == date
    assert serializer.serialize(date) == data


def test_datetime_serializer_aware_datetime():
    data = "2000-01-01T12:00:00+02:00"
    date = datetime(2000, 1, 1, 12, 0, tzinfo=timezone(timedelta(seconds=7200)))
    serializer = DateTimeSerializer()
    assert serializer.deserialize(data, datetime) == date
    assert serializer.serialize(date) == data


def test_datetime_serializer_format():
    data = "01/01/00 12:00:00"
    date = datetime(2000, 1, 1, 12, 0)
    serializer = DateTimeSerializer(format="%m/%d/%y %H:%M:%S")
    assert serializer.deserialize(data, datetime) == date
    assert serializer.serialize(date) == data


def test_date_serializer():
    data = "2000-01-01"
    date_ = datetime(2000, 1, 1).date()
    serializer = DateSerializer()
    assert serializer.deserialize(data, date) == date_
    assert serializer.serialize(date_) == data


def test_date_serializer_format():
    data = "01/01/00"
    date_ = datetime(2000, 1, 1).date()
    serializer = DateSerializer(format="%m/%d/%y")
    assert serializer.deserialize(data, date) == date_
    assert serializer.serialize(date_) == data


def test_time_serializer():
    data = "12:00:00"
    time_ = datetime(2000, 1, 1, 12, 0, 0).time()
    serializer = TimeSerializer()
    assert serializer.deserialize(data, time) == time_
    assert serializer.serialize(time_) == data


def test_time_serializer_format():
    data = "12:00 PM"
    time_ = datetime(2000, 1, 1, 12, 0, 0).time()
    serializer = TimeSerializer(format="%I:%M %p")
    assert serializer.deserialize(data, time) == time_
    assert serializer.serialize(time_) == data


def test_timestamp_serializer():
    now = datetime.now().replace(microsecond=0)
    timestamp_ = int(now.timestamp())
    serializer = TimestampSerializer()
    assert serializer.deserialize(timestamp_, datetime) == now
    assert serializer.serialize(now) == timestamp_


def test_timestamp_serializer_timezone():
    timestamp = 946728000
    date = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    serializer = TimestampSerializer(timezone=timezone.utc)
    assert serializer.deserialize(timestamp, datetime) == date
    assert serializer.serialize(date) == timestamp


def test_enum_serializer():
    class Foo(Enum):
        A = 1
        B = 2

    data = 1
    serializer = EnumSerializer()
    assert serializer.deserialize(data, Foo) == Foo.A
    assert serializer.serialize(Foo.A) == data


def test_decimal_serializer():
    data = "100.55"
    dec = Decimal("100.55")
    serializer = DecimalSerializer()
    assert serializer.deserialize(data, Decimal) == dec
    assert serializer.serialize(dec) == data


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
def test_literal_serializer():
    from typing import Literal

    from jsondataclass.serializers import LiteralSerializer

    seializer = LiteralSerializer()
    assert seializer.deserialize(1, Literal[1]) == 1
    assert seializer.deserialize(1, Literal[1, 2]) == 1
    assert seializer.serialize(1) == 1


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
def test_literal_serializer_fail():
    from typing import Literal

    from jsondataclass.serializers import LiteralSerializer
    from jsondataclass.exceptions import LiteralTypeMatchError

    seializer = LiteralSerializer()
    with pytest.raises(LiteralTypeMatchError):
        seializer.deserialize(5, Literal[1, 2, 3])
