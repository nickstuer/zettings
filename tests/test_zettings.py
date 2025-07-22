from pathlib import Path

import pytest
import toml

from tests.constants import DEFAULTS_NESTED, DEFAULTS_NORMAL, NAME
from zettings import Zettings, constants
from zettings.exceptions import (
    InvalidKeyError,
    MappingError,
    ReadOnlyError,
)


def test_zettings_initializes_without_defaults(temp_filepath):
    zettings = Zettings(name=NAME, filepath=temp_filepath)
    assert zettings.name == NAME
    assert zettings.filepath == temp_filepath
    assert zettings.auto_reload is True
    assert zettings.read_only is False
    assert zettings.get("metadata.notice") == constants.NOTICE
    assert zettings.get("metadata.created") is not None
    assert zettings.get("metadata.updated") is not None
    assert len(zettings) == 4


def test_zettings_initializes_with_defaults_normal(temp_filepath):
    zettings = Zettings(name=NAME, filepath=temp_filepath, defaults=DEFAULTS_NORMAL)
    assert zettings.name == NAME
    assert zettings.filepath == temp_filepath
    assert zettings.auto_reload is True
    assert zettings.read_only is False
    assert zettings.get("metadata.notice") == constants.NOTICE
    assert zettings.get("metadata.created") is not None
    assert zettings.get("metadata.updated") is not None
    assert len(zettings) == 24


def test_zettings_initializes_with_defaults_nested(temp_filepath):
    zettings = Zettings(name=NAME, filepath=temp_filepath, defaults=DEFAULTS_NESTED)
    assert zettings.name == NAME
    assert zettings.filepath == temp_filepath
    assert zettings.auto_reload is True
    assert zettings.read_only is False
    assert zettings.get("metadata.notice") == constants.NOTICE
    assert zettings.get("metadata.created") is not None
    assert zettings.get("metadata.updated") is not None
    assert len(zettings) == 24


def test_zettings_handles_missing_keys_from_defaults_normal(temp_filepath):
    defaults = DEFAULTS_NORMAL.copy()
    defaults["foo"] = {"bar": "baz"}
    zettings = Zettings(name=NAME, filepath=temp_filepath, defaults=defaults)

    assert zettings.get("foo") == {"bar": "baz"}
    for k, v in defaults.items():
        if isinstance(v, dict):
            assert zettings.get(k) == v
            for subkey, subvalue in v.items():
                assert zettings.get(f"{k}.{subkey}") == subvalue
        assert zettings.get(k) == v


def test_zettings_handles_missing_keys_from_defaults_nested(temp_filepath):
    defaults = DEFAULTS_NESTED.copy()
    defaults["foo"] = "bar"
    zettings = Zettings(name=NAME, filepath=temp_filepath, defaults=defaults)

    assert zettings.get("foo") == "bar"
    for k, v in defaults.items():
        assert zettings.get(k) == v


def test_zettings_set_overrides_existing_value(temp_zettings):
    temp_zettings.set("foo", "bar")
    assert temp_zettings.get("foo") == "bar"

    temp_zettings.set("foo", "baz")
    assert temp_zettings.get("foo") == "baz"


def test_zettings_get_returns_none_for_non_existent_key(temp_zettings):
    assert temp_zettings.get("non_existent_key") is None


def test_zettings_get_returns_default_value_for_non_existent_key(temp_zettings):
    assert temp_zettings.get("non_existent_key", default="default_value") == "default_value"


def test_zettings_init_creates_parent_directory(temp_filepath):
    parent_dir = temp_filepath.parent

    assert not parent_dir.exists()

    _ = Zettings(name=NAME, filepath=temp_filepath)
    assert parent_dir.exists()


def test_zettings_set_saves_to_file(temp_filepath):
    settings = Zettings(name=NAME, filepath=temp_filepath)

    settings.set("foo", "bar")

    with Path.open(temp_filepath, "r") as f:
        data = toml.load(f)
    assert data["foo"] == "bar"


def test_zettings_get_handles_case_sensitivity(temp_filepath):
    settings = Zettings(name=NAME, filepath=temp_filepath)
    settings["foo"] = "bar"

    assert settings["foo"] == "bar"
    assert settings.get("Foo") is None


def test_zettings_auto_reload_true(temp_filepath):
    settings = Zettings(name=NAME, filepath=temp_filepath, auto_reload=True)
    settings.set("foo", "bar")

    assert settings.get("foo") == "bar"

    with Path.open(temp_filepath, "r") as f:
        data = toml.load(f)
    assert data["foo"] == "bar"
    data["foo"] = "baz"
    with Path.open(temp_filepath, "w") as f:
        toml.dump(data, f)

    assert settings.get("foo") == "baz"


def test_zettings_auto_reload_false(temp_filepath):
    settings = Zettings(name=NAME, filepath=temp_filepath, auto_reload=False)
    settings.set("foo", "bar")

    with Path.open(temp_filepath, "r") as f:
        data = toml.load(f)
    assert data["foo"] == "bar"
    data["foo"] = "baz"
    with Path.open(temp_filepath, "w") as f:
        toml.dump(data, f)

    assert settings.get("foo") == "bar"


