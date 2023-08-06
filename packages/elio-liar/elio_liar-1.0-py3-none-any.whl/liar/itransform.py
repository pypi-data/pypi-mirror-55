# -*- encoding: utf-8 -*-
"""
TODO: add a sorting transform"""
import json
from random import randint
from slugify import slugify
from liar.ijusthelp import rewrite_dict
from liar.iamprimitive import IAmPrimitive


class ITransform(object):
    """ITransform operates on full datasets or fields."""

    class Data(object):
        """Data has transform methods to operate on columns."""

        def transform(column, transformations):
            """"Returns the transformed data.

            :param column:              The column of data to transform.
            :param transformations:     List of method names from below.

            The order of transformations is worth considering!"""

            for method_name in transformations:
                transformer = getattr(ITransform.Fields, method_name)
                column = [transformer(val) for val in column]

            return column

        def splutterer(column, splutter):
            """Randomly erase splutter percent of the data."""
            return [ITransform.Fields.splutter(val, splutter) for val in column]

        def zip_column(column, new_column, field_name):
            """Data is created one entire column at a time - rather than row by row.
            Every new column of data is zipped into the main recordset."""
            # zip the new column up with the existing columns
            x = 0
            for new_field_data in new_column:
                column[x][field_name] = new_field_data
                x += 1
            return column

        def concat_column(column, new_column):
            """As data is created one column at a time, you might like to concatonate
            # the values to make a single column."""
            # zip the new column up with the existing columns
            x = 0
            for new_field_data in new_column:
                current_field_data = column[x] if column[x] else ""
                column[x] = f"{current_field_data}{new_field_data}"
                x += 1
            return column

        def fix_raw_json(raw):
            """Fiw json data read from a file."""
            return json.loads(json.dumps(eval(raw)))

        def convert_2_simple_list(dictionary_list, field_name):
            """Convert a dictionary list to a word list."""
            return [xdict[field_name] for xdict in dictionary_list]

        def rand_sort(data):
            """Sort a list randomly: shuffle it!"""
            # create a list of random numbers the same dataset size
            rand_list = IAmPrimitive.Lists.dec_list(0, 100, len(data))
            # zip them
            sort_list = list(zip(rand_list, data))
            # sort them - thus randomizing the order
            sort_list.sort(key=lambda tup: tup[0])
            # remove the sorter
            return [tup[1] for tup in sort_list]

        def remove_column(data_set, column):
            for row in data_set:
                row.pop(column)
            return data_set

    class Fields(object):
        """Fields methods operate on single fields."""

        def upper(val):
            """I AM UPPER"""
            return str(val).upper()

        def lower(val):
            """i am lower"""

            return str(val).lower()

        def title(val):
            """I Am A Title"""

            return str(val).title()

        def chomp(val):
            """[c]homps the first letter"""

            return str(val)[0]

        def capitalize(val):
            """I am capitilized."""

            return str(val).capitalize()

        def slugify(val):
            """i-am-slugified"""

            return slugify(str(val))

        def splutter(val, splutter):
            """I have a splutter% chance of being erased."""

            return val if randint(1, 100) > splutter else ""
