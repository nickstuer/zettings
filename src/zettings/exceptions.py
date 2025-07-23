from typing import Any


class ZettingsError(Exception):
    """Base class for all zettings specific errors."""

    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)


class InvalidKeyError(ZettingsError):
    """Raised when a key is invalid."""

    def __init__(self, key: str, *args, **kwargs):  # noqa: ANN002, ANN003
        message = f"Invalid key: '{key}'. Keys must be alphanumeric, underscores, or dashes."
        super().__init__(message, *args, **kwargs)
        self.key = key


class KeyNotFoundError(ZettingsError):
    """Raised when a key is not found in the settings file."""

    def __init__(self, key: str, *args, **kwargs):  # noqa: ANN002, ANN003
        message = f"Key not found: '{key}'."
        super().__init__(message, *args, **kwargs)
        self.key = key


class MappingError(ZettingsError):
    """Raised when a key is expected to be a dictionary but is not."""

    def __init__(self, key: str, *args, **kwargs):  # noqa: ANN002, ANN003
        message = f"Key '{key}' is expected to be a dictionary but is not."
        super().__init__(message, *args, **kwargs)
        self.key = key


class ReadOnlyError(ZettingsError):
    """Raised when attempting to modify the settings with read only enabled."""

    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        message: str = ("Settings are in read only mode and cannot be modified.",)
        super().__init__(message, *args, **kwargs)


class InvalidValueError(ZettingsError):
    """Raised when a value is invalid."""

    def __init__(self, key: str, value: Any, *args, **kwargs):  # noqa: ANN002, ANN003, ANN401
        message = f"Invalid value '{value}' for key '{key}'."
        super().__init__(message, *args, **kwargs)
        self.key = key
        self.value = value


class TypeHintError(ZettingsError):
    """Raised when a value does not match the expected type hint."""

    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)


class ConflictingParametersError(ZettingsError):
    """Raised when conflicting parameters are provided to a function or method."""

    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
