"""Dictionary utilities for dotted key notation in the Zettings library.

This module provides utility functions for working with nested dictionaries
using dotted key notation (e.g., "parent.child.key"). These functions enable
getting, setting, and deleting values in nested dictionary structures using
string based key paths.
"""

from __future__ import annotations

from typing import Annotated, Any, TypeAlias

from beartype import beartype
from beartype.vale import Is

from zettings.exceptions import KeyNotFoundError, MappingError
from zettings.utils.validation_utils import is_valid_key

__all__ = ["del_dotted_key", "get_dotted_key", "set_dotted_key"]

_KEY_SEPARATOR = "."

# Type aliases for type hinting
ZettingsValue: TypeAlias = int | float | str | bool | list[Any] | dict[str, Any]
ZettingsDict: TypeAlias = dict[str, Any]
ZettingsKey: TypeAlias = Annotated[str, Is[lambda s: is_valid_key(s)]]


@beartype
def get_dotted_key(
    data: ZettingsDict,
    key: ZettingsKey,
) -> object:
    """Get a value from a dictionary using a dotted key notation.

    Args:
        data: The dictionary to search.
        key: The key to retrieve the value for.

    Returns:
        The value associated with the key.

    Raises:
        KeyNotFoundError: If the key is not found in the dictionary.

    """
    for part in key.split(_KEY_SEPARATOR):
        if isinstance(data, dict) and part in data:
            data = data[part]
        else:
            raise KeyNotFoundError(key)

    return data


@beartype
def set_dotted_key(
    data: ZettingsDict,
    key: ZettingsKey,
    value: Annotated[object, Is[lambda v: v is not None]],
) -> None:
    """Set a value from a dictionary using a dotted key notation.

    Args:
        data: The dictionary to modify.
        key: The key to set the value for.
        value: The value to set.

    Raises:
        MappingError: If the key points to a non dictionary value.

    """
    keys = key.split(_KEY_SEPARATOR)
    current_dict = data

    for part in keys[:-1]:
        if part not in current_dict:
            current_dict[part] = {}
        if not isinstance(current_dict[part], dict):
            raise MappingError(part)
        current_dict = current_dict[part]

    current_dict[keys[-1]] = value


@beartype
def del_dotted_key(
    data: ZettingsDict,
    key: ZettingsKey,
) -> None:
    """Delete a dotted key from a dictionary.

    Args:
        data: The dictionary to modify.
        key: The key to delete.

    Raises:
        KeyNotFoundError: If the key is not found in the dictionary.
        MappingError: If the key points to a non dictionary value.

    """
    keys = key.split(_KEY_SEPARATOR)
    current_dict = data

    for part in keys[:-1]:
        if part not in current_dict:
            raise KeyNotFoundError(key)
        if not isinstance(current_dict[part], dict):
            raise MappingError(part)
        current_dict = current_dict[part]

    if keys[-1] not in current_dict:
        raise KeyNotFoundError(key)
    del current_dict[keys[-1]]
