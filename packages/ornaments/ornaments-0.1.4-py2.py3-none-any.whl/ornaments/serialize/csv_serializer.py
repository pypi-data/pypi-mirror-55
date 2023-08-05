from __future__ import unicode_literals
import csv as py_csv
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from functools import wraps


def csv_serializer(field_names=None, header=True):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            rows = function(*args, **kwargs)
            csv_string = StringIO()
            fields = field_names
            if fields is None:
                fields = sorted(rows[1].keys())
            writer = py_csv.DictWriter(csv_string, fieldnames=fields, extrasaction='ignore')
            if header:
                writer.writeheader()
            writer.writerows(rows)
            return csv_string.getvalue()
        return wrapper
    return inner_function
