from __future__ import annotations

import re
from typing import Any

from zettings.exceptions import InvalidKeyError, KeyNotFoundError, MappingError


def validate_dictionary(d: dict) -> None:
    has_dict_values = False
    for v in d.values():
        if isinstance(v, dict):
            has_dict_values = True

    if has_dict_values:
        validate_dictionary_keys_loop(d)
    else:
        for k in d:
            keys = k.split(".")
            for sub_k in keys:
                if not is_valid_key(sub_k):
                    raise InvalidKeyError(sub_k)


def validate_dictionary_keys_loop(d: dict) -> None:
    """Validate that all keys in the dictionary are valid."""
    for key, value in d.items():
        if not is_valid_key(key):
            raise InvalidKeyError(key)
        if isinstance(value, dict):
            validate_dictionary_keys_loop(value)


def is_valid_key(key: str) -> bool:
    # Bare keys: a-z, A-Z, 0-9, _, -, no quotes or spaces
    # No support for keys with nested quotes (violation of TOML spec but needed for nested keys)
    return bool(re.fullmatch(r"[A-Za-z0-9_-]+", key))


def set_nested_value(d: dict, key: str, value: Any, sep: str = ".") -> None:  # noqa: ANN401
    """Set a nested value in a dictionary by key."""
    keys = key.split(sep)
    previous_key = None
    previous_dict = {}
    for k in keys[:-1]:
        if not is_valid_key(k):
            raise InvalidKeyError(k)

        if not isinstance(d, dict):
            raise MappingError(k)
        if k not in d:
            d[k] = {}

        previous_dict = d
        previous_key = k
        d = d[k]
    if not is_valid_key(keys[-1]):
        raise InvalidKeyError(keys[-1])

    if previous_key is not None and previous_key not in previous_dict:
        raise KeyNotFoundError(previous_key)
    if previous_key is not None and not isinstance(previous_dict[previous_key], dict):
        raise MappingError(previous_key)

    d[keys[-1]] = value


def get_nested_value(d: dict, key: str, sep: str = ".") -> Any | None:  # noqa: ANN401
    """Get a nested value from a dictionary by key."""
    keys = key.split(sep)
    for k in keys:
        if not is_valid_key(k):
            raise InvalidKeyError(k)
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return None
    return d


def delete_nested_key(d: dict, key: str, sep: str = ".") -> None:
    """Delete a nested key from a dictionary."""
    value = get_nested_value(d, key, sep)
    if value is None:
        raise KeyNotFoundError(key)
    keys = key.split(sep)
    for k in keys:
        if not is_valid_key(k):
            raise InvalidKeyError(k)

        if not isinstance(d, dict):
            raise MappingError(k)
        if keys[-1] in d:
            del d[keys[-1]]
            return

        d = d[k]
