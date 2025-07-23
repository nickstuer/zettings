from __future__ import annotations

import re

from zettings.exceptions import InvalidKeyError, InvalidValueError


def is_exact_regex_match(string: str, regex_pattern: str) -> bool:
    """Check if the string matches the exact regex pattern."""
    return bool(re.fullmatch(regex_pattern, string))


def validate_key(key: str) -> None:
    """Check if a key is valid.

    Args:
        key (str): The key to check.

    Raises:
        InvalidKeyError: If the key is not valid.

    A valid key must:
    - Contain only letters, numbers, underscores, or dashes.
    - Not contain spaces or quotes.
    - Not be empty.

    """
    keys = key.split(".")
    for k in keys:
        if not bool(re.fullmatch(r"[A-Za-z0-9_-]+", k)):
            raise InvalidKeyError(key)


def validate_dictionary(d: dict) -> None:
    """Validate that all keys and values in the dictionary are zettings compatible.

    Args:
        d (dict): The dictionary to validate.

    Raises:
        InvalidKeyError: If any key in the dictionary is not valid.
        InvalidValueError: If any value in the dictionary is invalid.

    """
    for k, v in d.items():
        for subkey in k.split("."):
            validate_key(subkey)
        if isinstance(v, dict):
            validate_dictionary_loop(v)
        if v is None:
            raise InvalidValueError(k, v)


def validate_dictionary_loop(d: dict) -> None:
    """Validate that all keys in the dictionary are valid recursively.

    Args:
        d (dict): The dictionary to validate.

    Raises:
        InvalidKeyError: If any key in the dictionary is not valid.

    """
    for key, value in d.items():
        validate_key(key)
        if isinstance(value, dict):
            validate_dictionary_loop(value)
        if value is None:
            raise InvalidValueError(key, value)
