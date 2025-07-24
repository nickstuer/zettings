import shutil
from pathlib import Path
from typing import ClassVar

import pytest

from zettings import Zettings


@pytest.fixture
def temp_filepath(tmpdir_factory: pytest.TempdirFactory):
    temp_dir = str(tmpdir_factory.mktemp("temp"))
    temp_testing_dir = temp_dir + "/testing/settings.toml"
    yield Path(temp_testing_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_homepath(test_constants):
    temp_homepath = Path.home() / f".{test_constants.NAME}/settings.toml"
    yield temp_homepath
    if temp_homepath.exists():
        shutil.rmtree(temp_homepath.parent)


@pytest.fixture
def temp_zettings(temp_filepath, test_constants):
    return Zettings(name=test_constants.NAME, filepath=temp_filepath, save_metadata=False)


class TestConstants:
    NAME: ClassVar[str] = "test_settings"

    DEFAULTS_NORMAL: ClassVar[dict] = {
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

    DEFAULTS_DOTTED: ClassVar[dict] = {
        "key1": "value1",
        "key2": "value2",
        "key3.subkey1": "subvalue1",
        "key3.subkey2": "subvalue2",
        "key3.subkey3.subsubkey1": "subsubvalue1",
        "key4": ["listitem1", "listitem2", "listitem3"],
        "key5.subkey1": ["listitem1", "listitem2", "listitem3"],
        "key5.subkey2": "subvalue2",
        "key6": "value6",
        "key7.subkey1": "subvalue1",
        "key7.subkey2": "subvalue2",
        "key7.subkey3.subsubkey1": "subsubvalue1",
        "key8": True,
        "key9": 69,
        "key10": 3.14,
    }


@pytest.fixture(scope="session")
def test_constants() -> TestConstants:
    return TestConstants()
