# -*- encoding: utf-8 -*-
""""""
import os
import importlib
from random import choice
from liar.ijusthelp import rewrite_dict
from liar.itransform import ITransform
from liar.iamprimitive import IAmPrimitive

self_dir = os.path.dirname(os.path.realpath(__file__))
app_path = os.sep.join(self_dir.split(os.sep)[:-1])


class IGetRaw(object):
    """IGetRaw pulls out data from the json files, or deals with static or quick_lists."""

    # gets data from a raw json file of data.
    def raw_list(data_def, data_prop, dataset_size=False, filters={}):
        """Pulls data from a raw data file."""

        raw = {}
        mod_name = f"liar.raw.{data_def}"
        mod = importlib.import_module(mod_name)
        jsn = getattr(mod, data_def)
        data = jsn or ["no", "data", "found"]

        # Filter the data?
        for filter_prop, filter_values in filters.items():
            data = [row for row in data if row[filter_prop] in filter_values]

        if not len(data):
            raise Exception(f"No records found. Did you filter correctly?")

        # Increase the size by doubling the set if there weren't enough records
        # in the raw data.
        while len(data) < dataset_size:
            data += data

        # use a field of the dictionary
        if data_prop:
            data = [data_row.get(data_prop, data_prop) for data_row in data]

        # randomly sort this column
        data = ITransform.Data.rand_sort(data)

        # if no specified datasize, get the whole lot
        if not dataset_size:
            dataset_size = len(data)

        # abspath the images of dictionary types
        if isinstance(data[0], dict):
            if data[0].get("images", False):
                for row in data:
                    for key in row["images"].keys():
                        row["images"][key] = os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            "liar",
                            row["images"][key],
                        )

        return data[:dataset_size]

    def exact_list(exact, list_size):
        """Returns a list of an exact item * list_size."""
        return [exact for _ in range(0, list_size)]

    def quick_list(choices, list_size):
        """Returns a list selecting randomly from your choices * list_size."""
        return [choice(choices) for _ in range(0, list_size)]

    def toothpaste_list(choices, list_size):
        """Rotates through a list * list_size."""
        return [choices[x % len(choices)] for x in range(0, list_size)]

    def choosy_list(choosy):
        """Returns a list randomly choosing from different column definitions * list_size."""
        return [choice(list(choices.values())) for choices in choosy]

    def field_list(field_name, source_list):
        """Retrieves data from another named field already created - handy to reuse."""
        # does the list contain data?
        if source_list:
            # is it a list?
            if isinstance(source_list, list):
                # does the source list contain dictionaries
                if isinstance(source_list[0], dict):
                    # does the source list contain the requested field?
                    if source_list[0].get(field_name, False):
                        # extract the column for this
                        return [row[field_name] for row in source_list]
        return []
