# -*- encoding: utf-8 -*-
"""Ready made column definitions for time data."""

from liar.ijusthelp import rewrite_dict
from liar.model.primitive import time_list

from datetime import timedelta
from datetime import datetime

mn = timedelta(minutes=1)
hr = timedelta(hours=1)
n = datetime.now()

time_short_format = "{:%H:%M:%S}"

last_minute = rewrite_dict(
    time_list,
    {"name": "last_minute", "min": "00:00:00.0", "max": "00:00:59.99"},
)

within_minutes = rewrite_dict(
    time_list,
    {"name": "within_minutes", "min": "23:45:00.0", "max": "23:59:59.99"},
)

last_hour = rewrite_dict(
    time_list, {"name": "last_hour", "min": "00:00:00.0", "max": "00:59:59.99"}
)

within_hours = rewrite_dict(
    time_list,
    {"name": "within_hours", "min": "08:00:00.0", "max": "17:59:59.99"},
)

opening_hours = rewrite_dict(
    time_list,
    {
        "name": "opening_hours",
        "min": time_short_format.format(
            datetime(n.year, n.month, n.day, 8, 0, 0)
        ),
        "max": time_short_format.format(
            datetime(n.year, n.month, n.day, 18, 30, 0)
        ),
    },
)

last_24 = rewrite_dict(
    time_list, {"name": "last_24", "min": "00:00:00.0", "max": "23:59:59.99"}
)

time_collection = [
    last_minute,
    last_hour,
    within_minutes,
    within_hours,
    opening_hours,
    last_24,
]
