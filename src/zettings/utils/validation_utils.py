"""Validation utilities for the Zettings settings library.

This module provides validation functions for keys, values, and dictionaries
used within the Zettings library. It ensures that settings keys follow
the required naming conventions and that values meet the library's standards.
"""

from __future__ import annotations

import re
from typing import Annotated, Any, TypeAlias

from beartype import beartype
from beartype.vale import Is

from zettings.exceptions import InvalidKeyError, InvalidValueError

__all__ = [
    "is_exact_regex_match",
    "is_valid_key",
    "validate_dictionary",
    "validate_dictionary_loop",
    "validate_key",
]


_VALID_KEY_PATTERN = r"[A-Za-z0-9_-]+"
_KEY_SEPARATOR = "."

# Type aliases for type hinting
ZettingsValue: TypeAlias = int | float | str | bool | list[Any] | dict[str, Any]
ZettingsDict: TypeAlias = dict[str, Any]
ZettingsKey: TypeAlias = Annotated[str, Is[lambda s: is_valid_key(s)]]


@beartype
def is_exact_regex_match(string: str, regex_pattern: str) -> bool:
    """Check if the string matches the exact regex pattern.

    Args:
        string: The string to test against the pattern.
        regex_pattern: The regular expression pattern to match.

    Returns:
        True if the string exactly matches the pattern, False otherwise.

    """
    return bool(re.fullmatch(regex_pattern, string))


@beartype
def is_valid_key(key: str, /) -> bool:
    """Check if a key is valid according to the zettings rules.

    Args:
        key: The key to validate using dotted notation.

    Returns:
        True if the key is valid, False otherwise.

    Note:
        Valid keys contain only letters, numbers, underscores, or dashes.
        Dotted notation is supported for nested keys.

    """
    return all(re.fullmatch(_VALID_KEY_PATTERN, part) for part in key.split(_KEY_SEPARATOR))


@beartype
def validate_key(key: str) -> None:
    """Check if a key is valid and raise an exception if not.

    Args:
        key: The key to validate.

    Raises:
        InvalidKeyError: If the key is not valid.

    Note:
        A valid key must:
        - Contain only letters, numbers, underscores, or dashes
        - Not contain spaces or quotes
        - Not be empty

    """
    key_parts = key.split(_KEY_SEPARATOR)
    for part in key_parts:
        if not re.fullmatch(_VALID_KEY_PATTERN, part):
            raise InvalidKeyError(key)


@beartype
def validate_dictionary(data: ZettingsDict) -> None:
    """Validate that all keys and values in the dictionary are zettings compatible.

    Args:
        data: The dictionary to validate.

    Raises:
        InvalidKeyError: If any key in the dictionary is not valid.
        InvalidValueError: If any value in the dictionary is invalid.

    """
    for key, value in data.items():
        for subkey in key.split(_KEY_SEPARATOR):
            validate_key(subkey)
        if isinstance(value, dict):
            validate_dictionary_loop(value)
        if value is None:
            raise InvalidValueError(key, value)


@beartype
def validate_dictionary_loop(data: ZettingsDict) -> None:
    """Validate that all keys in the dictionary are valid recursively.

    Args:
        data: The dictionary to validate.

    Raises:
        InvalidKeyError: If any key in the dictionary is not valid.
        InvalidValueError: If any value in the dictionary is None.

    """
    for key, value in data.items():
        validate_key(key)
        if isinstance(value, dict):
            validate_dictionary_loop(value)
        if value is None:
            raise InvalidValueError(key, value)
