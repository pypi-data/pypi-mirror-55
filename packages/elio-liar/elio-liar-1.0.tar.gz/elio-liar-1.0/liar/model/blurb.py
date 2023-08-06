# -*- encoding: utf-8 -*-
"""Ready made column definitions for blurb data."""

from liar.ijusthelp import rewrite_dict

blurb = {
    "name": "blurb",
    "class": "iblurb",
    "method": "html_paragraphs",
    "min": 500,
    "max": 1000,
    "language": "ainu",
}

ainu_blurb = rewrite_dict(blurb, {"name": "ainu_blurb", "language": "ainu"})

danish_blurb = rewrite_dict(blurb, {"name": "ainu_blurb", "language": "danish"})

english_blurb = rewrite_dict(
    blurb, {"name": "ainu_blurb", "language": "english"}
)

latin_blurb = rewrite_dict(blurb, {"name": "ainu_blurb", "language": "latin"})

ainu_title = rewrite_dict(
    ainu_blurb, {"method": "plaintext_title", "min": 3, "max": 5}
)

danish_title = rewrite_dict(
    danish_blurb, {"method": "plaintext_title", "min": 5, "max": 8}
)

english_title = rewrite_dict(
    english_blurb,
    {"name": "english_title", "method": "html_bullets", "min": 7, "max": 10},
)

latin_title = rewrite_dict(
    latin_blurb,
    {"name": "latin_title", "method": "plaintext_title", "min": 5, "max": 5},
)

latin_motto = rewrite_dict(
    latin_blurb,
    {"name": "latin_motto", "method": "plaintext_title", "min": 2, "max": 10},
)

blurb_collection = [
    blurb,
    ainu_blurb,
    danish_blurb,
    english_blurb,
    latin_blurb,
    ainu_title,
    danish_title,
    english_title,
    latin_title,
    latin_motto,
]
