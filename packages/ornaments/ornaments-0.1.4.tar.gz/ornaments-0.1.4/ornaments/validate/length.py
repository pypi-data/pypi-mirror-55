from functools import wraps


def length(exact=None, minimum=None, maximum=None):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            value = function(*args, **kwargs)
            value_length = len(value)
            assert any([exact, minimum, maximum]), "Must define one or more of exact, minimum, maximum kwargs"
            if exact is not None:
                assert minimum is None and maximum is None, "Cannot define both exact and minimum/maximum"
                assert value_length == exact, "Invalid length %s != %s" % (value_length, exact)
            else:
                if minimum:
                    assert value_length >= minimum, "Invalid length %s < %s" % (value_length, minimum)
                if maximum:
                    assert value_length <= maximum, "Invalid length %s > %s" % (value_length, maximum)
            return value
        return wrapper
    return inner_function