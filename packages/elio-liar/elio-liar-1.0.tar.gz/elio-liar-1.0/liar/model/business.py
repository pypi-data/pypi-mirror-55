# -*- encoding: utf-8 -*-
"""Ready made column definitions for business data."""

from liar.ijusthelp import rewrite_dict
from liar.model.blurb import latin_blurb
from liar.model.location import (
    address1,
    address2,
    locality,
    geo_location,
    post_code,
)
from liar.model.raw import raw, job_title_raw
from liar.model.primitive import int_list

employee_number = {
    "name": "employee_number",
    "class": "pk",
    "calc": [{"add": 10000}],
}

company_name = {
    "name": "company_name",
    "class": "concat",
    "data": [
        rewrite_dict(
            latin_blurb,
            {
                "method": "plaintext_title",
                "min": 1,
                "max": 2,
                "itransform": ["title"],
            },
        ),
        {"class": "exact", "data": " "},
        rewrite_dict(raw, {"data": "business_type", "splutter": 10}),
    ],
}

department = {
    "name": "department",
    "class": "quicklist",
    "data": ["Sales", "Accounts", "Marketing", "Development", "Facilities"],
}

job_title = job_title_raw

company_slug = {
    "name": "company_slug",
    "class": "field",
    "data": "company_name",
    "itransform": ["lower", "slugify"],
}

company_domain = {
    "name": "company_domain",
    "class": "concat",
    "data": [
        company_slug,
        {
            "class": "quicklist",
            "data": [".net", ".co.uk", ".com", ".org", ".gov", ".gov.uk"],
        },
    ],
}

company_email = {
    "name": "company_email",
    "class": "concat",
    "itransform": ["lower"],
    "data": [
        {"class": "quicklist", "data": ["info", "contact", "web", "sales"]},
        {"class": "exact", "data": "@"},
        {"class": "field", "data": "company_domain"},
    ],
}

info_email = {
    "name": "info_email",
    "class": "concat",
    "itransform": ["lower"],
    "data": [
        {"class": "exact", "data": "info@"},
        {"class": "field", "data": "company_domain"},
    ],
}

contact_email = {
    "name": "contact_email",
    "class": "concat",
    "itransform": ["lower"],
    "data": [
        {"class": "exact", "data": "contact@"},
        {"class": "field", "data": "company_domain"},
    ],
}

web_email = {
    "name": "web_email",
    "class": "concat",
    "itransform": ["lower"],
    "data": [
        {"class": "exact", "data": "web@"},
        {"class": "field", "data": "company_domain"},
    ],
}

sales_email = {
    "name": "sales_email",
    "class": "concat",
    "itransform": ["lower"],
    "data": [
        {"class": "exact", "data": "sales@"},
        {"class": "field", "data": "company_domain"},
    ],
}

company_web = {
    "name": "company_web",
    "class": "concat",
    "itransform": ["lower"],
    "data": [
        {"class": "exact", "data": "https://www."},
        {"class": "field", "data": "company_domain"},
    ],
}

company_phone = {
    "name": "company_phone",
    "class": "concat",
    "data": [
        {"class": "exact", "data": "0"},
        rewrite_dict(int_list, {"min": 1100, "max": 1999}),
        {"class": "exact", "data": " "},
        rewrite_dict(int_list, {"min": 100000, "max": 999999}),
    ],
}

company_fax = {
    "name": "company_fax",
    "class": "concat",
    "data": [
        {"class": "exact", "data": "0"},
        rewrite_dict(int_list, {"min": 1188, "max": 1988}),
        {"class": "exact", "data": " "},
        rewrite_dict(int_list, {"min": 100000, "max": 999999}),
    ],
}


company_address1 = rewrite_dict(address1, {"name": "company_address1"})
company_address2 = rewrite_dict(address2, {"name": "company_address2"})
company_locality = rewrite_dict(locality, {"name": "company_locality"})
company_geo_location = rewrite_dict(
    geo_location, {"name": "company_geo_location"}
)
company_post_code = rewrite_dict(post_code, {"name": "company_post_code"})

business_model = [
    employee_number,
    company_name,
    company_address1,
    company_address2,
    company_locality,
    company_geo_location,
    company_post_code,
    department,
    job_title,
    company_slug,
    company_domain,
    company_email,
    info_email,
    contact_email,
    sales_email,
    web_email,
    company_web,
    company_phone,
    company_fax,
]
