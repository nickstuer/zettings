class ZettingsError(Exception):
    """Base class for all zettings specific errors."""


class InvalidKeyFormatError(ZettingsError, KeyError):
    """Raised when a requested key is invalid."""

    def __init__(self, key: str):
        super().__init__(f"Invalid key: '{key}'. Keys must be alphanumeric, underscores, or dashes.")
        self.key = key


class KeyNotFoundError(ZettingsError, KeyError):
    """Raised when a requested key is not found in the settings file."""

    def __init__(self, key: str):
        super().__init__(f"Key not found: '{key}'.")
        self.key = key


class KeyNotADictionaryError(ZettingsError, KeyError):
    """Raised when a key is expected to be a dictionary but is not."""

    def __init__(self, key: str):
        super().__init__(f"Key '{key}' is not a dictionary.")
        self.key = key


class ReadOnlyError(ZettingsError, PermissionError):
    """Raised when attempting to modify the settings with read only enabled."""

    def __init__(self, message: str = "Settings are read only and cannot be modified."):
        super().__init__(message)
        self.message = message
