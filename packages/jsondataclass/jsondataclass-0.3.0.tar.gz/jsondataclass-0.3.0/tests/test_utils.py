import sys
from typing import Collection, Dict, List, Mapping, Optional, Union

import pytest

from jsondataclass.exceptions import WrongTypeError
from jsondataclass.utils import (
    extract_generic_args,
    extract_generic_origin,
    extract_optional_type,
    extract_union_types,
    is_generic,
    is_optional,
    is_subclass,
    is_union,
    type_check,
)


def test_is_generic():
    assert is_generic(List[int]) is True
    assert is_generic(int) is False


def test_is_subclass():
    assert is_subclass(List, Collection)
    assert is_subclass(Dict, Mapping)


def test_is_optional():
    assert is_optional(Optional[int]) is True
    assert is_optional(int) is False


def test_is_union():
    assert is_union(Union[int, str]) is True
    assert is_union(int) is False


def test_extract_generic_args():
    assert extract_generic_args(List[int]) == (int,)


def test_extract_generic_args_fail():
    with pytest.raises(TypeError):
        extract_generic_args(int)


def test_extract_generic_origin():
    assert extract_generic_origin(List[int]) is list


def test_extract_generic_origin_fail():
    with pytest.raises(TypeError):
        extract_generic_origin(int)


def test_type_check():
    type_check(1, int)


def test_type_check_fail():
    with pytest.raises(WrongTypeError):
        type_check(1, str)


def test_extract_optional_type():
    assert extract_optional_type(Optional[int]) is int


def test_extract_optional_type_fail():
    with pytest.raises(TypeError):
        extract_optional_type(int)


def test_extract_union_types():
    assert extract_union_types(Union[int, str]) == (int, str)


def test_extract_union_types_fail():
    with pytest.raises(TypeError):
        extract_union_types(int)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
def test_is_literal():
    from typing import Literal

    from jsondataclass.utils import is_literal

    assert is_literal(Literal[True]) is True
    assert is_literal(Literal[True, 1]) is True
    assert is_literal(int) is False


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
def test_extract_literal_values():
    from typing import Literal

    from jsondataclass.utils import extract_literal_values

    assert extract_literal_values(Literal[True]) == (True,)
    assert extract_literal_values(Literal[1, 2, 3]) == (1, 2, 3)
