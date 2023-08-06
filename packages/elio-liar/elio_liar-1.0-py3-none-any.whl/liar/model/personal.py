# -*- encoding: utf-8 -*-
"""Ready made column definitions for personal details data."""

from liar.ijusthelp import rewrite_dict
from liar.model.raw import surname_raw, person_raw, first_name_raw
from liar.model.location import (
    address1,
    address2,
    locality,
    geo_location,
    post_code,
)
from liar.model.date import (
    date_of_birth_oap,
    date_of_birth_adult,
    date_of_birth_parent,
    date_of_birth_student,
    date_of_birth_teen,
    date_of_birth_child,
    date_of_birth_toddler,
    date_of_birth_baby,
)
from liar.model.primitive import int_list


title = rewrite_dict(person_raw, {"name": "title", "property": "title"})

first_name = first_name_raw

last_name = surname_raw

gender = rewrite_dict(person_raw, {"name": "gender", "property": "gender"})

user_name = {
    "name": "user_name",
    "class": "concat",
    "data": [
        {
            "class": "field",
            "data": "first_name",
            "itransform": ["chomp", "lower"],
        },
        {"class": "field", "data": "last_name", "itransform": ["lower"]},
    ],
}

personal_email_domains = {
    "class": "concat",
    "data": [
        {
            "class": "quicklist",
            "data": ["gmail", "yahoo", "live", "hotmail", "mail"],
        },
        {"class": "quicklist", "data": [".net", ".co.uk", ".com"]},
    ],
}

personal_domain = {
    "name": "personal_domain",
    "class": "choose",
    "data": [
        {
            "class": "concat",
            "data": [
                {
                    "class": "field",
                    "data": "company_name",
                    "itransform": ["lower", "slugify"],
                },
                {
                    "class": "quicklist",
                    "data": [
                        ".net",
                        ".co.uk",
                        ".com",
                        ".org",
                        ".gov",
                        ".gov.uk",
                    ],
                },
            ],
        },
        personal_email_domains,
    ],
}

personal_email = {
    "name": "email",
    "class": "concat",
    "data": [
        {"class": "field", "data": "user_name"},
        {"class": "exact", "data": "@"},
        {"class": "field", "data": "personal_domain"},
    ],
    "itransform": ["lower"],
}

personal_web = {
    "name": "personal_web",
    "class": "concat",
    "itransform": ["lower"],
    "data": [
        {"class": "exact", "data": "http://www."},
        {"class": "field", "data": "personal_domain"},
    ],
}
personal_phone = {
    "name": "personal_phone",
    "class": "concat",
    "data": [
        {"class": "exact", "data": "0"},
        rewrite_dict(int_list, {"min": 1100, "max": 1999}),
        {"class": "exact", "data": " "},
        rewrite_dict(int_list, {"min": 100000, "max": 999999}),
    ],
}

personal_mobile = {
    "name": "personal_mobile",
    "class": "concat",
    "data": [
        {"class": "exact", "data": "0"},
        rewrite_dict(int_list, {"min": 7100, "max": 9999}),
        {"class": "exact", "data": " "},
        rewrite_dict(int_list, {"min": 100000, "max": 999999}),
    ],
}


skin_tone = {
    "name": "skin_tones",
    "class": "quicklist",
    "data": [
        "#FFDFC4",
        "#F0D5BE",
        "#EECEB3",
        "#E1B899",
        "#E5C298",
        "#FFDCB2",
        "#E5B887",
        "#E5A073",
        "#E79E6D",
        "#DB9065",
        "#CE967C",
        "#C67856",
        "#BA6C49",
        "#A57257",
        "#F0C8C9",
        "#DDA8A0",
        "#B97C6D",
        "#A8756C",
        "#AD6452",
        "#5C3836",
        "#CB8442",
        "#BD723C",
        "#704139",
        "#A3866A",
        "#870400",
        "#710101",
        "#430000",
        "#5B0001",
        "#302E2E",
        "#000000",
    ],
}

hair_color = {
    "name": "hair_color",
    "class": "quicklist",
    "data": [
        "#090806",
        "#2C222B",
        "#3B3024",
        "#4E433F",
        "#504444",
        "#533D32",
        "#554838",
        "#6A4E42",
        "#71635A",
        "#8D4A43",
        "#91553D",
        "#977961",
        "#A56B46",
        "#A7856A",
        "#B55239",
        "#B7A69E",
        "#B89778",
        "#CABFB1",
        "#D6C4C2",
        "#DCD0BA",
        "#DEBC99",
        "#E5C8A8",
        "#E6CEA8",
        "#FFF5E1",
    ],
}

