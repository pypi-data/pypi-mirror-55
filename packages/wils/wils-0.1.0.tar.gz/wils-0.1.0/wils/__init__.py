import json
import random
import string


def json_load(_string, _type=None):
    """Load json to specific type."""
    try:
        value = json.loads(_string)
    except (json.JSONDecodeError, TypeError):
        return None if _type is None else _type()
    if _type is None or isinstance(value, _type):
        return value
    return None if _type is None else _type()


def display_microseconds(microseconds: int) -> str:
    """Display microsecond value with unit."""
    if microseconds == 0:
        return '0'
    if microseconds < 1000:
        return '{} μs'.format(microseconds)
    if microseconds < 1000000:
        return '{:.3f} ms'.format(microseconds / 1000)
    return '{:.3f} s'.format(microseconds / 1000000)


def random_string(length=6, chars=string.ascii_uppercase + string.digits):
    """Random string."""
    return ''.join(random.choice(chars) for _ in range(length))


def string_brief(string: str, length: int = 20) -> str:
    """Like CSS eclipse."""
    if not string:
        return ''
    if len(string) <= length:
        return string
    return string[:length] + '...'