def test_zettings_set_fails_when_read_only_true(temp_filepath):
    settings = Zettings(name=NAME, filepath=temp_filepath, read_only=True)

    with pytest.raises(ReadOnlyError):
        settings.set("foo", "bar")


def test_zettings_del_fails_when_read_only_true(temp_filepath):
    settings = Zettings(name=NAME, filepath=temp_filepath, read_only=True)

    with pytest.raises(ReadOnlyError):
        del settings["foo"]


def test_zettings_repr_returns_expected_string(temp_filepath):
    zettings = Zettings(name=NAME, filepath=temp_filepath, defaults=DEFAULTS_NORMAL)
    expected = f"Settings `{zettings.name}`. File stored at: {temp_filepath}"
    assert repr(zettings) == expected


def test_zettings_stores_settings_in_home_directory_if_no_filepath(temp_homepath):
    _ = Zettings(name=NAME)
    assert temp_homepath.exists()


def test_settings_iter_(temp_filepath):
    zettings = Zettings(name=NAME, filepath=temp_filepath, save_metadata=False, auto_reload=False)
    keys = list(zettings)
    assert len(keys) == 0

    zettings._data["foo"] = "bar"  # noqa: SLF001
    zettings._data["baz"] = {"qux": "quux"}  # noqa: SLF001
    keys = list(zettings)

    assert len(keys) == 2
    assert len(zettings) == 3


def test_zettings_del(temp_filepath):
    zettings = Zettings(name=NAME, filepath=temp_filepath)

    zettings.set("newkey", "newkeyvalue")
    assert zettings.get("newkey") == "newkeyvalue"
    del zettings["newkey"]
    assert zettings.get("newkey") is None

    zettings.set("nested.key", "nested_value")
    zettings.set("nested.another_key", "another_value")
    assert zettings.get("nested.key") == "nested_value"
    assert zettings.get("nested.another_key") == "another_value"

    del zettings["nested.key"]
    assert zettings.get("nested.key") is None
    assert zettings.get("nested.another_key") == "another_value"

    zettings.set("nested.key", "nested_value")
    zettings.set("nested.another_key", "another_value")
    assert zettings.get("nested.key") == "nested_value"
    assert zettings.get("nested.another_key") == "another_value"
    del zettings["nested.another_key"]
    assert zettings.get("nested.key") == "nested_value"
    assert zettings.get("nested.another_key") is None


def test_zettings_delete_with_read_only_true(temp_filepath):
    zettings = Zettings(name=NAME, filepath=temp_filepath, save_metadata=False)
    zettings.set("foo", "bar")

    zettings.read_only = True
    with pytest.raises(ReadOnlyError):
        del zettings["foo"]

    assert zettings.get("foo") == "bar"


def test_get_with_duplicate_keynames(temp_filepath):
    defaults = {
        "key1.test": "value1",
        "key1.subkey.subsubkey": "value2",
        "key2.test": "value3",
        "key2.subkey.subsubkey": "value4",
        "key3.test": "value5",
        "key3.subkey.subsubkey": "value6",
    }

    settings = Zettings(name=NAME, filepath=temp_filepath, defaults=defaults)

    assert settings.get("key1.test") == "value1"
    assert settings.get("key1.subkey.subsubkey") == "value2"
    assert settings.get("key2.test") == "value3"
    assert settings.get("key2.subkey.subsubkey") == "value4"
    assert settings.get("key3.test") == "value5"
    assert settings.get("key3.subkey.subsubkey") == "value6"

    settings.set("key1.test", "new_value1")
    settings.set("key1.subkey.subsubkey", "new_value2")
    settings.set("key2.test", "new_value3")
    settings.set("key2.subkey.subsubkey", "new_value4")
    settings.set("key3.test", "new_value5")
    settings.set("key3.subkey.subsubkey", "new_value6")

    assert settings.get("key1.test") == "new_value1"
    assert settings.get("key1.subkey.subsubkey") == "new_value2"
    assert settings.get("key2.test") == "new_value3"
    assert settings.get("key2.subkey.subsubkey") == "new_value4"
    assert settings.get("key3.test") == "new_value5"
    assert settings.get("key3.subkey.subsubkey") == "new_value6"


@pytest.mark.parametrize(
    ("value", "expected_error"),
    [
        (
            {
                "key1.subkey": "value1",
                "key1.subkey.subsubkey": "value2",
            },
            MappingError,
        ),
        (
            {
                "settings": {"name": "MyName", "mood": "MyMood"},
                "dictionary": {
                    "key1'invalid'": "value1",
                    "key2": "value2",
                    "subdictionary": {"key1": "subvalue1", "key2": "subvalue2"},
                },
            },
            InvalidKeyError,
        ),
        (
            {
                "settings.name": "MyName",
                "settings.mood": "MyMood",
                "dictionary.key1": "value1",
                "dictionary.key2": "value2",
                "dictionary.subdict'invalidionary.key1": "subvalue1",
                "dictionary.subdictionary.key2": "subvalue2",
            },
            InvalidKeyError,
        ),
    ],
)
def test_zettings_with_invalid_defaults_format(value, expected_error, temp_filepath):
    with pytest.raises(expected_error):
        _ = Zettings(name=NAME, filepath=temp_filepath, defaults=value)
