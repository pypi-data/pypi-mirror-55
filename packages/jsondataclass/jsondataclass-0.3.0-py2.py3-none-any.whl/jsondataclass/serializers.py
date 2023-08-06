import sys
from abc import abstractmethod
from datetime import date, datetime, time, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Collection, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union

from .config import Config
from .exceptions import JsonDataClassError, TupleTypeMatchError, UnionTypeMatchError
from .field import JsonField
from .typing import DataClass
from .utils import (
    dataclass_fields,
    extract_generic_args,
    extract_generic_origin,
    extract_optional_type,
    extract_union_types,
    is_generic,
    is_optional,
    is_subclass,
    type_check,
)

T = TypeVar("T")


class Serializer(Generic[T]):
    def __init__(self, serializer_factory: "SerializerFactory" = None, config: Config = None, *args, **kwargs):
        if config is None:
            config = Config()
        if serializer_factory is None:
            serializer_factory = SerializerFactory(config)
        self._serializer_factory = serializer_factory
        self._config = config

    @abstractmethod
    def serialize(self, data: T) -> Any:
        ...

    @abstractmethod
    def deserialize(self, data: Any, type_: Type[T]) -> T:
        ...


class DefaultSerializer(Serializer[Any]):
    def serialize(self, data: Any) -> Any:
        return data

    def deserialize(self, data: Any, type_: Type) -> Any:
        return data


class StringSerializer(Serializer[str]):
    def serialize(self, data: Any) -> str:
        return str(data)

    def deserialize(self, data: Any, type_: Type[str]) -> str:
        return str(data)


def _serialize_collection(data: Collection, serializer_factory: "SerializerFactory") -> List:
    result = []
    for value in data:
        serializer = serializer_factory.get_serializer(type(value))
        result.append(serializer.serialize(value))
    return result


class ListSerializer(Serializer[List]):
    def serialize(self, data: List) -> List:
        return _serialize_collection(data, self._serializer_factory)

    def deserialize(self, data: list, type_: Type[List]) -> List:
        type_check(data, list)
        if not is_generic(type_):
            return list(data)
        item_type = extract_generic_args(type_)[0]
        serializer = self._serializer_factory.get_serializer(item_type)
        return list(serializer.deserialize(item, item_type) for item in data)


class TupleSerializer(Serializer[Tuple]):
    def serialize(self, data: Tuple) -> List:
        return _serialize_collection(data, self._serializer_factory)

    def _deserilize_generic(self, data: list, type_: Type[Tuple]) -> Tuple:
        item_types = extract_generic_args(type_)
        if len(item_types) == 0:
            return tuple(data)
        if len(item_types) == 2 and item_types[1] is Ellipsis:
            item_type = item_types[0]
            serializer = self._serializer_factory.get_serializer(item_type)
            return tuple(serializer.deserialize(item, item_type) for item in data)
        if len(item_types) != len(data):
            raise TupleTypeMatchError(type_, data)
        result = []
        for item, item_type in zip(data, item_types):
            serializer = self._serializer_factory.get_serializer(item_type)
            result.append(serializer.deserialize(item, item_type))
        return tuple(result)

    def deserialize(self, data: list, type_: Type[Tuple]) -> Tuple:
        type_check(data, list)
        if not is_generic(type_):
            return tuple(data)
        return self._deserilize_generic(data, type_)


class DictSerializer(Serializer[Dict]):
    def serialize(self, data: Dict) -> Dict:
        result = {}
        for key, value in data.items():
            serializer = self._serializer_factory.get_serializer(type(value))
            result[str(key)] = serializer.serialize(value)
        return result

    def _deserialize_generic(self, data: dict, type_: Type[Dict]) -> Dict:
        key_type, value_type = extract_generic_args(type_)[:2]
        if isinstance(key_type, TypeVar):  # type: ignore
            return dict(data)
        serializer = self._serializer_factory.get_serializer(value_type)
        return dict((key_type(key), serializer.deserialize(value, value_type)) for key, value in data.items())

    def deserialize(self, data: dict, type_: Type[Dict]) -> Dict:
        type_check(data, dict)
        if not is_generic(type_):
            return dict(data)
        return self._deserialize_generic(data, type_)


class DataClassSerializer(Serializer[DataClass]):
    def _get_field_serializer(self, field: JsonField):
        serializer_class = field.serializer_class
        if serializer_class is None:
            serializer_class = self._serializer_factory.get_serializer_class(field.type)
        return self._serializer_factory.create_serializer(
            serializer_class, *field.serializer_args, **field.serializer_kwargs
        )

    def serialize(self, data: DataClass) -> dict:
        result = {}
        for field in dataclass_fields(type(data)):
            value = getattr(data, field.name)
            if value is None and not is_optional(field.type):
                value = field.default_value
            serializer = self._get_field_serializer(field)
            result[field.serialized_name] = serializer.serialize(value)
        return result

    def deserialize(self, data: dict, type_: Type[DataClass]) -> DataClass:
        type_check(data, dict)
        init_kwargs = {}
        for field in dataclass_fields(type_):
            value = data.get(field.serialized_name)
            if value is None and not is_optional(field.type):
                value = field.default_value
            serializer = self._get_field_serializer(field)
            init_kwargs[field.name] = serializer.deserialize(value, field.type)
        return type_(**init_kwargs)


class OptionalSerializer(Serializer[Optional[Type]]):
    def serialize(self, data: Any) -> Any:
        if data is None:
            return None
        serializer = self._serializer_factory.get_serializer(type(data))
        return serializer.serialize(data)

    def deserialize(self, data: Any, type_: Type[Optional[Type]]) -> Optional[Type]:
        optional_type = extract_optional_type(type_)
        if data is not None:
            serializer = self._serializer_factory.get_serializer(optional_type)
            return serializer.deserialize(data, optional_type)
        return None


