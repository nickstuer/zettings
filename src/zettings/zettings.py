from __future__ import annotations

from collections.abc import MutableMapping
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Annotated, Any

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
    validate_dictionary,
)


class Zettings(MutableMapping[str, Any]):
    @beartype_wrapper
    @beartype
    def __init__(
        self,
        name: Annotated[str, Is[lambda s: is_exact_regex_match(s, NAME_PATTERN)]],
        defaults: dict | None = None,
        *,
        filepath: Path | None = None,
        ram_only: bool = False,
        auto_reload: bool = True,
        read_only: bool = False,
        save_metadata: bool = True,
    ) -> None:
        """Initialize the settings instance.

        Args:
            name (str): The name of the settings instance. Defaults to None.
            defaults (dict | None): Default values for the settings. Defaults to None.
            filepath (Path | None): An explicit path to the settings file.
             - When None, the Path object will be created using: Path.home() / f".{name}/settings.toml".
             - Not used when `ram_only` is True.
            ram_only (bool, optional): If True, the settings will only be stored in RAM and not saved to disk. Defaults to False.
            auto_reload (bool, optional): Whether to always reload settings from file. Defaults to True.
            read_only (bool, optional): If True, disables writing to the settings file. Defaults to False.
            save_metadata (bool, optional): If True, saves metadata to the settings file. Defaults to True.

        Raises:
            InvalidTypeError: If any argument is of an incorrect type.
            InvalidValueError: If any argument does not match the required format.
            ConflictingParametersError: If `filepath` is set when `ram_only` is True.

        """
        if filepath and ram_only:
            msg = "Cannot set `filepath` when `ram_only` is True."
            raise ConflictingParametersError(msg)
        self.name = name
        self._filepath = filepath if filepath else Path.home() / f"./.{name}/settings.toml"
        self.ram_only = ram_only
        self.lock = Lock()
        self.auto_reload = auto_reload
        self.read_only = read_only
        self.save_metadata = save_metadata
        self._data = {}
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

    @beartype_wrapper
    @beartype
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
            return get_dotted_key(self._data, key)
        except KeyNotFoundError:
            return default

    @beartype_wrapper
    @beartype
    def set(self, key: str, value: (int | float | str | bool | list | dict)) -> None:  # noqa: FBT001, PYI041
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

        set_dotted_key(self._data, key, value)
        self._save()

    def __getitem__(self, key: str) -> Any | None:  # noqa: ANN401
        """Get an item from the configuration by key."""
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Set an item in the configuration by key."""
        self.set(key, value)

    def __repr__(self) -> str:  # noqa: D105
        return f"Settings `{self.name}`. File stored at: {self._filepath}"

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

        del_dotted_key(self._data, key)
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
