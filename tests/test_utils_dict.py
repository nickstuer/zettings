import copy

import pytest
from beartype.roar import BeartypeHintViolation

from zettings.exceptions import KeyNotFoundError, MappingError
from zettings.utils.dict_utils import (
    del_dotted_key,
    get_dotted_key,
    set_dotted_key,
)


# fixtures
@pytest.fixture(
    params=[
        {
            "key1": "value1",
            "key2": "value2",
            "key3": {"subkey1": "subvalue1", "subkey2": "subvalue2", "subkey3": {"subsubkey1": "subsubvalue1"}},
            "key4": ["listitem1", "listitem2", "listitem3"],
            "key5": {"subkey1": ["listitem1", "listitem2", "listitem3"], "subkey2": "subvalue2"},
            "key6": "value6",
            "key7": {"subkey1": "subvalue1", "subkey2": "subvalue2", "subkey3": {"subsubkey1": "subsubvalue1"}},
            "key8": True,
            "key9": 69,
            "key10": 3.14,
        }
    ],
)
def sample_dict(request):
    return copy.deepcopy(request.param)


@pytest.fixture(
    params=[
        "nonexistent",
        "key1.nonexistent",
        "key3.nonexistent",
        "key7.subkey3.nonexistent",
        "nonexistent.nonexistent",
    ]
)
def sample_fake_but_valid_keys(request):
    return request.param


# get_dotted_key tests
def test_get_has_typehint_validation():
    with pytest.raises(BeartypeHintViolation):
        get_dotted_key("not a dict", "some.key")


def test_get_validates_key_format():
    with pytest.raises(BeartypeHintViolation):
        get_dotted_key({}, "invalid key")


def test_get_success(sample_dict):
    assert get_dotted_key(sample_dict, "key1") == "value1"
    assert get_dotted_key(sample_dict, "key3.subkey2") == "subvalue2"
    assert get_dotted_key(sample_dict, "key7.subkey3.subsubkey1") == "subsubvalue1"


def test_get_fail(sample_dict, sample_fake_but_valid_keys):
    with pytest.raises(KeyNotFoundError):
        get_dotted_key(sample_dict, sample_fake_but_valid_keys)


# set_dotted_key tests
def test_set_has_typehint_validation():
    with pytest.raises(BeartypeHintViolation):
        set_dotted_key("not a dict", "some.key", "value")


def test_set_validates_key_format():
    with pytest.raises(BeartypeHintViolation):
        set_dotted_key({}, "invalid key", "value")


def test_set_validates_value_is_not_none():
    with pytest.raises(BeartypeHintViolation):
        set_dotted_key({}, "valid.key", None)


def test_set_overwrites_existing_values(sample_dict):
    set_dotted_key(sample_dict, "key1", "new_value1")
    assert get_dotted_key(sample_dict, "key1") == "new_value1"
    set_dotted_key(sample_dict, "key3.subkey2", "new_subvalue2")
    assert get_dotted_key(sample_dict, "key3.subkey2") == "new_subvalue2"
    set_dotted_key(sample_dict, "key7.subkey3.subsubkey1", "new_subsubvalue1")
    assert get_dotted_key(sample_dict, "key7.subkey3.subsubkey1") == "new_subsubvalue1"


def test_set_non_existing_keys(sample_dict):
    set_dotted_key(sample_dict, "new", "new_value")
    assert get_dotted_key(sample_dict, "new") == "new_value"
    set_dotted_key(sample_dict, "key3.new", "new_value")
    assert get_dotted_key(sample_dict, "key3.new") == "new_value"
    set_dotted_key(sample_dict, "key7.subkey3.new", "new_value")
    assert get_dotted_key(sample_dict, "key7.subkey3.new") == "new_value"


def test_set_cannot_overwrite_non_dict_keys(sample_dict):
    with pytest.raises(MappingError):
        set_dotted_key(sample_dict, "key1.new", "new_value")
    with pytest.raises(MappingError):
        set_dotted_key(sample_dict, "key3.subkey2.new", "new_value")
    with pytest.raises(MappingError):
        set_dotted_key(sample_dict, "key7.subkey3.subsubkey1.new", "new_value")


def test_set_creates_missing_keys(sample_dict):
    set_dotted_key(sample_dict, "key3.new.new", "new_value")
    assert get_dotted_key(sample_dict, "key3.new.new") == "new_value"


## del_dotted_key tests
def test_del_has_typehint_validation():
    with pytest.raises(BeartypeHintViolation):
        del_dotted_key("not a dict", "some.key")


def test_del_validates_key_format():
    with pytest.raises(BeartypeHintViolation):
        del_dotted_key({}, "invalid key")


def test_del_success(sample_dict):
    del_dotted_key(sample_dict, "key1")
    assert "key1" not in sample_dict
    del_dotted_key(sample_dict, "key3.subkey2")
    with pytest.raises(KeyNotFoundError):
        get_dotted_key(sample_dict, "key3.subkey2")
    assert get_dotted_key(sample_dict, "key3.subkey1") == "subvalue1"
    assert get_dotted_key(sample_dict, "key3.subkey3") == {"subsubkey1": "subsubvalue1"}


def test_del_fail(sample_dict, sample_fake_but_valid_keys):
    with pytest.raises((KeyNotFoundError, MappingError)):
        del_dotted_key(sample_dict, sample_fake_but_valid_keys)
