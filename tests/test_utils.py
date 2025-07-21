import shutil
from pathlib import Path

import pytest

from zettings.exceptions import InvalidKeyError, KeyNotFoundError, MappingError
from zettings.utils import delete_nested_key, get_nested_value, is_valid_key, set_nested_value, validate_dictionary


@pytest.fixture
def temp_filepath(tmpdir_factory: pytest.TempdirFactory):
    temp_dir = str(tmpdir_factory.mktemp("temp"))
    temp_testing_dir = Path(temp_dir) / "testing"
    temp_testing_dir.mkdir(parents=True, exist_ok=True)
    yield Path(temp_testing_dir)
    shutil.rmtree(temp_dir)


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("DEBUG", True),
        ("debug-mode", True),
        ("db.host", False),
        ('"db.host"', False),
        ("db host", False),
        ("'db host'", False),
        ('"bad"key"', False),
        ("'bad'key'", False),
        ("simple_key", True),
        ("123key", True),
        ("key-with-dash", True),
        ("key with space", False),
        ('"key with space in nested quotes"', False),
        ('"key with \n newline"', False),
        ("'single'quote'", False),
        ("'valid key'", False),
        ('"valid key"', False),
        ('""', False),
        ("", False),
    ],
)
def test_is_valid_key(key, expected):
    assert is_valid_key(key) == expected


def test_get_nested_invalid_key():
    d = {"a": {"b": {"c": 1}}}
    with pytest.raises(InvalidKeyError):
        get_nested_value(d, "a.b ")
    with pytest.raises(InvalidKeyError):
        get_nested_value(d, "b ")
    with pytest.raises(InvalidKeyError):
        get_nested_value(d, "b .c.d.a")


def test_set_nested_invalid_key():
    d = {"a": {"b": {"c": 1}}}
    with pytest.raises(InvalidKeyError):
        set_nested_value(d, "a.b .c", 2)
    with pytest.raises(InvalidKeyError):
        set_nested_value(d, "b ", 2)
    with pytest.raises(InvalidKeyError):
        set_nested_value(d, "b .c.d.a", 2)
    with pytest.raises(InvalidKeyError):
        set_nested_value(d, "a.b.c ", 2)


@pytest.mark.parametrize(
    ("initial", "key", "value", "expected"),
    [
        ({}, "a.b.c", 1, {"a": {"b": {"c": 1}}}),
        ({"a": {}}, "a.b", 2, {"a": {"b": 2}}),
        ({"a": {"b": 3}}, "a.b", 4, {"a": {"b": 4}}),
        ({}, "x", 5, {"x": 5}),
        ({"a": {"b": {"c": 1}}}, "a.b.d", 6, {"a": {"b": {"c": 1, "d": 6}}}),
    ],
)
def test_set_nested(initial, key, value, expected):
    d = initial.copy()
    set_nested_value(d, key, value)
    assert d == expected


@pytest.mark.parametrize(
    ("d", "key", "expected"),
    [
        ({"a": {"b": {"c": 1}}}, "a.b.c", 1),
        ({"a": {"b": 2}}, "a.b", 2),
        ({"x": 5}, "x", 5),
        ({"a": {"b": {"c": 1}}}, "a.b", {"c": 1}),
        ({"a": {"b": {"c": 1}}}, "a.b.c.d", None),
        ({}, "foo.bar", None),
        ({"a": 1}, "a.b", None),
    ],
)
def test_get_nested(d, key, expected):
    assert get_nested_value(d, key) == expected


def test_set_nested_with_custom_separator():
    d = {}
    set_nested_value(d, "a|b|c", 10, sep="|")
    assert d == {"a": {"b": {"c": 10}}}


def test_get_nested_with_custom_separator():
    d = {"a": {"b": {"c": 42}}}
    assert get_nested_value(d, "a|b|c", sep="|") == 42


def test_set_nested_cannot_overwrite_non_dict():
    d = {"a": 1}

    with pytest.raises(MappingError):
        set_nested_value(d, "a.b", 3)

    with pytest.raises(MappingError):
        set_nested_value(d, "a.b.c", 3)
    assert d == {"a": 1}


def test_get_nested_returns_none_for_non_dict():
    d = {"a": 1}
    assert get_nested_value(d, "a.b") is None


def test_delete_nested_key():
    d = {"a": {"b": {"c": 1}}}
    delete_nested_key(d, "a.b.c")
    assert d == {"a": {"b": {}}}

    d = {"a": {"b": 2}}
    delete_nested_key(d, "a.b")
    assert d == {"a": {}}

    d = {"x": 5}
    delete_nested_key(d, "x")
    assert d == {}


def test_delete_nested_key_invalid():
    d = {"a": {"b": {"c": 1}}}
    with pytest.raises(InvalidKeyError):
        delete_nested_key(d, "a.b.c ")
    with pytest.raises(InvalidKeyError):
        delete_nested_key(d, "b .c.d.a")
    with pytest.raises(InvalidKeyError):
        delete_nested_key(d, "a.b.c ")
    with pytest.raises(KeyNotFoundError):
        delete_nested_key(d, "a.b.c.d.e")


def test_validate_dictionary():
    valid_dict = {"a": {"b": {"c": 1}}}
    valid_dict2 = {"a": True}

    invalid_dict = {"a": {"b": {"c": 1, "d+": 2}}}
    invalid_dict2 = {"a": True, "b+": True}

    validate_dictionary(valid_dict)
    validate_dictionary(valid_dict2)
    with pytest.raises(InvalidKeyError):
        validate_dictionary(invalid_dict)
    with pytest.raises(InvalidKeyError):
        validate_dictionary(invalid_dict2)
