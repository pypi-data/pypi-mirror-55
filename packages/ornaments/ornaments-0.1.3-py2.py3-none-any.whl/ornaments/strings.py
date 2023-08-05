import string


def printable(f):
    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        return "".join(filter(lambda x: x in string.printable, result))
    return decorated
