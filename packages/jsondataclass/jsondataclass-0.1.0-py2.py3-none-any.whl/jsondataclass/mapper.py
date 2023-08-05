import json
from typing import Any, Optional, Type, TypeVar

from .config import Config
from .serializers import Serializer, SerializerFactory
from .typing import DataClass

T = TypeVar("T")


class DataClassMapper:
    def __init__(self, serializer_factory: Optional[SerializerFactory] = None, config: Optional[Config] = None):
        if config is None:
            config = Config()
        self._config = config
        if serializer_factory is None:
            serializer_factory = SerializerFactory(self._config)
        self._serializer_factory = serializer_factory

    @property
    def default_serializer_class(self) -> Type[Serializer]:
        return self._config.default_serializer_class

    @default_serializer_class.setter
    def default_serializer_class(self, serializer_class: Type[Serializer]):
        self._config.default_serializer_class = serializer_class

    @property
    def datetime_format(self) -> Optional[str]:
        return self._config.datetime_format

    @datetime_format.setter
    def datetime_format(self, format: str):
        self._config.datetime_format = format

    @property
    def date_format(self) -> Optional[str]:
        return self._config.date_format

    @date_format.setter
    def date_format(self, format: str):
        self._config.date_format = format

    @property
    def time_format(self) -> Optional[str]:
        return self._config.time_format

    @time_format.setter
    def time_format(self, format: str):
        self._config.time_format = format

    def register_serializer(self, type_: Type, serializer_class: Type[Serializer]):
        self._serializer_factory.register(type_, serializer_class)

    def unregister_serializer(self, type_: Type):
        self._serializer_factory.unregister(type_)

    def from_json(self, json_: str, type_: Type[T], **loads_kwargs: Any) -> T:
        data = json.loads(json_, **loads_kwargs)
        serializer = self._serializer_factory.get_serializer(type_)
        return serializer.deserialize(data, type_)

    def to_json(self, dataclass: DataClass, **dumps_kwargs: Any) -> str:
        serializer = self._serializer_factory.get_serializer(type(dataclass))
        data = serializer.serialize(dataclass)
        return json.dumps(data, **dumps_kwargs)

    def from_dict(self, data: dict, type_: Type[T]) -> T:
        serializer = self._serializer_factory.get_serializer(type_)
        return serializer.deserialize(data, type_)

    def to_dict(self, dataclass: DataClass) -> dict:
        serializer = self._serializer_factory.get_serializer(type(dataclass))
        data = serializer.serialize(dataclass)
        return data


def from_json(json_: str, type_: Type[T], **loads_kwargs: Any) -> T:
    mapper = DataClassMapper()
    return mapper.from_json(json_, type_)


def to_json(dataclass: DataClass, **dumps_kwargs: Any) -> str:
    mapper = DataClassMapper()
    return mapper.to_json(dataclass, **dumps_kwargs)


def from_dict(data: dict, type_: Type[T]) -> T:
    mapper = DataClassMapper()
    return mapper.from_dict(data, type_)


def to_dict(dataclass: DataClass) -> dict:
    mapper = DataClassMapper()
    return mapper.to_dict(dataclass)
