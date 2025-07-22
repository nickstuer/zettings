from __future__ import annotations

import re
from collections.abc import MutableMapping
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

import toml

from zettings.constants import CREATED_KEY, NOTICE, NOTICE_KEY, UPDATED_KEY
from zettings.exceptions import KeyNotFoundError, ReadOnlyError
from zettings.utils import delete_nested_key, get_nested_value, set_nested_value, validate_dictionary_keys


class Settings(MutableMapping[str, Any]):
    def __init__(
        self,
        filepath: str | Path,
        defaults: dict | None = None,
        *,
        auto_reload: bool = True,
        read_only: bool = False,
    ) -> None:
        """Initialize the settings manager.

        Args:
            filepath (str): Must be in the format '.name/subname.toml'
                name and subname must be alphanumeric, underscores, or dashes.
                the '.' in front of name is optional.
                Examples: 'myproject/settings.toml', '.myproject/settings.toml'.

                When using a str for filepath, the Path object will be created using Path.home() / filepath.
            filepath (Path): An explicit path to the settings file.

            defaults (dict | None, optional): A dictionary of default settings. Defaults to None.
            auto_reload (bool, optional): Whether to always reload settings from file. Defaults to True.
            read_only (bool, optional): If True, disables writing to the settings file. Defaults to False.


        Raises:
            TypeError: If any argument is of an incorrect type.
            ValueError: If filepath (str) does not match the required format.

        """
        # Validate the arguments
        if not isinstance(filepath, (str, Path)):
            error_message = "filepath must be a string or Path"
            raise TypeError(error_message)
        if isinstance(filepath, str):
            if not re.fullmatch(r"^(?:\.)?[a-zA-Z0-9_-]+[\\/]{1}[a-zA-Z0-9_-]+\.toml$", filepath, re.IGNORECASE):
                error_message = (
                    "home_filepath must be alphanumeric, underscores, or dashes in format '.name/subname.toml'"
                )
                raise ValueError(error_message)
            self._filepath = Path.home() / filepath
        else:
            self._filepath = filepath  # assume Path object
        if not isinstance(defaults, (dict, type(None))):
            error_message = "defaults must be a dictionary or None"
            raise TypeError(error_message)
        if not isinstance(auto_reload, bool):
            error_message = "auto_reload must be a boolean"
            raise TypeError(error_message)
        if not isinstance(read_only, bool):
            error_message = "read_only must be a boolean"
            raise TypeError(error_message)

        self.lock = Lock()
        self.auto_reload = auto_reload
        self.read_only = read_only
        self._data = {}
        if defaults is None:
            defaults = {}

        validate_dictionary_keys(defaults)
        if not self.read_only:
            self._initialize_file()
            self._initialize_defaults(defaults)

    def _initialize_file(self) -> None:
        """Initialize the settings file with metadata values and sets defaults for missing keys."""
        if self._filepath.exists():
            return
        self._filepath.parent.mkdir(parents=True, exist_ok=True)
        set_nested_value(self._data, NOTICE_KEY, NOTICE)
        set_nested_value(self._data, CREATED_KEY, datetime.now(tz=timezone.utc).isoformat())
        set_nested_value(self._data, UPDATED_KEY, datetime.now(tz=timezone.utc).isoformat())
        self._save()

    def _initialize_defaults(self, d: dict, parent_key: str = "") -> None:
        """Recursively set default values for missing keys in the settings dictionary."""
        for k, v in d.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            if not self.exists(full_key):
                self.set(full_key, v)
            elif isinstance(v, dict):
                self._initialize_defaults(v, full_key)

    def _save(self) -> None:
        """Save the settings to the file and update the updated timestamp."""
        set_nested_value(self._data, UPDATED_KEY, datetime.now(tz=timezone.utc).isoformat())
        with self.lock, Path.open(self._filepath, mode="w", encoding="utf-8") as f:
            toml.dump(self._data, f)

    def _load(self) -> None:
        """Load the settings from the file."""
        with self.lock, Path.open(self._filepath, mode="r", encoding="utf-8") as f:
            self._data = toml.load(f)

    def exists(self, key: str) -> bool:
        """Check if a key exists in the configuration.

        Args:
        key (str): The key to check for existence.

        Returns:
        bool: True if the key exists, False otherwise.

        """
        if self.auto_reload:
            self._load()

        return self.get(key) is not None

    def get(self, key: str, default: Any = None) -> Any | None:  # noqa: ANN401
        """Return a value from the configuration by key.

        Args:
        key (str): The key to return a value from.
        default (Any | None): The default value to return if the key does not exist. Defaults to None.

        Returns:
        Any | None: The value associated with the key, or `default` if the key does not exist.

        Raises:
        KeyNotValidError: If the key is not valid.

        """
        if self.auto_reload:
            self._load()

        try:
            return get_nested_value(self._data, key)
        except KeyNotFoundError:
            return default

    def set(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Set a value in the configuration by key.

        Args:
        key (str): The key to store the value under.
        value (Any): The value to set for the key.

        Returns:
        None

        Raises:
        InvalidKeyError: If the key is not valid.
        InvalidValueError: If the value is None.
        MappingError: If the key points to a non dictionary value.

        """
        if self.read_only:
            raise ReadOnlyError

        if self.auto_reload:
            self._load()

        set_nested_value(self._data, key, value)
        self._save()

    def __getitem__(self, key: str) -> Any | None:  # noqa: ANN401
        """Get an item from the configuration by key."""
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Set an item in the configuration by key."""
        self.set(key, value)

    def __repr__(self) -> str:  # noqa: D105
        return f"Settings stored at: {self._filepath}"

    def __delitem__(self, key: str) -> None:
        """Delete an item from the settings by key.

        Args:
        key (str): The key to delete from the settings file.

        Returns:
        None

        Raises:
        PermissionError: If the settings are read only.

        """
        if self.read_only:
            error_message = "Settings are read only and cannot be modified."
            raise ReadOnlyError(error_message)

        if self.auto_reload:
            self._load()

        delete_nested_key(self._data, key)
        self._save()

    def __iter__(self):
        """Return an iterator over the keys in the settings."""
        if self.auto_reload:
            self._load()
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of items in the settings."""
        if self.auto_reload:
            self._load()

        return self.count(self._data)

    def count(self, d: dict) -> int:
        """Count the number of items in a nested dictionary."""
        total = 0
        for value in d.values():
            total += 1
            if isinstance(value, dict):
                total += self.count(value)
        return total