class UnionSerializer(Serializer[Union[Type]]):
    def serialize(self, data: Any) -> Any:
        serializer = self._serializer_factory.get_serializer(type(data))
        return serializer.serialize(data)

    def deserialize(self, data: Any, type_: Type[Union[Type]]) -> Union[Type]:
        union_types = extract_union_types(type_)
        if type(data) in union_types:
            union_type = type(data)
            serializer = self._serializer_factory.get_serializer(union_type)
            return serializer.deserialize(data, union_type)
        for union_type in union_types:
            try:
                serializer = self._serializer_factory.get_serializer(union_type)
                value = serializer.deserialize(data, union_type)
                if isinstance(value, union_type):
                    return value
            except (TypeError, ValueError, JsonDataClassError):
                pass
        raise UnionTypeMatchError(type_, data)


def _serialize_datetime(data: Union[datetime, date, time], format: Optional[str]) -> str:
    if format is None:
        return data.isoformat()
    return data.strftime(format)


class DateTimeSerializerBase(Serializer[T]):
    _config_format_attr = NotImplemented

    def __init__(
        self, serializer_factory: "SerializerFactory" = None, config: Config = None, format: Optional[str] = None
    ):
        super().__init__(serializer_factory, config)
        self._format: Optional[str] = format if format is not None else getattr(self._config, self._config_format_attr)


class DateTimeSerializer(DateTimeSerializerBase[datetime]):
    _config_format_attr = "datetime_format"

    def serialize(self, data: datetime) -> str:
        return _serialize_datetime(data, self._format)

    def deserialize(self, data: str, type_: Type[datetime]) -> datetime:
        if self._format is None:
            return datetime.fromisoformat(data)
        return datetime.strptime(data, self._format)


class DateSerializer(DateTimeSerializerBase[date]):
    _config_format_attr = "date_format"

    def serialize(self, data: date) -> str:
        return _serialize_datetime(data, self._format)

    def deserialize(self, data: str, type_: Type[date]) -> date:
        if self._format is None:
            return date.fromisoformat(data)
        return datetime.strptime(data, self._format).date()


class TimeSerializer(DateTimeSerializerBase[time]):
    _config_format_attr = "time_format"

    def serialize(self, data: time) -> str:
        return _serialize_datetime(data, self._format)

    def deserialize(self, data: str, type_: Type[time]) -> time:
        if self._format is None:
            return time.fromisoformat(data)
        return datetime.strptime(data, self._format).time()


class TimestampSerializer(Serializer[datetime]):
    def __init__(
        self,
        serializer_factory: "SerializerFactory" = None,
        config: Config = None,
        timezone: Optional[timezone] = None,
    ):
        super().__init__(serializer_factory, config)
        self._timezone = timezone

    def serialize(self, data: datetime) -> int:
        return int(data.timestamp())

    def deserialize(self, data: int, type_: Type[datetime]) -> datetime:
        return datetime.fromtimestamp(data, tz=self._timezone)


class EnumSerializer(Serializer[Enum]):
    def serialize(self, data: Enum) -> Any:
        return data.value

    def deserialize(self, data: Any, type_: Type[Enum]) -> Enum:
        return type_(data)


class DecimalSerializer(Serializer[Decimal]):
    def serialize(self, data: Decimal) -> str:
        return str(data)

    def deserialize(self, data: str, type_: Type[Decimal]) -> Decimal:
        return Decimal(data)


SERIALIZERS: tuple = (
    (DataClass, DataClassSerializer),
    (str, StringSerializer),
    (list, ListSerializer),
    (tuple, TupleSerializer),
    (dict, DictSerializer),
    (Optional, OptionalSerializer),
    (Union, UnionSerializer),
    (datetime, DateTimeSerializer),
    (date, DateSerializer),
    (time, TimeSerializer),
    (datetime.timestamp, TimestampSerializer),
    (Enum, EnumSerializer),
    (Decimal, DecimalSerializer),
)

if sys.version_info >= (3, 8):
    from typing import Literal
    from .utils import extract_literal_values
    from .exceptions import LiteralTypeMatchError

    class LiteralSerializer(Serializer):
        def serialize(self, data: Any) -> Any:
            return data

        def deserialize(self, data: Any, type_: Type) -> Any:
            literal_values = extract_literal_values(type_)
            if data not in literal_values:
                raise LiteralTypeMatchError(type_, data)
            return data

    SERIALIZERS += ((Literal, LiteralSerializer),)


class SerializerFactory:
    def __init__(self, config: Optional[Config] = None):
        self._serializers: Dict[Type, Type[Serializer]] = dict(SERIALIZERS)
        if config is None:
            config = Config()
        self._config = config

    def register(self, type_: Type, serializer_class: Type[Serializer]):
        self._serializers[type_] = serializer_class

    def unregister(self, type_: Type):
        del self._serializers[type_]

    def create_serializer(self, serializer_class: Type[Serializer], *args, **kwargs) -> Serializer:
        return serializer_class(self, self._config, *args, **kwargs)

    def get_serializer_class(self, type_: Type) -> Type[Serializer]:
        serializer_class = self._serializers.get(type_)
        if serializer_class:
            return serializer_class
        if is_generic(type_):
            type_ = extract_generic_origin(type_)
            return self.get_serializer_class(type_)
        for t, serializer_class in self._serializers.items():
            if is_subclass(type_, t):
                return serializer_class
        if self._config.default_serializer_class is not None:
            return self._config.default_serializer_class
        return DefaultSerializer

    def get_serializer(self, type_: Type) -> Serializer:
        serializer_class = self.get_serializer_class(type_)
        return self.create_serializer(serializer_class)
