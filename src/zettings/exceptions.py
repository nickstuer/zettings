"""Exception classes for the Zettings library.

This module defines a comprehensive hierarchy of custom exceptions used
throughout the Zettings library. All exceptions inherit from the base
ZettingsError class for consistent error handling across the entire library.
"""

from __future__ import annotations

__all__ = [
    "ConflictingParametersError",
    "InvalidKeyError",
    "InvalidValueError",
    "KeyNotFoundError",
    "MappingError",
    "ReadOnlyError",
    "TypeHintError",
    "ZettingsError",
]


_INVALID_KEY_MSG = "Invalid key: '{key}'. Keys must be alphanumeric, underscores, or dashes."
_KEY_NOT_FOUND_MSG = "Key not found: '{key}'."
_MAPPING_ERROR_MSG = "Key '{key}' is expected to be a dictionary but is not."
_READ_ONLY_MSG = "Settings are in read only mode and cannot be modified."
_INVALID_VALUE_MSG = "Invalid value '{value}' for key '{key}'."


class ZettingsError(Exception):
    """Base class for all zettings specific errors."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


class InvalidKeyError(ZettingsError):
    """Raised when a key is invalid."""

    def __init__(self, key: str, *args: object, **kwargs: object) -> None:
        message = _INVALID_KEY_MSG.format(key=key)
        super().__init__(message, *args, **kwargs)
        self.key = key


class KeyNotFoundError(ZettingsError):
    """Raised when a key is not found in the settings file."""

    def __init__(self, key: str, *args: object, **kwargs: object) -> None:
        message = _KEY_NOT_FOUND_MSG.format(key=key)
        super().__init__(message, *args, **kwargs)
        self.key = key


class MappingError(ZettingsError):
    """Raised when a key is expected to be a dictionary but is not."""

    def __init__(self, key: str, *args: object, **kwargs: object) -> None:
        message = _MAPPING_ERROR_MSG.format(key=key)
        super().__init__(message, *args, **kwargs)
        self.key = key


class ReadOnlyError(ZettingsError):
    """Raised when attempting to modify the settings with read only enabled."""

    def __init__(
        self,
        message: str = _READ_ONLY_MSG,
        *args: object,
        **kwargs: object,
    ) -> None:
        super().__init__(message, *args, **kwargs)


class InvalidValueError(ZettingsError):
    """Raised when a value is invalid."""

    def __init__(self, key: str, value: object, *args: object, **kwargs: object) -> None:
        message = _INVALID_VALUE_MSG.format(key=key, value=value)
        super().__init__(message, *args, **kwargs)
        self.key = key
        self.value = value


class TypeHintError(ZettingsError):
    """Raised when a value does not match the expected type hint."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


class ConflictingParametersError(ZettingsError):
    """Raised when conflicting parameters are provided to a function or method."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
