"""IAmALiar is where the magic happens.

Using a list of json "column definitions" this class builds one column at a
time, zipping them into a full data set.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

Build from ready-made column definitions:

::

    from liar.ijusthelp import rewrite_dict
    from liar.model.marketing import product_title, postage_cost
    from liar.model.date import within_days

    # using an existing definition, but giving it a new name
    delivery_date = rewrite_dict(within_days,
                                {'name': 'delivery_date'}
                            )

    data_set = maker.get_data([product_title, postage_cost, delivery_date])

    for row in data_set:
        liar.product_title = row['product_title']
        liar.postage_cost = row['postage_cost']
        liar.delivery_date = row['delivery_date']


Build from large, but ready-made model definitions:

::

    from liar.model.personal import employee_model
    data_set = maker.get_data(employee_model)

    for row in data_set:
        liar.employee.first_name = row['first_name']
        liar.employee.last_name = row['last_name']
        liar.employee.employee_number = row['employee_number']

"""
# -*- encoding: utf-8 -*-
from liar.igetraw import IGetRaw
from liar.iamprimitive import IAmPrimitive
from liar.iblurb import IBlurb
from liar.itransform import ITransform

# TODO: from liar.ipictureit import IPictureIt


class IAmALiar(object):
    """Call an instance of IAmALiar to create random data sets."""

    def __init__(self, dataset_size):
        """Intialise the class with a dataset size."""
        self.dataset_size = dataset_size

    def get_data(self, data_definition):
        """Get a recordset of random data matching the definition.

        :param data_definition: The entire data definition.
        """
        if not isinstance(data_definition, list):
            raise Exception(
                """
                            Your data_definition must be a list of
                            dictionaries, not a single (dict) defintion.
                            """
            )

        if not isinstance(data_definition[0], dict):
            raise Exception("Each data_definition must be a dictionary.")

        # Get all records
        record_list = self.get_records(data_definition, None, {})

        # Finally, remove any columns which were temporary
        for column_definition in data_definition:
            if column_definition.get("remove", False):
                field_name = column_definition.get("name", "")
                record_list = ITransform.Data.remove_column(
                    record_list, field_name
                )

        return record_list

    def get_records(self, data_definition, parent_list, parent_def):
        """Get rows of records based on a definition of columns.

        As individual column in the definition are also built by combining
        fields, this method is called recursively.

        :param data_definition: The entire data definition.

        :param parent_list:  The entire data which we have built so far.

        Columns are added and zipped one column at a time.

        :param parent_def: The root column definition follows the sub
        definitions around.
        """
        # create an empty column
        loc_record_list = [{} for x in range(1, self.dataset_size + 1)]

        # make the first one the primary object. We use this to find
        # fields which can be referenced by other fields.
        if not parent_list:
            parent_list = loc_record_list

        col_count = 1
        parent_field = parent_def.get("name", "field")
        parent_class = parent_def.get("class", False)

        # for each column required in the definition
        for column_definition in data_definition:
            # what field name is required by the user
            field_name = column_definition.get(
                "name", f"{parent_field}{col_count}"
            )
            # where will we get this data?
            data_class = column_definition.get("class", False)
            # what data do we want?
            data_def = column_definition.get("data", False)

            # does the column request data from another field in the dataset?
            if data_class == "field":
                column = IGetRaw.field_list(data_def, parent_list)
            else:
                # get the column of data defined
                column = self.get_column(column_definition, parent_list)

            # What do we do with this new column?
            if column:
                # what transformations do we want?
                transformations = column_definition.get("itransform", [])
                if transformations:
                    column = ITransform.Data.transform(column, transformations)
                # what calculations do we want?
                calculations = column_definition.get("calc", [])
                if calculations:
                    column = IAmPrimitive.Lists.calculate(column, calculations)
                # splutter results with blanks?
                splutter = column_definition.get("splutter", 0)
                if splutter:
                    column = ITransform.Data.splutterer(column, splutter)
                # flatten breaks JSON column into many columns.
                flatten = column_definition.get("flatten", False)
                if flatten:
                    # check we can flatten this column
                    test_row = column[0]
                    if isinstance(test_row, dict):
                        for subfield in test_row.keys():
                            loc_record_list = ITransform.Data.zip_column(
                                loc_record_list,
                                [f[subfield] for f in column],
                                f"{field_name}_{subfield}",
                            )
                            col_count += 1
                    else:
                        loc_record_list = ITransform.Data.zip_column(
                            loc_record_list, column, field_name
                        )
                        col_count += 1
                else:
                    # Two columns become one
                    if parent_class == "concat":
                        loc_record_list = ITransform.Data.concat_column(
                            loc_record_list, column
                        )
                    # Two columns are zipped up against eachother into a recordset
                    else:
                        loc_record_list = ITransform.Data.zip_column(
                            loc_record_list, column, field_name
                        )
                    col_count += 1

        return loc_record_list

    def get_column(self, column_definition, parent_list):
        """Build and return a column of data.

        :param column_definition: A column definition from the root list.

        :param parent_list: The column of data which we have built so far.

        Columns are added and zipped one column at a time.
        """
        # get the column defintion
        data_class = column_definition.get("class", "")
        data_def = column_definition.get("data", "")
        data_method = column_definition.get("method", "")
        data_filters = column_definition.get("filters", {})

        # start with a empty column
        column = []

        if data_class == "igetraw":
            # comes from json object
            data_prop = column_definition.get("property", "")
            column = IGetRaw.raw_list(
                data_def, data_prop, self.dataset_size, data_filters
            )

        elif data_class == "iamprimitive":
            # comes from primitive class
            raw_call = getattr(IAmPrimitive.Lists, data_method)
            min = column_definition.get("min", 1)
            max = column_definition.get("max", 2)
            column = raw_call(min, max, self.dataset_size)

        elif data_class == "pk":
            # create a primary key / counter value. Starts at 1
            column = IAmPrimitive.Lists.primary_key_list(
                0, 0, self.dataset_size
            )

        elif data_class == "iblurb":
            # comes from the IBlurb class
            language = column_definition.get("language", "English")
            min = column_definition.get("min", 1)
            max = column_definition.get("max", 2)
            # get a big word list
            dictionary_list = IGetRaw.raw_list(language, "")
            blb = IBlurb(dictionary_list, min, max)
            column = blb.blurb_column(data_method, self.dataset_size)

        elif data_class == "quicklist":
            # user quick list
            column = IGetRaw.quick_list(data_def, self.dataset_size)

        elif data_class == "toothpaste":
            # user list in rotation
            column = IGetRaw.toothpaste_list(data_def, self.dataset_size)

        elif data_class == "exact":
            # user provided static data
            column = IGetRaw.exact_list(data_def, self.dataset_size)

        elif data_class == "concat":
            # a whole sub-definition in itself - but to concat the columns
            # into one field. Concat is handled by the get_records method
            column = self.get_records(data_def, parent_list, column_definition)

        elif data_class == "choose":
            # a whole sub-definition in itself - but to choose one field per
            # record of the columns created.
            column = self.get_records(data_def, parent_list, column_definition)
            column = IGetRaw.choosy_list(column)

        elif data_class == "field":
            # Use the data which has already been created by another field.
            # This class is handled in calling method - where all the columns
            # can be checked - but I added the case here for clarity.
            pass

        return column
