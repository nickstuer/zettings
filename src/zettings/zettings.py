"""Core settings functionality for the Zettings library.

This module contains the main Zettings class that provides a comprehensive
settings management system. It implements the MutableMapping protocol
to expose settings as standard Python dictionaries while providing persistent
storage to TOML files with advanced features like auto_reload, read_only mode,
thread safety, and dotted key notation for nested settings.
"""

from __future__ import annotations

from collections.abc import Iterator, MutableMapping
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Annotated, Any, Final, TypeAlias

import toml
from beartype import beartype
from beartype.vale import Is

from zettings.constants import CREATED_KEY, NAME_PATTERN, NOTICE, NOTICE_KEY, UPDATED_KEY
from zettings.decorators import beartype_wrapper
from zettings.exceptions import ConflictingParametersError, KeyNotFoundError, ReadOnlyError
from zettings.utils.dict_utils import (
    del_dotted_key,
    get_dotted_key,
    set_dotted_key,
)
from zettings.utils.validation_utils import (
    is_exact_regex_match,
    is_valid_key,
    validate_dictionary,
)

# Type aliases for type hinting
ZettingsValue: TypeAlias = int | float | str | bool | list[Any] | dict[str, Any]
ZettingsDict: TypeAlias = dict[str, Any]
ZettingsKey: TypeAlias = Annotated[str, Is[lambda s: is_valid_key(s)]]


