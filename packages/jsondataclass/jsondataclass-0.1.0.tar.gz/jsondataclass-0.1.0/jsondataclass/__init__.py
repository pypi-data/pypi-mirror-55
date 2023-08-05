# -*- coding: utf-8 -*-

from .mapper import DataClassMapper, from_dict, from_json, to_dict, to_json
from .field import jsonfield

__all__ = ["DataClassMapper", "from_json", "from_dict", "to_json", "to_dict", "jsonfield"]

__author__ = """Aleksey Shulga"""
__email__ = "oleksii.shulga@gmail.com"
__version__ = "__version__ = '0.1.0'"
