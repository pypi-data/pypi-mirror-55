import sys
from dataclasses import fields
from typing import TYPE_CHECKING, Any, Generator, Optional, Tuple, Type, Union, get_type_hints

from .typing import DataClass

if TYPE_CHECKING:
    from .field import JsonField  # noqa: F401


def is_generic(type_: Type) -> bool:
    return hasattr(type_, "__origin__")


def is_subclass(type_a: Type, type_b: Type):
    try:
        return issubclass(type_a, type_b)
    except TypeError:
        return False


def is_union(type_: Type) -> bool:
    return is_generic(type_) and type_.__origin__ is Union


def is_optional(type_: Type) -> bool:
    if not is_union(type_) or not len(type_.__args__) == 2:
        return False
    return type(None) in type_.__args__


def extract_generic_args(type_: Type) -> Tuple[Type, ...]:
    if not is_generic(type_):
        raise TypeError(f"{type_} is not Generic")
    return type_.__args__


def extract_generic_origin(type_: Type[Any]) -> Any:
    if not is_generic(type_):
        raise TypeError(f"{type_} is not Generic")
    if is_optional(type_):
        return Optional
    return type_.__origin__


def type_check(data: Any, type_: Type):
    from .exceptions import WrongTypeError

    if not isinstance(data, type_):
        raise WrongTypeError(type_, data)


def set_forward_refs(dataclass: Type[DataClass], refs: dict):
    dataclass.__forward_refs__ = refs


def get_forward_refs(dataclass: Type[DataClass]):
    return getattr(dataclass, "__forward_refs__", {})


def dataclass_fields(dataclass: Type[DataClass]) -> Generator["JsonField", None, None]:
    from .field import JsonField  # noqa: F811

    forward_refs = get_forward_refs(dataclass)
    type_hints = get_type_hints(dataclass, globalns=forward_refs)
    for field in fields(dataclass):
        json_field = JsonField(field, type_hints[field.name])
        yield json_field


def extract_optional_type(type_: Type[Optional[Type]]) -> Type:
    if not is_optional(type_):
        raise TypeError(f"{type_} is not Optional")
    return extract_generic_args(type_)[0]


def extract_union_types(type_: Type[Union[Type]]) -> Tuple[Type, ...]:
    if not is_union(type_):
        raise TypeError(f"{type_} is not Union")
    return extract_generic_args(type_)


if sys.version_info >= (3, 8):
    from typing import Literal

    def is_literal(type_: Type):
        return is_generic(type_) and type_.__origin__ is Literal

    def extract_literal_values(type_: Type) -> Tuple[Any, ...]:
        if not is_literal(type_):
            raise TypeError(f"{type_} is not Literal")
        return extract_generic_args(type_)