class Zettings(MutableMapping[str, Any]):
    """A configuration/settings utility that that exposes project settings as standard Python dictionaries."""

    _DEFAULT_FILEPATH_TEMPLATE: Final[str] = "./.{name}/settings.toml"

    @beartype_wrapper
    @beartype
    def __init__(
        self,
        name: Annotated[str, Is[lambda s: is_exact_regex_match(s, NAME_PATTERN)]],
        defaults: ZettingsDict | None = None,
        *,
        filepath: Path | None = None,
        ram_only: bool = False,
        auto_reload: bool = True,
        read_only: bool = False,
        save_metadata: bool = True,
    ) -> None:
        """Initialize the settings instance.

        Args:
            name: The name of the settings instance.
            defaults: Default values for the settings. Defaults to None.
            filepath: An explicit path to the settings file.
                When None, the Path object will be created using: Path.home() / f".{name}/settings.toml".
                Not used when `ram_only` is True.
            ram_only: If True, the settings will only be stored in RAM and not saved to disk. Defaults to False.
            auto_reload: If True, the settings will be reloaded on each get/set. Defaults to True.
            read_only: If True, disables writing to the settings file. Defaults to False.
            save_metadata: If True, saves metadata to the settings file. Defaults to True.

        Raises:
            InvalidTypeError: If any argument is of an incorrect type.
            InvalidValueError: If any argument does not match the required format.
            ConflictingParametersError: If `filepath` is True and `ram_only` is True.

        """
        if filepath and ram_only:
            msg = "Cannot set `filepath` when `ram_only` is True."
            raise ConflictingParametersError(msg)

        self.name: str = name
        self._filepath: Path = (
            filepath
            if filepath
            else Path.home() / self._DEFAULT_FILEPATH_TEMPLATE.format(name=name)
            if not ram_only
            else None
        )
        self.ram_only: bool = ram_only
        self.lock: Lock = Lock()
        self.auto_reload: bool = auto_reload
        self.read_only: bool = read_only
        self.save_metadata: bool = save_metadata
        self._data: ZettingsDict = {}
        if defaults is None:
            defaults = {}

        validate_dictionary(defaults)
        if not self.read_only:
            self._initialize_file()
            self._initialize_defaults(defaults)

    @property
    def filepath(self) -> Path:
        """Return the path to the settings file."""
        return self._filepath

    def _initialize_file(self) -> None:
        """Initialize the settings file with metadata values and sets defaults for missing keys."""
        if self.ram_only:
            return

        if self._filepath.exists():
            return
        self._filepath.parent.mkdir(parents=True, exist_ok=True)

        if self.save_metadata:
            set_dotted_key(self._data, NOTICE_KEY, NOTICE)
            set_dotted_key(self._data, CREATED_KEY, datetime.now(tz=timezone.utc).isoformat())
            set_dotted_key(self._data, UPDATED_KEY, datetime.now(tz=timezone.utc).isoformat())
        self._save()

    def _initialize_defaults(self, d: ZettingsDict, parent_key: str = "") -> None:
        """Recursively set default values for missing keys in the settings dictionary."""
        for key, value in d.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if not self.exists(full_key):
                self.set(full_key, value)

    def _save(self) -> None:
        """Save the settings to the file and update the updated timestamp."""
        if self.save_metadata:
            set_dotted_key(self._data, UPDATED_KEY, datetime.now(tz=timezone.utc).isoformat())

        if self.ram_only:
            return
        with self.lock, Path.open(self._filepath, mode="w", encoding="utf-8") as f:
            toml.dump(self._data, f)

    def _load(self) -> None:
        """Load the settings from the file."""
        if self.ram_only:
            return
        with self.lock, Path.open(self._filepath, mode="r", encoding="utf-8") as f:
            self._data = toml.load(f)

    @beartype_wrapper
    @beartype
    def exists(self, key: str) -> bool:
        """Check if a key exists in the settings.

        Args:
            key: The key to check for existence.

        Returns:
            True if the key exists, False otherwise.

        """
        if self.auto_reload:
            self._load()

        return self.get(key) is not None

    @beartype_wrapper
    @beartype
    def get(self, key: str, fallback: ZettingsValue | None = None) -> ZettingsValue | None:
        """Return a value from the settings by key.

        Args:
            key: The key to return a value from.
            fallback: The fallback value to return if the key does not exist. Defaults to None.

        Returns:
            The value associated with the key, or `fallback` if the key does not exist.

        Raises:
            KeyNotValidError: If the key is not valid.

        """
        if self.auto_reload:
            self._load()

        try:
            return get_dotted_key(self._data, key)
        except KeyNotFoundError:
            return fallback

    @beartype_wrapper
    @beartype
    def set(self, key: str, value: ZettingsValue) -> None:
        """Set a value in the settings by key.

        Args:
            key: The key to store the value under.
            value: The value to set for the key.

        Raises:
            InvalidKeyError: If the key is not valid.
            InvalidValueError: If the value is None.
            MappingError: If the key points to a non dictionary value.

        """
        if self.read_only:
            raise ReadOnlyError

        if self.auto_reload:
            self._load()

        set_dotted_key(self._data, key, value)
        self._save()

    def __getitem__(self, key: str) -> ZettingsValue | None:
        """Get an item from the settings by key."""
        return self.get(key)

    def __setitem__(self, key: str, value: ZettingsValue) -> None:
        """Set an item in the settings by key."""
        self.set(key, value)

    def __repr__(self) -> str:
        """Return a string representation of the Zettings instance."""
        return f"Settings `{self.name}`. File stored at: {self._filepath}"

    def __delitem__(self, key: str) -> None:
        """Delete an item from the settings by key.

        Args:
            key: The key to delete from the settings file.

        Raises:
            ReadOnlyError: If the settings are read only.

        """
        if self.read_only:
            error_message = "Settings are read only and cannot be modified."
            raise ReadOnlyError(error_message)

        if self.auto_reload:
            self._load()

        del_dotted_key(self._data, key)
        self._save()

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the keys in the settings."""
        if self.auto_reload:
            self._load()
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of items in the settings."""
        if self.auto_reload:
            self._load()

        return self._count(self._data)

    def _count(self, d: ZettingsDict) -> int:
        """Count the number of items in a nested dictionary."""
        total = 0
        for value in d.values():
            total += 1
            if isinstance(value, dict):
                total += self._count(value)
        return total
