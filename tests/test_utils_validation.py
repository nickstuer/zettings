import pytest

from zettings.exceptions import InvalidKeyError, InvalidValueError
from zettings.utils.validation_utils import (
    validate_dictionary,
    validate_key,
)


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("DEBUG", True),
        ("debug-mode", True),
        ("db.host", True),
        ('"db.host"', False),
        ("db host", False),
        ("'db host'", False),
        ('"bad"key"', False),
        ("'bad'key'", False),
        ("simple_key", True),
        ("123key", True),
        ("key-with-dash", True),
        ("key with space", False),
        ('"key with space in nested quotes"', False),
        ('"key with \n newline"', False),
        ("'single'quote'", False),
        ("'valid key'", False),
        ('"valid key"', False),
        ('""', False),
        ("", False),
        ("{}", False),
    ],
)
def test_is_valid_key(key, expected):
    if expected:
        validate_key(key)
    else:
        with pytest.raises(InvalidKeyError):
            validate_key(key)


def test_validate_dictionary():
    valid_dict = {"a": {"b": {"c": 1}}}
    valid_dict2 = {"a": True}

    invalid_dict = {"a": {"b": {"c": 1, "d+": 2}}}
    invalid_dict2 = {"a": True, "b+": True}
    invalid_dict3 = {"a": {"b": {"c": 1, "d": {"e": None}}}}
    invalid_dict4 = {"a": True, "b": None}

    validate_dictionary(valid_dict)
    validate_dictionary(valid_dict2)
    with pytest.raises(InvalidKeyError):
        validate_dictionary(invalid_dict)
    with pytest.raises(InvalidKeyError):
        validate_dictionary(invalid_dict2)
    with pytest.raises(InvalidValueError):
        validate_dictionary(invalid_dict3)
    with pytest.raises(InvalidValueError):
        validate_dictionary(invalid_dict4)
