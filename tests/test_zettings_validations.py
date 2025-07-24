from pathlib import Path

import pytest

from zettings import Zettings
from zettings.exceptions import ConflictingParametersError, TypeHintError


@pytest.mark.parametrize(
    ("value", "expected_error"),
    [
        (69, TypeHintError),
        (420.69, TypeHintError),
        ("abc", None),
        (True, TypeHintError),
        (None, TypeHintError),
        ([], TypeHintError),
        ({}, TypeHintError),
        (Path(), TypeHintError),
        ("abc123", None),
        ("ABC", None),
        ("ABC123", None),
        ("abc.123", TypeHintError),
        ("abc-123", None),
        ("abc/123", TypeHintError),
        ("", TypeHintError),
    ],
)
def test_zettings_init_validates_name(value, expected_error, temp_filepath):
    if expected_error:
        with pytest.raises(expected_error):
            _ = Zettings(name=value, filepath=temp_filepath)
    else:
        _ = Zettings(name=value, filepath=temp_filepath)


@pytest.mark.parametrize(
    ("value", "expected_error"),
    [
        (69, TypeHintError),
        (420.69, TypeHintError),
        ("abc", TypeHintError),
        (True, TypeHintError),
        (None, None),
        ([], TypeHintError),
        ({}, None),
        (Path(), TypeHintError),
    ],
)
def test_zettings_init_validates_defaults(test_constants, value, expected_error, temp_filepath):
    if expected_error:
        with pytest.raises(expected_error):
            Zettings(name=test_constants.NAME, filepath=temp_filepath, defaults=value)
    else:
        Zettings(name=test_constants.NAME, filepath=temp_filepath, defaults=value)


def test_zettings_init_validates_test_defaults(test_constants, temp_filepath):
    _ = Zettings(name=test_constants.NAME, filepath=temp_filepath, defaults=test_constants.DEFAULTS_NORMAL)
    _ = Zettings(name=test_constants.NAME, filepath=temp_filepath, defaults=test_constants.DEFAULTS_DOTTED)


@pytest.mark.parametrize(
    ("value", "expected_error"),
    [
        (69, TypeHintError),
        (420.69, TypeHintError),
        ("abc", TypeHintError),
        (True, None),
        (None, TypeHintError),
        ([], TypeHintError),
        ({}, TypeHintError),
        (Path(), TypeHintError),
        (False, None),
    ],
)
@pytest.mark.parametrize(("name"), ["read_only", "auto_reload"])
def test_zettings_init_validates_optional_bools(test_constants, name, value, expected_error, temp_filepath):
    if expected_error:
        with pytest.raises(expected_error):
            Zettings(name=test_constants.NAME, filepath=temp_filepath, **{name: value})
    else:
        Zettings(name=test_constants.NAME, filepath=temp_filepath, **{name: value})


@pytest.mark.parametrize(
    ("value", "expected_error"),
    [
        (69, TypeHintError),
        (420.69, TypeHintError),
        ("abc", TypeHintError),
        (True, TypeHintError),
        (None, None),
        ([], TypeHintError),
        ({}, TypeHintError),
        (Path(), None),
        (False, TypeHintError),
        (Path.home() / ".test-settings/settings.toml", None),
    ],
)
def test_zettings_init_validates_filepath(test_constants, value, expected_error, temp_filepath):
    # ensure read_only is True to avoid file creation
    if expected_error:
        with pytest.raises(expected_error):
            _ = Zettings(name=test_constants.NAME, filepath=value, read_only=True)
    else:
        _ = Zettings(name=test_constants.NAME, filepath=temp_filepath, read_only=True)


@pytest.mark.parametrize(
    ("key", "value", "expected_error"),
    [
        ("int", 69, None),
        ("float", 420.69, None),
        ("string", "value", None),
        ("bool", True, None),
        ("list", [1, 2, 3], None),
        ("dict", {"key": "value"}, None),
        # ("path", Path.home(), None),  # noqa: ERA001
        ("nested_dict", {"nested_key": {"sub_key": "sub_value"}}, None),
        ("empty_list", [], None),
        ("nested_list", [[1, 2, 3], [4, 5, 6], ["a", "b", "c"]], None),
        ("empty_dict", {}, None),
        ("complex", {"list": [1, 2, 3], "dict": {"key": "value"}}, None),
        ("complex_nested", {"outer": {"inner": {"key": "value"}}}, None),
        ("unicode", "こんにちは", None),
        ("emoji", "😊", None),
        (69, 69, TypeHintError),
        (420.69, 420.69, TypeHintError),
        ("abc", "abc", None),
        (True, True, TypeHintError),
        (None, None, TypeHintError),
        ([], [], TypeHintError),
        ({}, {}, TypeHintError),
        (Path(), Path(), TypeHintError),
    ],
)
def test_zettings_validates_get(test_constants, key, value, expected_error, temp_filepath):
    zettings = Zettings(name=test_constants.NAME, filepath=temp_filepath, auto_reload=False, read_only=True)

    if expected_error:
        with pytest.raises(expected_error):
            _ = zettings.get(key)
    else:
        zettings._data[key] = value  # noqa: SLF001
        assert zettings.get(key) == value


