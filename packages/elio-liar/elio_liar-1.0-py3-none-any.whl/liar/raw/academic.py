# -*- encoding: utf-8 -*-
"""
Contains a list of Academic study areas.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

    # Use:
    from liar.model.raw import academic_raw

    # Or from scratch:
    academic_raw = {
        'name': 'academic_raw',
        'class': 'igetraw',
        'data': 'academic',
    }

    data_set = maker.get_data([academic_raw])

    for row in data_set:
        data = Model()
        data.subject = row['academic_raw']['subject']
        data.department = row['academic_raw']['department']
        data.save()

"""

academic = [
    {"subject": "Art", "department": "Arts"},
    {"subject": "Art History", "department": "Arts"},
    {"subject": "Drama", "department": "Arts"},
    {"subject": "Classics", "department": "Arts"},
    {"subject": "English", "department": "Arts"},
    {"subject": "Geography", "department": "Arts"},
    {"subject": "History", "department": "Arts"},
    {"subject": "Modern Languages", "department": "Arts"},
    {"subject": "Modern Studies", "department": "Arts"},
    {"subject": "Philosophy", "department": "Arts"},
    {"subject": "Politics", "department": "Arts"},
    {"subject": "Accounting", "department": "Business"},
    {"subject": "Administration", "department": "Business"},
    {"subject": "Business Studies", "department": "Business"},
    {"subject": "Economics", "department": "Business"},
    {"subject": "Biology", "department": "Science"},
    {"subject": "Chemistry", "department": "Science"},
    {"subject": "Computing", "department": "Science"},
    {"subject": "Mathematics", "department": "Science"},
    {"subject": "Physics", "department": "Science"},
    {"subject": "Zoology", "department": "Science"},
]