accessory_color = {
    "name": "accessory_color",
    "class": "quicklist",
    "data": [
        "#FFB6C1",
        "#FFC0CB",
        "#DC143C",
        "#DB7093",
        "#FF69B4",
        "#FF1493",
        "#C71585",
        "#DA70D6",
        "#D8BFD8",
        "#DDA0DD",
        "#EE82EE",
        "#FF00FF",
        "#FF00FF",
        "#8B008B",
        "#800080",
        "#BA55D3",
        "#9400D3",
        "#9932CC",
        "#4B0082",
        "#8A2BE2",
        "#9370DB",
        "#7B68EE",
        "#6A5ACD",
        "#483D8B",
        "#E6E6FA",
        "#0000FF",
        "#0000CD",
        "#191970",
        "#00008B",
        "#000080",
        "#4169E1",
        "#6495ED",
        "#B0C4DE",
        "#778899",
        "#708090",
        "#1E90FF",
        "#4682B4",
        "#87CEFA",
        "#87CEEB",
        "#00BFFF",
        "#ADD8E6",
        "#B0E0E6",
        "#5F9EA0",
        "#AFEEEE",
        "#00FFFF",
        "#00FFFF",
        "#00CED1",
        "#2F4F4F",
        "#008B8B",
        "#008080",
        "#48D1CC",
        "#20B2AA",
        "#40E0D0",
        "#7FFFD4",
        "#66CDAA",
        "#00FA9A",
        "#00FF7F",
        "#3CB371",
        "#2E8B57",
        "#90EE90",
        "#98FB98",
        "#8FBC8F",
        "#32CD32",
        "#00FF00",
        "#228B22",
        "#008000",
        "#006400",
        "#7FFF00",
        "#7CFC00",
        "#ADFF2F",
        "#556B2F",
        "#9ACD32",
        "#6B8E23",
        "#F5F5DC",
        "#FAFAD2",
        "#808000",
        "#BDB76B",
        "#FFFACD",
        "#EEE8AA",
        "#F0E68C",
        "#FFD700",
        "#FFF8DC",
        "#DAA520",
        "#B8860B",
        "#FDF5E6",
        "#F5DEB3",
        "#FFE4B5",
        "#FFA500",
        "#FFEFD5",
        "#FFEBCD",
        "#FFDEAD",
        "#FAEBD7",
        "#D2B48C",
        "#DEB887",
        "#FFE4C4",
        "#FF8C00",
        "#FAF0E6",
        "#CD853F",
        "#FFDAB9",
        "#F4A460",
        "#D2691E",
        "#8B4513",
        "#A0522D",
        "#FFA07A",
        "#FF7F50",
        "#FF4500",
        "#E9967A",
        "#FF6347",
    ],
}


home_address1 = rewrite_dict(address1, {"name": "home_address1"})
home_address2 = rewrite_dict(address2, {"name": "home_address2"})
home_locality = rewrite_dict(locality, {"name": "home_locality"})
home_geo_location = rewrite_dict(geo_location, {"name": "home_geo_location"})
home_post_code = rewrite_dict(post_code, {"name": "home_post_code"})

personal_model = [
    title,
    first_name,
    last_name,
    gender,
    user_name,
    home_address1,
    home_address2,
    home_locality,
    home_geo_location,
    home_post_code,
    personal_domain,
    personal_email,
    personal_web,
    personal_phone,
    personal_mobile,
    skin_tone,
    hair_color,
    accessory_color,
]

oap_model = personal_model + [date_of_birth_oap]
adult_model = personal_model + [date_of_birth_adult]
parent_model = personal_model + [date_of_birth_parent]
student_model = personal_model + [date_of_birth_student]
teen_model = personal_model + [date_of_birth_teen]
child_model = personal_model + [date_of_birth_child]
toddler_model = personal_model + [date_of_birth_toddler]
baby_model = personal_model + [date_of_birth_baby]

from liar.model.business import (
    employee_number,
    company_name,
    department,
    job_title,
)

employee_model = adult_model + [
    employee_number,
    company_name,
    department,
    job_title,
]
