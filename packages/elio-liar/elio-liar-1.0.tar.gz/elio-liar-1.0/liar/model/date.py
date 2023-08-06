# -*- encoding: utf-8 -*-
"""Ready made column definitions for date data."""

from liar.ijusthelp import rewrite_dict
from liar.model.primitive import date_list
from datetime import timedelta
from datetime import datetime, date

wk = timedelta(weeks=1)
mn = timedelta(weeks=4)
yr = timedelta(weeks=52)
n = datetime.now()

date_time_format = "{:%Y-%m-%d %H:%M:%S}"
date_format = "{:%Y-%m-%d}"

date_of_birth = rewrite_dict(
    date_list,
    {
        "name": "date_of_birth",
        "min": date_format.format(n - (yr * 100)),
        "max": date_format.format(n),
    },
)

date_of_birth_oap = rewrite_dict(
    date_list,
    {
        "name": "date_of_birth_oap",
        "min": date_format.format(n - (yr * 100)),
        "max": date_format.format(n - (yr * 65)),
    },
)

date_of_birth_adult = rewrite_dict(
    date_list,
    {
        "name": "date_of_birth_adult",
        "min": date_format.format(n - (yr * 100)),
        "max": date_format.format(n - (yr * 18)),
    },
)

date_of_birth_parent = rewrite_dict(
    date_list,
    {
        "name": "date_of_birth_parent",
        "min": date_format.format(n - (yr * 60)),
        "max": date_format.format(n - (yr * 24)),
    },
)

date_of_birth_student = rewrite_dict(
    date_list,
    {
        "name": "date_of_birth_student",
        "min": date_format.format(n - (yr * 24)),
        "max": date_format.format(n - (yr * 18)),
    },
)

date_of_birth_teen = rewrite_dict(
    date_list,
    {
        "name": "date_of_birth_teen",
        "min": date_format.format(n - (yr * 18)),
        "max": date_format.format(n - (yr * 13)),
    },
)

date_of_birth_child = rewrite_dict(
    date_list,
    {
        "name": "date_of_birth_child",
        "min": date_format.format(n - (yr * 12)),
        "max": date_format.format(n - (yr * 5)),
    },
)

date_of_birth_toddler = rewrite_dict(
    date_list,
    {
        "name": "date_of_birth_baby",
        "min": date_format.format(n - (yr * 5)),
        "max": date_format.format(n - (yr * 2)),
    },
)

date_of_birth_baby = rewrite_dict(
    date_list,
    {
        "name": "date_of_birth_baby",
        "min": date_format.format(n - (yr * 2)),
        "max": date_format.format(n - wk),
    },
)

department = {
    "name": "department",
    "class": "quicklist",
    "data": [
        "Sales",
        "Accounts",
        "Marketing",
        "Development",
        "Facilities",
        "Transport",
        "HR",
        "Warehouse",
        "Logitics",
    ],
}

day_of_week = {
    "name": "day_of_week",
    "class": "quicklist",
    "data": [date(2000, 1, m).strftime("%A") for m in range(2, 10)],
}

day_of_week_abrev = {
    "name": "day_of_week_abrev",
    "class": "quicklist",
    "data": [date(2000, 1, m).strftime("%a") for m in range(2, 10)],
}

month_of_year = {
    "name": "month_of_year",
    "class": "quicklist",
    "data": [date(2000, m, 1).strftime("%B") for m in range(1, 13)],
}

month_of_year_abrev = {
    "name": "month_of_year_abrev",
    "class": "quicklist",
    "data": [date(2000, m, 1).strftime("%b") for m in range(1, 13)],
}

last_week = rewrite_dict(
    date_list,
    {
        "name": "last_week",
        "min": date_time_format.format(n - wk),
        "max": date_time_format.format(n),
    },
)

last_month = rewrite_dict(
    date_list,
    {
        "name": "last_month",
        "min": date_format.format(n - mn),
        "max": date_format.format(n),
    },
)

last_6_months = rewrite_dict(
    date_list,
    {
        "name": "last_year",
        "min": date_format.format(n - (mn * 6)),
        "max": date_format.format(n),
    },
)

last_year = rewrite_dict(
    date_list,
    {
        "name": "last_year",
        "min": date_format.format(n - yr),
        "max": date_format.format(n),
    },
)

last_2_years = rewrite_dict(
    date_list,
    {
        "name": "last_2_years",
        "min": date_format.format(n - (yr * 2)),
        "max": date_format.format(n),
    },
)

last_decade = rewrite_dict(
    date_list,
    {
        "name": "last_decade",
        "min": date_format.format(n - (yr * 10)),
        "max": date_format.format(n),
    },
)

last_century = rewrite_dict(
    date_list,
    {
        "name": "last_century",
        "min": date_format.format(n - (yr * 130)),
        "max": date_format.format(n),
    },
)

within_days = rewrite_dict(
    date_list,
    {
        "name": "within_days",
        "min": date_time_format.format(n),
        "max": date_time_format.format(n + (wk * 2)),
    },
)

within_weeks = rewrite_dict(
    date_list,
    {
        "name": "within_weeks",
        "min": date_format.format(n),
        "max": date_format.format(n + (wk * 6)),
    },
)

within_months = rewrite_dict(
    date_list,
    {
        "name": "within_months",
        "min": date_format.format(n),
        "max": date_format.format(n + (mn * 6)),
    },
)

within_12_months = rewrite_dict(
    date_list,
    {
        "name": "within_12_months",
        "min": date_format.format(n),
        "max": date_format.format(n + yr),
    },
)

within_years = rewrite_dict(
    date_list,
    {
        "name": "within_years",
        "min": date_format.format(n + (yr * 2)),
        "max": date_format.format(n + (yr * 15)),
    },
)

sci_fi = rewrite_dict(
    date_list,
    {
        "name": "sci_fi",
        "min": date_format.format(n + (yr * 10)),
        "max": date_format.format(n + (yr * 3000)),
    },
)

date_collection = [
    date_of_birth,
    date_of_birth_oap,
    date_of_birth_adult,
    date_of_birth_parent,
    date_of_birth_student,
    date_of_birth_teen,
    date_of_birth_child,
    date_of_birth_toddler,
    date_of_birth_baby,
    department,
    day_of_week,
    day_of_week_abrev,
    month_of_year,
    month_of_year_abrev,
    last_week,
    last_month,
    last_6_months,
    last_year,
    last_2_years,
    last_decade,
    last_century,
    within_days,
    within_weeks,
    within_months,
    within_12_months,
    within_years,
    sci_fi,
]
