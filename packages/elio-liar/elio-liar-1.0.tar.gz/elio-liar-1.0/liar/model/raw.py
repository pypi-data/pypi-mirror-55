# -*- encoding: utf-8 -*-
"""Ready made column definitions for raw data."""

from liar.ijusthelp import rewrite_dict
import string

raw = {"name": "raw", "class": "igetraw", "data": "raw"}

academic_raw = rewrite_dict(raw, {"name": "academic_raw", "data": "academic"})

ainu_raw = rewrite_dict(raw, {"name": "ainu_raw", "data": "ainu"})

animal_raw = rewrite_dict(raw, {"name": "animal_raw", "data": "animal"})

animal_name_raw = rewrite_dict(
    animal_raw, {"name": "animal_name_raw", "property": "animal"}
)

animal_prefix_raw = rewrite_dict(
    raw, {"name": "animal_prefix_raw", "data": "animal_prefix"}
)

animal_suffix_raw = rewrite_dict(
    raw, {"name": "animal_suffix_raw", "data": "animal_suffix"}
)

business_type_raw = rewrite_dict(
    raw, {"name": "business_type_raw", "data": "business_type"}
)

car_raw = rewrite_dict(raw, {"name": "car_raw", "data": "car"})

char_raw = rewrite_dict(raw, {"name": "char_raw", "data": "char"})

ascii_letter_raw = rewrite_dict(
    raw,
    {
        "name": "ascii_letter_raw",
        "class": "quicklist",
        "data": list(string.ascii_letters),
    },
)
ascii_lowercase_raw = rewrite_dict(
    raw,
    {
        "name": "ascii_lowercase_raw",
        "class": "quicklist",
        "data": list(string.ascii_lowercase),
    },
)
ascii_uppercase_raw = rewrite_dict(
    raw,
    {
        "name": "ascii_uppercase_raw",
        "class": "quicklist",
        "data": list(string.ascii_uppercase),
    },
)
digit_raw = rewrite_dict(
    raw,
    {"name": "digit_raw", "class": "quicklist", "data": list(string.digits)},
)
hexdigit_raw = rewrite_dict(
    raw,
    {
        "name": "hexdigit_raw",
        "class": "quicklist",
        "data": list(string.hexdigits),
    },
)
octdigit_raw = rewrite_dict(
    raw,
    {
        "name": "octdigit_raw",
        "class": "quicklist",
        "data": list(string.octdigits),
    },
)
printable_raw = rewrite_dict(
    raw,
    {
        "name": "printable_raw",
        "class": "quicklist",
        "data": list(string.printable),
    },
)
punctuation_raw = rewrite_dict(
    raw,
    {
        "name": "punctuation_raw",
        "class": "quicklist",
        "data": list(string.punctuation),
    },
)
whitespace_raw = rewrite_dict(
    raw,
    {
        "name": "whitespace_raw",
        "class": "quicklist",
        "data": list(string.whitespace),
    },
)

danish_raw = rewrite_dict(raw, {"name": "danish_raw", "data": "danish"})

district_suffix_raw = rewrite_dict(
    raw, {"name": "district_suffix_raw", "data": "district_suffix"}
)

english_raw = rewrite_dict(raw, {"name": "english_raw", "data": "english"})

english_word_raw = rewrite_dict(
    english_raw, {"name": "english_word_raw", "property": "word"}
)

geo_location_raw = rewrite_dict(
    raw, {"name": "geo_location_raw", "data": "geo_location"}
)

job_title_raw = rewrite_dict(
    raw, {"name": "job_title_raw", "data": "job_title"}
)

latin_raw = rewrite_dict(raw, {"name": "latin_raw", "data": "latin"})

person_raw = rewrite_dict(raw, {"name": "person_raw", "data": "person"})

first_name_raw = rewrite_dict(
    person_raw, {"name": "first_name_raw", "property": "first_name"}
)

product_raw = rewrite_dict(raw, {"name": "product_raw", "data": "product"})

product_name_raw = rewrite_dict(
    product_raw, {"name": "product_name_raw", "property": "product"}
)

street_type_raw = rewrite_dict(
    raw, {"name": "street_type_raw", "data": "street_type"}
)

surname_raw = rewrite_dict(raw, {"name": "surname_raw", "data": "surname"})


transport_raw = rewrite_dict(raw, {"name": "academic_raw", "data": "transport"})

word_prefix_raw = rewrite_dict(
    raw, {"name": "word_prefix_raw", "data": "word_prefix"}
)

word_suffix_raw = rewrite_dict(
    raw, {"name": "word_suffix_raw", "data": "word_suffix"}
)

raw_collection = [
    academic_raw,
    ainu_raw,
    animal_raw,
    animal_name_raw,
    animal_prefix_raw,
    animal_suffix_raw,
    business_type_raw,
    car_raw,
    char_raw,
    ascii_letter_raw,
    ascii_lowercase_raw,
    ascii_uppercase_raw,
    digit_raw,
    hexdigit_raw,
    octdigit_raw,
    printable_raw,
    punctuation_raw,
    whitespace_raw,
    danish_raw,
    district_suffix_raw,
    english_raw,
    first_name_raw,
    geo_location_raw,
    job_title_raw,
    latin_raw,
    person_raw,
    first_name_raw,
    product_raw,
    product_name_raw,
    street_type_raw,
    surname_raw,
    transport_raw,
    word_prefix_raw,
    word_suffix_raw,
]
