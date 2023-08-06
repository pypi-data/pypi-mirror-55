# -*- encoding: utf-8 -*-
""""""
from datetime import datetime, timedelta
from dateutil.parser import parse
from random import randint, uniform
from liar.ijusthelp import rewrite_dict


class IAmPrimitive(object):
    """Makes lists of primitive values like ints, floats, dates, and times."""

    class Lists(object):
        """Compile randomly generated primitives into a list.

        :param min:         the smallest number you'll allow in your list
        :param max:         the largest number you'll allow in your list
        :param start_date:  the oldest date you'll allow in your list
        :param end_date:    the furthest date you'll allow in your list
        :param list_size:   the size of your list

        """

        def dec_list(min, max, list_size=0):
            """Returns a list of floating point numbers * list_size within the bounds specified."""

            return [
                IAmPrimitive.Values.get_dec(min, max)
                for _ in range(0, list_size)
            ]

        def int_list(min, max, list_size=0):
            """Returns a list of whole numbers * list_size within the bounds specified."""

            return [
                IAmPrimitive.Values.get_int(min, max)
                for _ in range(0, list_size)
            ]

        def datetimes_list(start_date, end_date, list_size=0):
            """Returns a list of datetimes * list_size within the bounds specified."""

            start_date = parse(start_date)
            end_date = parse(end_date)
            second_diff = int((end_date - start_date).total_seconds())
            return [
                start_date + timedelta(seconds=randint(0, second_diff))
                for _ in range(0, list_size)
            ]

        def time_list(start_date, end_date, list_size=0):
            """Returns a list of times * list_size within the bounds specified."""

            return [
                str(time.time())
                for time in IAmPrimitive.Lists.datetimes_list(
                    start_date, end_date, list_size
                )
            ]

        def date_list(start_date, end_date, list_size=0):
            """Returns a list of dates * list_size within the bounds specified."""

            return [
                str(time.date())
                for time in IAmPrimitive.Lists.datetimes_list(
                    start_date, end_date, list_size
                )
            ]

        def primary_key_list(min, max, list_size):
            """Returns a list of primary keys * list_size."""

            return list(range(1, list_size + 1))

        def calculate(val_list, calculations):
            """Performs a calculation on a each primitive item in the list."""

            for calc in calculations:
                method_name, val_adjust = calc.popitem()
                calculator = getattr(IAmPrimitive.Calc, method_name)
                val_list = calculator(val_list, val_adjust)
            return val_list

    class Calc(object):
        """
        Calc performs calculations of each primitive in the list.

        :param val_list:     a list of primitive values
        :param val_adjust:   the largest number you'll allow

        """

        def add(val_list, val_adjust):
            """"""
            return [val + val_adjust for val in val_list]

        def subtract(val_list, val_adjust):
            """"""
            return [val - val_adjust for val in val_list]

        def multiply(val_list, val_adjust):
            """"""
            return [val * val_adjust for val in val_list]

        def divide(val_list, val_adjust):
            """"""
            return [val / val_adjust for val in val_list]

        def format(val_list, val_adjust):
            """"""
            return [val_adjust.format(val) for val in val_list]

    class Values(object):
        """
        Values methods to return random integer or float.

        :param min:         the smallest number you'll allow
        :param max:         the largest number you'll allow

        """

        def get_int(min, max):
            """Returns an integer within the bounds specified."""

            return randint(min, max)

        def get_dec(min, max):
            """Returns an float within the bounds specified."""

            return uniform(min, max)