@pytest.mark.parametrize(
    ("key", "value", "expected_error"),
    [
        ("int", 69, None),
        ("float", 420.69, None),
        ("string", "value", None),
        ("bool", True, None),
        ("none", None, TypeHintError),
        ("list", [1, 2, 3], None),
        ("dict", {"key": "value"}, None),
        ("path", Path.home(), TypeHintError),
        ("nested_dict", {"nested_key": {"sub_key": "sub_value"}}, None),
        ("empty_list", [], None),
        ("nested_list", [[1, 2, 3], [4, 5, 6], ["a", "b", "c"]], None),
        ("empty_dict", {}, None),
        ("complex", {"list": [1, 2, 3], "dict": {"key": "value"}}, None),
        ("complex_nested", {"outer": {"inner": {"key": "value"}}}, None),
        ("unicode", "こんにちは", None),
        ("emoji", "😊", None),
        (69, 69, TypeHintError),
        (420.69, 420.69, TypeHintError),
        ("abc", "abc", None),
        (True, True, TypeHintError),
        (None, None, TypeHintError),
        ([], [], TypeHintError),
        ({}, {}, TypeHintError),
        (Path(), Path(), TypeHintError),
    ],
)
def test_zettings_validates_set(test_constants, temp_filepath, key, value, expected_error):
    zettings = Zettings(name=test_constants.NAME, filepath=temp_filepath, auto_reload=False)
    if expected_error:
        with pytest.raises(expected_error):
            zettings.set(key, value)
    else:
        zettings.set(key, value)
        assert zettings._data[key] == value  # noqa: SLF001


def test_zettings_auto_reload_is_true_by_default(test_constants, temp_filepath):
    zettings = Zettings(name=test_constants.NAME, filepath=temp_filepath)
    assert zettings.auto_reload is True


def test_zettings_read_only_is_false_by_default(test_constants, temp_filepath):
    zettings = Zettings(name=test_constants.NAME, filepath=temp_filepath)
    assert zettings.read_only is False


def test_zettings_ram_only_is_false_by_default(test_constants, temp_filepath):
    zettings = Zettings(name=test_constants.NAME, filepath=temp_filepath)
    assert zettings.ram_only is False


def test_zettings_init_cannot_set_filepath_when_ram_only(test_constants, temp_filepath):
    with pytest.raises(ConflictingParametersError):
        _ = Zettings(name=test_constants.NAME, filepath=temp_filepath, ram_only=True)


@pytest.mark.parametrize(
    ("key", "value", "expected_error"),
    [
        ("int", 69, None),
        ("float", 420.69, None),
        ("string", "value", None),
        ("bool", True, None),
        ("list", [1, 2, 3], None),
        ("dict", {"key": "value"}, None),
        # ("path", Path.home(), None),  # noqa: ERA001
        ("nested_dict", {"nested_key": {"sub_key": "sub_value"}}, None),
        ("empty_list", [], None),
        ("nested_list", [[1, 2, 3], [4, 5, 6], ["a", "b", "c"]], None),
        ("empty_dict", {}, None),
        ("complex", {"list": [1, 2, 3], "dict": {"key": "value"}}, None),
        ("complex_nested", {"outer": {"inner": {"key": "value"}}}, None),
        ("unicode", "こんにちは", None),
        ("emoji", "😊", None),
        (69, 69, TypeHintError),
        (420.69, 420.69, TypeHintError),
        ("abc", "abc", None),
        (True, True, TypeHintError),
        (None, None, TypeHintError),
        ([], [], TypeHintError),
        ({}, {}, TypeHintError),
        (Path(), Path(), TypeHintError),
    ],
)
def test_zettings_validates_exists(test_constants, key, value, expected_error, temp_filepath):
    zettings = Zettings(name=test_constants.NAME, filepath=temp_filepath, auto_reload=False, read_only=True)

    if expected_error:
        with pytest.raises(expected_error):
            _ = zettings.exists(key)
    else:
        zettings._data[key] = value  # noqa: SLF001
        assert zettings.exists(key)
