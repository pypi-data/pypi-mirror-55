# -*- encoding: utf-8 -*-
"""
A single character.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

    # Use:
    from liar.model.raw import char_raw

    # Or from scratch:
    char_raw = {
        'name': 'char_raw',
        'class': 'igetraw',
        'data': 'char',
    }

    data_set = maker.get_data([char_raw])

    for row in data_set:
        data = Model()
        data.ascii = row['char_raw']['ascii']
        data.lower = row['char_raw']['lower']
        data.upper = row['char_raw']['upper']
        data.digits = row['char_raw']['digit']
        data.hexdigits = row['char_raw']['hexdigit']
        data.octdigits = row['char_raw']['octdigit']
        data.printable = row['char_raw']['printable']
        data.punctuation = row['char_raw']['punctuation']
        data.whitespace = row['char_raw']['whitespace']
        data.save()

The char data is compiled from these raw data sets:

::

    ascii_letter_raw = {'name': 'char_raw', 'data': 'ascii_letter'}
    ascii_lowercase_raw = {'name': 'ascii_lowercase_raw', 'data': 'ascii_lowercase'}
    ascii_uppercase_raw = {'name': 'ascii_uppercase_raw', 'data': 'ascii_uppercase'}
    digit_raw = {'name': 'digit_raw', 'data': 'digit'}
    hexdigit_raw = {'name': 'hexdigit_raw', 'data': 'hexdigit'}
    octdigit_raw = {'name': 'octdigit_raw', 'data': 'octdigit'}
    printable_raw = {'name': 'printable_raw', 'data': 'printable'}
    punctuation_raw = {'name': 'punctuation_raw', 'data': 'punctuation'}
    whitespace_raw = {'name': 'whitespace_raw', 'data': 'whitespace'}

"""
import string

ascii_letter = list(string.ascii_letters)
ascii_lowercase = list(string.ascii_lowercase)
ascii_uppercase = list(string.ascii_uppercase)
digit = list(string.digits)
hexdigit = list(string.hexdigits)
octdigit = list(string.octdigits)
printable = list(string.printable)
punctuation = list(string.punctuation)
whitespace = list(string.whitespace)

char = (
    [{"classification": "ascii", "char": r} for r in ascii_letter]
    + [{"classification": "lower", "char": r} for r in ascii_lowercase]
    + [{"classification": "upper", "char": r} for r in ascii_uppercase]
    + [{"classification": "digit", "char": r} for r in digit]
    + [{"classification": "hexdigit", "char": r} for r in hexdigit]
    + [{"classification": "octdigit", "char": r} for r in octdigit]
    + [{"classification": "printable", "char": r} for r in printable]
    + [{"classification": "punctuation", "char": r} for r in punctuation]
    + [{"classification": "whitespace", "char": r} for r in whitespace]
)
