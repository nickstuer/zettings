from __future__ import annotations

import re
from typing import Any


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
                    error_msg = (
                        f"Invalid key: '{sub_k}'. "
                        "Keys must be alphanumeric, underscores, or dashes, "
                        "and cannot contain spaces or quotes."
                    )
                    raise ValueError(error_msg)


def validate_dictionary_keys_loop(d: dict) -> None:
    """Validate that all keys in the dictionary are valid."""
    for key, value in d.items():
        if not is_valid_key(key):
            error_msg = (
                f"Invalid key: '{key}'. "
                "Keys must be alphanumeric, underscores, or dashes, "
                "and cannot contain spaces or quotes."
            )
            raise ValueError(error_msg)
        if isinstance(value, dict):
            validate_dictionary_keys_loop(value)


def is_valid_key(key: str) -> bool:
    # Bare keys: a-z, A-Z, 0-9, _, -, no quotes or spaces
    # No support for keys with nested quotes
    return bool(re.fullmatch(r"[A-Za-z0-9_-]+", key))


def set_nested_value(d: dict, key: str, value: Any, sep: str = ".") -> None:  # noqa: ANN401
    """Set a nested value in a dictionary by key."""
    keys = key.split(sep)
    for k in keys[:-1]:
        if not is_valid_key(k):
            error_msg = (
                f"Invalid key: '{k}'. "
                "Keys must be alphanumeric, underscores, or dashes, "
                "and cannot contain spaces or quotes."
            )
            raise ValueError(error_msg)

        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    if not is_valid_key(keys[-1]):
        error_msg = (
            f"Invalid key: '{keys[-1]}'. "
            "Keys must be alphanumeric, underscores, or dashes, "
            "and cannot contain spaces or quotes."
        )
        raise ValueError(error_msg)
    d[keys[-1]] = value


def get_nested_value(d: dict, key: str, sep: str = ".") -> Any | None:  # noqa: ANN401
    """Get a nested value from a dictionary by key."""
    keys = key.split(sep)
    for k in keys:
        if not is_valid_key(k):
            error_msg = (
                f"Invalid key: '{k}'. "
                "Keys must be alphanumeric, underscores, or dashes, "
                "and cannot contain spaces or quotes."
            )
            raise ValueError(error_msg)
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return None
    return d
