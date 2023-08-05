import string
from functools import wraps


def _filter_chars(data, allowed):
    return "".join(filter(lambda x: x in allowed, data))


def printable():
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return _filter_chars(function(*args, **kwargs), string.printable)
        return wrapper
    return inner_function


def ascii():
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return _filter_chars(function(*args, **kwargs), string.ascii_letters)
        return wrapper
    return inner_function


def ascii_lower():
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return _filter_chars(function(*args, **kwargs), string.ascii_lowercase)
        return wrapper
    return inner_function


def ascii_upper():
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return _filter_chars(function(*args, **kwargs), string.ascii_uppercase)
        return wrapper
    return inner_function


def digits():
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return _filter_chars(function(*args, **kwargs), string.digits)
        return wrapper
    return inner_function
