# -*- encoding: utf-8 -*-
""""""
import copy
from random import randint


def get_single_from_list(source_list):
    """Returns a random instance from a list."""
    max = len(source_list)
    return source_list[randint(0, max - 1)]


def rewrite_dict(source_dict, diffs):
    """Returns a copy of source_dict, updated with the new key-value
       pairs in diffs."""
    result = copy.deepcopy(source_dict)
    result.update(diffs)
    return result


def rename_def(source_dict, new_name):
    """Returns an existing data defintion with a new field name."""
    return rewrite_dict(source_dict, {"name": new_name})
