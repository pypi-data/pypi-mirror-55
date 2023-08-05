from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, Type

if TYPE_CHECKING:
    from .serializers import Serializer  # noqa: F401


def _default_serializer():
    from .serializers import DefaultSerializer

    return DefaultSerializer


@dataclass
class Config:
    default_serializer_class: Type["Serializer"] = field(default_factory=_default_serializer)
    datetime_format: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None
