# -*- encoding: utf-8 -*-
"""Ready made column definitions for products and marketing data."""

from liar.ijusthelp import rewrite_dict
from liar.model.raw import product_name_raw
from liar.model.primitive import dec_list
from liar.model.blurb import (
    blurb,
    ainu_blurb,
    danish_blurb,
    english_blurb,
    latin_blurb,
)

product_weight = rewrite_dict(
    dec_list, {"name": "product_weight", "min": 0.3, "max": 20}
)

postage_cost = {
    "name": "postage_cost",
    "class": "field",
    "data": "product_weight",
    "calc": [{"multiply": 10}, {"divide": 2}, {"add": 0.99}],
}

product_title = rewrite_dict(
    english_blurb,
    {"name": "product_title", "method": "plaintext_title", "min": 2, "max": 7},
)

product_name = product_name_raw

news_title = rewrite_dict(
    ainu_blurb,
    {"name": "news_title", "method": "plaintext_title", "min": 5, "max": 15},
)

tweet = rewrite_dict(
    english_blurb,
    {"name": "tweet", "method": "plaintext_sentences", "min": 6, "max": 15},
)

description = rewrite_dict(
    english_blurb,
    {"name": "description", "method": "html_paragraph", "min": 20, "max": 40},
)

short_blurb = rewrite_dict(
    ainu_blurb,
    {
        "name": "short_blurb",
        "method": "html_paragraphs",
        "min": 100,
        "max": 150,
    },
)

long_blurb = rewrite_dict(
    ainu_blurb,
    {
        "name": "long_blurb",
        "method": "html_paragraphs",
        "min": 1000,
        "max": 2000,
    },
)

essay = rewrite_dict(
    ainu_blurb,
    {"name": "essay", "method": "html_paragraphs", "min": 3000, "max": 8000},
)

foreign_chars = rewrite_dict(
    danish_blurb,
    {
        "name": "foreign_chars",
        "method": "plaintext_sentences",
        "min": 100,
        "max": 200,
    },
)

marketing_model = [
    postage_cost,
    product_weight,
    news_title,
    product_title,
    product_name,
    tweet,
    description,
    short_blurb,
    long_blurb,
    essay,
    foreign_chars,
]

product_model = [product_name, short_blurb, tweet, product_weight, postage_cost]
