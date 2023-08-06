from dataclasses import MISSING, Field, dataclass, field
from typing import TYPE_CHECKING, Any, Optional, Type

from .exceptions import MissingDefaultValueError
from .utils import is_optional

if TYPE_CHECKING:
    from .serializers import Serializer  # noqa: F401

__all__ = ["Meta", "jsonfield", "JsonField"]

_METADATA_KEY = "_jsondataclass"


@dataclass
class Meta:
    serialized_name: Optional[str] = ""
    serializer_class: Optional[Type["Serializer"]] = None
    serializer_args: Optional[tuple] = None
    serializer_kwargs: Optional[dict] = None


def jsonfield(
    serialized_name: Optional[str] = "",
    *,
    serializer_class: Optional[Type["Serializer"]] = None,
    serializer_args: Optional[tuple] = None,
    serializer_kwargs: Optional[dict] = None,
    **field_kwargs,
):
    metadata = field_kwargs.setdefault("metadata", {})
    metadata[_METADATA_KEY] = Meta(serialized_name, serializer_class, serializer_args, serializer_kwargs)
    return field(**field_kwargs)


class JsonField:
    def __init__(self, field: Field, type_: Optional[Type] = None):
        self._field = field
        self.type = type_ if type_ is not None else field.type
        self._meta = field.metadata.get(_METADATA_KEY, Meta())

    @property
    def serialized_name(self) -> str:
        return self._meta.serialized_name or self._field.name

    @property
    def serializer_class(self) -> Type:
        return self._meta.serializer_class

    @property
    def serializer_args(self) -> tuple:
        args = self._meta.serializer_args
        return args if args is not None else tuple()

    @property
    def serializer_kwargs(self) -> dict:
        kwargs = self._meta.serializer_kwargs
        return kwargs if kwargs is not None else dict()

    @property
    def default_value(self) -> Any:
        if self._field.default is not MISSING:
            return self._field.default

        default_factory = self._field.default_factory  # type: ignore
        if default_factory is not MISSING:
            return default_factory()
        if is_optional(self._field.type):
            return None
        raise MissingDefaultValueError(self._field)

    def __getattr__(self, attr):
        return getattr(self._field, attr)
