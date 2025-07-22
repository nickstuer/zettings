from __future__ import annotations

import re
from typing import Any

from zettings.exceptions import InvalidKeyError, InvalidValueError, KeyNotFoundError, MappingError


def check_for_valid_key(key: str) -> None:
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
    if not bool(re.fullmatch(r"[A-Za-z0-9_-]+", key)):
        raise InvalidKeyError(key)


def validate_dictionary_keys(d: dict) -> None:
    """Validate that all keys in the dictionary are valid.

    Args:
        d (dict): The dictionary to validate.

    Raises:
        InvalidKeyError: If any key in the dictionary is not valid.

    """
    for k, v in d.items():
        for subkey in k.split("."):
            check_for_valid_key(subkey)
        if isinstance(v, dict):
            validate_dictionary_keys_loop(v)


def validate_dictionary_keys_loop(d: dict) -> None:
    """Validate that all keys in the dictionary are valid recursively.

    Args:
        d (dict): The dictionary to validate.

    Raises:
        InvalidKeyError: If any key in the dictionary is not valid.

    """
    for key, value in d.items():
        check_for_valid_key(key)
        if isinstance(value, dict):
            validate_dictionary_keys_loop(value)


def get_nested_value(d: dict, key: str, sep: str = ".") -> Any:  # noqa: ANN401
    """Get a value from a dictionary by key or dotted key notation.

    Args:
        d (dict): The dictionary to search.
        key (str): The key to search for.
        sep (str): The separator to use for nested keys. Defaults to '.'.

    Returns:
        Any: The value found for the key.

    Raises:
        InvalidKeyError: If the key is not valid.
        KeyNotFoundError: If the key is not found in the dictionary.

    """
    validate_dictionary_keys(d)
    keys = key.split(sep)
    for k in keys:
        check_for_valid_key(k)
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            raise KeyNotFoundError(key)

    return d


def set_nested_value(d: dict, key: str, value: Any, sep: str = ".") -> None:  # noqa: ANN401
    """Set a value in a dictionary by key or dotted key notation.

    Args:
        d (dict): The dictionary to modify.
        key (str): The key to set the value for.
        value (Any): The value to set.
        sep (str): The separator to use for nested keys. Defaults to '.'.

    Raises:
        InvalidKeyError: If the key is not valid.
        MappingError: If the key points to a non dictionary value.

    """
    if value is None:
        raise InvalidValueError(key, value)

    validate_dictionary_keys(d)
    keys = key.split(sep)
    for k in keys:
        check_for_valid_key(k)

    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
        if not isinstance(d[k], dict):
            raise MappingError(k)
        d = d[k]

    d[keys[-1]] = value


def delete_nested_key(d: dict, key: str, sep: str = ".") -> None:
    """Delete a key or nested key from a dictionary.

    Args:
        d (dict): The dictionary to modify.
        key (str): The key to delete.
        sep (str): The separator to use for nested keys. Defaults to '.'.

    Raises:
        InvalidKeyError: If the key is not valid.
        KeyNotFoundError: If the key is not found in the dictionary.
        MappingError: If the key points to a non dictionary value.

    """
    validate_dictionary_keys(d)
    keys = key.split(sep)
    for k in keys:
        check_for_valid_key(k)

    for k in keys[:-1]:
        if k not in d:
            raise KeyNotFoundError(key)
        if not isinstance(d[k], dict):
            raise MappingError(k)
        d = d[k]

    if keys[-1] not in d:
        raise KeyNotFoundError(key)
    del d[keys[-1]]
