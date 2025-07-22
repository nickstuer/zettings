from typing import Any


class ZettingsError(Exception):
    """Base class for all zettings specific errors."""


class InvalidKeyError(ZettingsError):
    """Raised when a key is invalid."""

    def __init__(self, key: str):
        super().__init__(f"Invalid key: '{key}'. Keys must be alphanumeric, underscores, or dashes.")
        self.key = key


class KeyNotFoundError(ZettingsError):
    """Raised when a key is not found in the settings file."""

    def __init__(self, key: str):
        super().__init__(f"Key not found: '{key}'.")
        self.key = key


class MappingError(ZettingsError):
    """Raised when a key is expected to be a dictionary but is not."""

    def __init__(self, key: str):
        super().__init__(f"Key '{key}' is not a dictionary.")
        self.key = key


class ReadOnlyError(ZettingsError):
    """Raised when attempting to modify the settings with read only enabled."""

    def __init__(self, message: str = "Settings are in read only mode and cannot be modified."):
        super().__init__(message)
        self.message = message


class InvalidValueError(ZettingsError):
    """Raised when a value is invalid."""

    def __init__(self, key: str, value: Any):  # noqa: ANN401
        super().__init__(f"Invalid value '{value}' for key '{key}'.")
        self.key = key
        self.value = value
